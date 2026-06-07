---
name: obsidian-canvas
description: Create or update Obsidian canvas files for visual wiki organization. Use when the user asks for a canvas, visual map, zones, cards, or pinned notes.
---

# Obsidian Canvas

Maintain `.canvas` JSON files under `wiki/canvases/`.

## Workflow

1. Resolve the vault path and canvas name.
2. Run `python scripts/canvas.py <vault-path> --name <name>` to create the canvas.
3. Add text cards with `--add-text` or update the canvas JSON directly for files, notes, and layout zones.
4. Keep nodes readable and avoid overlapping coordinates.

Use note cards for wiki pages and text cards for summaries or zones.
