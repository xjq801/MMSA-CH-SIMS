"""Run task-20 item 6 as a native, non-T0 legacy compatibility baseline."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
from pathlib import Path
from typing import Any, Mapping

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

from task20_legacy48 import (
    assign_group_splits,
    binary_metrics,
    build_split_manifest,
    expand_grid,
    load_legacy48,
    tune_then_test,
    validate_split_contract,
)


ROOT = Path(__file__).resolve().parents[1]


def _json_write(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _jsonl_write(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "NOT_INSTALLED"


def _git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(ROOT), check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def _positive_probability(model: Any, features: np.ndarray) -> np.ndarray:
    probabilities = np.asarray(model.predict_proba(features), dtype=float)
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise ValueError("binary predict_proba output must have shape [N, 2]")
    return probabilities[:, 1]


def _make_trainer(
    model_id: str,
    *,
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_dev: np.ndarray,
    y_dev: np.ndarray,
    seed: int,
    max_rounds: int,
    patience: int,
):
    if model_id == "legacy_48_catboost":
        from catboost import CatBoostClassifier

        def train(params: Mapping[str, Any]):
            model = CatBoostClassifier(
                iterations=max_rounds,
                loss_function="Logloss",
                eval_metric="Logloss",
                random_seed=seed,
                allow_writing_files=False,
                verbose=False,
                thread_count=-1,
                **dict(params),
            )
            model.fit(
                x_train,
                y_train,
                eval_set=(x_dev, y_dev),
                use_best_model=True,
                early_stopping_rounds=patience,
                verbose=False,
            )
            return model

        return train

    if model_id == "legacy_48_hgb":
        def train(params: Mapping[str, Any]):
            model = HistGradientBoostingClassifier(
                max_iter=max_rounds,
                early_stopping=True,
                validation_fraction=0.1,
                n_iter_no_change=patience,
                random_state=seed,
                **dict(params),
            )
            model.fit(x_train, y_train)
            return model

        return train

    if model_id == "legacy_48_lightgbm":
        import lightgbm as lgb

        def train(params: Mapping[str, Any]):
            model = lgb.LGBMClassifier(
                n_estimators=max_rounds,
                objective="binary",
                random_state=seed,
                n_jobs=-1,
                deterministic=True,
                force_col_wise=True,
                verbosity=-1,
                **dict(params),
            )
            model.fit(
                x_train,
                y_train,
                eval_set=[(x_dev, y_dev)],
                eval_metric="binary_logloss",
                callbacks=[lgb.early_stopping(patience, verbose=False)],
            )
            return model

        return train
    raise ValueError(f"unknown model id: {model_id}")


def _complexity(model_id: str, params: Mapping[str, Any], model: Any) -> float:
    if model_id == "legacy_48_catboost":
        return float(model.tree_count_ * (2 ** int(params["depth"])))
    if model_id == "legacy_48_hgb":
        return float(model.n_iter_ * int(params["max_leaf_nodes"]))
    if model_id == "legacy_48_lightgbm":
        rounds = int(model.best_iteration_ or model.n_estimators)
        return float(rounds * int(params["num_leaves"]))
    raise ValueError(model_id)


def run(args: argparse.Namespace) -> dict[str, Any]:
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if config.get("eligible_for_unified_csmv_table") is not False:
        raise ValueError("legacy rerun must remain ineligible for the unified CSMV table")
    data = load_legacy48(args.data_dir)
    split_config = config["split"]
    splits = assign_group_splits(
        data.groups,
        salt=split_config["salt"],
        train_cut=float(split_config["train_cut"]),
        dev_cut=float(split_config["dev_cut"]),
    )
    split_summary = validate_split_contract(data.labels, data.groups, splits)
    indices = {split: np.flatnonzero(splits == split) for split in ("train", "dev", "test")}
    x_train, y_train = data.features[indices["train"]], data.labels[indices["train"]]
    x_dev, y_dev = data.features[indices["dev"]], data.labels[indices["dev"]]
    x_test, y_test = data.features[indices["test"]], data.labels[indices["test"]]

    args.output.mkdir(parents=True, exist_ok=True)
    _json_write(args.output / "split-manifest.json", build_split_manifest(data.row_ids, data.groups, splits))

    requested_models = set(args.models or [item["id"] for item in config["models"]])
    family_results: dict[str, Any] = {}
    prediction_rows: list[dict[str, Any]] = []
    total_started = time.perf_counter()
    for family in config["models"]:
        model_id = family["id"]
        if model_id not in requested_models:
            continue
        trials = expand_grid(family["space"])
        if len(trials) != int(family["max_trials"]):
            raise ValueError(f"grid for {model_id} does not match frozen max_trials")
        if args.max_trials_per_model is not None:
            trials = trials[: args.max_trials_per_model]

        trainer = _make_trainer(
            model_id,
            x_train=x_train,
            y_train=y_train,
            x_dev=x_dev,
            y_dev=y_dev,
            seed=int(config["model_seed"]),
            max_rounds=int(family["max_rounds"]),
            patience=int(family["patience_rounds"]),
        )
        test_probabilities: list[np.ndarray] = []

        def dev_evaluator(model: Any) -> Mapping[str, float]:
            return binary_metrics(y_dev, _positive_probability(model, x_dev))

        def test_evaluator(model: Any) -> Mapping[str, float]:
            probabilities = _positive_probability(model, x_test)
            test_probabilities.append(probabilities)
            return binary_metrics(y_test, probabilities)

        started = time.perf_counter()
        if args.dev_only:
            def blocked_test(_: Any) -> Mapping[str, float]:
                return {"not_evaluated": 1.0}

            result = tune_then_test(
                trials,
                train_trial=trainer,
                dev_evaluator=dev_evaluator,
                test_evaluator=blocked_test,
                complexity=lambda params, model: _complexity(model_id, params, model),
            )
            result["test_evaluation_calls"] = 0
            result["test_metrics"] = {"status": "NOT_EVALUATED_DEV_ONLY"}
        else:
            result = tune_then_test(
                trials,
                train_trial=trainer,
                dev_evaluator=dev_evaluator,
                test_evaluator=test_evaluator,
                complexity=lambda params, model: _complexity(model_id, params, model),
            )
        result.pop("selected_model")
        result["elapsed_seconds"] = time.perf_counter() - started
        result["executed_trials"] = len(trials)
        family_results[model_id] = result
        if not args.dev_only:
            probabilities = test_probabilities[0]
            for row_index, probability in zip(indices["test"], probabilities):
                prediction_rows.append(
                    {
                        "sample_id": str(data.row_ids[row_index]),
                        "split": "test",
                        "true_native_binary_label": int(data.labels[row_index]),
                        "positive_probability": float(probability),
                        "predicted_label": int(probability >= 0.5),
                        "model_id": model_id,
                        "config_id": config["schema_version"],
                        "evidence_class": config["evidence_class"],
                    }
                )

    if not family_results:
        raise ValueError("no requested model family was found in config")
    status = "DEV_SMOKE_COMPLETED_TEST_NOT_EVALUATED" if args.dev_only else config["reporting"]["status_on_success"]
    result_bundle = {
        "schema_version": "task20-legacy48-result-v1",
        "status": status,
        "evidence_class": config["evidence_class"],
        "eligible_for_unified_csmv_table": False,
        "eligible_for_main_claims": False,
        "task_timepoint": config["task_timepoint"],
        "execution_device": "LOCAL_CPU",
        "dataset": data.report,
        "split": {"id": split_config["id"], "summary": split_summary},
        "families": family_results,
        "elapsed_seconds": time.perf_counter() - total_started,
        "limitations": config["dataset"]["known_limitations"],
    }
    _json_write(args.output / "metrics.json", result_bundle)
    if not args.dev_only:
        _jsonl_write(args.output / "predictions.jsonl", prediction_rows)
    run_manifest = {
        "schema_version": "task20-legacy48-run-manifest-v1",
        "status": status,
        "config_id": config["schema_version"],
        "code_commit_at_run_start": _git_commit(),
        "environment": {
            "python": platform.python_version(),
            "numpy": _version("numpy"),
            "scikit_learn": _version("scikit-learn"),
            "catboost": _version("catboost"),
            "lightgbm": _version("lightgbm"),
        },
        "source_path_recorded": False,
        "historical_numbers_reused": False,
        "test_evaluation_calls": {model: row["test_evaluation_calls"] for model, row in family_results.items()},
    }
    _json_write(args.output / "run-manifest.json", run_manifest)
    hashes = {
        name: _sha256(args.output / name)
        for name in ("metrics.json", "run-manifest.json", "split-manifest.json")
    }
    if not args.dev_only:
        hashes["predictions.jsonl"] = _sha256(args.output / "predictions.jsonl")
    _json_write(args.output / "artifact-hashes.json", hashes)
    return result_bundle


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "task20" / "legacy-48-native-rerun-v1.json",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", nargs="+")
    parser.add_argument("--max-trials-per-model", type=int)
    parser.add_argument("--dev-only", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    output = run(parse_args())
    print(json.dumps(output, ensure_ascii=False, indent=2))
