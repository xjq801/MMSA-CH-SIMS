from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_contracts import DatasetSpec, LeakageBlockedError
from task30_teacher import aggregate_train_reactions, audit_teacher_records


SPEC = DatasetSpec(
    dataset_id="toy",
    class_order=("a", "b", "c"),
    privileged_supervision_status="TRAIN_RESPONSES_ONLY",
)


def reaction(sample_id, label, confidence=1.0, split="train"):
    return {
        "dataset_id": "toy",
        "sample_id": sample_id,
        "split": split,
        "reaction_label": label,
        "label_confidence": confidence,
    }


class Task30TeacherAggregationTests(unittest.TestCase):
    def test_aggregation_rejects_dev_and_test_reactions(self):
        for split in ("dev", "test"):
            with self.subTest(split=split):
                with self.assertRaisesRegex(LeakageBlockedError, "train"):
                    aggregate_train_reactions([reaction("x", "a", split=split)], SPEC)

    def test_aggregation_builds_dynamic_video_distribution_and_confidence(self):
        rows = [
            reaction("video-1", "a", 0.8),
            reaction("video-1", "a", 0.6),
            reaction("video-1", "c", 1.0),
            reaction("video-2", "b", 0.5),
        ]
        records = aggregate_train_reactions(rows, SPEC)
        self.assertEqual([record["sample_id"] for record in records], ["video-1", "video-2"])
        self.assertEqual(records[0]["response_count"], 3)
        self.assertEqual(records[0]["class_order"], ["a", "b", "c"])
        self.assertEqual(records[0]["teacher_distribution"], [2 / 3, 0.0, 1 / 3])
        self.assertAlmostEqual(records[0]["teacher_confidence"], 0.8)

    def test_aggregation_rejects_unknown_label_and_nonfinite_confidence(self):
        with self.assertRaisesRegex(ValueError, "label"):
            aggregate_train_reactions([reaction("x", "unknown")], SPEC)
        with self.assertRaisesRegex(ValueError, "confidence"):
            aggregate_train_reactions([reaction("x", "a", float("nan"))], SPEC)


class Task30TeacherAuditTests(unittest.TestCase):
    def test_audit_reports_counts_without_sample_identifiers(self):
        rows = [
            reaction("video-1", "a", 0.8),
            reaction("video-1", "a", 0.6),
            reaction("video-2", "b", 0.5),
        ]
        audit = audit_teacher_records(
            aggregate_train_reactions(rows, SPEC),
            SPEC,
            sparse_mass_threshold=0.05,
            low_response_threshold=1,
        )
        self.assertEqual(audit["sample_count"], 2)
        self.assertEqual(audit["response_count"]["total"], 3)
        self.assertEqual(audit["low_response_sample_count"], 1)
        self.assertEqual(audit["sparse_classes"], ["c"])
        self.assertNotIn("sample_id", str(audit))
        self.assertNotIn("video-1", str(audit))


if __name__ == "__main__":
    unittest.main()
