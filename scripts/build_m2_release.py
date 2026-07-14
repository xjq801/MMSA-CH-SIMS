"""Build the step-36 M2 release candidate only after the leakage gate passes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# Python isolated mode intentionally removes the script directory from sys.path.
# Re-add only this reviewed local directory so the adjacent leakage gate can be
# imported without enabling site-packages or user-site code.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_m2_leakage_tests import ROOT, MANIFEST_ROOT, run_live


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_data_audit(leakage: dict, human: dict, silver: dict, split: dict, cuc: dict) -> str:
    return """# 数据审计报告 v1

## 结论

- 发布级别：`LOCAL_CANDIDATE_G1_BLOCKED`，不是正式benchmark发布。
- 泄漏自动门：`{leakage_gate}`，Critical失败数 `{failures}`。
- G1：`BLOCKED_SECOND_PRIMARY_NOT_FROZEN`。
- G2：`NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN`。

## 数据闭环

| 层级 | 数据 | 记录数 | 定位 |
|---|---|---:|---|
| HUMAN_GOLD | CSMV视频级人工评论经验分布 | {human_records} | 唯一当前公开人工主集 |
| SILVER | CUC-IGPE-v2遗留银标canonical | {silver_records} | 辅助、本地、不得并入人工test |
| UNLABELED | 预留入口 | 0 | 当前为空 |

CSMV的`group_by_video_v1`为train/dev/test `{group_counts}`；`hashtag_heldout_v1`为 `{hashtag_counts}`。原生topic和发布时间缺失，因此topic/time协议未发布。

## 已证实问题

- CUC历史2815与当前2787相差 `{drift}` 条，缺少2815原始manifest，去向未解释。
- CUC有 `{conflicts}` 条标签冲突、`{missing_time}` 条缺发布时间；许可仍为`UNKNOWN_LOCAL_ONLY`。
- CSMV媒体、发布者和媒体指纹未纳入本地包，语义近重复、同源事件和发布者捷径不能声明已查全。
- 第二人工多模态主集未冻结，故dataset-v1/split-v1只能是本地候选。

## 泄漏边界

已自动检查ID交集、source group、评论—视频归属、目标评论字段、未来候选字段、train-only索引合同、时间split合同和fit范围。检查是确定性的启发式门，不替代媒体/语义人工审计。任一Critical失败时构建器先退出并输出`LEAKAGE_BLOCKED`，不会写出新的release manifest。
""".format(
        leakage_gate=leakage["gate"],
        failures=leakage["critical_failure_count"],
        human_records=human["records"],
        silver_records=silver["records"],
        group_counts=json.dumps(split["counts"]["group_by_video_v1"], ensure_ascii=False, sort_keys=True),
        hashtag_counts=json.dumps(split["counts"]["hashtag_heldout_v1"], ensure_ascii=False, sort_keys=True),
        drift=cuc["unresolved_drift"],
        conflicts=cuc["stats"]["label_conflicts"],
        missing_time=cuc["stats"]["publish_time_missing"],
    )


def build_release() -> dict:
    leakage = run_live(write_outputs=True)
    if not leakage["passed"]:
        return {"passed": False, "gate": "LEAKAGE_BLOCKED", "written": []}

    human = read_json(MANIFEST_ROOT / "human-gold-v1.manifest.json")
    silver = read_json(MANIFEST_ROOT / "silver-v1.manifest.json")
    unlabeled = read_json(MANIFEST_ROOT / "unlabeled-v1.manifest.json")
    csmv_split = read_json(MANIFEST_ROOT / "csmv-split-v1.manifest.json")
    cuc = read_json(MANIFEST_ROOT / "cuc-canonical-v1.manifest.json")
    second = read_json(MANIFEST_ROOT / "second-primary-label-map-v1.manifest.json")

    provenance_path = MANIFEST_ROOT / "label-provenance-v1.manifest.json"
    provenance = {
        "schema_version": "label-provenance-v1",
        "release_version": "dataset-v1",
        "release_status": "LOCAL_CANDIDATE_G1_BLOCKED",
        "tiers": [
            {"manifest": name, "sha256": sha256_file(MANIFEST_ROOT / name)}
            for name in ("human-gold-v1.manifest.json", "silver-v1.manifest.json", "unlabeled-v1.manifest.json")
        ],
        "physical_roots": {
            "HUMAN_GOLD": "data/processed/HUMAN_GOLD",
            "SILVER": "data/processed/SILVER",
            "UNLABELED": "data/processed/UNLABELED",
        },
        "mixed_tier_loading": "PROHIBITED",
        "public_human_test_with_silver": "PROHIBITED",
        "second_primary_status": second["status"],
        "formal_evaluation_eligible": False,
    }
    write_json(provenance_path, provenance)

    split_path = MANIFEST_ROOT / "split-v1.manifest.json"
    split_release = {
        "schema_version": "split-v1-release",
        "release_version": "split-v1",
        "status": "LOCAL_CANDIDATE_G1_BLOCKED",
        "formal_split": False,
        "primary_dataset": human["dataset_id"],
        "second_primary_status": second["status"],
        "schemes": csmv_split["counts"],
        "source_manifest": "csmv-split-v1.manifest.json",
        "source_manifest_sha256": sha256_file(MANIFEST_ROOT / "csmv-split-v1.manifest.json"),
        "leakage_manifest": "leakage-audit-v1.manifest.json",
        "leakage_manifest_sha256": sha256_file(MANIFEST_ROOT / "leakage-audit-v1.manifest.json"),
        "leakage_gate": leakage["gate"],
        "index_status": "NOT_BUILT",
        "fit_scope": "train_only",
        "topic_protocol": "BLOCKED_NATIVE_TOPIC_ABSENT",
        "time_protocol": "NOT_RELEASED_TIMESTAMPS_ABSENT",
    }
    write_json(split_path, split_release)

    audit_path = ROOT / "DATA_AUDIT_REPORT_V1.md"
    audit_path.write_text(render_data_audit(leakage, human, silver, csmv_split, cuc), encoding="utf-8")

    documentation = [
        "DATA_CARD_DATASET_V1.md",
        "DATASHEET_DATASET_V1.md",
        "PRIVACY_STATEMENT.md",
        "PLATFORM_TERMS_STATEMENT.md",
        "DATA_RELEASE_BOUNDARY.md",
    ]
    missing_documents = [path for path in documentation if not (ROOT / path).is_file()]
    if missing_documents:
        raise FileNotFoundError("missing release documentation: " + ", ".join(missing_documents))

    dataset_path = MANIFEST_ROOT / "dataset-v1.manifest.json"
    dataset = {
        "schema_version": "dataset-release-manifest-v1",
        "release_version": "dataset-v1",
        "status": "LOCAL_CANDIDATE_G1_BLOCKED",
        "formal_model_use_allowed": False,
        "g1_passed": False,
        "g1_status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
        "g2_passed": False,
        "g2_status": "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN",
        "primary_human_gold": {"manifest": "human-gold-v1.manifest.json", "sha256": sha256_file(MANIFEST_ROOT / "human-gold-v1.manifest.json"), "records": human["records"]},
        "second_primary": {"manifest": "second-primary-label-map-v1.manifest.json", "status": second["status"]},
        "auxiliary_silver": {"manifest": "silver-v1.manifest.json", "sha256": sha256_file(MANIFEST_ROOT / "silver-v1.manifest.json"), "records": silver["records"], "formal_test_use": "PROHIBITED"},
        "unlabeled": {"manifest": "unlabeled-v1.manifest.json", "records": unlabeled["records"]},
        "split_manifest": {"manifest": "split-v1.manifest.json", "sha256": sha256_file(split_path)},
        "label_provenance_manifest": {"manifest": "label-provenance-v1.manifest.json", "sha256": sha256_file(provenance_path)},
        "leakage_manifest": {"manifest": "leakage-audit-v1.manifest.json", "sha256": sha256_file(MANIFEST_ROOT / "leakage-audit-v1.manifest.json")},
        "data_audit_report": {"path": "DATA_AUDIT_REPORT_V1.md", "sha256": sha256_file(audit_path)},
        "documentation": [
            {"path": path, "sha256": sha256_file(ROOT / path)}
            for path in documentation
        ],
        "raw_media_in_release": False,
        "comment_text_in_release": False,
        "sensitive_user_identifiers_in_release": False,
    }
    write_json(dataset_path, dataset)
    return {
        "schema": "m2-release-build-v1",
        "passed": True,
        "gate": leakage["gate"],
        "status": dataset["status"],
        "written": [
            "data/manifests/leakage-audit-v1.manifest.json",
            "M2_LEAKAGE_AUDIT.md",
            "data/manifests/label-provenance-v1.manifest.json",
            "data/manifests/split-v1.manifest.json",
            "DATA_AUDIT_REPORT_V1.md",
            "data/manifests/dataset-v1.manifest.json",
        ],
    }


def main() -> int:
    report = build_release()
    if not report["passed"]:
        print("LEAKAGE_BLOCKED")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
