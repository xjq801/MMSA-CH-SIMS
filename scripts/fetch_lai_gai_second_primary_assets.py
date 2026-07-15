"""Fetch the public LAI-GAI image tree under the task-00 resolution authorization.

The script is deliberately limited to the official project host.  It serializes
all requests, preserves the public page snapshots in the Git-ignored raw area,
and maps the website storage suffix back to the frozen image names in the
human-rating summary.  It never reads credentials or follows third-party URLs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw" / "lai-gai" / "second-primary-resolution" / "20260714"
BASE = "https://www.affectdatabases.amu.edu.pl"
ALLOWED_HOST = "www.affectdatabases.amu.edu.pl"
RATING_SUMMARY = RAW_ROOT / "image_emotion_means_S123456.csv"
PAGE_DIR = RAW_ROOT / "image-browser-pages"
IMAGE_DIR = RAW_ROOT / "images"
RAW_MANIFEST = RAW_ROOT / "image-download-manifest.json"
MIN_INTERVAL_SECONDS = 1.1
# Django's storage layer inserts a seven-character token immediately before
# the final extension for ordinary names, but before an earlier dotted suffix
# for names such as ``6250.1_midj_sa.jpg``.  Only accept the normalized result
# when it matches the frozen 847-name list below.
STORAGE_SUFFIX = re.compile(r"_[A-Za-z0-9]{7}(?=[._])")


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.media: set[str] = set()
        self.details: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value for key, value in attrs if value is not None}
        for key in ("src", "href"):
            value = values.get(key, "")
            if value.startswith("/media/images/"):
                self.media.add(value)
            elif value.startswith("/enhanced_image/"):
                self.details.add(value)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def frozen_names() -> dict[str, str]:
    with RATING_SUMMARY.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    selected = [row["image_name"].strip() for row in rows if row.get("is_ai") == "True"]
    if len(selected) != 847 or len(set(selected)) != 847:
        raise RuntimeError("FROZEN_IMAGE_LIST_NOT_847_UNIQUE")
    return {name.casefold(): name for name in selected}


class SerialFetcher:
    def __init__(self) -> None:
        self.last_request_end = 0.0
        self.requests: list[dict[str, object]] = []

    def get(self, url: str, timeout: int = 180) -> bytes:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
            raise RuntimeError(f"OUT_OF_SCOPE_URL:{url}")
        wait = MIN_INTERVAL_SECONDS - (time.monotonic() - self.last_request_end)
        if wait > 0:
            time.sleep(wait)
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "MMSA-CH-SIMS-task10-public-data-audit/1.0"},
            method="GET",
        )
        started = time.time()
        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    status = int(response.status)
                    final = urllib.parse.urlparse(response.geturl())
                    if final.scheme != "https" or final.hostname != ALLOWED_HOST:
                        raise RuntimeError(f"REDIRECT_OUT_OF_SCOPE:{response.geturl()}")
                    body = response.read()
                if status != 200:
                    raise RuntimeError(f"HTTP_{status}:{url}")
                self.last_request_end = time.monotonic()
                self.requests.append(
                    {
                        "url": url,
                        "status": status,
                        "bytes": len(body),
                        "sha256": digest_bytes(body),
                        "attempt": attempt,
                        "started_unix": started,
                    }
                )
                return body
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                last_error = error
                self.last_request_end = time.monotonic()
                if attempt == 3:
                    break
                time.sleep(2.0 * attempt)
        raise RuntimeError(f"GET_FAILED:{url}:{last_error}")


def discover(fetcher: SerialFetcher) -> list[dict[str, str]]:
    PAGE_DIR.mkdir(parents=True, exist_ok=True)
    frozen = frozen_names()
    discovered: dict[str, dict[str, str]] = {}
    for page in range(1, 10):
        url = f"{BASE}/images/?page={page}&per_page=100"
        page_path = PAGE_DIR / f"page-{page:03d}.html"
        if page_path.exists() and page_path.stat().st_size > 0:
            body = page_path.read_bytes()
        else:
            body = fetcher.get(url, timeout=60)
            page_path.write_bytes(body)
        parser = AssetParser()
        parser.feed(body.decode("utf-8", errors="replace"))
        expected = 100 if page < 9 else 47
        if len(parser.media) != expected or len(parser.details) != expected:
            raise RuntimeError(
                f"PAGE_COUNT_MISMATCH:page={page}:media={len(parser.media)}:details={len(parser.details)}"
            )
        for relative in sorted(parser.media):
            storage_name = Path(urllib.parse.urlparse(relative).path).name
            candidate_keys = {storage_name.casefold()}
            for match in STORAGE_SUFFIX.finditer(storage_name):
                candidate_keys.add(
                    (storage_name[: match.start()] + storage_name[match.end() :]).casefold()
                )
            canonical_matches = {frozen[key] for key in candidate_keys if key in frozen}
            if len(canonical_matches) != 1:
                raise RuntimeError(f"UNMAPPED_STORAGE_NAME:{storage_name}")
            canonical = canonical_matches.pop()
            if canonical in discovered:
                raise RuntimeError(f"DUPLICATE_CANONICAL_ASSET:{canonical}")
            discovered[canonical] = {
                "canonical_name": canonical,
                "storage_name": storage_name,
                "url": urllib.parse.urljoin(BASE, relative),
            }
    if len(discovered) != 847 or set(discovered) != set(frozen.values()):
        missing = sorted(set(frozen.values()) - set(discovered))
        raise RuntimeError(f"IMAGE_TREE_NOT_CLOSED:count={len(discovered)}:missing={missing[:5]}")
    return [discovered[name] for name in sorted(discovered, key=str.casefold)]


def verify_image_bytes(name: str, body: bytes) -> None:
    suffix = Path(name).suffix.lower()
    valid = (
        suffix in {".jpg", ".jpeg"} and body.startswith(b"\xff\xd8\xff")
    ) or (suffix == ".png" and body.startswith(b"\x89PNG\r\n\x1a\n"))
    if not valid:
        raise RuntimeError(f"INVALID_IMAGE_MAGIC:{name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true")
    args = parser.parse_args()
    fetcher = SerialFetcher()
    assets = discover(fetcher)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    if not args.metadata_only:
        for index, asset in enumerate(assets, start=1):
            destination = IMAGE_DIR / asset["canonical_name"]
            if destination.exists() and destination.stat().st_size > 0:
                body = destination.read_bytes()
                verify_image_bytes(destination.name, body)
                status = "REUSED_VERIFIED_LOCAL"
            else:
                body = fetcher.get(asset["url"])
                verify_image_bytes(destination.name, body)
                destination.write_bytes(body)
                status = "DOWNLOADED_VERIFIED"
            records.append(
                {
                    **asset,
                    "bytes": len(body),
                    "sha256": digest_file(destination),
                    "status": status,
                }
            )
            if index % 50 == 0 or index == len(assets):
                print(f"images_verified={index}/{len(assets)}", flush=True)
    manifest = {
        "schema": "lai-gai-image-download-raw-v1",
        "authorization": "AUTH-00-SECOND-PRIMARY-RESOLUTION-20260714",
        "official_base": BASE,
        "license": "CC BY 4.0 (official Data Card and OSF component license)",
        "request_policy": {
            "method": "GET",
            "anonymous": True,
            "serial": True,
            "minimum_interval_seconds": MIN_INTERVAL_SECONDS,
            "allowed_host": ALLOWED_HOST,
        },
        "discovered_asset_count": len(assets),
        "downloaded_asset_count": len(records),
        "assets": records if records else assets,
        "requests": fetcher.requests,
        "partial_all_images_zip": {
            "status": "INCOMPLETE_NOT_USED",
            "relative_path": "all_images.zip",
            "bytes": (RAW_ROOT / "all_images.zip").stat().st_size
            if (RAW_ROOT / "all_images.zip").exists()
            else 0,
        },
    }
    RAW_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "discovered": len(assets),
                "downloaded": len(records),
                "requests": len(fetcher.requests),
                "raw_manifest": str(RAW_MANIFEST.relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
