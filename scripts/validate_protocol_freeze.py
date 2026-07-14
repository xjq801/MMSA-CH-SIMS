"""Validate the frozen M1 construct, protocol, lineage and threat-model bundle."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = {
    "legacy-asset-lineage.md": ["2787", "2815", "221", "目标评论", "随机"],
    "legacy-experiment-classification.md": ["可复用代码", "历史基线", "仅探索结果", "禁止进入新论文证据"],
    "research-question-v1.md": ["public-induced audience affect", "说话者情感", "画面群体情绪", "第三章传播链", "FROZEN_v1"],
    "experiment-protocol-v1.md": ["主任务：T0", "可选次任务：T+Δ", "视频或帖子", "标签窗口原则", "二分类兼容任务边界", "LEAKAGE_BLOCKED"],
    "leakage-threat-model.md": ["LT-01", "LT-02", "LT-03", "LT-04", "LT-05", "LT-06", "LEAKAGE_BLOCKED"],
}


def validate_protocol_freeze():
    missing_files = []
    missing_terms = []
    for relative, terms in CONTRACT.items():
        path = ROOT / relative
        if not path.is_file():
            missing_files.append(relative)
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                missing_terms.append({"file": relative, "term": term})
    return {
        "passed": not missing_files and not missing_terms,
        "files": len(CONTRACT),
        "missing_files": missing_files,
        "missing_terms": missing_terms,
    }


def main() -> int:
    result = validate_protocol_freeze()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
