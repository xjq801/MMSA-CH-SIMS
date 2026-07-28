"""Render the Task20 VC-CSA complete-epoch training-loss curve."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "paper" / "figures" / "task20_vccsa_loss_curve.csv"
OUTPUT_BASE = ROOT / "paper" / "figures" / "task20_vccsa_loss_curve"
STEPS_PER_EPOCH = 4693
FROZEN_DEV_BEST_EPOCH = 22


def read_rows() -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {
        "epoch": [],
        "total_mean": [],
        "opinion_mean": [],
        "emotion_mean": [],
    }
    with DATA_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for key in columns:
                columns[key].append(float(row[key]))
    return columns


def main() -> None:
    data = read_rows()
    epochs = data["epoch"]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "svg.fonttype": "none",
        }
    )
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    fig.subplots_adjust(left=0.12, right=0.985, top=0.90, bottom=0.22)

    # Okabe-Ito colors plus redundant line styles/markers for grayscale access.
    ax.plot(
        epochs,
        data["total_mean"],
        color="#0072B2",
        linewidth=2.2,
        marker="o",
        markevery=2,
        markersize=3.4,
        label="Total loss",
    )
    ax.plot(
        epochs,
        data["opinion_mean"],
        color="#D55E00",
        linewidth=1.8,
        linestyle="--",
        marker="s",
        markevery=2,
        markersize=3.0,
        label="Opinion loss",
    )
    ax.plot(
        epochs,
        data["emotion_mean"],
        color="#009E73",
        linewidth=1.8,
        linestyle="-.",
        marker="^",
        markevery=2,
        markersize=3.2,
        label="Emotion loss",
    )

    ax.axvline(
        FROZEN_DEV_BEST_EPOCH,
        color="#6F6F6F",
        linewidth=1.2,
        linestyle=(0, (3, 3)),
        label="Frozen dev best (Epoch 22)",
    )
    ax.annotate(
        "Train loss keeps falling\nafter the frozen dev best",
        xy=(FROZEN_DEV_BEST_EPOCH, data["total_mean"][18]),
        xytext=(23.5, 0.069),
        arrowprops={"arrowstyle": "->", "color": "#555555", "linewidth": 0.9},
        color="#444444",
        fontsize=8,
    )

    ax.set_title("VC-CSA training loss — seed 3407")
    ax.set_xlabel("Completed epoch")
    ax.set_ylabel(f"Mean loss per batch (n={STEPS_PER_EPOCH:,} batches/epoch)")
    ax.set_xlim(3.5, 33.5)
    ax.set_ylim(0.0, 0.16)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.02))
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.7, alpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", frameon=False)
    fig.text(
        0.01,
        0.025,
        "Complete-epoch artifacts available for Epochs 4–33; Epochs 1–3 are not reconstructed. "
        "Single exploratory run; no uncertainty band.",
        fontsize=7,
        color="#555555",
    )

    OUTPUT_BASE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_BASE.with_suffix(".png"), dpi=300, facecolor="white")
    fig.savefig(OUTPUT_BASE.with_suffix(".svg"), facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
