"""Fail-closed data contracts for Task30 response-privileged supervision."""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List, Mapping, Sequence, Tuple

import numpy as np


class LeakageBlockedError(ValueError):
    """Raised when response or future information crosses the Task30 T0 boundary."""


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: str
    class_order: Tuple[str, ...]
    privileged_supervision_status: str

    def __post_init__(self) -> None:
        if not self.dataset_id:
            raise ValueError("dataset_id is required")
        if len(self.class_order) < 2 or len(set(self.class_order)) != len(self.class_order):
            raise ValueError("class order must contain at least two unique labels")
        if self.privileged_supervision_status not in {
            "TRAIN_RESPONSES_ONLY",
            "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE",
            "NOT_APPLICABLE_DATA_NOT_RELEASED",
        }:
            raise ValueError("unknown privileged supervision status")


def dataset_applicability(dataset_id: str) -> str:
    normalized = dataset_id.strip().lower().replace("_", "-")
    if normalized == "csmv":
        return "APPLICABLE_TRAIN_RESPONSES_ONLY"
    if normalized in {"lai-gai", "laigai"}:
        return "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE"
    if normalized in {"video2reaction", "video2reaction-native"}:
        return "NOT_APPLICABLE_DATA_NOT_RELEASED"
    return "UNKNOWN_DATASET_REQUIRES_EXPLICIT_CONTRACT"


def validate_distribution(values: Sequence[float], class_order: Sequence[str], name: str) -> np.ndarray:
    distribution = np.asarray(values, dtype=np.float64)
    if distribution.shape != (len(class_order),):
        raise ValueError("{} distribution/class order shape mismatch".format(name))
    if not np.isfinite(distribution).all():
        raise ValueError("{} distribution must be finite".format(name))
    if (distribution < 0.0).any():
        raise ValueError("{} distribution must be non-negative".format(name))
    total = float(distribution.sum())
    if not np.isclose(total, 1.0, rtol=0.0, atol=1e-6):
        raise ValueError("{} distribution must sum to one".format(name))
    return distribution / total


_TEACHER_REQUIRED_FIELDS = {
    "dataset_id",
    "sample_id",
    "split",
    "class_order",
    "teacher_distribution",
    "response_count",
    "teacher_confidence",
}


def validate_teacher_records(
    records: Sequence[Mapping[str, object]],
    spec: DatasetSpec,
) -> List[Dict[str, object]]:
    if spec.privileged_supervision_status != "TRAIN_RESPONSES_ONLY":
        raise ValueError("comment teacher is not applicable for dataset")
    if not records:
        raise ValueError("teacher records must be non-empty")

    validated: List[Dict[str, object]] = []
    seen = set()
    for record in records:
        missing = sorted(_TEACHER_REQUIRED_FIELDS - set(record))
        if missing:
            raise ValueError("teacher record missing fields: {}".format(", ".join(missing)))
        if record["dataset_id"] != spec.dataset_id:
            raise ValueError("teacher dataset mismatch")
        if record["split"] != "train":
            raise LeakageBlockedError("teacher records must be restricted to train")
        if tuple(record["class_order"]) != spec.class_order:
            raise ValueError("teacher class order mismatch")
        sample_id = str(record["sample_id"])
        if not sample_id or sample_id in seen:
            raise ValueError("teacher sample IDs must be unique and non-empty")
        seen.add(sample_id)
        response_count = record["response_count"]
        if not isinstance(response_count, int) or isinstance(response_count, bool) or response_count <= 0:
            raise ValueError("response_count must be a positive integer")
        confidence = float(record["teacher_confidence"])
        if not np.isfinite(confidence) or confidence < 0.0 or confidence > 1.0:
            raise ValueError("teacher_confidence must be finite and in [0, 1]")
        distribution = validate_distribution(
            record["teacher_distribution"], spec.class_order, "teacher"
        )
        validated.append(
            {
                "dataset_id": spec.dataset_id,
                "sample_id": sample_id,
                "split": "train",
                "class_order": list(spec.class_order),
                "teacher_distribution": distribution.tolist(),
                "response_count": response_count,
                "teacher_confidence": confidence,
            }
        )
    return validated


_STUDENT_FORBIDDEN_TOKENS = (
    "comment",
    "response",
    "future",
    "engagement",
    "teacher",
    "privileged",
)


def validate_student_batch(batch: Mapping[str, object], spec: DatasetSpec) -> Dict[str, object]:
    forbidden = sorted(
        key
        for key in batch
        if any(token in key.lower() for token in _STUDENT_FORBIDDEN_TOKENS)
    )
    if forbidden:
        raise LeakageBlockedError("forbidden student fields: {}".format(", ".join(forbidden)))
    required = {"dataset_id", "sample_ids", "content_features", "target_distribution"}
    missing = sorted(required - set(batch))
    if missing:
        raise ValueError("student batch missing fields: {}".format(", ".join(missing)))
    if batch["dataset_id"] != spec.dataset_id:
        raise ValueError("student dataset mismatch")
    sample_ids = [str(value) for value in batch["sample_ids"]]
    if not sample_ids or len(set(sample_ids)) != len(sample_ids) or any(not value for value in sample_ids):
        raise ValueError("student sample IDs must be unique and non-empty")
    features = np.asarray(batch["content_features"], dtype=np.float32)
    targets = np.asarray(batch["target_distribution"], dtype=np.float64)
    if features.ndim != 2 or features.shape[0] != len(sample_ids) or not np.isfinite(features).all():
        raise ValueError("invalid content features")
    if targets.shape != (len(sample_ids), len(spec.class_order)):
        raise ValueError("student target shape mismatch")
    normalized_targets = np.vstack(
        [validate_distribution(row, spec.class_order, "student target") for row in targets]
    )
    return {
        "dataset_id": spec.dataset_id,
        "sample_ids": sample_ids,
        "content_features": features,
        "target_distribution": normalized_targets,
    }


def make_mismatched_teacher_targets(
    records: Sequence[Mapping[str, object]],
    spec: DatasetSpec,
    seed: int,
) -> List[Dict[str, object]]:
    validated = validate_teacher_records(records, spec)
    if len(validated) < 2:
        raise ValueError("mismatched teacher requires at least two train samples")
    shift = random.Random(seed).randrange(1, len(validated))
    sources = validated[shift:] + validated[:shift]
    output: List[Dict[str, object]] = []
    for target, source in zip(validated, sources):
        output.append(
            {
                "dataset_id": spec.dataset_id,
                "sample_id": target["sample_id"],
                "split": "train",
                "class_order": list(spec.class_order),
                "teacher_distribution": list(source["teacher_distribution"]),
                "teacher_source_sample_id": source["sample_id"],
                "control": "MISMATCHED_TEACHER_DERANGEMENT",
                "seed": int(seed),
            }
        )
    return output
