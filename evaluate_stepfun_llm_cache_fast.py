from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
KEYS = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]


def read_cached():
    cached = {}
    for line in (OUT / "llm_annotations.jsonl").read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        cached[obj["bv"]] = obj["annotation"]
    return cached


def load_base(cached_bvs):
    rows = {}
    for vec in sorted(DATA.rglob("5*.csv")):
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < FEATURE_COUNT + 2:
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                if key not in cached_bvs or key in rows:
                    continue
                try:
                    x = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                y = row[FEATURE_COUNT].strip()
                if y in {"0", "1"} and all(math.isfinite(v) for v in x):
                    rows[key] = (x, int(y))
    return rows


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def eval_many(x, y):
    tr, te = train_test_split(np.arange(len(y)), test_size=0.3, random_state=42, stratify=y)
    runs = []
    for seed in SEEDS:
        clf = CatBoostClassifier(iterations=300, loss_function="Logloss", eval_metric="Accuracy", random_seed=seed, allow_writing_files=False, verbose=False)
        clf.fit(x[tr], y[tr])
        runs.append(metrics(y[te], clf.predict(x[te]).astype(int).ravel()))
    return {
        "runs": runs,
        "summary": {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in ["accuracy", "precision", "recall", "f1"]},
    }


def main():
    cached = read_cached()
    base = load_base(set(cached))
    bvs = sorted(base)
    x_base = np.asarray([base[k][0] for k in bvs], dtype=np.float32)
    x_llm = np.asarray([[float(cached[k].get(name, 0.0)) for name in KEYS] for k in bvs], dtype=np.float32)
    y = np.asarray([base[k][1] for k in bvs], dtype=np.int64)
    result = {
        "note": "Fast offline evaluation from cached StepFun LLM annotations; rule emotion features are reported separately.",
        "usable_videos": int(len(bvs)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "base_48": eval_many(x_base, y),
        "llm_emotion_only": eval_many(x_llm, y),
        "base_48_plus_llm": eval_many(np.concatenate([x_base, x_llm], axis=1), y),
    }
    (OUT / "stepfun_llm_cache_fast_eval_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
