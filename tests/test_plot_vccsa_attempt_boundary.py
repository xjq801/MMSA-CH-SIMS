import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from plot_vccsa_attempt_boundary import ATTEMPT1, ATTEMPT2, build_rows, validate_rows


class VccsaAttemptBoundaryTests(unittest.TestCase):
    def test_rows_fail_closed_without_exact_attempt_partitions(self):
        with self.assertRaisesRegex(ValueError, "exactly 120"):
            validate_rows([])

    def test_builder_marks_every_row_non_comparable_and_keeps_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a2 = root / "a2"
            a1 = root / "a1"
            a2.mkdir()
            a1.mkdir()
            for epoch in range(1, 121):
                target = (a2 if epoch <= 3 else a1) / f"loss_epoc_{epoch}.json"
                target.write_text(
                    json.dumps(
                        {
                            "epoch_loss": epoch * 10.0,
                            "epoch_opinion_loss": epoch * 4.0,
                            "epoch_emotion_loss": epoch * 6.0,
                        }
                    ),
                    encoding="utf-8",
                )
            rows = build_rows(a2, a1, "a" * 64, "b" * 64, steps_per_epoch=10)

        self.assertEqual([row["epoch"] for row in rows if row["attempt_id"] == ATTEMPT2], [1, 2, 3])
        self.assertEqual([row["epoch"] for row in rows if row["attempt_id"] == ATTEMPT1], list(range(4, 121)))
        self.assertTrue(all(row["cross_attempt_comparable"] == "false" for row in rows))
        self.assertEqual(rows[2]["total_mean"], 3.0)
        self.assertEqual(rows[3]["total_mean"], 4.0)


if __name__ == "__main__":
    unittest.main()
