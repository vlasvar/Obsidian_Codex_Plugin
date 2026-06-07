import tempfile
import unittest
from pathlib import Path

from scripts.ingest_source import ingest_source


class IngestSourceTests(unittest.TestCase):
    def test_ingest_source_updates_core_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            source = vault / ".raw" / "essay.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Compounding Notes\n\nA source about durable synthesis.", encoding="utf-8")

            result = ingest_source(vault, source)

            self.assertEqual(result["status"], "created")
            self.assertTrue((vault / "wiki" / "sources" / "compounding-notes.md").exists())
            self.assertIn("[[compounding-notes|Compounding Notes]]", (vault / "wiki" / "index.md").read_text(encoding="utf-8"))
            self.assertIn("Compounding Notes", (vault / "wiki" / "log.md").read_text(encoding="utf-8"))
            self.assertIn("Compounding Notes", (vault / "wiki" / "hot.md").read_text(encoding="utf-8"))

    def test_ingest_source_skips_unchanged_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            source = vault / ".raw" / "essay.md"
            source.parent.mkdir(parents=True)
            source.write_text("# Stable Source\n\nNo changes.", encoding="utf-8")

            ingest_source(vault, source)
            result = ingest_source(vault, source)

            self.assertEqual(result["status"], "unchanged")

    def test_ingest_source_creates_structured_entity_and_concept_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            source = vault / ".raw" / "research.md"
            source.parent.mkdir(parents=True)
            source.write_text(
                "# Durable Synthesis\n\n"
                "OpenAI uses retrieval patterns to maintain Codex project knowledge.",
                encoding="utf-8",
            )

            ingest_source(vault, source)

            self.assertTrue((vault / "wiki" / "concepts" / "durable-synthesis.md").exists())
            self.assertTrue((vault / "wiki" / "entities" / "openai.md").exists())
            self.assertIn(
                "[[openai|OpenAI]]",
                (vault / "wiki" / "sources" / "durable-synthesis.md").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
