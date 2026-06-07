# Obsidian Codex Wiki Bootstrap

This file is the existing-vault bootstrap contract for Codex.

When asked to add the wiki system to an existing Obsidian vault:

1. Resolve the vault root from the user or the current workspace.
2. Run `python scripts/setup_vault.py <vault-path> --mode generic` from the plugin root, unless the user requested `lyt`, `para`, or `zettelkasten`.
3. Preserve existing notes and only add missing wiki infrastructure.
4. Check `.vault-meta/transport.json`; use filesystem transport by default.
5. Ask at most one purpose question if the vault purpose is not already clear.
6. Suggest the first ingest after setup.

The maintained structure is:

```text
vault/
|-- .raw/
|-- .vault-meta/
|-- wiki/
|   |-- index.md
|   |-- log.md
|   |-- hot.md
|   |-- overview.md
|   |-- 00.inbox/
|   |-- sources/
|   |-- literature/
|   |-- permanent/
|   |-- indexes/
|   |-- concepts/
|   |-- entities/
|   |-- questions/
|   |-- canvases/
|   `-- meta/
|-- _templates/
`-- .obsidian/
```

Use direct filesystem access unless an optional REST, MCP, or Obsidian CLI transport has been explicitly selected.
