"""Minimal content-only student and response-privileged teacher for Task30."""
from __future__ import annotations

import math
import os
import random

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


def _validate_dimensions(*values: int) -> None:
    if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in values):
        raise ValueError("model dimensions must be positive integers")


def _validate_dropout(dropout: float) -> None:
    if not math.isfinite(dropout) or dropout < 0.0 or dropout >= 1.0:
        raise ValueError("dropout must be finite and in [0, 1)")


def seed_everything(seed: int) -> None:
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        raise ValueError("seed must be a non-negative integer")
    # Launchers must set this before Python starts for hash-order determinism;
    # recording it here keeps the runtime contract explicit and auditable.
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True)


class ContentOnlyStudent(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, class_count: int, dropout: float) -> None:
        super().__init__()
        _validate_dimensions(input_dim, hidden_dim, class_count)
        if class_count < 2:
            raise ValueError("class_count must be at least two")
        _validate_dropout(dropout)
        self.input_dim = input_dim
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, class_count),
        )

    def logits(self, content_features: torch.Tensor) -> torch.Tensor:
        if (
            content_features.ndim != 2
            or content_features.shape[1] != self.input_dim
            or not bool(torch.isfinite(content_features).all())
        ):
            raise ValueError("invalid content-only student features")
        return self.network(content_features)

    def forward(self, content_features: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.logits(content_features), dim=-1)


class ResponsePrivilegedTeacher(nn.Module):
    def __init__(
        self,
        content_dim: int,
        privileged_dim: int,
        hidden_dim: int,
        class_count: int,
        dropout: float,
    ) -> None:
        super().__init__()
        _validate_dimensions(content_dim, privileged_dim, hidden_dim, class_count)
        if class_count < 2:
            raise ValueError("class_count must be at least two")
        _validate_dropout(dropout)
        self.content_dim = content_dim
        self.privileged_dim = privileged_dim
        self.network = nn.Sequential(
            nn.Linear(content_dim + privileged_dim, hidden_dim),
            nn.Tanh(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, class_count),
        )

    def logits(self, content_features: torch.Tensor, privileged_summary: torch.Tensor) -> torch.Tensor:
        if content_features.ndim != 2 or content_features.shape[1] != self.content_dim:
            raise ValueError("invalid teacher content features")
        if privileged_summary.ndim != 2 or privileged_summary.shape[1] != self.privileged_dim:
            raise ValueError("invalid teacher privileged summary")
        if content_features.shape[0] != privileged_summary.shape[0]:
            raise ValueError("teacher batch size mismatch")
        if not bool(torch.isfinite(content_features).all()) or not bool(torch.isfinite(privileged_summary).all()):
            raise ValueError("teacher features must be finite")
        combined = torch.cat([content_features, privileged_summary], dim=1)
        return self.network(combined)

    def forward(self, content_features: torch.Tensor, privileged_summary: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.logits(content_features, privileged_summary), dim=-1)


def _validate_logits(logits: torch.Tensor, name: str) -> None:
    if logits.ndim != 2 or logits.shape[0] == 0 or logits.shape[1] < 2:
        raise ValueError("{} logits must be a non-empty matrix".format(name))
    if not bool(torch.isfinite(logits).all()):
        raise ValueError("{} logits must be finite".format(name))


def hard_label_loss(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    _validate_logits(logits, "student")
    if labels.ndim != 1 or labels.shape[0] != logits.shape[0]:
        raise ValueError("hard label shape mismatch")
    if labels.dtype != torch.long:
        raise ValueError("hard labels must use torch.long")
    if bool((labels < 0).any()) or bool((labels >= logits.shape[1]).any()):
        raise ValueError("hard label out of range")
    return F.cross_entropy(logits, labels)


def soft_distribution_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    _validate_logits(logits, "student")
    if targets.shape != logits.shape:
        raise ValueError("soft target shape mismatch")
    if not bool(torch.isfinite(targets).all()):
        raise ValueError("soft targets must be finite")
    if bool((targets < 0.0).any()):
        raise ValueError("soft targets must be non-negative")
    expected = torch.ones(targets.shape[0], dtype=targets.dtype, device=targets.device)
    if not bool(torch.allclose(targets.sum(dim=1), expected, rtol=0.0, atol=1e-6)):
        raise ValueError("soft targets must sum to one")
    return -(targets * F.log_softmax(logits, dim=1)).sum(dim=1).mean()


def kd_loss(student_logits: torch.Tensor, teacher_logits: torch.Tensor, temperature: float) -> torch.Tensor:
    _validate_logits(student_logits, "student")
    _validate_logits(teacher_logits, "teacher")
    if student_logits.shape != teacher_logits.shape:
        raise ValueError("student/teacher logit shape mismatch")
    if not math.isfinite(temperature) or temperature <= 0.0:
        raise ValueError("temperature must be finite and positive")
    student_log_probabilities = F.log_softmax(student_logits / temperature, dim=1)
    teacher_probabilities = F.softmax(teacher_logits / temperature, dim=1)
    return F.kl_div(
        student_log_probabilities,
        teacher_probabilities,
        reduction="batchmean",
    ) * (temperature ** 2)
