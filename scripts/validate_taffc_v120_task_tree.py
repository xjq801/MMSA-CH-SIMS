"""Validate the v1.20 task-tree contract for benefit-aware routing."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md"

MASTER_TERMS = [
    "版本：v1.20",
    "规格版本：v1.4",
    "只把C2后半的“收益感知历史反应记忆”落实为可执行、可证伪的任务40/50合同",
    "预判检索相对content-only是否有益",
    "train内部cross-fitting/out-of-fold效用标签",
    "u_i=L(content-only_i,y_i)-L(memory_i,y_i)",
    "固定融合、相似度阈值、预测熵阈值和SelectiveNet式拒绝",
    "比较拒绝方法时匹配coverage或风险预算",
    "被避免的负迁移比例",
    "success、failure和inconclusive分支",
    "不得只给目标方法五种子而给路由对照单种子",
    "任务30尚未创建",
    "不恢复v1.17的3%/5%/8%硬效应门",
]

CURRENT_FILES = {
    "AGENTS.md": ["v1.20"],
    "TASK_REGISTRY.md": ["版本：v1.2", "v1.20门", "train内部OOF效用标签"],
    "CONTRIBUTION_PRIOR_ART_MATRIX.md": [
        "FROZEN_v4",
        "coverage匹配",
        "SelectiveNet式拒绝",
    ],
    "CLAIM_EVIDENCE_MATRIX.md": [
        "版本：v1.2",
        "2026-07-27 第17节收益感知路由执行合同",
    ],
    "RISK_REGISTER.md": ["总纲v1.20", "删除完整检索创新claim"],
    ".light/project_card.md": ["v1.20", "OOF效用标签"],
    ".light/terminology.md": ["收益感知可靠性路由", "benefit-aware reliability routing"],
}


def main() -> int:
    errors: list[str] = []
    if not MASTER.is_file():
        errors.append("missing_master")
        master = ""
    else:
        master = MASTER.read_text(encoding="utf-8")

    for term in MASTER_TERMS:
        if term not in master:
            errors.append(f"missing_master_term:{term}")

    task20_start = master.find("### 4. 任务20")
    task30_start = master.find("### 5. 任务30")
    task40_start = master.find("### 6. 任务40")
    task50_start = master.find("### 7. 任务50")
    if min(task20_start, task30_start, task40_start, task50_start) < 0:
        errors.append("missing_task_section")
    elif "收益感知" in master[task20_start:task30_start]:
        errors.append("task20_frozen_interface_was_expanded_with_benefit_router")

    for relative, terms in CURRENT_FILES.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing_file:{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term not in text:
                errors.append(f"missing_term:{relative}:{term}")

    result = {
        "schema": "taffc.v120.task_tree.validation.v1",
        "passed": not errors,
        "master_terms_checked": len(MASTER_TERMS),
        "current_files_checked": len(CURRENT_FILES),
        "errors": errors,
        "coverage": "PROJECT_SPECIFIC_TEXT_CONTRACT_NOT_EMPIRICAL_METHOD_VALIDATION",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
