import pickle
from pathlib import Path

import numpy as np


DATA = Path(__file__).parent / "data" / "SIMS" / "Processed" / "unaligned_39.pkl"
BINS = {
    "Acc-2": ([0.0], ["[-1, 0]", "(0, 1]"]),
    "Acc-3": ([-0.1, 0.1], ["[-1, -0.1]", "(-0.1, 0.1]", "(0.1, 1]"]),
    "Acc-5": ([-0.7, -0.1, 0.1, 0.7], ["[-1, -0.7]", "(-0.7, -0.1]", "(-0.1, 0.1]", "(0.1, 0.7]", "(0.7, 1]"]),
}


def counts(labels, boundaries):
    return np.bincount(np.digitize(labels, boundaries, right=True), minlength=len(boundaries) + 1)


with DATA.open("rb") as f:
    data = pickle.load(f)

splits = {name: np.asarray(data[name]["regression_labels"]).reshape(-1) for name in ("train", "valid", "test")}
splits["total"] = np.concatenate(list(splits.values()))

for name, labels in splits.items():
    print(f"\n## {name} (n={len(labels)})")
    print(f"range=[{labels.min():.1f}, {labels.max():.1f}], mean={labels.mean():.4f}, std={labels.std():.4f}, zero={(labels == 0).sum()}")
    for metric, (boundaries, names) in BINS.items():
        values = counts(labels, boundaries)
        assert values.sum() == len(labels)
        cells = [f"{label}: {count} ({count / len(labels):.2%})" for label, count in zip(names, values)]
        print(metric + " | " + " | ".join(cells))

labels = splits["total"]
values, frequencies = np.unique(labels, return_counts=True)
print("\n## exact values (total)")
print(" | ".join(f"{value:.1f}: {count} ({count / len(labels):.2%})" for value, count in zip(values, frequencies)))
