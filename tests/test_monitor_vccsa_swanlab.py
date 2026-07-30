import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import monitor_vccsa_swanlab as monitor


class MonitorVccsaSwanlabTests(unittest.TestCase):
    def test_parse_step_record_extracts_only_expected_scalars(self):
        line = (
            "[Epoch 89][Step 3305/4692] Loss_sum: 0.0001,"
            "opinion_loss: 0.0000, emotion_loss: 0.0001, "
            "Lr: 1.45e-05, 18 mremaining"
        )

        record = monitor.parse_step_record(line, steps_per_epoch=4693)

        self.assertEqual(record["step"], 89 * 4693 + 3305)
        self.assertEqual(record["metrics"]["train/epoch"], 89)
        self.assertEqual(record["metrics"]["train/batch"], 3305)
        self.assertAlmostEqual(record["metrics"]["train/total_loss"], 0.0001)
        self.assertAlmostEqual(record["metrics"]["train/lr"], 1.45e-5)
        self.assertIsNone(
            monitor.parse_step_record("Accuracy: {'comment': 'restricted'}", 4693)
        )

    def test_complete_epoch_records_fail_closed_without_both_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            run_dir = Path(td)
            (run_dir / "loss_epoc_4.json").write_text(
                json.dumps(
                    {
                        "epoch_loss": 4.693,
                        "epoch_opinion_loss": 1.8772,
                        "epoch_emotion_loss": 2.8158,
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                monitor.complete_epoch_records(run_dir, steps_per_epoch=4693), []
            )

            (run_dir / "dev_performance_4.json").write_text(
                json.dumps(
                    {
                        "opinion": {
                            "micro": {"f1_score": 0.7},
                            "macro": {"f1_score": 0.6},
                            "accuracy": 0.7,
                        },
                        "emotion": {
                            "micro": {"f1_score": 0.5},
                            "macro": {"f1_score": 0.4},
                            "accuracy": 0.5,
                        },
                    }
                ),
                encoding="utf-8",
            )

            records = monitor.complete_epoch_records(
                run_dir, steps_per_epoch=4693
            )

            self.assertEqual(len(records), 1)
            epoch, metrics = records[0]
            self.assertEqual(epoch, 4)
            self.assertAlmostEqual(metrics["epoch/train_total_loss"], 0.001)
            self.assertAlmostEqual(metrics["dev/combined_micro_f1"], 1.2)
            self.assertNotIn("prediction", metrics)
            self.assertNotIn("path", metrics)


if __name__ == "__main__":
    unittest.main()
