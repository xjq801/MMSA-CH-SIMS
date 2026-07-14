"""Acceptance checks for M2 steps 34--39 without claiming G1/G2 pass."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "data" / "manifests"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_m2_leakage_tests import run_live  # noqa: E402


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
            dataset.get("status") == "LOCAL_CANDIDATE_G1_BLOCKED"
            and dataset.get("formal_model_use_allowed") is False
            and dataset.get("g1_passed") is False
            and dataset.get("g2_passed") is False
            and split.get("formal_split") is False
            and split.get("status") == "LOCAL_CANDIDATE_G1_BLOCKED"
            and provenance.get("formal_evaluation_eligible") is False
            and provenance.get("mixed_tier_loading") == "PROHIBITED"
        ),
        "dataset_status": dataset.get("status"),
        "split_formal": split.get("formal_split"),
        "g1_status": dataset.get("g1_status"),
        "g2_status": dataset.get("g2_status"),
    }

    references = [
        dataset["primary_human_gold"],
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

    document_hashes = []
    for reference in dataset.get("documentation", []):
        path = ROOT / reference["path"]
        document_hashes.append(path.is_file() and sha256_file(path) == reference["sha256"])
    checks["documentation"] = {
        "passed": len(document_hashes) == 5 and all(document_hashes),
        "documents_checked": len(document_hashes),
    }

    reproducibility = read_json(MANIFEST_ROOT / "reproducibility-v1.manifest.json")
    checks["reproducibility"] = {
        "passed": (
            reproducibility.get("passed") is True
            and reproducibility.get("mode") == "PYTHON_ISOLATED_STDLIB_ONLY"
            and reproducibility.get("command_returncodes") == [0, 0]
            and reproducibility.get("mismatches") == []
            and reproducibility.get("credential_environment_forwarded") is False
        ),
        "outputs_checked": reproducibility.get("outputs_checked"),
        "mismatches": reproducibility.get("mismatches"),
    }

    matrix = (ROOT / "G1_G2_EVIDENCE_MATRIX.md").read_text(encoding="utf-8")
    handoff = (ROOT / "HANDOFF_10.md").read_text(encoding="utf-8")
    checks["gate_evidence_and_handoff"] = {
        "passed": (
            "BLOCKED_SECOND_PRIMARY_NOT_FROZEN" in matrix
            and "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN" in matrix
            and "提交给：任务00总控审核" in handoff
            and "不创建任务20" in handoff
        ),
        "g1_claimed_pass": False,
        "g2_claimed_pass": False,
    }

    passed = all(result["passed"] for result in checks.values())
    return {
        "schema": "m2-release-check-v1",
        "passed": passed,
        "steps_34_39_local_package_ready": passed,
        "g1_passed": False,
        "g1_status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
        "g2_passed": False,
        "g2_status": "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN",
        "checks": checks,
    }


def main() -> int:
    report = validate_m2_release()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
