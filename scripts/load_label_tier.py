"""Load exactly one canonical label tier with T0 leakage guards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, Iterator


TIERS = {"HUMAN_GOLD", "SILVER", "UNLABELED"}
FORBIDDEN_TEXT_KEYS = {
    "comment",
    "comments",
    "comment_text",
    "target_comment",
    "target_comments",
}


def load_tier(path: Path, expected_tier: str) -> Iterator[dict]:
    if expected_tier not in TIERS:
        raise ValueError("expected_tier must be HUMAN_GOLD, SILVER, or UNLABELED")
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            actual = record.get("label_tier")
            if actual != expected_tier:
                raise ValueError(
                    "mixed label tiers are forbidden: line {} expected {} got {}".format(
                        line_number, expected_tier, actual
                    )
                )
            leaked = FORBIDDEN_TEXT_KEYS & set(record)
            if leaked:
                raise ValueError("target comment fields are forbidden: {}".format(sorted(leaked)))
            if expected_tier == "HUMAN_GOLD" and record.get("label_source", "").startswith("silver"):
                raise ValueError("silver provenance cannot enter HUMAN_GOLD")
            yield record


def count_tier(path: Path, expected_tier: str) -> int:
    return sum(1 for _ in load_tier(path, expected_tier))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument("--tier", required=True, choices=sorted(TIERS))
    args = parser.parse_args()
    print(json.dumps({"tier": args.tier, "records": count_tier(args.path, args.tier)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
