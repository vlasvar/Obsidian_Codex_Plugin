"""Build a lightweight lexical retrieval index for wiki pages."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from .lockfile import write_text_locked
except ImportError:
    from lockfile import write_text_locked

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
EXCLUDED_DIRS = {
    ".git",
    ".obsidian",
    ".raw",
    ".trash",
    ".vault-meta",
    "_attachments",
    "_templates",
    "attachments",
    "node_modules",
}


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _title_from_text(path: Path, text: str) -> str:
    match = re.search(r'^title:\s*"?([^"\n]+)"?$', text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def _vault_pages(vault_path: Path) -> list[Path]:
    if not vault_path.exists():
        return []
    pages: list[Path] = []
    for path in vault_path.rglob("*.md"):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(vault_path).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        pages.append(path)
    return sorted(pages)


def build_retrieval_index(vault_path: Path) -> dict[str, object]:
    vault_path = vault_path.expanduser().resolve()
    pages: dict[str, dict[str, object]] = {}
    for path in _vault_pages(vault_path):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(vault_path).as_posix()
        counts = Counter(_tokens(text))
        pages[rel] = {
            "title": _title_from_text(path, text),
            "token_count": sum(counts.values()),
            "top_terms": [term for term, _ in counts.most_common(12)],
        }

    meta = vault_path / ".vault-meta"
    meta.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "updated": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "strategy": "whole-vault lexical",
        "pages": pages,
    }
    write_text_locked(meta / "retrieval-index.json", json.dumps(result, indent=2) + "\n")
    return result


def search_wiki(vault_path: Path, query: str, *, limit: int = 5) -> list[dict[str, object]]:
    vault_path = vault_path.expanduser().resolve()
    query_terms = set(_tokens(query))
    results: list[dict[str, object]] = []
    for path in _vault_pages(vault_path):
        text = path.read_text(encoding="utf-8")
        body_terms = Counter(_tokens(text))
        matched_terms = {term for term in query_terms if body_terms[term] > 0}
        score = (len(matched_terms) * 100) + sum(body_terms[term] for term in matched_terms)
        if score <= 0:
            continue
        title = _title_from_text(path, text)
        results.append(
            {
                "title": title,
                "path": path.relative_to(vault_path).as_posix(),
                "score": score,
                "citation": f"[[{title}]]",
            }
        )
    return sorted(results, key=lambda item: (-int(item["score"]), str(item["title"])))[:limit]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or query the wiki retrieval index.")
    parser.add_argument("vault_path", type=Path)
    parser.add_argument("--query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result: object = search_wiki(args.vault_path, args.query, limit=args.limit) if args.query else build_retrieval_index(args.vault_path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if isinstance(result, list):
            for item in result:
                print(f"{item['score']}: {item['citation']} {item['path']}")
        else:
            print(f"indexed: {len(result['pages'])} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
