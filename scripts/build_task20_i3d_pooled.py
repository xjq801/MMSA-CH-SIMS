"""Build an internal-only, non-reversible mean/std cache from frozen I3D."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import List, Tuple

import numpy as np

from load_csmv_i3d import load_by_item_id
from task20_models import pool_i3d_statistics


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LABELS = ROOT / "data" / "processed" / "HUMAN_GOLD" / "csmv" / "video_labels.v1.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_item_splits(path: Path, split_scheme: str) -> List[Tuple[str, str]]:
    rows = []
    seen = set()
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            item_id = str(row.get("item_id", ""))
            split_map = row.get("split")
            if not item_id or item_id in seen:
                raise ValueError("missing or duplicate item_id at line {}".format(line_number))
            if not isinstance(split_map, dict) or split_map.get(split_scheme) not in {"train", "dev", "test"}:
                raise ValueError("invalid frozen split at line {}".format(line_number))
            rows.append((item_id, split_map[split_scheme]))
            seen.add(item_id)
    if not rows:
        raise ValueError("empty canonical input")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
    parser.add_argument("--split-scheme", default="group_by_video_v1")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    try:
        output_dir.relative_to((ROOT / "results").resolve())
    except ValueError as error:
        raise ValueError("pooled feature cache must stay under ignored results/") from error
    output_dir.mkdir(parents=True, exist_ok=False)

    item_splits = load_item_splits(args.labels.resolve(), args.split_scheme)
    features = np.empty((len(item_splits), 2048), dtype=np.float32)
    for index, (item_id, _) in enumerate(item_splits):
        features[index] = pool_i3d_statistics(load_by_item_id(item_id))
    if not np.isfinite(features).all():
        raise ValueError("pooled feature cache contains non-finite values")

    item_ids = np.asarray([item_id for item_id, _ in item_splits], dtype="<U64")
    splits = np.asarray([split for _, split in item_splits], dtype="<U5")
    cache_path = output_dir / "pooled_features.npz"
    np.savez(cache_path, item_ids=item_ids, splits=splits, features=features)
    counts = {split: int(np.sum(splits == split)) for split in ("train", "dev", "test")}
    metadata = {
        "schema_version": "task20-pooled-i3d-v1",
        "status": "INTERNAL_ONLY_NON_REVERSIBLE_MEAN_STD_DERIVATIVE",
        "source_feature_family": "I3D",
        "pooling": "per_dimension_mean_std_no_label_fit",
        "feature_dimension": 2048,
        "split_scheme": args.split_scheme,
        "split_counts": counts,
        "canonical_labels_sha256": sha256(args.labels.resolve()),
        "cache_sha256": sha256(cache_path),
        "contains_labels": False,
        "contains_raw_sequences": False,
        "redistribution": "PROHIBITED_INTERNAL_RESEARCH_ONLY",
        "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
