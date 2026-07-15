"""Validate the minimum experiment configuration contract without running training."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable

import yaml


FORBIDDEN_MODALITIES = {
    "target_future_comments",
    "final_engagement",
    "future_retrieval_candidates",
    "test_comments",
}


def _get(mapping: Dict[str, Any], path: Iterable[str]) -> Any:
    value: Any = mapping
    traversed = []
    for key in path:
        traversed.append(key)
        if not isinstance(value, dict) or key not in value:
            raise ValueError("missing required field: " + ".".join(traversed))
        value = value[key]
    return value


def validate(config: Dict[str, Any], root: Path) -> None:
    required = [
        ("schema_version",),
        ("experiment_id",),
        ("protocol", "master_plan_version"),
        ("protocol", "experiment_protocol_version"),
        ("protocol", "task_timepoint"),
        ("protocol", "unit_of_analysis"),
        ("protocol", "label_window"),
        ("data", "dataset_id"),
        ("data", "dataset_version"),
        ("data", "split_version"),
        ("data", "manifest"),
        ("data", "index_scope"),
        ("run", "seed"),
        ("run", "input_modalities"),
        ("run", "baseline"),
        ("run", "primary_metric"),
        ("run", "stop_condition"),
        ("run", "output_dir"),
        ("representation_contract", "family"),
        ("representation_contract", "state"),
        ("representation_contract", "sequence_protocol"),
        ("representation_contract", "main_rule"),
        ("representation_contract", "primary_sensitivity"),
        ("representation_contract", "test_adaptation_allowed"),
        ("representation_contract", "all_splits_same_rule"),
        ("modality_contract", "policy"),
        ("modality_contract", "structurally_unavailable"),
        ("modality_contract", "missing_modality_experiment_eligible"),
        ("modality_contract", "not_applicable_reason"),
        ("leakage", "forbidden_inputs"),
        ("leakage", "fit_statistics_on"),
        ("leakage", "test_comments_input_allowed"),
    ]
    for path in required:
        value = _get(config, path)
        if value is None or value == "":
            raise ValueError("empty required field: " + ".".join(path))

    if _get(config, ("protocol", "master_plan_version")) != "v1.12":
        raise ValueError("master plan version must be v1.12")
    if _get(config, ("protocol", "experiment_protocol_version")) != "v2":
        raise ValueError("experiment protocol version must be v2")
    if _get(config, ("protocol", "task_timepoint")) != "T0":
        raise ValueError("bootstrap main-task config must use T0")
    if _get(config, ("data", "index_scope")) != "train_only":
        raise ValueError("retrieval index scope must be train_only")
    if _get(config, ("leakage", "fit_statistics_on")) != "train_only":
        raise ValueError("fit_statistics_on must be train_only")
    if _get(config, ("leakage", "test_comments_input_allowed")) is not False:
        raise ValueError("test comments must not be allowed as input")
    if _get(config, ("modality_contract", "policy")) != "ACTUAL_AVAILABLE_INPUTS_ONLY":
        raise ValueError("modality policy must be ACTUAL_AVAILABLE_INPUTS_ONLY")
    unavailable = set(_get(config, ("modality_contract", "structurally_unavailable")))
    if "audio" not in unavailable:
        raise ValueError("audio must be declared structurally unavailable")
    if _get(config, ("modality_contract", "missing_modality_experiment_eligible")) is not False:
        raise ValueError("bootstrap single-input config is not eligible for missing-modality experiments")
    if (
        _get(config, ("modality_contract", "not_applicable_reason"))
        != "NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY"
    ):
        raise ValueError("single-input not-applicable reason is required")

    if _get(config, ("representation_contract", "family")) != "I3D":
        raise ValueError("bootstrap representation family must be I3D")
    if (
        _get(config, ("representation_contract", "state"))
        != "QUARANTINE_ONLY_PENDING_G2_ASSET_ADMISSION"
    ):
        raise ValueError("I3D must remain quarantine-only before G2 asset admission")
    if (
        _get(config, ("representation_contract", "main_rule"))
        != "FULL_SEQUENCE_DYNAMIC_PADDING_MASK"
    ):
        raise ValueError("frozen I3D main sequence rule mismatch")
    if (
        _get(config, ("representation_contract", "primary_sensitivity"))
        != "UNIFORM_180_ENDPOINT_INCLUSIVE"
    ):
        raise ValueError("frozen I3D sensitivity rule mismatch")
    if _get(config, ("representation_contract", "test_adaptation_allowed")) is not False:
        raise ValueError("test-adaptive I3D sequence processing is prohibited")
    if _get(config, ("representation_contract", "all_splits_same_rule")) is not True:
        raise ValueError("all splits must share the frozen I3D sequence rule")
    sequence_protocol = root / str(_get(config, ("representation_contract", "sequence_protocol")))
    if not sequence_protocol.is_file():
        raise ValueError("sequence protocol does not exist: " + str(sequence_protocol))

    modalities = set(_get(config, ("run", "input_modalities")))
    if modalities & FORBIDDEN_MODALITIES:
        raise ValueError("forbidden future/test input present")
    if "audio" in modalities:
        raise ValueError("structurally unavailable audio cannot be an input modality")
    if len(modalities) != 1:
        raise ValueError("bootstrap config must declare exactly one actually available input modality")
    declared_forbidden = set(_get(config, ("leakage", "forbidden_inputs")))
    if not FORBIDDEN_MODALITIES - {"test_comments"} <= declared_forbidden:
        raise ValueError("all core forbidden inputs must be declared")

    manifest = root / str(_get(config, ("data", "manifest")))
    if not manifest.is_file():
        raise ValueError("manifest does not exist: " + str(manifest))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    config_path = args.config.resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict):
        raise ValueError("configuration root must be a mapping")
    root = Path(__file__).resolve().parents[1]
    validate(config, root)
    print("CONFIG_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
