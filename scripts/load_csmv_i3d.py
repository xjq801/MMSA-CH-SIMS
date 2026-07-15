"""Read-only loader for one CSMV I3D feature array.

The loader accepts either the official ``video_file_id`` or the canonical
hashed ``item_id``. It never exposes labels or comments and never fits data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Dict

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEATURE_ROOT = ROOT / "data" / "raw" / "csmv" / "features" / "visual_feature" / "I3D"
DEFAULT_VIDEO_MAP = (
    ROOT
    / "data"
    / "raw"
    / "csmv"
    / "99d14240254b1381dde0b9c56add140381f65117"
    / "CSMV"
    / "Comments_Anno"
    / "video_to_comment.json"
)


def stable_id(namespace: str, value: str) -> str:
    return hashlib.sha256((namespace + "|" + value).encode("utf-8")).hexdigest()


def resolve_feature_root(explicit: Path = None) -> Path:
    if explicit is not None:
        root = explicit
    elif os.environ.get("CSMV_I3D_ROOT"):
        root = Path(os.environ["CSMV_I3D_ROOT"])
    else:
        root = DEFAULT_FEATURE_ROOT
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    return root


def canonical_item_lookup(video_map_path: Path = DEFAULT_VIDEO_MAP) -> Dict[str, str]:
    mapping = json.loads(video_map_path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict):
        raise ValueError("video_to_comment.json must contain an object")
    result = {}
    for raw_video_id in mapping:
        video_file_id = Path(str(raw_video_id)).stem
        canonical_item_id = stable_id("csmv-video-v1", video_file_id + ".mp4")
        result[canonical_item_id] = video_file_id
    if len(result) != 8210:
        raise ValueError("expected 8210 canonical CSMV video IDs, got {}".format(len(result)))
    return result


def validate_video_file_id(value: str) -> str:
    video_file_id = Path(str(value)).stem
    if not video_file_id.isdigit():
        raise ValueError("video_file_id must be a numeric CSMV platform ID")
    return video_file_id


def load_by_video_file_id(video_file_id: str, feature_root: Path = None) -> np.ndarray:
    root = resolve_feature_root(feature_root)
    safe_id = validate_video_file_id(video_file_id)
    path = root / (safe_id + ".npy")
    if not path.is_file():
        raise FileNotFoundError(path)
    array = np.load(path, mmap_mode="r", allow_pickle=False)
    if array.ndim != 2 or array.shape[1] != 1024 or array.dtype != np.float32:
        raise ValueError("invalid I3D feature schema at {}: {} {}".format(path, array.shape, array.dtype))
    return array


def load_by_item_id(item_id: str, feature_root: Path = None) -> np.ndarray:
    lookup = canonical_item_lookup()
    if item_id not in lookup:
        raise KeyError("unknown canonical CSMV item_id")
    return load_by_video_file_id(lookup[item_id], feature_root)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video-file-id")
    group.add_argument("--item-id")
    parser.add_argument("--feature-root", type=Path)
    args = parser.parse_args()

    if args.video_file_id:
        array = load_by_video_file_id(args.video_file_id, args.feature_root)
        lookup_key = "video_file_id"
        lookup_value = validate_video_file_id(args.video_file_id)
    else:
        array = load_by_item_id(args.item_id, args.feature_root)
        lookup_key = "item_id"
        lookup_value = args.item_id
    print(
        json.dumps(
            {
                lookup_key: lookup_value,
                "shape": list(array.shape),
                "dtype": str(array.dtype),
                "mmap": True,
                "formal_use_boundary": "QUARANTINE_ONLY_PENDING_ASSET_APPROVAL",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
