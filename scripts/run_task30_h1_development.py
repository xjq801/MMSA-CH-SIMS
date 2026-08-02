"""Development-only Task30 H1 runner; formal test is intentionally unreachable."""
from __future__ import annotations

import argparse
import itertools
from dataclasses import asdict
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from typing import Dict, List

import numpy as np
import torch

from task20_metrics import per_sample_jensen_shannon
from load_csmv_i3d import load_by_video_file_id
from task30_data import (
    derive_train_only_privileged_inputs,
    load_pooled_content_features,
    make_mismatched_privileged_features,
    stable_csmv_item_id,
)
from task30_training import fit_teacher_train_logits
from task30_training import StudentTrialConfig
from task30_training import train_student_trial


def validate_development_policy(evaluation_split: str) -> None:
    if evaluation_split != "dev":
        raise ValueError("Task30 development permits dev only; formal test is unreachable")


def load_canonical_train_dev(labels_path: Path, class_order) -> Dict[str, object]:
    classes = tuple(str(value) for value in class_order)
    if len(classes) < 2 or len(set(classes)) != len(classes):
        raise ValueError("class_order must contain unique labels")
    output = {
        "train_ids": [], "train_targets": [],
        "dev_ids": [], "dev_targets": [], "dev_response_counts": [],
    }
    seen = set()
    with Path(labels_path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            row = json.loads(line)
            split_map = row.get("split")
            if not isinstance(split_map, dict) or "group_by_video_v1" not in split_map:
                raise ValueError("canonical row missing frozen split")
            split = split_map["group_by_video_v1"]
            if split not in {"train", "dev", "test"}:
                raise ValueError("unknown canonical split")
            if split == "test":
                continue
            item_id = str(row.get("item_id", ""))
            if not item_id or item_id in seen:
                raise ValueError("canonical train/dev item IDs must be unique")
            distribution = row.get("emotion_distribution")
            if not isinstance(distribution, dict) or set(distribution) != set(classes):
                raise ValueError("canonical emotion distribution class mismatch")
            target = np.asarray([distribution[label] for label in classes], dtype=np.float64)
            if not np.isfinite(target).all() or (target < 0.0).any() or not np.isclose(target.sum(), 1.0, atol=1e-6):
                raise ValueError("canonical distribution must be finite and normalized")
            response_count = row.get("response_count")
            if not isinstance(response_count, int) or isinstance(response_count, bool) or response_count <= 0:
                raise ValueError("canonical response_count must be a positive integer")
            output[split + "_ids"].append(item_id)
            output[split + "_targets"].append(target.astype(np.float32))
            if split == "dev":
                output["dev_response_counts"].append(response_count)
            seen.add(item_id)
    if not output["train_ids"] or not output["dev_ids"]:
        raise ValueError("canonical train/dev splits must be non-empty")
    output["train_targets"] = np.vstack(output["train_targets"])
    output["dev_targets"] = np.vstack(output["dev_targets"])
    output["dev_response_counts"] = np.asarray(output["dev_response_counts"], dtype=np.int64)
    return output


def student_trial_grid(row_id: str, smoke: bool) -> List[StudentTrialConfig]:
    allowed = {
        "hard_label_student",
        "soft_distribution_student",
        "soft_distribution_student_dirichlet",
        "ordinary_kd_student",
        "comment_privileged_kd_student",
        "mismatched_comment_teacher_control",
    }
    if row_id not in allowed:
        raise ValueError("unknown Task30 development row")
    head = "dirichlet" if row_id == "soft_distribution_student_dirichlet" else "softmax"
    architectures = list(itertools.product((128, 256, 512), (0.1, 0.3), (0.0003, 0.001)))
    kd_schedule = list(itertools.product((1.0, 2.0, 4.0), (0.25, 0.5, 0.75)))
    kd_schedule.extend(kd_schedule[:3])
    rows = [
        StudentTrialConfig(
            hidden_dim=hidden_dim,
            dropout=dropout,
            learning_rate=learning_rate,
            max_epochs=200,
            patience=20,
            batch_size=64,
            head=head,
            temperature=kd_schedule[index][0],
            kd_weight=kd_schedule[index][1],
        )
        for index, (hidden_dim, dropout, learning_rate) in enumerate(architectures)
    ]
    if len(rows) != 12:
        raise RuntimeError("Task30 student grid must contain 12 trials")
    if smoke:
        first = rows[0]
        return [
            StudentTrialConfig(
                hidden_dim=first.hidden_dim,
                dropout=first.dropout,
                learning_rate=first.learning_rate,
                max_epochs=2,
                patience=2,
                batch_size=first.batch_size,
                head=first.head,
                temperature=first.temperature,
                kd_weight=first.kd_weight,
            )
        ]
    return rows


def _parameter_count(model) -> int:
    return int(sum(parameter.numel() for parameter in model.parameters()))


def _teacher_config(smoke: bool) -> Dict[str, object]:
    return {
        "hidden_dim": 128,
        "dropout": 0.3,
        "learning_rate": 0.001,
        "max_epochs": 2 if smoke else 50,
        "batch_size": 64,
    }


def _subgroup_gain(
    dev_targets: np.ndarray,
    baseline_predictions: np.ndarray,
    privileged_predictions: np.ndarray,
    response_counts: np.ndarray,
) -> Dict[str, object]:
    counts = np.asarray(response_counts, dtype=np.int64)
    if counts.shape != (dev_targets.shape[0],) or (counts <= 0).any():
        raise ValueError("dev response counts must be positive and row aligned")
    baseline_js = per_sample_jensen_shannon(dev_targets, baseline_predictions)
    privileged_js = per_sample_jensen_shannon(dev_targets, privileged_predictions)
    gain = baseline_js - privileged_js
    groups = {
        "low_1_2": counts <= 2,
        "medium_3_10": (counts >= 3) & (counts <= 10),
        "high_11_plus": counts >= 11,
    }
    return {
        name: {
            "n": int(mask.sum()),
            "mean_js_gain_vs_soft": float(gain[mask].mean()) if mask.any() else None,
        }
        for name, mask in groups.items()
    }


def run_development_matrix(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    dev_features: np.ndarray,
    dev_targets: np.ndarray,
    privileged_train_features: np.ndarray,
    dev_response_counts: np.ndarray,
    seed: int,
    device: str,
    smoke: bool,
    frozen_configs: Dict[str, Dict[str, object]] = None,
) -> Dict[str, object]:
    train_features = np.asarray(train_features, dtype=np.float32)
    train_targets = np.asarray(train_targets, dtype=np.float32)
    dev_features = np.asarray(dev_features, dtype=np.float32)
    dev_targets = np.asarray(dev_targets, dtype=np.float32)
    privileged_train_features = np.asarray(privileged_train_features, dtype=np.float32)
    if privileged_train_features.ndim != 2 or privileged_train_features.shape[0] != train_features.shape[0]:
        raise ValueError("privileged train features must be row aligned")
    fit_labels = ["train"] * train_features.shape[0]
    teacher_config = _teacher_config(smoke)
    ordinary_teacher = fit_teacher_train_logits(
        train_features, train_targets, fit_labels, privileged_features=None,
        seed=seed + 100, device=device, **teacher_config
    )
    privileged_teacher = fit_teacher_train_logits(
        train_features, train_targets, fit_labels,
        privileged_features=privileged_train_features,
        seed=seed + 200, device=device, **teacher_config
    )
    mismatched_features, mismatch_source_indices = make_mismatched_privileged_features(
        privileged_train_features, seed=seed + 300
    )
    mismatched_teacher = fit_teacher_train_logits(
        train_features, train_targets, fit_labels,
        privileged_features=mismatched_features,
        seed=seed + 200, device=device, **teacher_config
    )
    row_contract = {
        "hard_label_student": ("hard", None),
        "soft_distribution_student": ("soft", None),
        "soft_distribution_student_dirichlet": ("soft", None),
        "ordinary_kd_student": ("kd", ordinary_teacher["train_logits"]),
        "comment_privileged_kd_student": ("kd", privileged_teacher["train_logits"]),
        "mismatched_comment_teacher_control": ("kd", mismatched_teacher["train_logits"]),
    }
    rows = {}
    for row_id, (supervision, teacher_logits) in row_contract.items():
        trials = []
        selected = None
        selected_key = None
        if frozen_configs is None:
            configs = student_trial_grid(row_id, smoke)
        else:
            if set(frozen_configs) != set(row_contract):
                raise ValueError("frozen selection must cover every Task30 development row exactly")
            config = StudentTrialConfig(**frozen_configs[row_id])
            expected_head = "dirichlet" if row_id == "soft_distribution_student_dirichlet" else "softmax"
            if config.head != expected_head:
                raise ValueError("frozen selection head does not match development row")
            configs = [config]
        for trial_index, config in enumerate(configs, 1):
            result = train_student_trial(
                train_features, train_targets, fit_labels,
                dev_features, dev_targets, supervision=supervision,
                config=config, seed=seed, device=device,
                teacher_train_logits=teacher_logits,
            )
            parameter_count = _parameter_count(result["model"])
            trial = {
                "trial": trial_index,
                "config": asdict(config),
                "best_epoch": result["best_epoch"],
                "epochs_ran": result["epochs_ran"],
                "parameter_count": parameter_count,
                "metrics": result["dev_metrics"],
                "maximum_gradient_norm": float(max(row["max_gradient_norm"] for row in result["history"])),
            }
            trials.append(trial)
            metrics = result["dev_metrics"]
            key = (
                metrics["jensen_shannon_divergence"],
                metrics["negative_log_likelihood"],
                metrics["brier_score"],
                parameter_count,
                trial_index,
            )
            if selected_key is None or key < selected_key:
                selected_key = key
                selected = (trial, result["dev_predictions"])
        if selected is None:
            raise RuntimeError("development row produced no selectable trial")
        rows[row_id] = {
            "trials": trials,
            "selected_trial": selected[0]["trial"],
            "selected_config": selected[0]["config"],
            "dev_metrics": selected[0]["metrics"],
            "dev_predictions": selected[1],
        }
    subgroup = _subgroup_gain(
        dev_targets,
        rows["soft_distribution_student"]["dev_predictions"],
        rows["comment_privileged_kd_student"]["dev_predictions"],
        dev_response_counts,
    )
    return {
        "schema_version": "task30-h1-development-result-v1",
        "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
        "selection_identity": (
            "FROZEN_FROM_PRIOR_DEV_SELECTION" if frozen_configs is not None else "SEARCHED_CURRENT_DEV"
        ),
        "device": device,
        "rows": rows,
        "teacher_only_upper_bound": {
            "evaluation_scope": "TRAIN_DIAGNOSTIC_ONLY",
            "deployable": False,
            "metrics": privileged_teacher["train_metrics"],
            "reason": "DEV_TEST_RESPONSES_UNREACHABLE_TO_TEACHER",
        },
        "teacher_diagnostics": {
            "ordinary": ordinary_teacher["train_metrics"],
            "privileged": privileged_teacher["train_metrics"],
            "mismatched": mismatched_teacher["train_metrics"],
            "mismatch_fixed_points": int(np.sum(mismatch_source_indices == np.arange(len(mismatch_source_indices)))),
        },
        "subgroup_analysis": {"response_count": subgroup},
        "test_access": "TEST_ROWS_NOT_MATERIALIZED_OR_USED",
    }


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write_json(path: Path, value: Dict[str, object]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_run_bundle(
    output_dir: Path,
    result: Dict[str, object],
    dev_sample_ids,
    dev_targets: np.ndarray,
    class_order,
    seed: int,
    smoke: bool,
    git_commit: str,
    git_dirty: bool,
    source_hashes: Dict[str, str],
) -> Dict[str, object]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=False)
    sample_ids = [str(value) for value in dev_sample_ids]
    targets = np.asarray(dev_targets, dtype=np.float64)
    classes = tuple(str(value) for value in class_order)
    if targets.shape != (len(sample_ids), len(classes)) or len(set(sample_ids)) != len(sample_ids):
        raise ValueError("private prediction rows must be aligned and unique")
    if len(git_commit) != 40 or any(len(str(value)) != 64 for value in source_hashes.values()):
        raise ValueError("run provenance requires full commit and SHA-256 values")
    config = {
        "schema_version": "task30-run-config-v1",
        "master_plan_version": "v1.21",
        "task": "30-M4",
        "hypothesis": "H1",
        "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
        "split_scheme": "group_by_video_v1",
        "evaluation_split": "dev",
        "test_policy": "UNREACHABLE_TASK30_DEVELOPMENT",
        "seed": int(seed),
        "seed_role": "fixed_repro_development",
        "smoke": bool(smoke),
        "device": result["device"],
        "selection_identity": result["selection_identity"],
        "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
        "redistribution": "PROHIBITED",
    }
    _write_json(output / "config.json", config)
    environment = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": np.__version__,
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "dtype": "float32",
        "amp": False,
    }
    _write_json(output / "environment.json", environment)
    aggregate_rows = {}
    raw_metric_lines = []
    for row_id, row in result["rows"].items():
        aggregate_rows[row_id] = {
            "selected_trial": row["selected_trial"],
            "selected_config": row["selected_config"],
            "dev_metrics": row["dev_metrics"],
            "trial_count": len(row["trials"]),
        }
        for trial in row["trials"]:
            raw_metric_lines.append(
                json.dumps({"row_id": row_id, **trial}, ensure_ascii=False, sort_keys=True)
            )
    (output / "raw_metrics.jsonl").write_text("\n".join(raw_metric_lines) + "\n", encoding="utf-8")
    aggregate = {
        "schema_version": result["schema_version"],
        "evidence_identity": result["evidence_identity"],
        "selection_identity": result["selection_identity"],
        "rows": aggregate_rows,
        "teacher_only_upper_bound": result["teacher_only_upper_bound"],
        "teacher_diagnostics": result["teacher_diagnostics"],
        "subgroup_analysis": result["subgroup_analysis"],
        "test_access": result["test_access"],
        "privacy_boundary": "AGGREGATES_ONLY_NO_SAMPLE_IDS_OR_PREDICTION_ROWS",
    }
    _write_json(output / "aggregate_summary.json", aggregate)
    prediction_path = output / "predictions.csv"
    fieldnames = ["sample_id"]
    fieldnames.extend("target_{}".format(label) for label in classes)
    for row_id in result["rows"]:
        fieldnames.extend("prediction_{}_{}".format(row_id, label) for label in classes)
    with prediction_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, sample_id in enumerate(sample_ids):
            row = {"sample_id": sample_id}
            for class_index, label in enumerate(classes):
                row["target_{}".format(label)] = float(targets[index, class_index])
            for row_id, row_result in result["rows"].items():
                predictions = np.asarray(row_result["dev_predictions"], dtype=np.float64)
                for class_index, label in enumerate(classes):
                    row["prediction_{}_{}".format(row_id, label)] = float(predictions[index, class_index])
            writer.writerow(row)
    guardrails = {
        "teacher_fit_scope": "train_only",
        "student_input": "T0_CONTENT_ONLY",
        "dev_selection_only": True,
        "test_rows_materialized": False,
        "mismatch_fixed_points": result["teacher_diagnostics"]["mismatch_fixed_points"],
        "all_prediction_rows_finite_normalized": True,
        "task20_evaluation_core_modified": False,
    }
    _write_json(output / "guardrails.json", guardrails)
    _write_json(
        output / "test_evidence.json",
        {
            "formal_test_policy": "UNREACHABLE_TASK30_DEVELOPMENT",
            "test_rows_materialized": False,
            "test_used_for_selection_calibration_threshold_early_stopping": False,
        },
    )
    (output / "stdout.log").write_text(
        json.dumps({"status": "COMPLETED", "row_count": len(result["rows"])}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output / "stderr.log").write_text("", encoding="utf-8")
    artifact_names = [
        "config.json", "environment.json", "stdout.log", "stderr.log", "raw_metrics.jsonl",
        "predictions.csv", "test_evidence.json", "guardrails.json", "aggregate_summary.json",
    ]
    ended_at = _now()
    manifest = {
        "schema_version": "task30-run-manifest-v1",
        "run_id": output.name,
        "status": "COMPLETED",
        "task": "30-M4",
        "hypothesis": "H1",
        "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
        "evaluation_split": "dev",
        "test_adaptation": False,
        "seed": int(seed),
        "smoke": bool(smoke),
        "ended_at": ended_at,
        "git": {"commit": git_commit, "dirty": bool(git_dirty)},
        "inputs": [{"role": role, "sha256": sha} for role, sha in sorted(source_hashes.items())],
        "artifacts": [
            {"file": name, "bytes": (output / name).stat().st_size, "sha256": _file_sha256(output / name)}
            for name in artifact_names
        ],
        "asset_admissibility": "DEFERRED_ACCEPTED_RISK",
        "redistribution": "PROHIBITED",
    }
    _write_json(output / "manifest.json", manifest)
    return manifest


def _restricted_sequence_loader(video_map_path: Path, feature_root: Path):
    video_map = json.loads(Path(video_map_path).read_text(encoding="utf-8"))
    if not isinstance(video_map, dict):
        raise ValueError("video map must contain an object")
    lookup = {}
    for raw_video_id in video_map:
        item_id = stable_csmv_item_id(str(raw_video_id))
        raw_stem = Path(str(raw_video_id)).stem
        if item_id in lookup:
            raise ValueError("duplicate canonical video mapping")
        lookup[item_id] = raw_stem

    def load_sequence(item_id: str) -> np.ndarray:
        if item_id not in lookup:
            raise KeyError("unknown canonical CSMV item_id")
        return load_by_video_file_id(lookup[item_id], Path(feature_root))

    return load_sequence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--video-map", type=Path, required=True)
    parser.add_argument("--annotation-archive", type=Path, required=True)
    parser.add_argument("--feature-root", type=Path, required=True)
    parser.add_argument("--i3d-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--git-commit", required=True)
    parser.add_argument("--git-dirty", action="store_true")
    parser.add_argument("--selection-summary", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    validate_development_policy("dev")
    if os.environ.get("TASK30_ALLOW_TEST"):
        raise ValueError("TASK30_ALLOW_TEST is forbidden; Task30 development has no test override")
    classes = ("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust")
    canonical = load_canonical_train_dev(args.labels, classes)
    privileged = derive_train_only_privileged_inputs(
        args.labels, args.video_map, args.annotation_archive, classes
    )
    privileged_by_id = {
        sample_id: privileged["privileged_features"][index]
        for index, sample_id in enumerate(privileged["sample_ids"])
    }
    missing = sorted(set(canonical["train_ids"]) - set(privileged_by_id))
    if missing:
        raise ValueError("formal train content lacks privileged response aggregates")
    privileged_matrix = np.vstack([privileged_by_id[item_id] for item_id in canonical["train_ids"]]).astype(np.float32)
    train_ids = list(canonical["train_ids"])
    train_targets = canonical["train_targets"]
    dev_ids = list(canonical["dev_ids"])
    dev_targets = canonical["dev_targets"]
    dev_response_counts = canonical["dev_response_counts"]
    if args.smoke:
        train_count = min(128, len(train_ids))
        dev_count = min(64, len(dev_ids))
        train_ids = train_ids[:train_count]
        train_targets = train_targets[:train_count]
        privileged_matrix = privileged_matrix[:train_count]
        dev_ids = dev_ids[:dev_count]
        dev_targets = dev_targets[:dev_count]
        dev_response_counts = dev_response_counts[:dev_count]
    load_sequence = _restricted_sequence_loader(args.video_map, args.feature_root)
    train_features = load_pooled_content_features(train_ids, load_sequence)
    dev_features = load_pooled_content_features(dev_ids, load_sequence)
    frozen_configs = None
    if args.selection_summary is not None:
        frozen_summary = json.loads(args.selection_summary.read_text(encoding="utf-8"))
        if frozen_summary.get("evidence_identity") != "DEVELOPMENT_EVIDENCE_ONLY":
            raise ValueError("selection summary has the wrong evidence identity")
        frozen_configs = {
            row_id: row["selected_config"] for row_id, row in frozen_summary.get("rows", {}).items()
        }
    result = run_development_matrix(
        train_features, train_targets, dev_features, dev_targets,
        privileged_matrix, dev_response_counts,
        seed=args.seed, device=args.device, smoke=args.smoke,
        frozen_configs=frozen_configs,
    )
    source_hashes = dict(privileged["source_hashes"])
    source_hashes["i3d_quarantine_manifest"] = _file_sha256(args.i3d_manifest)
    if args.selection_summary is not None:
        source_hashes["frozen_dev_selection"] = _file_sha256(args.selection_summary)
    manifest = write_run_bundle(
        args.output_dir, result, dev_ids, dev_targets, classes,
        seed=args.seed, smoke=args.smoke,
        git_commit=args.git_commit, git_dirty=args.git_dirty,
        source_hashes=source_hashes,
    )
    summary = {
        "run_id": manifest["run_id"],
        "status": manifest["status"],
        "evidence_identity": manifest["evidence_identity"],
        "smoke": manifest["smoke"],
        "test_adaptation": manifest["test_adaptation"],
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
