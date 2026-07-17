from pathlib import Path
import json
import sys
import tempfile
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task20_evaluation import (
    build_prediction_rows,
    paired_bootstrap_delta,
    validate_e0_alignment,
    validate_prediction_rows,
)
from task20_metrics import evaluate_distribution_predictions


class Task20MetricTests(unittest.TestCase):
    def test_perfect_one_hot_predictions_have_perfect_metrics(self):
        targets = np.eye(3, dtype=np.float64)
        metrics = evaluate_distribution_predictions(targets, targets, calibration_bins=3)

        self.assertAlmostEqual(metrics["jensen_shannon_divergence"], 0.0)
        self.assertAlmostEqual(metrics["negative_log_likelihood"], 0.0)
        self.assertAlmostEqual(metrics["earth_movers_distance"], 0.0)
        self.assertAlmostEqual(metrics["macro_f1"], 1.0)
        self.assertAlmostEqual(metrics["balanced_accuracy"], 1.0)
        self.assertAlmostEqual(metrics["brier_score"], 0.0)
        self.assertAlmostEqual(metrics["expected_calibration_error"], 0.0)
        self.assertAlmostEqual(metrics["adaptive_calibration_error"], 0.0)
        self.assertAlmostEqual(metrics["aurc_js"], 0.0)

    def test_metrics_reject_invalid_probabilities(self):
        targets = np.asarray([[0.5, 0.5]], dtype=np.float64)
        with self.assertRaisesRegex(ValueError, "probability"):
            evaluate_distribution_predictions(targets, np.asarray([[1.2, -0.2]]))

    def test_emd_uses_frozen_class_order(self):
        targets = np.asarray([[1.0, 0.0, 0.0]], dtype=np.float64)
        predictions = np.asarray([[0.0, 0.0, 1.0]], dtype=np.float64)
        metrics = evaluate_distribution_predictions(targets, predictions)
        self.assertAlmostEqual(metrics["earth_movers_distance"], 1.0)

    def test_aurc_is_invariant_to_order_when_confidence_ties(self):
        targets = np.asarray([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]], dtype=np.float64)
        predictions = np.asarray([[0.75, 0.25], [0.75, 0.25], [0.75, 0.25]], dtype=np.float64)
        original = evaluate_distribution_predictions(targets, predictions)["aurc_js"]
        permuted = evaluate_distribution_predictions(targets[[1, 2, 0]], predictions[[1, 2, 0]])["aurc_js"]
        self.assertAlmostEqual(original, permuted)


class Task20PredictionContractTests(unittest.TestCase):
    def setUp(self):
        self.sample_ids = ["v1", "v2"]
        self.targets = np.asarray([[1.0, 0.0], [0.25, 0.75]])
        self.predictions = np.asarray([[0.8, 0.2], [0.4, 0.6]])
        self.rows = build_prediction_rows(
            sample_ids=self.sample_ids,
            split="dev",
            class_order=["a", "b"],
            targets=self.targets,
            predictions=self.predictions,
            model_id="overall_mean",
            config_id="task20-common-v1",
        )

    def test_prediction_rows_include_required_auditable_fields(self):
        validate_prediction_rows(
            self.rows,
            expected_ids=self.sample_ids,
            expected_split="dev",
            class_order=["a", "b"],
        )
        self.assertEqual(self.rows[0]["sample_id"], "v1")
        self.assertAlmostEqual(self.rows[0]["confidence"], 0.8)
        self.assertAlmostEqual(self.rows[0]["rejection_score"], 0.2)
        json.dumps(self.rows)

    def test_e0_rejects_misaligned_sample_order(self):
        reversed_rows = list(reversed(self.rows))
        with self.assertRaisesRegex(ValueError, "order"):
            validate_prediction_rows(
                reversed_rows,
                expected_ids=self.sample_ids,
                expected_split="dev",
                class_order=["a", "b"],
            )

    def test_e0_rejects_train_eval_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            validate_e0_alignment(
                train_ids=["v1", "train-only"],
                evaluation_ids=self.sample_ids,
                prediction_rows=self.rows,
                expected_split="dev",
                class_order=["a", "b"],
            )


class Task20BootstrapTests(unittest.TestCase):
    def test_paired_bootstrap_is_deterministic_and_zero_for_identical_models(self):
        targets = np.eye(2, dtype=np.float64)
        predictions = np.asarray([[0.8, 0.2], [0.3, 0.7]], dtype=np.float64)
        first = paired_bootstrap_delta(
            sample_ids=["v1", "v2"],
            targets=targets,
            predictions_a=predictions,
            predictions_b=predictions,
            metric="jensen_shannon_divergence",
            replicates=100,
            seed=20260717,
        )
        second = paired_bootstrap_delta(
            sample_ids=["v1", "v2"],
            targets=targets,
            predictions_a=predictions,
            predictions_b=predictions,
            metric="jensen_shannon_divergence",
            replicates=100,
            seed=20260717,
        )
        self.assertEqual(first, second)
        self.assertEqual(first["unit"], "video")
        self.assertAlmostEqual(first["observed_delta_a_minus_b"], 0.0)
        self.assertAlmostEqual(first["ci95"][0], 0.0)
        self.assertAlmostEqual(first["ci95"][1], 0.0)


class Task20FrozenPlanTests(unittest.TestCase):
    def test_tuning_plan_has_equal_budget_and_dev_only_selection(self):
        plan = json.loads((ROOT / "configs" / "task20" / "tuning-plan-v1.json").read_text(encoding="utf-8"))
        budgets = [entry["max_trials"] for entry in plan["model_families"]]
        self.assertTrue(budgets)
        self.assertEqual(len(set(budgets)), 1)
        self.assertEqual(plan["selection"]["split"], "dev")
        self.assertEqual(plan["selection"]["primary_metric"], "jensen_shannon_divergence")
        self.assertFalse(plan["test_policy"]["visible_during_selection"])


if __name__ == "__main__":
    unittest.main()
