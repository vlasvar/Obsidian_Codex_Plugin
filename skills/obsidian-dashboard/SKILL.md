---
name: obsidian-dashboard
description: Create or refresh Obsidian wiki dashboard files. Use when the user asks for dashboard, Bases, metadata views, or a wiki overview panel.
---

# Obsidian Dashboard

Generate dashboard metadata and a markdown fallback.

## Workflow

Run `python scripts/dashboard.py <vault-path> --json`.

The helper writes `wiki/meta/dashboard.base` and `wiki/meta/dashboard.md`. Keep dashboard content generated from wiki folders and metadata rather than hard-coded source claims.
