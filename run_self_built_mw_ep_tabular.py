from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


FEATURES = 48


def load_data(root: Path):
    xs, ys = [], []
    rejected = Counter()
    for path in sorted(root.rglob("5*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)
            for row in reader:
                if len(row) < FEATURES + 1:
                    rejected["too_few_columns"] += 1
                    continue
                try:
                    x = [float(v) for v in row[:FEATURES]]
                except ValueError:
                    rejected["non_numeric_features"] += 1
                    continue
                y = row[FEATURES].strip()
                if y not in {"0", "1"} or not all(math.isfinite(v) for v in x):
                    rejected["bad_label_or_feature"] += 1
                    continue
                xs.append(x)
                ys.append(int(y))
    if not xs:
        raise RuntimeError(f"No usable rows under {root}")
    return np.asarray(xs, dtype=np.float32), np.asarray(ys, dtype=np.int64), dict(rejected)


class TabularMWEP(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.encoders = nn.ModuleList(
            [nn.Sequential(nn.Linear(12, hidden), nn.ReLU(), nn.Dropout(0.1)) for _ in range(4)]
        )
        self.gate = nn.Sequential(nn.Linear(hidden * 4, hidden), nn.ReLU(), nn.Linear(hidden, 4))
        self.classifier = nn.Linear(hidden, 2)
        self.prototypes = nn.Parameter(torch.randn(2, hidden) * 0.02)

    def forward(self, x):
        # 48 dims = 4 pseudo modalities(title/tag/intro/cover) * 12 statistics.
        chunks = [x[:, i::4] for i in range(4)]
        feats = torch.stack([enc(chunk) for enc, chunk in zip(self.encoders, chunks)], dim=1)
        weights = torch.softmax(self.gate(feats.flatten(1)), dim=-1).unsqueeze(-1)
        fused = (weights * feats).sum(dim=1)
        cls_logits = self.classifier(fused)
        proto_logits = -torch.cdist(fused, self.prototypes)
        return cls_logits + 0.3 * proto_logits


def evaluate(model, x, y, device):
    model.eval()
    with torch.no_grad():
        pred = model(torch.from_numpy(x).to(device)).argmax(dim=1).cpu().numpy()
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred, zero_division=0)),
        "recall": float(recall_score(y, pred, zero_division=0)),
        "f1": float(f1_score(y, pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }


def run_seed(x, y, seed, epochs):
    torch.manual_seed(seed)
    np.random.seed(seed)
    train_idx, test_idx = train_test_split(
        np.arange(len(y)), test_size=0.2, random_state=42, stratify=y
    )
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    mean, std = x_train.mean(axis=0, keepdims=True), x_train.std(axis=0, keepdims=True) + 1e-6
    x_train, x_test = (x_train - mean) / std, (x_test - mean) / std

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = TabularMWEP().to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-3)
    loss_fn = nn.CrossEntropyLoss()
    loader = DataLoader(
        TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
        batch_size=64,
        shuffle=True,
    )
    for _ in range(epochs):
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
    return evaluate(model, x_test, y_test, device)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("experiments/self_built_dataset/tabular_mw_ep/results.json"))
    parser.add_argument("--seeds", nargs="+", type=int, default=[1111, 1112, 1113])
    parser.add_argument("--epochs", type=int, default=120)
    args = parser.parse_args()

    x, y, rejected = load_data(args.data_dir)
    runs = [run_seed(x, y, seed, args.epochs) for seed in args.seeds]
    keys = ["accuracy", "precision", "recall", "f1"]
    summary = {k: {"mean": float(np.mean([r[k] for r in runs])), "std": float(np.std([r[k] for r in runs]))} for k in keys}
    result = {
        "note": "Tabular MW+EP transfer, not original Self-MM sequence model.",
        "rows": int(len(y)),
        "labels": {"0": int((y == 0).sum()), "1": int((y == 1).sum())},
        "rejected": rejected,
        "seeds": args.seeds,
        "epochs": args.epochs,
        "runs": runs,
        "summary": summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
