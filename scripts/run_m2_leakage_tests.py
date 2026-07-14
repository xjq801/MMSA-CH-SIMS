"""Critical leakage gate for M2 steps 34--35.

The gate is intentionally independent from model code.  A critical failure prints
``LEAKAGE_BLOCKED`` and returns a non-zero exit status.  A pass only certifies the
implemented checks; it does not imply that G1 or G2 has passed.
"""

from __future__ import annotations

import argparse
import copy
import json
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "data" / "manifests"
CSMV_REVISION = "99d14240254b1381dde0b9c56add140381f65117"
CSMV_ANNOTATIONS = ROOT / "data" / "raw" / "csmv" / CSMV_REVISION / "CSMV" / "Comments_Anno"
REPORT_JSON = MANIFEST_ROOT / "leakage-audit-v1.manifest.json"
REPORT_MD = ROOT / "M2_LEAKAGE_AUDIT.md"
ASSIGNED = ("train", "dev", "test")
TARGET_COMMENT_FIELDS = {
    "comment",
    "comments",
    "comment_text",
    "comment_body",
    "target_comment",
    "target_comments",
    "test_comment",
    "test_comments",
}
FUTURE_FIELDS = {
    "candidate_ids",
    "retrieved_ids",
    "recommended_ids",
    "recommendation_result",
    "future_interaction_count",
    "future_like_count",
    "future_share_count",
    "future_view_count",
    "final_like_count",
    "final_share_count",
    "final_view_count",
    "comment_popularity",
}
REQUIRED_INDEX_ORDER = [
    "freeze_raw_manifest",
    "aggregate_by_item",
    "assign_split",
    "select_train_only",
    "build_index",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[dict]:
    records = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                records.append(json.loads(line))
    return records


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def nested_keys(value: object) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key).lower()
            for nested in nested_keys(child):
                yield nested
    elif isinstance(value, list):
        for child in value:
            for nested in nested_keys(child):
                yield nested


def check(name: str, passed: bool, status: str, **details: object) -> dict:
    return {"name": name, "passed": bool(passed), "status": status, "severity": "CRITICAL", **details}


def split_sets(records: Sequence[dict], scheme: str, key: str) -> Dict[str, Set[str]]:
    values = {split: set() for split in ASSIGNED}
    for record in records:
        split = record.get("split", {}).get(scheme)
        value = record.get(key)
        if split in values and value:
            values[split].add(str(value))
    return values


def intersections(values: Dict[str, Set[str]]) -> Dict[str, int]:
    return {
        "train_dev": len(values["train"] & values["dev"]),
        "train_test": len(values["train"] & values["test"]),
        "dev_test": len(values["dev"] & values["test"]),
    }


def audit_raw_comment_grouping() -> dict:
    official_by_split = {}
    official_ids = []
    for split in ASSIGNED:
        values = [str(value) for value in read_json(CSMV_ANNOTATIONS / (split + "_set.json"))]
        official_by_split[split] = set(values)
        official_ids.extend(values)

    split_overlap = intersections(official_by_split)
    video_to_comment = read_json(CSMV_ANNOTATIONS / "video_to_comment.json")
    comment_to_video = {}
    duplicate_comment_memberships = 0
    for video_id, comment_ids in video_to_comment.items():
        for comment_id in comment_ids:
            comment_id = str(comment_id)
            if comment_id in comment_to_video and comment_to_video[comment_id] != str(video_id):
                duplicate_comment_memberships += 1
            comment_to_video[comment_id] = str(video_id)

    with zipfile.ZipFile(CSMV_ANNOTATIONS / "lable_data_dict.json.zip") as archive:
        labels = json.loads(archive.read("lable_data_dict.json").decode("utf-8"))
    missing_label = 0
    missing_video_map = 0
    mismatched_video = 0
    for comment_id in official_ids:
        record = labels.get(comment_id)
        if record is None:
            missing_label += 1
            continue
        mapped_video = comment_to_video.get(comment_id)
        if mapped_video is None:
            missing_video_map += 1
        elif mapped_video != str(record.get("video_file_id")):
            mismatched_video += 1
    passed = (
        len(official_ids) == len(set(official_ids)) == 107267
        and not any(split_overlap.values())
        and duplicate_comment_memberships == 0
        and missing_label == 0
        and missing_video_map == 0
        and mismatched_video == 0
    )
    return check(
        "same_video_comment_grouping",
        passed,
        "PASS" if passed else "FAIL_COMMENT_GROUPING",
        official_comment_count=len(official_ids),
        official_comment_split_intersections=split_overlap,
        video_groups=len(video_to_comment),
        duplicate_comment_memberships=duplicate_comment_memberships,
        missing_label_records=missing_label,
        missing_video_memberships=missing_video_map,
        video_id_mismatches=mismatched_video,
        sensitive_values_emitted=False,
    )


def parse_time(value: object) -> Optional[datetime]:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def audit_time_order(records: Sequence[dict]) -> dict:
    time_schemes = sorted(
        {
            scheme
            for record in records
            for scheme in record.get("split", {})
            if "time" in scheme.lower() and record.get("split", {}).get(scheme) in ASSIGNED
        }
    )
    if not time_schemes:
        return check(
            "time_order",
            True,
            "NOT_APPLICABLE_NO_TIME_SPLIT",
            evaluated_schemes=[],
            limitation="CSMV publish_time is absent; no chronological split is released or claimed safe.",
        )
    failures = []
    summaries = {}
    for scheme in time_schemes:
        by_split = defaultdict(list)
        missing = 0
        for record in records:
            split = record.get("split", {}).get(scheme)
            if split not in ASSIGNED:
                continue
            value = parse_time(record.get("publish_time"))
            if value is None:
                missing += 1
            else:
                by_split[split].append(value)
        boundaries = {}
        for split in ASSIGNED:
            if by_split[split]:
                boundaries[split] = {"min": min(by_split[split]).isoformat(), "max": max(by_split[split]).isoformat()}
        if missing:
            failures.append(scheme + ":missing_or_invalid_time")
        if by_split["train"] and by_split["dev"] and max(by_split["train"]) > min(by_split["dev"]):
            failures.append(scheme + ":train_after_dev")
        if by_split["train"] and by_split["test"] and max(by_split["train"]) > min(by_split["test"]):
            failures.append(scheme + ":train_after_test")
        if by_split["dev"] and by_split["test"] and max(by_split["dev"]) > min(by_split["test"]):
            failures.append(scheme + ":dev_after_test")
        summaries[scheme] = {"missing_or_invalid": missing, "boundaries": boundaries}
    return check(
        "time_order",
        not failures,
        "PASS" if not failures else "FAIL_TIME_ORDER",
        evaluated_schemes=time_schemes,
        failures=failures,
        summaries=summaries,
    )


def audit_records(records: Sequence[dict], index_manifest: dict, raw_grouping: Optional[dict] = None) -> dict:
    checks = []
    schemes = sorted({scheme for record in records for scheme in record.get("split", {})})
    id_details = {}
    group_details = {}
    id_passed = True
    group_passed = True
    for scheme in schemes:
        ids = split_sets(records, scheme, "item_id")
        groups = split_sets(records, scheme, "source_group_id")
        id_overlap = intersections(ids)
        group_overlap = intersections(groups)
        id_details[scheme] = id_overlap
        group_details[scheme] = group_overlap
        id_passed = id_passed and not any(id_overlap.values())
        group_passed = group_passed and not any(group_overlap.values())
    duplicate_ids = len(records) - len({record.get("item_id") for record in records})
    checks.append(
        check(
            "id_intersection",
            id_passed and duplicate_ids == 0,
            "PASS" if id_passed and duplicate_ids == 0 else "FAIL_ID_INTERSECTION",
            duplicate_item_rows=duplicate_ids,
            cross_split_intersections=id_details,
        )
    )
    checks.append(
        check(
            "source_group_intersection",
            group_passed,
            "PASS" if group_passed else "FAIL_SOURCE_GROUP_INTERSECTION",
            cross_split_intersections=group_details,
        )
    )
    checks.append(raw_grouping or audit_raw_comment_grouping())

    target_hits = []
    future_hits = []
    unsafe_legacy = 0
    for index, record in enumerate(records):
        keys = set(nested_keys(record))
        target = sorted(keys & TARGET_COMMENT_FIELDS)
        future = sorted(keys & FUTURE_FIELDS)
        if target:
            target_hits.append({"row": index, "fields": target})
        if future:
            future_hits.append({"row": index, "fields": future})
        if record.get("legacy_features") is not None and record.get("legacy_features_available_at_t0") is not False:
            unsafe_legacy += 1
    checks.append(
        check(
            "target_comment_fields",
            not target_hits,
            "PASS" if not target_hits else "FAIL_TARGET_COMMENT_FIELD",
            hit_count=len(target_hits),
            hits=target_hits[:20],
        )
    )
    checks.append(
        check(
            "future_candidate_fields",
            not future_hits and unsafe_legacy == 0,
            "PASS" if not future_hits and unsafe_legacy == 0 else "FAIL_FUTURE_FIELD",
            forbidden_field_hit_count=len(future_hits),
            unsafe_legacy_feature_rows=unsafe_legacy,
            hits=future_hits[:20],
        )
    )

    index_passed = (
        index_manifest.get("allowed_fit_split") == "train"
        and index_manifest.get("dev_test_candidates_in_index") == "PROHIBITED"
        and index_manifest.get("required_build_order") == REQUIRED_INDEX_ORDER
        and index_manifest.get("status") in {"NOT_BUILT", "TRAIN_ONLY_BUILT"}
    )
    checks.append(
        check(
            "index_train_only",
            index_passed,
            "PASS_NOT_BUILT" if index_passed and index_manifest.get("status") == "NOT_BUILT" else "PASS" if index_passed else "FAIL_INDEX_SCOPE",
            index_status=index_manifest.get("status"),
            allowed_fit_split=index_manifest.get("allowed_fit_split"),
            dev_test_candidates_in_index=index_manifest.get("dev_test_candidates_in_index"),
            required_build_order=index_manifest.get("required_build_order"),
        )
    )
    checks.append(audit_time_order(records))

    fit_passed = (
        index_manifest.get("allowed_fit_split") == "train"
        and index_manifest.get("required_build_order", []).index("assign_split")
        < index_manifest.get("required_build_order", []).index("build_index")
        if all(value in index_manifest.get("required_build_order", []) for value in ("assign_split", "build_index"))
        else False
    )
    checks.append(
        check(
            "fit_scope",
            fit_passed,
            "PASS_NO_FIT_ARTIFACTS" if fit_passed and index_manifest.get("status") == "NOT_BUILT" else "PASS" if fit_passed else "FAIL_FIT_SCOPE",
            allowed_fit_split=index_manifest.get("allowed_fit_split"),
            fit_artifacts_present=index_manifest.get("status") != "NOT_BUILT",
        )
    )

    failures = [value for value in checks if not value["passed"]]
    return {
        "schema_version": "m2-leakage-audit-v1",
        "gate": "PASS_WITH_LIMITATIONS" if not failures else "LEAKAGE_BLOCKED",
        "passed": not failures,
        "critical_failure_count": len(failures),
        "checks": {value["name"]: {key: item for key, item in value.items() if key != "name"} for value in checks},
        "scope_limitations": [
            "Checks are deterministic but not proof that every semantic near-duplicate or same-event leak has been found.",
            "No CSMV chronological split is evaluated because publish timestamps are unavailable.",
            "Publisher and media-fingerprint leakage remain unresolved where source metadata/media are unavailable.",
        ],
        "g1_passed": False,
        "g1_status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
        "g2_passed": False,
        "g2_status": "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN",
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# M2泄漏测试报告 v1",
        "",
        "> 本报告是步骤34—35的自动化证据，不等同于G1/G2通过。",
        "",
        "## 门状态",
        "",
        "- 泄漏门：`{}`".format(report["gate"]),
        "- Critical失败数：{}".format(report["critical_failure_count"]),
        "- G1：`{}`".format(report["g1_status"]),
        "- G2：`{}`".format(report["g2_status"]),
        "",
        "## 检查结果",
        "",
        "| 检查 | 结果 | 状态 |",
        "|---|---:|---|",
    ]
    for name, result in report["checks"].items():
        lines.append("| `{}` | {} | `{}` |".format(name, "PASS" if result["passed"] else "FAIL", result["status"]))
    lines.extend(["", "## 边界", ""])
    lines.extend("- " + value for value in report["scope_limitations"])
    lines.extend(
        [
            "",
            "时间顺序检查当前为`NOT_APPLICABLE_NO_TIME_SPLIT`：这表示未发布时间split，不表示时间安全已被证明。",
            "任何后续新增time split、索引、拟合状态或候选字段都必须重新运行本门。",
            "",
        ]
    )
    return "\n".join(lines)


def run_live(write_outputs: bool = True) -> dict:
    human_manifest = read_json(MANIFEST_ROOT / "human-gold-v1.manifest.json")
    records = read_jsonl(ROOT / human_manifest["path"])
    index_manifest = read_json(MANIFEST_ROOT / "index-boundary-v1.manifest.json")
    report = audit_records(records, index_manifest)
    report["dataset_id"] = human_manifest["dataset_id"]
    report["record_count"] = len(records)
    if write_outputs:
        write_json(REPORT_JSON, report)
        REPORT_MD.write_text(render_markdown(report), encoding="utf-8")
    return report


def selftest() -> int:
    human_manifest = read_json(MANIFEST_ROOT / "human-gold-v1.manifest.json")
    records = read_jsonl(ROOT / human_manifest["path"])
    first = copy.deepcopy(records[0])
    duplicate = copy.deepcopy(first)
    current = first["split"]["group_by_video_v1"]
    duplicate["split"]["group_by_video_v1"] = "test" if current != "test" else "train"
    duplicate["target_comment"] = "fixture-only"
    duplicate["future_interaction_count"] = 999
    first["split"]["time_order_fixture_v1"] = "train"
    first["publish_time"] = "2026-01-02T00:00:00+00:00"
    duplicate["split"]["time_order_fixture_v1"] = "test"
    duplicate["publish_time"] = "2026-01-01T00:00:00+00:00"
    index_manifest = read_json(MANIFEST_ROOT / "index-boundary-v1.manifest.json")
    index_manifest["allowed_fit_split"] = "all"
    raw_grouping = check("same_video_comment_grouping", True, "PASS_SELFTEST_REUSED_LIVE_CONTRACT")
    report = audit_records([first, duplicate], index_manifest, raw_grouping=raw_grouping)
    expected = {
        "id_intersection",
        "source_group_intersection",
        "target_comment_fields",
        "future_candidate_fields",
        "index_train_only",
        "time_order",
        "fit_scope",
    }
    failed = {name for name, result in report["checks"].items() if not result["passed"]}
    ok = report["gate"] == "LEAKAGE_BLOCKED" and expected <= failed
    print("LEAKAGE_BLOCKED (expected negative fixture)")
    print(json.dumps({"schema": "m2-leakage-selftest-v1", "passed": ok, "failed_checks": sorted(failed)}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    report = run_live(write_outputs=not args.no_write)
    if not report["passed"]:
        print("LEAKAGE_BLOCKED")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
