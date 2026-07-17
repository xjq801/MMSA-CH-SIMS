import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compare_task20_runs import compare_run_dirs


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


class Task20ReproducibilityTests(unittest.TestCase):
    def _write_run(self, root: Path, name: str, *, prediction: str = "same\n", commit: str = "a") -> Path:
        run_dir = root / name
        run_dir.mkdir()
        payloads = {
            "predictions.jsonl": prediction,
            "metrics.json": '{"jsd": 0.2}\n',
            "selection.json": '{"trial": 4}\n',
            "trial_results.json": '[{"trial": 4}]\n',
        }
        for filename, payload in payloads.items():
            (run_dir / filename).write_text(payload, encoding="utf-8")
        artifacts = [
            {"file": filename, "sha256": _sha256(run_dir / filename), "bytes": (run_dir / filename).stat().st_size}
            for filename in payloads
        ]
        manifest = {
            "schema_version": "task20-run-manifest-v1",
            "run_id": name,
            "experiment_id": "task20-frozen-i3d-temporal-attention-v1",
            "model": {"id": "frozen_i3d_temporal_attention", "family": "strong_visual_baseline"},
            "fit_scope": "train_only",
            "split_scheme": "group_by_video_v1",
            "evaluation_split": "dev",
            "seed": 20260717,
            "attempt": 1,
            "status": "COMPLETED",
            "git": {"commit": commit, "dirty": False},
            "config": {"file": "tuning-plan-v1.json", "sha256": "config-hash"},
            "inputs": [{"role": "canonical_labels", "file": "labels.jsonl", "sha256": "input-hash"}],
            "code": [{"file": "runner.py", "sha256": "code-hash", "bytes": 10}],
            "artifacts": artifacts,
            "smoke": False,
        }
        (run_dir / "environment.json").write_text(
            json.dumps({"python": "3.8.20", "torch": "2.4.1", "device": "cuda", "dtype": "float32", "amp": False}),
            encoding="utf-8",
        )
        manifest["artifacts"].append(
            {
                "file": "environment.json",
                "sha256": _sha256(run_dir / "environment.json"),
                "bytes": (run_dir / "environment.json").stat().st_size,
            }
        )
        (run_dir / "run-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return run_dir

    def test_identical_runs_pass_when_only_clean_git_commit_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._write_run(root, "run-a", commit="commit-a")
            second = self._write_run(root, "run-b", commit="commit-b")

            report = compare_run_dirs(first, second)

        self.assertTrue(report["passed"])
        self.assertEqual(report["comparison_scope"], "SAME_ENVIRONMENT_FIXED_SEED")
        self.assertEqual(report["differing_git_commits"], ["commit-a", "commit-b"])
        self.assertEqual(report["matching_artifacts"], 4)

    def test_prediction_content_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._write_run(root, "run-a")
            second = self._write_run(root, "run-b", prediction="different\n")

            with self.assertRaisesRegex(ValueError, "predictions.jsonl"):
                compare_run_dirs(first, second)

    def test_dirty_run_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._write_run(root, "run-a")
            second = self._write_run(root, "run-b")
            manifest_path = second / "run-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["git"]["dirty"] = True
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "dirty"):
                compare_run_dirs(first, second)


if __name__ == "__main__":
    unittest.main()
