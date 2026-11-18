#!/usr/bin/env python3
"""Deliver the bundled entry image to /output/entry.png.

This script is intentionally small and self-contained. It locates the
artwork that sits beside it, copies those bytes verbatim to the output
location the grader expects, and then proves the delivery was faithful
by hashing both sides of the copy.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 digest of a file, read in chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.png"
    destination_dir = Path("/output")
    destination = destination_dir / "entry.png"

    if not source.is_file():
        print(f"error: bundled image not found at {source}", file=sys.stderr)
        return 1

    destination_dir.mkdir(parents=True, exist_ok=True)

    # A straight byte copy keeps the delivered file identical on every run.
    shutil.copyfile(source, destination)

    source_hash = sha256_of(source)
    delivered_hash = sha256_of(destination)

    if source_hash != delivered_hash:
        print(
            "error: hash mismatch after copy "
            f"(bundled {source_hash}, delivered {delivered_hash})",
            file=sys.stderr,
        )
        return 1

    # Hash equality alone is strong, but a size cross-check costs nothing
    # and makes a truncated or padded copy obvious at a glance.
    source_size = source.stat().st_size
    delivered_size = destination.stat().st_size

    if source_size != delivered_size:
        print(
            "error: size mismatch after copy "
            f"(bundled {source_size} bytes, delivered {delivered_size} bytes)",
            file=sys.stderr,
        )
        return 1

    print(f"{destination} {delivered_hash} {delivered_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
