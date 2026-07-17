"""Minimal frozen-I3D model components for task 20."""
from __future__ import annotations

from dataclasses import dataclass
import os
import random
from typing import Sequence

import numpy as np
import torch
from torch import nn

from csmv_i3d_sequence_protocol import validate_feature_array


def pool_i3d_statistics(sequence: np.ndarray) -> np.ndarray:
    sequence = validate_feature_array(sequence)
    return np.concatenate(
        [sequence.mean(axis=0, dtype=np.float64), sequence.std(axis=0, dtype=np.float64)],
        axis=0,
    ).astype(np.float32)


@dataclass(frozen=True)
class StandardizerState:
    mean: np.ndarray
    scale: np.ndarray


def fit_train_standardizer(features: np.ndarray, split_labels: Sequence[str]) -> StandardizerState:
    features = np.asarray(features, dtype=np.float32)
    if features.ndim != 2 or features.shape[0] == 0 or not np.isfinite(features).all():
        raise ValueError("invalid standardizer features")
    if len(split_labels) != features.shape[0] or any(split != "train" for split in split_labels):
        raise ValueError("standardizer may fit on train only")
    mean = features.mean(axis=0, dtype=np.float64)
    scale = features.std(axis=0, dtype=np.float64)
    scale[scale < 1e-12] = 1.0
    return StandardizerState(mean.astype(np.float32), scale.astype(np.float32))


def apply_standardizer(features: np.ndarray, state: StandardizerState) -> np.ndarray:
    features = np.asarray(features, dtype=np.float32)
    if features.ndim != 2 or features.shape[1:] != state.mean.shape or not np.isfinite(features).all():
        raise ValueError("standardizer feature shape mismatch")
    return ((features - state.mean) / state.scale).astype(np.float32)


def seed_everything(seed: int) -> None:
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class PooledDistributionMLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, class_count: int, dropout: float) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, class_count),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.network(features), dim=-1)


class TemporalAttentionDistributionModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, class_count: int, dropout: float) -> None:
        super().__init__()
        self.projection = nn.Sequential(nn.Linear(input_dim, hidden_dim), nn.Tanh())
        self.attention = nn.Linear(hidden_dim, 1, bias=False)
        self.dropout = nn.Dropout(dropout)
        self.head = nn.Linear(hidden_dim, class_count)

    def forward(self, sequence: torch.Tensor, observed_mask: torch.Tensor) -> torch.Tensor:
        if sequence.ndim != 3 or observed_mask.shape != sequence.shape[:2] or observed_mask.dtype != torch.bool:
            raise ValueError("sequence/mask shape mismatch")
        if not bool(observed_mask.any(dim=1).all()):
            raise ValueError("each sequence requires at least one observed timestep")
        hidden = self.projection(sequence)
        scores = self.attention(hidden).squeeze(-1)
        scores = scores.masked_fill(~observed_mask, torch.finfo(scores.dtype).min)
        weights = torch.softmax(scores, dim=1)
        pooled = torch.sum(hidden * weights.unsqueeze(-1), dim=1)
        return torch.softmax(self.head(self.dropout(pooled)), dim=-1)


def soft_target_cross_entropy(probabilities: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    if probabilities.shape != targets.shape or probabilities.ndim != 2:
        raise ValueError("probability/target shape mismatch")
    if not torch.isfinite(probabilities).all() or not torch.isfinite(targets).all():
        raise ValueError("non-finite loss input")
    return -(targets * torch.log(probabilities.clamp_min(1e-12))).sum(dim=1).mean()
