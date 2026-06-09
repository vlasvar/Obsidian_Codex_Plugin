---
name: obsidian-wiki
description: Set up or maintain a local Obsidian wiki vault from Codex. Use when the user asks to set up an Obsidian wiki, scaffold a vault, create a knowledge base, update hot cache, or use persistent wiki memory.
---

# Obsidian Wiki

You are maintaining a local-first Obsidian vault through the filesystem.
Use direct filesystem access by default. REST, MCP, and Obsidian CLI transports are optional and must be detected before use.

Core promise: the user writes naturally anywhere in the vault, and Codex keeps the vault organized, searchable, linked, and recoverable.

## Vault Structure

Use this structure:

```text
vault/
|-- .raw/
|-- .vault-meta/
|-- wiki/
|   |-- index.md
|   |-- log.md
|   |-- hot.md
|   |-- overview.md
|   |-- sources/
|   |-- archive/
|   |   `-- originals/
|   |-- literature/
|   |-- permanent/
|   |-- indexes/
|   |-- entities/
|   |-- concepts/
|   |-- questions/
|   |-- canvases/
|   `-- meta/
|-- _templates/
`-- .obsidian/
```

`.raw/` contains imported source tracking and should not be edited except for `.raw/.manifest.json`.
`wiki/` is the maintained knowledge layer.
`wiki/archive/originals/` preserves messy original notes after Codex has organized them.

## Setup Workflow

1. Resolve the vault path from the user's message or current workspace.
2. Run `python scripts/setup_vault.py <vault-path> --mode generic` from the plugin root when the helper is available.
3. If the user requested LYT, PARA, or Zettelkasten, pass `--mode lyt`, `--mode para`, or `--mode zettelkasten`.
4. If the setup helper is not available, fall back to `python scripts/detect_vault.py <vault-path> --create`.
5. Tell the user to open the folder in Obsidian as a vault.
6. Tell the user they can keep writing anywhere in the vault and ask Codex to maintain or organize the vault later.

## Hot Cache

`wiki/hot.md` is a compact recent-context cache, not a folder for loose files. Update it after setup, ingestion, substantial queries, and lint reports.

Keep it short and overwrite it rather than turning it into a journal.

Required shape:

```markdown
---
type: meta
title: "Hot Cache"
updated: YYYY-MM-DDTHH:MM:SS
---

# Recent Context

## Last Updated
[one sentence]

## Key Recent Facts
- [fact]

## Recent Changes
- [change]

## Active Threads
- [thread]
```

## Routing

- Setup or scaffold requests: use this skill.
- Ingest requests: use `obsidian-ingest`.
- Query requests: use `obsidian-query`.
- Lint or health-check requests: use `obsidian-lint`.
- Save requests: use `obsidian-save`.
- Research requests: use `obsidian-autoresearch`.
- Canvas requests: use `obsidian-canvas`.
- Search/retrieval requests: use `obsidian-retrieve`.
- Mode requests: use `obsidian-mode`.
