"""Create and update Obsidian canvas files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .lockfile import write_text_locked
    from .slugify import slugify_title
except ImportError:
    from lockfile import write_text_locked
    from slugify import slugify_title


def _canvas_path(vault_path: Path, name: str) -> Path:
    return vault_path / "wiki" / "canvases" / f"{slugify_title(name)}.canvas"


def _read_canvas(path: Path) -> dict[str, list[dict[str, object]]]:
    if not path.exists():
        return {"nodes": [], "edges": []}
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_canvas(vault_path: Path, name: str = "main") -> dict[str, str]:
    vault_path = vault_path.expanduser().resolve()
    path = _canvas_path(vault_path, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        write_text_locked(path, json.dumps({"nodes": [], "edges": []}, indent=2) + "\n")
    return {"name": name, "path": path.relative_to(vault_path).as_posix()}


def add_canvas_node(
    vault_path: Path,
    name: str,
    node_type: str,
    text: str,
    *,
    x: int = 0,
    y: int = 0,
    width: int = 320,
    height: int = 180,
) -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    canvas = ensure_canvas(vault_path, name)
    path = vault_path / canvas["path"]
    data = _read_canvas(path)
    node = {
        "id": f"node-{len(data['nodes']) + 1}",
        "type": node_type,
        "text": text,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }
    data["nodes"].append(node)
    write_text_locked(path, json.dumps(data, indent=2) + "\n")
    return {"path": canvas["path"], "node": node}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or update an Obsidian canvas.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--name", default="main")
    parser.add_argument("--add-text")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result: dict[str, object]
    if args.add_text:
        result = add_canvas_node(args.vault_path, args.name, "text", args.add_text)
    else:
        result = ensure_canvas(args.vault_path, args.name)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"canvas: {result['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
