"""Deterministic baseline ingest for Markdown/text sources."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from .detect_vault import scaffold_vault
    from .lockfile import write_text_locked
    from .manifest import is_unchanged, record_source
    from .slugify import slugify_title
except ImportError:
    from detect_vault import scaffold_vault
    from lockfile import write_text_locked
    from manifest import is_unchanged, record_source
    from slugify import slugify_title


def title_from_source(source_path: Path, text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+)$", line.strip().lstrip("\ufeff"))
        if match:
            return match.group(1).strip()
    return source_path.stem.replace("-", " ").replace("_", " ").title()


def summarize_text(text: str, *, max_chars: int = 900) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3].rstrip() + "..."


def frontmatter(note_type: str, title: str, status: str = "draft") -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return (
        "---\n"
        f"type: {note_type}\n"
        f'title: "{title}"\n'
        f"created: {today}\n"
        f"updated: {today}\n"
        f"status: {status}\n"
        "---\n\n"
    )


def wiki_alias(slug: str, title: str) -> str:
    return f"[[{slug}|{title}]]"


def extract_entities(text: str, *, exclude: set[str] | None = None) -> list[str]:
    exclude = exclude or set()
    candidates = re.findall(r"\b(?:[A-Z][A-Za-z0-9]+|[A-Z]{2,})(?:[ \t]+[A-Z][A-Za-z0-9]+)*\b", text)
    ignored = {"The", "This", "Source", "Summary", "Links", "Add"}
    entities: list[str] = []
    for candidate in candidates:
        cleaned = candidate.strip()
        if cleaned in ignored or cleaned in exclude or len(cleaned) < 3:
            continue
        if cleaned not in entities:
            entities.append(cleaned)
    return entities[:8]


def write_concept_page(vault_path: Path, title: str, source_slug: str, source_title: str) -> str:
    slug = slugify_title(title)
    rel = f"wiki/concepts/{slug}.md"
    path = vault_path / rel
    content = (
        frontmatter("concept", title, "draft")
        + f"# {title}\n\n"
        + "## Summary\n"
        + f"Concept synthesized from {wiki_alias(source_slug, source_title)}.\n\n"
        + "## Links\n"
        + f"- Source: {wiki_alias(source_slug, source_title)}\n"
    )
    write_text_locked(path, content)
    return rel


def write_entity_page(vault_path: Path, title: str, source_slug: str, source_title: str) -> str:
    slug = slugify_title(title)
    rel = f"wiki/entities/{slug}.md"
    path = vault_path / rel
    content = (
        frontmatter("entity", title, "draft")
        + f"# {title}\n\n"
        + "## Summary\n"
        + f"Entity mentioned in {wiki_alias(source_slug, source_title)}.\n\n"
        + "## Links\n"
        + f"- Source: {wiki_alias(source_slug, source_title)}\n"
    )
    write_text_locked(path, content)
    return rel


def update_index(vault_path: Path, title: str, slug: str, source_page: str) -> None:
    index = vault_path / "wiki" / "index.md"
    existing = index.read_text(encoding="utf-8") if index.exists() else "# Wiki Index\n\n"
    entry = f"- {wiki_alias(slug, title)} - source summary at `{source_page}`\n"
    if entry not in existing:
        existing = existing.rstrip() + "\n" + entry
    write_text_locked(index, existing)


def prepend_log(vault_path: Path, title: str, slug: str, source_rel: str, page_title: str) -> None:
    log = vault_path / "wiki" / "log.md"
    existing = log.read_text(encoding="utf-8") if log.exists() else "# Wiki Log\n\n"
    today = datetime.now(timezone.utc).date().isoformat()
    entry = (
        f"## [{today}] ingest | {title}\n"
        f"- Source: `{source_rel}`\n"
        f"- Summary: {wiki_alias(slug, page_title)}\n"
        f"- Pages created: {wiki_alias(slug, page_title)}\n"
        "- Key insight: Baseline source summary added for later synthesis.\n\n"
    )
    body = existing.removeprefix("# Wiki Log\n\n")
    write_text_locked(log, "# Wiki Log\n\n" + entry + body)


def update_hot(vault_path: Path, title: str, slug: str, page_title: str) -> None:
    hot = vault_path / "wiki" / "hot.md"
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    content = (
        "---\n"
        "type: meta\n"
        'title: "Hot Cache"\n'
        f"updated: {now}\n"
        "---\n\n"
        "# Recent Context\n\n"
        "## Last Updated\n"
        f"Ingested {title}.\n\n"
        "## Key Recent Facts\n"
        f"- {wiki_alias(slug, page_title)} is the latest source summary.\n\n"
        "## Recent Changes\n"
        f"- Created or updated {wiki_alias(slug, page_title)}.\n\n"
        "## Active Threads\n"
        "- Continue synthesizing entities and concepts from recent ingests.\n"
    )
    write_text_locked(hot, content)


def ingest_source(vault_path: Path, source_path: Path, *, force: bool = False) -> dict[str, str]:
    vault_path = vault_path.expanduser().resolve()
    source_path = source_path.expanduser().resolve()
    scaffold_vault(vault_path, create=True)

    if not force and is_unchanged(vault_path, source_path):
        return {"status": "unchanged", "title": "", "page": ""}

    text = source_path.read_text(encoding="utf-8")
    title = title_from_source(source_path, text)
    slug = slugify_title(title)
    page_title = title
    page_rel = f"wiki/sources/{slug}.md"
    page_path = vault_path / page_rel
    try:
        source_rel = source_path.relative_to(vault_path).as_posix()
    except ValueError:
        source_rel = source_path.as_posix()

    entities = extract_entities(text, exclude={title})
    entity_links = [wiki_alias(slugify_title(entity), entity) for entity in entities]
    structured_links = [f"- Concept: {wiki_alias(slug, page_title)}"]
    structured_links.extend(f"- Entity: {link}" for link in entity_links)

    content = (
        frontmatter("source", page_title, "draft")
        + f"# {page_title}\n\n"
        + "## Source\n"
        + f"`{source_rel}`\n\n"
        + "## Summary\n"
        + summarize_text(text)
        + "\n\n## Links\n"
        + "\n".join(structured_links)
        + "\n"
    )
    existed = page_path.exists()
    write_text_locked(page_path, content)
    created_or_updated_pages = [page_rel]
    concept_rel = write_concept_page(vault_path, page_title, slug, page_title)
    created_or_updated_pages.append(concept_rel)
    for entity in entities:
        created_or_updated_pages.append(write_entity_page(vault_path, entity, slug, page_title))
    update_index(vault_path, page_title, slug, page_rel)
    prepend_log(vault_path, title, slug, source_rel, page_title)
    update_hot(vault_path, title, slug, page_title)
    record_source(
        vault_path,
        source_path,
        pages_created=[] if existed else created_or_updated_pages,
        pages_updated=created_or_updated_pages + ["wiki/index.md", "wiki/log.md", "wiki/hot.md"],
    )
    return {"status": "updated" if existed else "created", "title": page_title, "page": page_rel}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest a Markdown/text source into an Obsidian wiki vault.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("source_path", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    result = ingest_source(args.vault_path, args.source_path, force=args.force)
    print(f"{result['status']}: {result['page']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
