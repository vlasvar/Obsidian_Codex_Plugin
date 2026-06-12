---
name: obsidian-zettelkasten-organizer
description: "Organize and maintain an Obsidian vault using Zettelkasten principles (sources, literature, permanent, indexes) using native Hermes tools."
version: 1.0.0
author: Hermes Agent (based on vlasvar/Obsidian_Codex_Plugin)
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, Zettelkasten, Knowledge-Management, File-Organization]
    related_skills: [obsidian]
---

# Obsidian Zettelkasten Organizer

This skill provides a structured workflow for maintaining an Obsidian vault using Zettelkasten/Luhmann methodology. It is designed to be used by Hermes Agent to automatically organize loose or new notes without disturbing already well-organized content.

## When to Use
- You have accumulated new notes in `wiki/00_inbox` or scattered across the vault.
- You want to enforce a clean separation between raw sources, literature, permanent notes, and index maps.
- You want an AI to handle the mechanical sorting while leaving ambiguous notes for your human review.

## Core Principles
1. **Sources**: Raw, unprocessed material, meeting notes, or direct copy-pastes go to `wiki/sources/`.
2. **Literature**: Notes derived from articles, videos, research papers, or books go to `wiki/literature/`.
3. **Permanent**: The user's own clear ideas, syntheses, or conclusions go to `wiki/permanent/`.
4. **Indexes**: When a large theme becomes visible, create or update an index in `wiki/indexes/` to link related notes.
5. **Preservation**: Always preserve original content. Improve frontmatter, tags, and wikilinks when useful.
6. **Ambiguity**: Leave ambiguous notes in their current location (or add a `#needs-review` tag) rather than forcing a wrong classification.
7. **Non-Interference**: Do not disturb notes that are already clearly organized with proper frontmatter and links.

## Execution Workflow

### 1. Scan for New/Stranded Notes
Use `search_files` or `terminal` to identify `.md` files in `wiki/00_inbox` or files in the root `wiki/` directory that lack proper frontmatter or index links.

### 2. Classify and Move
For each candidate note:
- Read the note using `read_file`.
- Determine its category based on the Core Principles.
- If it belongs in a subfolder (e.g., `wiki/sources/`), use `terminal` (`mv` or `move`) to move the file, or `write_file` to create it in the new location and `terminal` to remove the old one.

### 3. Enhance Metadata
- Ensure the note has clean YAML frontmatter (e.g., `type`, `title`, `date`, `tags`).
- Add relevant wikilinks `[[like-this]]` to existing concepts or indexes if a clear connection exists.

### 4. Update Indexes
If a note introduces or strongly relates to a new theme, check `wiki/indexes/`. If an index doesn't exist, create it. If it does, append a link to the new note.

### 5. Report Back
At the end of the run, provide a concise summary to the user:
- ✅ Notes successfully organized (and where they went).
- ⚠️ Notes left for human review (and why).
- 🛡️ Confirmation that already organized notes were left untouched.

## Example Hermes Prompt
"Use the `obsidian-zettelkasten-organizer` skill to check `wiki/00_inbox` and organize any stranded notes in my vault at `[YOUR_VAULT_PATH]`."

## Pitfalls to Avoid
- **Do not delete original files** unless you have explicitly moved their content and confirmed the new file is correctly saved.
- **Do not over-link**. Only add wikilinks if the connection is strong and contextual.
- **Do not guess**. If a note's purpose is unclear, tag it with `#needs-review` and leave it in a visible location.