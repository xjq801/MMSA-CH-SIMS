from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from torch import nn


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
LLM = Path(r"D:\MMSA-CH-SIMS\experiments\stepfun_llm_emotion_student\llm_annotations.jsonl")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\llm_temporal_gnn")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
LLM_KEYS = ["polarity_pos", "polarity_neg", "intensity", "aggressiveness", "sarcasm", "controversy", "confidence"]


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def read_cached() -> dict[str, dict[str, float]]:
    cached = {}
    for line in LLM.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        cached[obj["bv"]] = obj["annotation"]
    return cached


def read_timestamps(folder: Path) -> dict[str, int]:
    paths = list(folder.glob("6*.csv"))
    if not paths:
        return {}
    out = {}
    with paths[0].open("r", encoding="utf-8-sig", newline="") as f:
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
    return nodes


def temporal_adj(nodes, window: int):
    by_pub = defaultdict(list)
    for i, n in enumerate(nodes):
        by_pub[n["publisher"]].append((n["timestamp"], n["order"], i))
    a = np.zeros((len(nodes), len(nodes)), dtype=np.float32)
    edges = 0
    for items in by_pub.values():
        for pos, (_, _, dst) in enumerate(sorted(items)):
            for _, _, src in sorted(items)[max(0, pos - window):pos]:
                a[dst, src] = 1.0
                edges += 1
    deg = a.sum(axis=1, keepdims=True)
    return np.divide(a, deg, out=np.zeros_like(a), where=deg > 0), edges, int((deg.reshape(-1) == 0).sum())


class MLP(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim, 64), nn.ReLU(), nn.Dropout(0.2), nn.Linear(64, 2))

    def forward(self, x):
        return self.net(x)


class TemporalSAGE(nn.Module):
    def __init__(self, dim: int, adj: torch.Tensor):
        super().__init__()
        self.register_buffer("adj", adj)
        self.self1 = nn.Linear(dim, 64)
        self.prev1 = nn.Linear(dim, 64)
        self.self2 = nn.Linear(64, 2)
        self.prev2 = nn.Linear(64, 2)
        self.drop = nn.Dropout(0.2)

    def forward(self, x):
        prev = self.adj @ x
        h = torch.relu(self.self1(x) + self.prev1(prev))
        h = self.drop(h)
        return self.self2(h) + self.prev2(self.adj @ h)


def metric(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def run_model(kind: str, x: np.ndarray, y: np.ndarray, adj: np.ndarray, seed: int):
    torch.manual_seed(seed)
    np.random.seed(seed)
    idx = np.arange(len(y))
    train_val, test = train_test_split(idx, test_size=0.3, random_state=42, stratify=y)
    train_idx, val_idx = train_test_split(train_val, test_size=0.25, random_state=seed, stratify=y[train_val])
    mean, std = x[train_idx].mean(0, keepdims=True), x[train_idx].std(0, keepdims=True) + 1e-6
    xt = torch.tensor((x - mean) / std, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.long)
    model = MLP(x.shape[1]) if kind == "mlp" else TemporalSAGE(x.shape[1], torch.tensor(adj, dtype=torch.float32))
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    best, best_f1 = None, -1.0
    for _ in range(300):
        model.train()
        opt.zero_grad()
        loss = loss_fn(model(xt)[train_idx], yt[train_idx])
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            pred = model(xt)[val_idx].argmax(1).numpy()
        score = f1_score(y[val_idx], pred, zero_division=0)
        if score > best_f1:
            best_f1 = score
            best = {k: v.detach().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best)
    model.eval()
    with torch.no_grad():
        pred = model(xt)[test].argmax(1).numpy()
    return metric(y[test], pred)


def summarize(runs):
    return {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in ["accuracy", "precision", "recall", "f1"]}


def eval_variant(kind: str, x: np.ndarray, y: np.ndarray, adj: np.ndarray):
    runs = [run_model(kind, x, y, adj, seed) for seed in SEEDS]
    return {"runs": runs, "summary": summarize(runs)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes(read_cached())
    x48 = np.asarray([n["x48"] for n in nodes], dtype=np.float32)
    xllm = np.asarray([n["xllm"] for n in nodes], dtype=np.float32)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    adj, edges, no_prev = temporal_adj(nodes, window=10)
    zero = np.zeros_like(adj)
    result = {
        "note": "Same 195 StepFun-cached videos. TemporalSAGE uses causal previous videos from the same publisher, window=10.",
        "usable_videos": int(len(nodes)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "temporal_graph": {"window": 10, "directed_edges": int(edges), "nodes_without_previous": no_prev},
        "mlp_48": eval_variant("mlp", x48, y, zero),
        "mlp_48_plus_llm": eval_variant("mlp", np.concatenate([x48, xllm], axis=1), y, zero),
        "temporal_48": eval_variant("temporal", x48, y, adj),
        "temporal_48_plus_llm": eval_variant("temporal", np.concatenate([x48, xllm], axis=1), y, adj),
    }
    (OUT / "llm_temporal_gnn_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
