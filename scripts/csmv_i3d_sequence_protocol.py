"""Deterministic preprocessing contract for frozen CSMV I3D sequences.

This module performs no fitting, label access, indexing, or model training.  It
only validates already acquired I3D arrays and applies the preregistered main
or sensitivity sequence rule identically across splits.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "csmv-i3d-sequence-protocol-v1.json"
FEATURE_DIMENSION = 1024
TARGET_STEPS = 180
DEFAULT_BUCKET_BOUNDARIES = (32, 64, 128, 256, 512, 1024, 2048)


class ProtocolViolation(ValueError):
    """Raised when an input or configuration violates the frozen protocol."""


def validate_feature_array(array: np.ndarray) -> np.ndarray:
    """Fail closed unless ``array`` is finite ``float32[T,1024]`` with T >= 1."""

    if not isinstance(array, np.ndarray):
        raise ProtocolViolation("I3D input must be a NumPy ndarray or memmap")
    if array.dtype != np.float32:
        raise ProtocolViolation("I3D dtype must be float32")
    if array.ndim != 2 or array.shape[0] < 1 or array.shape[1] != FEATURE_DIMENSION:
        raise ProtocolViolation("I3D shape must be [T,1024] with T >= 1")
    if not np.isfinite(array).all():
        raise ProtocolViolation("I3D input must contain only finite values")
    return array


def collate_full_sequences(
    arrays: Sequence[np.ndarray],
    *,
    max_padded_steps: int = 16384,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pad complete sequences to the batch maximum without truncation.

    The boolean mask uses ``True`` for an observed timestep and ``False`` for
    zero padding.  ``max_padded_steps`` caps only the raw input tensor; it is
    not a claim about total accelerator memory during future model training.
    """

    if not arrays:
        raise ProtocolViolation("cannot collate an empty batch")
    checked = [validate_feature_array(array) for array in arrays]
    lengths = np.asarray([array.shape[0] for array in checked], dtype=np.int64)
    maximum = int(lengths.max())
    padded_steps = len(checked) * maximum
    if max_padded_steps < 1 or padded_steps > max_padded_steps:
        raise ProtocolViolation(
            "batch requires {} padded steps, above frozen cap {}".format(
                padded_steps, max_padded_steps
            )
        )
    batch = np.zeros((len(checked), maximum, FEATURE_DIMENSION), dtype=np.float32)
    mask = np.zeros((len(checked), maximum), dtype=np.bool_)
    for row, array in enumerate(checked):
        length = array.shape[0]
        batch[row, :length] = array
        mask[row, :length] = True
    return batch, mask, lengths


def _fixed_180_output(array: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    output = np.zeros((TARGET_STEPS, FEATURE_DIMENSION), dtype=np.float32)
    mask = np.zeros((TARGET_STEPS,), dtype=np.bool_)
    return output, mask


def uniform_180_sensitivity(
    array: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply the primary 180-step sensitivity rule deterministically.

    Sequences at or below 180 steps are preserved and right-padded.  Longer
    sequences use 180 unique, monotonically increasing, endpoint-inclusive
    integer indices, chosen without labels or randomness.
    """

    array = validate_feature_array(array)
    output, mask = _fixed_180_output(array)
    length = array.shape[0]
    if length <= TARGET_STEPS:
        indices = np.arange(length, dtype=np.int64)
        output[:length] = array
        mask[:length] = True
        return output, mask, indices
    numerators = np.arange(TARGET_STEPS, dtype=np.int64) * (length - 1)
    indices = numerators // (TARGET_STEPS - 1)
    output[:] = array[indices]
    mask[:] = True
    return output, mask, indices


def first_180_supplementary(
    array: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Apply the preregistered supplementary first-180 diagnostic rule."""

    array = validate_feature_array(array)
    output, mask = _fixed_180_output(array)
    length = min(array.shape[0], TARGET_STEPS)
    indices = np.arange(length, dtype=np.int64)
    output[:length] = array[:length]
    mask[:length] = True
    return output, mask, indices


def _bucket_upper(length: int, boundaries: Sequence[int]) -> int:
    for boundary in boundaries:
        if length <= boundary:
            return int(boundary)
    return int(length)


def plan_deterministic_batches(
    lengths_by_item: Mapping[str, int],
    *,
    max_batch_size: int = 64,
    max_padded_steps: int = 16384,
    bucket_boundaries: Sequence[int] = DEFAULT_BUCKET_BOUNDARIES,
) -> List[dict]:
    """Create deterministic length-bucketed batches from input metadata only."""

    if max_batch_size < 1 or max_padded_steps < 1:
        raise ProtocolViolation("batch caps must be positive")
    if any(int(value) < 1 for value in lengths_by_item.values()):
        raise ProtocolViolation("all temporal lengths must be positive")
    rows = sorted(
        ((str(item), int(length)) for item, length in lengths_by_item.items()),
        key=lambda row: (_bucket_upper(row[1], bucket_boundaries), row[1], row[0]),
    )
    planned: List[dict] = []
    current: List[Tuple[str, int]] = []
    current_bucket: Optional[int] = None

    def flush() -> None:
        nonlocal current
        if not current:
            return
        maximum = max(length for _, length in current)
        planned.append(
            {
                "bucket_upper": current_bucket,
                "item_ids": [item for item, _ in current],
                "lengths": [length for _, length in current],
                "max_length": maximum,
                "padded_steps": len(current) * maximum,
            }
        )
        current = []

    for item, length in rows:
        bucket = _bucket_upper(length, bucket_boundaries)
        candidate = current + [(item, length)]
        candidate_max = max(value for _, value in candidate)
        exceeds = len(candidate) > max_batch_size or len(candidate) * candidate_max > max_padded_steps
        if current and (bucket != current_bucket or exceeds):
            flush()
            current_bucket = bucket
            candidate = [(item, length)]
        elif current_bucket is None:
            current_bucket = bucket
        if length > max_padded_steps:
            raise ProtocolViolation("single sequence exceeds frozen padded-step cap")
        current = candidate
    flush()
    return planned


def validate_protocol_config(config: Mapping[str, object]) -> None:
    required = {
        "schema_version": "csmv-i3d-sequence-protocol-v1",
        "selection_basis": "PRE_TEST_INPUT_LENGTH_AUDIT_ONLY",
        "main_protocol": "FULL_SEQUENCE_DYNAMIC_PADDING_MASK",
        "primary_sensitivity": "UNIFORM_180_ENDPOINT_INCLUSIVE",
        "dtype": "float32",
        "feature_dimension": FEATURE_DIMENSION,
        "mask_true_means": "OBSERVED_TIMESTEP",
    }
    for key, expected in required.items():
        if config.get(key) != expected:
            raise ProtocolViolation("invalid frozen config field: {}".format(key))
    if config.get("test_adaptation_allowed") is not False:
        raise ProtocolViolation("test-adaptive sequence processing is prohibited")
    if config.get("split_specific_overrides") != {}:
        raise ProtocolViolation("all splits must use one sequence rule without overrides")


def load_protocol_config(path: Path = DEFAULT_CONFIG) -> Dict[str, object]:
    config = json.loads(path.read_text(encoding="utf-8"))
    validate_protocol_config(config)
    return config
