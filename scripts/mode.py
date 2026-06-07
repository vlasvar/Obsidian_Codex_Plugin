"""Configure methodology modes for a Codex-maintained Obsidian wiki."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from .lockfile import write_text_locked
except ImportError:
    from lockfile import write_text_locked


MODES = {
    "generic": {
        "description": "General linked knowledge base with sources, concepts, entities, and questions.",
        "folders": ["wiki/sources", "wiki/concepts", "wiki/entities", "wiki/questions"],
        "template": "generic-note.md",
    },
    "lyt": {
        "description": "Linking Your Thinking mode with map notes and durable concept links.",
        "folders": ["wiki/maps", "wiki/sources", "wiki/concepts", "wiki/entities", "wiki/questions"],
        "template": "lyt-note.md",
    },
    "para": {
        "description": "PARA mode with projects, areas, resources, and archive views.",
        "folders": ["wiki/projects", "wiki/areas", "wiki/resources", "wiki/archive", "wiki/sources"],
        "template": "para-note.md",
    },
    "zettelkasten": {
        "description": "Zettelkasten mode with atomic permanent notes and source literature notes.",
        "folders": ["wiki/literature", "wiki/permanent", "wiki/indexes", "wiki/sources"],
        "template": "zettelkasten-note.md",
    },
}


def set_mode(vault_path: Path, mode: str = "generic") -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    normalized = mode.lower().strip()
    if normalized not in MODES:
        raise ValueError(f"Unsupported mode: {mode}. Choose one of: {', '.join(sorted(MODES))}")

    config = MODES[normalized]
    for rel in config["folders"]:
        (vault_path / rel).mkdir(parents=True, exist_ok=True)

    templates = vault_path / "_templates"
    templates.mkdir(parents=True, exist_ok=True)
    template_rel = f"_templates/{config['template']}"
    write_text_locked(
        vault_path / template_rel,
        "---\n"
        f"type: {normalized}\n"
        'title: "{{title}}"\n'
        "created: {{date}}\n"
        "updated: {{date}}\n"
        "status: draft\n"
        "---\n\n"
        "# {{title}}\n\n"
        "## Summary\n\n"
        "## Links\n\n",
    )

    meta = vault_path / ".vault-meta"
    meta.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "mode": normalized,
        "description": config["description"],
        "folders": config["folders"],
        "template": template_rel,
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    write_text_locked(meta / "mode.json", json.dumps(result, indent=2) + "\n")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Configure a wiki methodology mode.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--mode", choices=sorted(MODES), default="generic")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = set_mode(args.vault_path, args.mode)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"mode: {result['mode']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
