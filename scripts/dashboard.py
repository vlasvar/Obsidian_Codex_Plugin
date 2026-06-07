"""Create Obsidian dashboard files for the maintained wiki."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from .lockfile import write_text_locked
except ImportError:
    from lockfile import write_text_locked


def write_dashboard(vault_path: Path) -> dict[str, str]:
    vault_path = vault_path.expanduser().resolve()
    meta = vault_path / "wiki" / "meta"
    meta.mkdir(parents=True, exist_ok=True)

    base_rel = "wiki/meta/dashboard.base"
    md_rel = "wiki/meta/dashboard.md"
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    base = {
        "version": 1,
        "name": "Wiki Dashboard",
        "description": "Clean-room dashboard metadata for the Codex-maintained Obsidian wiki.",
        "updated": now,
        "views": [
            {"name": "Inbox", "folder": "wiki/00.inbox", "type": "inbox"},
            {"name": "Sources", "folder": "wiki/sources", "type": "source"},
            {"name": "Literature", "folder": "wiki/literature", "type": "literature"},
            {"name": "Permanent", "folder": "wiki/permanent", "type": "permanent"},
            {"name": "Indexes", "folder": "wiki/indexes", "type": "index"},
            {"name": "Concepts", "folder": "wiki/concepts", "type": "concept"},
            {"name": "Entities", "folder": "wiki/entities", "type": "entity"},
            {"name": "Questions", "folder": "wiki/questions", "type": "question"},
        ],
    }
    write_text_locked(vault_path / base_rel, json.dumps(base, indent=2) + "\n")
    write_text_locked(
        vault_path / md_rel,
        "---\ntype: meta\ntitle: \"Wiki Dashboard\"\n---\n\n"
        "# Wiki Dashboard\n\n"
        "- [[index|Wiki Index]]\n"
        "- [[hot|Hot Cache]]\n"
        "- [[log|Wiki Log]]\n"
        "- Inbox: `wiki/00.inbox/`\n"
        "- Sources: `wiki/sources/`\n"
        "- Literature: `wiki/literature/`\n"
        "- Permanent notes: `wiki/permanent/`\n"
        "- Indexes: `wiki/indexes/`\n"
        "- Concepts: `wiki/concepts/`\n"
        "- Entities: `wiki/entities/`\n"
        "- Questions: `wiki/questions/`\n",
    )
    return {"base": base_rel, "markdown": md_rel}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Obsidian dashboard metadata.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = write_dashboard(args.vault_path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"dashboard: {result['base']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
