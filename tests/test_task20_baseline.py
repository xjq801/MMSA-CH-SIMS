from pathlib import Path
import json
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task20_baseline import evaluate, fit_train, load_records, predict


def _write(path: Path, rows):
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


class Task20BaselineTests(unittest.TestCase):
    def test_train_only_baselines_and_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "train.jsonl"
            _write(path, [{"item_id": "a", "split": "train", "target_distribution": [1, 0]}, {"item_id": "b", "split": "train", "target_distribution": [0, 1]}, {"item_id": "c", "split": "train", "target_distribution": [1, 0]}])
            model = fit_train(load_records(path, "train"))
            self.assertTrue(np.allclose(model["overall_mean"], [2 / 3, 1 / 3]))
            self.assertTrue(np.allclose(model["empirical_distribution"], [2 / 3, 1 / 3]))
            self.assertTrue(np.allclose(predict(model, "majority_class", 2), [[1, 0], [1, 0]]))
            metrics = evaluate(np.asarray([[1, 0], [0, 1]]), predict(model, "overall_mean", 2))
            self.assertEqual(set(metrics), {"jensen_shannon_divergence", "mean_absolute_error", "argmax_accuracy"})

    def test_fit_rejects_dev_or_test(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev.jsonl"
            _write(path, [{"item_id": "a", "split": "dev", "target_distribution": [1, 0]}])
            with self.assertRaisesRegex(ValueError, "fit scope"):
                fit_train(load_records(path, "dev"))

    def test_loader_rejects_forbidden_future_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            _write(path, [{"item_id": "a", "split": "train", "target_distribution": [1, 0], "comment_text": "redacted"}])
            with self.assertRaisesRegex(ValueError, "forbidden"):
                load_records(path, "train")


if __name__ == "__main__":
    unittest.main()
