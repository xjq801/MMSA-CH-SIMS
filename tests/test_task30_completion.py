from pathlib import Path
import json
import sys
import tempfile
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task30_analysis import analyze_teacher_confidence_effect
from task30_contracts import DatasetRuntimeSpec
from task30_freeze import build_nonsecret_freeze
from validate_task30_completion import validate_completion_freeze
from run_task30_h1_development import load_canonical_train_dev


class Task30DatasetRuntimeContractTests(unittest.TestCase):
    def test_loader_uses_configured_fields_and_dynamic_class_order(self):
        spec = DatasetRuntimeSpec(
            dataset_id="toy-public",
            class_order=("calm", "tense", "mixed"),
            split_scheme="group_by_post_v2",
            item_id_field="post_key",
            target_distribution_field="audience_affect",
            response_count_field="audience_count",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "labels.jsonl"
            rows = [
                {
                    "post_key": "train-1",
                    "split": {"group_by_post_v2": "train"},
                    "audience_affect": {"calm": 0.2, "tense": 0.3, "mixed": 0.5},
                    "audience_count": 4,
                },
                {
                    "post_key": "dev-1",
                    "split": {"group_by_post_v2": "dev"},
                    "audience_affect": {"calm": 0.6, "tense": 0.1, "mixed": 0.3},
                    "audience_count": 5,
                },
                {
                    "post_key": "test-never-materialized",
                    "split": {"group_by_post_v2": "test"},
                    "audience_affect": {"calm": 0.3, "tense": 0.3, "mixed": 0.4},
                    "audience_count": 6,
                },
            ]
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            loaded = load_canonical_train_dev(path, spec)
        self.assertEqual(loaded["train_ids"], ["train-1"])
        self.assertEqual(loaded["dev_ids"], ["dev-1"])
        self.assertEqual(loaded["dev_targets"].shape, (1, 3))
        self.assertNotIn("test-never-materialized", str(loaded))


class Task30ConfidenceAnalysisTests(unittest.TestCase):
    def test_teacher_confidence_effect_is_train_diagnostic_and_aggregate_only(self):
        targets = np.asarray(
            [[0.9, 0.1], [0.6, 0.4], [0.5, 0.5], [0.2, 0.8], [0.1, 0.9], [0.7, 0.3]],
            dtype=np.float64,
        )
        ordinary = np.asarray(
            [[0.7, 0.3], [0.55, 0.45], [0.6, 0.4], [0.4, 0.6], [0.3, 0.7], [0.55, 0.45]],
            dtype=np.float64,
        )
        privileged = np.asarray(
            [[0.85, 0.15], [0.58, 0.42], [0.52, 0.48], [0.25, 0.75], [0.15, 0.85], [0.65, 0.35]],
            dtype=np.float64,
        )
        result = analyze_teacher_confidence_effect(
            targets,
            ordinary,
            privileged,
            teacher_confidences=np.asarray([0.95, 0.7, 0.1, 0.5, 0.9, 0.3]),
        )
        self.assertEqual(result["scope"], "TRAIN_TEACHER_FIT_DIAGNOSTIC_NOT_DEV_STUDENT_SUBGROUP")
        self.assertEqual(set(result["confidence_thirds"]), {"lower", "middle", "upper"})
        self.assertTrue(np.isfinite(result["pearson_confidence_vs_teacher_js_gain"]))
        self.assertNotIn("sample_id", str(result))


class Task30DurableFreezeTests(unittest.TestCase):
    def test_nonsecret_freeze_rejects_private_fields_and_keeps_selected_configs(self):
        aggregate = {
            "schema_version": "task30-h1-development-result-v2",
            "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
            "rows": {
                "soft_distribution_student": {
                    "selected_config": {"hidden_dim": 8, "dropout": 0.1},
                    "dev_metrics": {"jensen_shannon_divergence": 0.2},
                    "trial_count": 2,
                }
            },
            "teacher_audit": {"privacy_boundary": "AGGREGATES_ONLY"},
            "teacher_confidence_analysis": {"scope": "TRAIN_TEACHER_FIT_DIAGNOSTIC_NOT_DEV_STUDENT_SUBGROUP"},
            "test_access": "TEST_ROWS_NOT_MATERIALIZED_OR_USED",
        }
        manifest = {
            "schema_version": "task30-run-manifest-v2",
            "run_id": "clean-run-a",
            "git": {"commit": "a" * 40, "dirty": False},
            "artifacts": [{"file": "predictions.csv", "sha256": "b" * 64}],
        }
        frozen = build_nonsecret_freeze(aggregate, manifest)
        self.assertEqual(frozen["selected_configs"]["soft_distribution_student"]["hidden_dim"], 8)
        self.assertEqual(frozen["run_identity"]["git_commit"], "a" * 40)
        self.assertNotIn("predictions.csv", json.dumps(frozen))
        with self.assertRaisesRegex(ValueError, "private"):
            build_nonsecret_freeze({**aggregate, "sample_id": "private-row"}, manifest)


class Task30CompletionGateTests(unittest.TestCase):
    def test_completion_gate_requires_clean_runs_and_explicit_unavailable_boundaries(self):
        freeze = {
            "schema_version": "task30-completion-freeze-v1",
            "evidence_identity": "DEVELOPMENT_EVIDENCE_ONLY",
            "decision": "NOT_PASSED_MECHANISM_NOT_STABLE",
            "code_commit": "a" * 40,
            "runs": {
                "search": {"manifest_sha256": "b" * 64, "git_dirty": False, "exit_code": 0},
                "replay": {"manifest_sha256": "c" * 64, "git_dirty": False, "exit_code": 0},
                "seed_20260803": {"manifest_sha256": "d" * 64, "git_dirty": False, "exit_code": 0},
                "seed_20260804": {"manifest_sha256": "e" * 64, "git_dirty": False, "exit_code": 0},
            },
            "reproducibility": {
                "same_seed_prediction_byte_identical": True,
                "same_seed_model_hashes_identical": True,
            },
            "data_flow": {
                "artifact": "TASK30_DATA_FLOW.md",
                "sha256": "f" * 64,
                "test_comment_access": "UNREACHABLE",
                "test_rows": "NOT_MATERIALIZED",
            },
            "boundaries": {
                "independent_00_review": "EXTERNAL_REVIEW_REQUIRED_NOT_SELF_APPROVABLE",
                "second_comment_bearing_dataset": "NOT_EVALUABLE_DATA_NOT_RELEASED",
                "teacher_only_dev_upper_bound": "NOT_COMPARABLE_DEV_RESPONSES_PROHIBITED",
                "sarcasm": "NOT_EVALUABLE_DEV_RESPONSE_TEXT_UNREACHABLE",
                "cross_domain_h1": "NOT_APPLICABLE_NO_SECOND_COMMENT_BEARING_DATASET",
                "video2reaction_h1": "NOT_APPLICABLE_DATA_NOT_RELEASED",
            },
            "test_access": "TEST_ROWS_NOT_MATERIALIZED_OR_USED",
            "privacy_boundary": "TRACKED_AGGREGATES_ONLY_NO_SAMPLE_IDS_PATHS_WEIGHTS_OR_PREDICTION_ROWS",
        }
        validate_completion_freeze(freeze)
        broken = json.loads(json.dumps(freeze))
        broken["runs"]["search"]["git_dirty"] = True
        with self.assertRaisesRegex(ValueError, "clean"):
            validate_completion_freeze(broken)
        broken = json.loads(json.dumps(freeze))
        del broken["boundaries"]["sarcasm"]
        with self.assertRaisesRegex(ValueError, "boundary"):
            validate_completion_freeze(broken)
        broken = json.loads(json.dumps(freeze))
        del broken["data_flow"]
        with self.assertRaisesRegex(ValueError, "data flow"):
            validate_completion_freeze(broken)

    def test_data_flow_artifact_maps_allowed_and_blocked_edges(self):
        path = ROOT / "TASK30_DATA_FLOW.md"
        text = path.read_text(encoding="utf-8")
        required = {
            "flowchart LR",
            "TRAIN_RESPONSES_ALLOWED",
            "DEV_SELECTION_CONTENT_AND_TARGETS_ONLY",
            "TEST_RESPONSES_UNREACHABLE",
            "TEST_ROWS_NOT_MATERIALIZED",
            "CONTENT_ONLY_STUDENT_INFERENCE",
        }
        self.assertFalse(required.difference(set(text.splitlines())))
        self.assertNotIn("C:\\Users\\", text)
        self.assertNotIn("D:\\", text)

    def test_handoff_references_data_flow_and_avoids_stale_log_count(self):
        text = (ROOT / "HANDOFF_30.md").read_text(encoding="utf-8")
        self.assertIn("TASK30_DATA_FLOW.md", text)
        self.assertNotIn("253条", text)

    def test_environment_lock_matches_private_model_state_boundary(self):
        text = (ROOT / "TASK30_ENVIRONMENT_LOCK.md").read_text(encoding="utf-8")
        self.assertIn("LOCAL_PRIVATE_MODEL_STATES_FROZEN", text)
        self.assertNotIn("No model weights were saved.", text)


if __name__ == "__main__":
    unittest.main()
