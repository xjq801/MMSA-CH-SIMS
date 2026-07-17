from pathlib import Path
import sys
import unittest
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_task20_pooled_mlp as runner
from task20_training import PooledTrialConfig


class Task20PooledRunnerTests(unittest.TestCase):
    def test_test_features_are_never_used_for_early_stopping(self):
        train_features = np.zeros((2, 2), dtype=np.float32)
        train_targets = np.asarray([[1, 0], [0, 1]], dtype=np.float32)
        dev_features = np.full((1, 2), 3.0, dtype=np.float32)
        dev_targets = np.asarray([[0.5, 0.5]], dtype=np.float32)
        test_features = np.full((1, 2), 9.0, dtype=np.float32)
        config = PooledTrialConfig(4, 0.0, 0.01, 2, 2, 2)
        trained = {"model": object(), "standardizer": object(), "dev_metrics": {}}
        expected = np.asarray([[0.25, 0.75]], dtype=np.float64)

        with mock.patch.object(runner, "train_pooled_trial", return_value=trained) as train_mock:
            with mock.patch.object(runner, "predict_pooled_model", return_value=expected) as predict_mock:
                result, predictions = runner.fit_pooled_for_evaluation(
                    train_features,
                    train_targets,
                    dev_features,
                    dev_targets,
                    test_features,
                    config,
                    seed=7,
                    device="cpu",
                )

        self.assertIs(result, trained)
        np.testing.assert_array_equal(predictions, expected)
        np.testing.assert_array_equal(train_mock.call_args.args[3], dev_features)
        np.testing.assert_array_equal(train_mock.call_args.args[4], dev_targets)
        np.testing.assert_array_equal(predict_mock.call_args.args[2], test_features)


if __name__ == "__main__":
    unittest.main()
