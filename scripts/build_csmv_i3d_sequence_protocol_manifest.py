"""Build the tracked evidence manifest for the frozen I3D sequence protocol."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUARANTINE = ROOT / "data/manifests/csmv-i3d-quarantine-v1.manifest.json"
CONFIG = ROOT / "configs/csmv-i3d-sequence-protocol-v1.json"
OUTPUT = ROOT / "data/manifests/csmv-i3d-sequence-protocol-v1.manifest.json"
EVIDENCE_FILES = [
    "CSMV_I3D_SEQUENCE_PROTOCOL_V1.md",
    "configs/csmv-i3d-sequence-protocol-v1.json",
    "scripts/csmv_i3d_sequence_protocol.py",
    "scripts/build_csmv_i3d_sequence_protocol_manifest.py",
    "scripts/validate_csmv_i3d_sequence_protocol.py",
    "tests/test_csmv_i3d_sequence_protocol.py",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nearest_rank(values, probability: float) -> int:
    ordered = sorted(values)
    return int(ordered[max(0, math.ceil(probability * len(ordered)) - 1)])


def build_manifest() -> dict:
    quarantine = json.loads(QUARANTINE.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    lengths = [int(item["shape"][0]) for item in quarantine["required_files"]]
    if len(lengths) != 8210:
        raise ValueError("expected 8210 required I3D entries")
    profile = {
        "required_samples": len(lengths),
        "min": min(lengths),
        "max": max(lengths),
        "median_nearest_rank": nearest_rank(lengths, 0.50),
        "p90_nearest_rank": nearest_rank(lengths, 0.90),
        "p95_nearest_rank": nearest_rank(lengths, 0.95),
        "p99_nearest_rank": nearest_rank(lengths, 0.99),
        "equal_180": sum(value == 180 for value in lengths),
        "greater_than_180": sum(value > 180 for value in lengths),
        "maximum_single_input_bytes": max(lengths) * 1024 * 4,
    }
    expected = config["observed_input_profile"]
    if (
        profile["required_samples"] != expected["required_samples"]
        or profile["min"] != expected["min_temporal_steps"]
        or profile["max"] != expected["max_temporal_steps"]
        or profile["equal_180"] != expected["count_equal_180"]
        or profile["greater_than_180"] != expected["count_greater_than_180"]
    ):
        raise ValueError("frozen config does not match quarantine length evidence")
    return {
        "schema_version": "csmv-i3d-sequence-protocol-manifest-v1",
        "freeze_date": "2026-07-16",
        "status": "PREREGISTERED_BEFORE_TEST_RESULTS",
        "selection_basis": "PRE_TEST_INPUT_LENGTH_AUDIT_ONLY",
        "source_quarantine_manifest": {
            "path": QUARANTINE.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(QUARANTINE),
            "content_tree_sha256": quarantine["package"]["content_tree_sha256"],
            "coverage": "8210_OF_8210",
        },
        "length_profile": profile,
        "protocol": {
            "main": config["main_protocol"],
            "primary_sensitivity": config["primary_sensitivity"],
            "supplementary_sensitivity": config["supplementary_sensitivity"],
            "same_rule_all_splits": config["all_splits_same_rule"],
            "test_adaptation_allowed": config["test_adaptation_allowed"],
            "mask_true_means": config["mask_true_means"],
            "randomness": config["randomness"],
            "batching": config["batching"],
        },
        "paper_claim_contract": {
            "allowed": "PUBLIC_INDUCED_AUDIENCE_AFFECT_DISTRIBUTION_FORECASTING_ON_FROZEN_I3D_VISUAL_REPRESENTATIONS",
            "prohibited": [
                "END_TO_END_VIDEO_ENCODING",
                "RAW_FRAME_LEARNING",
                "AUDIO_VISUAL_FUSION",
                "AUDIO_GAIN",
                "COMMENT_TEXT_AS_T0_STUDENT_INPUT",
            ],
            "audio": "STRUCTURALLY_UNAVAILABLE_NOT_IMPUTED",
            "e1": "ALL_AVAILABLE_INPUTS_EQUALS_I3D_ONLY",
            "e5": "NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY",
            "h3": "NOT_APPLICABLE_NO_ELIGIBLE_MULTIMODAL_PROTOCOL_UNLESS_ANOTHER_PROTOCOL_QUALIFIES",
        },
        "external_attestation": "DEFERRED_ACCEPTED_RISK",
        "gate_state": {
            "g1": "PASS",
            "g2": "PASS_WITH_ACCEPTED_ASSET_RISK",
            "g2_protocol_data": "PASS_WITH_LIMITATIONS",
            "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
            "formal_split": True,
            "task20_authorized": True,
            "asset_redistribution_allowed": False,
        },
        "evidence_files": [
            {"path": relative, "sha256": sha256_file(ROOT / relative)}
            for relative in EVIDENCE_FILES
        ],
    }


def main() -> int:
    manifest = build_manifest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "schema": manifest["schema_version"],
                "status": manifest["status"],
                "main": manifest["protocol"]["main"],
                "primary_sensitivity": manifest["protocol"]["primary_sensitivity"],
                "required_samples": manifest["length_profile"]["required_samples"],
                "greater_than_180": manifest["length_profile"]["greater_than_180"],
                "g2": manifest["gate_state"]["g2"],
                "output": OUTPUT.relative_to(ROOT).as_posix(),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
