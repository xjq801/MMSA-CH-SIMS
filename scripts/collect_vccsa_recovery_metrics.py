"""Derive private Task20 distribution metrics from author VC-CSA dev predictions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import pickle
from typing import Dict, Iterable

import numpy as np

from task20_metrics import evaluate_distribution_predictions


REQUIRED_KEYS = {
    "comments_key",
    "opinion_preds",
    "opinion_preds_classidx",
    "emotion_preds",
    "emotion_preds_classidx",
    "opinions_label",
    "opinions_label_classindex",
    "emotions_label",
    "emotions_label_classindex",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _matrix(payload: Dict[str, object], key: str, rows: int) -> np.ndarray:
    value = np.asarray(payload[key], dtype=np.float64)
    if value.ndim != 2 or value.shape[0] != rows:
        raise ValueError(f"{key} has an invalid shape")
    if not np.all(np.isfinite(value)) or np.any(value < 0.0):
        raise ValueError(f"{key} contains invalid probabilities")
    if not np.allclose(value.sum(axis=1), 1.0, atol=1e-5):
        raise ValueError(f"{key} rows are not normalized")
    return value


def _indices(payload: Dict[str, object], key: str, rows: int) -> np.ndarray:
    value = np.asarray(payload[key], dtype=np.int64)
    if value.shape != (rows,):
        raise ValueError(f"{key} has an invalid shape")
    return value


def _raw_label_matrix(payload: Dict[str, object], key: str, rows: int) -> np.ndarray:
    value = np.asarray(payload[key], dtype=np.float64)
    if value.ndim != 2 or value.shape[0] != rows:
        raise ValueError(f"{key} has an invalid shape")
    if not np.all(np.isfinite(value)) or np.any(value < 0.0):
        raise ValueError(f"{key} contains invalid labels")
    return value


def collect_prediction_metrics(path: Path, expected_rows: int) -> Dict[str, object]:
    # The input is a private, locally generated author-runtime artifact. It must
    # never be accepted from an untrusted source because pickle is executable.
    with path.open("rb") as handle:
        payload = pickle.load(handle)
    if not isinstance(payload, dict) or set(payload) != REQUIRED_KEYS:
        raise ValueError("prediction payload schema mismatch")

    sample_ids = payload["comments_key"]
    if not isinstance(sample_ids, list) or len(sample_ids) != expected_rows:
        raise ValueError("prediction sample count mismatch")
    if any(not isinstance(value, str) or not value for value in sample_ids):
        raise ValueError("prediction sample IDs must be non-empty strings")
    if len(set(sample_ids)) != expected_rows:
        raise ValueError("prediction sample IDs are not unique")

    tasks = {}
    raw_non_normalized_rows = {}
    for task, prediction_key, prediction_index_key, target_key, target_index_key in (
        ("opinion", "opinion_preds", "opinion_preds_classidx", "opinions_label", "opinions_label_classindex"),
        ("emotion", "emotion_preds", "emotion_preds_classidx", "emotions_label", "emotions_label_classindex"),
    ):
        predictions = _matrix(payload, prediction_key, expected_rows)
        raw_targets = _raw_label_matrix(payload, target_key, expected_rows)
        predicted_indices = _indices(payload, prediction_index_key, expected_rows)
        target_indices = _indices(payload, target_index_key, expected_rows)
        if not np.array_equal(predicted_indices, np.argmax(predictions, axis=1)):
            raise ValueError(f"{task} predicted class indices are misaligned")
        if np.any(target_indices < 0) or np.any(target_indices >= predictions.shape[1]):
            raise ValueError(f"{task} target class indices are out of range")
        normalized = np.isclose(raw_targets.sum(axis=1), 1.0, atol=1e-5)
        raw_non_normalized_rows[task] = int(np.count_nonzero(~normalized))
        if not np.array_equal(
            target_indices[normalized], np.argmax(raw_targets[normalized], axis=1)
        ):
            raise ValueError(f"{task} normalized raw labels and class indices are misaligned")
        targets = np.eye(predictions.shape[1], dtype=np.float64)[target_indices]
        raw_metrics = evaluate_distribution_predictions(targets, predictions)
        tasks[task] = {
            "js": raw_metrics["jensen_shannon_divergence"],
            "nll": raw_metrics["negative_log_likelihood"],
            "emd": raw_metrics["earth_movers_distance"],
            "macro_f1": raw_metrics["macro_f1"],
            "balanced_accuracy": raw_metrics["balanced_accuracy"],
            "brier": raw_metrics["brier_score"],
            "ece": raw_metrics["expected_calibration_error"],
            "ace": raw_metrics["adaptive_calibration_error"],
            "aurc_js": raw_metrics["aurc_js"],
        }

    return {
        "schema_version": "task20-vccsa-recovery-dev-nine-metrics-v1",
        "source_prediction_sha256": _sha256(path),
        "sample_count": expected_rows,
        "test_access": 0,
        "target_contract": {
            "source": "author_label_classindex_one_hot",
            "raw_non_normalized_rows": raw_non_normalized_rows,
            "policy": "never silently normalize malformed raw label vectors",
        },
        "tasks": tasks,
    }


def _parse_epochs(value: str) -> Iterable[int]:
    epochs = [int(item) for item in value.split(",") if item]
    if not epochs or any(epoch < 1 for epoch in epochs) or len(set(epochs)) != len(epochs):
        raise argparse.ArgumentTypeError("epochs must be unique positive integers")
    return epochs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prediction-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--epochs", type=_parse_epochs, default=[1, 2, 3])
    parser.add_argument("--expected-rows", type=int, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    for epoch in args.epochs:
        source = args.prediction_dir / f"dev_predict_{epoch}.pkl"
        result = collect_prediction_metrics(source, args.expected_rows)
        result["epoch"] = epoch
        destination = args.output_dir / f"dev_nine_metrics_{epoch}.json"
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, indent=2, sort_keys=True)
            handle.write("\n")
        destination.chmod(0o600)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
