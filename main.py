"""news-23 b17 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
which the grader points outside the repo.
"""
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    out_dir = os.path.abspath(out_dir)
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    if out_dir == repo_dir or out_dir.startswith(repo_dir + os.sep):
        raise ValueError("MAKEFUN_OUTPUT_DIR must point outside the repo")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        raise ValueError("entry.png exceeds 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG")
    w, h = struct.unpack(">II", data[16:24])
    if (w, h) != (1024, 1024):
        raise ValueError("entry.png must be 1024x1024, got %dx%d" % (w, h))
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise ValueError("entry.png is truncated (missing IEND trailer)")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print("wrote", dst, len(data), "bytes")


if __name__ == "__main__":
    sys.exit(main())
