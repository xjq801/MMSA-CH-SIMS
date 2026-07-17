"""Frozen distribution-prediction metrics for task 20."""
from __future__ import annotations

from typing import Dict

import numpy as np


def _probability_matrix(values: np.ndarray, name: str) -> np.ndarray:
    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] == 0 or matrix.shape[1] < 2:
        raise ValueError("{} probability matrix must be non-empty and two-dimensional".format(name))
    if not np.isfinite(matrix).all() or (matrix < 0.0).any():
        raise ValueError("{} probability matrix contains invalid values".format(name))
    sums = matrix.sum(axis=1)
    if not np.allclose(sums, 1.0, rtol=0.0, atol=1e-6):
        raise ValueError("{} probability rows must sum to one".format(name))
    return matrix / sums[:, None]


def per_sample_jensen_shannon(targets: np.ndarray, predictions: np.ndarray) -> np.ndarray:
    targets = _probability_matrix(targets, "target")
    predictions = _probability_matrix(predictions, "prediction")
    if targets.shape != predictions.shape:
        raise ValueError("target/prediction shape mismatch")
    eps = np.finfo(np.float64).tiny
    p = np.clip(targets, eps, 1.0)
    q = np.clip(predictions, eps, 1.0)
    midpoint = 0.5 * (p + q)
    return 0.5 * np.sum(p * np.log(p / midpoint), axis=1) + 0.5 * np.sum(q * np.log(q / midpoint), axis=1)


def _macro_f1_and_balanced_accuracy(targets: np.ndarray, predictions: np.ndarray) -> tuple:
    true_labels = np.argmax(targets, axis=1)
    predicted_labels = np.argmax(predictions, axis=1)
    f1_values = []
    recalls = []
    for class_id in range(targets.shape[1]):
        true_positive = int(np.sum((true_labels == class_id) & (predicted_labels == class_id)))
        false_positive = int(np.sum((true_labels != class_id) & (predicted_labels == class_id)))
        false_negative = int(np.sum((true_labels == class_id) & (predicted_labels != class_id)))
        precision_denominator = true_positive + false_positive
        recall_denominator = true_positive + false_negative
        precision = true_positive / precision_denominator if precision_denominator else 0.0
        recall = true_positive / recall_denominator if recall_denominator else None
        f1_values.append(2.0 * precision * recall / (precision + recall) if recall is not None and precision + recall else 0.0)
        if recall is not None:
            recalls.append(recall)
    return float(np.mean(f1_values)), float(np.mean(recalls))


def _expected_calibration_error(confidence: np.ndarray, correct: np.ndarray, bins: int) -> float:
    edges = np.linspace(0.0, 1.0, bins + 1)
    error = 0.0
    for index in range(bins):
        if index == 0:
            mask = (confidence >= edges[index]) & (confidence <= edges[index + 1])
        else:
            mask = (confidence > edges[index]) & (confidence <= edges[index + 1])
        if mask.any():
            error += float(mask.mean()) * abs(float(correct[mask].mean()) - float(confidence[mask].mean()))
    return error


def _adaptive_calibration_error(confidence: np.ndarray, correct: np.ndarray, bins: int) -> float:
    order = np.argsort(confidence, kind="mergesort")
    groups = np.array_split(order, min(bins, confidence.size))
    error = 0.0
    for group in groups:
        if group.size:
            error += float(group.size / confidence.size) * abs(
                float(correct[group].mean()) - float(confidence[group].mean())
            )
    return error


def evaluate_distribution_predictions(
    targets: np.ndarray,
    predictions: np.ndarray,
    calibration_bins: int = 15,
) -> Dict[str, float]:
    """Evaluate one frozen class order; EMD uses normalized class-index distance."""
    targets = _probability_matrix(targets, "target")
    predictions = _probability_matrix(predictions, "prediction")
    if targets.shape != predictions.shape:
        raise ValueError("target/prediction shape mismatch")
    if calibration_bins <= 0:
        raise ValueError("calibration_bins must be positive")

    eps = 1e-12
    js_values = per_sample_jensen_shannon(targets, predictions)
    nll_values = -np.sum(targets * np.log(np.clip(predictions, eps, 1.0)), axis=1)
    emd_values = np.sum(np.abs(np.cumsum(targets, axis=1)[:, :-1] - np.cumsum(predictions, axis=1)[:, :-1]), axis=1)
    emd_values /= targets.shape[1] - 1
    macro_f1, balanced_accuracy = _macro_f1_and_balanced_accuracy(targets, predictions)
    confidence = np.max(predictions, axis=1)
    correct = (np.argmax(targets, axis=1) == np.argmax(predictions, axis=1)).astype(np.float64)
    order = np.argsort(-confidence, kind="mergesort")
    sorted_confidence = confidence[order]
    sorted_risk = js_values[order]
    group_ends = np.r_[np.flatnonzero(np.diff(sorted_confidence) != 0.0) + 1, targets.shape[0]]
    cumulative_sum = np.cumsum(sorted_risk)
    previous_end = 0
    aurc = 0.0
    for end in group_ends:
        group_weight = (int(end) - previous_end) / targets.shape[0]
        aurc += group_weight * float(cumulative_sum[int(end) - 1] / int(end))
        previous_end = int(end)

    return {
        "jensen_shannon_divergence": float(js_values.mean()),
        "negative_log_likelihood": float(nll_values.mean()),
        "earth_movers_distance": float(emd_values.mean()),
        "macro_f1": macro_f1,
        "balanced_accuracy": balanced_accuracy,
        "brier_score": float(np.sum((predictions - targets) ** 2, axis=1).mean()),
        "expected_calibration_error": _expected_calibration_error(confidence, correct, calibration_bins),
        "adaptive_calibration_error": _adaptive_calibration_error(confidence, correct, calibration_bins),
        "aurc_js": aurc,
    }
