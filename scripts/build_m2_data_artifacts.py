"""Build deterministic M2 canonical artifacts without media, APIs, or training."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[1]
CSMV_REVISION = "99d14240254b1381dde0b9c56add140381f65117"
CSMV_ROOT = ROOT / "data" / "raw" / "csmv" / CSMV_REVISION
MANIFEST_ROOT = ROOT / "data" / "manifests"
PROCESSED_ROOT = ROOT / "data" / "processed"
CSMV_EMOTIONS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
CSMV_OPINIONS = ["negative", "neutral", "positive"]
VIDEO_SPLIT_SALT = "mmsa-csmv-group-by-video-v1"
HASHTAG_SPLIT_SALT = "mmsa-csmv-hashtag-heldout-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(namespace: str, value: str) -> str:
    return hashlib.sha256((namespace + "|" + value).encode("utf-8")).hexdigest()


def stable_split(value: str, salt: str) -> str:
    number = int(hashlib.sha256((salt + "|" + value).encode("utf-8")).hexdigest()[:16], 16)
    fraction = number / float(16 ** 16)
    if fraction < 0.70:
        return "train"
    if fraction < 0.80:
        return "dev"
    return "test"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Sequence[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def verify_source_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    raw_root = ROOT / manifest["raw_root"]
    for entry in manifest["files"]:
        source = raw_root / entry["relative_path"]
        if not source.is_file():
            raise FileNotFoundError(source)
        if source.stat().st_size != entry["bytes"] or sha256_file(source) != entry["sha256"]:
            raise ValueError("source manifest mismatch: {}".format(entry["relative_path"]))
    return manifest


def distribution(counts: Counter, classes: Sequence[str]) -> Tuple[dict, Optional[dict]]:
    total = sum(counts.get(label, 0) for label in classes)
    if not total:
        return {}, None
    probabilities = {label: counts.get(label, 0) / total for label in classes}
    entropy = -sum(value * math.log(value) for value in probabilities.values() if value > 0)
    uncertainty = {
        "valid_response_count": total,
        "entropy_nats": round(entropy, 12),
        "normalized_entropy": round(entropy / math.log(len(classes)), 12),
        "effective_class_count": round(math.exp(entropy), 12),
        "max_class_share": round(max(probabilities.values()), 12),
        "binomial_standard_error": {
            label: round(math.sqrt(value * (1.0 - value) / total), 12)
            for label, value in probabilities.items()
        },
    }
    return {key: round(value, 12) for key, value in probabilities.items()}, uncertainty


class UnionFind:
    def __init__(self) -> None:
        self.parent: Dict[str, str] = {}

    def find(self, value: str) -> str:
        self.parent.setdefault(value, value)
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[max(left_root, right_root)] = min(left_root, right_root)


def build_csmv() -> dict:
    source_manifest_path = MANIFEST_ROOT / "csmv-source-v1.manifest.json"
    source_manifest = verify_source_manifest(source_manifest_path)
    annotations = CSMV_ROOT / "CSMV" / "Comments_Anno"
    with zipfile.ZipFile(annotations / "lable_data_dict.json.zip") as archive:
        labels = json.loads(archive.read("lable_data_dict.json").decode("utf-8"))

    official_ids: List[str] = []
    split_counts = {}
    for split in ("train", "dev", "test"):
        ids = [str(value) for value in json.loads((annotations / (split + "_set.json")).read_text(encoding="utf-8"))]
        split_counts[split] = len(ids)
        official_ids.extend(ids)
    if len(official_ids) != len(set(official_ids)):
        raise ValueError("official comment IDs overlap")

    grouped = defaultdict(lambda: {"emotion": Counter(), "opinion": Counter(), "hashtags": set(), "responses": 0})
    for comment_id in official_ids:
        record = labels[comment_id]
        video_id = str(record["video_file_id"])
        group = grouped[video_id]
        group["responses"] += 1
        emotion = record.get("emotion_label")
        opinion = record.get("opinion_label")
        if emotion in CSMV_EMOTIONS:
            group["emotion"][emotion] += 1
        if opinion in CSMV_OPINIONS:
            group["opinion"][opinion] += 1
        hashtag = record.get("hashtag")
        values = hashtag if isinstance(hashtag, list) else [hashtag]
        for value in values:
            if value not in (None, ""):
                group["hashtags"].add(stable_id("csmv-hashtag-v1", str(value)))

    union_find = UnionFind()
    for group in grouped.values():
        hashtags = sorted(group["hashtags"])
        for value in hashtags:
            union_find.find(value)
        for value in hashtags[1:]:
            union_find.union(hashtags[0], value)

    records = []
    for video_id, group in grouped.items():
        item_id = stable_id("csmv-video-v1", video_id)
        hashtags = sorted(group["hashtags"])
        component = union_find.find(hashtags[0]) if hashtags else None
        emotion_dist, emotion_uncertainty = distribution(group["emotion"], CSMV_EMOTIONS)
        opinion_dist, opinion_uncertainty = distribution(group["opinion"], CSMV_OPINIONS)
        records.append(
            {
                "schema_version": "canonical-audience-affect-v1",
                "dataset_id": "CSMV@" + CSMV_REVISION,
                "item_id": item_id,
                "label_tier": "HUMAN_GOLD",
                "label_source": "csmv_public_human_comment_annotations",
                "available_at_t0": False,
                "source_group_id": item_id,
                "source_domain": "tiktok",
                "topic_id": None,
                "publisher_id": None,
                "publish_time": None,
                "response_count": group["responses"],
                "emotion_distribution": emotion_dist,
                "opinion_distribution": opinion_dist,
                "distribution_uncertainty": {
                    "emotion": emotion_uncertainty,
                    "opinion": opinion_uncertainty,
                    "missing_emotion": group["responses"] - sum(group["emotion"].values()),
                    "missing_opinion": group["responses"] - sum(group["opinion"].values()),
                },
                "hashtag_component_id": component,
                "native_label": None,
                "continuous_affect": None,
                "label_conflict": False,
                "duplicate_source_id": False,
                "missing_time": True,
                "legacy_features": None,
                "legacy_features_available_at_t0": False,
                "split": {
                    "group_by_video_v1": stable_split(item_id, VIDEO_SPLIT_SALT),
                    "hashtag_heldout_v1": stable_split(component, HASHTAG_SPLIT_SALT) if component else "not_assigned",
                    "topic_heldout_v1": "not_assigned",
                },
                "provenance": {
                    "source_manifest_sha256": sha256_file(source_manifest_path),
                    "source_revision": CSMV_REVISION,
                    "aggregation_version": "csmv-video-distribution-v1",
                    "comment_text_exported": False,
                },
            }
        )
    records.sort(key=lambda value: value["item_id"])

    output = PROCESSED_ROOT / "HUMAN_GOLD" / "csmv" / "video_labels.v1.jsonl"
    write_jsonl(output, records)
    split_summary = {}
    for scheme in ("group_by_video_v1", "hashtag_heldout_v1", "topic_heldout_v1"):
        split_summary[scheme] = dict(sorted(Counter(record["split"][scheme] for record in records).items()))

    raw_file_meta = {
        "train_set.json": (75086, ["comment_id"]),
        "dev_set.json": (10727, ["comment_id"]),
        "test_set.json": (21454, ["comment_id"]),
        "lable_data_dict.json.zip": (117057, ["video_file_id", "comment", "opinion_label", "emotion_label", "hashtag"]),
        "video_to_comment.json": (8210, ["video_file_id", "comment_ids"]),
        "emotion_label_map.json": (8, ["native_emotion", "class_index"]),
        "opinion_label_map.json": (3, ["native_opinion", "class_index"]),
        "CSMV_rawLinks.xlsx": (8210, ["video_file_id", "source_url_metadata"]),
    }
    enriched_files = []
    for entry in source_manifest["files"]:
        name = Path(entry["relative_path"]).name
        count, fields = raw_file_meta.get(name, (None, []))
        enriched_files.append(
            dict(
                entry,
                sample_count=count,
                sample_count_status="VERIFIED_OR_SOURCE_ALIGNED" if count is not None else "NOT_APPLICABLE",
                fields=fields,
                license="CC-BY-SA-4.0" if "Comments_Anno" in entry["relative_path"] else "ASSET_SPECIFIC_SEE_SOURCE",
            )
        )
    write_json(
        MANIFEST_ROOT / "csmv-primary-raw-v1.manifest.json",
        {
            "schema_version": "immutable-primary-raw-manifest-v1",
            "dataset_id": "CSMV@" + CSMV_REVISION,
            "status": "PRIMARY_HUMAN_GOLD_SOURCE",
            "source": "official MSA-CRVI repository fixed commit",
            "license": "annotations CC-BY-SA-4.0; code/media/features separately scoped",
            "source_manifest_sha256": sha256_file(source_manifest_path),
            "files": enriched_files,
            "immutable": True,
        },
    )
    write_json(
        MANIFEST_ROOT / "csmv-split-v1.manifest.json",
        {
            "schema_version": "split-v1",
            "dataset_id": "CSMV@" + CSMV_REVISION,
            "created_from": "aggregated video records before any index or fit",
            "video_split_salt": VIDEO_SPLIT_SALT,
            "hashtag_split_salt": HASHTAG_SPLIT_SALT,
            "counts": split_summary,
            "group_overlap_allowed": False,
            "topic_status": "BLOCKED_NATIVE_TOPIC_ABSENT",
            "index_status": "NOT_BUILT",
            "future_index_scope": "TRAIN_ONLY",
        },
    )
    write_json(
        MANIFEST_ROOT / "human-gold-v1.manifest.json",
        {
            "schema_version": "label-tier-manifest-v1",
            "tier": "HUMAN_GOLD",
            "dataset_id": "CSMV@" + CSMV_REVISION,
            "path": str(output.relative_to(ROOT)).replace(os.sep, "/"),
            "records": len(records),
            "sha256": sha256_file(output),
            "contains_comment_text": False,
            "merge_with_silver": "PROHIBITED",
        },
    )
    return {"records": len(records), "split_counts": split_summary, "official_comment_counts": split_counts}


def video_id(value: str) -> str:
    match = re.search(r"BV[0-9A-Za-z]+", value or "")
    return match.group(0) if match else ""


def csv_rows(path: Path, delimiter: str) -> Tuple[List[str], List[List[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, delimiter=delimiter)
        header = next(reader, [])
        return header, list(reader)


def build_cuc(cuc_root: Path) -> dict:
    if not cuc_root.is_dir():
        raise FileNotFoundError(cuc_root)
    source_files = []
    canonical = []
    bv_counts = Counter()
    global_timestamps = {}
    global_timestamp_publishers = defaultdict(set)

    # Build the global timestamp lookup separately. A local miss with a global hit is
    # retained as an explicit cross-publisher metadata warning, not silently treated
    # as ordinary local provenance.
    for path in sorted(cuc_root.rglob("6.发布者视频列表.csv")):
        publisher_key = str(path.parent.relative_to(cuc_root)).replace(os.sep, "/")
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream, delimiter=";"):
                identifier = video_id(row.get("视频地址", ""))
                if identifier and row.get("发布时间"):
                    global_timestamps.setdefault(identifier, row["发布时间"])
                    global_timestamp_publishers[identifier].add(publisher_key)

    for topic_path in sorted(path for path in cuc_root.iterdir() if path.is_dir()):
        for publisher_path in sorted(path for path in topic_path.iterdir() if path.is_dir()):
            relative_publisher = str(publisher_path.relative_to(cuc_root)).replace(os.sep, "/")
            topic_id = stable_id("cuc-topic-v1", topic_path.name)
            publisher_id = stable_id("cuc-publisher-v1", relative_publisher)
            label_path = publisher_path / "3.视频群体情绪值对应.csv"
            vector_path = publisher_path / "5.预测向量.csv"
            video_path = publisher_path / "6.发布者视频列表.csv"
            local_labels = defaultdict(list)
            timestamps = {}

            for path, delimiter, kind in (
                (label_path, ",", "label"),
                (vector_path, ";", "vector"),
                (video_path, ";", "video_metadata"),
            ):
                if not path.is_file():
                    continue
                header, rows = csv_rows(path, delimiter)
                source_files.append(
                    {
                        "path_id": stable_id("cuc-source-path-v1", str(path.relative_to(cuc_root)).replace(os.sep, "/")),
                        "kind": kind,
                        "source": "EXTERNAL_LOCAL_READ_ONLY_PATH_ID",
                        "license": "UNKNOWN_NOT_CLEARED_FOR_REDISTRIBUTION",
                        "bytes": path.stat().st_size,
                        "sha256": sha256_file(path),
                        "sample_count": len(rows),
                        "fields": [value.strip() for value in header if value.strip()],
                    }
                )

            if label_path.is_file():
                with label_path.open("r", encoding="utf-8-sig", newline="") as stream:
                    for row_number, row in enumerate(csv.DictReader(stream), 2):
                        try:
                            affect = float(row["群体情绪"])
                        except (KeyError, TypeError, ValueError):
                            continue
                        fallback = int(affect > 0.5217 or affect < -0.2558)
                        try:
                            local_label = int(float(row["极端情绪分类"]))
                            source = "explicit"
                        except (KeyError, TypeError, ValueError):
                            local_label = fallback
                            source = "legacy_threshold_fallback"
                        identifier = video_id(row.get("视频地址", "") or row.get("urls", ""))
                        if identifier:
                            local_labels[identifier].append((affect, local_label, source, row_number))

            if video_path.is_file():
                with video_path.open("r", encoding="utf-8-sig", newline="") as stream:
                    for row in csv.DictReader(stream, delimiter=";"):
                        identifier = video_id(row.get("视频地址", ""))
                        if identifier and row.get("发布时间"):
                            timestamps[identifier] = row["发布时间"]

            if not vector_path.is_file():
                continue
            with vector_path.open("r", encoding="utf-8-sig", newline="") as stream:
                reader = csv.reader(stream, delimiter=";")
                next(reader, None)
                for row_number, row in enumerate(reader, 2):
                    if len(row) < 49:
                        continue
                    try:
                        features = [float(value) for value in row[:48]]
                        native_label = int(float(row[48]))
                    except ValueError:
                        continue
                    identifier = video_id(row[49]) if len(row) > 49 else ""
                    if identifier:
                        bv_counts[identifier] += 1
                        item_id = stable_id("cuc-bv-v1", identifier)
                    else:
                        item_id = stable_id("cuc-missing-bv-v1", relative_publisher + "|" + str(row_number))
                    matching = local_labels.get(identifier, [])
                    conflict = bool(matching) and not any(value[1] == native_label for value in matching)
                    publish_time = timestamps.get(identifier) or global_timestamps.get(identifier)
                    timestamp_scope = (
                        "LOCAL_PUBLISHER"
                        if identifier in timestamps
                        else "GLOBAL_CROSS_PUBLISHER"
                        if identifier in global_timestamps
                        else "MISSING"
                    )
                    canonical.append(
                        {
                            "schema_version": "canonical-audience-affect-v1",
                            "dataset_id": "CUC-IGPE-v2@legacy-2787",
                            "item_id": item_id,
                            "label_tier": "SILVER",
                            "label_source": "silver_legacy_vector_binary_label",
                            "available_at_t0": False,
                            "source_group_id": item_id if identifier else None,
                            "source_domain": "bilibili",
                            "topic_id": topic_id,
                            "publisher_id": publisher_id,
                            "publish_time": publish_time,
                            "response_count": 0,
                            "emotion_distribution": None,
                            "opinion_distribution": None,
                            "distribution_uncertainty": None,
                            "hashtag_component_id": None,
                            "native_label": native_label,
                            "continuous_affect": matching[0][0] if matching else None,
                            "label_conflict": conflict,
                            "duplicate_source_id": False,
                            "missing_time": publish_time is None,
                            "legacy_features": features,
                            "legacy_features_available_at_t0": False,
                            "split": {
                                "group_by_video_v1": "not_assigned",
                                "publisher_heldout_v1": "not_assigned",
                                "topic_heldout_v1": "not_assigned",
                            },
                            "provenance": {
                                "source_path_id": stable_id("cuc-source-path-v1", str(vector_path.relative_to(cuc_root)).replace(os.sep, "/")),
                                "source_row": row_number,
                                "local_label_record_count": len(matching),
                                "teacher_model": "UNKNOWN_LEGACY_TEACHER",
                                "confidence": None,
                                "pipeline_version": "cuc-igpe-v2-legacy-import-v1",
                                "timestamp_scope": timestamp_scope,
                            },
                        }
                    )

    duplicate_ids = {identifier for identifier, count in bv_counts.items() if count > 1}
    for record in canonical:
        # A duplicate hashed item ID is sufficient here; raw BV values are never exported.
        record["duplicate_source_id"] = sum(1 for item in canonical if item["item_id"] == record["item_id"]) > 1
    canonical.sort(key=lambda value: (value["item_id"], value["provenance"]["source_path_id"], value["provenance"]["source_row"]))

    output = PROCESSED_ROOT / "SILVER" / "cuc_igpe_v2" / "canonical.v1.jsonl"
    write_jsonl(output, canonical)
    issues = []
    for record in canonical:
        codes = []
        if record["label_conflict"]:
            codes.append("LABEL_CONFLICT")
        if record["source_group_id"] is None:
            codes.append("MISSING_BV")
        if record["missing_time"]:
            codes.append("MISSING_PUBLISH_TIME")
        if record["duplicate_source_id"]:
            codes.append("DUPLICATE_BV")
        if codes:
            issues.append({"item_id": record["item_id"], "issue_codes": codes, "review_status": "PENDING_HUMAN"})
    issues.sort(key=lambda value: ("LABEL_CONFLICT" not in value["issue_codes"], "MISSING_BV" not in value["issue_codes"], value["item_id"]))
    review_output = PROCESSED_ROOT / "SILVER" / "cuc_igpe_v2" / "error_review_candidates.v1.jsonl"
    write_jsonl(review_output, issues[:100])

    stats = {
        "canonical_records": len(canonical),
        "records_with_bv": sum(record["source_group_id"] is not None for record in canonical),
        "missing_bv": sum(record["source_group_id"] is None for record in canonical),
        "duplicate_bv_rows": sum(record["duplicate_source_id"] for record in canonical),
        "label_conflicts": sum(record["label_conflict"] for record in canonical),
        "publish_time_present": sum(not record["missing_time"] for record in canonical),
        "publish_time_missing": sum(record["missing_time"] for record in canonical),
        "cross_publisher_timestamp_matches": sum(
            record["provenance"]["timestamp_scope"] == "GLOBAL_CROSS_PUBLISHER"
            for record in canonical
        ),
        "review_candidates": min(100, len(issues)),
    }
    write_json(
        MANIFEST_ROOT / "cuc-auxiliary-raw-v1.manifest.json",
        {
            "schema_version": "immutable-auxiliary-raw-manifest-v1",
            "dataset_id": "CUC-IGPE-v2@legacy-local",
            "status": "AUXILIARY_SILVER_LOCAL_ONLY",
            "source": "external local read-only root supplied at runtime",
            "license": "UNKNOWN_NOT_CLEARED_FOR_REDISTRIBUTION",
            "files": sorted(source_files, key=lambda value: (value["path_id"], value["kind"])),
            "raw_file_count": len(source_files),
            "immutable": True,
        },
    )
    write_json(
        MANIFEST_ROOT / "cuc-canonical-v1.manifest.json",
        {
            "schema_version": "canonical-dataset-manifest-v1",
            "dataset_id": "CUC-IGPE-v2@legacy-2787",
            "tier": "SILVER",
            "output_path": str(output.relative_to(ROOT)).replace(os.sep, "/"),
            "output_sha256": sha256_file(output),
            "stats": stats,
            "historical_expected_records": 2815,
            "current_records": len(canonical),
            "unresolved_drift": 2815 - len(canonical),
            "drift_status": "UNRESOLVED_NO_2815_MANIFEST",
            "license_status": "UNKNOWN_LOCAL_ONLY",
            "t0_feature_status": "LEGACY_48_BLOCKED_NOT_PROVEN_AT_T0",
        },
    )
    write_json(
        MANIFEST_ROOT / "silver-v1.manifest.json",
        {
            "schema_version": "label-tier-manifest-v1",
            "tier": "SILVER",
            "dataset_id": "CUC-IGPE-v2@legacy-2787",
            "path": str(output.relative_to(ROOT)).replace(os.sep, "/"),
            "records": len(canonical),
            "sha256": sha256_file(output),
            "pipeline_config": "configs/silver-label-pipeline-v1.yaml",
            "teacher_model": "UNKNOWN_LEGACY_TEACHER",
            "confidence_status": "UNKNOWN_NOT_RECORDED",
            "merge_with_human_gold": "PROHIBITED",
        },
    )
    write_json(
        MANIFEST_ROOT / "label-error-review-v1.manifest.json",
        {
            "schema_version": "label-error-review-manifest-v1",
            "purpose": "DATA_DEFECT_DISCOVERY_ONLY",
            "path": str(review_output.relative_to(ROOT)).replace(os.sep, "/"),
            "records": min(100, len(issues)),
            "sha256": sha256_file(review_output),
            "status": "PENDING_HUMAN_REVIEW",
            "formal_model_superiority_evidence": False,
        },
    )
    return stats


def write_fixed_manifests() -> None:
    mapping = ROOT / "LABEL_SPACE_MAPPING_DRAFT.md"
    write_json(
        MANIFEST_ROOT / "second-primary-label-map-v1.manifest.json",
        {
            "schema_version": "label-map-manifest-v1",
            "version": "v1",
            "status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
            "mapping_document": "LABEL_SPACE_MAPPING_DRAFT.md",
            "mapping_document_sha256": sha256_file(mapping),
            "test_result_tuning_allowed": False,
            "g1_effect": "BLOCKED",
        },
    )
    unlabeled = PROCESSED_ROOT / "UNLABELED"
    unlabeled.mkdir(parents=True, exist_ok=True)
    write_json(
        MANIFEST_ROOT / "unlabeled-v1.manifest.json",
        {
            "schema_version": "label-tier-manifest-v1",
            "tier": "UNLABELED",
            "records": 0,
            "status": "EMPTY_RESERVED_ENTRY_POINT",
            "merge_with_labeled_eval": "PROHIBITED",
        },
    )
    tier_manifests = [
        "human-gold-v1.manifest.json",
        "silver-v1.manifest.json",
        "unlabeled-v1.manifest.json",
    ]
    write_json(
        MANIFEST_ROOT / "label-provenance-v1.manifest.json",
        {
            "schema_version": "label-provenance-v1",
            "tiers": [
                {"manifest": name, "sha256": sha256_file(MANIFEST_ROOT / name)}
                for name in tier_manifests
            ],
            "physical_roots": {
                "HUMAN_GOLD": "data/processed/HUMAN_GOLD",
                "SILVER": "data/processed/SILVER",
                "UNLABELED": "data/processed/UNLABELED",
            },
            "mixed_tier_loading": "PROHIBITED",
            "public_human_test_with_silver": "PROHIBITED",
        },
    )
    write_json(
        MANIFEST_ROOT / "index-boundary-v1.manifest.json",
        {
            "schema_version": "index-boundary-v1",
            "status": "NOT_BUILT",
            "required_build_order": ["freeze_raw_manifest", "aggregate_by_item", "assign_split", "select_train_only", "build_index"],
            "allowed_fit_split": "train",
            "dev_test_candidates_in_index": "PROHIBITED",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuc-root", type=Path, required=True)
    args = parser.parse_args()
    for tier in ("HUMAN_GOLD", "SILVER", "UNLABELED"):
        (PROCESSED_ROOT / tier).mkdir(parents=True, exist_ok=True)
    csmv = build_csmv()
    cuc = build_cuc(args.cuc_root.resolve())
    write_fixed_manifests()
    print(json.dumps({"schema": "m2-build-summary-v1", "csmv": csmv, "cuc": cuc}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
