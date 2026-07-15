"""Contract tests for the preregistered CSMV I3D sequence protocol."""

from __future__ import annotations

import hashlib
import unittest

import numpy as np

from scripts.csmv_i3d_sequence_protocol import (
    ProtocolViolation,
    collate_full_sequences,
    first_180_supplementary,
    plan_deterministic_batches,
    uniform_180_sensitivity,
    validate_feature_array,
    validate_protocol_config,
)


def array_digest(array: np.ndarray) -> str:
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


class CsmvI3dSequenceProtocolTests(unittest.TestCase):
    def feature(self, length: int, offset: float = 0.0) -> np.ndarray:
        values = np.arange(length * 1024, dtype=np.float32).reshape(length, 1024)
        return values + np.float32(offset)

    def test_full_sequence_collation_preserves_values_and_masks_padding(self) -> None:
        first = self.feature(6)
        second = self.feature(9, offset=1.0)
        batch, mask, lengths = collate_full_sequences([first, second])
        self.assertEqual(batch.shape, (2, 9, 1024))
        self.assertEqual(mask.shape, (2, 9))
        self.assertEqual(batch.dtype, np.float32)
        self.assertEqual(mask.dtype, np.bool_)
        self.assertEqual(lengths.tolist(), [6, 9])
        np.testing.assert_array_equal(batch[0, :6], first)
        np.testing.assert_array_equal(batch[1], second)
        self.assertTrue(mask[0, :6].all())
        self.assertFalse(mask[0, 6:].any())
        self.assertTrue(mask[1].all())
        self.assertTrue(np.equal(batch[0, 6:], 0.0).all())

    def test_full_sequence_boundary_accepts_longest_observed_length(self) -> None:
        longest = np.zeros((1719, 1024), dtype=np.float32)
        batch, mask, lengths = collate_full_sequences([longest])
        self.assertEqual(batch.shape, (1, 1719, 1024))
        self.assertTrue(mask.all())
        self.assertEqual(lengths.tolist(), [1719])

    def test_uniform_180_is_deterministic_and_covers_both_endpoints(self) -> None:
        source = self.feature(1719)
        first, first_mask, first_indices = uniform_180_sensitivity(source)
        second, second_mask, second_indices = uniform_180_sensitivity(source)
        self.assertEqual(first.shape, (180, 1024))
        self.assertTrue(first_mask.all())
        self.assertEqual(first_indices[0], 0)
        self.assertEqual(first_indices[-1], 1718)
        self.assertEqual(len(np.unique(first_indices)), 180)
        np.testing.assert_array_equal(first, second)
        np.testing.assert_array_equal(first_mask, second_mask)
        np.testing.assert_array_equal(first_indices, second_indices)
        self.assertEqual(array_digest(first), array_digest(second))

    def test_uniform_180_pads_short_sequences_without_repeating_observations(self) -> None:
        source = self.feature(6)
        output, mask, indices = uniform_180_sensitivity(source)
        self.assertEqual(output.shape, (180, 1024))
        np.testing.assert_array_equal(output[:6], source)
        self.assertTrue(np.equal(output[6:], 0.0).all())
        self.assertEqual(mask.sum(), 6)
        self.assertEqual(indices.tolist(), [0, 1, 2, 3, 4, 5])

    def test_first_180_is_only_a_deterministic_supplementary_rule(self) -> None:
        source = self.feature(200)
        output, mask, indices = first_180_supplementary(source)
        self.assertEqual(output.shape, (180, 1024))
        self.assertTrue(mask.all())
        self.assertEqual(indices.tolist(), list(range(180)))
        self.assertFalse(np.array_equal(output, uniform_180_sensitivity(source)[0]))

    def test_invalid_shapes_dtype_and_nonfinite_values_fail_closed(self) -> None:
        invalid = (
            np.empty((0, 1024), dtype=np.float32),
            np.empty((3,), dtype=np.float32),
            np.empty((3, 512), dtype=np.float32),
            np.empty((3, 1024), dtype=np.float64),
        )
        for value in invalid:
            with self.subTest(shape=value.shape, dtype=str(value.dtype)):
                with self.assertRaises(ProtocolViolation):
                    validate_feature_array(value)
        nonfinite = np.zeros((3, 1024), dtype=np.float32)
        nonfinite[1, 1] = np.nan
        with self.assertRaises(ProtocolViolation):
            validate_feature_array(nonfinite)

    def test_batch_plan_is_deterministic_and_respects_input_tensor_cap(self) -> None:
        lengths = {"a": 6, "b": 43, "c": 180, "d": 181, "e": 1719}
        first = plan_deterministic_batches(lengths, max_batch_size=64, max_padded_steps=16384)
        second = plan_deterministic_batches(lengths, max_batch_size=64, max_padded_steps=16384)
        self.assertEqual(first, second)
        self.assertEqual(sorted(item for batch in first for item in batch["item_ids"]), sorted(lengths))
        for batch in first:
            self.assertLessEqual(batch["padded_steps"], 16384)

    def test_config_rejects_test_adaptation_and_split_specific_overrides(self) -> None:
        valid = {
            "schema_version": "csmv-i3d-sequence-protocol-v1",
            "selection_basis": "PRE_TEST_INPUT_LENGTH_AUDIT_ONLY",
            "main_protocol": "FULL_SEQUENCE_DYNAMIC_PADDING_MASK",
            "primary_sensitivity": "UNIFORM_180_ENDPOINT_INCLUSIVE",
            "split_specific_overrides": {},
            "test_adaptation_allowed": False,
            "dtype": "float32",
            "feature_dimension": 1024,
            "mask_true_means": "OBSERVED_TIMESTEP",
        }
        validate_protocol_config(valid)
        bad_adaptation = dict(valid, test_adaptation_allowed=True)
        with self.assertRaises(ProtocolViolation):
            validate_protocol_config(bad_adaptation)
        bad_override = dict(valid, split_specific_overrides={"test": {"max_steps": 180}})
        with self.assertRaises(ProtocolViolation):
            validate_protocol_config(bad_override)


if __name__ == "__main__":
    unittest.main()
