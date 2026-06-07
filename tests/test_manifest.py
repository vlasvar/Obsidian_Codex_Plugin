import tempfile
import unittest
from pathlib import Path

from scripts.manifest import is_unchanged, load_manifest, record_source


class ManifestTests(unittest.TestCase):
    def test_manifest_tracks_source_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            source = vault / ".raw" / "note.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Note\n\nBody", encoding="utf-8")

            self.assertFalse(is_unchanged(vault, source))
            record_source(vault, source, pages_created=["wiki/sources/note.md"])

            self.assertTrue(is_unchanged(vault, source))
            data = load_manifest(vault)
            self.assertIn(".raw/note.md", data["sources"])
            self.assertEqual(data["sources"][".raw/note.md"]["pages_created"], ["wiki/sources/note.md"])


if __name__ == "__main__":
    unittest.main()
