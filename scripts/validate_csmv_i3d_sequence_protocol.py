"""Validate protocol fixity, deterministic behavior, and fail-closed rules."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

import numpy as np

from csmv_i3d_sequence_protocol import (
    ProtocolViolation,
    collate_full_sequences,
    first_180_supplementary,
    plan_deterministic_batches,
    uniform_180_sensitivity,
    validate_feature_array,
    validate_protocol_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs/csmv-i3d-sequence-protocol-v1.json"
MANIFEST = ROOT / "data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json"
QUARANTINE = ROOT / "data/manifests/csmv-i3d-quarantine-v1.manifest.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def must_reject(call: Callable[[], object]) -> bool:
    try:
        call()
    except ProtocolViolation:
        return True
    return False


def validate() -> dict:
    required = [CONFIG, MANIFEST, QUARANTINE]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"schema": "csmv-i3d-sequence-protocol-check-v1", "passed": False, "checks": checks}

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    quarantine = json.loads(QUARANTINE.read_text(encoding="utf-8"))
    try:
        validate_protocol_config(config)
        config_valid = True
    except ProtocolViolation:
        config_valid = False
    checks["frozen_config"] = {
        "passed": config_valid,
        "main": config.get("main_protocol"),
        "primary_sensitivity": config.get("primary_sensitivity"),
    }

    evidence_hashes = [
        (ROOT / item["path"]).is_file()
        and sha256_file(ROOT / item["path"]) == item["sha256"]
        for item in manifest.get("evidence_files", [])
    ]
    checks["manifest_fixity"] = {
        "passed": (
            manifest.get("schema_version") == "csmv-i3d-sequence-protocol-manifest-v1"
            and manifest.get("status") == "PREREGISTERED_BEFORE_TEST_RESULTS"
            and manifest.get("source_quarantine_manifest", {}).get("sha256") == sha256_file(QUARANTINE)
            and len(evidence_hashes) == 6
            and all(evidence_hashes)
        ),
        "evidence_files_checked": len(evidence_hashes),
    }
    profile = manifest.get("length_profile", {})
    checks["input_length_evidence"] = {
        "passed": (
            len(quarantine.get("required_files", [])) == 8210
            and profile.get("required_samples") == 8210
            and profile.get("min") == 6
            and profile.get("max") == 1719
            and profile.get("equal_180") == 4
            and profile.get("greater_than_180") == 531
        ),
        "profile": profile,
    }

    short = np.arange(6 * 1024, dtype=np.float32).reshape(6, 1024)
    long = np.arange(181 * 1024, dtype=np.float32).reshape(181, 1024)
    full, full_mask, full_lengths = collate_full_sequences([short, long])
    uniform_a = uniform_180_sensitivity(long)
    uniform_b = uniform_180_sensitivity(long)
    first = first_180_supplementary(long)
    checks["positive_and_boundary"] = {
        "passed": (
            full.shape == (2, 181, 1024)
            and full_mask.dtype == np.bool_
            and full_lengths.tolist() == [6, 181]
            and uniform_a[0].shape == (180, 1024)
            and int(uniform_a[2][0]) == 0
            and int(uniform_a[2][-1]) == 180
            and first[2].tolist() == list(range(180))
        )
    }
    digest_a = hashlib.sha256(
        uniform_a[0].tobytes() + uniform_a[1].tobytes() + uniform_a[2].tobytes()
    ).hexdigest()
    digest_b = hashlib.sha256(
        uniform_b[0].tobytes() + uniform_b[1].tobytes() + uniform_b[2].tobytes()
    ).hexdigest()
    plan_a = plan_deterministic_batches({"x": 6, "y": 180, "z": 1719})
    plan_b = plan_deterministic_batches({"x": 6, "y": 180, "z": 1719})
    checks["determinism"] = {
        "passed": digest_a == digest_b and plan_a == plan_b,
        "uniform_output_sha256": digest_a,
        "batch_plan_sha256": hashlib.sha256(
            json.dumps(plan_a, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }

    invalid = [
        np.empty((0, 1024), dtype=np.float32),
        np.empty((3,), dtype=np.float32),
        np.empty((3, 512), dtype=np.float32),
        np.empty((3, 1024), dtype=np.float64),
    ]
    nonfinite = np.zeros((3, 1024), dtype=np.float32)
    nonfinite[0, 0] = np.inf
    bad_config = dict(config, test_adaptation_allowed=True)
    test_override = dict(config, split_specific_overrides={"test": {"max_steps": 180}})
    checks["negative_fail_closed"] = {
        "passed": (
            all(must_reject(lambda value=value: validate_feature_array(value)) for value in invalid)
            and must_reject(lambda: validate_feature_array(nonfinite))
            and must_reject(lambda: validate_protocol_config(bad_config))
            and must_reject(lambda: validate_protocol_config(test_override))
            and must_reject(lambda: collate_full_sequences([long] * 64, max_padded_steps=1000))
        ),
        "cases": 8,
    }
    gate = manifest.get("gate_state", {})
    claim = manifest.get("paper_claim_contract", {})
    checks["honest_boundary"] = {
        "passed": (
            manifest.get("external_attestation") == "DEFERRED_ACCEPTED_RISK"
            and gate.get("g1") == "PASS"
            and gate.get("g2") == "PASS_WITH_ACCEPTED_ASSET_RISK"
            and gate.get("g2_protocol_data") == "PASS_WITH_LIMITATIONS"
            and gate.get("asset_admissibility") == "DEFERRED_ACCEPTED_RISK"
            and gate.get("formal_split") is True
            and gate.get("task20_authorized") is True
            and gate.get("asset_redistribution_allowed") is False
            and claim.get("audio") == "STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED"
            and "END_TO_END_VIDEO_ENCODING" in claim.get("prohibited", [])
            and "COMMENT_TEXT_AS_T0_STUDENT_INPUT" in claim.get("prohibited", [])
        )
    }
    passed = all(item["passed"] for item in checks.values())
    return {
        "schema": "csmv-i3d-sequence-protocol-check-v1",
        "passed": passed,
        "status": "PASS_PROTOCOL_G2_RISK_ACCEPTED_TASK20_AUTHORIZED" if passed else "PROTOCOL_VALIDATION_FAILED",
        "checks": checks,
    }


def main() -> int:
    report = validate()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
