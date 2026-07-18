import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from prepare_vccsa_author_reproduction import (
    EXPECTED_AUTHOR_REVISION,
    apply_compatibility_patch,
    audit_peer_isolation,
    build_smoke_inputs,
    load_reproduction_contract,
    validate_reproduction_contract,
)


class VccsaAuthorReproductionTests(unittest.TestCase):
    def test_full_author_split_fails_closed_when_peer_requires_another_split(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "Comments_Anno"
            source.mkdir()
            for name, value in {
                "train_set.json": ["tr0"],
                "dev_set.json": ["dv0", "dv1"],
                "test_set.json": ["te0"],
                "video_to_comment.json": {
                    "cross.mp4": ["tr0", "te0"],
                    "dev.mp4": ["dv0", "dv1"],
                },
            }.items():
                (source / name).write_text(json.dumps(value), encoding="utf-8")
            with zipfile.ZipFile(source / "lable_data_dict.json.zip", "w") as archive:
                archive.writestr(
                    "lable_data_dict.json",
                    json.dumps({
                        "tr0": {"video_file_id": "cross.mp4"},
                        "dv0": {"video_file_id": "dev.mp4"},
                        "dv1": {"video_file_id": "dev.mp4"},
                        "te0": {"video_file_id": "cross.mp4"},
                    }),
                )

            report = audit_peer_isolation(source)

            self.assertEqual(
                report["status"], "LEAKAGE_BLOCKED_AUTHOR_ORIGINAL_PEER_DEPENDENCY"
            )
            self.assertEqual(report["splits"]["train"]["singleton_ids"], 1)
            self.assertEqual(
                report["splits"]["train"]["cross_split_only_peer_ids"], 1
            )
            self.assertEqual(report["splits"]["train"]["no_global_peer_ids"], 0)
            self.assertEqual(report["videos_spanning_splits"], 1)
            self.assertNotIn("tr0", json.dumps(report))
            self.assertNotIn("te0", json.dumps(report))

    def test_post_snapshot_erratum_preserves_frozen_bytes_and_precedence(self):
        frozen = {
            "TASK20_G3_EVIDENCE_PACKAGE_20260718.md": "cf906a93c9cd1c8ad6c022d7bfe019d323ba19d0f6aa4bd7786a338c152248c6",
            "BASELINE_TABLE_V1.md": "7a2b612c16ebe8110a67a4108877ae0aca4082d8b7ab7d87897dc48f6c651f44",
            "HANDOFF_20.md": "5a503d90308781620b4e4a7c99b409e29f30cd0872fc6f8b51da6c580a9b56cb",
        }
        for name, expected in frozen.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected)
        audit = (ROOT / "TASK20_BASELINE_EXECUTION_AUDIT.md").read_text(encoding="utf-8")
        erratum = (ROOT / "TASK20_POST_SNAPSHOT_VCCSA_ERRATUM_20260718.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("`FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH`", audit)
        self.assertIn("HISTORICAL_OFFICIAL_MAIN_99D1424_ATTEMPT_FAILED", audit)
        self.assertIn(
            "AUTHOR_ORIGINAL_PATH_SMOKE_EXECUTABLE_FULL_REPRODUCTION_BLOCKED_COMPUTE",
            erratum,
        )
        self.assertIn("适用范围与优先级", erratum)

    def test_smoke_builder_physically_excludes_unselected_and_test_records(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "Comments_Anno"
            output = root / "runtime"
            source.mkdir()
            fixtures = {
                "train_set.json": ["tr0", "tr1", "tr2"],
                "dev_set.json": ["dv0", "dv1"],
                "test_set.json": ["te0"],
                "video_to_comment.json": {
                    "train.mp4": ["tr0", "tr1", "te0"],
                    "dev.mp4": ["dv0", "dv1"],
                    "other.mp4": ["tr2"],
                },
                "opinion_label_map.json": {"neutral": 0},
                "emotion_label_map.json": {"neutral": 0},
            }
            for name, value in fixtures.items():
                (source / name).write_text(json.dumps(value), encoding="utf-8")
            with zipfile.ZipFile(source / "lable_data_dict.json.zip", "w") as archive:
                archive.writestr(
                    "lable_data_dict.json",
                    json.dumps(
                        {
                            "tr0": {"video_file_id": "train.mp4"},
                            "tr1": {"video_file_id": "train.mp4"},
                            "tr2": {"video_file_id": "other.mp4"},
                            "dv0": {"video_file_id": "dev.mp4"},
                            "dv1": {"video_file_id": "dev.mp4"},
                            "te0": {"video_file_id": "train.mp4"},
                        }
                    ),
                )

            report = build_smoke_inputs(source, output, train_examples=2, dev_examples=2)

            self.assertEqual(json.loads((output / "train_set.json").read_text()), ["tr0", "tr1"])
            self.assertEqual(json.loads((output / "dev_set.json").read_text()), ["dv0", "dv1"])
            self.assertEqual(json.loads((output / "test_set.json").read_text()), [])
            annotations = json.loads((output / "lable_data_dict.json").read_text())
            video_map = json.loads((output / "video_to_comment.json").read_text())
            self.assertEqual(set(annotations), {"tr0", "tr1", "dv0", "dv1"})
            self.assertEqual(video_map, {
                "train.mp4": ["tr0", "tr1"],
                "dev.mp4": ["dv0", "dv1"],
            })
            self.assertNotIn("te0", json.dumps(annotations))
            self.assertNotIn("te0", json.dumps(video_map))
            self.assertEqual(report["test_examples"], 0)

    def test_smoke_builder_fails_closed_when_selected_id_has_no_peer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "Comments_Anno"
            source.mkdir()
            for name, value in {
                "train_set.json": ["tr0"],
                "dev_set.json": ["dv0"],
                "test_set.json": ["te0"],
                "video_to_comment.json": {"v0.mp4": ["tr0"], "v1.mp4": ["dv0"]},
                "opinion_label_map.json": {"neutral": 0},
                "emotion_label_map.json": {"neutral": 0},
            }.items():
                (source / name).write_text(json.dumps(value), encoding="utf-8")
            with zipfile.ZipFile(source / "lable_data_dict.json.zip", "w") as archive:
                archive.writestr(
                    "lable_data_dict.json",
                    json.dumps({
                        "tr0": {"video_file_id": "v0.mp4"},
                        "dv0": {"video_file_id": "v1.mp4"},
                        "te0": {"video_file_id": "v0.mp4"},
                    }),
                )
            with self.assertRaisesRegex(ValueError, "at least two selected comments"):
                build_smoke_inputs(source, root / "runtime", 1, 1)

    def test_contract_keeps_author_reproduction_outside_t0(self):
        contract = load_reproduction_contract(
            ROOT / "configs" / "task20" / "vccsa-author-original-v1.json"
        )
        validate_reproduction_contract(contract)
        scope = contract["claim_scope"]
        self.assertEqual(scope["classification"], "AUTHOR_ORIGINAL_SETTING_NON_T0")
        self.assertTrue(scope["uses_target_comment_text"])
        self.assertEqual(scope["split_unit"], "comment")
        self.assertFalse(scope["t0_adaptation"])
        self.assertFalse(scope["may_be_reported_as_t0_baseline"])
        self.assertEqual(contract["source"]["revision"], EXPECTED_AUTHOR_REVISION)

    def test_contract_rejects_silent_t0_relabel(self):
        contract = json.loads(
            (ROOT / "configs" / "task20" / "vccsa-author-original-v1.json").read_text(
                encoding="utf-8"
            )
        )
        contract["claim_scope"]["t0_adaptation"] = True
        with self.assertRaisesRegex(ValueError, "separate REIMPLEMENTATION"):
            validate_reproduction_contract(contract)

    def test_patch_removes_dead_glove_import_and_fixes_launchers(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td)
            (source / "utils").mkdir()
            (source / "script").mkdir()
            (source / "utils" / "tokenize.py").write_text(
                "import en_vectors_web_lg\n"
                "def create_dict(use_glove=True):\n"
                "    if use_glove:\n"
                "        spacy_tool = en_vectors_web_lg.load()\n",
                encoding="utf-8",
            )
            (source / "utils" / "compute_args.py").write_text(
                "def compute_args(args):\n    return args\n",
                encoding="utf-8",
            )
            (source / "csmv_dataset.py").write_text(
                'pretrained_model_name_or_path="~/.cache/torch/hub/transformers/roberta-base")\n',
                encoding="utf-8",
            )
            (source / "main.py").write_text(
                "from csmv_dataset import CSMV_Dataset, CSMV_Dataset_VideoMAEv2FPS16\n",
                encoding="utf-8",
            )
            (source / "model_VCCSA.py").write_text(
                "from layers.fc import MLP\n"
                "from layers.layer_norm import LayerNorm\n"
                "class UsedModel:\n    pass\n",
                encoding="utf-8",
            )
            (source / "script" / "train.sh").write_text(
                "video_feature=../visual-feature\n"
                "python ../main.py \\\n"
                "--video_feature_dir ${video_feature_dir} \\ \n"
                "--datadir ../comments\n",
                encoding="utf-8",
            )
            (source / "script" / "eval.sh").write_text(
                "python ../main_eval.py \\\n"
                "--datadir ../comments\n",
                encoding="utf-8",
            )

            report = apply_compatibility_patch(source)

            tokenize = (source / "utils" / "tokenize.py").read_text(encoding="utf-8")
            dataset = (source / "csmv_dataset.py").read_text(encoding="utf-8")
            train = (source / "script" / "train.sh").read_text(encoding="utf-8")
            evaluate = (source / "script" / "eval.sh").read_text(encoding="utf-8")
            main = (source / "main.py").read_text(encoding="utf-8")
            model = (source / "model_VCCSA.py").read_text(encoding="utf-8")
            compute_args = (source / "utils" / "compute_args.py").read_text(encoding="utf-8")
            self.assertIn("try:\n    import en_vectors_web_lg", tokenize)
            self.assertIn("en_vectors_web_lg is None", tokenize)
            self.assertIn("args.pre_trained_LM", dataset)
            self.assertIn("--video_feature_dir ${video_feature}", train)
            self.assertNotIn("\\ ", train)
            self.assertIn("--pre_trained_LM ${pre_trained_lm}", train)
            self.assertIn("--pre_trained_LM ${pre_trained_lm}", evaluate)
            self.assertNotIn("CSMV_Dataset_VideoMAEv2FPS16", main)
            self.assertIn("CSMV_Dataset", main)
            self.assertNotIn("from layers.", model)
            self.assertIn("class UsedModel", model)
            self.assertIn("args.aux_task = False", compute_args)
            self.assertEqual(report["status"], "PATCHED_AND_VERIFIED")


if __name__ == "__main__":
    unittest.main()
