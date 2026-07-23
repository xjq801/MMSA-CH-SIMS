import random
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def _runtime():
    import vccsa_resume_runtime

    return vccsa_resume_runtime


class _RandomDataset(Dataset):
    def __len__(self):
        return 12

    def __getitem__(self, index):
        return (
            index,
            random.random(),
            float(np.random.random()),
            float(torch.rand(())),
        )


class VccsaResumeRuntimeTests(unittest.TestCase):
    def test_atomic_checkpoint_roundtrip_restores_full_training_and_rng_state(self):
        runtime = _runtime()
        random.seed(3407)
        np.random.seed(3407)
        torch.manual_seed(3407)
        generator = torch.Generator().manual_seed(3407)
        model = torch.nn.Linear(3, 2)
        optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
        scheduler = torch.optim.lr_scheduler.LambdaLR(
            optimizer, lr_lambda=lambda step: 1.0 - step / 20.0
        )
        loss = model(torch.ones(2, 3)).sum()
        loss.backward()
        optimizer.step()
        scheduler.step()
        expected_parameters = {
            name: value.detach().clone() for name, value in model.state_dict().items()
        }

        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "last.ckpt"
            runtime.save_training_checkpoint(
                checkpoint,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                train_generator=generator,
                identity={
                    "seed": 3407,
                    "dataset": "CSMV",
                    "batch_size": 16,
                    "steps_per_epoch": 4692,
                },
                cursor={
                    "epoch_index": 3,
                    "next_batch_index": 117,
                    "global_step": 14193,
                    "tensorboard_steps": 283,
                    "epoch_start_generator_state": generator.get_state(),
                },
                training_state={
                    "epoch_loss": 1.25,
                    "epoch_op_loss": 0.5,
                    "epoch_em_loss": 0.75,
                    "best_eval_accuracy": 1.31,
                    "best_epoch": 3,
                    "eval_accuracies": [{"score": 1.31}],
                },
            )
            self.assertTrue(checkpoint.is_file())
            self.assertFalse(checkpoint.with_name(checkpoint.name + ".tmp").exists())
            expected_random = (
                random.random(),
                float(np.random.random()),
                float(torch.rand(())),
                torch.rand((), generator=generator).item(),
            )

            with torch.no_grad():
                for parameter in model.parameters():
                    parameter.add_(100)
            random.seed(9)
            np.random.seed(9)
            torch.manual_seed(9)
            generator.manual_seed(9)

            payload = runtime.load_training_checkpoint(
                checkpoint,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                train_generator=generator,
                expected_identity={
                    "seed": 3407,
                    "dataset": "CSMV",
                    "batch_size": 16,
                    "steps_per_epoch": 4692,
                },
            )
            observed_random = (
                random.random(),
                float(np.random.random()),
                float(torch.rand(())),
                torch.rand((), generator=generator).item(),
            )

        self.assertEqual(payload["cursor"]["next_batch_index"], 117)
        self.assertEqual(payload["training_state"]["best_epoch"], 3)
        self.assertEqual(scheduler.last_epoch, 1)
        self.assertEqual(expected_random, observed_random)
        for name, expected in expected_parameters.items():
            torch.testing.assert_close(model.state_dict()[name], expected)

    def test_identity_mismatch_fails_before_mutating_model(self):
        runtime = _runtime()
        model = torch.nn.Linear(2, 1)
        optimizer = torch.optim.AdamW(model.parameters())
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lambda _: 1.0)
        generator = torch.Generator().manual_seed(3407)
        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "last.ckpt"
            runtime.save_training_checkpoint(
                checkpoint,
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                train_generator=generator,
                identity={"seed": 3407, "dataset": "CSMV"},
                cursor={
                    "epoch_index": 0,
                    "next_batch_index": 0,
                    "global_step": 0,
                    "tensorboard_steps": 0,
                    "epoch_start_generator_state": generator.get_state(),
                },
                training_state={},
            )
            original = {
                name: value.detach().clone() for name, value in model.state_dict().items()
            }
            with self.assertRaisesRegex(ValueError, "identity mismatch"):
                runtime.load_training_checkpoint(
                    checkpoint,
                    model=model,
                    optimizer=optimizer,
                    scheduler=scheduler,
                    train_generator=generator,
                    expected_identity={"seed": 99, "dataset": "CSMV"},
                )
        for name, expected in original.items():
            torch.testing.assert_close(model.state_dict()[name], expected)

    def test_mid_epoch_replay_returns_exact_next_batch_and_rng_stream(self):
        runtime = _runtime()
        random.seed(3407)
        np.random.seed(3407)
        torch.manual_seed(3407)
        generator = torch.Generator().manual_seed(3407)
        loader = DataLoader(
            _RandomDataset(),
            batch_size=2,
            shuffle=True,
            num_workers=0,
            generator=generator,
        )
        epoch_start_generator_state = generator.get_state()
        iterator = iter(loader)
        next(iterator)
        next(iterator)
        checkpoint_rng_state = runtime.capture_rng_state(generator)
        expected = next(iterator)
        expected_following_rng = (
            random.random(),
            float(np.random.random()),
            float(torch.rand(())),
        )

        random.seed(1)
        np.random.seed(1)
        torch.manual_seed(1)
        generator.manual_seed(1)
        resumed_iterator = runtime.resume_batch_iterator(
            loader,
            next_batch_index=2,
            train_generator=generator,
            epoch_start_generator_state=epoch_start_generator_state,
            checkpoint_rng_state=checkpoint_rng_state,
        )
        observed = next(resumed_iterator)
        observed_following_rng = (
            random.random(),
            float(np.random.random()),
            float(torch.rand(())),
        )

        for expected_tensor, observed_tensor in zip(expected, observed):
            torch.testing.assert_close(expected_tensor, observed_tensor)
        self.assertEqual(expected_following_rng, observed_following_rng)

    def test_resume_requires_single_process_loader_for_exact_replay(self):
        runtime = _runtime()
        loader = DataLoader(_RandomDataset(), num_workers=1)
        with self.assertRaisesRegex(ValueError, "num_workers=0"):
            runtime.require_exact_resume_loader(loader)


if __name__ == "__main__":
    unittest.main()
