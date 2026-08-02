from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
import zipfile

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_data import (
    derive_train_only_privileged_inputs,
    load_pooled_content_features,
    make_mismatched_privileged_features,
    stable_csmv_item_id,
)


CLASS_ORDER = ("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust")


class Task30DataBoundaryTests(unittest.TestCase):
    def test_derivation_emits_only_formal_train_videos_and_no_comment_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            train_raw = "100"
            dev_raw = "200"
            train_id = stable_csmv_item_id(train_raw)
            dev_id = stable_csmv_item_id(dev_raw)
            labels = root / "labels.jsonl"
            labels.write_text(
                "".join(
                    json.dumps(row) + "\n"
                    for row in (
                        {"item_id": train_id, "split": {"group_by_video_v1": "train"}},
                        {"item_id": dev_id, "split": {"group_by_video_v1": "dev"}},
                    )
                ),
                encoding="utf-8",
            )
            video_map = root / "video_to_comment.json"
            video_map.write_text(json.dumps({"100.mp4": ["c1", "c2"], "200.mp4": ["c3"]}), encoding="utf-8")
            archive = root / "labels.zip"
            annotation = {
                "c1": {"video_file_id": "100.mp4", "comment": "private-a", "emotion_label": "joy", "opinion_label": "positive", "hashtag": "x"},
                "c2": {"video_file_id": "100.mp4", "comment": "private-b", "emotion_label": "sadness", "opinion_label": "negative", "hashtag": "x"},
                "c3": {"video_file_id": "200.mp4", "comment": "must-not-escape", "emotion_label": "anger", "opinion_label": "neutral", "hashtag": "y"},
            }
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("lable_data_dict.json", json.dumps(annotation))

            result = derive_train_only_privileged_inputs(labels, video_map, archive, CLASS_ORDER)

            self.assertEqual(result["sample_ids"], [train_id])
            self.assertEqual(result["response_counts"].tolist(), [2])
            self.assertEqual(result["privileged_features"].shape, (1, 12))
            self.assertTrue(np.isfinite(result["privileged_features"]).all())
            self.assertNotIn("comment", str(result).lower())
            self.assertNotIn("private", str(result).lower())
            self.assertEqual(result["source_hashes"]["annotation_archive"], hashlib.sha256(archive.read_bytes()).hexdigest())

    def test_derivation_fails_closed_on_missing_annotation_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            item_id = stable_csmv_item_id("100")
            labels = root / "labels.jsonl"
            labels.write_text(json.dumps({"item_id": item_id, "split": {"group_by_video_v1": "train"}}) + "\n", encoding="utf-8")
            video_map = root / "video_to_comment.json"
            video_map.write_text(json.dumps({"100.mp4": ["c1"]}), encoding="utf-8")
            archive = root / "labels.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("lable_data_dict.json", json.dumps({"c1": {"video_file_id": "100.mp4"}}))
            with self.assertRaisesRegex(ValueError, "missing"):
                derive_train_only_privileged_inputs(labels, video_map, archive, CLASS_ORDER)

    def test_derivation_tracks_released_null_labels_without_inventing_a_class(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            item_id = stable_csmv_item_id("100")
            labels = root / "labels.jsonl"
            labels.write_text(json.dumps({"item_id": item_id, "split": {"group_by_video_v1": "train"}, "response_count": 2}) + "\n", encoding="utf-8")
            video_map = root / "video_to_comment.json"
            video_map.write_text(json.dumps({"100.mp4": ["c1", "c2"]}), encoding="utf-8")
            archive = root / "labels.zip"
            annotation = {
                "c1": {"video_file_id": "100.mp4", "comment": "x", "emotion_label": "joy", "opinion_label": "positive"},
                "c2": {"video_file_id": "100.mp4", "comment": "y", "emotion_label": None, "opinion_label": None},
            }
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("lable_data_dict.json", json.dumps(annotation))
            result = derive_train_only_privileged_inputs(labels, video_map, archive, CLASS_ORDER)
            self.assertEqual(result["audit"]["missing_emotion_label_count"], 1)
            self.assertEqual(result["audit"]["missing_opinion_label_count"], 1)
            self.assertEqual(result["response_counts"].tolist(), [2])
            self.assertAlmostEqual(float(result["privileged_features"][0, CLASS_ORDER.index("joy")]), 1.0)

    def test_pooled_content_features_reject_nonfinite_and_preserve_order(self):
        arrays = {
            "a": np.asarray([[1.0, 3.0], [3.0, 5.0]], dtype=np.float32),
            "b": np.asarray([[2.0, 4.0]], dtype=np.float32),
        }
        actual = load_pooled_content_features(["b", "a"], arrays.__getitem__)
        np.testing.assert_allclose(actual, [[2.0, 4.0], [2.0, 4.0]])
        arrays["b"] = np.asarray([[np.nan, 4.0]], dtype=np.float32)
        with self.assertRaisesRegex(ValueError, "finite"):
            load_pooled_content_features(["b"], arrays.__getitem__)

    def test_mismatched_privileged_features_are_deterministic_and_deranged(self):
        values = np.arange(20, dtype=np.float32).reshape(5, 4)
        first, first_sources = make_mismatched_privileged_features(values, seed=19)
        second, second_sources = make_mismatched_privileged_features(values, seed=19)
        np.testing.assert_array_equal(first, second)
        np.testing.assert_array_equal(first_sources, second_sources)
        self.assertTrue(np.all(first_sources != np.arange(5)))
        self.assertEqual(first.shape, values.shape)


if __name__ == "__main__":
    unittest.main()
