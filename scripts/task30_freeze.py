"""Build a tracked, aggregate-only Task30 freeze from a private run bundle."""
from __future__ import annotations

from typing import Dict, Mapping


_PRIVATE_KEYS = {"sample_id", "sample_ids", "predictions", "argv", "local_path"}


def _reject_private_keys(value, path="root") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in _PRIVATE_KEYS:
                raise ValueError("private field is not allowed in nonsecret freeze: {}.{}".format(path, key))
            _reject_private_keys(child, "{}.{}".format(path, key))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_private_keys(child, "{}[{}]".format(path, index))


def build_nonsecret_freeze(
    aggregate: Mapping[str, object],
    manifest: Mapping[str, object],
) -> Dict[str, object]:
    _reject_private_keys(aggregate)
    if aggregate.get("evidence_identity") != "DEVELOPMENT_EVIDENCE_ONLY":
        raise ValueError("aggregate has the wrong evidence identity")
    git = manifest.get("git")
    if not isinstance(git, Mapping) or git.get("dirty") is not False:
        raise ValueError("nonsecret freeze requires a clean committed run")
    commit = str(git.get("commit", ""))
    if len(commit) != 40:
        raise ValueError("nonsecret freeze requires a full git commit")
    rows = aggregate.get("rows")
    if not isinstance(rows, Mapping) or not rows:
        raise ValueError("aggregate rows are required")
    selected_configs = {}
    aggregate_metrics = {}
    for row_id, row in sorted(rows.items()):
        if not isinstance(row, Mapping) or "selected_config" not in row or "dev_metrics" not in row:
            raise ValueError("aggregate row is incomplete")
        selected_configs[str(row_id)] = dict(row["selected_config"])
        aggregate_metrics[str(row_id)] = dict(row["dev_metrics"])
    return {
        "schema_version": "task30-nonsecret-freeze-v1",
        "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
        "run_identity": {
            "run_id": str(manifest.get("run_id", "")),
            "git_commit": commit,
            "manifest_schema": str(manifest.get("schema_version", "")),
        },
        "selected_configs": selected_configs,
        "aggregate_metrics": aggregate_metrics,
        "teacher_audit": aggregate.get("teacher_audit"),
        "teacher_confidence_analysis": aggregate.get("teacher_confidence_analysis"),
        "test_access": aggregate.get("test_access"),
        "privacy_boundary": "TRACKED_AGGREGATES_ONLY_NO_SAMPLE_IDS_PATHS_WEIGHTS_OR_PREDICTION_ROWS",
    }
