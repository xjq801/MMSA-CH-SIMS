from pathlib import Path
import json
import sys
import unittest
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_task20_temporal_attention as runner
from run_task20_temporal_attention import (
    limit_smoke_records,
    memoize_sequence_loader,
    temporal_trial_grid,
    validate_eval_policy,
)


class Task20TemporalRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tuning_plan = json.loads(
            (ROOT / "configs" / "task20" / "tuning-plan-v1.json").read_text(encoding="utf-8")
        )

    def test_temporal_grid_matches_frozen_twelve_trial_budget(self):
        rows = temporal_trial_grid(self.tuning_plan, smoke=False)
        self.assertEqual(len(rows), 12)
        self.assertEqual({row.max_batch_size for row in rows}, {64})
        self.assertEqual({row.max_padded_steps for row in rows}, {16384})

    def test_smoke_grid_does_not_change_frozen_cartesian_identity(self):
        row = temporal_trial_grid(self.tuning_plan, smoke=True)[0]
        self.assertEqual(row.max_epochs, 2)
        self.assertEqual(row.patience, 2)

    def test_test_split_requires_authorization_and_frozen_selection(self):
        with self.assertRaisesRegex(ValueError, "test requires"):
            validate_eval_policy("test", allow_final_test=False, selection_file=None)
        with self.assertRaisesRegex(ValueError, "test requires"):
            validate_eval_policy("test", allow_final_test=True, selection_file=None)

    def test_test_split_rejects_smoke_mode(self):
        with self.assertRaisesRegex(ValueError, "smoke"):
            validate_eval_policy(
                "test",
                allow_final_test=True,
                selection_file=Path("selection.json"),
                smoke=True,
            )

    def test_dev_rejects_external_selection(self):
        with self.assertRaisesRegex(ValueError, "dev tuning"):
            validate_eval_policy("dev", allow_final_test=False, selection_file=Path("selection.json"))

    def test_test_ids_are_never_used_for_early_stopping(self):
        config = temporal_trial_grid(self.tuning_plan, smoke=True)[0]
        train_ids = ["train-a", "train-b"]
        train_targets = np.asarray([[1, 0], [0, 1]], dtype=np.float32)
        dev_ids = ["dev-a"]
        dev_targets = np.asarray([[0.5, 0.5]], dtype=np.float32)
        test_ids = ["test-a"]
        trained = {"model": object(), "standardizer": object(), "dev_metrics": {}}
        expected = np.asarray([[0.25, 0.75]], dtype=np.float64)

        with mock.patch.object(runner, "train_temporal_trial", return_value=trained) as train_mock:
            with mock.patch.object(runner, "predict_temporal_model", return_value=expected) as predict_mock:
                result, predictions = runner.fit_temporal_for_evaluation(
                    train_ids,
                    train_targets,
                    dev_ids,
                    dev_targets,
                    test_ids,
                    lambda item_id: np.zeros((1, 1024), dtype=np.float32),
                    config,
                    seed=7,
                    device="cpu",
                )

        self.assertIs(result, trained)
        np.testing.assert_array_equal(predictions, expected)
        self.assertEqual(train_mock.call_args.args[3], dev_ids)
        np.testing.assert_array_equal(train_mock.call_args.args[4], dev_targets)
        self.assertEqual(predict_mock.call_args.args[2], test_ids)

    def test_smoke_subset_is_deterministic_and_order_preserving(self):
        item_ids = ["c", "a", "b"]
        targets = np.asarray([[1, 0], [0, 1], [0.5, 0.5]], dtype=np.float32)
        selected_ids, selected_targets = limit_smoke_records(item_ids, targets, limit=2)
        self.assertEqual(selected_ids, ["c", "a"])
        np.testing.assert_array_equal(selected_targets, targets[:2])

    def test_memory_cache_loads_each_restricted_sequence_once_without_writing(self):
        calls = []

        def source(item_id):
            calls.append(item_id)
            return np.full((2, 1024), len(calls), dtype=np.float32)

        cached = memoize_sequence_loader(source)
        first = cached("item-a")
        second = cached("item-a")
        other = cached("item-b")

        self.assertEqual(calls, ["item-a", "item-b"])
        self.assertIs(first, second)
        self.assertFalse(first.flags.writeable)
        self.assertEqual(other.dtype, np.float32)


if __name__ == "__main__":
    unittest.main()
