import hashlib
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_task20_handoff import (
    reject_unsafe_paths,
    validate_handoff_text,
    validate_tracked_evidence,
)


class Task20HandoffValidationTests(unittest.TestCase):
    def test_tracked_evidence_is_bound_to_exact_commit_bytes(self):
        payload = b"frozen evidence\n"
        manifest = {
            "evidence_snapshot_commit": "abc123",
            "tracked_evidence": [
                {
                    "path": "evidence.md",
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": len(payload),
                }
            ],
        }

        checked = validate_tracked_evidence(manifest, lambda commit, path: payload)

        self.assertEqual(checked, 1)

    def test_tracked_evidence_hash_drift_fails_closed(self):
        manifest = {
            "evidence_snapshot_commit": "abc123",
            "tracked_evidence": [
                {"path": "evidence.md", "sha256": "0" * 64, "bytes": 7}
            ],
        }

        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            validate_tracked_evidence(manifest, lambda commit, path: b"changed")

    def test_tracked_evidence_can_bind_a_row_to_submission_commit(self):
        payload = b"submitted status\n"
        manifest = {
            "evidence_snapshot_commit": "evidence-commit",
            "tracked_evidence": [
                {
                    "commit": "submission-commit",
                    "path": "status.md",
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "bytes": len(payload),
                }
            ],
        }
        seen = []

        def show_blob(commit, path):
            seen.append((commit, path))
            return payload

        validate_tracked_evidence(manifest, show_blob)

        self.assertEqual(seen, [("submission-commit", "status.md")])

    def test_handoff_rejects_absolute_or_parent_paths_and_requires_boundaries(self):
        with self.assertRaisesRegex(ValueError, "unsafe path"):
            reject_unsafe_paths({"path": r"D:\\restricted\\asset.npy"})
        with self.assertRaisesRegex(ValueError, "unsafe path"):
            reject_unsafe_paths({"path": "../outside.json"})

        text = "\n".join(
            [
                "b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d",
                "DEFERRED_ACCEPTED_RISK",
                "FAILED_OFFICIAL_CODE_ABSENT_AND_TARGET_COMMENT_INPUT_MISMATCH",
                "ASSET_INVALIDATED_DO_NOT_REPORT",
                "NOT_APPLICABLE_SINGLE_AVAILABLE_INPUT_MODALITY",
                "TASK50_NOT_COMPLETED",
            ]
        )
        validate_handoff_text(text, "b89d8dc1d62b5d6ea7b07b1d30cc8f19224c030d")

        with self.assertRaisesRegex(ValueError, "missing required handoff term"):
            validate_handoff_text("incomplete", "b89d8dc")


if __name__ == "__main__":
    unittest.main()
