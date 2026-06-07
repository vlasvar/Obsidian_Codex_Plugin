"""Manifest tracking for immutable raw sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def source_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_path(vault_path: Path) -> Path:
    return vault_path / ".raw" / ".manifest.json"


def load_manifest(vault_path: Path) -> dict[str, Any]:
    path = manifest_path(vault_path)
    if not path.exists():
        return {"sources": {}, "address_map": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("sources", {})
    data.setdefault("address_map", {})
    return data


def save_manifest(vault_path: Path, data: dict[str, Any]) -> None:
    path = manifest_path(vault_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_key(vault_path: Path, source_path: Path) -> str:
    try:
        return source_path.resolve().relative_to(vault_path.resolve()).as_posix()
    except ValueError:
        return source_path.resolve().as_posix()


def is_unchanged(vault_path: Path, source_path: Path) -> bool:
    data = load_manifest(vault_path)
    key = source_key(vault_path, source_path)
    entry = data["sources"].get(key)
    return bool(entry and entry.get("hash") == source_hash(source_path))


def record_source(
    vault_path: Path,
    source_path: Path,
    *,
    pages_created: list[str] | None = None,
    pages_updated: list[str] | None = None,
) -> dict[str, Any]:
    data = load_manifest(vault_path)
    key = source_key(vault_path, source_path)
    data["sources"][key] = {
        "hash": source_hash(source_path),
        "ingested_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "pages_created": pages_created or [],
        "pages_updated": pages_updated or [],
    }
    save_manifest(vault_path, data)
    return data["sources"][key]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read or update a vault source manifest.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("source_path", type=Path)
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args(argv)

    if args.record:
        entry = record_source(args.vault_path, args.source_path)
        print(json.dumps(entry, indent=2))
        return 0

    print("unchanged" if is_unchanged(args.vault_path, args.source_path) else "changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
