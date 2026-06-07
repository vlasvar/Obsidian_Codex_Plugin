---
name: obsidian-lint
description: Lint a local Obsidian wiki vault for dead wikilinks, orphan pages, missing frontmatter, and stale hot cache. Use when the user asks to lint, health check, clean up, or audit the wiki.
---

# Obsidian Lint

Run a vault health check and report actionable fixes.

## Helper Script

Use the filesystem linter when available:

```powershell
python scripts\lint_wiki.py <vault-path>
```

## Checks

- Missing YAML frontmatter on wiki pages.
- Dead wikilinks that point to no page.
- Orphan pages that are not linked from another wiki page and are not core meta pages.
- Missing core files: `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`, `wiki/overview.md`.
- Stale `wiki/hot.md` based on its `updated:` frontmatter.
- Duplicate display titles.
- Weak source attribution in `wiki/sources/`.
- Dashboard and metadata drift when generated files are missing.

## Report

Group findings by severity:

- Blocker: core structure missing or unreadable.
- High: dead links or malformed pages that break navigation.
- Medium: orphan pages or stale hot cache.
- Low: style and organization suggestions.

After linting, update `wiki/hot.md` with the lint date and top findings if the user wants the report filed.
