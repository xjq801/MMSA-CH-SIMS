from pathlib import Path
import math
import os
import random
import sys
import unittest
from unittest import mock

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_models import (
    ContentOnlyStudent,
    ResponsePrivilegedTeacher,
    hard_label_loss,
    kd_loss,
    seed_everything,
    soft_distribution_loss,
)


class Task30ModelTests(unittest.TestCase):
    def test_seed_helper_covers_python_numpy_torch_and_deterministic_contract(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            seed_everything(31)
            first = (random.random(), float(np.random.rand()), float(torch.rand(1)))
            seed_everything(31)
            second = (random.random(), float(np.random.rand()), float(torch.rand(1)))
            self.assertEqual(first, second)
            self.assertEqual(os.environ["PYTHONHASHSEED"], "31")
            self.assertEqual(os.environ["CUBLAS_WORKSPACE_CONFIG"], ":4096:8")
            self.assertFalse(torch.backends.cudnn.benchmark)
            self.assertTrue(torch.backends.cudnn.deterministic)

    def test_student_forward_is_content_only_and_returns_finite_normalized_distribution(self):
        model = ContentOnlyStudent(input_dim=4, hidden_dim=6, class_count=3, dropout=0.0)
        features = torch.zeros((2, 4), dtype=torch.float32)
        logits = model.logits(features)
        output = model(features)
        self.assertEqual(tuple(logits.shape), (2, 3))
        torch.testing.assert_close(output, torch.softmax(logits, dim=1))
        self.assertEqual(tuple(output.shape), (2, 3))
        self.assertTrue(bool(torch.isfinite(output).all()))
        torch.testing.assert_close(output.sum(dim=1), torch.ones(2))
        with self.assertRaises(TypeError):
            model(torch.zeros((2, 4)), comment_text=["not allowed", "not allowed"])

    def test_teacher_uses_separate_privileged_summary_and_dynamic_head(self):
        model = ResponsePrivilegedTeacher(
            content_dim=4,
            privileged_dim=2,
            hidden_dim=6,
            class_count=5,
            dropout=0.0,
        )
        content = torch.zeros((2, 4))
        privileged = torch.zeros((2, 2))
        logits = model.logits(content, privileged)
        output = model(content, privileged)
        torch.testing.assert_close(output, torch.softmax(logits, dim=1))
        self.assertEqual(tuple(output.shape), (2, 5))
        torch.testing.assert_close(output.sum(dim=1), torch.ones(2))


class Task30LossGoldTests(unittest.TestCase):
    def test_hard_label_loss_matches_hand_calculation(self):
        logits = torch.log(torch.tensor([[0.75, 0.25]], dtype=torch.float64))
        loss = hard_label_loss(logits, torch.tensor([0]))
        self.assertAlmostEqual(float(loss), -math.log(0.75), places=12)

    def test_soft_distribution_loss_matches_hand_calculation(self):
        logits = torch.log(torch.tensor([[0.75, 0.25]], dtype=torch.float64))
        targets = torch.tensor([[0.25, 0.75]], dtype=torch.float64)
        loss = soft_distribution_loss(logits, targets)
        expected = -(0.25 * math.log(0.75) + 0.75 * math.log(0.25))
        self.assertAlmostEqual(float(loss), expected, places=12)

    def test_kd_loss_is_zero_for_identical_logits(self):
        logits = torch.tensor([[0.2, -0.1, 0.7]], dtype=torch.float64)
        loss = kd_loss(logits, logits.clone(), temperature=2.0)
        self.assertAlmostEqual(float(loss), 0.0, places=12)

    def test_losses_reject_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            soft_distribution_loss(
                torch.tensor([[0.0, float("nan")]]),
                torch.tensor([[0.5, 0.5]]),
            )
        with self.assertRaisesRegex(ValueError, "finite"):
            kd_loss(
                torch.tensor([[0.0, 1.0]]),
                torch.tensor([[0.0, float("inf")]]),
                temperature=1.0,
            )


if __name__ == "__main__":
    unittest.main()
