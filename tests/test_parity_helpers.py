import json
import tempfile
import unittest
from pathlib import Path

from scripts.canvas import add_canvas_node, ensure_canvas
from scripts.dashboard import write_dashboard
from scripts.mode import set_mode
from scripts.retrieve import build_retrieval_index, search_wiki
from scripts.save_note import save_conversation
from scripts.setup_vault import setup_vault
from scripts.transport import detect_transport


class ParityHelperTests(unittest.TestCase):
    def test_setup_vault_creates_seeded_quick_start_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"

            result = setup_vault(vault, mode="lyt")

            self.assertEqual(result["mode"], "lyt")
            self.assertTrue((vault / ".vault-meta" / "mode.json").exists())
            self.assertTrue((vault / ".vault-meta" / "transport.json").exists())
            self.assertTrue((vault / "wiki" / "concepts" / "llm-wiki-pattern.md").exists())
            self.assertTrue((vault / "wiki" / "entities" / "andrej-karpathy.md").exists())
            self.assertTrue((vault / "wiki" / "meta" / "dashboard.base").exists())
            self.assertTrue((vault / ".obsidian" / "graph.json").exists())
            self.assertIn("LLM Wiki Pattern", (vault / "wiki" / "index.md").read_text(encoding="utf-8"))

    def test_existing_vault_setup_preserves_existing_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            existing = vault / "notes" / "keep.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("# Keep\n\nDo not touch.", encoding="utf-8")

            setup_vault(vault)

            self.assertEqual("# Keep\n\nDo not touch.", existing.read_text(encoding="utf-8"))
            self.assertTrue((vault / "wiki" / "hot.md").exists())

    def test_detect_transport_records_filesystem_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"

            result = detect_transport(vault)

            self.assertEqual("filesystem", result["selected"])
            self.assertTrue(result["transports"]["filesystem"]["available"])
            self.assertTrue((vault / ".vault-meta" / "transport.json").exists())

    def test_set_mode_records_templates_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"

            result = set_mode(vault, "zettelkasten")

            self.assertEqual("zettelkasten", result["mode"])
            self.assertTrue((vault / "_templates" / "zettelkasten-note.md").exists())
            mode_data = json.loads((vault / ".vault-meta" / "mode.json").read_text(encoding="utf-8"))
            self.assertEqual("zettelkasten", mode_data["mode"])

    def test_retrieval_index_and_search_return_cited_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            setup_vault(vault)
            note = vault / "wiki" / "concepts" / "durable-synthesis.md"
            note.write_text(
                "---\ntype: concept\ntitle: \"Durable Synthesis\"\n---\n\n"
                "# Durable Synthesis\n\nPersistent notes compound knowledge.",
                encoding="utf-8",
            )

            index = build_retrieval_index(vault)
            results = search_wiki(vault, "persistent knowledge", limit=3)

            self.assertIn("wiki/concepts/durable-synthesis.md", index["pages"])
            self.assertEqual("Durable Synthesis", results[0]["title"])
            self.assertIn("[[Durable Synthesis]]", results[0]["citation"])

    def test_save_conversation_creates_question_note_and_updates_hot(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            setup_vault(vault)

            result = save_conversation(vault, "Planning Thread", "User and Codex planned parity.")

            self.assertTrue((vault / result["page"]).exists())
            self.assertIn("Planning Thread", (vault / "wiki" / "hot.md").read_text(encoding="utf-8"))

    def test_canvas_helpers_create_canvas_json_with_nodes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            setup_vault(vault)

            canvas = ensure_canvas(vault, "main")
            add_canvas_node(vault, "main", "text", "Welcome", x=10, y=20)
            data = json.loads((vault / canvas["path"]).read_text(encoding="utf-8"))

            self.assertEqual(1, len(data["nodes"]))
            self.assertEqual("Welcome", data["nodes"][0]["text"])

    def test_dashboard_writer_creates_base_and_markdown_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"

            result = write_dashboard(vault)

            self.assertTrue((vault / result["base"]).exists())
            self.assertTrue((vault / result["markdown"]).exists())


if __name__ == "__main__":
    unittest.main()
