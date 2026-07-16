"""Validate the durable IJCV project handoff without requiring CSMV raw assets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "IJCV_PROJECT_CONTEXT_HANDOFF_20260716.md",
    "IJCV_TAFFC_DUAL_TRACK_FEASIBILITY_AND_PLAN_20260716.md",
    "TAFFC_CH4_10_MONTH_MASTER_PLAN_20260713.md",
    "CLAIM_EVIDENCE_MATRIX.md",
    "DECISION_LOG.md",
    "RISK_REGISTER.md",
    "DATA_SOURCE_LEDGER.md",
    "WORK_RECORD_POLICY.md",
    "WORK_LOG.md",
]

REQUIRED_HANDOFF_TERMS = [
    "00-IJCV总控与J0启动任务",
    "2026-08-12",
    "2026-12-15",
    "847张AI生成图像",
    "63,682条合规HUMAN_GOLD响应",
    "ad58c268e34adf02bd8e639338069d34576e1d9602f819a2cc6fa89be6836818",
    "BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE",
    "JH1",
    "JH2",
    "JH3",
    "PC Loss",
    "SAMNet",
    "MFRN",
    "J0未通过不得创建任务25",
]


def main() -> int:
    missing_files = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    handoff_path = ROOT / "IJCV_PROJECT_CONTEXT_HANDOFF_20260716.md"
    handoff = handoff_path.read_text("utf-8") if handoff_path.is_file() else ""
    missing_terms = [term for term in REQUIRED_HANDOFF_TERMS if term not in handoff]

    agents = (ROOT / "AGENTS.md").read_text("utf-8") if (ROOT / "AGENTS.md").is_file() else ""
    agent_contract = {
        "j0_only_before_gate": "当前只执行IJCV的J0" in agents,
        "taffc_read_only": "T-AFFC" in agents and "只读" in agents,
        "branch_isolated": "codex/ijcv-j0" in agents,
        "no_dual_submission": "同一稿件" in agents and "不得同时送审" in agents,
    }

    forbidden_handoff_fragments = ["BEGIN PRIVATE KEY", "ghp_", "Cookie:"]
    forbidden_hits = [value for value in forbidden_handoff_fragments if value in handoff]

    passed = (
        not missing_files
        and not missing_terms
        and all(agent_contract.values())
        and not forbidden_hits
    )
    report = {
        "schema": "ijcv-project-handoff-check-v1",
        "passed": passed,
        "required_files": {"missing": missing_files, "passed": not missing_files},
        "handoff_terms": {"missing": missing_terms, "passed": not missing_terms},
        "agent_contract": agent_contract,
        "sensitive_fragment_hits": forbidden_hits,
        "scientific_gate_state": {
            "ijcv_j0": "NOT_YET_REVIEWED",
            "source_g1": "PASS",
            "source_g2": "BLOCKED_CSMV_INPUT_ASSET_LICENSE_FIXITY_AND_COVERAGE",
            "task25_created": False,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
