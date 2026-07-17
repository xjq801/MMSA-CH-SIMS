"""Leakage-guarded training helpers for task 20 pooled frozen features."""
from __future__ import annotations

import copy
from dataclasses import dataclass
import random
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from task20_metrics import evaluate_distribution_predictions
from task20_models import (
    PooledDistributionMLP,
    StandardizerState,
    TemporalAttentionDistributionModel,
    apply_standardizer,
    fit_train_standardizer,
    seed_everything,
    soft_target_cross_entropy,
)
from csmv_i3d_sequence_protocol import (
    collate_full_sequences,
    plan_deterministic_batches,
    validate_feature_array,
)


@dataclass(frozen=True)
class PooledTrialConfig:
    hidden_dim: int
    dropout: float
    learning_rate: float
    max_epochs: int
    patience: int
    batch_size: int


@dataclass(frozen=True)
class TemporalTrialConfig:
    hidden_dim: int
    dropout: float
    learning_rate: float
    max_epochs: int
    patience: int
    max_batch_size: int
    max_padded_steps: int


def _matrix(values: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or not np.isfinite(matrix).all():
        raise ValueError("invalid {} matrix".format(name))
    return matrix


def train_pooled_trial(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    fit_split_labels: Sequence[str],
    dev_features: np.ndarray,
    dev_targets: np.ndarray,
    config: PooledTrialConfig,
    seed: int,
    device: str,
) -> Dict[str, object]:
    train_features = _matrix(train_features, "train feature")
    train_targets = _matrix(train_targets, "train target")
    dev_features = _matrix(dev_features, "dev feature")
    dev_targets = _matrix(dev_targets, "dev target")
    if train_features.shape[0] != train_targets.shape[0] or dev_features.shape[0] != dev_targets.shape[0]:
        raise ValueError("feature/target row mismatch")
    if train_features.shape[1] != dev_features.shape[1] or train_targets.shape[1] != dev_targets.shape[1]:
        raise ValueError("train/dev dimension mismatch")
    if any(split != "train" for split in fit_split_labels) or len(fit_split_labels) != train_features.shape[0]:
        raise ValueError("model and preprocessing may fit on train only")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    if config.max_epochs < 1 or config.patience < 1 or config.batch_size < 1:
        raise ValueError("training budget must be positive")

    seed_everything(seed)
    torch.use_deterministic_algorithms(True)
    standardizer = fit_train_standardizer(train_features, fit_split_labels)
    train_features = apply_standardizer(train_features, standardizer)
    dev_features = apply_standardizer(dev_features, standardizer)
    torch_device = torch.device(device)
    model = PooledDistributionMLP(
        input_dim=train_features.shape[1],
        hidden_dim=config.hidden_dim,
        class_count=train_targets.shape[1],
        dropout=config.dropout,
    ).to(torch_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    generator = torch.Generator()
    generator.manual_seed(seed)
    loader = DataLoader(
        TensorDataset(torch.from_numpy(train_features), torch.from_numpy(train_targets)),
        batch_size=config.batch_size,
        shuffle=True,
        generator=generator,
        num_workers=0,
    )
    dev_x = torch.from_numpy(dev_features).to(torch_device)
    dev_y = torch.from_numpy(dev_targets).to(torch_device)
    best_js = float("inf")
    best_epoch = 0
    best_state = None
    epochs_without_improvement = 0
    history = []
    for epoch in range(1, config.max_epochs + 1):
        model.train()
        losses = []
        for features_batch, target_batch in loader:
            features_batch = features_batch.to(torch_device)
            target_batch = target_batch.to(torch_device)
            optimizer.zero_grad(set_to_none=True)
            probabilities = model(features_batch)
            loss = soft_target_cross_entropy(probabilities, target_batch)
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        model.eval()
        with torch.no_grad():
            dev_predictions = model(dev_x).cpu().numpy().astype(np.float64)
        dev_metrics = evaluate_distribution_predictions(dev_targets.astype(np.float64), dev_predictions)
        history.append({"epoch": epoch, "train_loss": float(np.mean(losses)), "dev_js": dev_metrics["jensen_shannon_divergence"]})
        if dev_metrics["jensen_shannon_divergence"] < best_js - 1e-12:
            best_js = dev_metrics["jensen_shannon_divergence"]
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
    model.eval()
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
        "device": device,
        "dtype": "float32",
        "amp": False,
    }


def predict_pooled_model(
    model: PooledDistributionMLP,
    standardizer: StandardizerState,
    features: np.ndarray,
    device: str,
) -> np.ndarray:
    features = _matrix(features, "evaluation feature")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    transformed = apply_standardizer(features, standardizer)
    model.eval()
    with torch.no_grad():
        return (
            model(torch.from_numpy(transformed).to(torch.device(device)))
            .cpu()
            .numpy()
            .astype(np.float64)
        )


def _validate_temporal_inputs(
    item_ids: Sequence[str],
    targets: np.ndarray,
    name: str,
) -> Tuple[List[str], np.ndarray]:
    normalized_ids = [str(item_id) for item_id in item_ids]
    matrix = _matrix(targets, "{} target".format(name))
    if not normalized_ids or len(normalized_ids) != matrix.shape[0] or len(set(normalized_ids)) != len(normalized_ids):
        raise ValueError("invalid {} item IDs".format(name))
    return normalized_ids, matrix


def _fit_sequence_standardizer_and_lengths(
    item_ids: Sequence[str],
    split_labels: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
) -> Tuple[StandardizerState, Dict[str, int]]:
    if len(split_labels) != len(item_ids) or any(split != "train" for split in split_labels):
        raise ValueError("sequence standardizer may fit on train only")
    total = None
    squared_total = None
    timestep_count = 0
    lengths: Dict[str, int] = {}
    for item_id in item_ids:
        sequence = validate_feature_array(load_sequence(item_id))
        values = np.asarray(sequence, dtype=np.float64)
        if total is None:
            total = np.zeros(values.shape[1], dtype=np.float64)
            squared_total = np.zeros(values.shape[1], dtype=np.float64)
        total += values.sum(axis=0, dtype=np.float64)
        squared_total += np.square(values, dtype=np.float64).sum(axis=0, dtype=np.float64)
        timestep_count += values.shape[0]
        lengths[item_id] = values.shape[0]
    if total is None or squared_total is None or timestep_count < 1:
        raise ValueError("cannot fit an empty sequence standardizer")
    mean = total / timestep_count
    variance = np.maximum(squared_total / timestep_count - np.square(mean), 0.0)
    scale = np.sqrt(variance)
    scale[scale < 1e-12] = 1.0
    return StandardizerState(mean.astype(np.float32), scale.astype(np.float32)), lengths


def _sequence_lengths(
    item_ids: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
) -> Dict[str, int]:
    return {item_id: int(validate_feature_array(load_sequence(item_id)).shape[0]) for item_id in item_ids}


def _temporal_batches(
    lengths: Dict[str, int],
    config: TemporalTrialConfig,
) -> List[dict]:
    return plan_deterministic_batches(
        lengths,
        max_batch_size=config.max_batch_size,
        max_padded_steps=config.max_padded_steps,
    )


def _collate_temporal_items(
    item_ids: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
    standardizer: StandardizerState,
    max_padded_steps: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    sequences = [apply_standardizer(validate_feature_array(load_sequence(item_id)), standardizer) for item_id in item_ids]
    values, mask, _ = collate_full_sequences(sequences, max_padded_steps=max_padded_steps)
    return torch.from_numpy(values), torch.from_numpy(mask)


def _predict_temporal(
    model: TemporalAttentionDistributionModel,
    item_ids: Sequence[str],
    lengths: Dict[str, int],
    load_sequence: Callable[[str], np.ndarray],
    standardizer: StandardizerState,
    config: TemporalTrialConfig,
    torch_device: torch.device,
    class_count: int,
) -> np.ndarray:
    positions = {item_id: index for index, item_id in enumerate(item_ids)}
    predictions = np.empty((len(item_ids), class_count), dtype=np.float64)
    model.eval()
    with torch.no_grad():
        for batch in _temporal_batches(lengths, config):
            batch_ids = batch["item_ids"]
            values, mask = _collate_temporal_items(
                batch_ids,
                load_sequence,
                standardizer,
                config.max_padded_steps,
            )
            output = model(values.to(torch_device), mask.to(torch_device)).cpu().numpy().astype(np.float64)
            for row, item_id in enumerate(batch_ids):
                predictions[positions[item_id]] = output[row]
    return predictions


def predict_temporal_model(
    model: TemporalAttentionDistributionModel,
    standardizer: StandardizerState,
    item_ids: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
    config: TemporalTrialConfig,
    device: str,
    class_count: int,
) -> np.ndarray:
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    normalized_ids = [str(item_id) for item_id in item_ids]
    if not normalized_ids or len(set(normalized_ids)) != len(normalized_ids):
        raise ValueError("invalid evaluation item IDs")
    return _predict_temporal(
        model,
        normalized_ids,
        _sequence_lengths(normalized_ids, load_sequence),
        load_sequence,
        standardizer,
        config,
        torch.device(device),
        class_count,
    )


def train_temporal_trial(
    train_item_ids: Sequence[str],
    train_targets: np.ndarray,
    fit_split_labels: Sequence[str],
    dev_item_ids: Sequence[str],
    dev_targets: np.ndarray,
    load_sequence: Callable[[str], np.ndarray],
    config: TemporalTrialConfig,
    seed: int,
    device: str,
) -> Dict[str, object]:
    train_item_ids, train_targets = _validate_temporal_inputs(train_item_ids, train_targets, "train")
    dev_item_ids, dev_targets = _validate_temporal_inputs(dev_item_ids, dev_targets, "dev")
    if set(train_item_ids) & set(dev_item_ids):
        raise ValueError("train/dev sequence IDs overlap")
    if train_targets.shape[1] != dev_targets.shape[1]:
        raise ValueError("train/dev target dimension mismatch")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA device is unavailable")
    if (
        config.max_epochs < 1
        or config.patience < 1
        or config.max_batch_size < 1
        or config.max_padded_steps < 1
    ):
        raise ValueError("training budget must be positive")

    seed_everything(seed)
    torch.use_deterministic_algorithms(True)
    standardizer, train_lengths = _fit_sequence_standardizer_and_lengths(
        train_item_ids,
        fit_split_labels,
        load_sequence,
    )
    dev_lengths = _sequence_lengths(dev_item_ids, load_sequence)
    train_target_by_id = {item_id: train_targets[index] for index, item_id in enumerate(train_item_ids)}
    torch_device = torch.device(device)
    model = TemporalAttentionDistributionModel(
        input_dim=standardizer.mean.size,
        hidden_dim=config.hidden_dim,
        class_count=train_targets.shape[1],
        dropout=config.dropout,
    ).to(torch_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    base_batches = _temporal_batches(train_lengths, config)
    best_js = float("inf")
    best_epoch = 0
    best_state = None
    epochs_without_improvement = 0
    history = []
    for epoch in range(1, config.max_epochs + 1):
        model.train()
        batches = list(base_batches)
        random.Random(seed + epoch).shuffle(batches)
        losses = []
        for batch in batches:
            batch_ids = batch["item_ids"]
            values, mask = _collate_temporal_items(
                batch_ids,
                load_sequence,
                standardizer,
                config.max_padded_steps,
            )
            target_batch = torch.from_numpy(np.vstack([train_target_by_id[item_id] for item_id in batch_ids]))
            optimizer.zero_grad(set_to_none=True)
            probabilities = model(values.to(torch_device), mask.to(torch_device))
            loss = soft_target_cross_entropy(probabilities, target_batch.to(torch_device))
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        dev_predictions = _predict_temporal(
            model,
            dev_item_ids,
            dev_lengths,
            load_sequence,
            standardizer,
            config,
            torch_device,
            dev_targets.shape[1],
        )
        dev_metrics = evaluate_distribution_predictions(dev_targets.astype(np.float64), dev_predictions)
        history.append(
            {
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "dev_js": dev_metrics["jensen_shannon_divergence"],
            }
        )
        if dev_metrics["jensen_shannon_divergence"] < best_js - 1e-12:
            best_js = dev_metrics["jensen_shannon_divergence"]
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
    predictions = _predict_temporal(
        model,
        dev_item_ids,
        dev_lengths,
        load_sequence,
        standardizer,
        config,
        torch_device,
        dev_targets.shape[1],
    )
    return {
        "model": model,
        "standardizer": standardizer,
        "dev_predictions": predictions,
        "dev_metrics": evaluate_distribution_predictions(dev_targets.astype(np.float64), predictions),
        "best_epoch": best_epoch,
        "epochs_ran": len(history),
        "history": history,
        "device": device,
        "dtype": "float32",
        "amp": False,
    }
