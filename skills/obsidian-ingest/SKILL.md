---
name: obsidian-ingest
description: Ingest Markdown or text sources into a local Obsidian wiki vault. Use when the user says ingest this, add this to my wiki, process this source, organize my vault, or file this into Obsidian.
---

# Obsidian Ingest

Read sources or loose vault notes, synthesize wiki notes, and maintain the vault indexes.
The v1 transport is direct filesystem access only.

## Before Writing

1. Verify the vault with `python scripts/detect_vault.py <vault-path> --create`.
2. Read `wiki/hot.md` for recent context.
3. Read `wiki/index.md` to avoid duplicate pages.
4. Check `.raw/.manifest.json` for unchanged sources when `scripts/manifest.py` is available.

## Whole-Vault Maintenance Flow

When the user asks to organize or maintain the vault, scan the whole vault for Markdown notes that are outside maintained/generated folders.

Skip obvious internal or generated locations such as `.git/`, `.obsidian/`, `.raw/`, `.vault-meta/`, `_templates/`, attachments folders, and maintained output under `wiki/archive/originals/`.

For each loose or mixed Markdown file:

1. Read the note completely.
2. Split mixed capture material into useful atomic source, literature, permanent, entity, concept, or index notes.
3. Create or update maintained notes under `wiki/sources/`, `wiki/literature/`, `wiki/permanent/`, `wiki/indexes/`, `wiki/entities/`, `wiki/concepts/`, or `wiki/questions/`.
4. Preserve provenance with a link to the original note path and a relevant snippet.
5. Move the original messy capture into `wiki/archive/originals/` only after the material has been safely represented elsewhere.
6. Update `wiki/index.md`, prepend one entry to `wiki/log.md`, refresh `wiki/hot.md`, and rebuild retrieval.

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
- Do not delete original user notes automatically; archive originals after organization.

## Helper Script

For a basic deterministic ingest of Markdown text, use:

```powershell
python scripts\ingest_source.py <vault-path> <source-path>
```

The helper creates a source page, a baseline concept page, detected entity pages, and updates `index.md`, `log.md`, `hot.md`, and `.raw/.manifest.json`.
Codex should enrich those deterministic pages when the source warrants deeper synthesis.
