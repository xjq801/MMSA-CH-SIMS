"""Repeatable local acceptance checks for the M1 preparation package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

from validate_experiment_config import validate


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    ".gitignore",
    ".env.example",
    "T0_INPUT_POLICY.md",
    "DATA_SOURCE_LEDGER.md",
    "ENVIRONMENT_LOCK.md",
    "requirements-lock.txt",
    "PROJECT_STRUCTURE_POLICY.md",
    "configs/experiment.bootstrap.yaml",
    "experiments/EXPERIMENT_REGISTRY.md",
    "CLAIM_EVIDENCE_MATRIX.md",
    "SECURITY_COMPLIANCE_CHECKLIST.md",
    "RESOURCE_TIME_POLICY.md",
    "references/references.bib",
]
IGNORED_SAMPLES = [
    ".env",
    "data/raw/sample.bin",
    "data/processed/sample.pkl",
    "models/a.pt",
    "results/run.json",
]
TRACKED_SAMPLES = [
    ".env.example",
    "configs/experiment.bootstrap.yaml",
    "data/raw/README.md",
    "data/processed/README.md",
    "data/manifests/README.md",
    "paper/README.md",
    "references/references.bib",
]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yaml", ".yml", ".json", ".toml"}
SKIP_PARTS = {".git", ".venv", "data", "models", "saved_models", "installers", "__pycache__"}
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic_assignment": re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']([^\"'\s]{12,})[\"']"
    ),
}


def secret_hits():
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".env", ".env.example"}:
            continue
        for line_number, line in enumerate(path.read_text("utf-8", errors="ignore").splitlines(), 1):
            for kind, pattern in SECRET_PATTERNS.items():
                match = pattern.search(line)
                if not match or "os.getenv" in line or "environ.get" in line or "${" in line:
                    continue
                fingerprint = hashlib.sha256(match.group(0).encode()).hexdigest()[:12]
                hits.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "line": line_number,
                        "type": kind,
                        "fingerprint": fingerprint,
                    }
                )
    return hits


def main() -> int:
    checks = {}
    checks["required_files"] = {
        "passed": all((ROOT / path).is_file() for path in REQUIRED_FILES),
        "missing": [path for path in REQUIRED_FILES if not (ROOT / path).is_file()],
    }

    with (ROOT / "configs" / "experiment.bootstrap.yaml").open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)
    try:
        validate(config, ROOT)
        config_error = None
    except Exception as error:  # report exact local validation failure
        config_error = str(error)
    checks["experiment_config"] = {"passed": config_error is None, "error": config_error}

    imports = {
        name: importlib.util.find_spec(name) is not None
        for name in ["torch", "catboost", "transformers", "sklearn", "MMSA"]
    }
    checks["historical_environment"] = {"passed": all(imports.values()), "imports": imports}
    checks["formal_carm_environment"] = {
        "passed": importlib.util.find_spec("faiss") is not None,
        "faiss_available": importlib.util.find_spec("faiss") is not None,
        "classification": "BLOCKED_M1" if importlib.util.find_spec("faiss") is None else "READY_FOR_REVIEW",
    }

    ignored = {}
    for sample in IGNORED_SAMPLES:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", sample],
            cwd=str(ROOT),
            check=False,
        )
        ignored[sample] = result.returncode == 0
    checks["git_ignore"] = {"passed": all(ignored.values()), "samples": ignored}

    tracked = {}
    for sample in TRACKED_SAMPLES:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", sample],
            cwd=str(ROOT),
            check=False,
        )
        tracked[sample] = result.returncode != 0
    checks["git_trackable_policy_files"] = {
        "passed": all(tracked.values()),
        "samples": tracked,
    }

    hits = secret_hits()
    checks["secret_scan"] = {"passed": not hits, "hits": hits}

    placeholders = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text("utf-8", errors="ignore")
        for token in ["{{", "TODO_TEMPLATE", "[待填写]", "REPLACE_BEFORE_RUN"]:
            if token in text:
                placeholders.append({"file": relative, "token": token})
    checks["template_residuals"] = {"passed": not placeholders, "hits": placeholders}

    blocking = [
        name
        for name, result in checks.items()
        if name != "formal_carm_environment" and not result["passed"]
    ]
    report = {
        "schema": "mmsa.preparation-check.v1",
        "python": sys.version.split()[0],
        "checks": checks,
        "m1_read_only_work_ready": not blocking,
        "formal_model_work_ready": not blocking and checks["formal_carm_environment"]["passed"],
        "blocking_checks": blocking,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["m1_read_only_work_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
