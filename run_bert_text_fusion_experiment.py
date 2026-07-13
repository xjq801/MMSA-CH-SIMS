from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from catboost import CatBoostClassifier
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from transformers import AutoModel, AutoTokenizer


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
LLM = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student\llm_annotations.jsonl")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\bert_text_fusion")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
LLM_KEYS = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]
BERT_MODEL = Path(r"D:\MMSA-CH-SIMS\models\bert-base-chinese")
TEXT_PCA_DIM = 32

csv.field_size_limit(10_000_000)


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def safe_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def read_cached_llm() -> dict[str, dict[str, float]]:
    out = {}
    with LLM.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            out[obj["bv"]] = obj["annotation"]
    return out


def read_video_metadata(folder: Path) -> dict[str, dict[str, object]]:
    files = list(folder.glob("6*.csv"))
    if not files:
        return {}
    meta: dict[str, dict[str, object]] = {}
    with files[0].open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            key = bv(row.get("视频地址", ""))
            if not key:
                continue
            meta[key] = {
                "title": row.get("标题", ""),
                "tags": row.get("标签", ""),
                "intro": row.get("简介", ""),
                "timestamp": int(safe_float(row.get("发布时间", ""), 0.0)),
            }
    return meta


def read_legacy_timestamps(folder: Path) -> dict[str, int]:
    files = list(folder.glob("6*.csv"))
    if not files:
        return {}
    out: dict[str, int] = {}
    with files[0].open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            key = bv(row.get("视频地址", ""))
            ts = int(safe_float(row.get("发布时间", ""), 0.0))
            if key and ts:
                out[key] = ts
    return out


def read_comments(folder: Path) -> tuple[dict[str, list[tuple[float, str]]], dict[str, dict[str, object]]]:
    files = list(folder.glob("1*.csv"))
    comments: dict[str, list[tuple[float, str]]] = defaultdict(list)
    meta: dict[str, dict[str, object]] = {}
    if not files:
        return comments, meta
    with files[0].open("r", encoding="utf-8-sig", newline="") as f:
        clean_lines = (line.replace("\x00", "") for line in f)
        for row in csv.DictReader(clean_lines, delimiter=";"):
            key = bv(row.get("视频地址", ""))
            if not key:
                continue
            if key not in meta:
                meta[key] = {
                    "title": row.get("标题", ""),
                    "tags": row.get("视频标签", ""),
                    "intro": row.get("视频简介", ""),
                    "timestamp": int(safe_float(row.get("发布时间", ""), 0.0)),
                }
            like = safe_float(row.get("评论点赞数", ""), 0.0)
            content = (row.get("评论内容", "") or "").strip()
            if content:
                comments[key].append((like, content))
    return comments, meta


def make_text(meta: dict[str, object], comments: list[tuple[float, str]], top_k: int = 20) -> str:
    top_comments = [text for _, text in sorted(comments, reverse=True)[:top_k]]
    parts = [
        "标题：" + str(meta.get("title", "")),
        "标签：" + str(meta.get("tags", "")),
        "简介：" + str(meta.get("intro", "")),
        "代表评论：" + "；".join(top_comments),
    ]
    text = "\n".join(p for p in parts if p.strip())
    return text[:3000]


def load_nodes(cached: dict[str, dict[str, float]]) -> list[dict[str, object]]:
    nodes, seen = [], set()
    for vec in sorted(DATA.rglob("5*.csv")):
        publisher = "/".join(vec.relative_to(DATA).parts[:2])
        meta = read_video_metadata(vec.parent)
        legacy_timestamps = read_legacy_timestamps(vec.parent)
        comments, comment_meta = read_comments(vec.parent)
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for order, row in enumerate(reader):
                if len(row) < FEATURE_COUNT + 2:
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                if key not in cached or key in seen:
                    continue
                label = row[FEATURE_COUNT].strip()
                if label not in {"0", "1"}:
                    continue
                try:
                    x48 = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                if not all(math.isfinite(v) for v in x48):
                    continue
                video_meta = {**comment_meta.get(key, {}), **meta.get(key, {})}
                nodes.append(
                    {
                        "bv": key,
                        "x48": x48,
                        "xllm": [float(cached[key].get(k, 0.0)) for k in LLM_KEYS],
                        "y": int(label),
                        "publisher": publisher,
                        "timestamp": int(legacy_timestamps.get(key, 0)),
                        "order": order,
                        "text": make_text(video_meta, comments.get(key, [])),
                    }
                )
                seen.add(key)
    return sorted(nodes, key=lambda n: str(n["bv"]))


def temporal_features(nodes: list[dict[str, object]], base_x: np.ndarray, window: int = 10) -> np.ndarray:
    by_pub: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
    for i, n in enumerate(nodes):
        by_pub[str(n["publisher"])].append((int(n["timestamp"]), int(n["order"]), i))
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
            out[idx] = np.concatenate(
                [
                    mean,
                    base_x[idx] - mean,
                    np.asarray([len(prev) / window, 1.0, math.log1p(gap_days)], dtype=np.float32),
                ]
            )
    return out


def embed_texts(texts: list[str]) -> np.ndarray:
    OUT.mkdir(parents=True, exist_ok=True)
    cache = OUT / "bert_text_embeddings.npz"
    if cache.exists():
        data = np.load(cache, allow_pickle=True)
        cached_texts = data["texts"].tolist()
        if cached_texts == texts:
            return data["embeddings"].astype(np.float32)

    tokenizer = AutoTokenizer.from_pretrained(str(BERT_MODEL), local_files_only=True)
    model = AutoModel.from_pretrained(str(BERT_MODEL), local_files_only=True)
    model.eval()
    embs = []
    with torch.no_grad():
        for start in range(0, len(texts), 8):
            batch = texts[start : start + 8]
            encoded = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
            output = model(**encoded)
            mask = encoded["attention_mask"].unsqueeze(-1).float()
            pooled = (output.last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1.0)
            embs.append(pooled.cpu().numpy().astype(np.float32))
    arr = np.concatenate(embs, axis=0)
    np.savez_compressed(cache, texts=np.asarray(texts, dtype=object), embeddings=arr)
    return arr


def metric(y: np.ndarray, pred: np.ndarray) -> dict[str, object]:
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def reduce_text_for_split(x_text: np.ndarray, train: np.ndarray, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(x_text[train])
    test_scaled = scaler.transform(x_text[test])
    n_components = min(TEXT_PCA_DIM, train_scaled.shape[0] - 1, train_scaled.shape[1])
    pca = PCA(n_components=n_components, random_state=42)
    return pca.fit_transform(train_scaled), pca.transform(test_scaled)


def make_split_features(
    x_num: np.ndarray | None, x_text: np.ndarray | None, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    train, test = train_test_split(np.arange(len(y)), test_size=0.3, random_state=42, stratify=y)
    xtr_parts, xte_parts = [], []
    if x_num is not None:
        xtr_parts.append(x_num[train])
        xte_parts.append(x_num[test])
    if x_text is not None:
        text_train, text_test = reduce_text_for_split(x_text, train, test)
        xtr_parts.append(text_train)
        xte_parts.append(text_test)
    xtr = np.concatenate(xtr_parts, axis=1).astype(np.float32)
    xte = np.concatenate(xte_parts, axis=1).astype(np.float32)
    return xtr, xte, y[train], y[test]


def eval_hgb(x_num: np.ndarray | None, x_text: np.ndarray | None, y: np.ndarray) -> dict[str, object]:
    xtr, xte, ytr, yte = make_split_features(x_num, x_text, y)
    runs = []
    for seed in SEEDS:
        clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, l2_regularization=0.1, random_state=seed)
        clf.fit(xtr, ytr)
        runs.append(metric(yte, clf.predict(xte).astype(int)))
    return {
        "runs": runs,
        "summary": {
            k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))}
            for k in ["accuracy", "precision", "recall", "f1"]
        },
    }


def eval_catboost(x_num: np.ndarray | None, x_text: np.ndarray | None, y: np.ndarray) -> dict[str, object]:
    xtr, xte, ytr, yte = make_split_features(x_num, x_text, y)
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
        clf.fit(xtr, ytr)
        runs.append(metric(yte, clf.predict(xte).astype(int).ravel()))
    return {
        "runs": runs,
        "summary": {
            k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))}
            for k in ["accuracy", "precision", "recall", "f1"]
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes(read_cached_llm())
    x48 = np.asarray([n["x48"] for n in nodes], dtype=np.float32)
    xllm = np.asarray([n["xllm"] for n in nodes], dtype=np.float32)
    x55 = np.concatenate([x48, xllm], axis=1)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    t55 = temporal_features(nodes, x55)
    x_text = embed_texts([str(n["text"]) for n in nodes])

    result = {
        "note": "BERT frozen text embeddings from title/tags/intro/top-liked comments. Text embeddings are reduced by train-only PCA inside each split. Both CatBoost and sklearn HistGradientBoosting are reported.",
        "usable_videos": int(len(nodes)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "split": "BV-sorted samples, train_test_split(test_size=0.3, random_state=42, stratify=y)",
        "text_encoder": str(BERT_MODEL),
        "feature_dims": {
            "base_48": int(x48.shape[1]),
            "llm": int(xllm.shape[1]),
            "temporal_48_plus_llm": int(t55.shape[1]),
            "bert_text_raw": int(x_text.shape[1]),
            "bert_text_pca_train_only": TEXT_PCA_DIM,
        },
        "experiments": {
            "hgb_48": eval_hgb(x48, None, y),
            "hgb_bert_text": eval_hgb(None, x_text, y),
            "hgb_48_plus_bert_text": eval_hgb(x48, x_text, y),
            "hgb_48_plus_llm_plus_temporal": eval_hgb(np.concatenate([x55, t55], axis=1), None, y),
            "hgb_48_plus_llm_plus_temporal_plus_bert_text": eval_hgb(np.concatenate([x55, t55], axis=1), x_text, y),
            "catboost_48": eval_catboost(x48, None, y),
            "catboost_bert_text": eval_catboost(None, x_text, y),
            "catboost_48_plus_bert_text": eval_catboost(x48, x_text, y),
            "catboost_48_plus_llm_plus_temporal": eval_catboost(np.concatenate([x55, t55], axis=1), None, y),
            "catboost_48_plus_llm_plus_temporal_plus_bert_text": eval_catboost(np.concatenate([x55, t55], axis=1), x_text, y),
        },
        "sample_text_preview": [{"bv": nodes[i]["bv"], "text": str(nodes[i]["text"])[:300]} for i in range(min(3, len(nodes)))],
    }
    (OUT / "bert_text_fusion_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["experiments"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
