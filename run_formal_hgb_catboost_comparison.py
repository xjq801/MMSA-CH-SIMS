"""Formal, leakage-aware comparison of HGB and CatBoost on the current main feature set."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import GroupShuffleSplit, StratifiedKFold

ROOT = Path(r"D:\MMSA-CH-SIMS")
sys.path.insert(0, str(ROOT))
import run_bert_text_fusion_experiment as base  # noqa: E402

OUT = ROOT / "experiments" / "formal_hgb_catboost"
SEEDS = [1111, 1112, 1113]


def score(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
    }


def fit_predict(kind, xtr, ytr, xte, seed):
    if kind == "hgb":
        model = HistGradientBoostingClassifier(
            max_iter=300, learning_rate=0.05, l2_regularization=0.1, random_state=seed
        )
    else:
        model = CatBoostClassifier(
            iterations=300, loss_function="Logloss", eval_metric="Accuracy",
            random_seed=seed, allow_writing_files=False, verbose=False,
        )
    model.fit(xtr, ytr)
    return model.predict(xte).astype(int).ravel()


def evaluate_splits(x, y, splits, protocol):
    rows = []
    for split_id, (train, test) in enumerate(splits):
        for kind in ("hgb", "catboost"):
            for seed in SEEDS:
                pred = fit_predict(kind, x[train], y[train], x[test], seed)
                rows.append({"protocol": protocol, "split": split_id, "model": kind, "seed": seed,
                             "n_train": len(train), "n_test": len(test), **score(y[test], pred)})
    return rows


def summarize(rows):
    out = {}
    for model in ("hgb", "catboost"):
        part = [r for r in rows if r["model"] == model]
        out[model] = {
            metric: {"mean": float(np.mean([r[metric] for r in part])),
                     "std": float(np.std([r[metric] for r in part], ddof=1)) if len(part) > 1 else 0.0}
            for metric in ("accuracy", "precision", "recall", "f1")
        }
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = base.load_nodes(base.read_cached_llm())
    x48 = np.asarray([n["x48"] for n in nodes], dtype=np.float32)
    xllm = np.asarray([n["xllm"] for n in nodes], dtype=np.float32)
    x55 = np.concatenate([x48, xllm], axis=1)
    temporal = base.temporal_features(nodes, x55)
    x = np.concatenate([x55, temporal], axis=1).astype(np.float32)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    groups = np.asarray([n["publisher"] for n in nodes])
    timestamps = np.asarray([int(n["timestamp"]) for n in nodes])

    all_rows = []
    # Five-fold stratified CV: primary stability estimate.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=20260710)
    all_rows += evaluate_splits(x, y, list(cv.split(x, y)), "5fold_stratified")

    # Chronological holdout: train on earlier videos, test on later videos.
    order = np.argsort(timestamps)
    cut = int(len(order) * 0.7)
    time_train, time_test = order[:cut], order[cut:]
    all_rows += evaluate_splits(x, y, [(time_train, time_test)], "chronological_70_30")

    # Publisher-held-out evaluation: no publisher appears in both partitions.
    gss = GroupShuffleSplit(n_splits=3, test_size=0.3, random_state=20260710)
    all_rows += evaluate_splits(x, y, list(gss.split(x, y, groups)), "publisher_group_70_30")

    result = {
        "feature_set": "48维 + 7维LLM情绪元 + causal Temporal聚合",
        "usable_videos": int(len(y)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "publisher_count": int(len(set(groups.tolist()))),
        "seeds": SEEDS,
        "protocols": {p: {"rows": len([r for r in all_rows if r["protocol"] == p]),
                          "summary": summarize([r for r in all_rows if r["protocol"] == p])}
                      for p in ("5fold_stratified", "chronological_70_30", "publisher_group_70_30")},
        "raw_rows": all_rows,
    }
    (OUT / "formal_comparison_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["protocols"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
