"""Validate HANDOFF_20 evidence bindings without requiring restricted assets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Callable, Mapping


REQUIRED_HANDOFF_TERMS = (
    "DEFERRED_ACCEPTED_RISK",
    "FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH",
    "ASSET_INVALIDATED_DO_NOT_REPORT",
    "NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY",
    "TASK50_NOT_COMPLETED",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def reject_unsafe_paths(value: object) -> None:
    if isinstance(value, Mapping):
        for child in value.values():
            reject_unsafe_paths(child)
        return
    if isinstance(value, list):
        for child in value:
            reject_unsafe_paths(child)
        return
    if not isinstance(value, str):
        return
    normalized = value.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("/"):
        raise ValueError(f"unsafe path in handoff manifest: {value}")
    if ".." in normalized.split("/"):
        raise ValueError(f"unsafe path in handoff manifest: {value}")


def validate_tracked_evidence(
    manifest: Mapping[str, object],
    show_blob: Callable[[str, str], bytes],
) -> int:
    commit = str(manifest.get("evidence_snapshot_commit", ""))
    rows = manifest.get("tracked_evidence")
    if not commit or not isinstance(rows, list) or not rows:
        raise ValueError("missing evidence snapshot commit or tracked evidence")
    checked = 0
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("tracked evidence row must be an object")
        path = str(row.get("path", ""))
        row_commit = str(row.get("commit", commit))
        reject_unsafe_paths({"path": path})
        payload = show_blob(row_commit, path)
        actual_hash = sha256_bytes(payload)
        if actual_hash != row.get("sha256"):
            raise ValueError(f"SHA-256 mismatch for tracked evidence: {path}")
        if len(payload) != row.get("bytes"):
            raise ValueError(f"byte-size mismatch for tracked evidence: {path}")
        checked += 1
    return checked


def validate_handoff_text(text: str, evidence_commit: str, manifest_sha256: str = "") -> None:
    required = (evidence_commit,) + REQUIRED_HANDOFF_TERMS
    if manifest_sha256:
        required += (manifest_sha256,)
    for term in required:
        if term not in text:
            raise ValueError(f"missing required handoff term: {term}")


def git_show_blob(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"])
    except subprocess.CalledProcessError as error:
        raise ValueError(f"cannot read tracked evidence at commit: {path}") from error


def validate_commit(commit: str) -> None:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(f"unknown commit: {commit}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/manifests/task20-handoff-v1.manifest.json"),
    )
    parser.add_argument("--handoff", type=Path, default=Path("HANDOFF_20.md"))
    args = parser.parse_args()

    manifest_payload = args.manifest.read_bytes()
    manifest = json.loads(manifest_payload.decode("utf-8"))
    if manifest.get("schema_version") != "task20-handoff-evidence-v1":
        raise ValueError("unexpected task20 handoff manifest schema")
    reject_unsafe_paths(manifest)
    evidence_commit = str(manifest["evidence_snapshot_commit"])
    submission_commit = str(manifest["submission_status_commit"])
    validate_commit(evidence_commit)
    validate_commit(submission_commit)
    tracked_checked = validate_tracked_evidence(manifest, git_show_blob)
    manifest_hash = sha256_bytes(manifest_payload)
    handoff_payload = args.handoff.read_bytes()
    handoff_text = handoff_payload.decode("utf-8")
    validate_handoff_text(handoff_text, evidence_commit, manifest_hash)
    report = {
        "schema_version": "task20-handoff-validation-v1",
        "passed": True,
        "evidence_snapshot_commit": evidence_commit,
        "submission_status_commit": submission_commit,
        "tracked_evidence_checked": tracked_checked,
        "manifest_sha256": manifest_hash,
        "handoff_sha256": sha256_bytes(handoff_payload),
        "restricted_assets_required": False,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
