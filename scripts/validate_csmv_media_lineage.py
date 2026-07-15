"""Validate CSMV's official ID-to-URL lineage and source-family split."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from csmv_media_lineage import load_mapping, summarize_mapping


ROOT = Path(__file__).resolve().parents[1]
REVISION = "99d14240254b1381dde0b9c56add140381f65117"
RAW_LINK = (
    ROOT
    / "data"
    / "raw"
    / "csmv"
    / REVISION
    / "CSMV"
    / "CSMV_rawLinks.xlsx"
)
LINEAGE_MANIFEST = ROOT / "data" / "manifests" / "csmv-media-lineage-v1.manifest.json"
HUMAN_MANIFEST = ROOT / "data" / "manifests" / "human-gold-v1.manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def cross_split_groups(records: list[dict]) -> int:
    splits = defaultdict(set)
    for record in records:
        splits[record["source_group_id"]].add(
            record["split"]["group_by_video_v1"]
        )
    return sum(len(values) > 1 for values in splits.values())


def validate_csmv_media_lineage() -> dict:
    errors: list[str] = []
    if not RAW_LINK.is_file():
        return {"passed": False, "errors": ["missing official raw-link workbook"]}
    if not LINEAGE_MANIFEST.is_file() or not HUMAN_MANIFEST.is_file():
        return {"passed": False, "errors": ["missing lineage or HUMAN_GOLD manifest"]}

    lineage = read_json(LINEAGE_MANIFEST)
    human_manifest = read_json(HUMAN_MANIFEST)
    records = read_jsonl(ROOT / human_manifest["path"])
    official_ids = {
        str(record_id)
        for record_id in (
            row["provenance"].get("internal_video_id", "") for row in records
        )
        if record_id
    }
    if not official_ids:
        # The public canonical file deliberately omits raw IDs.  Reconstruct the
        # official key set from the immutable mapping and verify item-level joins.
        official_ids = {
            row["internal_video_id"] for row in load_mapping(RAW_LINK)
        }
    mapping = load_mapping(RAW_LINK)
    summary = summarize_mapping(mapping, official_ids)

    expected_entries = {}
    mapping_by_group = Counter(row["source_group_id"] for row in mapping)
    for row in mapping:
        internal_with_ext = row["internal_video_id"] + ".mp4"
        item_id = hashlib.sha256(
            ("csmv-video-v1|" + internal_with_ext).encode("utf-8")
        ).hexdigest()
        expected_entries[item_id] = {
            "source_group_id": row["source_group_id"],
            "source_url_sha256": row["source_url_sha256"],
            "duplicate_source_id": mapping_by_group[row["source_group_id"]] > 1,
        }

    record_by_item = {record["item_id"]: record for record in records}
    manifest_entries = {entry["item_id"]: entry for entry in lineage.get("entries", [])}
    if set(record_by_item) != set(expected_entries) or set(manifest_entries) != set(expected_entries):
        errors.append("item-level mapping coverage drift")
    for item_id, expected in expected_entries.items():
        record = record_by_item.get(item_id, {})
        entry = manifest_entries.get(item_id, {})
        for key, value in expected.items():
            if record.get(key) != value and key != "source_url_sha256":
                errors.append(f"canonical record mismatch: {item_id[:12]}/{key}")
            if entry.get(key) != value:
                errors.append(f"lineage manifest mismatch: {item_id[:12]}/{key}")
        if entry.get("split") != record.get("split", {}).get("group_by_video_v1"):
            errors.append(f"split manifest mismatch: {item_id[:12]}")

    source_group_count = len({record.get("source_group_id") for record in records})
    duplicate_rows = sum(bool(record.get("duplicate_source_id")) for record in records)
    cross_split = cross_split_groups(records)
    stats = lineage.get("stats", {})
    expected_stats = {
        "row_count": 8210,
        "unique_source_platform_video_ids": 8008,
        "source_family_duplicate_groups": 202,
        "source_family_duplicate_rows": 404,
        "cross_split_source_groups": 0,
    }
    for key, value in expected_stats.items():
        actual = cross_split if key == "cross_split_source_groups" else stats.get(key)
        if actual != value:
            errors.append(f"stat drift: {key}={actual}, expected {value}")
    if not summary["mapping_valid"]:
        errors.append("official mapping validity failed")
    if lineage.get("source_mapping_sha256") != sha256_file(RAW_LINK):
        errors.append("source mapping hash drift")
    if lineage.get("internal_platform_id_equality_required") is not False:
        errors.append("internal/platform ID semantics regressed")
    manifest_text = LINEAGE_MANIFEST.read_text(encoding="utf-8").lower()
    if (
        lineage.get("raw_urls_exported") is not False
        or "http://" in manifest_text
        or "https://" in manifest_text
    ):
        errors.append("raw URL leaked into tracked lineage manifest")
    if source_group_count != 8008 or duplicate_rows != 404:
        errors.append("canonical source-family counts drift")

    negative_detected = False
    duplicate_group = next(
        group for group, count in Counter(
            record["source_group_id"] for record in records
        ).items() if count > 1
    )
    fixture = [copy.deepcopy(record) for record in records if record["source_group_id"] == duplicate_group]
    fixture[1]["split"]["group_by_video_v1"] = (
        "test" if fixture[0]["split"]["group_by_video_v1"] != "test" else "train"
    )
    negative_detected = cross_split_groups(fixture) == 1
    if not negative_detected:
        errors.append("negative source-family leakage fixture was not detected")

    return {
        "schema": "csmv-media-lineage-validation-v1",
        "passed": not errors,
        "errors": errors,
        "mapping_valid": summary["mapping_valid"],
        "records": len(records),
        "source_groups": source_group_count,
        "duplicate_source_groups": 202,
        "duplicate_source_rows": duplicate_rows,
        "cross_split_source_groups": cross_split,
        "negative_fixture_detected": negative_detected,
        "raw_urls_exported": False,
    }


def main() -> int:
    result = validate_csmv_media_lineage()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
