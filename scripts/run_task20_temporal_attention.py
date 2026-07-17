"""Tune and evaluate minimal temporal attention on frozen full I3D sequences."""
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
from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np
import torch

from load_csmv_i3d import canonical_item_lookup, load_by_video_file_id
from run_task20_pooled_mlp import artifact_entry, now, parameter_count, sha256
from task20_baseline import load_canonical_records
from task20_evaluation import build_prediction_rows, validate_e0_alignment
from task20_metrics import evaluate_distribution_predictions
from task20_training import (
    TemporalTrialConfig,
    predict_temporal_model,
    train_temporal_trial,
)


ROOT = Path(__file__).resolve().parents[1]
CLASS_ORDER = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]


def validate_eval_policy(
    eval_split: str,
    allow_final_test: bool,
    selection_file: Path = None,
    smoke: bool = False,
) -> None:
    if eval_split == "test" and (not allow_final_test or selection_file is None):
        raise ValueError("test requires explicit authorization and a frozen dev selection file")
    if eval_split == "test" and smoke:
        raise ValueError("test evaluation cannot run in smoke mode")
    if eval_split == "dev" and selection_file is not None:
        raise ValueError("dev tuning must use the frozen search space, not an external selection")


def temporal_trial_grid(tuning_plan: Dict[str, object], smoke: bool) -> List[TemporalTrialConfig]:
    family = next(row for row in tuning_plan["model_families"] if row["id"] == "frozen_i3d_temporal_attention")
    space = family["space"]
    maximum = 1 if smoke else int(family["max_trials"])
    max_epochs = 2 if smoke else int(family["early_stopping"]["max_rounds"])
    patience = 2 if smoke else int(family["early_stopping"]["patience_rounds"])
    rows = [
        TemporalTrialConfig(
            hidden_dim=int(hidden_dim),
            dropout=float(dropout),
            learning_rate=float(learning_rate),
            max_epochs=max_epochs,
            patience=patience,
            max_batch_size=64,
            max_padded_steps=16384,
        )
        for hidden_dim, dropout, learning_rate in itertools.product(
            space["hidden_dim"], space["dropout"], space["learning_rate"]
        )
    ]
    if len(rows) != int(family["max_trials"]):
        raise ValueError("temporal attention search space does not equal max_trials")
    return rows[:maximum]


def temporal_config_dict(config: TemporalTrialConfig) -> Dict[str, object]:
    return {
        "hidden_dim": config.hidden_dim,
        "dropout": config.dropout,
        "learning_rate": config.learning_rate,
        "max_epochs": config.max_epochs,
        "patience": config.patience,
        "max_batch_size": config.max_batch_size,
        "max_padded_steps": config.max_padded_steps,
    }


def load_split_records(labels_path: Path, split: str) -> Tuple[List[str], np.ndarray]:
    records = load_canonical_records(
        labels_path,
        split_scheme="group_by_video_v1",
        expected_split=split,
        distribution_field="emotion_distribution",
        class_order=CLASS_ORDER,
    )
    return [record.item_id for record in records], np.vstack([record.target for record in records]).astype(np.float32)


def limit_smoke_records(
    item_ids: Sequence[str],
    targets: np.ndarray,
    limit: int,
) -> Tuple[List[str], np.ndarray]:
    normalized_ids = [str(item_id) for item_id in item_ids]
    matrix = np.asarray(targets, dtype=np.float32)
    if limit < 1 or matrix.ndim != 2 or len(normalized_ids) != matrix.shape[0]:
        raise ValueError("invalid smoke subset input")
    count = min(limit, len(normalized_ids))
    return normalized_ids[:count], matrix[:count].copy()


def memoize_sequence_loader(source: Callable[[str], np.ndarray]) -> Callable[[str], np.ndarray]:
    """Keep restricted sequences in process memory to avoid repeated file opens."""
    cache: Dict[str, np.ndarray] = {}

    def load_sequence(item_id: str) -> np.ndarray:
        key = str(item_id)
        if key not in cache:
            sequence = np.array(source(key), dtype=np.float32, copy=True)
            sequence.setflags(write=False)
            cache[key] = sequence
        return cache[key]

    return load_sequence


def build_sequence_loader() -> Callable[[str], np.ndarray]:
    lookup = canonical_item_lookup()

    def load_from_restricted_asset(item_id: str) -> np.ndarray:
        if item_id not in lookup:
            raise KeyError("unknown canonical CSMV item_id")
        return load_by_video_file_id(lookup[item_id])

    return memoize_sequence_loader(load_from_restricted_asset)


def fit_temporal_for_evaluation(
    train_ids: Sequence[str],
    train_targets: np.ndarray,
    dev_ids: Sequence[str],
    dev_targets: np.ndarray,
    eval_ids: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
    config: TemporalTrialConfig,
    seed: int,
    device: str,
) -> Tuple[Dict[str, object], np.ndarray]:
    result = train_temporal_trial(
        train_ids,
        train_targets,
        ["train"] * len(train_ids),
        dev_ids,
        dev_targets,
        load_sequence,
        config,
        seed=seed,
        device=device,
    )
    predictions = predict_temporal_model(
        result["model"],
        result["standardizer"],
        eval_ids,
        load_sequence,
        config,
        device,
        dev_targets.shape[1],
    )
    return result, predictions


def main() -> int:
    parser = argparse.ArgumentParser()
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
    validate_eval_policy(args.eval_split, args.allow_final_test, args.selection_file, smoke=args.smoke)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    started_at = now()
    try:
        tuning_plan = json.loads(args.tuning_plan.read_text(encoding="utf-8"))
        train_ids, train_targets = load_split_records(args.labels, "train")
        eval_ids, eval_targets = load_split_records(args.labels, args.eval_split)
        if args.eval_split == "test":
            dev_ids, dev_targets = load_split_records(args.labels, "dev")
        else:
            dev_ids, dev_targets = eval_ids, eval_targets
        if args.smoke:
            train_ids, train_targets = limit_smoke_records(train_ids, train_targets, limit=32)
            dev_ids, dev_targets = limit_smoke_records(dev_ids, dev_targets, limit=16)
            eval_ids, eval_targets = dev_ids, dev_targets
        load_sequence = build_sequence_loader()

        if args.selection_file is None:
            configs = temporal_trial_grid(tuning_plan, args.smoke)
        else:
            frozen = json.loads(args.selection_file.read_text(encoding="utf-8"))["selected_config"]
            configs = [TemporalTrialConfig(**frozen)]
        trials = []
        selected = None
        selected_key = None
        for index, config in enumerate(configs, 1):
            if args.eval_split == "test":
                result, eval_predictions = fit_temporal_for_evaluation(
                    train_ids,
                    train_targets,
                    dev_ids,
                    dev_targets,
                    eval_ids,
                    load_sequence,
                    config,
                    seed=args.seed,
                    device=args.device,
                )
            else:
                result = train_temporal_trial(
                    train_ids,
                    train_targets,
                    ["train"] * len(train_ids),
                    dev_ids,
                    dev_targets,
                    load_sequence,
                    config,
                    seed=args.seed,
                    device=args.device,
                )
                eval_predictions = result["dev_predictions"]
            params = parameter_count(result["model"])
            row = {
                "trial": index,
                "config": temporal_config_dict(config),
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
            model_id="frozen_i3d_temporal_attention",
            config_id="task20-frozen-i3d-temporal-attention-v1",
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
            "selected_config": temporal_config_dict(selected_config),
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
            "sequence_protocol": "FULL_SEQUENCE_DYNAMIC_PADDING_MASK",
            "max_padded_steps": selected_config.max_padded_steps,
        }
        environment_path.write_text(json.dumps(environment, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        artifacts = [predictions_path, metrics_path, trials_path, selection_path, model_path, standardizer_path, environment_path]
        protocol_manifest = ROOT / "data" / "manifests" / "csmv-i3d-sequence-protocol-v1.manifest.json"
        quarantine_manifest = ROOT / "data" / "manifests" / "csmv-i3d-quarantine-v1.manifest.json"
        input_rows = [
            {"role": "canonical_labels", "sha256": sha256(args.labels), "file": args.labels.name},
            {"role": "tuning_plan", "sha256": sha256(args.tuning_plan), "file": args.tuning_plan.name},
            {"role": "i3d_sequence_protocol", "sha256": sha256(protocol_manifest), "file": protocol_manifest.name},
            {"role": "restricted_i3d_quarantine_manifest", "sha256": sha256(quarantine_manifest), "file": quarantine_manifest.name},
        ]
        if args.selection_file is not None:
            input_rows.append(
                {"role": "frozen_dev_selection", "sha256": sha256(args.selection_file), "file": args.selection_file.name}
            )
        ended_at = now()
        manifest = {
            "schema_version": "task20-run-manifest-v1",
            "run_id": output_dir.name,
            "experiment_id": "task20-frozen-i3d-temporal-attention-v1",
            "model": {"id": "frozen_i3d_temporal_attention", "family": "strong_visual_baseline"},
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
                artifact_entry((ROOT / "scripts" / "load_csmv_i3d.py").resolve()),
                artifact_entry((ROOT / "scripts" / "csmv_i3d_sequence_protocol.py").resolve()),
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
