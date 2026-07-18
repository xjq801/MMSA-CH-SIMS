import json
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
    build_smoke_inputs,
    load_reproduction_contract,
    validate_reproduction_contract,
)


class VccsaAuthorReproductionTests(unittest.TestCase):
    def test_smoke_builder_is_deterministic_and_never_reads_test(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "Comments_Anno"
            output = root / "runtime"
            source.mkdir()
            fixtures = {
                "train_set.json": ["tr0", "tr1", "tr2"],
                "dev_set.json": ["dv0", "dv1"],
                "test_set.json": ["te0"],
                "video_to_comment.json": {"v.mp4": ["tr0", "tr1"]},
                "opinion_label_map.json": {"neutral": 0},
                "emotion_label_map.json": {"neutral": 0},
            }
            for name, value in fixtures.items():
                (source / name).write_text(json.dumps(value), encoding="utf-8")
            with zipfile.ZipFile(source / "lable_data_dict.json.zip", "w") as archive:
                archive.writestr("lable_data_dict.json", json.dumps({"tr0": {}}))

            report = build_smoke_inputs(source, output, train_examples=2, dev_examples=1)

            self.assertEqual(json.loads((output / "train_set.json").read_text()), ["tr0", "tr1"])
            self.assertEqual(json.loads((output / "dev_set.json").read_text()), ["dv0"])
            self.assertEqual(json.loads((output / "test_set.json").read_text()), [])
            self.assertEqual(report["test_examples"], 0)

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
