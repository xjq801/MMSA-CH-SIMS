from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\llm_ready_emotion_student")
FEATURE_COUNT = 48
SEEDS = [42]
csv.field_size_limit(10_000_000)

POS = "好棒赞强赢牛爱笑哈哈支持舒服优秀精彩巅峰希望喜欢感动快乐开心".split()
NEG = "差烂输骂滚蠢废惨哭怒气失望遗憾恶心垃圾离谱崩溃翻车攻击".split()
ATTACK = "傻逼垃圾废物滚闭嘴脑残恶心弱智".split()
SARC = ["doge", "笑死", "呵呵", "妙啊", "典", "绷", "乐"]


def bv(url_or_text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", url_or_text or "")
    return m.group(0) if m else ""


def score_text(text: str) -> dict[str, float]:
    # ponytail: rule weak-labels now; replace this with real LLM JSON output later.
    text = text or ""
    pos = sum(text.count(w) for w in POS)
    neg = sum(text.count(w) for w in NEG)
    attack = sum(text.count(w) for w in ATTACK)
    sarcasm = sum(text.count(w) for w in SARC)
    length = max(len(text), 1)
    polarity = (pos - neg) / (pos + neg + 1)
    intensity = min(1.0, (pos + neg + attack + sarcasm) / 5.0)
    confidence = min(1.0, (pos + neg + attack + sarcasm + 1) / 4.0)
    return {
        "polarity": polarity,
        "intensity": intensity,
        "attack": min(1.0, attack / 2.0),
        "sarcasm": min(1.0, sarcasm / 2.0),
        "confidence": confidence,
        "len": float(length),
        "exclaim": float(text.count("!") + text.count("！")),
        "question": float(text.count("?") + text.count("？")),
    }


def agg(rows: list[tuple[str, float]]) -> list[float]:
    if not rows:
        return [0.0] * 18
    keys = ["polarity", "intensity", "attack", "sarcasm", "confidence", "len", "exclaim", "question"]
    vals = {k: [] for k in keys}
    weights = []
    for text, like in rows:
        s = score_text(text)
        for k in keys:
            vals[k].append(s[k])
        weights.append(math.log1p(max(like, 0.0)))
    weights = np.asarray(weights, dtype=np.float64)
    weights = weights / weights.sum() if weights.sum() > 0 else np.ones(len(rows)) / len(rows)
    feats = []
    for k in keys[:5]:
        arr = np.asarray(vals[k], dtype=np.float64)
        feats.extend([float(arr.mean()), float(arr.std()), float(np.sum(arr * weights))])
    feats.extend([
        float(len(rows)),
        float(np.mean(vals["len"])),
        float(np.mean(vals["exclaim"]) + np.mean(vals["question"])),
    ])
    return feats


def read_comments(folder: Path) -> dict[str, list[tuple[str, float]]]:
    out = defaultdict(list)
    for path in folder.glob("1.评论数据*.csv"):
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            clean_lines = (line.replace("\x00", "") for line in f)
            for row in csv.DictReader(clean_lines, delimiter=";"):
                key = bv(row.get("视频地址", ""))
                if not key:
                    continue
                try:
                    like = float(row.get("评论点赞数", 0) or 0)
                except ValueError:
                    like = 0.0
                out[key].append((row.get("评论内容", ""), like))
    return out


def load_rows():
    xs_base, xs_emotion, ys = [], [], []
    rejected = Counter()
    for vec in sorted(DATA.rglob("5*.csv")):
        comments = read_comments(vec.parent)
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < FEATURE_COUNT + 2:
                    rejected["too_few_columns"] += 1
                    continue
                try:
                    base = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    rejected["non_numeric"] += 1
                    continue
                label = row[FEATURE_COUNT].strip()
                if label not in {"0", "1"} or not all(math.isfinite(v) for v in base):
                    rejected["bad_label_or_feature"] += 1
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                xs_base.append(base)
                xs_emotion.append(agg(comments.get(key, [])))
                ys.append(int(label))
    return np.asarray(xs_base, dtype=np.float32), np.asarray(xs_emotion, dtype=np.float32), np.asarray(ys), dict(rejected)


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def run_once(x, y, seed):
    tr, te = train_test_split(np.arange(len(y)), test_size=0.2, random_state=42, stratify=y)
    clf = CatBoostClassifier(
        iterations=500,
        loss_function="Logloss",
        eval_metric="Accuracy",
        random_seed=seed,
        allow_writing_files=False,
        verbose=False,
        thread_count=-1,
    )
    clf.fit(x[tr], y[tr])
    return metrics(y[te], clf.predict(x[te]).astype(int).ravel())


def summarize(runs):
    keys = ["accuracy", "precision", "recall", "f1"]
    return {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in keys}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    xb, xe, y, rejected = load_rows()
    experiments = {
        "catboost_original_48": xb,
        "emotion_elements_only": xe,
        "original_48_plus_emotion_elements": np.concatenate([xb, xe], axis=1),
    }
    result = {
        "note": "LLM-ready stage-1 prototype. Emotion elements are rule weak-labels now; replace score_text() with LLM annotation later.",
        "rows": int(len(y)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "rejected": rejected,
        "emotion_feature_dim": int(xe.shape[1]),
        "seeds": SEEDS,
        "experiments": {},
    }
    for name, x in experiments.items():
        runs = [run_once(x, y, seed) for seed in SEEDS]
        result["experiments"][name] = {"runs": runs, "summary": summarize(runs)}
    (OUT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["experiments"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
