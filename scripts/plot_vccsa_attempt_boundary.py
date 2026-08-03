"""Build an auditable VC-CSA loss display with an explicit attempt boundary.

The Epoch 1--3 recovery rerun and the historical Epoch 4--120 run are
independent attempts.  This module therefore validates and plots them as two
disconnected segments; it never interpolates or smooths across Epoch 3/4.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Dict, Iterable, List


ATTEMPT2 = "TASK20_VCCSA_EPOCH1_3_RECOVERY_RERUN_SEED3407_ATTEMPT2"
ATTEMPT1 = "TASK20_VCCSA_AUTHOR_ORIGINAL_FULL_SEED3407_ATTEMPT1"
BOUNDARY = "INDEPENDENT ATTEMPT BOUNDARY"
FIELDS = [
    "attempt_id",
    "epoch_label",
    "epoch",
    "total_mean",
    "opinion_mean",
    "emotion_mean",
    "source_artifact_sha256",
    "run_instance_digest",
    "cross_attempt_comparable",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_loss(path: Path) -> Dict[str, float]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    required = {"epoch_loss", "epoch_opinion_loss", "epoch_emotion_loss"}
    if set(raw) != required:
        raise ValueError(f"unexpected loss schema: {path}")
    return {key: float(raw[key]) for key in required}


def build_rows(
    attempt2_dir: Path,
    attempt1_dir: Path,
    attempt2_instance_digest: str,
    attempt1_instance_digest: str,
    steps_per_epoch: int = 4693,
) -> List[Dict[str, object]]:
    """Read aggregate author loss JSON and return two non-comparable segments."""
    if steps_per_epoch <= 0:
        raise ValueError("steps_per_epoch must be positive")
    rows: List[Dict[str, object]] = []
    specifications = (
        (ATTEMPT2, range(1, 4), attempt2_dir, attempt2_instance_digest),
        (ATTEMPT1, range(4, 121), attempt1_dir, attempt1_instance_digest),
    )
    for attempt_id, epochs, root, instance_digest in specifications:
        if len(instance_digest) != 64:
            raise ValueError("run_instance_digest must be a SHA-256 hex digest")
        for epoch in epochs:
            path = root / f"loss_epoc_{epoch}.json"
            values = _read_loss(path)
            rows.append(
                {
                    "attempt_id": attempt_id,
                    "epoch_label": f"Epoch {epoch}",
                    "epoch": epoch,
                    "total_mean": values["epoch_loss"] / steps_per_epoch,
                    "opinion_mean": values["epoch_opinion_loss"] / steps_per_epoch,
                    "emotion_mean": values["epoch_emotion_loss"] / steps_per_epoch,
                    "source_artifact_sha256": sha256_file(path),
                    "run_instance_digest": instance_digest,
                    "cross_attempt_comparable": "false",
                }
            )
    validate_rows(rows)
    return rows


def validate_rows(rows: Iterable[Dict[str, object]]) -> None:
    materialized = list(rows)
    if len(materialized) != 120:
        raise ValueError("display must contain exactly 120 partitioned rows")
    a2 = [int(row["epoch"]) for row in materialized if row["attempt_id"] == ATTEMPT2]
    a1 = [int(row["epoch"]) for row in materialized if row["attempt_id"] == ATTEMPT1]
    if a2 != [1, 2, 3] or a1 != list(range(4, 121)):
        raise ValueError("attempt partitions must be Epoch 1--3 and Epoch 4--120")
    if any(str(row["cross_attempt_comparable"]).lower() != "false" for row in materialized):
        raise ValueError("cross-attempt comparability must remain false")


def write_csv(rows: List[Dict[str, object]], output: Path) -> None:
    validate_rows(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, object]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        row["epoch"] = int(row["epoch"])
        for name in ("total_mean", "opinion_mean", "emotion_mean"):
            row[name] = float(row[name])
    validate_rows(rows)
    return rows


def plot_rows(rows: List[Dict[str, object]], png: Path, svg: Path) -> None:
    import matplotlib.pyplot as plt

    validate_rows(rows)
    fig, ax = plt.subplots(figsize=(11.5, 6.5))
    colors = {"total_mean": "#1f77b4", "opinion_mean": "#d95f02", "emotion_mean": "#2ca02c"}
    labels = {"total_mean": "Total", "opinion_mean": "Opinion", "emotion_mean": "Emotion"}
    for attempt_id, linestyle, alpha in ((ATTEMPT2, "--", 1.0), (ATTEMPT1, "-", 0.82)):
        segment = [row for row in rows if row["attempt_id"] == attempt_id]
        for metric in ("total_mean", "opinion_mean", "emotion_mean"):
            ax.plot(
                [row["epoch"] for row in segment],
                [row[metric] for row in segment],
                color=colors[metric],
                linestyle=linestyle,
                alpha=alpha,
                linewidth=2,
                label=f"{labels[metric]} ({'Attempt2 E1-3' if attempt_id == ATTEMPT2 else 'Attempt1 E4-120'})",
            )
    ax.axvspan(3.35, 3.65, color="#777777", alpha=0.22)
    ax.axvline(3.5, color="#333333", linestyle=":", linewidth=1.5)
    ax.text(3.72, ax.get_ylim()[1] * 0.93, BOUNDARY, rotation=90, va="top", fontsize=9)
    ax.set_title("VC-CSA NON-T0 loss: independent attempts shown without cross-boundary connection")
    ax.set_xlabel("Epoch label (attempt-partitioned)")
    ax.set_ylabel("Mean training loss per step")
    ax.grid(alpha=0.2)
    ax.legend(ncol=2, fontsize=8)
    fig.text(
        0.5,
        0.01,
        "NON_T0 / INELIGIBLE. Original Attempt1 Epoch 1-3 remain missing. "
        "Attempt2 and Attempt1 differ by initialization and instance provenance; cross-attempt comparison is invalid.",
        ha="center",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png, dpi=220)
    fig.savefig(svg)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt2-loss-dir", type=Path)
    parser.add_argument("--attempt1-loss-dir", type=Path)
    parser.add_argument("--attempt2-instance-digest")
    parser.add_argument("--attempt1-instance-digest")
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--png", type=Path, required=True)
    parser.add_argument("--svg", type=Path, required=True)
    parser.add_argument("--plot-existing-csv", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.plot_existing_csv:
        rows = read_csv(args.csv)
    else:
        required = (
            args.attempt2_loss_dir,
            args.attempt1_loss_dir,
            args.attempt2_instance_digest,
            args.attempt1_instance_digest,
        )
        if any(value is None for value in required):
            raise ValueError("loss directories and instance digests are required")
        rows = build_rows(
            args.attempt2_loss_dir,
            args.attempt1_loss_dir,
            args.attempt2_instance_digest,
            args.attempt1_instance_digest,
        )
        write_csv(rows, args.csv)
    plot_rows(rows, args.png, args.svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
