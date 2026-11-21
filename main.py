#!/usr/bin/env python3
"""news-image-20261120, account 3 (fansevanoo) -- WORLD-ATLAS poster.

Stdlib-only entry point. The poster itself is the pre-rendered entry.png
in this repository (drawn with PIL at authoring time, 1024x1024, 33
verified Friday 20 November 2026 stories in an atlas / map-led layout).
This script only copies that PNG into MAKEFUN_OUTPUT_DIR so the grader
can read it, after verifying the PNG header. It never writes ./entry.png.
"""
import hashlib
import os
import shutil
import struct
import sys

ENTRY = "entry.png"
EXPECTED_W, EXPECTED_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _png_size(path):
    """Return (width, height) from the PNG IHDR chunk, or raise."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk: %s" % path)
    return struct.unpack(">II", head[16:24])


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _output_dir():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not out.strip():
        out = "/output"
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    if not os.path.isfile(src):
        print("missing %s next to main.py" % ENTRY, file=sys.stderr)
        return 1
    w, h = _png_size(src)
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        print("entry.png is %dx%d, expected %dx%d"
              % (w, h, EXPECTED_W, EXPECTED_H), file=sys.stderr)
        return 1
    out_dir = _output_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, ENTRY)
    if os.path.abspath(src) == os.path.abspath(dst):
        print("entry.png already in output dir; nothing to copy")
        return 0
    try:
        if os.path.samefile(src, dst):
            print("entry.png already in output dir (same file); nothing to copy")
            return 0
    except OSError:
        pass  # dst does not exist yet; copy below
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch: %s != %s" % (dst, src), file=sys.stderr)
        return 1
    if _sha256(dst) != _sha256(src):
        print("copy mismatch: %s != %s" % (dst, src), file=sys.stderr)
        return 1
    print("wrote %s (%dx%d, sha256 %s)"
          % (dst, w, h, _sha256(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
