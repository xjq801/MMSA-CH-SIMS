from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from torch import nn


DATA = Path(r"D:\李佳怡毕业论文配套代码\极端群体情绪预测数据集")
OUT = Path(r"D:\MMSA-CH-SIMS\experiments\propagation_gcn")
FEATURE_COUNT = 48
SEEDS = [1111, 1112, 1113]
csv.field_size_limit(10_000_000)


def bv(text: str) -> str:
    m = re.search(r"BV[0-9A-Za-z]+", text or "")
    return m.group(0) if m else ""


def read_timestamps(folder: Path) -> dict[str, int]:
    out = {}
    path = folder / "6.发布者视频列表.csv"
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
    nodes = []
    seen = set()
    for vec in sorted(DATA.rglob("5*.csv")):
        rel = vec.relative_to(DATA)
        topic = rel.parts[0]
        publisher = rel.parts[1]
        timestamps = read_timestamps(vec.parent)
        with vec.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row_no, row in enumerate(reader):
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
                nodes.append({
                    "bv": key,
                    "x": x,
                    "y": int(y),
                    "topic": topic,
                    "publisher": f"{topic}/{publisher}",
                    "timestamp": timestamps.get(key, 0),
                    "row_order": row_no,
                    "folder": str(vec.parent),
                })
                seen.add(key)
    return nodes


def read_comment_users(target_bvs: set[str]):
    video_users = defaultdict(set)
    for path in DATA.rglob("1.评论数据*.csv"):
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            clean = (line.replace("\x00", "") for line in f)
            for row in csv.DictReader(clean, delimiter=";"):
                key = bv(row.get("视频地址", ""))
                if key not in target_bvs:
                    continue
                user = (row.get("用户名", "") or "").strip()
                if user:
                    video_users[key].add(user)
    return video_users


def build_edges(nodes):
    idx = {n["bv"]: i for i, n in enumerate(nodes)}
    edge_sets = {"publisher_temporal": set(), "shared_comment_user": set()}
    counts = Counter()

    by_pub = defaultdict(list)
    for i, n in enumerate(nodes):
        by_pub[n["publisher"]].append((n["timestamp"], n["row_order"], i))
    for items in by_pub.values():
        items = sorted(items)
        for a, b in zip(items, items[1:]):
            i, j = a[2], b[2]
            edge_sets["publisher_temporal"].add((min(i, j), max(i, j)))
            counts["publisher_temporal"] += 1

    video_users = read_comment_users(set(idx))
    user_videos = defaultdict(list)
    for key, users in video_users.items():
        for user in users:
            user_videos[user].append(idx[key])
    for vids in user_videos.values():
        uniq = sorted(set(vids))
        if 2 <= len(uniq) <= 20:
            for i, j in combinations(uniq, 2):
                edge_sets["shared_comment_user"].add((min(i, j), max(i, j)))
                counts["shared_comment_user"] += 1
    edges = set().union(*edge_sets.values())
    return {k: sorted(v) for k, v in edge_sets.items()}, sorted(edges), counts, {k: len(v) for k, v in video_users.items()}


def norm_adj(n, edges):
    a = np.eye(n, dtype=np.float32)
    for i, j in edges:
        a[i, j] = 1.0
        a[j, i] = 1.0
    deg = a.sum(axis=1)
    inv = np.power(deg, -0.5, where=deg > 0)
    return (inv[:, None] * a * inv[None, :]).astype(np.float32), deg


class MLP(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(dim, 64), nn.ReLU(), nn.Dropout(0.2), nn.Linear(64, 2))

    def forward(self, x):
        return self.net(x)


class GCN(nn.Module):
    def __init__(self, dim, adj):
        super().__init__()
        self.register_buffer("adj", adj)
        self.fc1 = nn.Linear(dim, 64)
        self.fc2 = nn.Linear(64, 2)
        self.drop = nn.Dropout(0.2)

    def forward(self, x):
        h = self.adj @ x
        h = torch.relu(self.fc1(h))
        h = self.drop(h)
        h = self.adj @ h
        return self.fc2(h)


def metrics(y, pred):
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def train_model(kind, x, y, adj, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    all_idx = np.arange(len(y))
    train_val, test = train_test_split(all_idx, test_size=0.2, random_state=42, stratify=y)
    train, val = train_test_split(train_val, test_size=0.2, random_state=seed, stratify=y[train_val])
    mean = x[train].mean(axis=0, keepdims=True)
    std = x[train].std(axis=0, keepdims=True) + 1e-6
    xt = torch.tensor((x - mean) / std, dtype=torch.float32)
    yt = torch.tensor(y, dtype=torch.long)
    adjt = torch.tensor(adj, dtype=torch.float32)
    model = MLP(x.shape[1]) if kind == "mlp" else GCN(x.shape[1], adjt)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    best_state, best_val = None, -1.0
    for _ in range(220):
        model.train()
        opt.zero_grad()
        out = model(xt)
        loss = loss_fn(out[train], yt[train])
        loss.backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            val_pred = model(xt)[val].argmax(1).numpy()
        val_f1 = f1_score(y[val], val_pred, zero_division=0)
        if val_f1 > best_val:
            best_val = val_f1
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pred = model(xt)[test].argmax(1).numpy()
    return metrics(y[test], pred)


def summarize(rows):
    return {
        k: {"mean": float(np.mean([r[k] for r in rows])), "std": float(np.std([r[k] for r in rows]))}
        for k in ["accuracy", "precision", "recall", "f1"]
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    nodes = load_nodes()
    edge_sets, edges, edge_counts, comment_counts = build_edges(nodes)
    variants = {
        "publisher_temporal": edge_sets["publisher_temporal"],
        "shared_comment_user": edge_sets["shared_comment_user"],
        "full_topology": edges,
    }
    adj, deg = norm_adj(len(nodes), edges)
    x = np.asarray([n["x"] for n in nodes], dtype=np.float32)
    y = np.asarray([n["y"] for n in nodes], dtype=np.int64)
    mlp_runs = [train_model("mlp", x, y, adj, seed) for seed in SEEDS]
    gcn_results = {}
    for name, variant_edges in variants.items():
        cur_adj, cur_deg = norm_adj(len(nodes), variant_edges)
        runs = [train_model("gcn", x, y, cur_adj, seed) for seed in SEEDS]
        gcn_results[name] = {
            "edges": int(len(variant_edges)),
            "degree": {"mean": float(cur_deg.mean()), "max": float(cur_deg.max()), "isolated": int((cur_deg <= 1).sum())},
            "runs": runs,
            "summary": summarize(runs),
        }
    result = {
        "note": "Pure PyTorch propagation-topology prototype: video nodes, shared-comment-user edges, publisher temporal edges.",
        "nodes": int(len(nodes)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "edges": int(len(edges)),
        "edge_sources": dict(edge_counts),
        "degree": {"mean": float(deg.mean()), "max": float(deg.max()), "isolated": int((deg <= 1).sum())},
        "comment_coverage": {
            "videos_with_comments": int(sum(1 for v in comment_counts.values() if v > 0)),
            "mean_users_per_commented_video": float(np.mean(list(comment_counts.values()))) if comment_counts else 0.0,
        },
        "seeds": SEEDS,
        "mlp_48": {"runs": mlp_runs, "summary": summarize(mlp_runs)},
        "gcn_variants": gcn_results,
    }
    (OUT / "propagation_gcn_results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
