"""Validate the append-only project work log contract."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "WORK_LOG.md"
ENTRY_RE = re.compile(r"^## (WR-(\d{8})-(\d{3})) — (.+)$", re.MULTILINE)
REQUIRED_METADATA = ["时间", "类型", "任务/门", "状态", "负责人"]
REQUIRED_SECTIONS = [
    "背景与目标",
    "实际变更",
    "验证与证据",
    "影响与边界",
    "风险、问题与阻塞",
    "下一步",
    "Git状态",
]


def validate_work_log(path: Path = LOG_PATH) -> Dict[str, object]:
    errors: List[str] = []
    if not path.is_file():
        return {"passed": False, "entries": 0, "latest_id": None, "errors": ["WORK_LOG.md不存在"]}

    text = path.read_text(encoding="utf-8")
    matches = list(ENTRY_RE.finditer(text))
    if not matches:
        return {"passed": False, "entries": 0, "latest_id": None, "errors": ["没有有效的WR记录"]}

    seen = set()
    order = []
    for index, match in enumerate(matches):
        entry_id, date_text, sequence_text, title = match.groups()
        if entry_id in seen:
            errors.append("重复记录编号: " + entry_id)
        seen.add(entry_id)
        order.append((date_text, int(sequence_text)))
        if not title.strip():
            errors.append(entry_id + "标题为空")

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        for field in REQUIRED_METADATA:
            if not re.search(r"^- " + re.escape(field) + r"：\S.*$", body, re.MULTILINE):
                errors.append(entry_id + "缺少元数据: " + field)
        for section in REQUIRED_SECTIONS:
            section_match = re.search(
                r"^### " + re.escape(section) + r"\s*$([\s\S]*?)(?=^### |\Z)",
                body,
                re.MULTILINE,
            )
            if not section_match or not section_match.group(1).strip():
                errors.append(entry_id + "缺少或留空章节: " + section)

    if order != sorted(order):
        errors.append("记录编号未按日期和序号递增")
    per_date = {}
    for date_text, sequence in order:
        per_date.setdefault(date_text, []).append(sequence)
    for date_text, sequences in per_date.items():
        expected = list(range(1, len(sequences) + 1))
        if sequences != expected:
            errors.append(date_text + "的序号必须从001连续递增")

    return {
        "passed": not errors,
        "entries": len(matches),
        "latest_id": matches[-1].group(1),
        "errors": errors,
    }


def main() -> int:
    result = validate_work_log()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
