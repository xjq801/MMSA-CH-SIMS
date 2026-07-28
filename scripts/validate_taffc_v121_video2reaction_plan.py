"""Validate the v1.21 Video2Reaction dual-track planning contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = {
    "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md": [
        "版本：v1.21",
        "规格版本：v1.5",
        "Video2Reaction公开资产边界与双轨证据角色",
        "SILVER_LLM_HUMAN_VERIFIED",
        "A轨为**CSMV公平适配主对比**",
        "B轨为**Video2Reaction原生外部验证**",
        "VIDEO2REACTION_DATA_INTAKE.md",
        "VIDEO2REACTION_REPRODUCTION_REPORT.md",
        "VIDEO2REACTION_MOVIE_SPLIT_AUDIT.md",
        "V2R_BASELINE_ADAPTATION_REPORT.md",
        "不改变现有G1—G3",
    ],
    "DATA_SOURCE_LEDGER.md": [
        "版本：v1.6",
        "DS-012",
        "APPROVED_PLANNED_DUAL_TRACK_INTAKE_NOT_FROZEN",
        "原始视频/独立音频/完整转写/原始评论不随公开包保证提供",
    ],
    "CLAIM_EVIDENCE_MATRIX.md": [
        "版本：v1.3",
        "Video2Reaction双轨证据合同",
        "第三HUMAN_GOLD主集",
    ],
    "CONTRIBUTION_PRIOR_ART_MATRIX.md": [
        "FROZEN_v5",
        "V2R-A",
        "V2R-B",
    ],
    "TASK_REGISTRY.md": [
        "版本：v1.3",
        "总纲v1.21",
        "Video2Reaction A轨CSMV公平适配+B轨原生银标外部验证",
    ],
    "RISK_REGISTER.md": [
        "R-DATA-004",
        "总纲v1.21",
    ],
    ".light/project_card.md": [
        "v1.21",
        "SILVER_LLM_HUMAN_VERIFIED",
    ],
    ".light/terminology.md": [
        "V2R-A",
        "V2R-B",
    ],
}


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for relative, terms in REQUIRED.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"missing_file:{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        for term in terms:
            if term not in text:
                errors.append(f"missing_term:{relative}:{term}")

    master = texts.get("TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md", "")
    task20_start = master.find("### 4. 任务20")
    task30_start = master.find("### 5. 任务30")
    if min(task20_start, task30_start) < 0:
        errors.append("missing_task20_or_task30_section")
    else:
        frozen_task20 = master[task20_start:task30_start]
        if "VIDEO2REACTION_DATA_INTAKE.md" in frozen_task20:
            errors.append("task20_was_retroactively_assigned_v2r_intake")

    if "HUMAN_GOLD`；评论经两阶段多代理LLM" in texts.get("DATA_SOURCE_LEDGER.md", ""):
        errors.append("v2r_silver_was_mislabeled_human_gold")

    result = {
        "schema": "taffc.v121.video2reaction.plan.validation.v1",
        "passed": not errors,
        "files_checked": len(REQUIRED),
        "errors": errors,
        "coverage": "PROJECT_SPECIFIC_SSOT_CONSISTENCY_NOT_DATA_ACQUISITION_OR_EMPIRICAL_VALIDATION",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
