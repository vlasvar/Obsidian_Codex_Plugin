"""Save a conversation or answer as a wiki question note."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from .detect_vault import scaffold_vault
    from .lockfile import write_text_locked
    from .slugify import slugify_title
except ImportError:
    from detect_vault import scaffold_vault
    from lockfile import write_text_locked
    from slugify import slugify_title


def save_conversation(vault_path: Path, title: str, content: str) -> dict[str, str]:
    vault_path = vault_path.expanduser().resolve()
    scaffold_vault(vault_path, create=True)
    today = datetime.now(timezone.utc).date().isoformat()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    slug = slugify_title(title)
    rel = f"wiki/questions/{slug}.md"
    note = (
        "---\n"
        "type: question\n"
        f'title: "{title}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "status: answered\n"
        "answer_quality: draft\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Saved Context\n\n"
        f"{content.strip()}\n"
    )
    write_text_locked(vault_path / rel, note)
    write_text_locked(
        vault_path / "wiki" / "hot.md",
        "---\ntype: meta\n"
        'title: "Hot Cache"\n'
        f"updated: {now}\n---\n\n"
        "# Recent Context\n\n"
        "## Last Updated\n"
        f"Saved conversation note {title}.\n\n"
        "## Key Recent Facts\n"
        f"- [[{slug}|{title}]] captures the latest saved thread.\n\n"
        "## Recent Changes\n"
        f"- Created or updated `{rel}`.\n\n"
        "## Active Threads\n"
        f"- Continue from [[{slug}|{title}]].\n",
    )
    return {"title": title, "page": rel}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Save a conversation into wiki/questions.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("title")
    parser.add_argument("--content", default="")
    parser.add_argument("--content-file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    content = args.content_file.read_text(encoding="utf-8") if args.content_file else args.content
    result = save_conversation(args.vault_path, args.title, content)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"saved: {result['page']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
