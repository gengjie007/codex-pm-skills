#!/usr/bin/env python3
"""Validate that a generated help manual includes screenshots."""

from __future__ import annotations

import argparse
import posixpath
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse


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

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def is_url(target: str) -> bool:
    parsed = urlparse(target)
    return parsed.scheme in {"http", "https", "data"}


def is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def screenshot_names(screenshot_dir: Path) -> set[str]:
    return {
        item.name
        for item in screenshot_dir.rglob("*")
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
    }


def validate_markdown(manual: Path, screenshot_dir: Path) -> list[str]:
    errors: list[str] = []
    text = manual.read_text(encoding="utf-8")
    refs = [match.strip().split()[0].strip("<>\"'") for match in IMAGE_RE.findall(text)]
    if not refs:
        return ["Markdown manual contains no image references."]

    names = screenshot_names(screenshot_dir)
    local_refs = []
    matched_screenshots = []
    for ref in refs:
        if is_url(ref):
            continue
        decoded = unquote(ref)
        if decoded.startswith("file://"):
            decoded = urlparse(decoded).path
        candidate = Path(decoded)
        if not candidate.is_absolute():
            candidate = (manual.parent / decoded).resolve()
        local_refs.append(candidate)
        normalized_parts = [part for part in Path(decoded).parts if part not in {".", ""}]
        if candidate.exists() and (is_relative_to(candidate, screenshot_dir) or candidate.name in names):
            matched_screenshots.append(candidate)
        elif posixpath.basename(decoded) in names:
            matched_screenshots.append(candidate)

    if not local_refs:
        errors.append("Markdown manual only contains remote/data images; use local screenshots from the provided directory.")
    missing = [str(path) for path in local_refs if not path.exists()]
    if missing:
        errors.append("Missing local image files: " + ", ".join(missing[:10]))
    if not matched_screenshots:
        errors.append("No image reference appears to come from the provided screenshot directory.")
    return errors


def validate_docx(manual: Path) -> list[str]:
    if not zipfile.is_zipfile(manual):
        return ["Word output is not a valid .docx file."]
    with zipfile.ZipFile(manual) as archive:
        media = [
            name
            for name in archive.namelist()
            if name.startswith("word/media/") and Path(name).suffix.lower() in SUPPORTED_EXTENSIONS
        ]
    if not media:
        return ["DOCX manual contains no embedded images under word/media/."]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a help manual generated from product screenshots.")
    parser.add_argument("manual_path", help="Generated .md or .docx manual")
    parser.add_argument("--screenshot-dir", required=True, help="Original screenshot directory")
    args = parser.parse_args()

    manual = Path(args.manual_path).expanduser().resolve()
    screenshot_dir = Path(args.screenshot_dir).expanduser().resolve()
    if not manual.exists():
        raise SystemExit(f"Manual does not exist: {manual}")
    if not screenshot_dir.exists() or not screenshot_dir.is_dir():
        raise SystemExit(f"Screenshot directory does not exist or is not a directory: {screenshot_dir}")

    suffix = manual.suffix.lower()
    if suffix == ".md":
        errors = validate_markdown(manual, screenshot_dir)
    elif suffix == ".docx":
        errors = validate_docx(manual)
    else:
        errors = [f"Unsupported manual format: {suffix}. Expected .md or .docx."]

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: manual includes screenshots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
