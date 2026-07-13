from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GroupShuffleSplit, StratifiedKFold, cross_val_predict, train_test_split


CODE_DIR = Path(r"D:\李佳怡毕业论文配套代码\模型和代码")
DATA_DIR = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\catboost_diagnosis")
sys.path.insert(0, str(CODE_DIR))
from data_loader import load_dataset  # noqa: E402


def model(seed=42, **kw):
    params = dict(
        iterations=1000,
        loss_function="Logloss",
        eval_metric="Accuracy",
        random_seed=seed,
        allow_writing_files=False,
        verbose=False,
        thread_count=-1,
    )
    params.update(kw)
    return CatBoostClassifier(**params)


def metrics(y, pred):
    report = classification_report(y, pred, zero_division=0, output_dict=True)
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "positive_precision": float(precision_score(y, pred, zero_division=0)),
        "positive_recall": float(recall_score(y, pred, zero_division=0)),
        "positive_f1": float(f1_score(y, pred, zero_division=0)),
        "macro_precision": report["macro avg"]["precision"],
        "macro_recall": report["macro avg"]["recall"],
        "macro_f1": report["macro avg"]["f1-score"],
        "weighted_precision": report["weighted avg"]["precision"],
        "weighted_recall": report["weighted avg"]["recall"],
        "weighted_f1": report["weighted avg"]["f1-score"],
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def fit_eval(x, y, train_idx, test_idx, seed=42, **kw):
    clf = model(seed, **kw)
    clf.fit(x[train_idx], y[train_idx])
    return metrics(y[test_idx], clf.predict(x[test_idx]).astype(int).ravel())


def parse_groups(row_ids):
    topics, publishers = [], []
    for rid in row_ids:
        parts = rid.split("::", 1)[0].replace("/", "\\").split("\\")
        topics.append(parts[0] if parts else "")
        publishers.append("\\".join(parts[:2]) if len(parts) >= 2 else topics[-1])
    return np.array(topics), np.array(publishers)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ds = load_dataset(DATA_DIR)
    x, y = ds.features, ds.labels
    topics, publishers = parse_groups(ds.row_ids)
    base = {
        "dataset": ds.report,
        "topic_groups": dict(Counter(topics)),
        "publisher_groups": len(set(publishers)),
    }

    seeds = list(range(50))
    multi_seed = []
    for seed in seeds:
        tr, te = train_test_split(np.arange(len(y)), test_size=0.2, random_state=seed, stratify=y)
        multi_seed.append({"seed": seed, **fit_eval(x, y, tr, te, seed=seed)})

    kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_pred = cross_val_predict(model(42), x, y, cv=kfold, n_jobs=1)
    cv_metrics = metrics(y, cv_pred.astype(int).ravel())

    grouped = {}
    for name, groups in [("topic", topics), ("publisher", publishers)]:
        splitter = GroupShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
        rows = []
        for i, (tr, te) in enumerate(splitter.split(x, y, groups)):
            rows.append({"split": i, "test_size": int(len(te)), **fit_eval(x, y, tr, te, seed=42)})
        grouped[name] = rows

    tuned_grid = [
        {"depth": 4, "learning_rate": 0.03, "l2_leaf_reg": 3, "iterations": 1200},
        {"depth": 6, "learning_rate": 0.03, "l2_leaf_reg": 3, "iterations": 1200},
        {"depth": 8, "learning_rate": 0.02, "l2_leaf_reg": 5, "iterations": 1500},
        {"depth": 10, "learning_rate": 0.02, "l2_leaf_reg": 7, "iterations": 1500},
        {"depth": 6, "learning_rate": 0.05, "l2_leaf_reg": 1, "iterations": 1000},
    ]
    tuned = []
    tr, te = train_test_split(np.arange(len(y)), test_size=0.2, random_state=42, stratify=y)
    for params in tuned_grid:
        tuned.append({"params": params, **fit_eval(x, y, tr, te, seed=42, **params)})

    result = {
        **base,
        "multi_seed_random_split": multi_seed,
        "stratified_5fold_cv": cv_metrics,
        "grouped_splits": grouped,
        "tuned_on_seed42_split": tuned,
    }
    (OUT / "catboost_diagnosis_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    def summarize(rows, key):
        vals = np.array([r[key] for r in rows], dtype=float)
        return {"mean": float(vals.mean()), "std": float(vals.std()), "min": float(vals.min()), "max": float(vals.max())}

    summary = {
        "multi_seed_random_split": {k: summarize(multi_seed, k) for k in ["accuracy", "positive_precision", "positive_recall", "positive_f1", "weighted_f1"]},
        "best_random_seed_by_accuracy": max(multi_seed, key=lambda r: r["accuracy"]),
        "stratified_5fold_cv": cv_metrics,
        "grouped_topic": {k: summarize(grouped["topic"], k) for k in ["accuracy", "positive_f1", "weighted_f1"]},
        "grouped_publisher": {k: summarize(grouped["publisher"], k) for k in ["accuracy", "positive_f1", "weighted_f1"]},
        "best_tuned_by_accuracy": max(tuned, key=lambda r: r["accuracy"]),
        "best_tuned_by_positive_f1": max(tuned, key=lambda r: r["positive_f1"]),
    }
    (OUT / "catboost_diagnosis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
