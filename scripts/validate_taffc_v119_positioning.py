from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md": [
        "版本：v1.19",
        "Reliable content-to-audience affect distribution forecasting under distribution shift and unavailable target responses.",
        "### 0.9 Claim blacklist与构念红线（v1.19）",
        "### 0.10 T-AFFC前三类预演拒稿与反驳证据（v1.19）",
        "### 0.11 仓库SSOT与外部Word关系（v1.19）",
        "WORKSHOP_APPEARANCE_CONFIRMED_ARCHIVAL_STATUS_UNRESOLVED",
        "AUTHOR_REPORTED_ECCV_2026_ACCEPTANCE_PENDING_OFFICIAL_PROCEEDINGS",
        "movie/group、topic/hashtag、publisher/source、time、platform held-out",
    ],
    "TAFFC_CLAIM_BLACKLIST_20260724.md": [
        "BL-01",
        "BL-08",
        "closest/direct prior",
        "评论者公开表达的诱发反应分布",
    ],
    "LITERATURE_SEARCH_REPORT.md": [
        "SCOPING_COMPLETE_v3",
        "closest/direct prior",
    ],
    "CONTRIBUTION_PRIOR_ART_MATRIX.md": [
        "FROZEN_v3",
        "去memory",
        "去router",
        "去rejection",
    ],
    "CLAIM_EVIDENCE_MATRIX.md": [
        "版本：v1.1",
        "2026-07-24 Claim blacklist与构念边界",
    ],
    "WORD_MASTER_BACKFILL_PLAN_20260724.md": [
        "历史派生快照",
        "不在旧v1.14上继续双向合并",
    ],
    "RESEARCH_PROTOCOL_FREEZE_AUDIT_V2_20260724.md": [
        "POSITIONING_AMENDMENT_FROZEN_V2",
        "数据、split、标签、评测器、G1—G3和Task20冻结核心不变",
    ],
}

CURRENT_VERSION_FILES = {
    "AGENTS.md": "v1.19",
    "TASK_REGISTRY.md": "v1.19",
    ".light/project_card.md": "v1.19",
}

FORBIDDEN_POSITIVE = [
    "我们首次从多模态内容预测观众情感反应",
    "我们首次从视频内容预测受众反应分布",
    "本文首次研究内容到群体情感分布映射",
    "本文认为现有工作只识别内容表达情感，从未预测观众诱发情感",
]


def main() -> int:
    errors: list[str] = []

    for relative, needles in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing_file:{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"missing_required:{relative}:{needle}")

    for relative, version in CURRENT_VERSION_FILES.items():
        path = ROOT / relative
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if version not in text:
            errors.append(f"stale_version:{relative}:expected={version}")

    master = (ROOT / "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md").read_text(
        encoding="utf-8"
    )
    for item in ("H1", "H2", "H3", "H4"):
        if not re.search(rf"\|\s*{item}(?:（[^|]+）)?\s*\|", master):
            errors.append(f"missing_hypothesis:{item}")
    for index in range(10):
        if not re.search(rf"\|\s*E{index}\s*\|", master):
            errors.append(f"missing_experiment:E{index}")

    active_materials = [
        ROOT / "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md",
        ROOT / "TAFFC_PAPER_INNOVATION_AND_EXPERIMENT_TARGETS_20260723.md",
        ROOT / "CLAIM_EVIDENCE_MATRIX.md",
        ROOT / ".light" / "project_card.md",
    ]
    for path in active_materials:
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_POSITIVE:
            if phrase in text:
                errors.append(f"forbidden_positive_claim:{path.relative_to(ROOT)}:{phrase}")

    result = {
        "schema": "taffc.v119.positioning.validation.v1",
        "passed": not errors,
        "required_files_checked": len(REQUIRED),
        "current_version_files_checked": len(CURRENT_VERSION_FILES),
        "errors": errors,
        "coverage": "PROJECT_SPECIFIC_TEXT_GATE_NOT_FULL_SEMANTIC_CONSISTENCY",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
