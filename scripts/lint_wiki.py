"""Lint an Obsidian wiki vault for basic graph health."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

CORE_FILES = ["wiki/index.md", "wiki/log.md", "wiki/hot.md", "wiki/overview.md"]
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def wiki_pages(vault_path: Path) -> list[Path]:
    wiki = vault_path / "wiki"
    if not wiki.exists():
        return []
    return sorted(p for p in wiki.rglob("*.md") if p.is_file())


def page_title(path: Path) -> str:
    return path.stem


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def extract_wikilinks(text: str) -> set[str]:
    return {match.group(1).strip() for match in WIKILINK_RE.finditer(text)}


def parse_hot_updated(text: str) -> datetime | None:
    match = re.search(r"^updated:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return None
    raw = match.group(1).strip().strip('"')
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_title(path: Path, text: str) -> str:
    match = re.search(r'^title:\s*"?([^"\n]+)"?$', text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return page_title(path)


def is_allowed_generated_duplicate(rels: list[str]) -> bool:
    if len(rels) != 2:
        return False
    first, second = sorted(rels)
    if not first.startswith("wiki/concepts/") or not second.startswith("wiki/sources/"):
        return False
    return Path(first).stem == Path(second).stem


def lint_vault(vault_path: Path, *, stale_days: int = 14) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {
        "blocker": [],
        "high": [],
        "medium": [],
        "low": [],
    }

    for rel in CORE_FILES:
        if not (vault_path / rel).exists():
            findings["blocker"].append(f"Missing core file: {rel}")

    pages = wiki_pages(vault_path)
    titles = {page_title(path) for path in pages}
    incoming: dict[str, int] = {title: 0 for title in titles}
    display_titles: dict[str, list[str]] = {}
    duplicate_title_exempt_rels = {"wiki/hot.md"}

    for path in pages:
        rel = path.relative_to(vault_path).as_posix()
        text = path.read_text(encoding="utf-8")
        if rel not in duplicate_title_exempt_rels:
            display_titles.setdefault(parse_title(path, text), []).append(rel)
        if not has_frontmatter(text) and path.name not in {"index.md", "log.md", "overview.md"}:
            findings["high"].append(f"Missing frontmatter: {rel}")
        if "/sources/" in rel and ("## Source" not in text or "`" not in text):
            findings["low"].append(f"Weak source attribution: {rel}")
        for link in extract_wikilinks(text):
            if link not in titles:
                findings["high"].append(f"Dead wikilink in {rel}: [[{link}]]")
            else:
                incoming[link] += 1

    for title, rels in sorted(display_titles.items()):
        if title and len(rels) > 1 and not is_allowed_generated_duplicate(rels):
            findings["medium"].append(f"Duplicate title: {title} appears in {', '.join(rels)}")

    exempt = {"index", "log", "hot", "overview", "dashboard"}
    for title, count in incoming.items():
        if count == 0 and title not in exempt:
            findings["medium"].append(f"Orphan page: [[{title}]]")

    hot = vault_path / "wiki" / "hot.md"
    if hot.exists():
        updated = parse_hot_updated(hot.read_text(encoding="utf-8"))
        if updated is None:
            findings["medium"].append("Hot cache is missing a parseable updated timestamp.")
        else:
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            age_days = (datetime.now(timezone.utc) - updated).days
            if age_days > stale_days:
                findings["medium"].append(f"Hot cache is stale: {age_days} days old.")

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint an Obsidian wiki vault.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    findings = lint_vault(args.vault_path)
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for severity, items in findings.items():
            print(f"{severity.upper()}: {len(items)}")
            for item in items:
                print(f"- {item}")

    return 1 if findings["blocker"] or findings["high"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
