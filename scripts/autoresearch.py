"""Create a clean-room autoresearch plan note for a topic."""

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


def create_research_plan(vault_path: Path, topic: str, *, rounds: int = 3) -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    scaffold_vault(vault_path, create=True)
    today = datetime.now(timezone.utc).date().isoformat()
    slug = slugify_title(topic)
    rel = f"wiki/questions/research-{slug}.md"
    content = (
        "---\n"
        "type: question\n"
        f'title: "Research: {topic}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        "status: planned\n"
        "answer_quality: research-plan\n"
        "---\n\n"
        f"# Research: {topic}\n\n"
        "## Research Program\n\n"
        f"- Topic: {topic}\n"
        f"- Rounds: {rounds}\n"
        "- Preferred sources: official documentation, primary sources, high-signal references.\n"
        "- Output: source notes, concept/entity notes, cited synthesis, and remaining gaps.\n\n"
        "## Open Questions\n\n"
        "- What must be true for this topic to be considered understood?\n"
        "- Which claims need primary-source support?\n"
    )
    write_text_locked(vault_path / rel, content)
    return {"topic": topic, "rounds": rounds, "page": rel}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an autoresearch plan note.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("topic")
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = create_research_plan(args.vault_path, args.topic, rounds=args.rounds)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"research plan: {result['page']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
