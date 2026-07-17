"""Small, deterministic T0 baseline kit for task 20."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np

FORBIDDEN_KEYS = {"comment", "comments", "comment_text", "target_comments", "future_retrieval_candidates"}

@dataclass(frozen=True)
class Record:
    item_id: str
    split: str
    target: np.ndarray

def load_records(path: Path, expected_split: str) -> List[Record]:
    records, seen = [], set()
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            raw = json.loads(line)
            leaked = FORBIDDEN_KEYS & set(raw)
            if leaked:
                raise ValueError("forbidden input fields at line {}: {}".format(line_number, sorted(leaked)))
            if raw.get("split") != expected_split:
                raise ValueError("expected {} records, got {} at line {}".format(expected_split, raw.get("split"), line_number))
            item_id = str(raw.get("item_id", ""))
            if not item_id or item_id in seen:
                raise ValueError("missing or duplicate item_id at line {}".format(line_number))
            target = np.asarray(raw.get("target_distribution"), dtype=np.float64)
            if target.ndim != 1 or target.size < 2 or not np.isfinite(target).all() or (target < 0).any() or target.sum() <= 0:
                raise ValueError("invalid target_distribution at line {}".format(line_number))
            records.append(Record(item_id, expected_split, target / target.sum()))
            seen.add(item_id)
    if not records:
        raise ValueError("empty {} input".format(expected_split))
    return records

def _targets(records: Sequence[Record]) -> np.ndarray:
    if not records:
        raise ValueError("cannot fit on empty records")
    if len({record.target.size for record in records}) != 1:
        raise ValueError("inconsistent target dimensions")
    return np.vstack([record.target for record in records])

def fit_train(records: Sequence[Record]) -> Dict[str, np.ndarray]:
    if any(record.split != "train" for record in records):
        raise ValueError("fit scope violation: baselines may fit on train only")
    targets = _targets(records)
    histogram = np.bincount(np.argmax(targets, axis=1), minlength=targets.shape[1]).astype(np.float64)
    return {"overall_mean": targets.mean(axis=0), "empirical_distribution": histogram / histogram.sum(), "majority_class": np.asarray(int(np.argmax(histogram)))}

def predict(model: Dict[str, np.ndarray], baseline: str, count: int) -> np.ndarray:
    if count <= 0:
        raise ValueError("count must be positive")
    if baseline == "majority_class":
        result = np.zeros((count, model["empirical_distribution"].size), dtype=np.float64)
        result[:, int(model["majority_class"])] = 1.0
        return result
    if baseline not in {"overall_mean", "empirical_distribution"}:
        raise ValueError("unknown baseline: {}".format(baseline))
    return np.repeat(model[baseline][None, :], count, axis=0)

def evaluate(targets: np.ndarray, predictions: np.ndarray) -> Dict[str, float]:
    targets, predictions = np.asarray(targets, dtype=np.float64), np.asarray(predictions, dtype=np.float64)
    if targets.shape != predictions.shape or targets.ndim != 2:
        raise ValueError("target/prediction shape mismatch")
    eps = 1e-12
    p, q = np.clip(targets, eps, 1.0), np.clip(predictions, eps, 1.0)
    p, q = p / p.sum(axis=1, keepdims=True), q / q.sum(axis=1, keepdims=True)
    midpoint = 0.5 * (p + q)
    js = 0.5 * np.sum(p * np.log(p / midpoint), axis=1) + 0.5 * np.sum(q * np.log(q / midpoint), axis=1)
    return {"jensen_shannon_divergence": float(js.mean()), "mean_absolute_error": float(np.abs(p - q).mean()), "argmax_accuracy": float((np.argmax(p, axis=1) == np.argmax(q, axis=1)).mean())}
