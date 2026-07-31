#!/usr/bin/env python3
"""Validate the living T-AFFC manuscript SSOT without treating gaps as results."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper" / "TAFFC_CARM_MANUSCRIPT_SSOT.md"
BLUEPRINT = ROOT / "paper" / "CLAIM_ARGUMENT_BLUEPRINT.md"

REQUIRED_MANUSCRIPT_MARKERS = (
    "manuscript_status: MANUSCRIPT_SCAFFOLD_NO_FORMAL_RESULTS",
    "## Abstract",
    "## 1. Introduction",
    "## 2. Related Work",
    "## 3. Problem Formulation and Information Boundary",
    "## 4. Method",
    "## 5. Experimental Design",
    "## 6. Results",
    "## 7. Discussion",
    "## 8. Limitations and Broader Considerations",
    "## 9. Conclusion",
    "## Data Availability",
    "## Code Availability",
    "## Ethics, Privacy, and Responsible Use",
    "## Author Contributions",
    "## Conflict of Interest",
    "## Funding",
    "## Generative AI and Automated-Tool Disclosure",
    "## References",
    "Video2Reaction is the closest direct prior",
    "publicly expressed induced-reaction distribution",
    "[RESULT-GAP:",
)

REQUIRED_BLUEPRINT_MARKERS = (
    "## 2. Argument chain",
    "## 3. Claim contracts",
    "## 5. Planned figures and tables",
    "## 6. Reviewer-attack pre-mortem",
    "## 7. Claim blacklist operationalization",
    "## 8. Citation-slot registry",
    "## 9. Result-ingestion contract",
    "## 10. Negative-result downgrade paths",
)

# These are forbidden as active English claims in the manuscript. The patterns
# intentionally target affirmative formulations rather than explicit negations.
FORBIDDEN_ACTIVE_PATTERNS = (
    r"\bwe (?:are the first to|first|pioneer)\b",
    r"\bthe first (?:framework|method|study|task|benchmark)\b",
    r"\bfor the first time\b",
    r"\bnovel combination\b",
    r"\bcomments represent all viewers\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bsignificantly outperforms\b",
)

FORBIDDEN_FORMAL_EVIDENCE_TOKENS = (
    "AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY",
    "Epoch 109",
    "Epoch 110",
    "1.370094",
)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []

    for path in (MANUSCRIPT, BLUEPRINT):
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}", failures)

    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        return 1

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    blueprint = BLUEPRINT.read_text(encoding="utf-8")

    for marker in REQUIRED_MANUSCRIPT_MARKERS:
        if marker not in manuscript:
            fail(f"manuscript missing marker: {marker}", failures)

    for marker in REQUIRED_BLUEPRINT_MARKERS:
        if marker not in blueprint:
            fail(f"blueprint missing marker: {marker}", failures)

    lowered = manuscript.lower()
    for pattern in FORBIDDEN_ACTIVE_PATTERNS:
        if re.search(pattern, lowered):
            fail(f"manuscript matches forbidden active-claim pattern: {pattern}", failures)

    for token in FORBIDDEN_FORMAL_EVIDENCE_TOKENS:
        if token in manuscript:
            fail(f"manuscript contains ineligible exploratory evidence token: {token}", failures)

    citation_slots = set(re.findall(r"\[CITATION-GAP:([A-Z0-9_]+)\]", manuscript))
    registry_slots = set(re.findall(r"\bCIT-([A-Z0-9_]+)\b", blueprint))
    missing_registry = citation_slots - registry_slots
    if missing_registry:
        fail(
            "citation slots missing from blueprint registry: "
            + ", ".join(sorted(missing_registry)),
            failures,
        )

    for claim in ("C1", "C2", "C3", "C4"):
        if not re.search(rf"\|\s*{claim}\b.*\bTO_VERIFY\b", manuscript):
            fail(f"main result shell does not preserve {claim}=TO_VERIFY", failures)

    if manuscript.count("[RESULT-GAP:") < 12:
        fail("too few explicit result gates for a no-results scaffold", failures)

    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        print(f"passed=false failures={len(failures)}")
        return 1

    print(
        "passed=true "
        f"manuscript_bytes={len(manuscript.encode('utf-8'))} "
        f"blueprint_bytes={len(blueprint.encode('utf-8'))} "
        f"citation_slots={len(citation_slots)} "
        f"result_gates={manuscript.count('[RESULT-GAP:')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
