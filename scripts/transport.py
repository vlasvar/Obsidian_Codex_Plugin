"""Detect optional Obsidian transports while keeping filesystem as default."""

from __future__ import annotations

import argparse
import json
import shutil
import socket
from datetime import datetime, timezone
from pathlib import Path

try:
    from .lockfile import write_text_locked
except ImportError:
    from lockfile import write_text_locked


def _port_open(host: str, port: int, timeout: float = 0.2) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def detect_transport(vault_path: Path, *, rest_port: int = 27124) -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    meta = vault_path / ".vault-meta"
    meta.mkdir(parents=True, exist_ok=True)
    transports = {
        "filesystem": {
            "available": True,
            "reason": "Direct local file access is always available to this plugin.",
        },
        "rest": {
            "available": _port_open("127.0.0.1", rest_port),
            "port": rest_port,
        },
        "mcp": {
            "available": shutil.which("npx") is not None,
            "reason": "npx is available for optional MCP vault servers." if shutil.which("npx") else "npx not found.",
        },
        "obsidian_cli": {
            "available": shutil.which("obsidian") is not None,
            "reason": "obsidian CLI found." if shutil.which("obsidian") else "obsidian CLI not found.",
        },
    }
    result: dict[str, object] = {
        "selected": "filesystem",
        "manual_override": False,
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "transports": transports,
    }
    write_text_locked(meta / "transport.json", json.dumps(result, indent=2) + "\n")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect available Obsidian transports.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = detect_transport(args.vault_path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"selected transport: {result['selected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
