#!/usr/bin/env python3
"""Fetch only the small, pre-approved public assets used by the M1 audit.

Raw files are written below ``data/raw`` (Git-ignored).  A reviewable manifest
containing source URLs, sizes and SHA-256 digests is written to
``data/manifests``.  This script deliberately has no media or feature-bundle
download target.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw"
MANIFEST_ROOT = ROOT / "data" / "manifests"
USER_AGENT = "MMSA-CH-SIMS-M1-audit/1.0"


@dataclass(frozen=True)
class Asset:
    path: str
    url: str
    expected_bytes: int


@dataclass(frozen=True)
class Source:
    source_id: str
    revision: str
    license_status: str
    assets: tuple[Asset, ...]


CSMV_REVISION = "99d14240254b1381dde0b9c56add140381f65117"
CSMV_BASE = f"https://raw.githubusercontent.com/IEIT-AGI/MSA-CRVI/{CSMV_REVISION}"
INEWS_REVISION = "a7ad599a257e94f04f796a86d39635adadb5f7cb"
INEWS_BASE = f"https://huggingface.co/datasets/pitehu/inews_public/resolve/{INEWS_REVISION}"

SOURCES = {
    "csmv": Source(
        source_id="DS-001",
        revision=CSMV_REVISION,
        license_status="annotations: CC-BY-SA-4.0 per upstream README; media excluded",
        assets=tuple(
            Asset(path, f"{CSMV_BASE}/{path}", size)
            for path, size in (
                ("README.md", 9334),
                ("LICENSE", 11357),
                ("CSMV/CSMV_rawLinks.xlsx", 403915),
                ("CSMV/Comments_Anno/dev_set.json", 468438),
                ("CSMV/Comments_Anno/emotion_label_map.json", 141),
                ("CSMV/Comments_Anno/lable_data_dict.json.zip", 3895749),
                ("CSMV/Comments_Anno/opinion_label_map.json", 58),
                ("CSMV/Comments_Anno/test_set.json", 937253),
                ("CSMV/Comments_Anno/train_set.json", 3277800),
                ("CSMV/Comments_Anno/video_to_comment.json", 5432745),
            )
        ),
    ),
    "inews": Source(
        source_id="DS-002",
        revision=INEWS_REVISION,
        license_status="CC-BY-NC-SA-4.0; public non-persona release; media excluded",
        assets=tuple(
            Asset(path, f"{INEWS_BASE}/{path}?download=true", size)
            for path, size in (
                ("README.md", 5159),
                ("survey_codebook.json", 3109),
                ("dev.csv", 360919),
                ("test_cold_start_public.csv", 1172002),
                ("test_generalization_public.csv", 3898213),
                ("test_personalization_public.csv", 3854192),
                ("train.csv", 17209148),
            )
        ),
    ),
    "nemo": Source(
        source_id="DS-003",
        revision="ACL-Anthology-2022-11-21",
        license_status="UNKNOWN: package inspection only; no research use promoted",
        assets=(
            Asset(
                "2022.aacl-main.29.Dataset.zip",
                "https://aclanthology.org/attachments/2022.aacl-main.29.Dataset.zip",
                2080204,
            ),
        ),
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(asset: Asset, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(asset.url, headers={"User-Agent": USER_AGENT})
    temporary = destination.with_suffix(destination.suffix + ".part")
    try:
        with urllib.request.urlopen(request, timeout=60) as response, temporary.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        actual_bytes = temporary.stat().st_size
        if actual_bytes != asset.expected_bytes:
            raise ValueError(
                f"size mismatch for {asset.path}: expected {asset.expected_bytes}, got {actual_bytes}"
            )
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def fetch(name: str) -> Path:
    source = SOURCES[name]
    destination_root = RAW_ROOT / name / source.revision
    MANIFEST_ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = MANIFEST_ROOT / f"{name}-source-v1.manifest.json"
    previous = (
        json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest_path.is_file()
        else {}
    )
    previous_files = {
        item["relative_path"]: item for item in previous.get("files", [])
    }
    records = []
    for asset in source.assets:
        destination = destination_root / asset.path
        downloaded = False
        if not destination.exists() or destination.stat().st_size != asset.expected_bytes:
            download(asset, destination)
            downloaded = True
        prior = previous_files.get(asset.path, {})
        records.append(
            {
                "relative_path": asset.path,
                "source_url": asset.url,
                "retrieved_date": (
                    date.today().isoformat()
                    if downloaded
                    else prior.get("retrieved_date", previous.get("retrieved_date", date.today().isoformat()))
                ),
                "bytes": destination.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    manifest = {
        "schema_version": "m1-source-manifest-v1",
        "source_id": source.source_id,
        "dataset": name,
        "upstream_revision": source.revision,
        "retrieved_date": previous.get("retrieved_date", date.today().isoformat()),
        "license_status_at_retrieval": source.license_status,
        "raw_root": str(destination_root.relative_to(ROOT)).replace("\\", "/"),
        "files": records,
        "excluded": ["media", "feature bundles", "persona data", "credentials"],
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "datasets",
        nargs="+",
        choices=sorted(SOURCES),
        help="Only the listed small public audit assets are supported.",
    )
    args = parser.parse_args()
    for dataset in args.datasets:
        path = fetch(dataset)
        print(f"{dataset}: manifest={path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
