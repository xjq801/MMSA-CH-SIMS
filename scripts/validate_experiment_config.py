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
        ("leakage", "forbidden_inputs"),
        ("leakage", "fit_statistics_on"),
        ("leakage", "test_comments_input_allowed"),
    ]
    for path in required:
        value = _get(config, path)
        if value is None or value == "":
            raise ValueError("empty required field: " + ".".join(path))

    if _get(config, ("protocol", "master_plan_version")) != "v1.5":
        raise ValueError("master plan version must be v1.5")
    if _get(config, ("protocol", "task_timepoint")) != "T0":
        raise ValueError("bootstrap main-task config must use T0")
    if _get(config, ("data", "index_scope")) != "train_only":
        raise ValueError("retrieval index scope must be train_only")
    if _get(config, ("leakage", "fit_statistics_on")) != "train_only":
        raise ValueError("fit_statistics_on must be train_only")
    if _get(config, ("leakage", "test_comments_input_allowed")) is not False:
        raise ValueError("test comments must not be allowed as input")

    modalities = set(_get(config, ("run", "input_modalities")))
    if modalities & FORBIDDEN_MODALITIES:
        raise ValueError("forbidden future/test input present")
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
