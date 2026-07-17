"""Tune and evaluate the frozen-I3D pooled MLP without test adaptation."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import sys
from typing import Dict, List, Sequence, Tuple

import numpy as np
import torch

from task20_baseline import load_canonical_records
from task20_evaluation import build_prediction_rows, validate_e0_alignment
from task20_metrics import evaluate_distribution_predictions
from task20_training import PooledTrialConfig, predict_pooled_model, train_pooled_trial


ROOT = Path(__file__).resolve().parents[1]
CLASS_ORDER = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def load_feature_split(cache_path: Path, split: str) -> Tuple[List[str], np.ndarray]:
    with np.load(cache_path, allow_pickle=False) as cache:
        item_ids = cache["item_ids"].astype(str)
        splits = cache["splits"].astype(str)
        features = cache["features"].astype(np.float32)
    if item_ids.shape != splits.shape or features.shape != (item_ids.size, 2048):
        raise ValueError("pooled cache schema mismatch")
    indices = np.flatnonzero(splits == split)
    if indices.size == 0:
        raise ValueError("empty cached split: {}".format(split))
    return item_ids[indices].tolist(), features[indices]


def load_targets(labels_path: Path, split: str, expected_ids: Sequence[str]) -> np.ndarray:
    records = load_canonical_records(
        labels_path,
        split_scheme="group_by_video_v1",
        expected_split=split,
        distribution_field="emotion_distribution",
        class_order=CLASS_ORDER,
    )
    by_id = {record.item_id: record.target for record in records}
    if set(by_id) != set(expected_ids):
        raise ValueError("label/cache sample ID mismatch for {}".format(split))
    return np.vstack([by_id[item_id] for item_id in expected_ids]).astype(np.float32)


def trial_grid(tuning_plan: Dict[str, object], smoke: bool) -> List[PooledTrialConfig]:
    family = next(row for row in tuning_plan["model_families"] if row["id"] == "frozen_i3d_mlp")
    space = family["space"]
    maximum = 1 if smoke else int(family["max_trials"])
    max_epochs = 2 if smoke else int(family["early_stopping"]["max_rounds"])
    patience = 2 if smoke else int(family["early_stopping"]["patience_rounds"])
    rows = [
        PooledTrialConfig(
            hidden_dim=int(hidden_dim),
            dropout=float(dropout),
            learning_rate=float(learning_rate),
            max_epochs=max_epochs,
            patience=patience,
            batch_size=128,
        )
        for hidden_dim, dropout, learning_rate in itertools.product(
            space["hidden_dim"], space["dropout"], space["learning_rate"]
        )
    ]
    if len(rows) != int(family["max_trials"]):
        raise ValueError("frozen MLP search space does not equal max_trials")
    return rows[:maximum]


def config_dict(config: PooledTrialConfig) -> Dict[str, object]:
    return {
        "hidden_dim": config.hidden_dim,
        "dropout": config.dropout,
        "learning_rate": config.learning_rate,
        "max_epochs": config.max_epochs,
        "patience": config.patience,
        "batch_size": config.batch_size,
    }


def parameter_count(model: torch.nn.Module) -> int:
    return int(sum(parameter.numel() for parameter in model.parameters()))


def artifact_entry(path: Path) -> Dict[str, object]:
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def fit_pooled_for_evaluation(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    dev_features: np.ndarray,
    dev_targets: np.ndarray,
    eval_features: np.ndarray,
    config: PooledTrialConfig,
    seed: int,
    device: str,
) -> Tuple[Dict[str, object], np.ndarray]:
    result = train_pooled_trial(
        train_features,
        train_targets,
        ["train"] * train_features.shape[0],
        dev_features,
        dev_targets,
        config,
        seed=seed,
        device=device,
    )
    predictions = predict_pooled_model(
        result["model"],
        result["standardizer"],
        eval_features,
        device,
    )
    return result, predictions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--tuning-plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--eval-split", choices=("dev", "test"), default="dev")
    parser.add_argument("--allow-final-test", action="store_true")
    parser.add_argument("--selection-file", type=Path)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    parser.add_argument("--seed", type=int, default=20260717)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--git-commit", required=True)
    parser.add_argument("--git-dirty", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.eval_split == "test" and (not args.allow_final_test or args.selection_file is None):
        raise ValueError("test requires explicit authorization and a frozen dev selection file")
    if args.eval_split == "dev" and args.selection_file is not None:
        raise ValueError("dev tuning must use the frozen search space, not an external selection")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    started_at = now()
    try:
        tuning_plan = json.loads(args.tuning_plan.read_text(encoding="utf-8"))
        train_ids, train_features = load_feature_split(args.cache, "train")
        eval_ids, eval_features = load_feature_split(args.cache, args.eval_split)
        train_targets = load_targets(args.labels, "train", train_ids)
        eval_targets = load_targets(args.labels, args.eval_split, eval_ids)
        if args.eval_split == "test":
            dev_ids, dev_features = load_feature_split(args.cache, "dev")
            dev_targets = load_targets(args.labels, "dev", dev_ids)
        else:
            dev_ids, dev_features, dev_targets = eval_ids, eval_features, eval_targets

        if args.selection_file is None:
            configs = trial_grid(tuning_plan, args.smoke)
        else:
            frozen = json.loads(args.selection_file.read_text(encoding="utf-8"))["selected_config"]
            configs = [PooledTrialConfig(**frozen)]
        trials = []
        selected = None
        selected_key = None
        for index, config in enumerate(configs, 1):
            if args.eval_split == "test":
                result, eval_predictions = fit_pooled_for_evaluation(
                    train_features,
                    train_targets,
                    dev_features,
                    dev_targets,
                    eval_features,
                    config,
                    seed=args.seed,
                    device=args.device,
                )
            else:
                result = train_pooled_trial(
                    train_features,
                    train_targets,
                    ["train"] * len(train_ids),
                    dev_features,
                    dev_targets,
                    config,
                    seed=args.seed,
                    device=args.device,
                )
                eval_predictions = result["dev_predictions"]
            params = parameter_count(result["model"])
            row = {
                "trial": index,
                "config": config_dict(config),
                "best_epoch": result["best_epoch"],
                "epochs_ran": result["epochs_ran"],
                "parameter_count": params,
                "metrics": result["dev_metrics"],
            }
            trials.append(row)
            metrics = result["dev_metrics"]
            key = (
                metrics["jensen_shannon_divergence"],
                metrics["negative_log_likelihood"],
                metrics["brier_score"],
                params,
                index,
            )
            if selected_key is None or key < selected_key:
                selected_key = key
                selected = (config, result, row, eval_predictions)
        if selected is None:
            raise RuntimeError("no completed trial")
        selected_config, selected_result, selected_row, predictions = selected
        evaluation_metrics = evaluate_distribution_predictions(eval_targets.astype(np.float64), predictions)
        prediction_rows = build_prediction_rows(
            sample_ids=eval_ids,
            split=args.eval_split,
            class_order=CLASS_ORDER,
            targets=eval_targets,
            predictions=predictions,
            model_id="frozen_i3d_pooled_mlp",
            config_id="task20-frozen-i3d-pooled-mlp-v1",
        )
        validate_e0_alignment(train_ids, eval_ids, prediction_rows, args.eval_split, CLASS_ORDER)

        predictions_path = output_dir / "predictions.jsonl"
        predictions_path.write_text(
            "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in prediction_rows),
            encoding="utf-8",
        )
        metrics_path = output_dir / "metrics.json"
        metrics_path.write_text(
            json.dumps(evaluation_metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        trials_path = output_dir / "trial_results.json"
        trials_path.write_text(json.dumps(trials, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        selection_path = output_dir / "selection.json"
        selection = {
            "schema_version": "task20-model-selection-v1",
            "selection_split": "dev" if args.selection_file is None else "frozen_from_dev_selection_file",
            "selected_config": config_dict(selected_config),
            "selected_trial": selected_row["trial"],
            "selection_metrics": selected_row["metrics"],
            "test_visible_during_selection": False,
        }
        selection_path.write_text(json.dumps(selection, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        model_path = output_dir / "model.pt"
        torch.save(selected_result["model"].state_dict(), model_path)
        standardizer_path = output_dir / "standardizer.npz"
        np.savez(
            standardizer_path,
            mean=selected_result["standardizer"].mean,
            scale=selected_result["standardizer"].scale,
        )
        environment_path = output_dir / "environment.json"
        environment = {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "device": args.device,
            "dtype": "float32",
            "amp": False,
            "pythonhashseed": os.environ.get("PYTHONHASHSEED"),
            "num_workers": 0,
        }
        environment_path.write_text(json.dumps(environment, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        ended_at = now()
        artifacts = [predictions_path, metrics_path, trials_path, selection_path, model_path, standardizer_path, environment_path]
        input_rows = [
            {"role": "non_reversible_pooled_i3d", "sha256": sha256(args.cache), "file": args.cache.name},
            {"role": "canonical_labels", "sha256": sha256(args.labels), "file": args.labels.name},
            {"role": "tuning_plan", "sha256": sha256(args.tuning_plan), "file": args.tuning_plan.name},
        ]
        if args.selection_file is not None:
            input_rows.append(
                {"role": "frozen_dev_selection", "sha256": sha256(args.selection_file), "file": args.selection_file.name}
            )
        manifest = {
            "schema_version": "task20-run-manifest-v1",
            "run_id": output_dir.name,
            "experiment_id": "task20-frozen-i3d-pooled-mlp-v1",
            "model": {"id": "frozen_i3d_pooled_mlp", "family": "frozen_feature_mlp"},
            "fit_scope": "train_only",
            "split_scheme": "group_by_video_v1",
            "evaluation_split": args.eval_split,
            "seed": args.seed,
            "attempt": args.attempt,
            "started_at": started_at,
            "ended_at": ended_at,
            "status": "COMPLETED",
            "termination": "early_stopping_or_frozen_max_epochs",
            "git": {"commit": args.git_commit, "dirty": args.git_dirty},
            "config": {"file": args.tuning_plan.name, "sha256": sha256(args.tuning_plan)},
            "inputs": input_rows,
            "code": [
                artifact_entry(Path(__file__).resolve()),
                artifact_entry((ROOT / "scripts" / "task20_training.py").resolve()),
                artifact_entry((ROOT / "scripts" / "task20_models.py").resolve()),
                artifact_entry((ROOT / "scripts" / "task20_metrics.py").resolve()),
                artifact_entry((ROOT / "scripts" / "task20_evaluation.py").resolve()),
            ],
            "artifacts": [artifact_entry(path) for path in artifacts],
            "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
            "redistribution": "PROHIBITED",
            "test_adaptation": False,
            "smoke": args.smoke,
        }
        (output_dir / "run-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"run_id": manifest["run_id"], "status": "COMPLETED", "metrics": evaluation_metrics}, sort_keys=True))
        return 0
    except Exception as error:
        failure = {
            "schema_version": "task20-failure-v1",
            "status": "FAILED",
            "started_at": started_at,
            "ended_at": now(),
            "failure_class": type(error).__name__,
            "message": str(error),
        }
        (output_dir / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
