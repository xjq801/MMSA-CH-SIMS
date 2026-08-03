"""Train-only response aggregation and privacy-safe teacher audit for Task30."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Mapping, Sequence

import numpy as np

from task30_contracts import DatasetSpec, LeakageBlockedError, validate_teacher_records


_REACTION_FIELDS = {
    "dataset_id",
    "sample_id",
    "split",
    "reaction_label",
    "label_confidence",
}


def aggregate_train_reactions(
    reactions: Sequence[Mapping[str, object]],
    spec: DatasetSpec,
) -> List[Dict[str, object]]:
    if spec.privileged_supervision_status != "TRAIN_RESPONSES_ONLY":
        raise ValueError("comment teacher is not applicable for dataset")
    if not reactions:
        raise ValueError("reaction rows must be non-empty")

    label_to_index = {label: index for index, label in enumerate(spec.class_order)}
    grouped_counts = defaultdict(lambda: np.zeros(len(spec.class_order), dtype=np.int64))
    grouped_confidence = defaultdict(list)
    for row in reactions:
        missing = sorted(_REACTION_FIELDS - set(row))
        extra = sorted(set(row) - _REACTION_FIELDS)
        if missing:
            raise ValueError("reaction row missing fields: {}".format(", ".join(missing)))
        if extra:
            raise ValueError("reaction row contains unapproved fields: {}".format(", ".join(extra)))
        if row["dataset_id"] != spec.dataset_id:
            raise ValueError("reaction dataset mismatch")
        if row["split"] != "train":
            raise LeakageBlockedError("teacher reaction aggregation is restricted to train")
        sample_id = str(row["sample_id"])
        if not sample_id:
            raise ValueError("reaction sample_id is required")
        label = str(row["reaction_label"])
        if label not in label_to_index:
            raise ValueError("reaction label is outside the dataset class order")
        confidence = float(row["label_confidence"])
        if not np.isfinite(confidence) or confidence < 0.0 or confidence > 1.0:
            raise ValueError("reaction label confidence must be finite and in [0, 1]")
        grouped_counts[sample_id][label_to_index[label]] += 1
        grouped_confidence[sample_id].append(confidence)

    records = []
    for sample_id in sorted(grouped_counts):
        counts = grouped_counts[sample_id]
        response_count = int(counts.sum())
        records.append(
            {
                "dataset_id": spec.dataset_id,
                "sample_id": sample_id,
                "split": "train",
                "class_order": list(spec.class_order),
                "teacher_distribution": (counts / response_count).astype(np.float64).tolist(),
                "response_count": response_count,
                "teacher_confidence": float(np.mean(grouped_confidence[sample_id])),
            }
        )
    return validate_teacher_records(records, spec)


def audit_teacher_records(
    records: Sequence[Mapping[str, object]],
    spec: DatasetSpec,
    sparse_mass_threshold: float = 0.01,
    low_response_threshold: int = 2,
) -> Dict[str, object]:
    if (
        not np.isfinite(sparse_mass_threshold)
        or sparse_mass_threshold < 0.0
        or sparse_mass_threshold > 1.0
    ):
        raise ValueError("sparse_mass_threshold must be finite and in [0, 1]")
    if not isinstance(low_response_threshold, int) or isinstance(low_response_threshold, bool) or low_response_threshold < 1:
        raise ValueError("low_response_threshold must be a positive integer")
    validated = validate_teacher_records(records, spec)
    response_counts = np.asarray([record["response_count"] for record in validated], dtype=np.int64)
    confidences = np.asarray([record["teacher_confidence"] for record in validated], dtype=np.float64)
    total_responses = int(response_counts.sum())
    class_counts = np.zeros(len(spec.class_order), dtype=np.float64)
    for record in validated:
        class_counts += (
            np.asarray(record["teacher_distribution"], dtype=np.float64) * record["response_count"]
        )
    class_mass = class_counts / total_responses
    sparse_classes = [
        label
        for label, mass in zip(spec.class_order, class_mass)
        if float(mass) < sparse_mass_threshold
    ]
    return {
        "schema_version": "task30-teacher-audit-v1",
        "dataset_id": spec.dataset_id,
        "sample_count": len(validated),
        "response_count": {
            "total": total_responses,
            "minimum": int(response_counts.min()),
            "median": float(np.median(response_counts)),
            "mean": float(response_counts.mean()),
            "maximum": int(response_counts.max()),
        },
        "teacher_confidence": {
            "minimum": float(confidences.min()),
            "mean": float(confidences.mean()),
            "maximum": float(confidences.max()),
        },
        "class_mass": {
            label: float(mass) for label, mass in zip(spec.class_order, class_mass)
        },
        "sparse_mass_threshold": float(sparse_mass_threshold),
        "sparse_classes": sparse_classes,
        "low_response_threshold": low_response_threshold,
        "low_response_sample_count": int(np.sum(response_counts <= low_response_threshold)),
        "privacy_boundary": "AGGREGATES_ONLY_NO_SAMPLE_IDS_OR_RESPONSE_TEXT",
    }
