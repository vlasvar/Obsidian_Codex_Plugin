---
name: obsidian-transport
description: Detect optional Obsidian transports while keeping filesystem access as the default. Use when the user asks about REST API, MCP, Obsidian CLI, or transport setup.
---

# Obsidian Transport

Detect available transports and record them in `.vault-meta/transport.json`.

## Workflow

Run `python scripts/transport.py <vault-path> --json`.

Filesystem transport remains selected unless the user explicitly asks to use another available transport. REST on port `27124`, MCP tooling, and Obsidian CLI are optional.
