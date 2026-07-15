"""Rebuild the tracked LAI-GAI metadata manifest from an existing raw API run.

This script performs no network operations. It verifies each stored response
against the per-request SHA-256 before projecting only authorized metadata.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

import audit_lai_gai_osf_api_metadata as contract


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw" / "lai-gai" / "osf-api-metadata"
MANIFEST = ROOT / "data" / "manifests" / "lai-gai-osf-api-metadata-v1.manifest.json"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_run(run_name: str):
    raw_dir = RAW_ROOT / run_name
    if not raw_dir.is_dir():
        raise RuntimeError("raw run not found: {}".format(run_name))
    records = []
    for meta_path in sorted(raw_dir.glob("*-meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        request = meta.get("request") or {}
        sequence = request.get("sequence")
        if not isinstance(sequence, int):
            raise RuntimeError("invalid request sequence in {}".format(meta_path.name))
        response_path = raw_dir / "{:03d}-response.json".format(sequence)
        body = response_path.read_bytes() if response_path.is_file() else b""
        if len(body) != request.get("response_bytes"):
            raise RuntimeError("response byte mismatch for sequence {}".format(sequence))
        expected_hash = request.get("response_sha256")
        actual_hash = sha256_bytes(body) if body else None
        if actual_hash != expected_hash:
            raise RuntimeError("response hash mismatch for sequence {}".format(sequence))
        document = json.loads(body.decode("utf-8")) if body else None
        records.append((request, document))
    if not records:
        raise RuntimeError("raw run has no request records")
    return raw_dir, records


def provider_from_url(url: str):
    segments = [segment for segment in urlparse(url).path.split("/") if segment]
    if "files" in segments:
        index = segments.index("files")
        if index + 1 < len(segments):
            candidate = segments[index + 1]
            if candidate not in {""} and len(candidate) <= 200:
                return candidate
    return None


def project(run_name: str) -> dict:
    raw_dir, raw_records = load_run(run_name)
    nodes: Dict[str, dict] = {
        node: {
            "node_id": node,
            "node_access": "NOT_REQUESTED",
            "public": None,
            "date_modified": None,
            "license": {"name": None, "url": None, "status": "UNKNOWN"},
            "providers": [],
            "files": [],
            "branch_stops": [],
        }
        for node in contract.ALLOWED_NODES
    }
    requests: List[dict] = []
    total_bytes = 0

    for raw_request, document in raw_records:
        node_id = raw_request.get("node_id")
        if node_id not in nodes:
            raise RuntimeError("request contains unauthorized node")
        allowed, reason = contract.validate_url(
            raw_request.get("request_url", ""), raw_request.get("parent_request") is not None
        )
        if not allowed:
            raise RuntimeError("stored request violates URL contract: {}".format(reason))
        request = {
            "sequence": raw_request.get("sequence"),
            "node_id": node_id,
            "method": "GET",
            "request_url": raw_request.get("request_url"),
            "request_kind": raw_request.get("request_kind"),
            "parent_request": raw_request.get("parent_request"),
            "requested_at_utc": raw_request.get("requested_at_utc"),
            "http_status": raw_request.get("http_status"),
            "content_type": raw_request.get("content_type"),
            "response_bytes": raw_request.get("response_bytes"),
            "response_sha256": raw_request.get("response_sha256"),
            "outcome": raw_request.get("outcome"),
        }
        requests.append(request)
        total_bytes += int(request["response_bytes"] or 0)
        node = nodes[node_id]
        if request["http_status"] != 200 or not isinstance(document, dict):
            node["branch_stops"].append(request["outcome"])
            continue

        data = document.get("data")
        entries = data if isinstance(data, list) else [data]
        entries = [entry for entry in entries if isinstance(entry, dict)]
        kind = request["request_kind"]

        if kind == "node" and entries:
            attributes = entries[0].get("attributes") or {}
            node["node_access"] = "HTTP_200_JSON"
            node["public"] = attributes.get("public") if isinstance(attributes.get("public"), bool) else None
            node["date_modified"] = (
                attributes.get("date_modified") if isinstance(attributes.get("date_modified"), str) else None
            )
        elif kind == "license" and entries:
            attributes = entries[0].get("attributes") or {}
            name = attributes.get("name")
            locator = attributes.get("url")
            if not isinstance(locator, str) or urlparse(locator).scheme not in {"http", "https"}:
                locator = None
            node["license"] = {
                "name": name if isinstance(name, str) else None,
                "url": locator,
                "status": "PRESENT" if isinstance(name, str) and name else "UNKNOWN",
            }
        elif kind == "providers":
            for entry in entries:
                attributes = entry.get("attributes") or {}
                provider = attributes.get("name") or attributes.get("provider")
                if isinstance(provider, str) and provider not in node["providers"]:
                    node["providers"].append(provider[:200])
        elif kind == "file_list":
            request_provider = provider_from_url(request["request_url"])
            for entry in entries:
                attributes = entry.get("attributes") or {}
                file_kind = attributes.get("kind")
                size = attributes.get("size")
                provider = attributes.get("provider") or request_provider
                file_record = {
                    "provider": provider[:200] if isinstance(provider, str) else None,
                    "relative_path": contract.safe_relative_path(attributes),
                    "kind": file_kind if file_kind in {"file", "folder"} else "UNKNOWN",
                    "size_bytes": size if isinstance(size, int) and size >= 0 else None,
                    "date_modified": attributes.get("date_modified")
                    if isinstance(attributes.get("date_modified"), str) else None,
                    "checksum": contract.safe_checksum(attributes),
                }
                if file_record not in node["files"]:
                    node["files"].append(file_record)

    for node in nodes.values():
        node["providers"].sort()
        node["files"].sort(key=lambda item: (
            item.get("provider") or "", item.get("relative_path") or "", item.get("kind") or ""
        ))
        actual_files = [item for item in node["files"] if item["kind"] == "file"]
        folders = [item for item in node["files"] if item["kind"] == "folder"]
        known_sizes = [item["size_bytes"] for item in actual_files if item["size_bytes"] is not None]
        checksummed = [item for item in actual_files if item["checksum"]]
        node["summary"] = {
            "file_count": len(actual_files),
            "folder_count": len(folders),
            "known_size_file_count": len(known_sizes),
            "unknown_size_file_count": len(actual_files) - len(known_sizes),
            "total_known_size_bytes": sum(known_sizes),
            "checksum_file_count": len(checksummed),
        }

    projected_nodes = [nodes[node] for node in contract.ALLOWED_NODES]
    ordered_requests = sorted(requests, key=lambda item: item["sequence"])
    intervals = [
        (parse_time(current["requested_at_utc"]) - parse_time(previous["requested_at_utc"])).total_seconds()
        for previous, current in zip(ordered_requests, ordered_requests[1:])
    ]
    minimum_interval = min(intervals) if intervals else None
    rate_interval_compliant = minimum_interval is not None and minimum_interval >= contract.MIN_INTERVAL_SECONDS
    license_complete = all(node["license"]["status"] == "PRESENT" for node in projected_nodes)
    tree_complete = all(
        node["node_access"] == "HTTP_200_JSON"
        and node["summary"]["file_count"] > 0
        and node["summary"]["unknown_size_file_count"] == 0
        for node in projected_nodes
    )
    checksum_complete = all(
        node["summary"]["file_count"] > 0
        and node["summary"]["checksum_file_count"] == node["summary"]["file_count"]
        for node in projected_nodes
    )
    no_branch_stops = all(not node["branch_stops"] for node in projected_nodes)
    public_complete = all(node["public"] is True for node in projected_nodes)
    ready = (
        license_complete and tree_complete and checksum_complete and no_branch_stops
        and public_complete and rate_interval_compliant
    )
    if ready:
        verdict = "FIT_FOR_NEXT_REVIEW"
    elif not rate_interval_compliant and not tree_complete:
        verdict = "NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE"
    elif not rate_interval_compliant:
        verdict = "NO_GO_PENDING_RATE_INTERVAL_COMPLIANCE_REVIEW"
    else:
        verdict = "NO_GO_PENDING_ASSET_METADATA"

    return {
        "schema": "lai-gai-osf-api-metadata-v1",
        "audit_date": "2026-07-14",
        "authorization": contract.AUTHORIZATION,
        "audit_mode": "ANONYMOUS_BOUNDED_OSF_METADATA_API_GET_ONLY",
        "limits": {
            "allowed_host": contract.ALLOWED_HOST,
            "allowed_nodes": list(contract.ALLOWED_NODES),
            "max_requests": contract.MAX_REQUESTS,
            "max_response_bytes": contract.MAX_BYTES,
            "min_interval_seconds": contract.MIN_INTERVAL_SECONDS,
        },
        "usage": {
            "request_count": len(requests),
            "response_bytes": total_bytes,
            "global_stop": None,
            "raw_run_relative_path": str(raw_dir.relative_to(ROOT)).replace("\\", "/"),
        },
        "requests": requests,
        "rejected_links": [],
        "nodes": projected_nodes,
        "admission_checks": {
            "all_nodes_public": public_complete,
            "component_license_complete": license_complete,
            "file_tree_and_size_complete": tree_complete,
            "public_checksum_fixity_complete": checksum_complete,
            "no_branch_stops": no_branch_stops,
            "rate_interval_compliant": rate_interval_compliant,
            "minimum_observed_interval_seconds": minimum_interval,
        },
        "verdict": verdict,
        "downloaded_or_previewed_assets": False,
        "followed_download_content_render_html_upload": False,
        "used_head_or_range": False,
        "used_login_cookie_token_proxy_or_mirror": False,
        "read_score_contents_or_built_mapping_split": False,
        "second_primary_frozen": False,
        "download_authorized": False,
        "g1_status": "BLOCKED_SECOND_PRIMARY_NOT_FROZEN",
        "g2_status": "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN",
        "formal_split": False,
        "task20_or_m3_allowed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    args = parser.parse_args()
    manifest = project(args.run)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "request_count": manifest["usage"]["request_count"],
        "response_bytes": manifest["usage"]["response_bytes"],
        "verdict": manifest["verdict"],
        "admission_checks": manifest["admission_checks"],
        "node_summaries": {
            node["node_id"]: {
                "license": node["license"]["name"],
                "public": node["public"],
                "date_modified": node["date_modified"],
                "providers": node["providers"],
                "summary": node["summary"],
            }
            for node in manifest["nodes"]
        },
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
