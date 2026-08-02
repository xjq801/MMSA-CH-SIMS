from pathlib import Path
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_training import StudentTrialConfig, fit_teacher_train_logits, train_student_trial


class Task30TrainingTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.RandomState(7)
        self.train_x = rng.normal(size=(24, 5)).astype(np.float32)
        self.dev_x = rng.normal(size=(8, 5)).astype(np.float32)
        raw_train = rng.uniform(size=(24, 3))
        raw_dev = rng.uniform(size=(8, 3))
        self.train_y = (raw_train / raw_train.sum(axis=1, keepdims=True)).astype(np.float32)
        self.dev_y = (raw_dev / raw_dev.sum(axis=1, keepdims=True)).astype(np.float32)
        self.config = StudentTrialConfig(
            hidden_dim=8,
            dropout=0.0,
            learning_rate=0.01,
            max_epochs=3,
            patience=3,
            batch_size=8,
            head="softmax",
            temperature=2.0,
            kd_weight=0.5,
        )

    def test_preprocessing_rejects_nontrain_fit_labels(self):
        labels = ["train"] * len(self.train_x)
        labels[-1] = "dev"
        with self.assertRaisesRegex(ValueError, "train"):
            train_student_trial(
                self.train_x, self.train_y, labels, self.dev_x, self.dev_y,
                supervision="soft", config=self.config, seed=5, device="cpu"
            )

    def test_softmax_and_dirichlet_trials_return_finite_normalized_predictions(self):
        for head in ("softmax", "dirichlet"):
            with self.subTest(head=head):
                config = StudentTrialConfig(**dict(self.config.__dict__, head=head))
                result = train_student_trial(
                    self.train_x, self.train_y, ["train"] * len(self.train_x),
                    self.dev_x, self.dev_y, supervision="soft", config=config,
                    seed=5, device="cpu"
                )
                self.assertEqual(result["dev_predictions"].shape, self.dev_y.shape)
                self.assertTrue(np.isfinite(result["dev_predictions"]).all())
                np.testing.assert_allclose(result["dev_predictions"].sum(axis=1), 1.0, atol=1e-6)
                self.assertTrue(all(np.isfinite(row["max_gradient_norm"]) for row in result["history"]))

    def test_kd_requires_finite_shape_matched_teacher_logits(self):
        with self.assertRaisesRegex(ValueError, "teacher"):
            train_student_trial(
                self.train_x, self.train_y, ["train"] * len(self.train_x),
                self.dev_x, self.dev_y, supervision="kd", config=self.config,
                seed=5, device="cpu"
            )
        with self.assertRaisesRegex(ValueError, "teacher"):
            train_student_trial(
                self.train_x, self.train_y, ["train"] * len(self.train_x),
                self.dev_x, self.dev_y, supervision="kd", config=self.config,
                seed=5, device="cpu", teacher_train_logits=np.zeros((24, 2), dtype=np.float32)
            )

    def test_hard_supervision_uses_same_student_contract(self):
        result = train_student_trial(
            self.train_x, self.train_y, ["train"] * len(self.train_x),
            self.dev_x, self.dev_y, supervision="hard", config=self.config,
            seed=5, device="cpu"
        )
        self.assertEqual(result["supervision"], "hard")

    def test_teacher_logits_support_content_only_and_train_privileged_modes(self):
        privileged = np.concatenate(
            (self.train_y, np.zeros((len(self.train_y), 2), dtype=np.float32)), axis=1
        )
        ordinary = fit_teacher_train_logits(
            self.train_x, self.train_y, ["train"] * len(self.train_x),
            privileged_features=None, hidden_dim=8, dropout=0.0,
            learning_rate=0.01, max_epochs=2, batch_size=8, seed=11, device="cpu"
        )
        privileged_result = fit_teacher_train_logits(
            self.train_x, self.train_y, ["train"] * len(self.train_x),
            privileged_features=privileged, hidden_dim=8, dropout=0.0,
            learning_rate=0.01, max_epochs=2, batch_size=8, seed=11, device="cpu"
        )
        self.assertEqual(ordinary["train_logits"].shape, self.train_y.shape)
        self.assertEqual(privileged_result["train_logits"].shape, self.train_y.shape)
        self.assertTrue(np.isfinite(privileged_result["train_logits"]).all())
        self.assertEqual(ordinary["teacher_mode"], "content_only")
        self.assertEqual(privileged_result["teacher_mode"], "train_response_privileged")

    def test_teacher_rejects_nontrain_fit_and_misaligned_privileged_features(self):
        with self.assertRaisesRegex(ValueError, "train"):
            fit_teacher_train_logits(
                self.train_x, self.train_y, ["dev"] * len(self.train_x),
                privileged_features=None, hidden_dim=8, dropout=0.0,
                learning_rate=0.01, max_epochs=2, batch_size=8, seed=11, device="cpu"
            )
        with self.assertRaisesRegex(ValueError, "privileged"):
            fit_teacher_train_logits(
                self.train_x, self.train_y, ["train"] * len(self.train_x),
                privileged_features=np.zeros((23, 2), dtype=np.float32), hidden_dim=8,
                dropout=0.0, learning_rate=0.01, max_epochs=2, batch_size=8,
                seed=11, device="cpu"
            )


if __name__ == "__main__":
    unittest.main()
