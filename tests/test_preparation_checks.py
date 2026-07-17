from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_preparation_checks as preparation_checks


class PreparationSecretScanTests(unittest.TestCase):
    def test_secret_scan_skips_named_local_virtualenvs(self):
        original_root = preparation_checks.ROOT
        try:
            with tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                dependency = root / ".venv-task20" / "dependency.py"
                source = root / "src" / "application.py"
                dependency.parent.mkdir(parents=True)
                source.parent.mkdir(parents=True)
                marker = "api_" + "key = '" + ("x" * 16) + "'"
                dependency.write_text(marker, encoding="utf-8")
                source.write_text(marker, encoding="utf-8")
                preparation_checks.ROOT = root

                hits = preparation_checks.secret_hits()

            self.assertEqual([hit["file"] for hit in hits], [str(Path("src") / "application.py")])
        finally:
            preparation_checks.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
