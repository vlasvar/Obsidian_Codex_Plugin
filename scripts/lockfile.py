"""Small lockfile helper for safe page writes."""

from __future__ import annotations

import contextlib
import os
import time
from pathlib import Path
from typing import Iterator


class LockError(RuntimeError):
    """Raised when a lock cannot be acquired."""


@contextlib.contextmanager
def file_lock(target: Path, *, timeout: float = 10.0, stale_after: float = 60.0) -> Iterator[None]:
    lock_path = target.with_suffix(target.suffix + ".lock")
    deadline = time.monotonic() + timeout
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"pid={os.getpid()}\ncreated={time.time()}\n")
            break
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > stale_after:
                    lock_path.unlink(missing_ok=True)
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= deadline:
                raise LockError(f"timed out waiting for lock: {lock_path}")
            time.sleep(0.1)

    try:
        yield
    finally:
        lock_path.unlink(missing_ok=True)


def write_text_locked(path: Path, content: str) -> None:
    with file_lock(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
