"""Fail-closed comparison for two Task 20 fixed-seed run bundles."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple


REPRODUCIBILITY_ARTIFACTS = (
    "predictions.jsonl",
    "metrics.json",
    "selection.json",
    "trial_results.json",
)
ENVIRONMENT_FIELDS = ("python", "platform", "numpy", "torch", "torch_cuda", "gpu", "device", "dtype", "amp")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> Dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path.name}")
    return value


def _canonical_rows(rows: Iterable[Mapping[str, object]], key: str) -> List[Tuple[object, ...]]:
    canonical = []
    for row in rows:
        canonical.append((row.get(key), row.get("file"), row.get("sha256"), row.get("bytes")))
    return sorted(canonical, key=lambda row: tuple("" if value is None else str(value) for value in row))


def _verify_artifacts(run_dir: Path, manifest: Mapping[str, object]) -> Dict[str, str]:
    declared = {str(row["file"]): row for row in manifest.get("artifacts", [])}
    verified = {}
    for filename, row in declared.items():
        path = run_dir / filename
        if not path.is_file():
            raise ValueError(f"missing declared artifact: {filename}")
        actual = sha256(path)
        if actual != row.get("sha256"):
            raise ValueError(f"artifact fixity mismatch: {filename}")
        if path.stat().st_size != row.get("bytes"):
            raise ValueError(f"artifact byte-size mismatch: {filename}")
        verified[filename] = actual
    return verified


def _identity(manifest: Mapping[str, object], environment: Mapping[str, object]) -> Dict[str, object]:
    return {
        "schema_version": manifest.get("schema_version"),
        "experiment_id": manifest.get("experiment_id"),
        "model": manifest.get("model"),
        "fit_scope": manifest.get("fit_scope"),
        "split_scheme": manifest.get("split_scheme"),
        "evaluation_split": manifest.get("evaluation_split"),
        "seed": manifest.get("seed"),
        "status": manifest.get("status"),
        "smoke": manifest.get("smoke"),
        "config": manifest.get("config"),
        "inputs": _canonical_rows(manifest.get("inputs", []), "role"),
        "code": _canonical_rows(manifest.get("code", []), "file"),
        "environment": {field: environment.get(field) for field in ENVIRONMENT_FIELDS},
    }


def compare_run_dirs(first_dir: Path, second_dir: Path) -> Dict[str, object]:
    first_dir = Path(first_dir)
    second_dir = Path(second_dir)
    first_manifest = _load_json(first_dir / "run-manifest.json")
    second_manifest = _load_json(second_dir / "run-manifest.json")
    for label, manifest in (("first", first_manifest), ("second", second_manifest)):
        if manifest.get("git", {}).get("dirty") is not False:
            raise ValueError(f"{label} run is dirty")
        if manifest.get("status") != "COMPLETED":
            raise ValueError(f"{label} run is not completed")
    first_hashes = _verify_artifacts(first_dir, first_manifest)
    second_hashes = _verify_artifacts(second_dir, second_manifest)
    first_environment = _load_json(first_dir / "environment.json")
    second_environment = _load_json(second_dir / "environment.json")
    if _identity(first_manifest, first_environment) != _identity(second_manifest, second_environment):
        raise ValueError("run identity mismatch")

    artifact_hashes = {}
    for filename in REPRODUCIBILITY_ARTIFACTS:
        if filename not in first_hashes or filename not in second_hashes:
            raise ValueError(f"missing reproducibility artifact: {filename}")
        if first_hashes[filename] != second_hashes[filename]:
            raise ValueError(f"reproducibility artifact mismatch: {filename}")
        artifact_hashes[filename] = first_hashes[filename]

    commits = [str(first_manifest["git"]["commit"]), str(second_manifest["git"]["commit"])]
    return {
        "schema_version": "task20-fixed-seed-reproducibility-comparison-v1",
        "passed": True,
        "comparison_scope": "SAME_ENVIRONMENT_FIXED_SEED",
        "run_ids": [first_manifest.get("run_id"), second_manifest.get("run_id")],
        "seed": first_manifest.get("seed"),
        "evaluation_split": first_manifest.get("evaluation_split"),
        "matching_artifacts": len(artifact_hashes),
        "artifact_sha256": artifact_hashes,
        "differing_git_commits": commits if commits[0] != commits[1] else [],
        "code_identity": "MATCHED_BY_DECLARED_FILE_SHA256",
        "boundary": "does_not_establish_cross_hardware_or_cross_release_bitwise_reproducibility",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("first_run", type=Path)
    parser.add_argument("second_run", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = compare_run_dirs(args.first_run, args.second_run)
    payload = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
