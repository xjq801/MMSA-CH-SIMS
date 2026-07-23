"""Crash-safe checkpoint primitives for the Task20 VC-CSA author runtime.

This module deliberately contains no project data or endpoint information.  The
author-source patch copies it beside ``main.py`` as ``resume_utils.py``.
"""

import os
from pathlib import Path
import random
from typing import Any, Dict, Mapping, Optional

import numpy as np
import torch


CHECKPOINT_SCHEMA = "task20-vccsa-exact-resume-v1"


def capture_rng_state(
    train_generator: Optional[torch.Generator] = None,
) -> Dict[str, Any]:
    state = {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
        "train_generator": None,
    }
    if train_generator is not None:
        state["train_generator"] = train_generator.get_state()
    return state


def restore_rng_state(
    state: Mapping[str, Any],
    train_generator: Optional[torch.Generator] = None,
) -> None:
    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch_cpu"])
    cuda_states = state.get("torch_cuda", [])
    if cuda_states and torch.cuda.is_available():
        if len(cuda_states) != torch.cuda.device_count():
            raise ValueError("CUDA RNG device count mismatch")
        torch.cuda.set_rng_state_all(cuda_states)
    generator_state = state.get("train_generator")
    if train_generator is not None and generator_state is not None:
        train_generator.set_state(generator_state)


def require_exact_resume_loader(train_loader: Any) -> None:
    if getattr(train_loader, "num_workers", None) != 0:
        raise ValueError("exact mid-epoch resume requires DataLoader num_workers=0")
    if getattr(train_loader, "generator", None) is None:
        raise ValueError("exact mid-epoch resume requires an explicit train generator")


def resume_batch_iterator(
    train_loader: Any,
    *,
    next_batch_index: int,
    train_generator: torch.Generator,
    epoch_start_generator_state: torch.Tensor,
    checkpoint_rng_state: Mapping[str, Any],
) -> Any:
    """Rebuild the epoch permutation, discard durable batches, and resume exactly.

    Dataset reads performed while replaying the cursor can consume Python, NumPy,
    or Torch randomness.  Restoring the post-checkpoint RNG state after the
    discard prevents those reads from advancing the resumed stream twice.
    """

    require_exact_resume_loader(train_loader)
    if next_batch_index < 0 or next_batch_index > len(train_loader):
        raise ValueError("resume next_batch_index is outside the loader")
    train_generator.set_state(epoch_start_generator_state)
    iterator = iter(train_loader)
    for _ in range(next_batch_index):
        try:
            next(iterator)
        except StopIteration as exc:
            raise ValueError("resume cursor exceeds the loader") from exc
    restore_rng_state(checkpoint_rng_state, train_generator)
    return iterator


def _atomic_torch_save(payload: Mapping[str, Any], path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    try:
        torch.save(dict(payload), str(temporary))
        with temporary.open("r+b") as handle:
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary), str(path))
        try:
            directory_fd = os.open(str(path.parent), os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def save_training_checkpoint(
    path: Path,
    *,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    train_generator: torch.Generator,
    identity: Mapping[str, Any],
    cursor: Mapping[str, Any],
    training_state: Mapping[str, Any],
) -> None:
    required_cursor = {
        "epoch_index",
        "next_batch_index",
        "global_step",
        "tensorboard_steps",
        "epoch_start_generator_state",
    }
    missing = required_cursor.difference(cursor)
    if missing:
        raise ValueError("checkpoint cursor missing: " + ", ".join(sorted(missing)))
    payload = {
        "schema": CHECKPOINT_SCHEMA,
        "identity": dict(identity),
        "cursor": dict(cursor),
        "training_state": dict(training_state),
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
        "rng_state": capture_rng_state(train_generator),
    }
    _atomic_torch_save(payload, Path(path))


def _torch_load(path: Path, map_location: Any) -> Mapping[str, Any]:
    try:
        return torch.load(str(path), map_location=map_location, weights_only=False)
    except TypeError:
        return torch.load(str(path), map_location=map_location)


def load_training_checkpoint(
    path: Path,
    *,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    train_generator: torch.Generator,
    expected_identity: Mapping[str, Any],
    map_location: Any = "cpu",
) -> Dict[str, Any]:
    payload = dict(_torch_load(Path(path), map_location))
    if payload.get("schema") != CHECKPOINT_SCHEMA:
        raise ValueError("unsupported resume checkpoint schema")
    if payload.get("identity") != dict(expected_identity):
        raise ValueError(
            "resume checkpoint identity mismatch: expected exact seed/data/loader contract"
        )
    required = {
        "cursor",
        "training_state",
        "model_state_dict",
        "optimizer_state_dict",
        "scheduler_state_dict",
        "rng_state",
    }
    missing = required.difference(payload)
    if missing:
        raise ValueError("resume checkpoint missing: " + ", ".join(sorted(missing)))

    model.load_state_dict(payload["model_state_dict"])
    optimizer.load_state_dict(payload["optimizer_state_dict"])
    scheduler.load_state_dict(payload["scheduler_state_dict"])
    restore_rng_state(payload["rng_state"], train_generator)
    return payload
