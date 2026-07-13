"""Minimal, side-effect-free environment import check."""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import sys


PROFILES = {
    "historical": ["torch", "catboost", "transformers", "sklearn", "MMSA"],
    "formal-carm": ["torch", "catboost", "transformers", "sklearn", "MMSA", "faiss"],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=sorted(PROFILES), default="historical")
    args = parser.parse_args()
    found = {name: importlib.util.find_spec(name) is not None for name in PROFILES[args.profile]}
    report = {
        "profile": args.profile,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "imports": found,
        "passed": all(found.values()),
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
