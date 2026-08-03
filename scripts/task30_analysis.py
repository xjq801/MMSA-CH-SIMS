"""Aggregate-only Task30 error and mechanism analysis."""
from __future__ import annotations

import math
from typing import Dict

import numpy as np

from task20_metrics import per_sample_jensen_shannon


def _group_summary(mask, baseline_js, privileged_js) -> Dict[str, object]:
    count = int(np.sum(mask))
    if count == 0:
        return {"n": 0, "baseline_js": None, "privileged_js": None, "mean_js_gain": None}
    return {
        "n": count,
        "baseline_js": float(np.mean(baseline_js[mask])),
        "privileged_js": float(np.mean(privileged_js[mask])),
        "mean_js_gain": float(np.mean(baseline_js[mask] - privileged_js[mask])),
    }


def analyze_error_groups(
    targets: np.ndarray,
    baseline_predictions: np.ndarray,
    privileged_predictions: np.ndarray,
    response_counts: np.ndarray,
    normalized_entropy: np.ndarray,
    noise_score: np.ndarray,
) -> Dict[str, object]:
    targets = np.asarray(targets, dtype=np.float64)
    baseline = np.asarray(baseline_predictions, dtype=np.float64)
    privileged = np.asarray(privileged_predictions, dtype=np.float64)
    counts = np.asarray(response_counts, dtype=np.int64)
    entropy = np.asarray(normalized_entropy, dtype=np.float64)
    noise = np.asarray(noise_score, dtype=np.float64)
    row_count = targets.shape[0]
    if (
        targets.ndim != 2
        or baseline.shape != targets.shape
        or privileged.shape != targets.shape
        or counts.shape != (row_count,)
        or entropy.shape != (row_count,)
        or noise.shape != (row_count,)
        or (counts <= 0).any()
        or not np.isfinite(entropy).all()
        or not np.isfinite(noise).all()
    ):
        raise ValueError("Task30 aggregate analysis inputs are invalid or misaligned")
    baseline_js = per_sample_jensen_shannon(targets, baseline)
    privileged_js = per_sample_jensen_shannon(targets, privileged)
    low_noise, high_noise = np.quantile(noise, [1 / 3, 2 / 3])
    response_groups = {
        "low_1_2": counts <= 2,
        "medium_3_10": (counts >= 3) & (counts <= 10),
        "high_11_plus": counts >= 11,
    }
    mixture_groups = {
        "low_entropy": entropy < 1 / 3,
        "mixed": (entropy >= 1 / 3) & (entropy < 2 / 3),
        "high_entropy": entropy >= 2 / 3,
    }
    noise_groups = {
        "lower_third": noise <= low_noise,
        "middle_third": (noise > low_noise) & (noise < high_noise),
        "upper_third": noise >= high_noise,
    }
    return {
        "response_count": {
            name: _group_summary(mask, baseline_js, privileged_js)
            for name, mask in response_groups.items()
        },
        "target_mixture": {
            name: _group_summary(mask, baseline_js, privileged_js)
            for name, mask in mixture_groups.items()
        },
        "label_noise_proxy": {
            name: _group_summary(mask, baseline_js, privileged_js)
            for name, mask in noise_groups.items()
        },
        "sarcasm": "NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE",
        "cross_domain": "LAI_GAI_REPORTED_SEPARATELY_H1_NOT_APPLICABLE",
        "privacy_boundary": "AGGREGATES_ONLY_NO_SAMPLE_IDS_OR_RESPONSE_TEXT",
    }


def analyze_teacher_confidence_effect(
    train_targets: np.ndarray,
    ordinary_teacher_predictions: np.ndarray,
    privileged_teacher_predictions: np.ndarray,
    teacher_confidences: np.ndarray,
) -> Dict[str, object]:
    """Relate train-only empirical confidence to the privileged teacher fit gain.

    Dev/test responses remain unreachable, so this is deliberately not presented
    as a dev-student subgroup effect.
    """
    targets = np.asarray(train_targets, dtype=np.float64)
    ordinary = np.asarray(ordinary_teacher_predictions, dtype=np.float64)
    privileged = np.asarray(privileged_teacher_predictions, dtype=np.float64)
    confidence = np.asarray(teacher_confidences, dtype=np.float64)
    if (
        targets.ndim != 2
        or ordinary.shape != targets.shape
        or privileged.shape != targets.shape
        or confidence.shape != (targets.shape[0],)
        or not np.isfinite(confidence).all()
        or (confidence < 0.0).any()
        or (confidence > 1.0).any()
    ):
        raise ValueError("teacher-confidence analysis inputs are invalid or misaligned")
    ordinary_js = per_sample_jensen_shannon(targets, ordinary)
    privileged_js = per_sample_jensen_shannon(targets, privileged)
    gain = ordinary_js - privileged_js
    low, high = np.quantile(confidence, [1 / 3, 2 / 3])
    masks = {
        "lower": confidence <= low,
        "middle": (confidence > low) & (confidence < high),
        "upper": confidence >= high,
    }
    if math.isclose(float(np.std(confidence)), 0.0, rel_tol=0.0, abs_tol=1e-15) or math.isclose(
        float(np.std(gain)), 0.0, rel_tol=0.0, abs_tol=1e-15
    ):
        correlation = 0.0
    else:
        correlation = float(np.corrcoef(confidence, gain)[0, 1])
    return {
        "scope": "TRAIN_TEACHER_FIT_DIAGNOSTIC_NOT_DEV_STUDENT_SUBGROUP",
        "confidence_definition": "ONE_MINUS_NORMALIZED_EMPIRICAL_ENTROPY",
        "pearson_confidence_vs_teacher_js_gain": correlation,
        "confidence_thirds": {
            name: {
                "n": int(mask.sum()),
                "mean_teacher_js_gain": float(gain[mask].mean()) if mask.any() else None,
                "mean_confidence": float(confidence[mask].mean()) if mask.any() else None,
            }
            for name, mask in masks.items()
        },
        "privacy_boundary": "AGGREGATES_ONLY_NO_SAMPLE_IDS_OR_RESPONSE_TEXT",
    }
