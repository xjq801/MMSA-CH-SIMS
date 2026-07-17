from pathlib import Path
import json
import sys
import tempfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from task20_baseline import (
    evaluate,
    fit_topic_train,
    fit_train,
    load_canonical_records,
    load_records,
    predict,
    predict_topic,
    run_minimum_baselines,
    topic_mean_eligibility,
)


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
            self.assertEqual(set(metrics), {
                "jensen_shannon_divergence",
                "negative_log_likelihood",
                "earth_movers_distance",
                "macro_f1",
                "balanced_accuracy",
                "brier_score",
                "expected_calibration_error",
                "adaptive_calibration_error",
                "aurc_js",
            })

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

    def test_canonical_loader_uses_frozen_split_and_class_order(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "canonical.jsonl"
            _write(path, [{
                "item_id": "a",
                "split": {"group_by_video_v1": "train"},
                "available_at_t0": False,
                "emotion_distribution": {"joy": 0.25, "sadness": 0.75},
                "topic_id": "topic-a",
            }])
            records = load_canonical_records(
                path,
                split_scheme="group_by_video_v1",
                expected_split="train",
                distribution_field="emotion_distribution",
                class_order=["sadness", "joy"],
            )
            self.assertEqual(records[0].item_id, "a")
            self.assertEqual(records[0].topic_id, "topic-a")
            self.assertTrue(np.allclose(records[0].target, [0.75, 0.25]))

    def test_topic_mean_is_train_only_and_topic_conditioned(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "canonical.jsonl"
            _write(path, [
                {"item_id": "a", "split": {"group_by_video_v1": "train"}, "emotion_distribution": {"x": 1, "y": 0}, "topic_id": "t1"},
                {"item_id": "b", "split": {"group_by_video_v1": "train"}, "emotion_distribution": {"x": 0, "y": 1}, "topic_id": "t2"},
            ])
            records = load_canonical_records(path, "group_by_video_v1", "train", "emotion_distribution", ["x", "y"])
            model = fit_topic_train(records)
            self.assertTrue(np.allclose(predict_topic(model, ["t2", "t1"]), [[0, 1], [1, 0]]))

    def test_topic_mean_is_not_applicable_without_native_topics(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "canonical.jsonl"
            _write(path, [{"item_id": "a", "split": {"group_by_video_v1": "train"}, "emotion_distribution": {"x": 1, "y": 0}, "topic_id": None}])
            records = load_canonical_records(path, "group_by_video_v1", "train", "emotion_distribution", ["x", "y"])
            self.assertEqual(topic_mean_eligibility(records), "NOT_APPLICABLE_NATIVE_TOPIC_ABSENT")
            with self.assertRaisesRegex(ValueError, "native topic"):
                fit_topic_train(records)

    def test_all_minimum_baselines_share_evaluation_sample_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "canonical.jsonl"
            _write(path, [
                {"item_id": "train-a", "split": {"group_by_video_v1": "train"}, "emotion_distribution": {"x": 1, "y": 0}, "topic_id": None},
                {"item_id": "train-b", "split": {"group_by_video_v1": "train"}, "emotion_distribution": {"x": 0, "y": 1}, "topic_id": None},
                {"item_id": "dev-a", "split": {"group_by_video_v1": "dev"}, "emotion_distribution": {"x": 0.5, "y": 0.5}, "topic_id": None},
            ])
            train = load_canonical_records(path, "group_by_video_v1", "train", "emotion_distribution", ["x", "y"])
            dev = load_canonical_records(path, "group_by_video_v1", "dev", "emotion_distribution", ["x", "y"])
            result = run_minimum_baselines(train, dev)
            for name in ("overall_mean", "empirical_distribution", "majority_class"):
                self.assertEqual(result[name]["sample_ids"], ["dev-a"])
                self.assertEqual(result[name]["status"], "COMPLETED")
            self.assertEqual(result["topic_mean"]["status"], "NOT_APPLICABLE_NATIVE_TOPIC_ABSENT")


if __name__ == "__main__":
    unittest.main()
