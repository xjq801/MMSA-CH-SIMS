from pathlib import Path
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task20_training import (
    PooledTrialConfig,
    TemporalTrialConfig,
    train_pooled_trial,
    train_temporal_trial,
)


class Task20PooledTrainingTests(unittest.TestCase):
    def test_training_is_deterministic_for_fixed_seed(self):
        train_features = np.asarray([[0, 0], [1, 1], [0, 1], [1, 0]], dtype=np.float32)
        train_targets = np.asarray([[1, 0], [0, 1], [1, 0], [0, 1]], dtype=np.float32)
        dev_features = np.asarray([[0.1, 0.1], [0.9, 0.9]], dtype=np.float32)
        dev_targets = np.asarray([[1, 0], [0, 1]], dtype=np.float32)
        config = PooledTrialConfig(hidden_dim=4, dropout=0.0, learning_rate=0.01, max_epochs=3, patience=3, batch_size=2)

        first = train_pooled_trial(
            train_features, train_targets, ["train"] * 4,
            dev_features, dev_targets, config, seed=19, device="cpu",
        )
        second = train_pooled_trial(
            train_features, train_targets, ["train"] * 4,
            dev_features, dev_targets, config, seed=19, device="cpu",
        )

        np.testing.assert_allclose(first["dev_predictions"], second["dev_predictions"], rtol=0, atol=0)
        self.assertEqual(first["best_epoch"], second["best_epoch"])

    def test_training_rejects_non_train_fit_rows(self):
        features = np.zeros((2, 2), dtype=np.float32)
        targets = np.asarray([[1, 0], [0, 1]], dtype=np.float32)
        config = PooledTrialConfig(hidden_dim=4, dropout=0.0, learning_rate=0.01, max_epochs=1, patience=1, batch_size=2)
        with self.assertRaisesRegex(ValueError, "train only"):
            train_pooled_trial(features, targets, ["train", "dev"], features, targets, config, seed=1, device="cpu")


class Task20TemporalTrainingTests(unittest.TestCase):
    def setUp(self):
        self.sequences = {
            "train-a": np.zeros((2, 1024), dtype=np.float32),
            "train-b": np.ones((3, 1024), dtype=np.float32),
            "train-c": np.full((1, 1024), 0.25, dtype=np.float32),
            "train-d": np.full((4, 1024), 0.75, dtype=np.float32),
            "dev-a": np.full((2, 1024), 0.1, dtype=np.float32),
            "dev-b": np.full((3, 1024), 0.9, dtype=np.float32),
        }

    def load_sequence(self, item_id):
        return self.sequences[item_id]

    def test_temporal_training_is_deterministic_for_fixed_seed(self):
        train_ids = ["train-a", "train-b", "train-c", "train-d"]
        train_targets = np.asarray([[1, 0], [0, 1], [1, 0], [0, 1]], dtype=np.float32)
        dev_ids = ["dev-a", "dev-b"]
        dev_targets = np.asarray([[1, 0], [0, 1]], dtype=np.float32)
        config = TemporalTrialConfig(
            hidden_dim=4,
            dropout=0.0,
            learning_rate=0.01,
            max_epochs=2,
            patience=2,
            max_batch_size=2,
            max_padded_steps=8,
        )

        first = train_temporal_trial(
            train_ids,
            train_targets,
            ["train"] * 4,
            dev_ids,
            dev_targets,
            self.load_sequence,
            config,
            seed=23,
            device="cpu",
        )
        second = train_temporal_trial(
            train_ids,
            train_targets,
            ["train"] * 4,
            dev_ids,
            dev_targets,
            self.load_sequence,
            config,
            seed=23,
            device="cpu",
        )

        np.testing.assert_allclose(first["dev_predictions"], second["dev_predictions"], rtol=0, atol=0)
        self.assertEqual(first["best_epoch"], second["best_epoch"])
        np.testing.assert_allclose(first["standardizer"].mean, 0.625, atol=1e-7)

    def test_temporal_training_rejects_non_train_fit_rows(self):
        config = TemporalTrialConfig(
            hidden_dim=4,
            dropout=0.0,
            learning_rate=0.01,
            max_epochs=1,
            patience=1,
            max_batch_size=2,
            max_padded_steps=8,
        )
        with self.assertRaisesRegex(ValueError, "train only"):
            train_temporal_trial(
                ["train-a", "train-b"],
                np.asarray([[1, 0], [0, 1]], dtype=np.float32),
                ["train", "dev"],
                ["dev-a"],
                np.asarray([[1, 0]], dtype=np.float32),
                self.load_sequence,
                config,
                seed=1,
                device="cpu",
            )


if __name__ == "__main__":
    unittest.main()
