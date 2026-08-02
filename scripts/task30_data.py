"""Read-only Task30 adapters that emit no response text or user identifiers."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import random
from typing import Callable, Dict, Sequence
import zipfile

import numpy as np


_OPINION_ORDER = ("positive", "neutral", "negative")
_ANNOTATION_FIELDS = {"video_file_id", "emotion_label", "opinion_label"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_csmv_item_id(video_file_id: str) -> str:
    stem = Path(str(video_file_id)).stem
    if not stem or not stem.isdigit():
        raise ValueError("CSMV video_file_id must be numeric")
    return hashlib.sha256(("csmv-video-v1|" + stem + ".mp4").encode("utf-8")).hexdigest()


def _load_formal_train_ids(labels_path: Path, split_scheme: str) -> Dict[str, int]:
    train_ids: Dict[str, int] = {}
    seen = set()
    with Path(labels_path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            row = json.loads(line)
            missing = {"item_id", "split"} - set(row)
            if missing:
                raise ValueError("canonical label row missing fields")
            item_id = str(row["item_id"])
            if item_id in seen:
                raise ValueError("duplicate canonical item_id")
            seen.add(item_id)
            split = row["split"]
            if not isinstance(split, dict) or split_scheme not in split:
                raise ValueError("canonical label row missing split scheme")
            if split[split_scheme] == "train":
                response_count = row.get("response_count")
                if response_count is not None and (
                    not isinstance(response_count, int)
                    or isinstance(response_count, bool)
                    or response_count <= 0
                ):
                    raise ValueError("invalid canonical response_count")
                train_ids[item_id] = response_count
    if not train_ids:
        raise ValueError("formal train split is empty")
    return train_ids


def _load_annotation_dictionary(annotation_archive: Path) -> Dict[str, object]:
    with zipfile.ZipFile(annotation_archive) as archive:
        members = [row for row in archive.infolist() if not row.is_dir() and row.filename.lower().endswith(".json")]
        if len(members) != 1:
            raise ValueError("annotation archive must contain exactly one JSON member")
        value = json.loads(archive.read(members[0]).decode("utf-8"))
    if not isinstance(value, dict) or not value:
        raise ValueError("annotation dictionary must be a non-empty object")
    return value


def derive_train_only_privileged_inputs(
    labels_path: Path,
    video_map_path: Path,
    annotation_archive: Path,
    class_order: Sequence[str],
    split_scheme: str = "group_by_video_v1",
) -> Dict[str, object]:
    """Derive aggregate train-video reaction features without returning response text."""
    classes = tuple(str(value) for value in class_order)
    if len(classes) < 2 or len(set(classes)) != len(classes):
        raise ValueError("class_order must contain unique labels")
    class_index = {label: index for index, label in enumerate(classes)}
    opinion_index = {label: index for index, label in enumerate(_OPINION_ORDER)}
    train_ids = _load_formal_train_ids(Path(labels_path), split_scheme)
    video_map = json.loads(Path(video_map_path).read_text(encoding="utf-8"))
    if not isinstance(video_map, dict):
        raise ValueError("video map must be an object")
    annotations = _load_annotation_dictionary(Path(annotation_archive))

    rows = []
    observed_train_ids = set()
    label_counts = Counter()
    total_responses = 0
    missing_emotion_label_count = 0
    missing_opinion_label_count = 0
    for raw_video_id, comment_ids in video_map.items():
        item_id = stable_csmv_item_id(str(raw_video_id))
        if item_id not in train_ids:
            continue
        if not isinstance(comment_ids, list) or not comment_ids:
            raise ValueError("train video comment membership must be non-empty")
        emotion = np.zeros(len(classes), dtype=np.float64)
        opinion = np.zeros(len(_OPINION_ORDER), dtype=np.float64)
        for comment_id in comment_ids:
            if comment_id not in annotations or not isinstance(annotations[comment_id], dict):
                raise ValueError("missing train annotation")
            annotation = annotations[comment_id]
            missing = _ANNOTATION_FIELDS - set(annotation)
            if missing:
                raise ValueError("train annotation missing fields")
            if stable_csmv_item_id(str(annotation["video_file_id"])) != item_id:
                raise ValueError("annotation/video membership mismatch")
            emotion_value = annotation["emotion_label"]
            opinion_value = annotation["opinion_label"]
            if emotion_value is None:
                missing_emotion_label_count += 1
            else:
                emotion_label = str(emotion_value)
                if emotion_label not in class_index:
                    raise ValueError("annotation emotion label outside frozen class order")
                emotion[class_index[emotion_label]] += 1.0
                label_counts[emotion_label] += 1
            if opinion_value is None:
                missing_opinion_label_count += 1
            else:
                opinion_label = str(opinion_value)
                if opinion_label not in opinion_index:
                    raise ValueError("annotation opinion label outside frozen class order")
                opinion[opinion_index[opinion_label]] += 1.0
        count = len(comment_ids)
        expected_count = train_ids[item_id]
        if expected_count is not None and expected_count != count:
            raise ValueError("canonical/raw train response_count mismatch")
        emotion_total = float(emotion.sum())
        opinion_total = float(opinion.sum())
        if emotion_total <= 0.0 or opinion_total <= 0.0:
            raise ValueError("train video cannot have all reaction labels missing")
        emotion /= emotion_total
        opinion /= opinion_total
        privileged = np.concatenate((emotion, opinion, np.asarray([np.log1p(count)], dtype=np.float64)))
        rows.append((item_id, count, privileged.astype(np.float32)))
        observed_train_ids.add(item_id)
        total_responses += count
    if observed_train_ids != set(train_ids):
        raise ValueError("formal train videos are not exactly covered by the comment map")
    rows.sort(key=lambda row: row[0])
    features = np.vstack([row[2] for row in rows])
    if not np.isfinite(features).all():
        raise ValueError("privileged features must be finite")
    return {
        "schema_version": "task30-train-privileged-input-v1",
        "sample_ids": [row[0] for row in rows],
        "privileged_features": features,
        "response_counts": np.asarray([row[1] for row in rows], dtype=np.int64),
        "audit": {
            "train_video_count": len(rows),
            "train_response_count": total_responses,
            "class_counts": {label: int(label_counts[label]) for label in classes},
            "missing_emotion_label_count": missing_emotion_label_count,
            "missing_opinion_label_count": missing_opinion_label_count,
            "privacy_boundary": "AGGREGATES_ONLY_NO_RESPONSE_TEXT_OR_USER_IDS",
        },
        "source_hashes": {
            "canonical_labels": _sha256(Path(labels_path)),
            "video_map": _sha256(Path(video_map_path)),
            "annotation_archive": _sha256(Path(annotation_archive)),
        },
    }


def load_pooled_content_features(
    sample_ids: Sequence[str],
    load_sequence: Callable[[str], np.ndarray],
) -> np.ndarray:
    normalized_ids = [str(value) for value in sample_ids]
    if not normalized_ids or len(set(normalized_ids)) != len(normalized_ids):
        raise ValueError("sample_ids must be non-empty and unique")
    pooled = []
    feature_dim = None
    for sample_id in normalized_ids:
        sequence = np.asarray(load_sequence(sample_id))
        if sequence.ndim != 2 or sequence.shape[0] < 1 or sequence.shape[1] < 1:
            raise ValueError("content sequence must be a non-empty matrix")
        if sequence.dtype != np.float32:
            raise ValueError("content sequence must use float32")
        if not np.isfinite(sequence).all():
            raise ValueError("content sequence must be finite")
        if feature_dim is None:
            feature_dim = sequence.shape[1]
        elif sequence.shape[1] != feature_dim:
            raise ValueError("content feature dimensions do not match")
        pooled.append(sequence.mean(axis=0, dtype=np.float64).astype(np.float32))
    return np.vstack(pooled)


def make_mismatched_privileged_features(values: np.ndarray, seed: int):
    matrix = np.asarray(values, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[0] < 2 or not np.isfinite(matrix).all():
        raise ValueError("mismatched privileged features require a finite matrix with at least two rows")
    shift = random.Random(seed).randrange(1, matrix.shape[0])
    source_indices = (np.arange(matrix.shape[0], dtype=np.int64) + shift) % matrix.shape[0]
    return matrix[source_indices].copy(), source_indices
