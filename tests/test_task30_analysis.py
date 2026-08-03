from pathlib import Path
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_analysis import analyze_error_groups


class Task30AnalysisTests(unittest.TestCase):
    def test_error_groups_are_aggregate_only_and_cover_supported_cases(self):
        targets = np.asarray([[0.9, 0.1], [0.5, 0.5], [0.1, 0.9], [0.6, 0.4]], dtype=np.float64)
        baseline = np.asarray([[0.7, 0.3], [0.7, 0.3], [0.3, 0.7], [0.5, 0.5]], dtype=np.float64)
        privileged = np.asarray([[0.8, 0.2], [0.6, 0.4], [0.2, 0.8], [0.55, 0.45]], dtype=np.float64)
        result = analyze_error_groups(
            targets, baseline, privileged,
            response_counts=np.asarray([1, 5, 12, 20]),
            normalized_entropy=np.asarray([0.1, 0.8, 0.2, 0.6]),
            noise_score=np.asarray([0.01, 0.08, 0.02, 0.04]),
        )
        self.assertEqual(set(result["response_count"]), {"low_1_2", "medium_3_10", "high_11_plus"})
        self.assertEqual(set(result["target_mixture"]), {"low_entropy", "mixed", "high_entropy"})
        self.assertEqual(result["sarcasm"], "NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE")
        self.assertNotIn("sample_id", str(result))


if __name__ == "__main__":
    unittest.main()
