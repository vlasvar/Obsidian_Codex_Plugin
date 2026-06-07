"""Quick-start setup for a ready-to-open Obsidian wiki vault."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from .canvas import ensure_canvas
    from .dashboard import write_dashboard
    from .detect_vault import scaffold_vault
    from .lockfile import write_text_locked
    from .mode import set_mode
    from .retrieve import build_retrieval_index
    from .transport import detect_transport
except ImportError:
    from canvas import ensure_canvas
    from dashboard import write_dashboard
    from detect_vault import scaffold_vault
    from lockfile import write_text_locked
    from mode import set_mode
    from retrieve import build_retrieval_index
    from transport import detect_transport


def _write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_locked(path, content)
    return True


def _frontmatter(note_type: str, title: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return (
        "---\n"
        f"type: {note_type}\n"
        f'title: "{title}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "status: seed\n"
        "---\n\n"
    )


def seed_notes(vault_path: Path) -> list[str]:
    created: list[str] = []
    seeds = {
        "wiki/concepts/llm-wiki-pattern.md": _frontmatter("concept", "LLM Wiki Pattern")
        + "# LLM Wiki Pattern\n\n"
        + "A maintained wiki lets an AI agent compound project knowledge through linked, cited notes.\n\n"
        + "## Links\n\n- [[hot-cache|Hot Cache]]\n- [[compounding-knowledge|Compounding Knowledge]]\n",
        "wiki/concepts/hot-cache.md": _frontmatter("concept", "Hot Cache")
        + "# Hot Cache\n\n"
        + "A short session-memory note that helps the next Codex turn resume with recent context.\n\n"
        + "## Links\n\n- [[llm-wiki-pattern|LLM Wiki Pattern]]\n",
        "wiki/concepts/compounding-knowledge.md": _frontmatter("concept", "Compounding Knowledge")
        + "# Compounding Knowledge\n\n"
        + "Each ingest, query, and lint pass should leave the vault easier to use next time.\n\n"
        + "## Links\n\n- [[llm-wiki-pattern|LLM Wiki Pattern]]\n",
        "wiki/entities/andrej-karpathy.md": _frontmatter("entity", "Andrej Karpathy")
        + "# Andrej Karpathy\n\n"
        + "Associated with the public LLM wiki pattern that inspired this clean-room Codex workflow.\n\n"
        + "## Links\n\n- [[llm-wiki-pattern|LLM Wiki Pattern]]\n",
    }
    for rel, content in seeds.items():
        if _write_if_missing(vault_path / rel, content):
            created.append(rel)
    return created


def write_obsidian_config(vault_path: Path) -> list[str]:
    created: list[str] = []
    configs = {
        ".obsidian/graph.json": json.dumps(
            {
                "collapse-filter": False,
                "search": "-path:.raw",
                "colorGroups": [
                    {"query": "path:wiki/concepts", "color": {"a": 1, "rgb": 3447003}},
                    {"query": "path:wiki/sources", "color": {"a": 1, "rgb": 2263842}},
                    {"query": "path:wiki/entities", "color": {"a": 1, "rgb": 10181046}},
                ],
            },
            indent=2,
        )
        + "\n",
        ".obsidian/app.json": json.dumps(
            {"attachmentFolderPath": "_attachments", "alwaysUpdateLinks": True, "showUnsupportedFiles": False},
            indent=2,
        )
        + "\n",
        ".obsidian/appearance.json": json.dumps({"cssTheme": "", "enabledCssSnippets": ["vault-colors"]}, indent=2)
        + "\n",
        ".obsidian/snippets/vault-colors.css": (
            "/* Clean-room folder color hints for the generated wiki. */\n"
            ".nav-folder-title[data-path^=\"wiki/concepts\"] { color: #2563eb; }\n"
            ".nav-folder-title[data-path^=\"wiki/sources\"] { color: #15803d; }\n"
            ".nav-folder-title[data-path^=\"wiki/entities\"] { color: #7e22ce; }\n"
        ),
    }
    for rel, content in configs.items():
        if _write_if_missing(vault_path / rel, content):
            created.append(rel)
    return created


def refresh_index(vault_path: Path) -> None:
    write_text_locked(
        vault_path / "wiki" / "index.md",
        "# Wiki Index\n\n"
        "## Seed Pages\n\n"
        "- [[llm-wiki-pattern|LLM Wiki Pattern]]\n"
        "- [[hot-cache|Hot Cache]]\n"
        "- [[compounding-knowledge|Compounding Knowledge]]\n"
        "- [[andrej-karpathy|Andrej Karpathy]]\n\n"
        "## Working Areas\n\n"
        "- Sources: `wiki/sources/`\n"
        "- Concepts: `wiki/concepts/`\n"
        "- Entities: `wiki/entities/`\n"
        "- Questions: `wiki/questions/`\n",
    )


def setup_vault(vault_path: Path, *, mode: str = "generic") -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    vault_path.mkdir(parents=True, exist_ok=True)
    scaffold = scaffold_vault(vault_path, create=True)
    seeded = seed_notes(vault_path)
    refresh_index(vault_path)
    dashboard = write_dashboard(vault_path)
    mode_result = set_mode(vault_path, mode)
    transport = detect_transport(vault_path)
    canvas = ensure_canvas(vault_path, "main")
    obsidian_config = write_obsidian_config(vault_path)
    retrieval = build_retrieval_index(vault_path)
    return {
        "vault": str(vault_path),
        "mode": mode_result["mode"],
        "created": scaffold["created"] + seeded + obsidian_config,
        "dashboard": dashboard,
        "transport": transport["selected"],
        "canvas": canvas["path"],
        "indexed_pages": len(retrieval["pages"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set up a ready-to-open Obsidian wiki vault.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--mode", default="generic", choices=["generic", "lyt", "para", "zettelkasten"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = setup_vault(args.vault_path, mode=args.mode)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"vault ready: {result['vault']}")
        print(f"mode: {result['mode']}")
        print(f"transport: {result['transport']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
