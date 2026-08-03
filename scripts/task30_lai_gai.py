"""LAI-GAI content/calibration boundary; no comment teacher exists by design."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
from typing import Dict, Sequence

import numpy as np
from PIL import Image

from task20_metrics import evaluate_distribution_predictions
from task30_training import StudentTrialConfig, train_student_trial


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _image_features(path: Path) -> np.ndarray:
    try:
        with Image.open(path) as image:
            pixels = np.asarray(image.convert("RGB").resize((32, 32)), dtype=np.float32) / 255.0
    except Exception as error:
        raise ValueError("LAI-GAI T0 image cannot be decoded") from error
    flattened = pixels.reshape(-1, 3)
    features = np.concatenate(
        (
            flattened.mean(axis=0),
            flattened.std(axis=0),
            np.quantile(flattened, 0.25, axis=0),
            np.quantile(flattened, 0.75, axis=0),
        )
    ).astype(np.float32)
    if features.shape != (12,) or not np.isfinite(features).all():
        raise ValueError("LAI-GAI content features must be finite 12-vectors")
    return features


def load_lai_gai_train_dev(
    canonical_path: Path,
    image_root: Path,
    class_order: Sequence[str],
) -> Dict[str, object]:
    classes = tuple(str(value) for value in class_order)
    if len(classes) < 2 or len(set(classes)) != len(classes):
        raise ValueError("LAI-GAI class order must contain unique labels")
    rows = {"train": [], "dev": []}
    seen = set()
    with Path(canonical_path).open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            split = row.get("split")
            if split not in {"train", "dev", "test"}:
                raise ValueError("unknown LAI-GAI split")
            if split == "test":
                continue
            item_id = str(row.get("item_id", ""))
            if not item_id or item_id in seen:
                raise ValueError("LAI-GAI train/dev IDs must be unique")
            if row.get("available_at_t0") is not True or row.get("label_available_at_t0") is not False:
                raise ValueError("LAI-GAI T0 availability contract mismatch")
            distribution = row.get("emotion_distribution")
            if not isinstance(distribution, dict) or set(distribution) != set(classes):
                raise ValueError("LAI-GAI distribution class mismatch")
            target = np.asarray([distribution[label] for label in classes], dtype=np.float64)
            if not np.isfinite(target).all() or (target < 0.0).any() or not np.isclose(target.sum(), 1.0, atol=1e-6):
                raise ValueError("LAI-GAI distribution must be finite and normalized")
            image_path = Path(image_root) / str(row.get("image_name", ""))
            if not image_path.is_file() or _sha256(image_path) != row.get("image_sha256"):
                raise ValueError("LAI-GAI image fixity mismatch")
            rows[split].append((item_id, _image_features(image_path), target.astype(np.float32)))
            seen.add(item_id)
    if not rows["train"] or not rows["dev"]:
        raise ValueError("LAI-GAI train/dev splits must be non-empty")
    return {
        "train_ids": [row[0] for row in rows["train"]],
        "train_features": np.vstack([row[1] for row in rows["train"]]),
        "train_targets": np.vstack([row[2] for row in rows["train"]]),
        "dev_ids": [row[0] for row in rows["dev"]],
        "dev_features": np.vstack([row[1] for row in rows["dev"]]),
        "dev_targets": np.vstack([row[2] for row in rows["dev"]]),
        "applicability": "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE",
        "canonical_sha256": _sha256(Path(canonical_path)),
    }


def _grid(head: str, smoke: bool):
    configs = [
        StudentTrialConfig(
            hidden_dim=hidden, dropout=dropout, learning_rate=learning_rate,
            max_epochs=200, patience=20, batch_size=64, head=head,
            temperature=1.0, kd_weight=0.0,
        )
        for hidden, dropout, learning_rate in itertools.product(
            (128, 256, 512), (0.1, 0.3), (0.0003, 0.001)
        )
    ]
    if smoke:
        first = configs[0]
        return [StudentTrialConfig(**dict(asdict(first), max_epochs=2, patience=2))]
    return configs


def run_lai_gai_boundary(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    dev_features: np.ndarray,
    dev_targets: np.ndarray,
    seed: int,
    device: str,
    smoke: bool,
) -> Dict[str, object]:
    train_targets = np.asarray(train_targets, dtype=np.float32)
    dev_targets = np.asarray(dev_targets, dtype=np.float32)
    mean = train_targets.mean(axis=0, dtype=np.float64)
    mean /= mean.sum()
    rows = {
        "overall_mean": {
            "trial_count": 0,
            "dev_metrics": evaluate_distribution_predictions(
                dev_targets.astype(np.float64), np.repeat(mean[None, :], len(dev_targets), axis=0)
            ),
        }
    }
    for row_id, head in (("content_softmax", "softmax"), ("content_dirichlet", "dirichlet")):
        selected = None
        selected_key = None
        trials = []
        for index, config in enumerate(_grid(head, smoke), 1):
            result = train_student_trial(
                train_features, train_targets, ["train"] * len(train_targets),
                dev_features, dev_targets, supervision="soft", config=config,
                seed=seed, device=device,
            )
            trial = {
                "trial": index, "config": asdict(config),
                "best_epoch": result["best_epoch"], "epochs_ran": result["epochs_ran"],
                "metrics": result["dev_metrics"],
            }
            trials.append(trial)
            metrics = trial["metrics"]
            key = (metrics["jensen_shannon_divergence"], metrics["negative_log_likelihood"], metrics["brier_score"], index)
            if selected_key is None or key < selected_key:
                selected_key = key
                selected = trial
        rows[row_id] = {
            "trial_count": len(trials), "selected_trial": selected["trial"],
            "selected_config": selected["config"], "dev_metrics": selected["metrics"],
        }
    return {
        "schema_version": "task30-lai-gai-content-boundary-v1",
        "evidence_identity": "DEVELOPMENT_BOUNDARY_ONLY",
        "h1_status": "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE",
        "rows": rows,
        "test_access": "TEST_ROWS_NOT_MATERIALIZED_OR_USED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--image-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    classes = (
        "amusement", "awe", "anger", "attachment_love", "craving", "disgust",
        "excitement", "fear", "joy", "neutral", "nurturant_love", "sadness",
    )
    loaded = load_lai_gai_train_dev(args.canonical, args.image_root, classes)
    result = run_lai_gai_boundary(
        loaded["train_features"], loaded["train_targets"], loaded["dev_features"],
        loaded["dev_targets"], seed=args.seed, device=args.device, smoke=args.smoke,
    )
    result["input"] = {
        "canonical_sha256": loaded["canonical_sha256"],
        "train_count": len(loaded["train_ids"]), "dev_count": len(loaded["dev_ids"]),
        "content_features": "FIXED_32X32_RGB_CHANNEL_MEAN_STD_Q25_Q75",
        "comment_fields_used": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "COMPLETED", "h1_status": result["h1_status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
