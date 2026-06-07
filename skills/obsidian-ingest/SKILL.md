---
name: obsidian-ingest
description: Ingest Markdown or text sources into a local Obsidian wiki vault. Use when the user says ingest this, add this to my wiki, process this source, or file this into Obsidian.
---

# Obsidian Ingest

Read the source, synthesize wiki notes, and maintain the vault indexes.
The v1 transport is direct filesystem access only.

## Before Writing

1. Verify the vault with `python scripts/detect_vault.py <vault-path> --create`.
2. Read `wiki/hot.md` for recent context.
3. Read `wiki/index.md` to avoid duplicate pages.
4. Check `.raw/.manifest.json` for unchanged sources when `scripts/manifest.py` is available.

## Inbox Flow

When the user asks to organize loose notes, check `wiki/00.inbox/` first.

For each Markdown file in `wiki/00.inbox/`:

1. Read the note completely.
2. Decide whether it is raw source material, a literature note, a permanent note, or an index/topic map.
3. Move or rewrite the maintained note under `wiki/sources/`, `wiki/literature/`, `wiki/permanent/`, or `wiki/indexes/`.
4. Update `wiki/index.md`, prepend one entry to `wiki/log.md`, and refresh `wiki/hot.md`.
5. Leave `wiki/00.inbox/` empty only after the material has been safely represented elsewhere.

## Single Source Flow

For each source:

1. Read the source completely.
2. Create or update one source summary in `wiki/sources/`.
3. Create or update entity notes in `wiki/entities/` for people, organizations, products, repositories, or places that matter.
4. Create or update concept notes in `wiki/concepts/` for important ideas, patterns, methods, or claims.
5. Update `wiki/index.md`.
6. Prepend one entry to `wiki/log.md`.
7. Overwrite `wiki/hot.md` with the latest context.
8. If new claims conflict with existing notes, add an Obsidian callout using `> [!contradiction]`.

## Page Rules

- Use YAML frontmatter on every wiki page.
- Use Obsidian wikilinks such as `[[Page Title]]`.
- Prefer short atomic notes over long mixed-topic pages.
- Update existing pages when they clearly match; do not create duplicates.
- Do not modify raw source files under `.raw/`.

## Helper Script

For a basic deterministic ingest of Markdown text, use:

```powershell
python scripts\ingest_source.py <vault-path> <source-path>
```

The helper creates a source page, a baseline concept page, detected entity pages, and updates `index.md`, `log.md`, `hot.md`, and `.raw/.manifest.json`.
Codex should enrich those deterministic pages when the source warrants deeper synthesis.
