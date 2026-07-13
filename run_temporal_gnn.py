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
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\temporal_gnn")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def read_timestamps(folder: Path) -> dict[str, int]:
    path = folder / "6.发布者视频列表.csv"
    out = {}
    if not path.exists():
        return out
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            key = bv(row.get("视频地址", ""))
            try:
                ts = int(float(row.get("发布时间", 0) or 0))
            except ValueError:
                ts = 0
            if key and ts:
                out[key] = ts
    return out


def load_nodes():
    nodes, seen = [], set()
    for vec in sorted(DATA.rglob("5*.csv")):
        rel = vec.relative_to(DATA)
        publisher = f"{rel.parts[0]}/{rel.parts[1]}"
        timestamps = read_timestamps(vec.parent)
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for order, row in enumerate(reader):
                if len(row) < FEATURE_COUNT + 2:
                    continue
                key = row[FEATURE_COUNT + 1].strip()
                if not key or key in seen:
                    continue
                try:
                    x = [float(v) for v in row[:FEATURE_COUNT]]
                except ValueError:
                    continue
                y = row[FEATURE_COUNT].strip()
                if y not in {"0", "1"} or not all(math.isfinite(v) for v in x):
                    continue
                nodes.append({"bv": key, "x": x, "y": int(y), "publisher": publisher, "timestamp": timestamps.get(key, 0), "order": order})
                seen.add(key)
    return nodes


def temporal_adj(nodes, window: int):
    by_pub = defaultdict(list)
    for i, n in enumerate(nodes):
        by_pub[n["publisher"]].append((n["timestamp"], n["order"], i))
    a = np.zeros((len(nodes), len(nodes)), dtype=np.float32)
    edges = 0
    for items in by_pub.values():
        items = sorted(items)
        for pos, (_, _, dst) in enumerate(items):
            prev = items[max(0, pos - window):pos]
            for _, _, src in prev:
                # causal: dst aggregates only previous videos from the same publisher.
                a[dst, src] = 1.0
                edges += 1
    deg = a.sum(axis=1, keepdims=True)
    a = np.divide(a, deg, out=np.zeros_like(a), where=deg > 0)
    return a, edges, int((deg.reshape(-1) == 0).sum())


class MLP(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim, 64), nn.ReLU(), nn.Dropout(0.2), nn.Linear(64, 2))

    def forward(self, x):
        return self.net(x)


class TemporalSAGE(nn.Module):
    def __init__(self, dim, adj):
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


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def train(kind, x, y, adj, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    idx = np.arange(len(y))
    train_val, test = train_test_split(idx, test_size=0.2, random_state=42, stratify=y)
    train_idx, val_idx = train_test_split(train_val, test_size=0.2, random_state=seed, stratify=y[train_val])
    mean, std = x[train_idx].mean(0, keepdims=True), x[train_idx].std(0, keepdims=True) + 1e-6
    xt = torch.tensor((x - mean) / std, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.long)
    model = MLP(x.shape[1]) if kind == "mlp" else TemporalSAGE(x.shape[1], torch.tensor(adj, dtype=torch.float32))
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    best, best_f1 = None, -1.0
    for _ in range(260):
        model.train()
        opt.zero_grad()
        out = model(xt)
        loss = loss_fn(out[train_idx], yt[train_idx])
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
    return metrics(y[test], pred)


def summarize(runs):
    return {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in ["accuracy", "precision", "recall", "f1"]}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes()
    x = np.asarray([n["x"] for n in nodes], dtype=np.float32)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    mlp_runs = [train("mlp", x, y, np.zeros((len(nodes), len(nodes)), dtype=np.float32), seed) for seed in SEEDS]
    variants = {}
    for window in [1, 3, 5, 10]:
        adj, edges, no_prev = temporal_adj(nodes, window)
        runs = [train("temporal", x, y, adj, seed) for seed in SEEDS]
        variants[f"temporal_sage_prev{window}"] = {
            "window": window,
            "directed_edges": int(edges),
            "nodes_without_previous": no_prev,
            "runs": runs,
            "summary": summarize(runs),
        }
    result = {
        "note": "Causal Temporal GraphSAGE: each video aggregates only previous videos from the same publisher.",
        "nodes": int(len(nodes)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "seeds": SEEDS,
        "mlp_48": {"runs": mlp_runs, "summary": summarize(mlp_runs)},
        "temporal_variants": variants,
    }
    (OUT / "temporal_gnn_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
