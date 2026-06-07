---
name: obsidian-query
description: Answer questions from a local Obsidian wiki vault. Use when the user asks what the wiki knows, asks to query my Obsidian wiki, or wants an answer based on vault notes.
---

# Obsidian Query

Answer from the maintained wiki, not from general memory when the vault has relevant material.

## Query Order

1. Read `wiki/hot.md`.
2. Read `wiki/index.md`.
3. When available, run `python scripts/retrieve.py <vault-path> --query "<query>" --json`.
4. Read only the most relevant pages from `wiki/sources/`, `wiki/literature/`, `wiki/permanent/`, `wiki/indexes/`, `wiki/entities/`, `wiki/concepts/`, and `wiki/questions/`.
5. Synthesize an answer with citations to wiki page names.

## Answer Style

- Cite pages with wikilinks, for example `[[Concept Name]]`.
- Distinguish wiki-supported facts from inference.
- If the wiki lacks evidence, say what is missing and suggest an ingest or research step.
- After a substantial query, update `wiki/hot.md` with the active thread and key facts.

## Filing Questions

When the user wants the answer saved, create a note in `wiki/questions/` with:

```yaml
---
type: question
title: "Question Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: answered
answer_quality: draft
---
```
