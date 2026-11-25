#!/usr/bin/env python3
"""news-image-20261124-r4: copy the shipped entry.png to the output dir.

Standard library only. Verifies the baked-in SHA-256 of entry.png
before writing, and exits non-zero on any mismatch.
"""
import hashlib
import os
import shutil
import struct
import sys

EXPECTED_SHA256 = "2afe18b2eb178dd447c1b1e750ece34bb301e8f4f332721320056304c6a67d8f"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(src, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"entry.png SHA-256 mismatch: got {digest}, expected {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"entry.png dimensions {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
