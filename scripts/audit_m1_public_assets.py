#!/usr/bin/env python3
"""Audit downloaded M1 public metadata without emitting raw text or identifiers."""

from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import statistics
import zipfile
from collections import Counter
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "data" / "manifests"
OUTPUT = MANIFEST_DIR / "m1-public-audit-v1.manifest.json"
DIRECT6 = {
    "anger": "anger",
    "disgust": "disgust",
    "fear": "fear",
    "happy": "joy",
    "joy": "joy",
    "sad": "sadness",
    "sadness": "sadness",
    "surprise": "surprise",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def verify_manifest(name: str) -> tuple[dict, Path]:
    manifest_path = MANIFEST_DIR / f"{name}-source-v1.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_root = ROOT / manifest["raw_root"]
    for item in manifest["files"]:
        path = raw_root / item["relative_path"]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            raise ValueError(f"manifest mismatch: {name}/{item['relative_path']}")
    return manifest, raw_root


def audit_csmv(raw_root: Path) -> dict:
    annotations = raw_root / "CSMV" / "Comments_Anno"
    with zipfile.ZipFile(annotations / "lable_data_dict.json.zip") as archive:
        labels = json.loads(archive.read("lable_data_dict.json").decode("utf-8"))

    split_ids: dict[str, list[str]] = {}
    split_videos: dict[str, set[str]] = {}
    for split in ("train", "dev", "test"):
        ids = [str(value) for value in json.loads((annotations / f"{split}_set.json").read_text(encoding="utf-8"))]
        missing = [value for value in ids if value not in labels]
        if missing:
            raise ValueError(f"{split} has {len(missing)} unknown comment ids")
        split_ids[split] = ids
        split_videos[split] = {str(labels[value]["video_file_id"]) for value in ids}

    official_ids = [value for values in split_ids.values() for value in values]
    official_records = [labels[value] for value in official_ids]
    video_map = json.loads((annotations / "video_to_comment.json").read_text(encoding="utf-8"))
    hashtag_types = Counter(type(record.get("hashtag")).__name__ for record in official_records)
    hashtag_values: set[str] = set()
    missing_hashtag = 0
    for record in official_records:
        value = record.get("hashtag")
        if value in (None, "", []):
            missing_hashtag += 1
        elif isinstance(value, list):
            hashtag_values.update(str(item) for item in value if str(item).strip())
        else:
            hashtag_values.add(str(value))

    emotion_counts = Counter(str(record["emotion_label"]) for record in official_records)
    opinion_counts = Counter(str(record["opinion_label"]) for record in official_records)
    direct6_count = sum(
        count for label, count in emotion_counts.items() if label.lower() in DIRECT6
    )
    pair_overlaps = {
        f"{left}_{right}": len(split_videos[left] & split_videos[right])
        for left, right in combinations(("train", "dev", "test"), 2)
    }
    return {
        "comment_records_in_label_archive": len(labels),
        "official_split_comment_counts": {key: len(value) for key, value in split_ids.items()},
        "official_split_comment_total": len(official_ids),
        "comment_id_split_overlap": len(official_ids) - len(set(official_ids)),
        "video_to_comment_video_count": len(video_map),
        "unique_video_count_in_official_splits": len(
            set().union(*split_videos.values())
        ),
        "unique_video_counts_by_split": {
            key: len(value) for key, value in split_videos.items()
        },
        "video_overlap_between_official_splits": pair_overlaps,
        "video_overlap_all_three": len(set.intersection(*split_videos.values())),
        "required_record_fields": sorted(
            set.intersection(*(set(record) for record in official_records))
        ),
        "missing_video_file_id": sum(
            not str(record.get("video_file_id", "")).strip() for record in official_records
        ),
        "hashtag_types": dict(sorted(hashtag_types.items())),
        "missing_hashtag": missing_hashtag,
        "unique_hashtag_values": len(hashtag_values),
        "emotion_counts": dict(sorted(emotion_counts.items())),
        "opinion_counts": dict(sorted(opinion_counts.items())),
        "direct6_retained_rows": direct6_count,
        "direct6_dropped_rows": len(official_records) - direct6_count,
        "direct6_retained_fraction": round(direct6_count / len(official_records), 6),
        "group_by_video_constructable": len(video_map) == 8210,
        "hashtag_held_out_constructable": missing_hashtag == 0 and bool(hashtag_values),
        "native_topic_field_present": all("topic" in record for record in official_records),
        "official_comment_split_is_video_leaky": any(pair_overlaps.values()),
    }


def audit_inews(raw_root: Path) -> dict:
    rows: list[dict[str, str]] = []
    split_posts: dict[str, set[str]] = {}
    split_row_counts: dict[str, int] = {}
    fields_by_file: dict[str, list[str]] = {}
    for path in sorted(raw_root.glob("*.csv")):
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            current = list(reader)
            fields_by_file[path.name] = list(reader.fieldnames or [])
        rows.extend(current)
        split_posts[path.name] = {row["Post_ID"] for row in current}
        split_row_counts[path.name] = len(current)

    discrete = Counter(row["Discrete"] for row in rows)
    direct6_count = sum(
        count for label, count in discrete.items() if label.lower() in DIRECT6
    )
    retained_posts = {
        row["Post_ID"] for row in rows if row["Discrete"].lower() in DIRECT6
    }
    all_posts = {row["Post_ID"] for row in rows}
    annotations_per_post = Counter(row["Post_ID"] for row in rows)
    overlaps = {
        f"{left}|{right}": len(split_posts[left] & split_posts[right])
        for left, right in combinations(sorted(split_posts), 2)
        if split_posts[left] & split_posts[right]
    }
    return {
        "row_count": len(rows),
        "unique_post_count": len(all_posts),
        "paper_post_count": 2899,
        "public_post_shortfall_vs_paper": 2899 - len(all_posts),
        "split_row_counts": split_row_counts,
        "unique_posts_by_file": {
            name: len(posts) for name, posts in split_posts.items()
        },
        "post_overlap_between_public_files": overlaps,
        "required_fields_common_to_all_csv": sorted(
            set.intersection(*(set(value) for value in fields_by_file.values()))
        ),
        "discrete_counts": dict(sorted(discrete.items())),
        "vad_range": {
            key: [min(float(row[key]) for row in rows), max(float(row[key]) for row in rows)]
            for key in "VAD"
        },
        "source_condition_counts": dict(
            sorted(Counter(row["Source"] for row in rows).items())
        ),
        "annotations_per_post_min_median_max": [
            min(annotations_per_post.values()),
            statistics.median(annotations_per_post.values()),
            max(annotations_per_post.values()),
        ],
        "direct6_retained_rows": direct6_count,
        "direct6_dropped_rows": len(rows) - direct6_count,
        "direct6_retained_fraction": round(direct6_count / len(rows), 6),
        "direct6_retained_posts": len(retained_posts),
        "direct6_posts_with_no_retained_annotation": len(all_posts - retained_posts),
        "media_file_field_present": any(
            field.lower() in {"image", "image_path", "image_url", "media", "media_path"}
            for field in set.intersection(*(set(value) for value in fields_by_file.values()))
        ),
        "post_group_resplit_constructable_for_labels": bool(all_posts),
    }


def audit_nemo(raw_root: Path) -> dict:
    package = raw_root / "2022.aacl-main.29.Dataset.zip"
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        data = archive.read("NEmoP/NEmoP.csv").decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(data))
    rows = list(reader)
    conditions = ("text_responses", "image_responses", "textimage_responses")
    condition_counts: dict[str, int] = {}
    label_counts: Counter[str] = Counter()
    for field in conditions:
        count = 0
        for row in rows:
            responses = ast.literal_eval(row[field])
            count += len(responses)
            label_counts.update(str(response["emotion"]) for response in responses)
        condition_counts[field] = count
    image_entries = [
        name for name in names if Path(name).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    license_entries = [
        name for name in names if "license" in Path(name).name.lower() or "copying" in Path(name).name.lower()
    ]
    direct6_count = sum(
        count for label, count in label_counts.items() if label.lower() in DIRECT6
    )
    return {
        "news_item_count": len(rows),
        "response_counts_by_condition": condition_counts,
        "total_response_count": sum(condition_counts.values()),
        "emotion_counts": dict(sorted(label_counts.items())),
        "direct6_retained_responses": direct6_count,
        "direct6_dropped_responses": sum(label_counts.values()) - direct6_count,
        "direct6_retained_fraction": round(direct6_count / sum(label_counts.values()), 6),
        "csv_fields": list(reader.fieldnames or []),
        "archive_entry_count": len(names),
        "image_file_count_in_package": len(image_entries),
        "license_file_count_in_package": len(license_entries),
        "all_image_references_are_anonymous_local_paths": all(
            row["url"].startswith("anonymous-source/") for row in rows
        ),
        "multimodal_input_reproducible_from_package": bool(image_entries),
        "license_identified": bool(license_entries),
    }


def main() -> int:
    manifests: dict[str, dict] = {}
    roots: dict[str, Path] = {}
    for name in ("csmv", "inews", "nemo"):
        manifests[name], roots[name] = verify_manifest(name)
    report = {
        "schema_version": "m1-public-audit-v1",
        "source_revisions": {
            name: manifest["upstream_revision"] for name, manifest in manifests.items()
        },
        "source_manifests_verified": True,
        "csmv": audit_csmv(roots["csmv"]),
        "inews": audit_inews(roots["inews"]),
        "nemo_plus": audit_nemo(roots["nemo"]),
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
