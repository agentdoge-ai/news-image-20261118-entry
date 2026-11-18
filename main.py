#!/usr/bin/env python3
"""news-image-20261118 entry program.

The entry artwork is a finished front-page image bundled beside this
script as ``entry.png``. Running the program copies that file, byte for
byte, to ``/output/entry.png``. Nothing is generated at run time, so
every run produces identical bytes.

Standard library only; no network access.
"""

import hashlib
import os
import shutil
import sys

OUTPUT_PATH = os.path.join("/output", "entry.png")


def file_digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(1 << 16)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(here, "entry.png")
    if not os.path.isfile(bundled):
        sys.stderr.write("missing bundled artwork: %s\n" % bundled)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    shutil.copyfile(bundled, OUTPUT_PATH)
    expected = file_digest(bundled)
    actual = file_digest(OUTPUT_PATH)
    if actual != expected:
        sys.stderr.write(
            "sha256 mismatch: bundled=%s output=%s\n" % (expected, actual)
        )
        return 1
    print("delivered %s sha256=%s" % (OUTPUT_PATH, actual))
    return 0


if __name__ == "__main__":
    sys.exit(run())
