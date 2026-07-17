"""Run task-20 minimum baselines on one frozen CSMV split."""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from task20_baseline import load_canonical_records, run_minimum_baselines
from task20_contracts import build_run_manifest, load_config, validate_config
from task20_evaluation import build_prediction_rows, validate_e0_alignment

ROOT = Path(__file__).resolve().parents[1]


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=str(ROOT), text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "task20" / "baseline-common.json")
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "processed" / "HUMAN_GOLD" / "csmv" / "video_labels.v1.jsonl")
    parser.add_argument("--eval-split", choices=("dev", "test"), default="dev")
    parser.add_argument("--allow-final-test", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.eval_split == "test" and not args.allow_final_test:
        raise ValueError("test evaluation requires explicit --allow-final-test after preregistration freeze")

    config_path = args.config.resolve()
    config = load_config(config_path)
    validate_config(config, ROOT / "configs" / "task20" / "experiment.schema.json")
    data_config = config["data"]
    train = load_canonical_records(args.data, data_config["split_scheme"], "train", data_config["distribution_field"], data_config["class_order"])
    evaluation = load_canonical_records(args.data, data_config["split_scheme"], args.eval_split, data_config["distribution_field"], data_config["class_order"])
    results = run_minimum_baselines(train, evaluation)

    summary = {
        name: {key: value for key, value in result.items() if key not in {"predictions", "sample_ids"}}
        for name, result in results.items()
    }
    summary["data_contract"] = {
        "train_records": len(train),
        "evaluation_records": len(evaluation),
        "evaluation_split": args.eval_split,
        "shared_sample_ids": all(
            result["sample_ids"] == [record.item_id for record in evaluation]
            for result in results.values()
        ),
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))

    if args.output_dir is not None:
        output_dir = args.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=False)
        predictions_dir = output_dir / "predictions"
        predictions_dir.mkdir()
        commit = _git("rev-parse", "HEAD")
        dirty = bool(_git("status", "--porcelain"))
        manifest = build_run_manifest(
            run_id=output_dir.name,
            config=config,
            config_path=config_path,
            input_paths=[args.data.resolve(), ROOT / data_config["split_manifest"], ROOT / data_config["label_provenance_manifest"]],
            code_paths=[Path(__file__).resolve(), ROOT / "scripts" / "task20_baseline.py", ROOT / "scripts" / "task20_contracts.py"],
            git_commit=commit,
            git_dirty=dirty,
        )
        prediction_artifacts = {}
        expected_ids = [record.item_id for record in evaluation]
        targets = np.vstack([record.target for record in evaluation])
        for model_id, result in results.items():
            if result["status"] != "COMPLETED":
                continue
            rows = build_prediction_rows(
                sample_ids=expected_ids,
                split=args.eval_split,
                class_order=data_config["class_order"],
                targets=targets,
                predictions=result["predictions"],
                model_id=model_id,
                config_id=config["experiment_id"],
            )
            validate_e0_alignment(
                train_ids=[record.item_id for record in train],
                evaluation_ids=expected_ids,
                prediction_rows=rows,
                expected_split=args.eval_split,
                class_order=data_config["class_order"],
            )
            relative_path = "predictions/{}.jsonl".format(model_id)
            (output_dir / relative_path).write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )
            prediction_artifacts[model_id] = relative_path
        manifest.update({
            "status": "COMPLETED",
            "completed_at": datetime.now(timezone.utc).astimezone().isoformat(),
            "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "numpy": np.__version__},
            "evaluation_split": args.eval_split,
            "artifacts": {"metrics": "metrics.json", "predictions": prediction_artifacts},
        })
        (output_dir / "metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / "run-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
