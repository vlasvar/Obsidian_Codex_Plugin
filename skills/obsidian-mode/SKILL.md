---
name: obsidian-mode
description: Configure methodology modes for an Obsidian wiki. Use when the user asks for LYT, PARA, Zettelkasten, generic mode, or a different knowledge-management method.
---

# Obsidian Mode

Set the vault methodology mode.

## Modes

- `generic`: sources, concepts, entities, questions.
- `lyt`: maps, concepts, sources, entities, questions.
- `para`: projects, areas, resources, archive, sources.
- `zettelkasten`: literature, permanent notes, indexes, sources.

## Workflow

Run `python scripts/mode.py <vault-path> --mode <mode> --json`.

Mode metadata is written to `.vault-meta/mode.json`, and templates are written under `_templates/`.
