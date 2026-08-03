from pathlib import Path
import json
import sys
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_contracts import (
    DatasetSpec,
    LeakageBlockedError,
    dataset_applicability,
    make_mismatched_teacher_targets,
    validate_distribution,
    validate_student_batch,
    validate_teacher_records,
)


CSMV_SPEC = DatasetSpec(
    dataset_id="csmv",
    class_order=("anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"),
    privileged_supervision_status="TRAIN_RESPONSES_ONLY",
)


def teacher_record(sample_id="sample-a", split="train", distribution=None):
    if distribution is None:
        distribution = [0.125] * 8
    return {
        "dataset_id": "csmv",
        "sample_id": sample_id,
        "split": split,
        "class_order": list(CSMV_SPEC.class_order),
        "teacher_distribution": distribution,
        "response_count": 4,
        "teacher_confidence": 0.75,
    }


class Task30LeakageContractTests(unittest.TestCase):
    def test_teacher_fit_rejects_dev_comments(self):
        with self.assertRaisesRegex(LeakageBlockedError, "train"):
            validate_teacher_records([teacher_record(split="dev")], CSMV_SPEC)

    def test_teacher_fit_rejects_test_comments(self):
        with self.assertRaisesRegex(LeakageBlockedError, "train"):
            validate_teacher_records([teacher_record(split="test")], CSMV_SPEC)

    def test_student_batch_rejects_response_or_future_fields(self):
        valid = {
            "dataset_id": "csmv",
            "sample_ids": ["sample-a"],
            "content_features": np.zeros((1, 4), dtype=np.float32),
            "target_distribution": np.asarray([[0.125] * 8], dtype=np.float32),
        }
        for forbidden in ("comment_text", "response_ids", "future_engagement"):
            candidate = dict(valid)
            candidate[forbidden] = ["forbidden"]
            with self.subTest(forbidden=forbidden):
                with self.assertRaisesRegex(LeakageBlockedError, "forbidden"):
                    validate_student_batch(candidate, CSMV_SPEC)

    def test_missing_teacher_fields_fail_closed(self):
        record = teacher_record()
        del record["teacher_confidence"]
        with self.assertRaisesRegex(ValueError, "missing"):
            validate_teacher_records([record], CSMV_SPEC)


class Task30DistributionContractTests(unittest.TestCase):
    def test_distribution_accepts_known_normalized_gold_case(self):
        actual = validate_distribution([0.2, 0.3, 0.5], ("a", "b", "c"), "gold")
        np.testing.assert_allclose(actual, [0.2, 0.3, 0.5], rtol=0.0, atol=1e-12)

    def test_distribution_rejects_negative_non_normalized_nan_and_inf(self):
        invalid = (
            [0.2, -0.1, 0.9],
            [0.2, 0.3, 0.4],
            [0.2, np.nan, 0.8],
            [0.2, np.inf, 0.8],
        )
        for values in invalid:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    validate_distribution(values, ("a", "b", "c"), "invalid")

    def test_dataset_head_is_dynamic_and_rejects_wrong_class_order(self):
        three_class = DatasetSpec("toy", ("low", "mid", "high"), "TRAIN_RESPONSES_ONLY")
        record = {
            "dataset_id": "toy",
            "sample_id": "toy-a",
            "split": "train",
            "class_order": ["low", "high", "mid"],
            "teacher_distribution": [0.2, 0.3, 0.5],
            "response_count": 2,
            "teacher_confidence": 0.5,
        }
        with self.assertRaisesRegex(ValueError, "class order"):
            validate_teacher_records([record], three_class)


class Task30MismatchAndApplicabilityTests(unittest.TestCase):
    def test_mismatched_teacher_is_train_only_deterministic_derangement(self):
        records = [
            teacher_record("a", distribution=[1.0] + [0.0] * 7),
            teacher_record("b", distribution=[0.0, 1.0] + [0.0] * 6),
            teacher_record("c", distribution=[0.0, 0.0, 1.0] + [0.0] * 5),
        ]
        first = make_mismatched_teacher_targets(records, CSMV_SPEC, seed=17)
        second = make_mismatched_teacher_targets(records, CSMV_SPEC, seed=17)
        self.assertEqual(first, second)
        self.assertTrue(all(row["split"] == "train" for row in first))
        self.assertTrue(all(row["sample_id"] != row["teacher_source_sample_id"] for row in first))
        self.assertTrue(all(row["control"] == "MISMATCHED_TEACHER_DERANGEMENT" for row in first))

    def test_lai_gai_disables_comment_teacher(self):
        self.assertEqual(dataset_applicability("lai-gai"), "NOT_APPLICABLE_COMMENT_FIELD_UNAVAILABLE")

    def test_video2reaction_h1_is_not_applicable_data_not_released(self):
        self.assertEqual(dataset_applicability("video2reaction-native"), "NOT_APPLICABLE_DATA_NOT_RELEASED")

    def test_development_matrix_keeps_student_budget_fair(self):
        matrix = json.loads(
            (ROOT / "configs" / "task30" / "development-matrix-v1.json").read_text(encoding="utf-8")
        )
        student_rows = [row for row in matrix["rows"] if row["deployable_student"]]
        projected = {
            (
                row["max_trials"],
                row["max_epochs"],
                row["early_stopping_patience"],
                row["selection_split"],
            )
            for row in student_rows
        }
        self.assertEqual(len(projected), 1)
        softmax_rows = [
            row for row in student_rows
            if row["id"] != "soft_distribution_student_dirichlet"
        ]
        self.assertEqual({row["student_architecture"] for row in softmax_rows}, {"content_only_student_v1"})
        teacher_upper = [row for row in matrix["rows"] if row["id"] == "teacher_only_upper_bound"]
        self.assertEqual(len(teacher_upper), 1)
        self.assertFalse(teacher_upper[0]["deployable_student"])
        self.assertEqual(matrix["test_policy"], "UNREACHABLE_TASK30_DEVELOPMENT")
        self.assertEqual(matrix["distillation"]["teacher_target_scope"], "train_only")
        self.assertEqual(matrix["distillation"]["selection_split"], "dev")
        self.assertFalse(matrix["distillation"]["test_visible_during_selection"])
        self.assertEqual(matrix["distillation"]["temperature_candidates"], [1.0, 2.0, 4.0])
        self.assertEqual(matrix["distillation"]["weight_candidates"], [0.25, 0.5, 0.75])
        dirichlet = [row for row in matrix["rows"] if row["id"] == "soft_distribution_student_dirichlet"]
        self.assertEqual(len(dirichlet), 1)
        self.assertEqual(dirichlet[0]["student_architecture"], "content_only_student_dirichlet_v1")
        self.assertEqual(teacher_upper[0]["evaluation_scope"], "train_diagnostic_only")


if __name__ == "__main__":
    unittest.main()
