"""Minimal leak-guarded training loops for Task30 content-only students."""
from __future__ import annotations

import copy
from dataclasses import dataclass
import math
from typing import Dict, Sequence

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from task20_metrics import evaluate_distribution_predictions
from task30_models import (
    ContentOnlyStudent,
    DirichletContentStudent,
    ResponsePrivilegedTeacher,
    dirichlet_distribution_loss,
    hard_label_loss,
    kd_loss,
    seed_everything,
    soft_distribution_loss,
)


@dataclass(frozen=True)
class StudentTrialConfig:
    hidden_dim: int
    dropout: float
    learning_rate: float
    max_epochs: int
    patience: int
    batch_size: int
    head: str
    temperature: float
    kd_weight: float


def _matrix(values: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or not np.isfinite(matrix).all():
        raise ValueError("invalid {} matrix".format(name))
    return matrix


def _targets(values: np.ndarray, name: str) -> np.ndarray:
    matrix = _matrix(values, name)
    if (matrix < 0.0).any() or not np.allclose(matrix.sum(axis=1), 1.0, rtol=0.0, atol=1e-6):
        raise ValueError("{} must contain normalized distributions".format(name))
    return matrix


def _validate_config(config: StudentTrialConfig) -> None:
    if config.head not in {"softmax", "dirichlet"}:
        raise ValueError("unknown student head")
    if any(value < 1 for value in (config.hidden_dim, config.max_epochs, config.patience, config.batch_size)):
        raise ValueError("training dimensions and budgets must be positive")
    if not math.isfinite(config.dropout) or config.dropout < 0.0 or config.dropout >= 1.0:
        raise ValueError("invalid dropout")
    if not math.isfinite(config.learning_rate) or config.learning_rate <= 0.0:
        raise ValueError("invalid learning rate")
    if not math.isfinite(config.temperature) or config.temperature <= 0.0:
        raise ValueError("invalid KD temperature")
    if not math.isfinite(config.kd_weight) or config.kd_weight < 0.0 or config.kd_weight > 1.0:
        raise ValueError("invalid KD weight")


def _fit_standardizer(features: np.ndarray, split_labels: Sequence[str]) -> Dict[str, np.ndarray]:
    if len(split_labels) != features.shape[0] or any(value != "train" for value in split_labels):
        raise ValueError("preprocessing may fit on train only")
    mean = features.mean(axis=0, dtype=np.float64)
    scale = features.std(axis=0, dtype=np.float64)
    scale[scale < 1e-12] = 1.0
    return {"mean": mean.astype(np.float32), "scale": scale.astype(np.float32)}


def _apply_standardizer(features: np.ndarray, state: Dict[str, np.ndarray]) -> np.ndarray:
    if features.shape[1] != state["mean"].size:
        raise ValueError("standardizer feature dimension mismatch")
    transformed = ((features - state["mean"]) / state["scale"]).astype(np.float32)
    if not np.isfinite(transformed).all():
        raise ValueError("standardized features must be finite")
    return transformed


def _gradient_norm(model: torch.nn.Module) -> float:
    squared = 0.0
    for parameter in model.parameters():
        if parameter.grad is None:
            continue
        if not bool(torch.isfinite(parameter.grad).all()):
            raise FloatingPointError("non-finite gradient")
        squared += float(torch.sum(parameter.grad.detach() ** 2).cpu())
    value = math.sqrt(squared)
    if not math.isfinite(value):
        raise FloatingPointError("non-finite gradient norm")
    return value


def train_student_trial(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    fit_split_labels: Sequence[str],
    dev_features: np.ndarray,
    dev_targets: np.ndarray,
    supervision: str,
    config: StudentTrialConfig,
    seed: int,
    device: str,
    teacher_train_logits: np.ndarray = None,
) -> Dict[str, object]:
    _validate_config(config)
    if supervision not in {"hard", "soft", "kd"}:
        raise ValueError("unknown supervision")
    train_features = _matrix(train_features, "train feature")
    dev_features = _matrix(dev_features, "dev feature")
    train_targets = _targets(train_targets, "train target")
    dev_targets = _targets(dev_targets, "dev target")
    if train_features.shape[0] != train_targets.shape[0] or dev_features.shape[0] != dev_targets.shape[0]:
        raise ValueError("feature/target row mismatch")
    if train_features.shape[1] != dev_features.shape[1] or train_targets.shape[1] != dev_targets.shape[1]:
        raise ValueError("train/dev dimension mismatch")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    if device not in {"cpu", "cuda"}:
        raise ValueError("device must be cpu or cuda")
    standardizer = _fit_standardizer(train_features, fit_split_labels)
    train_features = _apply_standardizer(train_features, standardizer)
    dev_features = _apply_standardizer(dev_features, standardizer)

    teacher_logits = None
    if supervision == "kd":
        if teacher_train_logits is None:
            raise ValueError("KD requires teacher logits")
        teacher_logits = np.asarray(teacher_train_logits, dtype=np.float32)
        if teacher_logits.shape != train_targets.shape or not np.isfinite(teacher_logits).all():
            raise ValueError("teacher logits must be finite and shape matched")
    elif teacher_train_logits is not None:
        raise ValueError("teacher logits are only valid for KD")

    seed_everything(seed)
    torch_device = torch.device(device)
    model_class = ContentOnlyStudent if config.head == "softmax" else DirichletContentStudent
    model = model_class(
        input_dim=train_features.shape[1],
        hidden_dim=config.hidden_dim,
        class_count=train_targets.shape[1],
        dropout=config.dropout,
    ).to(torch_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    tensors = [torch.from_numpy(train_features), torch.from_numpy(train_targets)]
    if teacher_logits is not None:
        tensors.append(torch.from_numpy(teacher_logits))
    generator = torch.Generator()
    generator.manual_seed(seed)
    loader = DataLoader(
        TensorDataset(*tensors),
        batch_size=config.batch_size,
        shuffle=True,
        generator=generator,
        num_workers=0,
    )
    dev_x = torch.from_numpy(dev_features).to(torch_device)
    best_js = float("inf")
    best_epoch = 0
    best_state = None
    epochs_without_improvement = 0
    history = []
    for epoch in range(1, config.max_epochs + 1):
        model.train()
        losses = []
        max_gradient_norm = 0.0
        for batch in loader:
            features_batch = batch[0].to(torch_device)
            target_batch = batch[1].to(torch_device)
            optimizer.zero_grad(set_to_none=True)
            if config.head == "dirichlet":
                concentration = model.concentration(features_batch)
                loss = dirichlet_distribution_loss(concentration, target_batch)
            else:
                logits = model.logits(features_batch)
                if supervision == "hard":
                    loss = hard_label_loss(logits, target_batch.argmax(dim=1).long())
                else:
                    base_loss = soft_distribution_loss(logits, target_batch)
                    if supervision == "kd":
                        teacher_batch = batch[2].to(torch_device)
                        loss = (1.0 - config.kd_weight) * base_loss + config.kd_weight * kd_loss(
                            logits, teacher_batch, config.temperature
                        )
                    else:
                        loss = base_loss
            if not bool(torch.isfinite(loss)):
                raise FloatingPointError("non-finite training loss")
            loss.backward()
            max_gradient_norm = max(max_gradient_norm, _gradient_norm(model))
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        model.train(False)
        with torch.no_grad():
            predictions = model(dev_x).cpu().numpy().astype(np.float64)
        metrics = evaluate_distribution_predictions(dev_targets.astype(np.float64), predictions)
        history.append(
            {
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "dev_js": metrics["jensen_shannon_divergence"],
                "max_gradient_norm": max_gradient_norm,
            }
        )
        if metrics["jensen_shannon_divergence"] < best_js - 1e-12:
            best_js = metrics["jensen_shannon_divergence"]
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.patience:
                break
    if best_state is None:
        raise RuntimeError("training produced no selectable epoch")
    model.load_state_dict(best_state)
    model.train(False)
    with torch.no_grad():
        predictions = model(dev_x).cpu().numpy().astype(np.float64)
    return {
        "model": model,
        "standardizer": standardizer,
        "dev_predictions": predictions,
        "dev_metrics": evaluate_distribution_predictions(dev_targets.astype(np.float64), predictions),
        "best_epoch": best_epoch,
        "epochs_ran": len(history),
        "history": history,
        "supervision": supervision,
        "head": config.head,
        "device": device,
        "dtype": "float32",
        "amp": False,
    }


def fit_teacher_train_logits(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    fit_split_labels: Sequence[str],
    privileged_features: np.ndarray,
    hidden_dim: int,
    dropout: float,
    learning_rate: float,
    max_epochs: int,
    batch_size: int,
    seed: int,
    device: str,
) -> Dict[str, object]:
    train_features = _matrix(train_features, "teacher train feature")
    train_targets = _targets(train_targets, "teacher train target")
    if train_features.shape[0] != train_targets.shape[0]:
        raise ValueError("teacher feature/target row mismatch")
    if len(fit_split_labels) != train_features.shape[0] or any(value != "train" for value in fit_split_labels):
        raise ValueError("teacher may fit on train only")
    if any(value < 1 for value in (hidden_dim, max_epochs, batch_size)):
        raise ValueError("teacher dimensions and budget must be positive")
    if not math.isfinite(dropout) or dropout < 0.0 or dropout >= 1.0:
        raise ValueError("invalid teacher dropout")
    if not math.isfinite(learning_rate) or learning_rate <= 0.0:
        raise ValueError("invalid teacher learning rate")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    if device not in {"cpu", "cuda"}:
        raise ValueError("device must be cpu or cuda")

    content_state = _fit_standardizer(train_features, fit_split_labels)
    content = _apply_standardizer(train_features, content_state)
    privileged = None
    privileged_state = None
    if privileged_features is not None:
        privileged = np.asarray(privileged_features, dtype=np.float32)
        if (
            privileged.ndim != 2
            or privileged.shape[0] != train_features.shape[0]
            or privileged.shape[1] < 1
            or not np.isfinite(privileged).all()
        ):
            raise ValueError("privileged features must be finite and row aligned")
        privileged_state = _fit_standardizer(privileged, fit_split_labels)
        privileged = _apply_standardizer(privileged, privileged_state)

    seed_everything(seed)
    torch_device = torch.device(device)
    if privileged is None:
        model = ContentOnlyStudent(
            input_dim=content.shape[1], hidden_dim=hidden_dim,
            class_count=train_targets.shape[1], dropout=dropout,
        ).to(torch_device)
        tensors = (torch.from_numpy(content), torch.from_numpy(train_targets))
        teacher_mode = "content_only"
    else:
        model = ResponsePrivilegedTeacher(
            content_dim=content.shape[1], privileged_dim=privileged.shape[1],
            hidden_dim=hidden_dim, class_count=train_targets.shape[1], dropout=dropout,
        ).to(torch_device)
        tensors = (
            torch.from_numpy(content), torch.from_numpy(privileged), torch.from_numpy(train_targets)
        )
        teacher_mode = "train_response_privileged"
    generator = torch.Generator()
    generator.manual_seed(seed)
    loader = DataLoader(
        TensorDataset(*tensors), batch_size=batch_size, shuffle=True,
        generator=generator, num_workers=0,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    history = []
    for epoch in range(1, max_epochs + 1):
        model.train()
        losses = []
        max_gradient_norm = 0.0
        for batch in loader:
            optimizer.zero_grad(set_to_none=True)
            if privileged is None:
                logits = model.logits(batch[0].to(torch_device))
                target = batch[1].to(torch_device)
            else:
                logits = model.logits(batch[0].to(torch_device), batch[1].to(torch_device))
                target = batch[2].to(torch_device)
            loss = soft_distribution_loss(logits, target)
            if not bool(torch.isfinite(loss)):
                raise FloatingPointError("non-finite teacher loss")
            loss.backward()
            max_gradient_norm = max(max_gradient_norm, _gradient_norm(model))
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        history.append(
            {"epoch": epoch, "train_loss": float(np.mean(losses)), "max_gradient_norm": max_gradient_norm}
        )
    model.train(False)
    with torch.no_grad():
        content_tensor = torch.from_numpy(content).to(torch_device)
        if privileged is None:
            logits = model.logits(content_tensor)
        else:
            logits = model.logits(content_tensor, torch.from_numpy(privileged).to(torch_device))
        logits_array = logits.cpu().numpy().astype(np.float64)
        predictions = torch.softmax(logits, dim=1).cpu().numpy().astype(np.float64)
    if not np.isfinite(logits_array).all():
        raise FloatingPointError("teacher logits must be finite")
    return {
        "train_logits": logits_array,
        "train_predictions": predictions,
        "train_metrics": evaluate_distribution_predictions(train_targets.astype(np.float64), predictions),
        "history": history,
        "teacher_mode": teacher_mode,
        "content_standardizer": content_state,
        "privileged_standardizer": privileged_state,
        "device": device,
        "dtype": "float32",
        "amp": False,
    }
