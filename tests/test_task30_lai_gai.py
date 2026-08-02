from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_lai_gai import load_lai_gai_train_dev, run_lai_gai_boundary


class Task30LaiGaiBoundaryTests(unittest.TestCase):
    def _fixture(self, root):
        classes = ("a", "b", "c")
        rows = []
        for index, split in enumerate(("train", "train", "dev", "test")):
            name = "image-{}.png".format(index)
            path = root / name
            Image.new("RGB", (8, 8), color=(index * 30, 40, 80)).save(path)
            rows.append({
                "item_id": "item-{}".format(index), "image_name": name,
                "image_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "split": split, "available_at_t0": True,
                "label_available_at_t0": False,
                "emotion_distribution": {"a": 0.2, "b": 0.3, "c": 0.5},
            })
        canonical = root / "canonical.jsonl"
        canonical.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        return canonical, classes

    def test_loader_uses_only_t0_images_and_materializes_no_test_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical, classes = self._fixture(root)
            loaded = load_lai_gai_train_dev(canonical, root, classes)
            self.assertEqual(loaded["train_features"].shape, (2, 12))
            self.assertEqual(loaded["dev_features"].shape, (1, 12))
            self.assertTrue(np.isfinite(loaded["train_features"]).all())
            self.assertNotIn("item-3", str(loaded))
            self.assertEqual(loaded["applicability"], "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE")

    def test_loader_rejects_image_fixity_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical, classes = self._fixture(root)
            (root / "image-0.png").write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "fixity"):
                load_lai_gai_train_dev(canonical, root, classes)

    def test_boundary_runs_content_only_softmax_and_dirichlet(self):
        rng = np.random.RandomState(2)
        train_x = rng.normal(size=(20, 12)).astype(np.float32)
        dev_x = rng.normal(size=(6, 12)).astype(np.float32)
        train_y = np.full((20, 3), 1 / 3, dtype=np.float32)
        dev_y = np.full((6, 3), 1 / 3, dtype=np.float32)
        result = run_lai_gai_boundary(train_x, train_y, dev_x, dev_y, seed=9, device="cpu", smoke=True)
        self.assertEqual(set(result["rows"]), {"overall_mean", "content_softmax", "content_dirichlet"})
        self.assertEqual(result["h1_status"], "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE")
        self.assertEqual(result["test_access"], "TEST_ROWS_NOT_MATERIALIZED_OR_USED")


if __name__ == "__main__":
    unittest.main()
