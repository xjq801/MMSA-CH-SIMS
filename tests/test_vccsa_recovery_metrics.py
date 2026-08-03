import pickle
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from collect_vccsa_recovery_metrics import collect_prediction_metrics


def _payload():
    return {
        "comments_key": ["a", "b"],
        "opinion_preds": [[0.8, 0.1, 0.1], [0.1, 0.7, 0.2]],
        "opinion_preds_classidx": [0, 1],
        "emotion_preds": [[0.8, 0.1, 0.1], [0.1, 0.7, 0.2]],
        "emotion_preds_classidx": [0, 1],
        "opinions_label": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        "opinions_label_classindex": [0, 1],
        "emotions_label": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        "emotions_label_classindex": [0, 1],
    }


class VccsaRecoveryMetricsTests(unittest.TestCase):
    def test_collects_nine_metrics_for_both_author_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev_predict_1.pkl"
            path.write_bytes(pickle.dumps(_payload()))
            result = collect_prediction_metrics(path, expected_rows=2)
        self.assertEqual(result["sample_count"], 2)
        self.assertEqual(result["test_access"], 0)
        self.assertEqual(set(result["tasks"]), {"opinion", "emotion"})
        self.assertEqual(result["target_contract"]["source"], "author_label_classindex_one_hot")
        self.assertEqual(
            set(result["tasks"]["opinion"]),
            {"js", "nll", "emd", "macro_f1", "balanced_accuracy", "brier", "ece", "ace", "aurc_js"},
        )

    def test_discloses_non_normalized_raw_label_but_uses_author_class_index(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev_predict_1.pkl"
            payload = _payload()
            payload["opinions_label"][0] = [1.0, 1.0, 1.0]
            path.write_bytes(pickle.dumps(payload))
            result = collect_prediction_metrics(path, expected_rows=2)
        self.assertEqual(
            result["target_contract"]["raw_non_normalized_rows"]["opinion"], 1
        )

    def test_fails_closed_on_duplicate_ids_or_index_misalignment(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dev_predict_1.pkl"
            payload = _payload()
            payload["comments_key"] = ["a", "a"]
            path.write_bytes(pickle.dumps(payload))
            with self.assertRaisesRegex(ValueError, "not unique"):
                collect_prediction_metrics(path, expected_rows=2)

            payload = _payload()
            payload["opinion_preds_classidx"] = [1, 1]
            path.write_bytes(pickle.dumps(payload))
            with self.assertRaisesRegex(ValueError, "misaligned"):
                collect_prediction_metrics(path, expected_rows=2)


if __name__ == "__main__":
    unittest.main()
