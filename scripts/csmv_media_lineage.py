"""Deterministic, read-only CSMV media lineage helpers.

The official workbook is an explicit mapping from the dataset-internal ``ID``
to a TikTok URL.  The URL path ID is a source-platform identifier; it is not an
equality constraint on the internal ``video_file_id``.
"""

from __future__ import annotations

import hashlib
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


EXPECTED_HEADER = ["No.", "ID", "URL"]
EXPECTED_HOST = "www.tiktok.com"


def stable_id(namespace: str, value: str) -> str:
    return hashlib.sha256((namespace + "|" + value).encode("utf-8")).hexdigest()


def read_ooxml_rows(
    path: Path, worksheet: str = "xl/worksheets/sheet1.xml"
) -> list[list[str]]:
    """Read cell text without loading the upstream workbook's malformed styles."""

    with zipfile.ZipFile(path) as archive:
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        namespace = shared_root.tag.split("}", 1)[0] + "}"
        shared = [
            "".join(node.text or "" for node in item.iter(namespace + "t"))
            for item in shared_root.findall(namespace + "si")
        ]
        rows: list[list[str]] = []
        with archive.open(worksheet) as stream:
            for _, element in ET.iterparse(stream, events=("end",)):
                if element.tag != namespace + "row":
                    continue
                values: list[str] = []
                for cell in element.findall(namespace + "c"):
                    value_node = cell.find(namespace + "v")
                    value = "" if value_node is None else (value_node.text or "")
                    if cell.attrib.get("t") == "s" and value:
                        value = shared[int(value)]
                    values.append(value.strip())
                rows.append(values)
                element.clear()
    return rows


def load_mapping(path: Path) -> list[dict]:
    rows = read_ooxml_rows(path)
    if not rows or rows[0] != EXPECTED_HEADER:
        raise ValueError("CSMV raw-link workbook has an unexpected header")
    if any(len(row) != 3 for row in rows[1:]):
        raise ValueError("CSMV raw-link workbook has an unexpected row width")

    result = []
    for row_number, (_, internal_id, source_url) in enumerate(rows[1:], 2):
        parsed = urlparse(source_url)
        source_platform_id = next(
            (part for part in reversed(parsed.path.split("/")) if part), ""
        )
        result.append(
            {
                "row_number": row_number,
                "internal_video_id": internal_id,
                "source_platform_video_id": source_platform_id,
                "source_host": parsed.netloc.lower(),
                "source_url": source_url,
                "source_url_sha256": hashlib.sha256(
                    source_url.encode("utf-8")
                ).hexdigest(),
                "source_group_id": stable_id(
                    "csmv-source-platform-video-v1", source_platform_id
                ),
            }
        )
    return result


def summarize_mapping(rows: list[dict], official_ids: set[str]) -> dict:
    internal_ids = [row["internal_video_id"] for row in rows]
    platform_ids = [row["source_platform_video_id"] for row in rows]
    urls = [row["source_url"] for row in rows]
    family_counts = Counter(platform_ids)
    hosts = Counter(row["source_host"] for row in rows)
    valid_urls = sum(
        urlparse(url).scheme == "https" and bool(urlparse(url).netloc)
        for url in urls
    )
    mapping_valid = (
        len(rows) == 8210
        and len(set(internal_ids)) == len(internal_ids)
        and not any(not value for value in internal_ids)
        and not any(not value for value in platform_ids)
        and not any(not value for value in urls)
        and valid_urls == len(rows)
        and set(hosts) == {EXPECTED_HOST}
        and set(internal_ids) == official_ids
    )
    return {
        "row_count": len(rows),
        "unique_internal_video_ids": len(set(internal_ids)),
        "unique_source_platform_video_ids": len(family_counts),
        "source_family_duplicate_groups": sum(
            count > 1 for count in family_counts.values()
        ),
        "source_family_duplicate_rows": sum(
            count for count in family_counts.values() if count > 1
        ),
        "duplicate_url_rows_excess": len(urls) - len(set(urls)),
        "duplicate_source_platform_id_rows_excess": len(platform_ids)
        - len(set(platform_ids)),
        "internal_id_differs_from_platform_id": sum(
            internal_id != platform_id
            for internal_id, platform_id in zip(internal_ids, platform_ids)
        ),
        "internal_ids_missing_from_official": len(set(internal_ids) - official_ids),
        "official_ids_missing_from_mapping": len(official_ids - set(internal_ids)),
        "https_row_count": valid_urls,
        "hosts": dict(sorted(hosts.items())),
        "mapping_key_coverage_valid": set(internal_ids) == official_ids,
        "mapping_semantics": "INTERNAL_VIDEO_ID_TO_SOURCE_PLATFORM_URL",
        "internal_platform_id_equality_required": False,
        "mapping_valid": mapping_valid,
        "source_family_grouped_split_required": any(
            count > 1 for count in family_counts.values()
        ),
    }
