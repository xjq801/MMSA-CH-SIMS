"""Validate the bounded second-primary public-metadata audit package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifests" / "second-primary-readonly-audit-v1.manifest.json"
REQUIRED = [
    "M1_SECOND_PRIMARY_SHORTLIST_20260714.md",
    "M1_LIRIS_ACCEDE_DEEP_AUDIT_20260714.md",
    "HANDOFF_10_SECOND_PRIMARY_READONLY.md",
    "data/manifests/second-primary-readonly-audit-v1.manifest.json",
]


def validate_second_primary_readonly_audit() -> dict:
    missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"schema": "second-primary-readonly-audit-check-v1", "passed": False, "checks": checks}

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])
    deep = [candidate for candidate in candidates if candidate.get("deep_audited") is True]
    checks["authorization_scope"] = {
        "passed": (
            data.get("authorization") == "AUTH-00-M1-SECOND-PRIMARY-READONLY-20260714"
            and data.get("audit_mode") == "PUBLIC_METADATA_READ_ONLY_NO_DOWNLOAD"
            and 1 <= len(candidates) <= 3
            and data.get("shortlist_count") == len(candidates)
            and len(deep) == 1
            and data.get("deep_audit_count") == 1
            and data.get("downloaded_assets") == []
            and data.get("used_login_or_gating_bypass") is False
            and data.get("used_api_or_paid_service") is False
            and data.get("contacted_authors") is False
        ),
        "shortlist_count": len(candidates),
        "deep_audit_ids": [item.get("id") for item in deep],
    }
    required_candidate_fields = {
        "id", "name", "deep_audited", "source_urls", "revision", "license",
        "package_size_bytes", "public_scale", "split", "media", "multi_annotator",
        "t0", "construct_mapping", "decision",
    }
    missing_fields = {
        candidate.get("id", "UNKNOWN"): sorted(required_candidate_fields - set(candidate))
        for candidate in candidates
        if required_candidate_fields - set(candidate)
    }
    checks["evidence_contract"] = {
        "passed": not missing_fields and all(item.get("source_urls") for item in candidates),
        "missing_fields": missing_fields,
    }
    checks["honest_gate_state"] = {
        "passed": (
            data.get("g1_status") == "BLOCKED_SECOND_PRIMARY_NOT_FROZEN"
            and data.get("g2_status") == "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN"
            and data.get("formal_split") is False
            and data.get("task20_or_m3_allowed") is False
            and all(str(item.get("decision", "")).startswith("NO_GO") for item in candidates)
        ),
        "g1_status": data.get("g1_status"),
        "g2_status": data.get("g2_status"),
        "formal_split": data.get("formal_split"),
    }
    passed = all(check["passed"] for check in checks.values())
    return {
        "schema": "second-primary-readonly-audit-check-v1",
        "passed": passed,
        "second_primary_frozen": False,
        "download_authorized": False,
        "checks": checks,
    }


def main() -> int:
    result = validate_second_primary_readonly_audit()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
