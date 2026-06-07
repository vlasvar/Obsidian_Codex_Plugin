import tempfile
import unittest
from pathlib import Path

from scripts.detect_vault import scaffold_vault
from scripts.lint_wiki import extract_wikilinks, lint_vault


class LintWikiTests(unittest.TestCase):
    def test_extract_wikilinks_ignores_embeds(self):
        text = "[[Concept]] ![[Image]] [[Page#Heading]] [[Alias|Text]]"
        self.assertEqual(extract_wikilinks(text), {"Concept", "Page", "Alias"})

    def test_lint_detects_dead_links_and_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            scaffold_vault(vault, create=True)
            page = vault / "wiki" / "concepts" / "Broken.md"
            page.write_text("# Broken\n\nLinks to [[Missing Page]].\n", encoding="utf-8")

            findings = lint_vault(vault)

            self.assertIn("Missing frontmatter: wiki/concepts/Broken.md", findings["high"])
            self.assertIn("Dead wikilink in wiki/concepts/Broken.md: [[Missing Page]]", findings["high"])

    def test_lint_detects_duplicate_titles_and_weak_source_attribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            scaffold_vault(vault, create=True)
            first = vault / "wiki" / "concepts" / "one.md"
            second = vault / "wiki" / "entities" / "two.md"
            source = vault / "wiki" / "sources" / "source.md"
            first.write_text("---\ntitle: \"Duplicate\"\n---\n\n# Duplicate\n", encoding="utf-8")
            second.write_text("---\ntitle: \"Duplicate\"\n---\n\n# Duplicate\n", encoding="utf-8")
            source.write_text(
                "---\ntype: source\ntitle: \"Source\"\n---\n\n# Source\n\nNo source path here.",
                encoding="utf-8",
            )

            findings = lint_vault(vault)

            self.assertTrue(any("Duplicate title" in item for item in findings["medium"]))
            self.assertTrue(any("Weak source attribution" in item for item in findings["low"]))

    def test_lint_allows_generated_source_and_concept_with_same_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            scaffold_vault(vault, create=True)
            concept = vault / "wiki" / "concepts" / "sample.md"
            source = vault / "wiki" / "sources" / "sample.md"
            concept.write_text("---\ntitle: \"Sample\"\n---\n\n# Sample\n", encoding="utf-8")
            source.write_text(
                "---\ntype: source\ntitle: \"Sample\"\n---\n\n# Sample\n\n## Source\n`raw/sample.md`\n",
                encoding="utf-8",
            )

            findings = lint_vault(vault)

            self.assertFalse(any("Duplicate title: Sample" in item for item in findings["medium"]))


if __name__ == "__main__":
    unittest.main()
