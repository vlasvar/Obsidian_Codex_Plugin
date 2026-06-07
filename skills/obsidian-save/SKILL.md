---
name: obsidian-save
description: Save a conversation, answer, or named thread into a local Obsidian wiki. Use when the user says save this, file this conversation, or persist this answer in the wiki.
---

# Obsidian Save

Save useful conversation context as a durable wiki note.

## Workflow

1. Resolve the vault path.
2. Choose a concise title from the user request or ask for one only if missing.
3. Run `python scripts/save_note.py <vault-path> "<title>" --content-file <temp-file>` when the helper is available.
4. Confirm the created `wiki/questions/` page and mention that `wiki/hot.md` was updated.

Keep the saved note factual and concise. Do not invent missing conversation details.
