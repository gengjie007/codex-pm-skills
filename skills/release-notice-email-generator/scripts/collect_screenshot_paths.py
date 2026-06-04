#!/usr/bin/env python3
"""Collect and naturally sort screenshot paths from a directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect and naturally sort screenshot file paths from a directory.",
    )
    parser.add_argument("directory", help="Directory containing screenshots")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan subdirectories",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON array instead of newline-separated paths",
    )
    return parser.parse_args()


def natural_key(path: Path) -> list[object]:
    parts = re.split(r"(\d+)", path.name.lower())
    key: list[object] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)
    key.append(str(path.parent).lower())
    return key


def collect_paths(directory: Path, recursive: bool) -> list[Path]:
    iterator = directory.rglob("*") if recursive else directory.iterdir()
    files = [
        path.resolve()
        for path in iterator
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ]
    return sorted(files, key=natural_key)


def main() -> None:
    args = parse_args()
    directory = Path(args.directory).expanduser().resolve()
    if not directory.exists():
        raise SystemExit(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise SystemExit(f"Not a directory: {directory}")

    files = collect_paths(directory, recursive=args.recursive)

    if args.json:
        print(json.dumps([str(path) for path in files], ensure_ascii=False, indent=2))
        return

    for path in files:
        print(path)


if __name__ == "__main__":
    main()
