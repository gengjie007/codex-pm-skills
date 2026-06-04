#!/usr/bin/env python3
"""Validate that a generated help manual includes screenshots."""

from __future__ import annotations

import argparse
import base64
import binascii
import re
import zipfile
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

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def validate_data_image(target: str) -> str | None:
    if not target.startswith("data:image/"):
        return "Markdown image is not a base64 data URI: " + target[:80]
    header, separator, payload = target.partition(",")
    if not separator or ";base64" not in header:
        return "Markdown data image is missing a base64 payload: " + target[:80]
    try:
        base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError):
        return "Markdown data image contains invalid base64: " + target[:80]
    return None


def validate_markdown(manual: Path, _screenshot_dir: Path) -> list[str]:
    errors: list[str] = []
    text = manual.read_text(encoding="utf-8")
    refs = [match.strip().split()[0].strip("<>\"'") for match in IMAGE_RE.findall(text)]
    if not refs:
        return ["Markdown manual contains no image references."]

    data_refs = []
    non_data_refs = []
    for ref in refs:
        if ref.startswith("data:"):
            data_refs.append(ref)
            error = validate_data_image(ref)
            if error:
                errors.append(error)
            continue
        non_data_refs.append(ref)

    if not data_refs:
        errors.append("Markdown manual contains no base64 data URI images.")
    if non_data_refs:
        errors.append("Markdown manual image references must be base64 data URIs, not paths or URLs: " + ", ".join(non_data_refs[:10]))
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
