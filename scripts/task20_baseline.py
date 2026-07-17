"""Small, deterministic T0 baseline kit for task 20."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np

from task20_metrics import evaluate_distribution_predictions

FORBIDDEN_KEYS = {"comment", "comments", "comment_text", "target_comments", "future_retrieval_candidates"}

@dataclass(frozen=True)
class Record:
    item_id: str
    split: str
    target: np.ndarray
    topic_id: Optional[str] = None

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

def load_canonical_records(
    path: Path,
    split_scheme: str,
    expected_split: str,
    distribution_field: str,
    class_order: Sequence[str],
) -> List[Record]:
    """Load canonical labels while preserving one frozen split and class order."""
    if not class_order or len(set(class_order)) != len(class_order):
        raise ValueError("class_order must contain unique classes")
    records: List[Record] = []
    seen = set()
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            raw = json.loads(line)
            leaked = FORBIDDEN_KEYS & set(raw)
            if leaked:
                raise ValueError("forbidden input fields at line {}: {}".format(line_number, sorted(leaked)))
            split_map = raw.get("split")
            if not isinstance(split_map, dict) or split_scheme not in split_map:
                raise ValueError("frozen split schema missing at line {}".format(line_number))
            if split_map[split_scheme] != expected_split:
                continue
            item_id = str(raw.get("item_id", ""))
            if not item_id or item_id in seen:
                raise ValueError("missing or duplicate item_id at line {}".format(line_number))
            distribution = raw.get(distribution_field)
            if not isinstance(distribution, dict) or set(distribution) != set(class_order):
                raise ValueError("distribution classes do not match class_order at line {}".format(line_number))
            target = np.asarray([distribution[name] for name in class_order], dtype=np.float64)
            if not np.isfinite(target).all() or (target < 0).any() or target.sum() <= 0:
                raise ValueError("invalid distribution at line {}".format(line_number))
            topic_id = raw.get("topic_id")
            records.append(Record(item_id, expected_split, target / target.sum(), None if topic_id is None else str(topic_id)))
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

def topic_mean_eligibility(records: Sequence[Record]) -> str:
    if not records or all(record.topic_id is None for record in records):
        return "NOT_APPLICABLE_NATIVE_TOPIC_ABSENT"
    if any(record.topic_id is None for record in records):
        return "INELIGIBLE_PARTIAL_TOPIC_COVERAGE"
    return "ELIGIBLE"

def fit_topic_train(records: Sequence[Record]) -> Dict[str, object]:
    if any(record.split != "train" for record in records):
        raise ValueError("fit scope violation: topic mean may fit on train only")
    eligibility = topic_mean_eligibility(records)
    if eligibility != "ELIGIBLE":
        raise ValueError("native topic unavailable: {}".format(eligibility))
    targets = _targets(records)
    topic_sums: Dict[str, np.ndarray] = {}
    topic_counts: Dict[str, int] = {}
    for record, target in zip(records, targets):
        topic = str(record.topic_id)
        topic_sums[topic] = topic_sums.get(topic, np.zeros_like(target)) + target
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    return {"topics": {topic: topic_sums[topic] / topic_counts[topic] for topic in sorted(topic_sums)}}

def predict_topic(model: Dict[str, object], topic_ids: Sequence[str]) -> np.ndarray:
    topics = model.get("topics")
    if not isinstance(topics, dict):
        raise ValueError("invalid topic mean model")
    missing = sorted({str(topic) for topic in topic_ids if str(topic) not in topics})
    if missing:
        raise ValueError("unseen topics have no train-only mean: {}".format(missing))
    return np.vstack([topics[str(topic)] for topic in topic_ids])

def run_minimum_baselines(
    train_records: Sequence[Record], evaluation_records: Sequence[Record]
) -> Dict[str, Dict[str, object]]:
    if not train_records or any(record.split != "train" for record in train_records):
        raise ValueError("minimum baselines require train-only fit records")
    if not evaluation_records or any(record.split == "train" for record in evaluation_records):
        raise ValueError("evaluation records must be dev or test")
    targets = _targets(evaluation_records)
    sample_ids = [record.item_id for record in evaluation_records]
    model = fit_train(train_records)
    results: Dict[str, Dict[str, object]] = {}
    for name in ("overall_mean", "empirical_distribution", "majority_class"):
        predictions = predict(model, name, len(evaluation_records))
        results[name] = {
            "status": "COMPLETED",
            "sample_ids": sample_ids,
            "predictions": predictions,
            "metrics": evaluate(targets, predictions),
        }
    eligibility = topic_mean_eligibility(train_records)
    if eligibility != "ELIGIBLE":
        results["topic_mean"] = {"status": eligibility, "sample_ids": sample_ids}
    elif any(record.topic_id is None for record in evaluation_records):
        results["topic_mean"] = {
            "status": "INELIGIBLE_EVALUATION_TOPIC_MISSING",
            "sample_ids": sample_ids,
        }
    else:
        topic_model = fit_topic_train(train_records)
        try:
            predictions = predict_topic(topic_model, [str(record.topic_id) for record in evaluation_records])
        except ValueError as error:
            results["topic_mean"] = {
                "status": "INELIGIBLE_UNSEEN_EVALUATION_TOPIC",
                "sample_ids": sample_ids,
                "reason": str(error),
            }
        else:
            results["topic_mean"] = {
                "status": "COMPLETED",
                "sample_ids": sample_ids,
                "predictions": predictions,
                "metrics": evaluate(targets, predictions),
            }
    return results

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
    return evaluate_distribution_predictions(targets, predictions)
