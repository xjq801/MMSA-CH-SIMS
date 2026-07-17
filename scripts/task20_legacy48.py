"""Leakage-aware utilities for the task-20 native legacy 48-D rerun.

This module intentionally does not make the legacy binary task eligible for the
CSMV distribution-prediction table.  It only provides a reproducible native
compatibility rerun with publisher-disjoint partitions.
"""
from __future__ import annotations

import csv
import hashlib
import math
from collections import Counter
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    f1_score,
    log_loss,
    recall_score,
)


FEATURE_COUNT = 48


@dataclass(frozen=True)
class Legacy48Data:
    features: np.ndarray
    labels: np.ndarray
    row_ids: np.ndarray
    groups: np.ndarray
    report: dict[str, Any]


def _safe_id(value: str, namespace: str = "task20-legacy48-v1") -> str:
    return hashlib.sha256(f"{namespace}|{value}".encode("utf-8")).hexdigest()


def load_legacy48(root: str | Path) -> Legacy48Data:
    """Load 48-D native binary rows without exposing an absolute source path."""
    root = Path(root).expanduser().resolve()
    files = sorted(root.rglob("5*.csv"))
    if not files:
        raise FileNotFoundError("no legacy 5*.csv vector files found")

    features: list[list[float]] = []
    labels: list[int] = []
    row_ids: list[str] = []
    groups: list[str] = []
    rejected: Counter[str] = Counter()
    fixity = hashlib.sha256()

    for path in files:
        relative = path.relative_to(root).as_posix()
        parts = Path(relative).parts
        group = "/".join(parts[:2]) if len(parts) >= 2 else parts[0]
        payload = path.read_bytes()
        fixity.update(relative.encode("utf-8"))
        fixity.update(b"\0")
        fixity.update(hashlib.sha256(payload).digest())
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=";")
            next(reader, None)
            for line_number, row in enumerate(reader, start=2):
                if len(row) < FEATURE_COUNT + 1:
                    rejected["too_few_columns"] += 1
                    continue
                try:
                    values = [float(value) for value in row[:FEATURE_COUNT]]
                except ValueError:
                    rejected["non_numeric_features"] += 1
                    continue
                if not all(math.isfinite(value) for value in values):
                    rejected["non_finite_features"] += 1
                    continue
                label = row[FEATURE_COUNT].strip()
                if label not in {"0", "1"}:
                    rejected["invalid_label"] += 1
                    continue
                raw_row_id = f"{relative}::{line_number}"
                features.append(values)
                labels.append(int(label))
                row_ids.append(_safe_id(raw_row_id))
                groups.append(group)

    if not features:
        raise ValueError("no usable finite 48-D binary rows")
    y = np.asarray(labels, dtype=np.int8)
    report: dict[str, Any] = {
        "dataset_id": "CUC-IGPE-v2@legacy-local",
        "feature_count": FEATURE_COUNT,
        "label_type": "SILVER_BINARY_NATIVE_LEGACY",
        "vector_files": len(files),
        "accepted_rows": len(features),
        "rejected_rows": int(sum(rejected.values())),
        "rejected_by_reason": dict(sorted(rejected.items())),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "publisher_groups": len(set(groups)),
        "asset_composite_sha256": fixity.hexdigest(),
        "source_path_recorded": False,
    }
    return Legacy48Data(
        features=np.asarray(features, dtype=np.float64),
        labels=y,
        row_ids=np.asarray(row_ids, dtype=object),
        groups=np.asarray(groups, dtype=object),
        report=report,
    )


def assign_group_splits(
    groups: Sequence[str],
    *,
    salt: str,
    train_cut: float,
    dev_cut: float,
) -> np.ndarray:
    """Assign an entire publisher group by a deterministic salted hash."""
    if not 0.0 < train_cut < dev_cut < 1.0:
        raise ValueError("split cuts must satisfy 0 < train_cut < dev_cut < 1")
    assignment: dict[str, str] = {}
    for group in sorted(set(str(item) for item in groups)):
        digest = hashlib.sha256(f"{salt}|{group}".encode("utf-8")).digest()
        unit = int.from_bytes(digest[:8], "big") / float(2**64)
        assignment[group] = "train" if unit < train_cut else ("dev" if unit < dev_cut else "test")
    return np.asarray([assignment[str(group)] for group in groups], dtype=object)


def validate_split_contract(labels: np.ndarray, groups: np.ndarray, splits: np.ndarray) -> dict[str, Any]:
    expected = {"train", "dev", "test"}
    actual = set(splits.tolist())
    if actual != expected:
        raise ValueError(f"all train/dev/test splits are required; got {sorted(actual)}")
    group_sets = {split: set(groups[splits == split].tolist()) for split in expected}
    if any(group_sets[a] & group_sets[b] for a, b in (("train", "dev"), ("train", "test"), ("dev", "test"))):
        raise ValueError("publisher groups cross split boundaries")
    summary: dict[str, Any] = {}
    for split in ("train", "dev", "test"):
        y = labels[splits == split]
        if set(y.tolist()) != {0, 1}:
            raise ValueError(f"split {split} does not contain both binary classes")
        summary[split] = {
            "rows": int(len(y)),
            "groups": len(group_sets[split]),
            "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        }
    return summary


def expand_grid(space: Mapping[str, Sequence[Any]]) -> list[dict[str, Any]]:
    keys = list(space)
    return [dict(zip(keys, values)) for values in product(*(space[key] for key in keys))]


def build_split_manifest(row_ids: np.ndarray, groups: np.ndarray, splits: np.ndarray) -> dict[str, Any]:
    if not (len(row_ids) == len(groups) == len(splits)):
        raise ValueError("split manifest arrays must align")
    rows = [
        {
            "sample_id": str(row_id),
            "group_id": _safe_id(str(group), namespace="task20-legacy48-group-v1"),
            "split": str(split),
        }
        for row_id, group, split in zip(row_ids, groups, splits)
    ]
    return {
        "schema_version": "task20-legacy48-split-manifest-v1",
        "sample_ids_are_one_way_hashes": True,
        "group_ids_are_one_way_hashes": True,
        "rows": rows,
    }


def binary_metrics(labels: np.ndarray, positive_probabilities: np.ndarray) -> dict[str, float]:
    labels = np.asarray(labels, dtype=np.int64).reshape(-1)
    probabilities = np.clip(np.asarray(positive_probabilities, dtype=float).reshape(-1), 1e-7, 1.0 - 1e-7)
    if len(labels) != len(probabilities):
        raise ValueError("labels and probabilities must align")
    predictions = (probabilities >= 0.5).astype(np.int64)
    return {
        "macro_f1": float(f1_score(labels, predictions, average="macro", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, predictions)),
        "auprc": float(average_precision_score(labels, probabilities)),
        "positive_recall": float(recall_score(labels, predictions, zero_division=0)),
        "accuracy": float(accuracy_score(labels, predictions)),
        "log_loss": float(log_loss(labels, np.column_stack([1.0 - probabilities, probabilities]), labels=[0, 1])),
        "brier_score": float(brier_score_loss(labels, probabilities)),
    }


def _selection_key(trial: Mapping[str, Any]) -> tuple[Any, ...]:
    metrics = trial["dev_metrics"]
    return (
        -float(metrics["macro_f1"]),
        -float(metrics["balanced_accuracy"]),
        float(metrics["log_loss"]),
        float(trial.get("complexity", math.inf)),
        str(trial["trial_id"]),
    )


def select_trial(trials: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not trials:
        raise ValueError("at least one dev trial is required")
    return min(trials, key=_selection_key)


def tune_then_test(
    parameter_trials: Iterable[Mapping[str, Any]],
    *,
    train_trial: Callable[[Mapping[str, Any]], Any],
    dev_evaluator: Callable[[Any], Mapping[str, float]],
    test_evaluator: Callable[[Any], Mapping[str, float]],
    complexity: Callable[[Mapping[str, Any], Any], float],
) -> dict[str, Any]:
    """Tune exclusively on dev and invoke the isolated test evaluator once."""
    trial_rows: list[dict[str, Any]] = []
    selected_model: Any = None
    selected_id: str | None = None
    for index, params in enumerate(parameter_trials):
        model = train_trial(params)
        row = {
            "trial_id": f"trial-{index:02d}",
            "params": dict(params),
            "dev_metrics": dict(dev_evaluator(model)),
            "complexity": float(complexity(params, model)),
        }
        trial_rows.append(row)
        best = select_trial(trial_rows)
        if best["trial_id"] == row["trial_id"]:
            selected_model = model
            selected_id = row["trial_id"]
    if selected_model is None or selected_id is None:
        raise ValueError("at least one parameter trial is required")
    selected = next(row for row in trial_rows if row["trial_id"] == selected_id)
    return {
        "trials": trial_rows,
        "selected": selected,
        "test_metrics": dict(test_evaluator(selected_model)),
        "test_evaluation_calls": 1,
        "selected_model": selected_model,
    }
