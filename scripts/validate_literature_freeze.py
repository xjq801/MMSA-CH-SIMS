"""Validate the M1 step 19-23 literature, name, protocol and baseline freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "references" / "search" / "step19-23" / "search-protocol.json"
DOCUMENT_CONTRACT = {
    "LITERATURE_SEARCH_REPORT.md": [
        "SCOPING_COMPLETE_v2",
        "评论特权监督",
        "公众诱发情绪分布",
        "检索增强情绪预测",
        "可靠性拒绝与缺失模态",
        "Video2Reaction",
        "DIRECT_NEAR_COLLISION",
        "不声称穷尽召回",
    ],
    "CONTRIBUTION_PRIOR_ART_MATRIX.md": [
        "最相近前作",
        "必须对比实验",
        "NEmo+",
        "M2PKD",
        "RAMER",
        "SelectiveNet",
        "Video2Reaction",
        "首次video-to-reaction-distribution",
    ],
    "CARM_NAME_AUDIT.md": ["NAME_BLOCKED", "Constraint-Aware Retrieval Module", "CarM"],
    "RESEARCH_PROTOCOL_FREEZE_AUDIT.md": [
        "FROZEN_v1_CONFIRMED",
        "C1—C3",
        "H1—H4",
        "Jensen–Shannon divergence",
        "LEAKAGE_BLOCKED",
    ],
    "BASELINE_CANDIDATES.md": [
        "代码可得性",
        "代码许可",
        "预计成本",
        "G1仍因第二人工多模态公开主集未冻结",
    ],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _protocol_content_hash(spec: dict) -> str:
    content = {key: value for key, value in spec.items() if key != "protocol_lock"}
    payload = json.dumps(
        content, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def validate_literature_freeze() -> dict:
    errors: list[str] = []
    for relative, terms in DOCUMENT_CONTRACT.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing document: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                errors.append(f"{relative}: missing token {term}")

    if not PROTOCOL.is_file():
        errors.append("missing search protocol")
        return {"passed": False, "errors": errors}

    spec = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if spec.get("schema") != "light.search_protocol.v1":
        errors.append("search protocol schema drift")
    if spec.get("review_type") != "SCOPING" or spec.get("protocol_state") != "FROZEN":
        errors.append("search protocol scope/state drift")
    if spec.get("coverage_claim") != "SCOPING_COVERAGE":
        errors.append("search protocol overclaims coverage")
    if spec.get("protocol_lock", {}).get("protocol_sha256") != _protocol_content_hash(spec):
        errors.append("search protocol lock mismatch")
    if len(spec.get("query_ledger", [])) != 4:
        errors.append("search protocol must retain four independent queries")

    source_total = 0
    for source in spec.get("sources", []):
        if source.get("status") != "SEARCHED":
            continue
        source_total += source.get("result_count", 0)
        raw_path = ROOT / source.get("raw_locator", "")
        if not raw_path.is_file():
            errors.append(f"missing raw search artifact: {source.get('source_id')}")
            continue
        expected = str(source.get("raw_sha256", ""))
        if expected.startswith("sha256:"):
            expected = expected[len("sha256:") :]
        if _sha256(raw_path) != expected:
            errors.append(f"raw search hash mismatch: {source.get('source_id')}")

    if spec.get("accounting", {}).get("identified") != source_total:
        errors.append("search accounting source total mismatch")
    if spec.get("accounting", {}).get("screened") != 488:
        errors.append("search screened-count drift")

    return {
        "passed": not errors,
        "documents": len(DOCUMENT_CONTRACT),
        "queries": len(spec.get("query_ledger", [])),
        "identified": source_total,
        "errors": errors,
    }


def main() -> int:
    result = validate_literature_freeze()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
