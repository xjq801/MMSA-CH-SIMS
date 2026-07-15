"""Bounded, anonymous OSF metadata audit for three authorized LAI-GAI nodes.

This collector is deliberately fail-closed. It never follows redirects or asset
links, disables proxies, performs sequential GET requests, and stores raw JSON
only beneath a Git-ignored data/raw directory.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "data" / "raw" / "lai-gai" / "osf-api-metadata"
MANIFEST = ROOT / "data" / "manifests" / "lai-gai-osf-api-metadata-v1.manifest.json"
AUTHORIZATION = "AUTH-00-LAI-GAI-OSF-API-META-RO-20260714"
ALLOWED_NODES = ("V8DKM", "8P572", "K8XVH")
ALLOWED_HOST = "api.osf.io"
MAX_REQUESTS = 100
MAX_BYTES = 5 * 1024 * 1024
MIN_INTERVAL_SECONDS = 1.0
FORBIDDEN_LINK_WORDS = {"download", "content", "render", "html", "upload"}
STOP_STATUSES = {401, 403, 404, 429}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def ensure_raw_ignored() -> None:
    sentinel = RAW_ROOT / "git-ignore-preflight.json"
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", str(sentinel.relative_to(ROOT))],
        cwd=str(ROOT),
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("raw API output path is not covered by Git ignore policy")


def validate_url(url: str, discovered: bool) -> Tuple[bool, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != ALLOWED_HOST:
        return False, "REJECT_NON_WHITELIST_SCHEME_OR_HOST"
    if parsed.username or parsed.password or parsed.fragment:
        return False, "REJECT_USERINFO_OR_FRAGMENT"
    segments = {segment.lower() for segment in parsed.path.split("/") if segment}
    if segments & FORBIDDEN_LINK_WORDS:
        return False, "REJECT_FORBIDDEN_LINK_KIND"
    if parsed.query:
        if not discovered:
            return False, "REJECT_MANUAL_QUERY"
        query_keys = {key.lower() for key in parse_qs(parsed.query, keep_blank_values=True)}
        if any(any(word in key for word in FORBIDDEN_LINK_WORDS) for key in query_keys):
            return False, "REJECT_FORBIDDEN_QUERY"
    if not parsed.path.startswith("/v2/"):
        return False, "REJECT_NON_V2_PATH"
    return True, "ALLOWED"


def related_href(value) -> Optional[str]:
    if not isinstance(value, dict):
        return None
    if isinstance(value.get("href"), str):
        return value["href"]
    related = value.get("related")
    if isinstance(related, dict) and isinstance(related.get("href"), str):
        return related["href"]
    if isinstance(related, str):
        return related
    return None


def next_href(document: dict) -> Optional[str]:
    links = document.get("links")
    if not isinstance(links, dict):
        return None
    nxt = links.get("next")
    if isinstance(nxt, str):
        return nxt
    if isinstance(nxt, dict) and isinstance(nxt.get("href"), str):
        return nxt["href"]
    return None


def safe_checksum(attributes: dict) -> dict:
    extra = attributes.get("extra")
    if not isinstance(extra, dict):
        return {}
    hashes = extra.get("hashes")
    if not isinstance(hashes, dict):
        return {}
    allowed = {}
    for algorithm in ("sha256", "md5"):
        value = hashes.get(algorithm)
        if isinstance(value, str) and value and len(value) <= 128:
            allowed[algorithm] = value
    return allowed


def safe_relative_path(attributes: dict) -> Optional[str]:
    value = attributes.get("materialized_path") or attributes.get("name")
    if not isinstance(value, str):
        return None
    value = value.replace("\\", "/")
    if "@" in value or ".." in value.split("/"):
        return "REDACTED_UNSAFE_PATH"
    return value[:1000]


def main() -> int:
    ensure_raw_ignored()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_dir = RAW_ROOT / run_id
    raw_dir.mkdir(parents=True, exist_ok=False)

    opener = build_opener(ProxyHandler({}), NoRedirect())
    queue: List[dict] = []
    for node_id in ALLOWED_NODES:
        node_lower = node_id.lower()
        queue.append({
            "node_id": node_id,
            "url": "https://api.osf.io/v2/nodes/{}/".format(node_lower),
            "kind": "node",
            "discovered": False,
            "parent_request": None,
        })
        queue.append({
            "node_id": node_id,
            "url": "https://api.osf.io/v2/nodes/{}/files/".format(node_lower),
            "kind": "providers",
            "discovered": False,
            "parent_request": None,
        })

    seen: Set[Tuple[str, str]] = set()
    requests_log: List[dict] = []
    rejected_links: List[dict] = []
    node_records: Dict[str, dict] = {
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
        for node in ALLOWED_NODES
    }
    total_bytes = 0
    last_request_at: Optional[float] = None
    request_sequence = 0
    global_stop = None

    while queue:
        if request_sequence >= MAX_REQUESTS:
            global_stop = "STOP_REQUEST_LIMIT"
            break
        if total_bytes >= MAX_BYTES:
            global_stop = "STOP_BODY_LIMIT"
            break

        item = queue.pop(0)
        key = (item["node_id"], item["url"])
        if key in seen:
            continue
        seen.add(key)
        allowed, reason = validate_url(item["url"], item["discovered"])
        if not allowed:
            rejected_links.append({
                "node_id": item["node_id"],
                "link_kind": item["kind"],
                "reason": reason,
            })
            node_records[item["node_id"]]["branch_stops"].append(reason)
            continue

        if last_request_at is not None:
            elapsed = time.monotonic() - last_request_at
            if elapsed < MIN_INTERVAL_SECONDS + 0.1:
                time.sleep(MIN_INTERVAL_SECONDS + 0.1 - elapsed)
        request_sequence += 1
        requested_at = utc_now()
        started = time.monotonic()
        request = Request(
            item["url"],
            method="GET",
            headers={
                "Accept": "application/vnd.api+json, application/json",
                "User-Agent": "MMSA-CH-SIMS-bounded-metadata-audit/1.0",
            },
        )
        status = None
        content_type = None
        body = b""
        outcome = "UNKNOWN"
        response_headers = {}
        try:
            with opener.open(request, timeout=30) as response:
                last_request_at = started
                status = int(response.status)
                content_type = response.headers.get("Content-Type")
                response_headers = {
                    "content_type": content_type,
                    "content_length": response.headers.get("Content-Length"),
                }
                remaining = MAX_BYTES - total_bytes
                declared = response.headers.get("Content-Length")
                if declared and declared.isdigit() and int(declared) > remaining:
                    outcome = "STOP_SIZE_LIMIT_BEFORE_BODY"
                    global_stop = outcome
                else:
                    chunks = []
                    body_complete = False
                    while remaining > 0:
                        chunk = response.read(min(65536, remaining))
                        if not chunk:
                            body_complete = True
                            break
                        chunks.append(chunk)
                        remaining -= len(chunk)
                    body = b"".join(chunks)
                    total_bytes += len(body)
                    if not body_complete and remaining == 0:
                        outcome = "STOP_BODY_LIMIT_AT_BOUNDARY"
                        global_stop = outcome
                    else:
                        outcome = "HTTP_{}".format(status)
        except HTTPError as error:
            last_request_at = started
            status = int(error.code)
            content_type = error.headers.get("Content-Type") if error.headers else None
            response_headers = {"content_type": content_type, "content_length": None}
            outcome = "HTTP_ERROR_{}".format(status)
        except (URLError, TimeoutError) as error:
            last_request_at = started
            outcome = "NETWORK_ERROR_{}".format(type(error).__name__)

        body_hash = sha256_bytes(body) if body else None
        request_record = {
            "sequence": request_sequence,
            "node_id": item["node_id"],
            "request_url": item["url"],
            "request_kind": item["kind"],
            "parent_request": item["parent_request"],
            "requested_at_utc": requested_at,
            "http_status": status,
            "content_type": content_type,
            "response_bytes": len(body),
            "response_sha256": body_hash,
            "outcome": outcome,
        }
        requests_log.append(request_record)

        raw_meta = {
            "request": request_record,
            "response_headers": response_headers,
        }
        (raw_dir / "{:03d}-meta.json".format(request_sequence)).write_text(
            json.dumps(raw_meta, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
        )
        if body:
            (raw_dir / "{:03d}-response.json".format(request_sequence)).write_bytes(body)

        node = node_records[item["node_id"]]
        if status in STOP_STATUSES or (status is not None and status >= 500):
            node["branch_stops"].append(outcome)
            continue
        if status != 200 or not body or global_stop:
            if outcome not in node["branch_stops"]:
                node["branch_stops"].append(outcome)
            if global_stop:
                break
            continue
        if not content_type or "json" not in content_type.lower():
            node["branch_stops"].append("NON_JSON_RESPONSE")
            continue
        try:
            document = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            node["branch_stops"].append("INVALID_JSON_RESPONSE")
            continue

        data = document.get("data")
        entries = data if isinstance(data, list) else [data]
        entries = [entry for entry in entries if isinstance(entry, dict)]

        if item["kind"] == "node" and entries:
            attributes = entries[0].get("attributes") or {}
            node["node_access"] = "HTTP_200_JSON"
            node["public"] = attributes.get("public") if isinstance(attributes.get("public"), bool) else None
            modified = attributes.get("date_modified")
            node["date_modified"] = modified if isinstance(modified, str) else None
            relationships = entries[0].get("relationships") or {}
            license_relation = relationships.get("license") if isinstance(relationships, dict) else None
            href = related_href((license_relation or {}).get("links") if isinstance(license_relation, dict) else None)
            if href:
                queue.append({
                    "node_id": item["node_id"], "url": href, "kind": "license",
                    "discovered": True, "parent_request": request_sequence,
                })

        elif item["kind"] == "license" and entries:
            attributes = entries[0].get("attributes") or {}
            name = attributes.get("name")
            url = attributes.get("url")
            if not isinstance(url, str) or urlparse(url).scheme not in {"https", "http"}:
                url = None
            node["license"] = {
                "name": name if isinstance(name, str) else None,
                "url": url,
                "status": "PRESENT" if isinstance(name, str) and name else "UNKNOWN",
            }

        elif item["kind"] == "providers":
            for entry in entries:
                attributes = entry.get("attributes") or {}
                provider = attributes.get("name") or attributes.get("provider")
                if isinstance(provider, str) and provider not in node["providers"]:
                    node["providers"].append(provider[:200])
                relationships = entry.get("relationships") or {}
                files_relation = relationships.get("files") if isinstance(relationships, dict) else None
                href = related_href((files_relation or {}).get("links") if isinstance(files_relation, dict) else None)
                if href:
                    queue.append({
                        "node_id": item["node_id"], "url": href, "kind": "file_list",
                        "discovered": True, "parent_request": request_sequence,
                    })

        elif item["kind"] == "file_list":
            for entry in entries:
                attributes = entry.get("attributes") or {}
                kind = attributes.get("kind")
                size = attributes.get("size")
                record = {
                    "relative_path": safe_relative_path(attributes),
                    "kind": kind if kind in {"file", "folder"} else "UNKNOWN",
                    "size_bytes": size if isinstance(size, int) and size >= 0 else None,
                    "date_modified": attributes.get("date_modified")
                    if isinstance(attributes.get("date_modified"), str) else None,
                    "checksum": safe_checksum(attributes),
                }
                if record not in node["files"]:
                    node["files"].append(record)
                if record["kind"] == "folder":
                    relationships = entry.get("relationships") or {}
                    files_relation = relationships.get("files") if isinstance(relationships, dict) else None
                    href = related_href((files_relation or {}).get("links") if isinstance(files_relation, dict) else None)
                    if href:
                        queue.append({
                            "node_id": item["node_id"], "url": href, "kind": "file_list",
                            "discovered": True, "parent_request": request_sequence,
                        })

        nxt = next_href(document)
        if nxt:
            queue.append({
                "node_id": item["node_id"], "url": nxt, "kind": item["kind"],
                "discovered": True, "parent_request": request_sequence,
            })

    for node in node_records.values():
        node["providers"].sort()
        node["files"].sort(key=lambda item: (item.get("relative_path") or "", item.get("kind") or ""))
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

    all_nodes = list(node_records.values())
    license_complete = all(node["license"]["status"] == "PRESENT" for node in all_nodes)
    tree_complete = all(
        node["node_access"] == "HTTP_200_JSON"
        and node["summary"]["file_count"] > 0
        and node["summary"]["unknown_size_file_count"] == 0
        for node in all_nodes
    )
    honest_fixity = all(
        node["summary"]["file_count"] > 0
        and node["summary"]["checksum_file_count"] == node["summary"]["file_count"]
        for node in all_nodes
    )
    no_branch_stops = all(not node["branch_stops"] for node in all_nodes)
    verdict = (
        "FIT_FOR_NEXT_REVIEW"
        if license_complete and tree_complete and honest_fixity and no_branch_stops and not global_stop
        else "NO_GO_PENDING_ASSET_METADATA"
    )

    manifest = {
        "schema": "lai-gai-osf-api-metadata-v1",
        "audit_date": "2026-07-14",
        "authorization": AUTHORIZATION,
        "audit_mode": "ANONYMOUS_BOUNDED_OSF_METADATA_API_GET_ONLY",
        "limits": {
            "allowed_host": ALLOWED_HOST,
            "allowed_nodes": list(ALLOWED_NODES),
            "max_requests": MAX_REQUESTS,
            "max_response_bytes": MAX_BYTES,
            "min_interval_seconds": MIN_INTERVAL_SECONDS,
        },
        "usage": {
            "request_count": request_sequence,
            "response_bytes": total_bytes,
            "global_stop": global_stop,
            "raw_run_relative_path": str(raw_dir.relative_to(ROOT)).replace("\\", "/"),
        },
        "requests": requests_log,
        "rejected_links": rejected_links,
        "nodes": all_nodes,
        "admission_checks": {
            "component_license_complete": license_complete,
            "file_tree_and_size_complete": tree_complete,
            "public_checksum_fixity_complete": honest_fixity,
            "no_branch_stops": no_branch_stops,
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
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (raw_dir / "requests.json").write_text(
        json.dumps(requests_log, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "raw_run": str(raw_dir.relative_to(ROOT)),
        "request_count": request_sequence,
        "response_bytes": total_bytes,
        "verdict": verdict,
        "global_stop": global_stop,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
