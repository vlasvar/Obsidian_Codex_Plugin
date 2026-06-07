"""Verify or create the filesystem structure for an Obsidian wiki vault."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


CORE_DIRS = [
    ".raw",
    ".obsidian",
    "wiki",
    "wiki/sources",
    "wiki/entities",
    "wiki/concepts",
    "wiki/questions",
    "wiki/meta",
]

CORE_FILES = {
    "wiki/index.md": "# Wiki Index\n\nNo pages have been indexed yet.\n",
    "wiki/log.md": "# Wiki Log\n\nNo operations recorded yet.\n",
    "wiki/overview.md": "# Wiki Overview\n\nThis wiki has not been summarized yet.\n",
}


def hot_cache_template() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return (
        "---\n"
        "type: meta\n"
        'title: "Hot Cache"\n'
        f"updated: {now}\n"
        "---\n\n"
        "# Recent Context\n\n"
        "## Last Updated\n"
        "Vault scaffolded or verified.\n\n"
        "## Key Recent Facts\n"
        "- The vault is ready for source ingestion.\n\n"
        "## Recent Changes\n"
        "- Core wiki folders and files are present.\n\n"
        "## Active Threads\n"
        "- None yet.\n"
    )


def scaffold_vault(vault_path: Path, *, create: bool = False) -> dict[str, list[str]]:
    vault_path = vault_path.expanduser().resolve()
    missing_dirs: list[str] = []
    missing_files: list[str] = []
    created: list[str] = []

    for rel in CORE_DIRS:
        target = vault_path / rel
        if target.exists():
            continue
        missing_dirs.append(rel)
        if create:
            target.mkdir(parents=True, exist_ok=True)
            created.append(rel)

    all_files = dict(CORE_FILES)
    all_files["wiki/hot.md"] = hot_cache_template()
    for rel, content in all_files.items():
        target = vault_path / rel
        if target.exists():
            continue
        missing_files.append(rel)
        if create:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            created.append(rel)

    manifest = vault_path / ".raw" / ".manifest.json"
    if not manifest.exists():
        missing_files.append(".raw/.manifest.json")
        if create:
            manifest.parent.mkdir(parents=True, exist_ok=True)
            manifest.write_text('{\n  "sources": {},\n  "address_map": {}\n}\n', encoding="utf-8")
            created.append(".raw/.manifest.json")

    return {
        "missing_dirs": missing_dirs,
        "missing_files": missing_files,
        "created": created,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify or create an Obsidian wiki vault.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--create", action="store_true", help="Create missing folders and seed files.")
    args = parser.parse_args(argv)

    result = scaffold_vault(args.vault_path, create=args.create)
    if result["created"]:
        print("created:")
        for item in result["created"]:
            print(f"- {item}")
    elif result["missing_dirs"] or result["missing_files"]:
        print("missing:")
        for item in result["missing_dirs"] + result["missing_files"]:
            print(f"- {item}")
        return 1
    else:
        print("vault ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
