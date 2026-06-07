"""Stable filename slugs for Obsidian wiki pages."""

from __future__ import annotations

import re
import sys
import unicodedata


def slugify_title(value: str, *, max_length: int = 80) -> str:
    """Return a filesystem-friendly, title-preserving slug."""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"https?://", "", normalized)
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    if not normalized:
        normalized = "untitled"
    return normalized[:max_length].rstrip("-") or "untitled"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: slugify.py <title>", file=sys.stderr)
        return 2
    print(slugify_title(" ".join(args)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
