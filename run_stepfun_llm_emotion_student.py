from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student")
FEATURE_COUNT = 48
csv.field_size_limit(10_000_000)
SEEDS = [1111, 1112, 1113]
POS = "好棒赞强赢牛爱笑哈哈支持舒服优秀精彩巅峰希望喜欢感动快乐开心".split()
NEG = "差烂输骂滚蠢废惨哭怒气失望遗憾恶心垃圾离谱崩溃翻车攻击".split()
ATTACK = "傻逼垃圾废物滚闭嘴脑残恶心弱智".split()
SARC = ["doge", "笑死", "呵呵", "妙啊", "典", "绷", "乐"]


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def read_comments(folder: Path) -> dict[str, list[tuple[str, float]]]:
    rows = defaultdict(list)
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
                comment = (row.get("评论内容", "") or "").strip()
                if comment:
                    rows[key].append((comment, like))
    return rows


def rule_score(text: str) -> dict[str, float]:
    text = text or ""
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


def aggregate_rule(comments: list[tuple[str, float]]) -> dict[str, float]:
    keys = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]
    if not comments:
        return {k: 0.0 for k in keys}
    weights = np.asarray([math.log1p(max(like, 0.0)) for _, like in comments], dtype=np.float64)
    weights = weights / weights.sum() if weights.sum() > 0 else np.ones(len(comments)) / len(comments)
    scores = [rule_score(text) for text, _ in comments]
    return {k: float(sum(score[k] * weights[i] for i, score in enumerate(scores))) for k in keys}


def load_candidates(limit: int):
    rows = []
    per_label = {0: limit // 2, 1: limit - limit // 2}
    for vec in sorted(DATA.rglob("5*.csv")):
        if all(sum(r["y"] == label for r in rows) >= per_label[label] for label in [0, 1]):
            break
        comments = read_comments(vec.parent)
        topic = vec.relative_to(DATA).parts[0]
        publisher = vec.relative_to(DATA).parts[1]
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < FEATURE_COUNT + 2:
                    continue
                try:
                    base = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                label = row[FEATURE_COUNT].strip()
                key = row[FEATURE_COUNT + 1].strip()
                if label not in {"0", "1"} or not key or key not in comments:
                    continue
                if not all(math.isfinite(v) for v in base):
                    continue
                y = int(label)
                if sum(r["y"] == y for r in rows) >= per_label[y]:
                    continue
                top_comments = sorted(comments[key], key=lambda x: x[1], reverse=True)[:4]
                rows.append({
                    "topic": topic,
                    "publisher": publisher,
                    "bv": key,
                    "x": base,
                    "y": y,
                    "comments": top_comments,
                })
    return rows


def extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError(f"No JSON found: {text[:200]}")
    return json.loads(m.group(0))


def call_stepfun(api_key: str, model: str, comments: list[tuple[str, float]]) -> dict:
    comment_text = "\n".join(
        f"{i+1}. [like={int(like)}] {text[:160]}"
        for i, (text, like) in enumerate(comments)
    )
    prompt = f"""Analyze these Chinese Bilibili comments as group-emotion evidence.
Return only one strict JSON object immediately. No markdown. No explanation. Do not reason step by step.
All values must be numbers between 0 and 1.
Required keys:
polarity_pos, polarity_neg, intensity, aggressiveness, sarcasm, controversy, confidence.

Comments:
{comment_text}
"""
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return strict JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 4000,
    }
    req = urllib.request.Request(
        "https://api.stepfun.com/step_plan/v1/chat/completions",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    parsed = extract_json(content)
    return {k: float(parsed.get(k, 0.0)) for k in [
        "polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"
    ]}


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def train_eval(x, y, seed):
    tr, te = train_test_split(np.arange(len(y)), test_size=0.3, random_state=42, stratify=y)
    clf = CatBoostClassifier(
        iterations=300,
        loss_function="Logloss",
        eval_metric="Accuracy",
        random_seed=seed,
        allow_writing_files=False,
        verbose=False,
        thread_count=-1,
    )
    clf.fit(x[tr], y[tr])
    return metrics(y[te], clf.predict(x[te]).astype(int).ravel())


def eval_many(x, y):
    runs = [train_eval(x, y, seed) for seed in SEEDS]
    keys = ["accuracy", "precision", "recall", "f1"]
    return {
        "runs": runs,
        "summary": {
            k: {
                "mean": float(np.mean([r[k] for r in runs])),
                "std": float(np.std([r[k] for r in runs])),
            }
            for k in keys
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-videos", type=int, default=80)
    parser.add_argument("--model", default="step-3.7-flash")
    parser.add_argument("--sleep", type=float, default=0.2)
    args = parser.parse_args()

    api_key = os.environ.get("STEPFUN_API_KEY")
    if not api_key:
        raise RuntimeError("Please set STEPFUN_API_KEY in environment.")
    OUT.mkdir(parents=True, exist_ok=True)
    cache_path = OUT / "llm_annotations.jsonl"
    cached = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            obj = json.loads(line)
            cached[obj["bv"]] = obj

    selected = load_candidates(args.max_videos)

    with cache_path.open("a", encoding="utf-8") as f:
        for i, row in enumerate(selected, start=1):
            if row["bv"] in cached:
                continue
            last_error = None
            for _ in range(2):
                try:
                    ann = call_stepfun(api_key, args.model, row["comments"])
                    break
                except (urllib.error.HTTPError, urllib.error.URLError, ValueError, KeyError) as e:
                    last_error = e
                    time.sleep(1)
            else:
                print(f"skip {row['bv']}: {last_error}")
                continue
            obj = {"bv": row["bv"], "y": row["y"], "annotation": ann}
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            f.flush()
            cached[row["bv"]] = obj
            print(f"annotated {i}/{len(selected)} {row['bv']}")
            time.sleep(args.sleep)

    usable = [r for r in selected if r["bv"] in cached]
    x_base = np.asarray([r["x"] for r in usable], dtype=np.float32)
    keys = [
        "polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"
    ]
    x_llm = np.asarray([[cached[r["bv"]]["annotation"][k] for k in keys] for r in usable], dtype=np.float32)
    x_rule = np.asarray([[aggregate_rule(r["comments"])[k] for k in keys] for r in usable], dtype=np.float32)
    y = np.asarray([r["y"] for r in usable], dtype=np.int64)
    can_eval = len(set(y)) == 2 and len(y) >= 20
    result = {
        "note": "Small real StepFun LLM emotion-element test; not final paper result.",
        "model": args.model,
        "requested_videos": args.max_videos,
        "usable_videos": int(len(usable)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "base_48": eval_many(x_base, y) if can_eval else None,
        "rule_emotion_only": eval_many(x_rule, y) if can_eval else None,
        "llm_emotion_only": eval_many(x_llm, y) if can_eval else None,
        "base_48_plus_rule": eval_many(np.concatenate([x_base, x_rule], axis=1), y) if can_eval else None,
        "base_48_plus_llm": eval_many(np.concatenate([x_base, x_llm], axis=1), y) if can_eval else None,
    }
    (OUT / "stepfun_llm_student_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
