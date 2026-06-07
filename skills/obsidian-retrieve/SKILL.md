---
name: obsidian-retrieve
description: Build or query a retrieval index for a local Obsidian wiki. Use when the user asks to search, retrieve, find relevant notes, or answer with wiki citations.
---

# Obsidian Retrieve

Use lightweight lexical retrieval before reading detailed pages.

## Workflow

1. Run `python scripts/retrieve.py <vault-path> --json` to refresh `.vault-meta/retrieval-index.json`.
2. Run `python scripts/retrieve.py <vault-path> --query "<query>" --json` for candidate pages.
3. Read the highest-scoring pages before answering.
4. Cite wiki pages with wikilinks and separate evidence from inference.

The current helper is lexical. Optional embedding/rerank integrations can be layered on later.
