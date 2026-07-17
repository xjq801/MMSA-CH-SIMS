from pathlib import Path
import csv
import sys
import tempfile
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task20_legacy48 import (
    assign_group_splits,
    binary_metrics,
    build_split_manifest,
    expand_grid,
    load_legacy48,
    select_trial,
    tune_then_test,
)


class Task20Legacy48Tests(unittest.TestCase):
    def test_group_split_is_deterministic_and_disjoint(self):
        groups = ["publisher-a", "publisher-a", "publisher-b", "publisher-c", "publisher-d"]
        first = assign_group_splits(groups, salt="task20-legacy48-v1", train_cut=0.70, dev_cut=0.85)
        second = assign_group_splits(groups, salt="task20-legacy48-v1", train_cut=0.70, dev_cut=0.85)
        self.assertEqual(first.tolist(), second.tolist())
        self.assertEqual(first[0], first[1])
        by_split = {
            split: {group for group, assigned in zip(groups, first) if assigned == split}
            for split in ("train", "dev", "test")
        }
        self.assertFalse(by_split["train"] & by_split["dev"])
        self.assertFalse(by_split["train"] & by_split["test"])
        self.assertFalse(by_split["dev"] & by_split["test"])

    def test_loader_accepts_only_finite_48d_binary_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            publisher = root / "topic-a" / "publisher-a"
            publisher.mkdir(parents=True)
            path = publisher / "5.sample.csv"
            with path.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle, delimiter=";")
                writer.writerow([f"f{i}" for i in range(48)] + ["label", "video"])
                writer.writerow([str(i) for i in range(48)] + ["1", "video-a"])
                writer.writerow([str(i) for i in range(47)] + ["0"])
                writer.writerow([str(i) for i in range(48)] + ["2", "video-b"])

            data = load_legacy48(root)
            self.assertEqual(data.features.shape, (1, 48))
            self.assertEqual(data.labels.tolist(), [1])
            self.assertEqual(data.groups.tolist(), ["topic-a/publisher-a"])
            self.assertEqual(data.report["accepted_rows"], 1)
            self.assertEqual(data.report["rejected_rows"], 2)
            self.assertNotIn(str(root), str(data.report))

    def test_binary_metrics_include_legacy_contract(self):
        metrics = binary_metrics(np.asarray([0, 1, 1, 0]), np.asarray([0.1, 0.8, 0.4, 0.3]))
        self.assertEqual(
            set(metrics),
            {"macro_f1", "balanced_accuracy", "auprc", "positive_recall", "accuracy", "log_loss", "brier_score"},
        )

    def test_selection_uses_dev_metrics_only(self):
        trials = [
            {"trial_id": "a", "params": {"depth": 4}, "dev_metrics": {"macro_f1": 0.7, "balanced_accuracy": 0.8, "log_loss": 0.4}, "complexity": 4},
            {"trial_id": "b", "params": {"depth": 6}, "dev_metrics": {"macro_f1": 0.8, "balanced_accuracy": 0.7, "log_loss": 0.3}, "complexity": 6},
        ]
        self.assertEqual(select_trial(trials)["trial_id"], "b")

    def test_test_evaluator_is_called_once_after_dev_selection(self):
        test_calls = []

        def train_trial(params):
            return {"name": params["name"]}

        def dev_evaluator(model):
            score = 0.9 if model["name"] == "best" else 0.5
            return {"macro_f1": score, "balanced_accuracy": score, "log_loss": 1.0 - score}

        def test_evaluator(model):
            test_calls.append(model["name"])
            return {"macro_f1": 0.75}

        result = tune_then_test(
            [{"name": "worse"}, {"name": "best"}],
            train_trial=train_trial,
            dev_evaluator=dev_evaluator,
            test_evaluator=test_evaluator,
            complexity=lambda params, model: 1,
        )
        self.assertEqual(result["selected"]["params"]["name"], "best")
        self.assertEqual(test_calls, ["best"])

    def test_grid_budget_and_split_manifest_are_auditable(self):
        trials = expand_grid({"depth": [4, 6, 8], "learning_rate": [0.03, 0.1], "l2": [1, 3]})
        self.assertEqual(len(trials), 12)
        manifest = build_split_manifest(
            np.asarray(["hashed-a", "hashed-b"], dtype=object),
            np.asarray(["publisher-a", "publisher-b"], dtype=object),
            np.asarray(["train", "test"], dtype=object),
        )
        self.assertEqual(manifest["rows"][0]["sample_id"], "hashed-a")
        self.assertNotEqual(manifest["rows"][0]["group_id"], "publisher-a")
        self.assertNotIn("publisher-a", str(manifest))


if __name__ == "__main__":
    unittest.main()
