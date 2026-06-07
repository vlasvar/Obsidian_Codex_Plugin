# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

## Build & Test

```bash
python -m unittest discover -s tests -v
```

## Architecture Overview

A Codex-native plugin for maintaining an Obsidian wiki vault. Core scripts live in `scripts/`, skills in `skills/`, and agent definitions in `agents/`. The vault structure is documented in `README.md`.

## Conventions & Patterns

- All vault paths are passed explicitly — no hardcoded paths
- Scripts are standalone and callable directly or via Codex skills
- Use non-interactive flags for shell operations (`cp -f`, `rm -f`, `mv -f`)
