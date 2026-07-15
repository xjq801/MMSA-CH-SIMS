"""Audit a locally acquired CSMV I3D-compatible feature package.

The audit is read-only with respect to the feature root. It records fixity for
the 8,210 CSMV-required files, verifies NumPy headers without loading arrays
into memory, and keeps formal-use approval fail-closed while license or asset
revision remains unresolved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEATURE_ROOT = ROOT / "data" / "raw" / "csmv" / "features" / "visual_feature" / "I3D"
DEFAULT_CSMV_ROOT = (
    ROOT
    / "data"
    / "raw"
    / "csmv"
    / "99d14240254b1381dde0b9c56add140381f65117"
    / "CSMV"
)
DEFAULT_OUTPUT = ROOT / "data" / "manifests" / "csmv-i3d-quarantine-v1.manifest.json"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def digest_rows(rows: Iterable[Tuple[str, int, str]]) -> str:
    digest = hashlib.sha256()
    for relative_path, size, checksum in rows:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(checksum.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def expected_video_ids(csmv_root: Path) -> set:
    mapping_path = csmv_root / "Comments_Anno" / "video_to_comment.json"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict):
        raise ValueError("video_to_comment.json must contain an object")
    return {Path(str(value)).stem for value in mapping}


def audit(feature_root: Path, csmv_root: Path, observed_date: str) -> dict:
    feature_root = feature_root.resolve()
    csmv_root = csmv_root.resolve()
    if not feature_root.is_dir():
        raise FileNotFoundError(feature_root)

    expected = expected_video_ids(csmv_root)
    files = sorted(feature_root.glob("*.npy"), key=lambda path: path.name)
    stems = {path.stem for path in files}
    missing = sorted(expected - stems)
    extras = sorted(stems - expected)

    shape_path = feature_root / "feature_shapes.json"
    shape_map: Dict[str, int] = {}
    if shape_path.is_file():
        raw_shape_map = json.loads(shape_path.read_text(encoding="utf-8"))
        if not isinstance(raw_shape_map, dict):
            raise ValueError("feature_shapes.json must contain an object")
        shape_map = {str(key): int(value) for key, value in raw_shape_map.items()}

    required_entries: List[dict] = []
    all_fixity_rows: List[Tuple[str, int, str]] = []
    extra_fixity_rows: List[Tuple[str, int, str]] = []
    schema_errors: List[dict] = []
    shape_map_mismatches: List[dict] = []
    temporal_lengths: List[int] = []
    dtype_counts: Dict[str, int] = {}
    trailing_dimension_counts: Dict[str, int] = {}
    total_bytes = 0
    required_bytes = 0

    for path in files:
        size = path.stat().st_size
        checksum = sha256_file(path)
        relative_path = path.name
        all_fixity_rows.append((relative_path, size, checksum))
        total_bytes += size

        try:
            array = np.load(path, mmap_mode="r", allow_pickle=False)
            shape = [int(value) for value in array.shape]
            dtype = str(array.dtype)
        except Exception as exc:  # pragma: no cover - exercised by corrupt assets
            schema_errors.append(
                {"relative_path": relative_path, "error": type(exc).__name__ + ": " + str(exc)}
            )
            shape = []
            dtype = "UNREADABLE"

        dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1
        trailing_key = str(tuple(shape[1:])) if shape else "UNREADABLE"
        trailing_dimension_counts[trailing_key] = trailing_dimension_counts.get(trailing_key, 0) + 1
        if shape:
            temporal_lengths.append(shape[0])
        if shape != [] and (len(shape) != 2 or shape[1] != 1024 or dtype != "float32"):
            schema_errors.append(
                {"relative_path": relative_path, "shape": shape, "dtype": dtype}
            )
        if path.stem in shape_map and shape and shape_map[path.stem] != shape[0]:
            shape_map_mismatches.append(
                {
                    "relative_path": relative_path,
                    "declared_temporal_length": shape_map[path.stem],
                    "observed_shape": shape,
                }
            )

        entry = {
            "relative_path": relative_path,
            "bytes": size,
            "sha256": checksum,
            "shape": shape,
            "dtype": dtype,
        }
        if path.stem in expected:
            required_entries.append(entry)
            required_bytes += size
        else:
            extra_fixity_rows.append((relative_path, size, checksum))

    feature_shapes_meta = None
    if shape_path.is_file():
        feature_shapes_meta = {
            "relative_path": shape_path.name,
            "bytes": shape_path.stat().st_size,
            "sha256": sha256_file(shape_path),
            "entries": len(shape_map),
            "matching_feature_files": len(set(shape_map) & stems),
            "missing_feature_files": len(set(shape_map) - stems),
            "feature_files_without_declared_shape": len(stems - set(shape_map)),
            "declared_shape_mismatches": len(shape_map_mismatches),
        }

    coverage_passed = len(expected) == 8210 and not missing
    schema_passed = not schema_errors and not shape_map_mismatches
    quarantine_ready = coverage_passed and schema_passed
    required_entries.sort(key=lambda value: value["relative_path"])

    return {
        "schema_version": "csmv-i3d-quarantine-v1",
        "observed_date": observed_date,
        "dataset_id": "CSMV@99d14240254b1381dde0b9c56add140381f65117",
        "feature_family_claim": "I3D",
        "asset_identity_status": "PROVISIONAL_I3D_COMPATIBLE_NOT_RIGHTS_HOLDER_ATTESTED",
        "acquisition_status": "QUARANTINE_ACQUIRED",
        "formal_model_input_allowed": False,
        "g2_asset_credit": False,
        "source": {
            "acquisition_method": "USER_PROVIDED_LOCAL_PACKAGE",
            "tracked_absolute_path": False,
            "source_folder_label": "I3D-feature-001/visual-feature-allCAMV",
            "stable_project_entry": "data/raw/csmv/features/visual_feature/I3D",
            "official_feature_folder_id": "1kSM9J6WdykcJxsfpSTAeE-FyuebUzy9z",
            "asset_revision": "UNKNOWN",
            "asset_license": "UNKNOWN_NOT_EXPLICITLY_COVERED",
        },
        "package": {
            "npy_files": len(files),
            "total_bytes": total_bytes,
            "content_tree_sha256": digest_rows(all_fixity_rows),
            "extra_files": len(extras),
            "extra_bytes": sum(row[1] for row in extra_fixity_rows),
            "extra_content_tree_sha256": digest_rows(extra_fixity_rows),
            "extra_filename_sample": [value + ".npy" for value in extras[:20]],
            "feature_shapes": feature_shapes_meta,
        },
        "coverage": {
            "required_video_file_ids": len(expected),
            "matched_video_file_ids": len(expected & stems),
            "missing_video_file_ids": len(missing),
            "missing_filename_sample": [value + ".npy" for value in missing[:20]],
            "required_bytes": required_bytes,
            "passed": coverage_passed,
        },
        "schema": {
            "expected": "float32[T,1024]",
            "dtype_counts": dict(sorted(dtype_counts.items())),
            "trailing_dimension_counts": dict(sorted(trailing_dimension_counts.items())),
            "temporal_length_min": min(temporal_lengths) if temporal_lengths else None,
            "temporal_length_max": max(temporal_lengths) if temporal_lengths else None,
            "schema_error_count": len(schema_errors),
            "schema_error_sample": schema_errors[:20],
            "shape_map_mismatch_sample": shape_map_mismatches[:20],
            "passed": schema_passed,
        },
        "required_files": required_entries,
        "verdict": {
            "quarantine_integrity_ready": quarantine_ready,
            "formal_use_ready": False,
            "blocking_unknowns": ["asset_level_license", "stable_asset_revision", "rights_holder_fixity_attestation"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature-root", type=Path, default=DEFAULT_FEATURE_ROOT)
    parser.add_argument("--csmv-root", type=Path, default=DEFAULT_CSMV_ROOT)
    parser.add_argument("--observed-date", default="2026-07-15")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest = audit(args.feature_root, args.csmv_root, args.observed_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = {
        "schema": manifest["schema_version"],
        "acquisition_status": manifest["acquisition_status"],
        "npy_files": manifest["package"]["npy_files"],
        "total_bytes": manifest["package"]["total_bytes"],
        "required": manifest["coverage"]["required_video_file_ids"],
        "matched": manifest["coverage"]["matched_video_file_ids"],
        "missing": manifest["coverage"]["missing_video_file_ids"],
        "schema_errors": manifest["schema"]["schema_error_count"],
        "content_tree_sha256": manifest["package"]["content_tree_sha256"],
        "quarantine_integrity_ready": manifest["verdict"]["quarantine_integrity_ready"],
        "formal_use_ready": manifest["verdict"]["formal_use_ready"],
        "output": args.output.as_posix(),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if manifest["verdict"]["quarantine_integrity_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
