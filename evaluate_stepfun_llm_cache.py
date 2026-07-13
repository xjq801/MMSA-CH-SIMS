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
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
KEYS = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]
POS = "好棒赞强赢牛爱笑哈哈支持舒服优秀精彩巅峰希望喜欢感动快乐开心".split()
NEG = "差烂输骂滚蠢废惨哭怒气失望遗憾恶心垃圾离谱崩溃翻车攻击".split()
ATTACK = "傻逼垃圾废物滚闭嘴脑残恶心弱智".split()
SARC = ["doge", "笑死", "呵呵", "妙啊", "典", "绷", "乐"]
csv.field_size_limit(10_000_000)


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def rule_score(text: str) -> dict[str, float]:
    pos = sum(text.count(w) for w in POS)
    neg = sum(text.count(w) for w in NEG)
    attack = sum(text.count(w) for w in ATTACK)
    sarcasm = sum(text.count(w) for w in SARC)
    total = pos + neg + attack + sarcasm
    return {
        "polarity_pos": min(1.0, pos / (pos + neg + 1)),
        "polarity_neg": min(1.0, neg / (pos + neg + 1)),
        "intensity": min(1.0, total / 5.0),
        "aggressiveness": min(1.0, attack / 2.0),
        "sarcasm": min(1.0, sarcasm / 2.0),
        "controversy": min(1.0, (neg + attack + sarcasm) / 5.0),
        "confidence": min(1.0, (total + 1) / 4.0),
    }


def read_cached():
    cached = {}
    for line in (OUT / "llm_annotations.jsonl").read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        cached[obj["bv"]] = obj["annotation"]
    return cached


def load_base(cached_bvs: set[str]):
    base = {}
    for vec in sorted(DATA.rglob("5*.csv")):
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < FEATURE_COUNT + 2:
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                if key not in cached_bvs or key in base:
                    continue
                try:
                    x = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                y = row[FEATURE_COUNT].strip()
                if y in {"0", "1"} and all(math.isfinite(v) for v in x):
                    base[key] = (x, int(y))
    return base


def load_rule(cached_bvs: set[str]):
    comments = defaultdict(list)
    remaining = set(cached_bvs)
    for path in DATA.rglob("1.评论数据*.csv"):
        if not remaining:
            break
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            clean = (line.replace("\x00", "") for line in f)
            for row in csv.DictReader(clean, delimiter=";"):
                key = bv(row.get("视频地址", ""))
                if key in remaining:
                    comments[key].append(row.get("评论内容", "") or "")
                    if len(comments[key]) >= 20:
                        remaining.discard(key)
    rule = {}
    for key in cached_bvs:
        rows = comments.get(key, [])
        if not rows:
            rule[key] = {k: 0.0 for k in KEYS}
            continue
        scores = [rule_score(text) for text in rows[:20]]
        rule[key] = {k: float(np.mean([s[k] for s in scores])) for k in KEYS}
    return rule


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def eval_many(x, y):
    runs = []
    tr, te = train_test_split(np.arange(len(y)), test_size=0.3, random_state=42, stratify=y)
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
    rule = load_rule(set(base))
    bvs = sorted(base)
    x_base = np.asarray([base[k][0] for k in bvs], dtype=np.float32)
    y = np.asarray([base[k][1] for k in bvs], dtype=np.int64)
    x_rule = np.asarray([[rule[k][name] for name in KEYS] for k in bvs], dtype=np.float32)
    x_llm = np.asarray([[float(cached[k].get(name, 0.0)) for name in KEYS] for k in bvs], dtype=np.float32)
    result = {
        "note": "Offline evaluation from cached StepFun LLM annotations.",
        "usable_videos": int(len(bvs)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "base_48": eval_many(x_base, y),
        "rule_emotion_only": eval_many(x_rule, y),
        "llm_emotion_only": eval_many(x_llm, y),
        "base_48_plus_rule": eval_many(np.concatenate([x_base, x_rule], axis=1), y),
        "base_48_plus_llm": eval_many(np.concatenate([x_base, x_llm], axis=1), y),
    }
    (OUT / "stepfun_llm_cache_eval_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
