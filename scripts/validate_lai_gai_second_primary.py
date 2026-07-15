"""Fail-closed validation for the LAI-GAI second-primary freeze candidate."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "data" / "manifests"
RAW_ROOT = ROOT / "data" / "raw" / "lai-gai" / "second-primary-resolution" / "20260714"
FORBIDDEN_KEYS = {
    "participantid",
    "prolific_id",
    "age",
    "gender",
    "country",
    "device",
    "date_of_completion",
    "prompt_gpt",
    "promt_gpt",
}
EMOTIONS = {
    "amusement",
    "awe",
    "anger",
    "attachment_love",
    "craving",
    "disgust",
    "excitement",
    "fear",
    "joy",
    "neutral",
    "nurturant_love",
    "sadness",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load(name: str) -> dict:
    return json.loads((MANIFESTS / name).read_text(encoding="utf-8"))


def all_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).casefold())
            keys.update(all_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(all_keys(child))
    return keys


def validate_lai_gai_second_primary() -> dict:
    raw = load("lai-gai-second-primary-raw-v1.manifest.json")
    split = load("lai-gai-split-v1.manifest.json")
    provenance = load("lai-gai-label-provenance-v1.manifest.json")
    label_map = load("second-primary-label-map-v1.manifest.json")
    canonical_path = ROOT / provenance["canonical_path"]
    records = [json.loads(line) for line in canonical_path.read_text(encoding="utf-8").splitlines() if line]
    images = {record["name"]: record for record in raw["images"]}
    split_records = split["records"]
    split_by_item = {record["item_id"]: record["split"] for record in split_records}
    group_splits: defaultdict[str, set[str]] = defaultdict(set)
    for record in split_records:
        group_splits[record["source_group_id"]].add(record["split"])

    image_fixity_failures = []
    for name, record in images.items():
        path = RAW_ROOT / "images" / name
        if not path.is_file() or path.stat().st_size != record["size_bytes"] or digest(path) != record["sha256"]:
            image_fixity_failures.append(name)
    score_fixity_failures = []
    for record in raw["score_files"]:
        path = RAW_ROOT / record["name"]
        if not path.is_file() or path.stat().st_size != record["size_bytes"] or digest(path) != record["sha256"]:
            score_fixity_failures.append(record["name"])

    canonical_errors = []
    for record in records:
        distribution = record.get("emotion_distribution") or {}
        if set(distribution) != EMOTIONS or abs(sum(distribution.values()) - 1.0) > 1e-9:
            canonical_errors.append(f"distribution:{record.get('item_id')}")
        if record.get("label_tier") != "HUMAN_GOLD" or record.get("response_count", 0) < 1:
            canonical_errors.append(f"label:{record.get('item_id')}")
        if record.get("split") != split_by_item.get(record.get("item_id")):
            canonical_errors.append(f"split:{record.get('item_id')}")
    forbidden = sorted(all_keys(records) & FORBIDDEN_KEYS)

    name_to_split = {
        record["image_name"]: record["split"] for record in records
    }
    exact_cross = 0
    near_cross = 0
    image_rows = list(images.values())
    for index, left in enumerate(image_rows):
        for right in image_rows[index + 1 :]:
            if left["sha256"] == right["sha256"] and name_to_split[left["name"]] != name_to_split[right["name"]]:
                exact_cross += 1
            if (
                bin(int(left["dhash64"], 16) ^ int(right["dhash64"], 16)).count("1") <= 4
                and name_to_split[left["name"]] != name_to_split[right["name"]]
            ):
                near_cross += 1

    split_counts = Counter(record["split"] for record in split_records)
    class_coverage = {
        split_name: set(split["target_emotion_provenance_counts"][split_name]) == EMOTIONS
        for split_name in ("train", "dev", "test")
    }
    raw_ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", "data/raw/lai-gai/second-primary-resolution/20260714/images/sample.jpg"],
        cwd=str(ROOT),
        check=False,
    ).returncode == 0
    processed_ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", provenance["canonical_path"]],
        cwd=str(ROOT),
        check=False,
    ).returncode == 0

    checks = {
        "image_count_847": len(images) == 847,
        "canonical_count_847": len(records) == 847,
        "split_count_847": len(split_records) == 847 and len(split_by_item) == 847,
        "image_fixity": not image_fixity_failures,
        "score_fixity": not score_fixity_failures,
        "canonical_hash": digest(canonical_path) == provenance["canonical_sha256"],
        "canonical_semantics": not canonical_errors,
        "sensitive_fields_absent": not forbidden,
        "group_overlap_zero": all(len(values) == 1 for values in group_splits.values()),
        "exact_duplicate_cross_split_zero": exact_cross == 0,
        "near_duplicate_cross_split_zero": near_cross == 0,
        "split_class_coverage": all(class_coverage.values()),
        "split_sizes": split_counts == Counter(split["counts"]),
        "raw_and_processed_ignored": raw_ignored and processed_ignored,
        "human_truth_only": provenance["truth_source"] == "independent human induced-affect ratings",
        "prompt_target_not_truth_or_input": (
            provenance["prompt_or_target_as_truth"] is False
            and provenance["prompt_available_to_model"] is False
            and provenance["target_emotion_available_to_model"] is False
            and label_map["prompt_or_target_category_used_as_truth"] is False
        ),
        "status_frozen_00_approved": (
            provenance["status"] == "FROZEN_00_APPROVED"
            and split["status"] == provenance["status"]
            and label_map["status"] == provenance["status"]
            and split["formal_split"] is True
            and provenance.get("review_id") == "REVIEW-00-LAI-GAI-FREEZE-20260715"
            and split.get("review_id") == provenance.get("review_id")
            and label_map.get("review_id") == provenance.get("review_id")
        ),
    }
    return {
        "passed": all(checks.values()),
        "status": "LAI_GAI_SECOND_PRIMARY_READY" if all(checks.values()) else "LEAKAGE_BLOCKED",
        "checks": checks,
        "counts": {
            "images": len(images),
            "canonical": len(records),
            "split": dict(sorted(split_counts.items())),
            "groups": len(group_splits),
            "exact_cross": exact_cross,
            "near_cross": near_cross,
        },
        "failures": {
            "image_fixity": image_fixity_failures[:10],
            "score_fixity": score_fixity_failures,
            "canonical": canonical_errors[:10],
            "forbidden_keys": forbidden,
            "class_coverage": class_coverage,
        },
    }


def main() -> int:
    result = validate_lai_gai_second_primary()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
