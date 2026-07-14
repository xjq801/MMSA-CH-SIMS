"""Validate the tracked M1 public-data audit contract without requiring raw data."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCUMENTS = {
    "M1_PUBLIC_DATA_AUDIT.md": [
        "NO_GO_PRIMARY_2026-07-14",
        "NO_GO_PRIMARY_PENDING_LICENSE_AND_MEDIA",
        "SILVER_ONLY_SOURCE_UNAVAILABLE",
        "G1：至少两个合法可用公开源",
        "**BLOCKED**",
    ],
    "LABEL_SPACE_MAPPING_DRAFT.md": [
        "audience_affect_direct6_v0",
        "UNMAPPABLE",
        "61,684",
        "7,024",
        "23,971",
    ],
    "DATASET_SELECTION_DECISION.md": [
        "iNews：NO-GO",
        "NEmo+：NO-GO",
        "第二人工标注主集尚未冻结",
    ],
    "DATA_SOURCE_LEDGER.md": [
        "CANONICAL_LABELS_READY_MEDIA_PENDING",
        "NO_GO_PRIMARY_MEDIA_REPRO",
        "NO_GO_PRIMARY_LICENSE_MEDIA",
        "SILVER_ONLY_SOURCE_UNAVAILABLE",
    ],
}
MANIFESTS = {
    "csmv-source-v1.manifest.json": "99d14240254b1381dde0b9c56add140381f65117",
    "inews-source-v1.manifest.json": "a7ad599a257e94f04f796a86d39635adadb5f7cb",
    "nemo-source-v1.manifest.json": "ACL-Anthology-2022-11-21",
}


def validate_m1_public_audit() -> dict:
    errors: list[str] = []
    for relative, tokens in REQUIRED_DOCUMENTS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing document: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{relative}: missing token {token}")

    for filename, revision in MANIFESTS.items():
        path = ROOT / "data" / "manifests" / filename
        if not path.is_file():
            errors.append(f"missing manifest: {filename}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema_version") != "m1-source-manifest-v1":
            errors.append(f"{filename}: wrong schema_version")
        if data.get("upstream_revision") != revision:
            errors.append(f"{filename}: revision drift")
        if data.get("retrieved_date") != "2026-07-14":
            errors.append(f"{filename}: retrieval date drift")
        if not data.get("files"):
            errors.append(f"{filename}: empty file list")
        for item in data.get("files", []):
            if not all(item.get(key) for key in ("relative_path", "source_url", "retrieved_date", "bytes", "sha256")):
                errors.append(f"{filename}: incomplete file record")
            if len(str(item.get("sha256", ""))) != 64:
                errors.append(f"{filename}: invalid sha256")

    audit_report = ROOT / "data" / "manifests" / "m1-public-audit-v1.manifest.json"
    if not audit_report.is_file():
        errors.append("missing manifest: m1-public-audit-v1.manifest.json")
    else:
        report = json.loads(audit_report.read_text(encoding="utf-8"))
        if report.get("schema_version") != "m1-public-audit-v1":
            errors.append("m1-public-audit-v1.manifest.json: wrong schema_version")
        if not report.get("source_manifests_verified"):
            errors.append("m1-public-audit-v1.manifest.json: source manifests not verified")
        if not report.get("csmv", {}).get("official_comment_split_is_video_leaky"):
            errors.append("m1-public-audit-v1.manifest.json: CSMV leakage evidence missing")
        if report.get("nemo_plus", {}).get("image_file_count_in_package") != 0:
            errors.append("m1-public-audit-v1.manifest.json: NEmo+ media finding drift")

    for script in ("scripts/fetch_m1_public_assets.py", "scripts/audit_m1_public_assets.py"):
        if not (ROOT / script).is_file():
            errors.append(f"missing script: {script}")
    return {"passed": not errors, "errors": errors}


def main() -> int:
    result = validate_m1_public_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
