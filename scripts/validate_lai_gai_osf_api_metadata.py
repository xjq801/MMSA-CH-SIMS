"""Validate the bounded LAI-GAI OSF API metadata audit and authority limits."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "manifests" / "lai-gai-osf-api-metadata-v1.manifest.json"
REPORT = ROOT / "M1_LAI_GAI_OSF_API_METADATA_AUDIT_20260714.md"
AUTH = ROOT / "TASK00_LAI_GAI_OSF_API_METADATA_AUTHORIZATION_20260714.md"
REVIEW = ROOT / "TASK00_LAI_GAI_OSF_API_METADATA_REVIEW_20260714.md"
REQUIRED = [
    REPORT,
    MANIFEST,
    AUTH,
    REVIEW,
    ROOT / "scripts" / "audit_lai_gai_osf_api_metadata.py",
    ROOT / "scripts" / "build_lai_gai_osf_api_manifest.py",
]
ALLOWED_NODES = {"V8DKM", "8P572", "K8XVH"}
FORBIDDEN_SEGMENTS = {"download", "content", "render", "html", "upload"}
FORBIDDEN_PERSON_KEYS = {
    "contributors", "contributor", "users", "user", "email", "emails",
    "avatar", "profile_image", "given_name", "family_name", "full_name",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def recursive_keys(value):
    keys = []
    if isinstance(value, dict):
        for key, child in value.items():
            keys.append(str(key).lower())
            keys.extend(recursive_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.extend(recursive_keys(child))
    return keys


def validate_lai_gai_osf_api_metadata() -> dict:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    checks = {"required_files": {"passed": not missing, "missing": missing}}
    if missing:
        return {"schema": "lai-gai-osf-api-metadata-check-v1", "passed": False, "checks": checks}

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    limits = data.get("limits") or {}
    usage = data.get("usage") or {}
    requests = data.get("requests") or []
    nodes = data.get("nodes") or []
    checks["authorization_contract"] = {
        "passed": (
            data.get("authorization") == "AUTH-00-LAI-GAI-OSF-API-META-RO-20260714"
            and data.get("audit_mode") == "ANONYMOUS_BOUNDED_OSF_METADATA_API_GET_ONLY"
            and limits.get("allowed_host") == "api.osf.io"
            and set(limits.get("allowed_nodes") or []) == ALLOWED_NODES
            and limits.get("max_requests") == 100
            and limits.get("max_response_bytes") == 5 * 1024 * 1024
            and float(limits.get("min_interval_seconds")) >= 1.0
        )
    }
    review = data.get("review") or {}
    checks["review_closure"] = {
        "passed": (
            review.get("review_id") == "REVIEW-00-LAI-GAI-OSF-API-20260714"
            and review.get("review_decision") == "ACCEPTED_AS_NONCONFORMING_OBSERVATION_NO_GATE_CREDIT"
            and review.get("authorization_status") == "CLOSED_NONCONFORMING_NO_RERUN_AUTHORIZED"
            and review.get("evidence_class") == "OBSERVED_WITH_PROTOCOL_DEVIATION_NO_GATE_CREDIT"
            and review.get("dataset_status") == "NO_GO_00_REVIEWED_NOT_FROZEN"
        )
    }

    sequences = {item.get("sequence"): item for item in requests}
    request_errors = []
    previous_time = None
    minimum_interval = None
    for item in sorted(requests, key=lambda row: row.get("sequence", 0)):
        parsed = urlparse(item.get("request_url", ""))
        segments = {segment.lower() for segment in parsed.path.split("/") if segment}
        if item.get("method") != "GET":
            request_errors.append([item.get("sequence"), "NON_GET"])
        if parsed.scheme != "https" or parsed.hostname != "api.osf.io":
            request_errors.append([item.get("sequence"), "HOST_OR_SCHEME"])
        if segments & FORBIDDEN_SEGMENTS:
            request_errors.append([item.get("sequence"), "FORBIDDEN_LINK"])
        if item.get("node_id") not in ALLOWED_NODES:
            request_errors.append([item.get("sequence"), "NODE"])
        if item.get("request_kind") not in {"node", "providers", "license", "file_list"}:
            request_errors.append([item.get("sequence"), "RELATION"])
        parent = item.get("parent_request")
        if parent is not None:
            parent_item = sequences.get(parent)
            if not parent_item or parent >= item.get("sequence") or parent_item.get("node_id") != item.get("node_id"):
                request_errors.append([item.get("sequence"), "PARENT_CHAIN"])
        elif item.get("request_kind") not in {"node", "providers"}:
            request_errors.append([item.get("sequence"), "UNDISCOVERED_RELATION"])
        if item.get("http_status") != 200:
            request_errors.append([item.get("sequence"), "HTTP_STATUS"])
        if int(item.get("response_bytes") or 0) <= 0 or not SHA256.match(item.get("response_sha256") or ""):
            request_errors.append([item.get("sequence"), "RESPONSE_EVIDENCE"])
        current_time = parse_time(item.get("requested_at_utc"))
        if previous_time is not None:
            interval = (current_time - previous_time).total_seconds()
            minimum_interval = interval if minimum_interval is None else min(minimum_interval, interval)
            if interval < 1.0:
                request_errors.append([item.get("sequence"), "RATE_INTERVAL"])
        previous_time = current_time
    checks["request_boundary"] = {
        "passed": not request_errors,
        "errors": request_errors,
        "minimum_interval_seconds": minimum_interval,
    }
    checks["resource_limits"] = {
        "passed": (
            len(requests) == usage.get("request_count") == 26
            and sum(int(item.get("response_bytes") or 0) for item in requests) == usage.get("response_bytes")
            and usage.get("request_count") <= limits.get("max_requests")
            and usage.get("response_bytes") <= limits.get("max_response_bytes")
            and usage.get("global_stop") is None
        ),
        "request_count": usage.get("request_count"),
        "response_bytes": usage.get("response_bytes"),
    }

    raw_relative = usage.get("raw_run_relative_path")
    raw_dir = ROOT / raw_relative if isinstance(raw_relative, str) else ROOT / "missing"
    raw_errors = []
    for item in requests:
        sequence = item["sequence"]
        meta_path = raw_dir / "{:03d}-meta.json".format(sequence)
        response_path = raw_dir / "{:03d}-response.json".format(sequence)
        if not meta_path.is_file() or not response_path.is_file():
            raw_errors.append([sequence, "MISSING_RAW_EVIDENCE"])
            continue
        body = response_path.read_bytes()
        if len(body) != item["response_bytes"] or hashlib.sha256(body).hexdigest() != item["response_sha256"]:
            raw_errors.append([sequence, "RAW_HASH_OR_SIZE"])
    ignore_result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", raw_relative or "missing"],
        cwd=str(ROOT), check=False,
    )
    checks["raw_evidence"] = {
        "passed": raw_dir.is_dir() and not raw_errors and ignore_result.returncode == 0,
        "errors": raw_errors,
        "git_ignored": ignore_result.returncode == 0,
    }

    keys = set(recursive_keys(data))
    person_hits = sorted(keys & FORBIDDEN_PERSON_KEYS)
    allowed_file_keys = {"provider", "relative_path", "kind", "size_bytes", "date_modified", "checksum"}
    file_key_errors = []
    email_path_hits = []
    for node in nodes:
        for item in node.get("files") or []:
            if set(item) - allowed_file_keys:
                file_key_errors.append({"node": node.get("node_id"), "keys": sorted(set(item) - allowed_file_keys)})
            if "@" in str(item.get("relative_path") or ""):
                email_path_hits.append([node.get("node_id"), item.get("relative_path")])
    checks["tracked_redaction"] = {
        "passed": not person_hits and not file_key_errors and not email_path_hits,
        "person_key_hits": person_hits,
        "file_key_errors": file_key_errors,
        "email_path_hits": email_path_hits,
    }

    by_node = {node.get("node_id"): node for node in nodes}
    expected = {
        "V8DKM": (9, 22108737, 9),
        "8P572": (137, 1122196956, 137),
        "K8XVH": (0, 0, 0),
    }
    matrix_errors = []
    for node_id, (file_count, total_size, checksum_count) in expected.items():
        node = by_node.get(node_id) or {}
        summary = node.get("summary") or {}
        if node.get("public") is not True or node.get("license", {}).get("status") != "PRESENT":
            matrix_errors.append([node_id, "PUBLIC_OR_LICENSE"])
        if (
            summary.get("file_count") != file_count
            or summary.get("total_known_size_bytes") != total_size
            or summary.get("checksum_file_count") != checksum_count
        ):
            matrix_errors.append([node_id, "SUMMARY"])
    checks["three_node_matrix"] = {
        "passed": set(by_node) == ALLOWED_NODES and not matrix_errors,
        "errors": matrix_errors,
    }
    negative_flags = [
        "downloaded_or_previewed_assets",
        "followed_download_content_render_html_upload",
        "used_head_or_range",
        "used_login_cookie_token_proxy_or_mirror",
        "read_score_contents_or_built_mapping_split",
        "second_primary_frozen",
        "download_authorized",
        "formal_split",
        "task20_or_m3_allowed",
    ]
    checks["honest_gate_state"] = {
        "passed": (
            all(data.get(flag) is False for flag in negative_flags)
            and data.get("verdict") == "NO_GO_PENDING_RATE_INTERVAL_AND_IMAGE_COMPONENT_FILE_TREE"
            and data.get("g1_status") == "BLOCKED_SECOND_PRIMARY_NOT_FROZEN"
            and data.get("g2_status") == "NOT_ELIGIBLE_G1_BLOCKED_AND_SEMANTIC_AUDITS_OPEN"
            and data.get("admission_checks", {}).get("file_tree_and_size_complete") is False
            and data.get("admission_checks", {}).get("public_checksum_fixity_complete") is False
            and data.get("admission_checks", {}).get("rate_interval_compliant") is False
        ),
        "verdict": data.get("verdict"),
        "g1_status": data.get("g1_status"),
        "g2_status": data.get("g2_status"),
    }
    passed = all(check["passed"] for check in checks.values())
    return {"schema": "lai-gai-osf-api-metadata-check-v1", "passed": passed, "checks": checks}


def main() -> int:
    result = validate_lai_gai_osf_api_metadata()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
