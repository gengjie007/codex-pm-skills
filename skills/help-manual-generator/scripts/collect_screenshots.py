#!/usr/bin/env python3
"""Inventory product screenshots for help-manual generation."""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
}


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def image_size(path: Path) -> tuple[int | None, int | None]:
    try:
        with path.open("rb") as fh:
            head = fh.read(32)
            if head.startswith(b"\x89PNG\r\n\x1a\n"):
                width, height = struct.unpack(">II", head[16:24])
                return width, height
            if head[:6] in (b"GIF87a", b"GIF89a"):
                width, height = struct.unpack("<HH", head[6:10])
                return width, height
            if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
                return None, None
            if head.startswith(b"\xff\xd8"):
                fh.seek(2)
                while True:
                    marker_start = fh.read(1)
                    if not marker_start:
                        break
                    if marker_start != b"\xff":
                        continue
                    marker = fh.read(1)
                    while marker == b"\xff":
                        marker = fh.read(1)
                    if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
                        fh.read(3)
                        height, width = struct.unpack(">HH", fh.read(4))
                        return width, height
                    segment_size_bytes = fh.read(2)
                    if len(segment_size_bytes) != 2:
                        break
                    segment_size = struct.unpack(">H", segment_size_bytes)[0]
                    fh.seek(segment_size - 2, 1)
    except OSError:
        return None, None
    return None, None


def collect(directory: Path) -> list[dict[str, object]]:
    files = [
        item
        for item in directory.rglob("*")
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    screenshots = []
    for index, path in enumerate(sorted(files, key=natural_key), start=1):
        width, height = image_size(path)
        screenshots.append(
            {
                "index": index,
                "path": str(path),
                "relative_path": str(path.relative_to(directory)),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "width": width,
                "height": height,
            }
        )
    return screenshots


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory screenshots in a directory.")
    parser.add_argument("screenshot_dir", help="Directory containing product screenshots")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of a Markdown table")
    args = parser.parse_args()

    screenshot_dir = Path(args.screenshot_dir).expanduser().resolve()
    if not screenshot_dir.exists():
        raise SystemExit(f"Screenshot directory does not exist: {screenshot_dir}")
    if not screenshot_dir.is_dir():
        raise SystemExit(f"Not a directory: {screenshot_dir}")

    screenshots = collect(screenshot_dir)
    if args.json:
        print(json.dumps({"screenshot_dir": str(screenshot_dir), "count": len(screenshots), "screenshots": screenshots}, ensure_ascii=False, indent=2))
        return 0

    print(f"# Screenshot Inventory\n\nDirectory: `{screenshot_dir}`\n\nCount: {len(screenshots)}\n")
    if not screenshots:
        return 0
    print("| # | File | Size | Dimensions |")
    print("| --- | --- | ---: | --- |")
    for item in screenshots:
        dimensions = (
            f"{item['width']}x{item['height']}"
            if item["width"] and item["height"]
            else "unknown"
        )
        print(f"| {item['index']} | `{item['relative_path']}` | {item['size_bytes']} | {dimensions} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
