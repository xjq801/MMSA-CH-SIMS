#!/usr/bin/env python3
"""Rebuild the frozen LAI-GAI HUMAN_GOLD canonical file fail-closed.

The tracked raw manifest contains only image-level hashes and non-identifying
frozen lineage. Participant rows remain in the Git-ignored raw directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data/raw/lai-gai/second-primary-resolution/20260714"
MANIFEST_PATH = ROOT / "data/manifests/lai-gai-second-primary-raw-v1.manifest.json"
PROVENANCE_PATH = ROOT / "data/manifests/lai-gai-label-provenance-v1.manifest.json"
CANONICAL_PATH = ROOT / "data/processed/HUMAN_GOLD/lai-gai-v1/canonical.jsonl"
DATASET_ID = "LAI-GAI@v05-2026-03-11"
EMOTIONS = [
    ("amusement", "Amusement"),
    ("awe", "Awe"),
    ("anger", "Anger"),
    ("attachment_love", "Attachment_love"),
    ("craving", "Craving"),
    ("disgust", "Disgust"),
    ("excitement", "Excitement"),
    ("fear", "Fear"),
    ("joy", "Joy"),
    ("neutral", "Neutral"),
    ("nurturant_love", "Nurturant_love"),
    ("sadness", "Sadness"),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def bootstrap_manifest_lineage() -> None:
    """One-time freeze operation: copy non-identifying lineage into the manifest."""
    if not CANONICAL_PATH.is_file():
        raise FileNotFoundError(CANONICAL_PATH)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    canonical = {record["image_name"]: record for record in read_records(CANONICAL_PATH)}
    if len(canonical) != 847 or len(manifest.get("images", [])) != 847:
        raise RuntimeError("BOOTSTRAP_REQUIRES_847_CANONICAL_AND_IMAGES")
    for image in manifest["images"]:
        record = canonical[image["name"]]
        image["frozen_lineage"] = {
            "item_id": record["item_id"],
            "source_group_id": record["source_group_id"],
            "split": record["split"],
            "generation_source": record["provenance"].get("generation_source"),
            "prompt_not_input_or_truth_sha256": record["provenance"].get(
                "prompt_not_input_or_truth_sha256"
            ),
            "raw_ai_flag_conflict": record["provenance"].get("raw_ai_flag_conflict", False),
            "target_emotion_not_truth": record["provenance"]["target_emotion_not_truth"],
        }
    manifest.update(
        {
            "schema_version": "lai-gai-second-primary-raw-v1",
            "dataset_id": DATASET_ID,
            "status": "FROZEN_00_APPROVED",
            "frozen_canonical_sha256": digest(CANONICAL_PATH),
            "frozen_lineage_contains_prompt_text": False,
            "frozen_lineage_contains_participant_identifiers": False,
        }
    )
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_valid_rows(names: set[str]) -> tuple[pd.DataFrame, int]:
    frames = []
    participant_count = 0
    for study in range(1, 7):
        path = RAW_ROOT / f"S{study}_data.csv"
        frame = pd.read_csv(path, low_memory=False)
        selected = frame[
            frame["consent"].eq("YES")
            & frame["useData"].eq("Yes")
            & frame["rating_cat"].eq(0)
            & frame["Image_name"].isin(names)
        ].copy()
        participant_count += selected["participantID"].nunique()
        frames.append(selected)
    return pd.concat(frames, ignore_index=True), participant_count


def dimension_statistics(group: pd.DataFrame) -> tuple[dict, dict, dict]:
    counts, means, standard_deviations, standard_errors, histograms = {}, {}, {}, {}, {}
    for canonical_name, raw_name in EMOTIONS:
        values = [float(value) for value in group[raw_name].dropna()]
        if not values:
            raise RuntimeError(f"NO_RATINGS:{group['Image_name'].iloc[0]}:{canonical_name}")
        counts[canonical_name] = len(values)
        means[canonical_name] = statistics.fmean(values)
        standard_deviations[canonical_name] = statistics.stdev(values)
        standard_errors[canonical_name] = standard_deviations[canonical_name] / math.sqrt(len(values))
        histograms[canonical_name] = {
            str(rating): int(sum(value == rating for value in values)) for rating in range(1, 8)
        }
    mass = {name: means[name] - 1.0 for name, _ in EMOTIONS}
    total = sum(mass.values())
    if total <= 0:
        raise RuntimeError(f"NON_POSITIVE_DISTRIBUTION:{group['Image_name'].iloc[0]}")
    distribution = {name: mass[name] / total for name, _ in EMOTIONS}
    uncertainty = {
        "likert_histogram_1_to_7": histograms,
        "likert_mean": means,
        "likert_sample_std": standard_deviations,
        "likert_standard_error": standard_errors,
    }
    return counts, distribution, uncertainty


def rebuild() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
    images = {entry["name"]: entry for entry in manifest["images"]}
    if len(images) != 847 or any("frozen_lineage" not in entry for entry in images.values()):
        raise RuntimeError("RAW_MANIFEST_LINEAGE_NOT_FROZEN")
    for name, entry in images.items():
        path = RAW_ROOT / "images" / name
        if (
            not path.is_file()
            or path.stat().st_size != entry["size_bytes"]
            or digest(path) != entry["sha256"]
        ):
            raise RuntimeError(f"IMAGE_FIXITY_FAILURE:{name}")
    for entry in manifest["score_files"]:
        path = RAW_ROOT / entry["name"]
        if (
            not path.is_file()
            or path.stat().st_size != entry["size_bytes"]
            or digest(path) != entry["sha256"]
        ):
            raise RuntimeError(f"SCORE_FIXITY_FAILURE:{entry['name']}")

    rows, participant_count = load_valid_rows(set(images))
    if len(rows) != 63682 or rows["Image_name"].nunique() != 847 or participant_count != 2557:
        raise RuntimeError(
            f"FILTER_CONTRACT_FAILURE:rows={len(rows)}:images={rows['Image_name'].nunique()}:participants={participant_count}"
        )
    grouped = {name: group for name, group in rows.groupby("Image_name", sort=True)}
    records = []
    split_counts = Counter()
    for name in sorted(images, key=str.casefold):
        entry = images[name]
        lineage = entry["frozen_lineage"]
        counts, distribution, uncertainty = dimension_statistics(grouped[name])
        split_counts[lineage["split"]] += 1
        records.append(
            {
                "available_at_t0": True,
                "dataset_id": DATASET_ID,
                "dimension_response_count": counts,
                "distribution_uncertainty": uncertainty,
                "emotion_distribution": distribution,
                "image_name": name,
                "image_sha256": entry["sha256"],
                "item_id": lineage["item_id"],
                "label_available_at_t0": False,
                "label_source": "six_independent_human_affect_induction_studies",
                "label_tier": "HUMAN_GOLD",
                "provenance": {
                    "generation_source": lineage["generation_source"],
                    "mapping_version": "lai-gai-label-map-v1",
                    "prompt_not_input_or_truth_sha256": lineage[
                        "prompt_not_input_or_truth_sha256"
                    ],
                    "raw_ai_flag_conflict": lineage["raw_ai_flag_conflict"],
                    "target_emotion_not_truth": lineage["target_emotion_not_truth"],
                },
                # Count eligible image-response rows independently from per-dimension N;
                # a retained respondent may have a missing value on every scored dimension.
                "response_count": len(grouped[name]),
                "schema_version": "lai-gai-canonical-human-gold-v1",
                "source_domain": "lai-gai-ai-generated-affective-images",
                "source_group_id": lineage["source_group_id"],
                "split": lineage["split"],
            }
        )
    payload = "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records
    )
    temporary = CANONICAL_PATH.with_suffix(".jsonl.tmp")
    temporary.parent.mkdir(parents=True, exist_ok=True)
    # Freeze byte-identical LF newlines across Windows/Linux environments.
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(payload)
    actual_hash = digest(temporary)
    expected_hash = provenance["canonical_sha256"]
    if actual_hash != expected_hash or actual_hash != manifest["frozen_canonical_sha256"]:
        raise RuntimeError(f"CANONICAL_HASH_DRIFT:{actual_hash}:{expected_hash}")
    temporary.replace(CANONICAL_PATH)
    result = {
        "status": "LAI_GAI_SECOND_PRIMARY_REPRODUCED",
        "records": len(records),
        "valid_response_rows": len(rows),
        "participants_study_scoped": participant_count,
        "split": dict(sorted(split_counts.items())),
        "canonical_sha256": actual_hash,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap-manifest-lineage", action="store_true")
    args = parser.parse_args()
    if args.bootstrap_manifest_lineage:
        bootstrap_manifest_lineage()
    rebuild()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
