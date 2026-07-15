"""Validate the bounded LAI-GAI OSF public-page metadata audit."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md"
MANIFEST = ROOT / "data" / "manifests" / "lai-gai-osf-metadata-audit-v1.manifest.json"
EXPECTED_NODES = {"V8DKM", "8P572", "K8XVH"}
UNKNOWN = "UNKNOWN_NOT_VISIBLE_ON_PUBLIC_PAGE"


def validate_lai_gai_osf_metadata_audit() -> dict:
    missing = [str(path.relative_to(ROOT)) for path in (REPORT, MANIFEST) if not path.is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"schema": "lai-gai-osf-metadata-audit-check-v1", "passed": False, "checks": checks}

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    components = data.get("components", [])
    checks["authorization_scope"] = {
        "passed": (
            data.get("scope_decision") == "SC-20260714-01"
            and data.get("authorization") == "AUTH-00-LAI-GAI-OSF-META-RO-20260714"
            and data.get("audit_mode") == "PUBLIC_WEB_METADATA_ONLY_NO_DOWNLOAD_NO_API"
            and {item.get("node_id") for item in components} == EXPECTED_NODES
        ),
        "node_ids": sorted(item.get("node_id", "") for item in components),
    }
    checks["no_expanded_access"] = {
        "passed": (
            data.get("downloaded_assets") == []
            and data.get("previewed_or_streamed_assets") is False
            and data.get("used_login_cookie_or_gating_bypass") is False
            and data.get("used_api_or_automated_scraping") is False
            and data.get("contacted_authors") is False
            and data.get("built_label_mapping_or_split") is False
        )
    }
    unknown_fields = (
        "asset_license", "revision_or_update", "file_tree_count_size", "checksum",
        "gating", "public_data_dictionary",
    )
    checks["unknowns_preserved"] = {
        "passed": len(components) == 3 and all(
            all(item.get(field) == UNKNOWN for field in unknown_fields) for item in components
        ),
        "fields": list(unknown_fields),
    }
    checks["honest_gate_state"] = {
        "passed": (
            data.get("candidate_status") == "NO_GO_PENDING_ASSET_METADATA"
            and data.get("second_primary_frozen") is False
            and data.get("download_authorized") is False
            and data.get("g1_status") == "BLOCKED_SECOND_PRIMARY_NOT_FROZEN"
            and data.get("g2_status") == "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN"
            and data.get("formal_split") is False
            and data.get("task20_or_m3_allowed") is False
        ),
        "candidate_status": data.get("candidate_status"),
        "g1_status": data.get("g1_status"),
        "g2_status": data.get("g2_status"),
    }
    passed = all(check["passed"] for check in checks.values())
    return {
        "schema": "lai-gai-osf-metadata-audit-check-v1",
        "passed": passed,
        "checks": checks,
    }


def main() -> int:
    result = validate_lai_gai_osf_metadata_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
