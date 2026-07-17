from pathlib import Path
import os
import sys
import unittest
from unittest import mock

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task20_models import (
    PooledDistributionMLP,
    TemporalAttentionDistributionModel,
    apply_standardizer,
    fit_train_standardizer,
    pool_i3d_statistics,
    seed_everything,
)


class Task20FrozenFeatureTests(unittest.TestCase):
    def test_pool_i3d_statistics_returns_mean_and_std(self):
        sequence = np.vstack([
            np.zeros((1, 1024), dtype=np.float32),
            np.full((1, 1024), 2.0, dtype=np.float32),
        ])
        pooled = pool_i3d_statistics(sequence)
        self.assertEqual(pooled.shape, (2048,))
        np.testing.assert_allclose(pooled[:1024], 1.0)
        np.testing.assert_allclose(pooled[1024:], 1.0)

    def test_standardizer_fits_train_only(self):
        features = np.asarray([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
        state = fit_train_standardizer(features, ["train", "train"])
        transformed = apply_standardizer(features, state)
        np.testing.assert_allclose(transformed.mean(axis=0), 0.0, atol=1e-7)
        with self.assertRaisesRegex(ValueError, "train only"):
            fit_train_standardizer(features, ["train", "dev"])


class Task20NeuralModelTests(unittest.TestCase):
    def test_seed_helper_freezes_cublas_workspace_contract(self):
        with mock.patch.dict(os.environ, {"CUBLAS_WORKSPACE_CONFIG": "invalid"}):
            seed_everything(11)
            self.assertEqual(os.environ["CUBLAS_WORKSPACE_CONFIG"], ":4096:8")

    def test_pooled_mlp_outputs_distributions(self):
        model = PooledDistributionMLP(input_dim=4, hidden_dim=8, class_count=3, dropout=0.0)
        probabilities = model(torch.zeros((2, 4), dtype=torch.float32))
        self.assertEqual(tuple(probabilities.shape), (2, 3))
        torch.testing.assert_close(probabilities.sum(dim=1), torch.ones(2))

    def test_temporal_attention_ignores_masked_padding(self):
        torch.manual_seed(7)
        model = TemporalAttentionDistributionModel(input_dim=4, hidden_dim=8, class_count=3, dropout=0.0)
        model.eval()
        observed = torch.randn((1, 2, 4), dtype=torch.float32)
        padded_a = torch.cat([observed, torch.zeros((1, 2, 4))], dim=1)
        padded_b = torch.cat([observed, torch.full((1, 2, 4), 99.0)], dim=1)
        mask = torch.tensor([[True, True, False, False]])
        with torch.no_grad():
            output_a = model(padded_a, mask)
            output_b = model(padded_b, mask)
        torch.testing.assert_close(output_a, output_b)

    def test_temporal_attention_rejects_empty_observation_mask(self):
        model = TemporalAttentionDistributionModel(input_dim=4, hidden_dim=8, class_count=3, dropout=0.0)
        with self.assertRaisesRegex(ValueError, "observed"):
            model(torch.zeros((1, 2, 4)), torch.zeros((1, 2), dtype=torch.bool))


if __name__ == "__main__":
    unittest.main()
