from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
LLM = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student\llm_annotations.jsonl")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\catboost_llm_temporal")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
LLM_KEYS = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def read_cached() -> dict[str, dict[str, float]]:
    return {obj["bv"]: obj["annotation"] for obj in map(json.loads, LLM.read_text(encoding="utf-8").splitlines())}


def read_timestamps(folder: Path) -> dict[str, int]:
    files = list(folder.glob("6*.csv"))
    if not files:
        return {}
    out = {}
    with files[0].open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            key = bv(row.get("视频地址", "") or row.get("瑙嗛鍦板潃", ""))
            try:
                ts = int(float(row.get("发布时间", "") or row.get("鍙戝竷鏃堕棿", "") or 0))
            except ValueError:
                ts = 0
            if key and ts:
                out[key] = ts
    return out


def load_nodes(cached: dict[str, dict[str, float]]):
    nodes, seen = [], set()
    for vec in sorted(DATA.rglob("5*.csv")):
        rel = vec.relative_to(DATA)
        publisher = "/".join(rel.parts[:2])
        timestamps = read_timestamps(vec.parent)
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for order, row in enumerate(reader):
                if len(row) < FEATURE_COUNT + 2:
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                if key not in cached or key in seen:
                    continue
                try:
                    x48 = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                y = row[FEATURE_COUNT].strip()
                if y not in {"0", "1"} or not all(math.isfinite(v) for v in x48):
                    continue
                xllm = [float(cached[key].get(k, 0.0)) for k in LLM_KEYS]
                nodes.append({"bv": key, "x48": x48, "xllm": xllm, "y": int(y), "publisher": publisher, "timestamp": timestamps.get(key, 0), "order": order})
                seen.add(key)
    return sorted(nodes, key=lambda n: n["bv"])


def temporal_features(nodes, base_x: np.ndarray, window: int = 10) -> np.ndarray:
    by_pub = defaultdict(list)
    for i, n in enumerate(nodes):
        by_pub[n["publisher"]].append((n["timestamp"], n["order"], i))
    out = np.zeros((len(nodes), base_x.shape[1] * 2 + 3), dtype=np.float32)
    for items in by_pub.values():
        items = sorted(items)
        for pos, (ts, _, idx) in enumerate(items):
            prev = [j for _, _, j in items[max(0, pos - window):pos]]
            if not prev:
                continue
            hist = base_x[prev]
            mean = hist.mean(axis=0)
            last_ts = items[pos - 1][0]
            gap_days = max(0.0, (ts - last_ts) / 86400.0) if ts and last_ts else 0.0
            out[idx] = np.concatenate([
                mean,
                base_x[idx] - mean,
                np.asarray([len(prev) / window, 1.0, math.log1p(gap_days)], dtype=np.float32),
            ])
    return out


def metric(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def eval_catboost(x: np.ndarray, y: np.ndarray):
    train, test = train_test_split(np.arange(len(y)), test_size=0.3, random_state=42, stratify=y)
    runs = []
    for seed in SEEDS:
        clf = CatBoostClassifier(
            iterations=300,
            loss_function="Logloss",
            eval_metric="Accuracy",
            random_seed=seed,
            allow_writing_files=False,
            verbose=False,
        )
        clf.fit(x[train], y[train])
        runs.append(metric(y[test], clf.predict(x[test]).astype(int).ravel()))
    return {
        "runs": runs,
        "summary": {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in ["accuracy", "precision", "recall", "f1"]},
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes(read_cached())
    x48 = np.asarray([n["x48"] for n in nodes], dtype=np.float32)
    xllm = np.asarray([n["xllm"] for n in nodes], dtype=np.float32)
    x55 = np.concatenate([x48, xllm], axis=1)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    t48 = temporal_features(nodes, x48)
    t55 = temporal_features(nodes, x55)
    result = {
        "note": "CatBoost with StepFun LLM emotion features and causal publisher-history temporal aggregation. No historical labels are used.",
        "usable_videos": int(len(nodes)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "feature_dims": {
            "base_48": int(x48.shape[1]),
            "llm": int(xllm.shape[1]),
            "temporal_48": int(t48.shape[1]),
            "temporal_48_plus_llm": int(t55.shape[1]),
        },
        "base_48": eval_catboost(x48, y),
        "base_48_plus_llm": eval_catboost(x55, y),
        "base_48_plus_temporal": eval_catboost(np.concatenate([x48, t48], axis=1), y),
        "base_48_plus_llm_plus_temporal": eval_catboost(np.concatenate([x55, t55], axis=1), y),
    }
    (OUT / "catboost_llm_temporal_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
