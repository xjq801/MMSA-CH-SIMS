#!/usr/bin/env python3
"""Audit aggregate response support for the CARM preregistration package.

The script reads only tracked aggregate HUMAN_GOLD records.  It does not emit
item identifiers, response text, participant identifiers, or raw records.
"""

import argparse
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def distribution_summary(values):
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "sum": sum(ordered),
        "min": min(ordered),
        "median": statistics.median(ordered),
        "max": max(ordered),
        "histogram": {str(key): value for key, value in sorted(Counter(ordered).items())},
    }


def csmv_audit(path):
    response_counts = []
    valid_emotion_counts = []
    split_counts = Counter()
    split_response_counts = defaultdict(list)
    missing_emotion = 0
    reconstruction_noninteger_cells = 0
    reconstruction_max_abs_residual = 0.0

    for record in read_jsonl(path):
        response_count = int(record["response_count"])
        emotion_info = record["distribution_uncertainty"]["emotion"]
        valid_count = int(emotion_info["valid_response_count"])
        split_field = record["split"]
        split = split_field["group_by_video_v1"] if isinstance(split_field, dict) else split_field

        response_counts.append(response_count)
        valid_emotion_counts.append(valid_count)
        split_counts[split] += 1
        split_response_counts[split].append(valid_count)
        missing_emotion += int(record["distribution_uncertainty"].get("missing_emotion", 0))

        distribution = record["emotion_distribution"]
        probabilities = distribution.values() if isinstance(distribution, dict) else distribution
        for probability in probabilities:
            reconstructed = float(probability) * valid_count
            residual = abs(reconstructed - round(reconstructed))
            reconstruction_max_abs_residual = max(reconstruction_max_abs_residual, residual)
            if residual > 1e-8:
                reconstruction_noninteger_cells += 1

    thresholds = [2, 4, 8, 16]
    return {
        "path": path.as_posix(),
        "sha256": sha256(path),
        "rows": len(response_counts),
        "response_count": distribution_summary(response_counts),
        "valid_emotion_response_count": distribution_summary(valid_emotion_counts),
        "eligible_items": {
            "all": len(valid_emotion_counts),
            **{f"n_ge_{threshold}": sum(value >= threshold for value in valid_emotion_counts) for threshold in thresholds},
        },
        "missing_emotion_labels": missing_emotion,
        "split_rows": dict(sorted(split_counts.items())),
        "split_valid_emotion_response_count": {
            split: distribution_summary(values) for split, values in sorted(split_response_counts.items())
        },
        "category_count_reconstruction": {
            "tolerance": 1e-8,
            "noninteger_cells": reconstruction_noninteger_cells,
            "max_abs_residual": reconstruction_max_abs_residual,
            "verdict": "EXACT_WITHIN_TOLERANCE" if reconstruction_noninteger_cells == 0 else "FAILED",
        },
    }


def lai_gai_audit(path):
    response_counts = []
    dimension_counts = []
    dimensions = set()
    histogram_sum_mismatches = 0

    for record in read_jsonl(path):
        response_counts.append(int(record["response_count"]))
        per_dimension = record["dimension_response_count"]
        histograms = record["distribution_uncertainty"]["likert_histogram_1_to_7"]
        dimensions.update(per_dimension)
        for dimension, count in per_dimension.items():
            count = int(count)
            dimension_counts.append(count)
            histogram_sum = sum(int(value) for value in histograms[dimension].values())
            if histogram_sum != count:
                histogram_sum_mismatches += 1

    return {
        "path": path.as_posix(),
        "sha256": sha256(path),
        "rows": len(response_counts),
        "response_count": distribution_summary(response_counts),
        "dimension_response_count": distribution_summary(dimension_counts),
        "dimensions": sorted(dimensions),
        "histogram_sum_mismatches": histogram_sum_mismatches,
        "marginal_histograms_available": True,
        "joint_respondent_vectors_available_in_canonical": False,
        "fitness_boundary": "MARGINAL_DIMENSION_THINNING_ONLY_NO_JOINT_RESPONDENT_RESAMPLING",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csmv",
        type=Path,
        default=Path("data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl"),
    )
    parser.add_argument(
        "--lai-gai",
        type=Path,
        default=Path("data/processed/HUMAN_GOLD/lai-gai-v1/canonical.jsonl"),
    )
    args = parser.parse_args()

    report = {
        "schema": "carm.response_support_audit.v1",
        "privacy": "AGGREGATE_ONLY_NO_ITEM_IDS_OR_RESPONSE_TEXT",
        "csmv": csmv_audit(args.csmv),
        "lai_gai": lai_gai_audit(args.lai_gai),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
