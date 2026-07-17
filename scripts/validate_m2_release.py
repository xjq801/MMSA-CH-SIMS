"""Acceptance checks for M2 steps 34--39 and the written G1/G2 gate state."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "data" / "manifests"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_m2_leakage_tests import run_live  # noqa: E402
from validate_csmv_feature_preflight import validate_csmv_feature_preflight  # noqa: E402
from validate_csmv_i3d_sequence_protocol import validate as validate_i3d_sequence_protocol  # noqa: E402


REQUIRED = [
    "scripts/run_m2_leakage_tests.py",
    "scripts/build_m2_release.py",
    "scripts/reproduce_m2_minimal.py",
    "M2_LEAKAGE_AUDIT.md",
    "DATA_AUDIT_REPORT_V1.md",
    "DATA_CARD_DATASET_V1.md",
    "DATASHEET_DATASET_V1.md",
    "PRIVACY_STATEMENT.md",
    "PLATFORM_TERMS_STATEMENT.md",
    "DATA_RELEASE_BOUNDARY.md",
    "G1_G2_EVIDENCE_MATRIX.md",
    "HANDOFF_10.md",
    "TASK00_CSMV_LINEAGE_G2_REVIEW_20260715.md",
    "TASK00_CSMV_FEATURE_PREFLIGHT_G2_REVIEW_20260715.md",
    "TASK00_G2_RISK_ACCEPTANCE_AND_TASK20_AUTHORIZATION_20260717.md",
    "TASK00_CSMV_ONE_FEATURE_FAMILY_METADATA_COORDINATION_AUTHORIZATION_20260715.md",
    "CSMV_FEATURE_ASSET_PREFLIGHT_20260715.md",
    "scripts/validate_csmv_feature_preflight.py",
    "data/manifests/csmv-feature-preflight-v1.manifest.json",
    "CSMV_I3D_SEQUENCE_PROTOCOL_V1.md",
    "configs/csmv-i3d-sequence-protocol-v1.json",
    "scripts/csmv_i3d_sequence_protocol.py",
    "scripts/validate_csmv_i3d_sequence_protocol.py",
    "data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json",
    "data/manifests/leakage-audit-v1.manifest.json",
    "data/manifests/dataset-v1.manifest.json",
    "data/manifests/split-v1.manifest.json",
    "data/manifests/label-provenance-v1.manifest.json",
    "data/manifests/reproducibility-v1.manifest.json",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_m2_release() -> dict:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {
            "schema": "m2-release-check-v1",
            "passed": False,
            "g1_passed": False,
            "g2_passed": False,
            "checks": checks,
        }

    live = run_live(write_outputs=False)
    stored = read_json(MANIFEST_ROOT / "leakage-audit-v1.manifest.json")
    checks["leakage_gate"] = {
        "passed": (
            live == stored
            and live["passed"] is True
            and live["critical_failure_count"] == 0
            and live["gate"] == "PASS_WITH_LIMITATIONS"
            and live["checks"]["time_order"]["status"] == "NOT_APPLICABLE_NO_TIME_SPLIT"
        ),
        "gate": live["gate"],
        "critical_failure_count": live["critical_failure_count"],
        "time_status": live["checks"]["time_order"]["status"],
    }

    dataset = read_json(MANIFEST_ROOT / "dataset-v1.manifest.json")
    split = read_json(MANIFEST_ROOT / "split-v1.manifest.json")
    provenance = read_json(MANIFEST_ROOT / "label-provenance-v1.manifest.json")
    checks["honest_release_state"] = {
        "passed": (
            dataset.get("status") == "PROTOCOL_DATA_G2_PASS_ASSET_RISK_ACCEPTED"
            and dataset.get("formal_model_use_allowed") is True
            and dataset.get("model_use_scope") == "INTERNAL_RESEARCH_ONLY_NO_ASSET_REDISTRIBUTION"
            and dataset.get("g1_passed") is True
            and dataset.get("g1_status") == "PASS"
            and dataset.get("g2_passed") is True
            and dataset.get("g2_status") == "PASS_WITH_ACCEPTED_ASSET_RISK"
            and dataset.get("g2_protocol_data") == "PASS_WITH_LIMITATIONS"
            and dataset.get("asset_admissibility") == "DEFERRED_ACCEPTED_RISK"
            and split.get("formal_split") is True
            and split.get("status") == "FORMAL_PROTOCOL_SPLIT_ASSET_RISK_ACCEPTED"
            and provenance.get("formal_evaluation_eligible") is True
            and provenance.get("asset_admissibility") == "DEFERRED_ACCEPTED_RISK"
            and provenance.get("mixed_tier_loading") == "PROHIBITED"
        ),
        "dataset_status": dataset.get("status"),
        "split_formal": split.get("formal_split"),
        "g1_status": dataset.get("g1_status"),
        "g2_status": dataset.get("g2_status"),
    }

    references = [
        dataset["primary_human_gold"],
        dataset["csmv_media_lineage"],
        dataset["csmv_input_asset_preflight"],
        dataset["csmv_i3d_sequence_protocol"],
        dataset["auxiliary_silver"],
        dataset["split_manifest"],
        dataset["label_provenance_manifest"],
        dataset["leakage_manifest"],
    ]
    manifest_hashes = []
    for reference in references:
        path = MANIFEST_ROOT / reference["manifest"]
        manifest_hashes.append(path.is_file() and sha256_file(path) == reference["sha256"])
    checks["manifest_lineage"] = {
        "passed": all(manifest_hashes),
        "references_checked": len(manifest_hashes),
    }

    checks["csmv_feature_preflight"] = validate_csmv_feature_preflight()
    checks["csmv_i3d_sequence_protocol"] = validate_i3d_sequence_protocol()

    document_hashes = []
    for reference in dataset.get("documentation", []):
        path = ROOT / reference["path"]
        document_hashes.append(path.is_file() and sha256_file(path) == reference["sha256"])
    checks["documentation"] = {
        "passed": len(document_hashes) == 5 and all(document_hashes),
        "documents_checked": len(document_hashes),
    }

    reproducibility = read_json(MANIFEST_ROOT / "reproducibility-v1.manifest.json")
    current_mismatches = []
    for relative, expected in reproducibility.get("after_sha256", {}).items():
        path = ROOT / relative
        actual = sha256_file(path) if path.is_file() else "MISSING"
        if actual != expected:
            current_mismatches.append(relative)
    checks["reproducibility"] = {
        "passed": (
            reproducibility.get("passed") is True
            and reproducibility.get("status") == "PASS_CURRENT_CSMV_SOURCE_GROUP_SPLIT"
            and reproducibility.get("replay_scope") == "PUBLIC_BENCHMARK_CORE"
            and reproducibility.get("frozen_auxiliary_inputs_verified") is True
            and reproducibility.get("mismatches", []) == []
            and current_mismatches == []
            and reproducibility.get("credential_environment_forwarded") is False
        ),
        "status": reproducibility.get("status"),
        "outputs_checked": reproducibility.get("outputs_checked"),
        "mismatches": current_mismatches,
        "current_replay_passed": reproducibility.get("passed") is True and not current_mismatches,
    }

    matrix = (ROOT / "G1_G2_EVIDENCE_MATRIX.md").read_text(encoding="utf-8")
    handoff = (ROOT / "HANDOFF_10.md").read_text(encoding="utf-8")
    checks["gate_evidence_and_handoff"] = {
        "passed": (
            "G1=`PASS`" in matrix
            and "G2=`PASS_WITH_ACCEPTED_ASSET_RISK`" in matrix
            and "ASSET_ADMISSIBILITY=`DEFERRED_ACCEPTED_RISK`" in matrix
            and "REVIEW-00-CSMV-FEATURE-PREFLIGHT-G2-20260715" in matrix
            and "00已确认" in handoff
            and "任务20已获创建授权" in handoff
        ),
        "g1_claimed_pass": True,
        "g2_claimed_pass": True,
    }

    passed = all(result["passed"] for result in checks.values())
    return {
        "schema": "m2-release-check-v1",
        "passed": passed,
        "steps_34_39_local_package_ready": passed,
        "g1_passed": passed,
        "g1_status": "PASS" if passed else "VALIDATION_FAILED",
        "g2_passed": passed,
        "g2_status": "PASS_WITH_ACCEPTED_ASSET_RISK" if passed else "VALIDATION_FAILED",
        "g2_protocol_data": "PASS_WITH_LIMITATIONS" if passed else "VALIDATION_FAILED",
        "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
        "checks": checks,
    }


def main() -> int:
    report = validate_m2_release()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
