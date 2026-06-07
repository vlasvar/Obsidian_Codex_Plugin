---
name: obsidian-autoresearch
description: Plan and file autonomous research loops into an Obsidian wiki. Use when the user asks to research a topic, run autoresearch, or fill knowledge gaps.
---

# Obsidian Autoresearch

Create a research plan note, then gather sources when web access is appropriate.

## Workflow

1. Resolve the vault path and topic.
2. Run `python scripts/autoresearch.py <vault-path> "<topic>" --json` to file the plan.
3. If the user wants live research, browse primary/high-quality sources, summarize them, and ingest the saved extracts.
4. End with cited wiki pages and remaining gaps.

Prefer primary sources. For time-sensitive topics, verify dates and cite web sources.
