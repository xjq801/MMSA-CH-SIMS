from pathlib import Path
import sys
import tempfile
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np

from run_task30_h1_development import (
    run_development_matrix,
    load_canonical_train_dev,
    student_trial_grid,
    validate_development_policy,
    write_run_bundle,
)
from task30_contracts import DatasetRuntimeSpec


class Task30RunnerPolicyTests(unittest.TestCase):
    def test_canonical_loader_materializes_train_and_dev_only(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "labels.jsonl"
            rows = []
            for split, count in (("train", 2), ("dev", 3), ("test", 4)):
                rows.append({
                    "item_id": split,
                    "split": {"group_by_video_v1": split},
                    "emotion_distribution": {"a": 0.25, "b": 0.75},
                    "response_count": count,
                })
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            loaded = load_canonical_train_dev(
                path,
                DatasetRuntimeSpec(
                    dataset_id="toy",
                    class_order=("a", "b"),
                    split_scheme="group_by_video_v1",
                    item_id_field="item_id",
                    target_distribution_field="emotion_distribution",
                    response_count_field="response_count",
                ),
            )
            self.assertEqual(loaded["train_ids"], ["train"])
            self.assertEqual(loaded["dev_ids"], ["dev"])
            self.assertEqual(loaded["dev_response_counts"].tolist(), [3])
            self.assertNotIn("test", str(loaded))

    def test_test_split_is_unreachable(self):
        with self.assertRaisesRegex(ValueError, "test"):
            validate_development_policy("test")

    def test_dev_split_is_allowed(self):
        validate_development_policy("dev")

    def test_each_deployable_row_has_same_twelve_trial_student_budget(self):
        for row in ("hard_label_student", "soft_distribution_student", "ordinary_kd_student", "comment_privileged_kd_student", "mismatched_comment_teacher_control"):
            with self.subTest(row=row):
                grid = student_trial_grid(row, smoke=False)
                self.assertEqual(len(grid), 12)
                self.assertEqual({config.max_epochs for config in grid}, {200})
                self.assertEqual({config.patience for config in grid}, {20})
        self.assertEqual(len(student_trial_grid("soft_distribution_student_dirichlet", smoke=False)), 12)

    def test_smoke_matrix_runs_all_rows_without_test_interface(self):
        rng = np.random.RandomState(3)
        train_x = rng.normal(size=(30, 6)).astype(np.float32)
        dev_x = rng.normal(size=(10, 6)).astype(np.float32)
        train_raw = rng.uniform(size=(30, 3))
        dev_raw = rng.uniform(size=(10, 3))
        train_y = (train_raw / train_raw.sum(axis=1, keepdims=True)).astype(np.float32)
        dev_y = (dev_raw / dev_raw.sum(axis=1, keepdims=True)).astype(np.float32)
        privileged = np.concatenate((train_y, rng.normal(size=(30, 2))), axis=1).astype(np.float32)
        result = run_development_matrix(
            train_x, train_y, dev_x, dev_y, privileged,
            dev_response_counts=np.arange(1, 11), seed=13, device="cpu", smoke=True,
        )
        expected = {
            "hard_label_student",
            "soft_distribution_student",
            "soft_distribution_student_dirichlet",
            "ordinary_kd_student",
            "comment_privileged_kd_student",
            "mismatched_comment_teacher_control",
        }
        self.assertEqual(set(result["rows"]), expected)
        for row in result["rows"].values():
            self.assertEqual(len(row["trials"]), 1)
            self.assertEqual(row["dev_predictions"].shape, dev_y.shape)
            self.assertTrue(np.isfinite(row["dev_predictions"]).all())
        self.assertEqual(result["teacher_only_upper_bound"]["evaluation_scope"], "TRAIN_DIAGNOSTIC_ONLY")
        self.assertIn("response_count", result["subgroup_analysis"])

    def test_frozen_selection_replay_runs_one_trial_per_row(self):
        rng = np.random.RandomState(8)
        train_x = rng.normal(size=(24, 5)).astype(np.float32)
        dev_x = rng.normal(size=(8, 5)).astype(np.float32)
        train_y = np.full((24, 3), 1 / 3, dtype=np.float32)
        dev_y = np.full((8, 3), 1 / 3, dtype=np.float32)
        privileged = np.concatenate((train_y, np.ones((24, 1), dtype=np.float32)), axis=1)
        first = run_development_matrix(
            train_x, train_y, dev_x, dev_y, privileged,
            dev_response_counts=np.arange(1, 9), seed=17, device="cpu", smoke=True,
        )
        frozen = {row_id: row["selected_config"] for row_id, row in first["rows"].items()}
        replay = run_development_matrix(
            train_x, train_y, dev_x, dev_y, privileged,
            dev_response_counts=np.arange(1, 9), seed=17, device="cpu", smoke=False,
            frozen_configs=frozen,
        )
        self.assertEqual(replay["selection_identity"], "FROZEN_FROM_PRIOR_DEV_SELECTION")
        self.assertTrue(all(len(row["trials"]) == 1 for row in replay["rows"].values()))

    def test_run_bundle_separates_private_predictions_from_aggregate_summary(self):
        rng = np.random.RandomState(4)
        train_x = rng.normal(size=(20, 4)).astype(np.float32)
        dev_x = rng.normal(size=(6, 4)).astype(np.float32)
        train_y = np.full((20, 3), 1 / 3, dtype=np.float32)
        dev_y = np.full((6, 3), 1 / 3, dtype=np.float32)
        privileged = np.concatenate((train_y, np.ones((20, 1), dtype=np.float32)), axis=1)
        result = run_development_matrix(
            train_x, train_y, dev_x, dev_y, privileged,
            dev_response_counts=np.arange(1, 7), seed=21, device="cpu", smoke=True,
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "run"
            manifest = write_run_bundle(
                output, result, ["private-{}".format(i) for i in range(6)], dev_y,
                class_order=("a", "b", "c"), seed=21, smoke=True,
                git_commit="a" * 40, git_dirty=False,
                source_hashes={"labels": "b" * 64},
            )
            expected = {
                "manifest.json", "config.json", "environment.json", "stdout.log",
                "stderr.log", "raw_metrics.jsonl", "predictions.csv",
                "training_history.jsonl", "model_state_hashes.json", "models",
                "test_evidence.json", "guardrails.json", "aggregate_summary.json",
            }
            self.assertEqual({path.name for path in output.iterdir()}, expected)
            self.assertEqual(manifest["status"], "COMPLETED")
            self.assertEqual(manifest["schema_version"], "task30-run-manifest-v2")
            self.assertEqual(manifest["exit_code"], 0)
            self.assertTrue(manifest["started_at"])
            self.assertEqual(set(manifest["matrix_row_ids"]), set(result["rows"]))
            self.assertEqual(len(list((output / "models").glob("*.pt"))), len(result["rows"]))
            aggregate = (output / "aggregate_summary.json").read_text(encoding="utf-8")
            self.assertNotIn("private-", aggregate)
            self.assertNotIn(str(output.resolve()), aggregate)
            self.assertIn("private-0", (output / "predictions.csv").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
