"""Deterministic acceptance checks for M2 steps 24--33."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from load_label_tier import count_tier


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "data" / "manifests"
FORBIDDEN = {"comment", "comments", "comment_text", "target_comment", "target_comments"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def validate_m2_data_engineering() -> dict:
    required = [
        "DATA_DICTIONARY.md",
        "M2_DATA_PROTOCOL.md",
        "SILVER_LABEL_PROTOCOL.md",
        "LABEL_ERROR_REVIEW_PROTOCOL.md",
        "NEAR_DUPLICATE_SOURCE_AUDIT.md",
        "CUC_CANONICAL_AUDIT.md",
        "configs/silver-label-pipeline-v1.yaml",
        "scripts/build_m2_data_artifacts.py",
        "scripts/load_label_tier.py",
        "data/manifests/canonical-audience-affect-v1.schema.json",
        "data/manifests/csmv-primary-raw-v1.manifest.json",
        "data/manifests/csmv-split-v1.manifest.json",
        "data/manifests/cuc-auxiliary-raw-v1.manifest.json",
        "data/manifests/cuc-canonical-v1.manifest.json",
        "data/manifests/human-gold-v1.manifest.json",
        "data/manifests/silver-v1.manifest.json",
        "data/manifests/unlabeled-v1.manifest.json",
        "data/manifests/label-provenance-v1.manifest.json",
        "data/manifests/second-primary-label-map-v1.manifest.json",
        "data/manifests/index-boundary-v1.manifest.json",
        "data/manifests/label-error-review-v1.manifest.json",
    ]
    missing = [value for value in required if not (ROOT / value).is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"passed": False, "checks": checks, "g1_passed": False}

    csmv_raw = read_json(MANIFEST_ROOT / "csmv-primary-raw-v1.manifest.json")
    cuc_raw = read_json(MANIFEST_ROOT / "cuc-auxiliary-raw-v1.manifest.json")
    raw_fields_complete = all(
        "sample_count" in entry and "fields" in entry and "sha256" in entry and "license" in entry
        for entry in csmv_raw["files"]
    ) and all(
        "sample_count" in entry and "fields" in entry and "sha256" in entry
        and "source" in entry and "license" in entry
        for entry in cuc_raw["files"]
    )
    checks["immutable_raw_manifests"] = {
        "passed": csmv_raw.get("immutable") is True and cuc_raw.get("immutable") is True and raw_fields_complete,
        "csmv_files": len(csmv_raw["files"]),
        "cuc_files": len(cuc_raw["files"]),
    }

    human_manifest = read_json(MANIFEST_ROOT / "human-gold-v1.manifest.json")
    silver_manifest = read_json(MANIFEST_ROOT / "silver-v1.manifest.json")
    human_path = ROOT / human_manifest["path"]
    silver_path = ROOT / silver_manifest["path"]
    human = list(read_jsonl(human_path))
    silver = list(read_jsonl(silver_path))
    mixed_tier_guard = False
    try:
        count_tier(human_path, "SILVER")
    except ValueError:
        mixed_tier_guard = True
    checks["physical_label_tiers"] = {
        "passed": (
            human_path.parent.parts[-2] == "HUMAN_GOLD"
            and silver_path.parent.parts[-2] == "SILVER"
            and (ROOT / "data" / "processed" / "UNLABELED").is_dir()
            and count_tier(human_path, "HUMAN_GOLD") == 8210
            and count_tier(silver_path, "SILVER") == 2787
            and mixed_tier_guard
        ),
        "human_records": len(human),
        "silver_records": len(silver),
        "mixed_tier_negative_test": mixed_tier_guard,
    }

    item_ids = [record["item_id"] for record in human]
    response_total = sum(record["response_count"] for record in human)
    forbidden_hits = sum(bool(FORBIDDEN & set(record)) for record in human + silver)
    component_splits = defaultdict(set)
    for record in human:
        component = record.get("hashtag_component_id")
        if component:
            component_splits[component].add(record["split"]["hashtag_heldout_v1"])
    distributions_valid = all(
        abs(sum(record["emotion_distribution"].values()) - 1.0) < 1e-8
        and abs(sum(record["opinion_distribution"].values()) - 1.0) < 1e-8
        for record in human
    )
    checks["csmv_aggregation_and_split"] = {
        "passed": (
            len(human) == 8210
            and len(item_ids) == len(set(item_ids))
            and response_total == 107267
            and distributions_valid
            and all(len(values) == 1 for values in component_splits.values())
            and forbidden_hits == 0
        ),
        "records": len(human),
        "response_total": response_total,
        "hashtag_components": len(component_splits),
        "cross_split_hashtag_components": sum(len(values) > 1 for values in component_splits.values()),
        "forbidden_text_field_hits": forbidden_hits,
    }

    split_manifest = read_json(MANIFEST_ROOT / "csmv-split-v1.manifest.json")
    index_manifest = read_json(MANIFEST_ROOT / "index-boundary-v1.manifest.json")
    checks["split_before_index"] = {
        "passed": split_manifest["index_status"] == "NOT_BUILT" and index_manifest["allowed_fit_split"] == "train",
        "index_status": split_manifest["index_status"],
    }

    cuc_stats = read_json(MANIFEST_ROOT / "cuc-canonical-v1.manifest.json")["stats"]
    actual_cuc = {
        "canonical_records": len(silver),
        "missing_bv": sum(record["source_group_id"] is None for record in silver),
        "duplicate_bv_rows": sum(record["duplicate_source_id"] for record in silver),
        "label_conflicts": sum(record["label_conflict"] for record in silver),
        "publish_time_present": sum(not record["missing_time"] for record in silver),
        "cross_publisher_timestamp_matches": sum(
            record["provenance"].get("timestamp_scope") == "GLOBAL_CROSS_PUBLISHER" for record in silver
        ),
    }
    expected_cuc = {
        "canonical_records": 2787,
        "missing_bv": 8,
        "duplicate_bv_rows": 0,
        "label_conflicts": 221,
        "publish_time_present": 883,
        "cross_publisher_timestamp_matches": 1,
    }
    checks["cuc_canonical"] = {
        "passed": actual_cuc == expected_cuc and all(cuc_stats[key] == value for key, value in expected_cuc.items()),
        "actual": actual_cuc,
        "expected": expected_cuc,
    }

    mapping = read_json(MANIFEST_ROOT / "second-primary-label-map-v1.manifest.json")
    checks["second_primary_mapping"] = {
        "passed": mapping["status"] == "BLOCKED_SECOND_PRIMARY_NOT_FROZEN" and mapping["test_result_tuning_allowed"] is False,
        "status": mapping["status"],
    }
    review = read_json(MANIFEST_ROOT / "label-error-review-v1.manifest.json")
    checks["error_review"] = {
        "passed": review["records"] == 100 and review["status"] == "PENDING_HUMAN_REVIEW" and review["formal_model_superiority_evidence"] is False,
        "records": review["records"],
    }
    passed = all(result["passed"] for result in checks.values())
    return {
        "schema": "m2-data-engineering-check-v1",
        "passed": passed,
        "m2_local_artifacts_ready": passed,
        "g1_passed": False,
        "g1_status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
        "g2_passed": False,
        "g2_status": "NOT_EVALUATED_G1_BLOCKED",
        "checks": checks,
    }


def main() -> int:
    report = validate_m2_data_engineering()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
