"""Rebuild minimal M2 artifacts in an isolated, site-package-free process."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Sequence


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_ROOT = ROOT / "data" / "manifests"
OUTPUTS = [
    "data/processed/HUMAN_GOLD/csmv/video_labels.v1.jsonl",
    "data/processed/SILVER/cuc_igpe_v2/canonical.v1.jsonl",
    "data/processed/SILVER/cuc_igpe_v2/error_review_candidates.v1.jsonl",
    "data/manifests/csmv-primary-raw-v1.manifest.json",
    "data/manifests/csmv-split-v1.manifest.json",
    "data/manifests/cuc-auxiliary-raw-v1.manifest.json",
    "data/manifests/cuc-canonical-v1.manifest.json",
    "data/manifests/human-gold-v1.manifest.json",
    "data/manifests/silver-v1.manifest.json",
    "data/manifests/unlabeled-v1.manifest.json",
    "data/manifests/label-provenance-v1.manifest.json",
    "data/manifests/index-boundary-v1.manifest.json",
    "data/manifests/label-error-review-v1.manifest.json",
    "data/manifests/leakage-audit-v1.manifest.json",
    "data/manifests/split-v1.manifest.json",
    "data/manifests/dataset-v1.manifest.json",
    "M2_LEAKAGE_AUDIT.md",
    "DATA_AUDIT_REPORT_V1.md",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hashes(paths: Sequence[str]) -> Dict[str, str]:
    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        raise FileNotFoundError("missing reproducibility baseline outputs: " + ", ".join(missing))
    return {path: sha256_file(ROOT / path) for path in paths}


def clean_environment() -> dict:
    allowed = ("SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATH")
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env.update({"PYTHONHASHSEED": "0", "PYTHONIOENCODING": "utf-8", "PYTHONNOUSERSITE": "1"})
    return env


def run_checked(command: Sequence[str], env: dict) -> dict:
    result = subprocess.run(command, cwd=str(ROOT), env=env, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return {
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cuc-root", type=Path, required=True)
    args = parser.parse_args()
    cuc_root = args.cuc_root.resolve()
    if not cuc_root.is_dir():
        raise FileNotFoundError(cuc_root)

    before = hashes(OUTPUTS)
    env = clean_environment()
    commands = [
        [sys.executable, "-I", "-S", str(ROOT / "scripts" / "build_m2_data_artifacts.py"), "--cuc-root", str(cuc_root)],
        [sys.executable, "-I", "-S", str(ROOT / "scripts" / "build_m2_release.py")],
    ]
    results = [run_checked(command, env) for command in commands]
    after = hashes(OUTPUTS)
    mismatches = [path for path in OUTPUTS if before[path] != after[path]]
    passed = all(result["returncode"] == 0 for result in results) and not mismatches
    report = {
        "schema_version": "m2-reproducibility-v1",
        "passed": passed,
        "mode": "PYTHON_ISOLATED_STDLIB_ONLY",
        "python": sys.version.split()[0],
        "flags": ["-I", "-S"],
        "site_packages_disabled": True,
        "credential_environment_forwarded": False,
        "raw_inputs_verified_by_manifest": True,
        "commands": [
            "<PYTHON> -I -S scripts/build_m2_data_artifacts.py --cuc-root <CUC_ROOT>",
            "<PYTHON> -I -S scripts/build_m2_release.py",
        ],
        "command_returncodes": [result["returncode"] for result in results],
        "outputs_checked": len(OUTPUTS),
        "mismatches": mismatches,
        "before_sha256": before,
        "after_sha256": after,
        "boundary": "This is a clean isolated process replay, not a fresh OS/container dependency installation; the pipeline is standard-library-only.",
    }
    path = MANIFEST_ROOT / "reproducibility-v1.manifest.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if not passed:
        for index, result in enumerate(results):
            if result["returncode"]:
                print("command {} stdout tail:\n{}".format(index + 1, result["stdout_tail"]))
                print("command {} stderr tail:\n{}".format(index + 1, result["stderr_tail"]))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
