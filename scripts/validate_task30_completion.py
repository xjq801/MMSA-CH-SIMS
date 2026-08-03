"""Validate the tracked, aggregate-only Task30 completion freeze."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Mapping


EXPECTED_BOUNDARIES = {
    "independent_00_review": "EXTERNAL_REVIEW_REQUIRED_NOT_SELF_APPROVABLE",
    "second_comment_bearing_dataset": "NOT_EVALUABLE_DATA_NOT_RELEASED",
    "teacher_only_dev_upper_bound": "NOT_COMPARABLE_DEV_RESPONSES_PROHIBITED",
    "sarcasm": "NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE",
    "cross_domain_h1": "NOT_APPLICABLE_NO_SECOND_COMMENT_BEARING_DATASET",
    "video2reaction_h1": "NOT_APPLICABLE_DATA_NOT_RELEASED",
}
EXPECTED_RUNS = {"search", "replay", "seed_20260803", "seed_20260804"}
PRIVATE_KEYS = {
    "argv",
    "local_path",
    "model_state",
    "model_weights",
    "prediction_rows",
    "sample_id",
    "sample_ids",
}


def _require_mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ValueError("{} must be a mapping".format(name))
    return value


def _reject_private_keys(value: object, path: str = "root") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in PRIVATE_KEYS:
                raise ValueError("private field is prohibited: {}.{}".format(path, key))
            _reject_private_keys(child, "{}.{}".format(path, key))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_private_keys(child, "{}[{}]".format(path, index))


def _require_hex(value: object, length: int, name: str) -> None:
    text = str(value)
    if len(text) != length or any(char not in "0123456789abcdef" for char in text):
        raise ValueError("{} must be a lowercase {}-character hex digest".format(name, length))


def validate_completion_freeze(freeze: Mapping[str, object]) -> None:
    _reject_private_keys(freeze)
    if freeze.get("schema_version") != "task30-completion-freeze-v1":
        raise ValueError("unexpected Task30 completion schema")
    if freeze.get("evidence_identity") != "DEVELOPMENT_EVIDENCE_ONLY":
        raise ValueError("Task30 evidence must remain development-only")
    if freeze.get("decision") != "NOT_PASSED_MECHANISM_NOT_STABLE":
        raise ValueError("Task30 cannot self-promote the H1 gate")
    _require_hex(freeze.get("code_commit"), 40, "code_commit")

    runs = _require_mapping(freeze.get("runs"), "runs")
    if set(runs) != EXPECTED_RUNS:
        raise ValueError("completion freeze must identify every required clean run")
    for run_id in sorted(EXPECTED_RUNS):
        run = _require_mapping(runs[run_id], "run {}".format(run_id))
        _require_hex(run.get("manifest_sha256"), 64, "{} manifest_sha256".format(run_id))
        if run.get("git_dirty") is not False or run.get("exit_code") != 0:
            raise ValueError("run {} is not a clean successful run".format(run_id))

    reproducibility = _require_mapping(freeze.get("reproducibility"), "reproducibility")
    if reproducibility.get("same_seed_prediction_byte_identical") is not True:
        raise ValueError("same-seed predictions are not byte-identical")
    if reproducibility.get("same_seed_model_hashes_identical") is not True:
        raise ValueError("same-seed model hashes are not identical")

    data_flow = _require_mapping(freeze.get("data_flow"), "data flow")
    if data_flow.get("artifact") != "TASK30_DATA_FLOW.md":
        raise ValueError("data flow artifact identity is missing or altered")
    _require_hex(data_flow.get("sha256"), 64, "data flow sha256")
    if data_flow.get("test_comment_access") != "UNREACHABLE":
        raise ValueError("data flow does not close test-comment access")
    if data_flow.get("test_rows") != "NOT_MATERIALIZED":
        raise ValueError("data flow does not close formal-test materialization")

    boundaries = _require_mapping(freeze.get("boundaries"), "boundaries")
    if dict(boundaries) != EXPECTED_BOUNDARIES:
        raise ValueError("completion boundary set is incomplete or altered")
    if freeze.get("test_access") != "TEST_ROWS_NOT_MATERIALIZED_OR_USED":
        raise ValueError("formal test access boundary is not closed")
    if freeze.get("privacy_boundary") != (
        "TRACKED_AGGREGATES_ONLY_NO_SAMPLE_IDS_PATHS_WEIGHTS_OR_PREDICTION_ROWS"
    ):
        raise ValueError("tracked privacy boundary is not closed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("experiments/task30-h1-development-v1/completion-freeze.json"),
    )
    args = parser.parse_args()
    freeze = json.loads(args.path.read_text(encoding="utf-8"))
    validate_completion_freeze(freeze)
    data_flow = _require_mapping(freeze.get("data_flow"), "data flow")
    data_flow_path = Path(str(data_flow["artifact"]))
    if not data_flow_path.is_file():
        raise ValueError("data flow artifact does not exist")
    observed_hash = hashlib.sha256(data_flow_path.read_bytes()).hexdigest()
    if observed_hash != data_flow["sha256"]:
        raise ValueError("data flow artifact hash mismatch")
    print("PASS Task30 completion freeze: {}".format(args.path.as_posix()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
