"""Upload safe VC-CSA training scalars to SwanLab from an existing run.

This sidecar never opens comments, labels, predictions, I3D features, model
weights, or checkpoints. Authentication is accepted only through the
SWANLAB_API_KEY environment variable and is never persisted by this script.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import signal
import time
from typing import Dict, List, Optional, Tuple


STEP_PATTERN = re.compile(
    r"\[Epoch\s+(?P<epoch>\d+)\]"
    r"\[Step\s+(?P<batch>\d+)/(?P<last_batch>\d+)\]\s+"
    r"Loss_sum:\s*(?P<total>[-+0-9.eE]+),"
    r"opinion_loss:\s*(?P<opinion>[-+0-9.eE]+),\s*"
    r"emotion_loss:\s*(?P<emotion>[-+0-9.eE]+),\s*"
    r"Lr:\s*(?P<lr>[-+0-9.eE]+)"
)


def parse_step_record(
    line: str, steps_per_epoch: int
) -> Optional[Dict[str, object]]:
    """Parse one author-log progress record into safe scalar metrics."""
    match = STEP_PATTERN.search(line)
    if match is None:
        return None
    epoch = int(match.group("epoch"))
    batch = int(match.group("batch"))
    return {
        "step": epoch * steps_per_epoch + batch,
        "metrics": {
            "train/epoch": epoch,
            "train/batch": batch,
            "train/total_loss": float(match.group("total")),
            "train/opinion_loss": float(match.group("opinion")),
            "train/emotion_loss": float(match.group("emotion")),
            "train/lr": float(match.group("lr")),
        },
    }


def complete_epoch_records(
    run_dir: Path, steps_per_epoch: int
) -> List[Tuple[int, Dict[str, float]]]:
    """Return only epochs with both loss and dev-performance artifacts."""
    records: List[Tuple[int, Dict[str, float]]] = []
    for loss_path in sorted(
        run_dir.glob("loss_epoc_*.json"),
        key=lambda path: int(path.stem.rsplit("_", 1)[1]),
    ):
        epoch = int(loss_path.stem.rsplit("_", 1)[1])
        dev_path = run_dir / f"dev_performance_{epoch}.json"
        if not dev_path.is_file():
            continue
        loss = json.loads(loss_path.read_text(encoding="utf-8"))
        dev = json.loads(dev_path.read_text(encoding="utf-8"))
        opinion_micro = float(dev["opinion"]["micro"]["f1_score"])
        emotion_micro = float(dev["emotion"]["micro"]["f1_score"])
        metrics = {
            "epoch/train_total_loss": float(loss["epoch_loss"])
            / steps_per_epoch,
            "epoch/train_opinion_loss": float(loss["epoch_opinion_loss"])
            / steps_per_epoch,
            "epoch/train_emotion_loss": float(loss["epoch_emotion_loss"])
            / steps_per_epoch,
            "dev/opinion_micro_f1": opinion_micro,
            "dev/opinion_macro_f1": float(
                dev["opinion"]["macro"]["f1_score"]
            ),
            "dev/opinion_accuracy": float(dev["opinion"]["accuracy"]),
            "dev/emotion_micro_f1": emotion_micro,
            "dev/emotion_macro_f1": float(
                dev["emotion"]["macro"]["f1_score"]
            ),
            "dev/emotion_accuracy": float(dev["emotion"]["accuracy"]),
            "dev/combined_micro_f1": opinion_micro + emotion_micro,
        }
        records.append((epoch, metrics))
    return records


def _split_progress_records(
    pending: str, payload: bytes
) -> Tuple[List[str], str]:
    text = pending + payload.decode("utf-8", errors="ignore")
    parts = re.split(r"[\r\n]", text)
    return parts[:-1], parts[-1]


def _process_exists(pid: Optional[int]) -> bool:
    if pid is None:
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--workspace")
    parser.add_argument("--experiment-name", required=True)
    parser.add_argument("--logdir", type=Path, required=True)
    parser.add_argument("--training-pid", type=int)
    parser.add_argument("--steps-per-epoch", type=int, default=4693)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--log-every", type=int, default=10)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = os.environ.get("SWANLAB_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("SWANLAB_API_KEY is required")
    if not args.log.is_file() or not args.run_dir.is_dir():
        raise SystemExit("author log or run directory is missing")
    args.logdir.mkdir(parents=True, exist_ok=True)
    os.chmod(args.logdir, 0o700)

    import swanlab

    swanlab.login(
        api_key=api_key,
        save=False,
    )
    init_kwargs = {
        "project": args.project,
        "experiment_name": args.experiment_name,
        "mode": "online",
        "logdir": str(args.logdir),
        "config": {
            "identity": "AUTHOR_ORIGINAL_SETTING_NON_T0_LEAKAGE_ACCEPTED_EXPLORATORY",
            "formal_evidence_eligibility": "INELIGIBLE",
            "seed": 3407,
            "batch_size": 16,
            "steps_per_epoch": args.steps_per_epoch,
            "monitor": "read_only_author_log_sidecar",
        },
    }
    if args.workspace:
        init_kwargs["workspace"] = args.workspace
    run = swanlab.init(**init_kwargs)
    print(f"SWANLAB_RUN_INITIALIZED {run}", flush=True)

    seen_epochs = set()
    for epoch, metrics in complete_epoch_records(
        args.run_dir, args.steps_per_epoch
    ):
        swanlab.log(metrics, step=epoch)
        seen_epochs.add(epoch)
    print(
        f"SWANLAB_BACKFILL_COMPLETE epochs={len(seen_epochs)} "
        f"latest={max(seen_epochs) if seen_epochs else 'none'}",
        flush=True,
    )

    stop_requested = False

    def request_stop(_signum, _frame):
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    missing_process_polls = 0
    pending = ""
    with args.log.open("rb") as handle:
        handle.seek(0, os.SEEK_END)
        while not stop_requested:
            payload = handle.read()
            if payload:
                lines, pending = _split_progress_records(pending, payload)
                for line in lines:
                    record = parse_step_record(
                        line, steps_per_epoch=args.steps_per_epoch
                    )
                    if record is None:
                        continue
                    batch = int(record["metrics"]["train/batch"])
                    if (
                        batch % args.log_every == 0
                        or batch == int(
                            STEP_PATTERN.search(line).group("last_batch")
                        )
                    ):
                        swanlab.log(
                            record["metrics"],
                            step=int(record["step"]),
                        )

            for epoch, metrics in complete_epoch_records(
                args.run_dir, args.steps_per_epoch
            ):
                if epoch not in seen_epochs:
                    swanlab.log(metrics, step=epoch)
                    seen_epochs.add(epoch)
                    print(
                        f"SWANLAB_EPOCH_SYNCED epoch={epoch}", flush=True
                    )

            if _process_exists(args.training_pid):
                missing_process_polls = 0
            else:
                missing_process_polls += 1
                if missing_process_polls >= 3:
                    break
            time.sleep(args.poll_seconds)

    swanlab.finish()
    print("SWANLAB_SIDECAR_FINISHED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
