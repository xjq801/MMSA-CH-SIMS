from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from task20_contracts import build_run_manifest, load_config, validate_config


class Task20ContractTests(unittest.TestCase):
    def test_frozen_config_is_schema_valid(self):
        config = load_config(ROOT / "configs" / "task20" / "baseline-common.json")
        validate_config(config, ROOT / "configs" / "task20" / "experiment.schema.json")

    def test_baseline_variants_only_change_model_field(self):
        base = load_config(ROOT / "configs" / "task20" / "baseline-common.json")
        variants = ["overall_mean", "topic_mean", "empirical_distribution", "majority_class"]
        projected = []
        for name in variants:
            candidate = copy.deepcopy(base)
            candidate["model"] = {"id": name, "family": "constant_or_group_statistic"}
            validate_config(candidate, ROOT / "configs" / "task20" / "experiment.schema.json")
            candidate.pop("model")
            projected.append(candidate)
        self.assertTrue(all(item == projected[0] for item in projected[1:]))

    def test_run_manifest_binds_config_code_and_input_hashes(self):
        config = load_config(ROOT / "configs" / "task20" / "baseline-common.json")
        manifest = build_run_manifest(
            run_id="task20-contract-test",
            config=config,
            config_path=ROOT / "configs" / "task20" / "baseline-common.json",
            input_paths=[ROOT / "data" / "manifests" / "split-v1.manifest.json"],
            code_paths=[ROOT / "scripts" / "task20_baseline.py"],
            git_commit="test-commit",
            git_dirty=False,
        )
        self.assertEqual(manifest["schema_version"], "task20-run-manifest-v1")
        self.assertEqual(manifest["fit_scope"], "train_only")
        self.assertEqual(len(manifest["inputs"]), 1)
        self.assertEqual(len(manifest["code"]), 1)
        self.assertEqual(len(manifest["inputs"][0]["sha256"]), 64)
        self.assertNotIn(":", manifest["inputs"][0]["path"])
        self.assertFalse(manifest["inputs"][0]["path"].startswith("/"))
        import jsonschema
        schema = json.loads((ROOT / "configs" / "task20" / "run-manifest.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(manifest, schema)
        json.dumps(manifest)


if __name__ == "__main__":
    unittest.main()
