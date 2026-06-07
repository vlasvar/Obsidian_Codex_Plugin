import tempfile
import unittest
from pathlib import Path

from scripts.detect_vault import scaffold_vault


class DetectVaultTests(unittest.TestCase):
    def test_scaffold_vault_creates_core_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"

            result = scaffold_vault(vault, create=True)

            self.assertIn("wiki/index.md", result["created"])
            self.assertTrue((vault / ".raw" / ".manifest.json").exists())
            self.assertTrue((vault / "wiki" / "00.inbox").is_dir())
            self.assertTrue((vault / "wiki" / "sources").is_dir())
            self.assertTrue((vault / "wiki" / "literature").is_dir())
            self.assertTrue((vault / "wiki" / "permanent").is_dir())
            self.assertTrue((vault / "wiki" / "indexes").is_dir())
            self.assertTrue((vault / "wiki" / "hot.md").read_text(encoding="utf-8").startswith("---"))


if __name__ == "__main__":
    unittest.main()
