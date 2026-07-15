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
        "I3D_QUARANTINE_8210_COVERAGE_EXTERNAL_ATTESTATION_DEFERRED",
        "DEFERRED_PENDING_MAINTAINER_REPLY",
        "csmv-i3d-quarantine-v1.manifest.json",
        "csmv-i3d-sequence-protocol-v1.manifest.json",
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
        csmv = report.get("csmv", {})
        if csmv.get("raw_link_row_count") != 8210:
            errors.append("m1-public-audit-v1.manifest.json: CSMV raw-link row drift")
        if not csmv.get("raw_link_ids_cover_official_videos"):
            errors.append("m1-public-audit-v1.manifest.json: CSMV raw-link ID coverage drift")
        if csmv.get("raw_link_row_id_url_path_mismatch") != 2644:
            errors.append("m1-public-audit-v1.manifest.json: CSMV raw-link mapping drift")
        if csmv.get("raw_link_mapping_semantically_consistent") is not True:
            errors.append("m1-public-audit-v1.manifest.json: CSMV mapping validity drift")
        if csmv.get("raw_link_internal_platform_id_equality_required") is not False:
            errors.append("m1-public-audit-v1.manifest.json: CSMV ID semantics drift")
        if csmv.get("raw_link_unique_source_platform_ids") != 8008:
            errors.append("m1-public-audit-v1.manifest.json: CSMV source-family drift")
        if csmv.get("raw_link_duplicate_source_groups") != 202:
            errors.append("m1-public-audit-v1.manifest.json: CSMV duplicate-family drift")
        if report.get("nemo_plus", {}).get("image_file_count_in_package") != 0:
            errors.append("m1-public-audit-v1.manifest.json: NEmo+ media finding drift")

    i3d_manifest_path = ROOT / "data" / "manifests" / "csmv-i3d-quarantine-v1.manifest.json"
    if not i3d_manifest_path.is_file():
        errors.append("missing manifest: csmv-i3d-quarantine-v1.manifest.json")
    else:
        i3d = json.loads(i3d_manifest_path.read_text(encoding="utf-8"))
        if i3d.get("schema_version") != "csmv-i3d-quarantine-v1":
            errors.append("csmv-i3d-quarantine-v1.manifest.json: wrong schema_version")
        if i3d.get("acquisition_status") != "QUARANTINE_ACQUIRED":
            errors.append("csmv-i3d-quarantine-v1.manifest.json: acquisition status drift")
        coverage = i3d.get("coverage", {})
        if coverage.get("required_video_file_ids") != 8210:
            errors.append("csmv-i3d-quarantine-v1.manifest.json: required coverage drift")
        if coverage.get("matched_video_file_ids") != 8210 or coverage.get("missing_video_file_ids") != 0:
            errors.append("csmv-i3d-quarantine-v1.manifest.json: observed coverage drift")
        if len(i3d.get("required_files", [])) != 8210:
            errors.append("csmv-i3d-quarantine-v1.manifest.json: per-file fixity count drift")
        if i3d.get("schema", {}).get("schema_error_count") != 0:
            errors.append("csmv-i3d-quarantine-v1.manifest.json: feature schema drift")
        if i3d.get("verdict", {}).get("formal_use_ready") is not False:
            errors.append("csmv-i3d-quarantine-v1.manifest.json: formal-use boundary drift")

    for script in (
        "scripts/fetch_m1_public_assets.py",
        "scripts/audit_m1_public_assets.py",
        "scripts/csmv_media_lineage.py",
        "scripts/validate_csmv_media_lineage.py",
        "scripts/validate_csmv_feature_preflight.py",
        "scripts/audit_csmv_i3d_asset.py",
        "scripts/load_csmv_i3d.py",
    ):
        if not (ROOT / script).is_file():
            errors.append(f"missing script: {script}")
    return {"passed": not errors, "errors": errors}


def main() -> int:
    result = validate_m1_public_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
