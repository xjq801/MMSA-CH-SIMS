"""Frozen configuration and run-manifest contracts for task 20."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable

ROOT = Path(__file__).resolve().parents[1]

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("config root must be an object")
    return value


def validate_config(config: Dict[str, object], schema_path: Path) -> None:
    with schema_path.open("r", encoding="utf-8") as stream:
        schema = json.load(stream)
    try:
        import jsonschema
    except ImportError as error:
        raise RuntimeError("jsonschema is required to validate task20 config") from error
    jsonschema.validate(instance=config, schema=schema)
    if config["data"]["fit_scope"] != "train_only":
        raise ValueError("fit_scope must be train_only")
    if config["data"]["split_scheme"] != "group_by_video_v1":
        raise ValueError("formal task20 config must use group_by_video_v1")
    if config["protocol"]["test_adaptation_allowed"] is not False:
        raise ValueError("test adaptation is prohibited")


def _file_entry(path: Path) -> Dict[str, str]:
    resolved = path.resolve()
    try:
        safe_path = resolved.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise ValueError("run manifest paths must stay inside the repository") from error
    return {"path": safe_path, "sha256": _sha256(resolved)}


def build_run_manifest(
    run_id: str,
    config: Dict[str, object],
    config_path: Path,
    input_paths: Iterable[Path],
    code_paths: Iterable[Path],
    git_commit: str,
    git_dirty: bool,
) -> Dict[str, object]:
    return {
        "schema_version": "task20-run-manifest-v1",
        "run_id": run_id,
        "experiment_id": config["experiment_id"],
        "model": config["model"],
        "fit_scope": config["data"]["fit_scope"],
        "split_scheme": config["data"]["split_scheme"],
        "config": _file_entry(config_path),
        "inputs": [_file_entry(path) for path in input_paths],
        "code": [_file_entry(path) for path in code_paths],
        "git": {"commit": git_commit, "dirty": bool(git_dirty)},
        "status": "CREATED_NOT_RUN",
        "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
    }
