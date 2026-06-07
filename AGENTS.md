# Agent Instructions

This file provides instructions for AI coding agents working on this project.

## Build & Test

```bash
python -m unittest discover -s tests -v
```

## Non-Interactive Shell Commands

Always use non-interactive flags to avoid hanging on confirmation prompts:

```bash
cp -f source dest
mv -f source dest
rm -f file
rm -rf directory
```

Other commands:
- `ssh` / `scp` — use `-o BatchMode=yes`
- `apt-get` — use `-y`

## Architecture

Core scripts are in `scripts/`. Skills are in `skills/`. Agent definitions are in `agents/`. See `README.md` for full vault structure and workflow.
