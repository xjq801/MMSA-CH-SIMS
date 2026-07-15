"""Validate the honest metadata-only CSMV feature-asset preflight."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/manifests/csmv-feature-preflight-v1.manifest.json"
SOURCE_MANIFEST = ROOT / "data/manifests/csmv-source-v1.manifest.json"
REPORT = ROOT / "CSMV_FEATURE_ASSET_PREFLIGHT_20260715.md"
QUARANTINE_MANIFEST = ROOT / "data/manifests/csmv-i3d-quarantine-v1.manifest.json"
LOCAL_FEATURE_ROOT = ROOT / "data/raw/csmv/features/visual_feature/I3D"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_csmv_feature_preflight() -> dict:
    missing = [
        str(path.relative_to(ROOT))
        for path in (MANIFEST, SOURCE_MANIFEST, REPORT, QUARANTINE_MANIFEST)
        if not path.is_file()
    ]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"schema": "csmv-feature-preflight-check-v1", "passed": False, "checks": checks}

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    quarantine = json.loads(QUARANTINE_MANIFEST.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    snapshot = manifest["official_snapshot"]
    raw_root = ROOT / source["raw_root"]
    readme = raw_root / snapshot["readme_relative_path"]
    families = manifest.get("feature_families", [])
    local_features = list(LOCAL_FEATURE_ROOT.glob("*.npy")) if LOCAL_FEATURE_ROOT.is_dir() else []
    i3d = next((item for item in families if item.get("family") == "I3D"), {})
    unresolved_families = [item for item in families if item.get("family") != "I3D"]

    checks["official_snapshot"] = {
        "passed": (
            source.get("upstream_revision") == snapshot.get("commit")
            and readme.is_file()
            and sha256_file(readme) == snapshot.get("readme_sha256")
        ),
        "commit": snapshot.get("commit"),
    }
    observation = manifest["anonymous_public_page_observation"]
    checks["public_page_observation"] = {
        "passed": (
            observation.get("method") == "ANONYMOUS_HTTPS_GET_PUBLIC_FOLDER_PAGE"
            and observation.get("final_host") == "drive.google.com"
            and observation.get("http_status") == 200
            and observation.get("revision_stability") == "UNKNOWN_DYNAMIC_PAGE_RESPONSE"
        ),
        "status": observation.get("http_status"),
        "host": observation.get("final_host"),
    }
    checks["unknowns_fail_closed"] = {
        "passed": (
            len(families) == 3
            and all(item.get("asset_license") == "UNKNOWN" for item in families)
            and all(item.get("asset_revision") == "UNKNOWN" for item in families)
            and i3d.get("file_count") == quarantine["package"].get("npy_files") == 9942
            and i3d.get("total_bytes") == quarantine["package"].get("total_bytes")
            and i3d.get("local_required_checksum_count") == 8210
            and all(item.get("file_count") is None for item in unresolved_families)
            and all(item.get("total_bytes") is None for item in unresolved_families)
            and all(item.get("public_checksum_count") == 0 for item in families)
            and manifest["coverage"].get("verified_coverage_count") == 8210
            and manifest["minimal_family_decision"].get("selected_family") == "I3D"
            and manifest["minimal_family_decision"].get("status") == "SELECTED_FOR_QUARANTINE_AUDIT_ONLY"
        ),
        "status": manifest.get("status"),
    }
    quarantine_ref = manifest.get("local_quarantine_manifest", {})
    checks["quarantine_manifest_fixity"] = {
        "passed": (
            quarantine_ref.get("path") == "data/manifests/csmv-i3d-quarantine-v1.manifest.json"
            and quarantine_ref.get("sha256") == sha256_file(QUARANTINE_MANIFEST)
            and quarantine.get("acquisition_status") == "QUARANTINE_ACQUIRED"
            and quarantine.get("coverage", {}).get("matched_video_file_ids") == 8210
            and quarantine.get("coverage", {}).get("missing_video_file_ids") == 0
            and quarantine.get("schema", {}).get("schema_error_count") == 0
            and quarantine.get("verdict", {}).get("quarantine_integrity_ready") is True
            and quarantine.get("verdict", {}).get("formal_use_ready") is False
        ),
        "manifest_sha256": sha256_file(QUARANTINE_MANIFEST),
        "required_file_hashes": len(quarantine.get("required_files", [])),
    }
    actions = manifest["network_or_asset_actions"]
    checks["authorization_boundary"] = {
        "passed": (
            actions.get("drive_api_used") is False
            and actions.get("login_or_cookie_used") is False
            and actions.get("feature_files_downloaded_by_codex") == 0
            and actions.get("feature_files_acquired_from_user_local_package") == 9942
            and actions.get("media_urls_visited") == 0
            and len(local_features) == 9942
        ),
        "local_npy_files": len(local_features),
    }
    checks["honest_gate_state"] = {
        "passed": (
            manifest.get("status") == "QUARANTINE_ACQUIRED_LICENSE_REVISION_ATTESTATION_PENDING"
            and manifest.get("g2_asset_credit") is False
            and manifest.get("formal_model_input_allowed") is False
        )
    }
    passed = all(check["passed"] for check in checks.values())
    return {
        "schema": "csmv-feature-preflight-check-v1",
        "passed": passed,
        "audit_contract_valid": passed,
        "g2_asset_ready": False,
        "checks": checks,
    }


def main() -> int:
    report = validate_csmv_feature_preflight()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
