"""Prediction, E0 alignment, and paired-bootstrap contracts for task 20."""
from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from task20_metrics import evaluate_distribution_predictions


def build_prediction_rows(
    sample_ids: Sequence[str],
    split: str,
    class_order: Sequence[str],
    targets: np.ndarray,
    predictions: np.ndarray,
    model_id: str,
    config_id: str,
) -> List[Dict[str, object]]:
    targets = np.asarray(targets, dtype=np.float64)
    predictions = np.asarray(predictions, dtype=np.float64)
    if targets.shape != predictions.shape or targets.ndim != 2 or len(sample_ids) != targets.shape[0]:
        raise ValueError("sample/target/prediction shape mismatch")
    if len(class_order) != targets.shape[1] or len(set(class_order)) != len(class_order):
        raise ValueError("class_order mismatch")
    rows = []
    for index, sample_id in enumerate(sample_ids):
        confidence = float(np.max(predictions[index]))
        rows.append(
            {
                "schema_version": "task20-prediction-v1",
                "sample_id": str(sample_id),
                "split": split,
                "class_order": list(class_order),
                "true_distribution": [float(value) for value in targets[index]],
                "predicted_distribution": [float(value) for value in predictions[index]],
                "confidence": confidence,
                "rejection_score": 1.0 - confidence,
                "model_id": model_id,
                "config_id": config_id,
            }
        )
    return rows


def validate_prediction_rows(
    rows: Sequence[Dict[str, object]],
    expected_ids: Sequence[str],
    expected_split: str,
    class_order: Sequence[str],
) -> None:
    if len(rows) != len(expected_ids):
        raise ValueError("prediction count mismatch")
    actual_ids = [str(row.get("sample_id", "")) for row in rows]
    if actual_ids != list(expected_ids):
        if set(actual_ids) == set(expected_ids):
            raise ValueError("prediction sample order mismatch")
        raise ValueError("prediction sample ID mismatch")
    if len(actual_ids) != len(set(actual_ids)):
        raise ValueError("duplicate prediction sample ID")
    for row in rows:
        if row.get("schema_version") != "task20-prediction-v1":
            raise ValueError("prediction schema mismatch")
        if row.get("split") != expected_split:
            raise ValueError("prediction split mismatch")
        if row.get("class_order") != list(class_order):
            raise ValueError("prediction class order mismatch")
        target = np.asarray(row.get("true_distribution"), dtype=np.float64)
        prediction = np.asarray(row.get("predicted_distribution"), dtype=np.float64)
        if target.shape != (len(class_order),) or prediction.shape != target.shape:
            raise ValueError("prediction distribution shape mismatch")
        if not np.isfinite(target).all() or not np.isfinite(prediction).all() or (target < 0).any() or (prediction < 0).any():
            raise ValueError("prediction probability contains invalid values")
        if not np.isclose(target.sum(), 1.0, atol=1e-6) or not np.isclose(prediction.sum(), 1.0, atol=1e-6):
            raise ValueError("prediction probability must sum to one")
        confidence = float(np.max(prediction))
        if not np.isclose(float(row.get("confidence")), confidence, atol=1e-12):
            raise ValueError("confidence mismatch")
        if not np.isclose(float(row.get("rejection_score")), 1.0 - confidence, atol=1e-12):
            raise ValueError("rejection score mismatch")
        if not row.get("model_id") or not row.get("config_id"):
            raise ValueError("prediction provenance missing")


def validate_e0_alignment(
    train_ids: Sequence[str],
    evaluation_ids: Sequence[str],
    prediction_rows: Sequence[Dict[str, object]],
    expected_split: str,
    class_order: Sequence[str],
) -> None:
    train_set = set(train_ids)
    evaluation_set = set(evaluation_ids)
    if len(train_set) != len(train_ids) or len(evaluation_set) != len(evaluation_ids):
        raise ValueError("duplicate sample IDs in frozen split")
    overlap = train_set & evaluation_set
    if overlap:
        raise ValueError("train/evaluation overlap detected")
    validate_prediction_rows(prediction_rows, evaluation_ids, expected_split, class_order)


def paired_bootstrap_delta(
    sample_ids: Sequence[str],
    targets: np.ndarray,
    predictions_a: np.ndarray,
    predictions_b: np.ndarray,
    metric: str,
    replicates: int = 2000,
    seed: int = 20260717,
) -> Dict[str, object]:
    if len(sample_ids) == 0 or len(sample_ids) != len(set(sample_ids)):
        raise ValueError("video bootstrap requires unique non-empty sample IDs")
    targets = np.asarray(targets, dtype=np.float64)
    predictions_a = np.asarray(predictions_a, dtype=np.float64)
    predictions_b = np.asarray(predictions_b, dtype=np.float64)
    if targets.shape != predictions_a.shape or targets.shape != predictions_b.shape or targets.shape[0] != len(sample_ids):
        raise ValueError("paired bootstrap shape mismatch")
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if metric not in evaluate_distribution_predictions(targets, predictions_a):
        raise ValueError("unknown metric: {}".format(metric))

    observed_a = evaluate_distribution_predictions(targets, predictions_a)[metric]
    observed_b = evaluate_distribution_predictions(targets, predictions_b)[metric]
    rng = np.random.RandomState(seed)
    deltas = np.empty(replicates, dtype=np.float64)
    for replicate in range(replicates):
        indices = rng.randint(0, len(sample_ids), size=len(sample_ids))
        value_a = evaluate_distribution_predictions(targets[indices], predictions_a[indices])[metric]
        value_b = evaluate_distribution_predictions(targets[indices], predictions_b[indices])[metric]
        deltas[replicate] = value_a - value_b
    ci = np.percentile(deltas, [2.5, 97.5])
    return {
        "schema_version": "task20-paired-bootstrap-v1",
        "unit": "video",
        "metric": metric,
        "replicates": replicates,
        "seed": seed,
        "observed_delta_a_minus_b": float(observed_a - observed_b),
        "ci95": [float(ci[0]), float(ci[1])],
    }
