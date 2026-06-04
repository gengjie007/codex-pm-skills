#!/usr/bin/env python3
"""Render a Markdown release-notice email from YAML or JSON input."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml


CHINESE_NUMERALS = "零一二三四五六七八九十"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Markdown release-notice email from YAML or JSON input.",
    )
    parser.add_argument("input_path", help="Path to a YAML or JSON data file")
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output path for the generated Markdown file",
    )
    return parser.parse_args()


def load_payload(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
    else:
        data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("Input payload must be a mapping/object at the top level.")
    return data


def require_fields(data: dict[str, Any], fields: list[str]) -> None:
    missing = [field for field in fields if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")


def sanitize(value: Any) -> str:
    return str(value).replace("|", "\\|").strip()


def image_to_data_uri(path_value: str) -> str:
    if path_value.startswith("data:image/"):
        return path_value
    path = Path(path_value).expanduser()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image file does not exist: {path_value}")
    mime_type = mimetypes.types_map.get(path.suffix.lower(), "application/octet-stream")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def to_chinese_number(number: int) -> str:
    if number <= 10:
        return CHINESE_NUMERALS[number]
    if number < 20:
        return "十" + CHINESE_NUMERALS[number - 10]
    tens, ones = divmod(number, 10)
    result = CHINESE_NUMERALS[tens] + "十"
    if ones:
        result += CHINESE_NUMERALS[ones]
    return result


def subject_line(data: dict[str, Any]) -> str:
    tag = data.get("subject_tag", "发版通知")
    return f"【{tag}】【{data['version']}】{data['topic']}"


def build_sections(data: dict[str, Any]) -> list[dict[str, Any]]:
    sections = data.get("sections")
    if isinstance(sections, list) and sections:
        return sections

    grouped: "OrderedDict[str, list[dict[str, Any]]]" = OrderedDict()
    for item in data["change_items"]:
        module = str(item.get("module") or data["topic"]).strip() or data["topic"]
        grouped.setdefault(module, []).append(item)

    generated = []
    for module, items in grouped.items():
        lines = []
        for item in items:
            feature = str(item.get("feature", "")).strip()
            description = str(item.get("description", "")).strip()
            if feature and description:
                lines.append(f"- {feature}：{description}")
            elif feature:
                lines.append(f"- {feature}")
        body = "\n".join(lines) if lines else "待补充详细说明。"
        generated.append({"title": module, "body": body, "images": []})
    return generated


def render_metadata(data: dict[str, Any]) -> list[str]:
    lines = [f"主题：{subject_line(data)}"]
    recipients = data.get("recipients")
    if isinstance(recipients, list) and recipients:
        lines.append("收件人：" + "；".join(str(item).strip() for item in recipients if str(item).strip()))
    elif isinstance(recipients, str) and recipients.strip():
        lines.append(f"收件人：{recipients.strip()}")
    release_date = str(data.get("release_date", "")).strip()
    if release_date:
        lines.append(f"时间：{release_date}")
    return lines


def render_table(change_items: list[dict[str, Any]]) -> list[str]:
    lines = [
        "更新范围：",
        "",
        "| 序号 | 模块 | 类型 | 功能 | 说明 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for index, item in enumerate(change_items, start=1):
        row = [
            str(index),
            sanitize(item.get("module", "")),
            sanitize(item.get("type", "")),
            sanitize(item.get("feature", "")),
            sanitize(item.get("description", "")),
        ]
        lines.append("| " + " | ".join(row) + " |")
    return lines


def render_sections(sections: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = ["---", ""]
    for index, section in enumerate(sections, start=1):
        title = str(section.get("title", f"第{index}部分")).strip()
        body = str(section.get("body", "")).strip()
        heading = f"{to_chinese_number(index)}、{title}"
        lines.append(heading)
        lines.append("")
        lines.append(body or "待补充详细说明。")
        lines.append("")
        for image in section.get("images", []) or []:
            if isinstance(image, dict):
                path = str(image.get("path", "")).strip()
                caption = str(image.get("caption", "")).strip()
            else:
                path = str(image).strip()
                caption = ""
            if not path:
                continue
            alt = caption or title
            lines.append(f"![{alt}]({image_to_data_uri(path)})")
            if caption:
                lines.append("")
                lines.append(caption)
            lines.append("")
    return lines


def render_markdown(data: dict[str, Any]) -> str:
    require_fields(data, ["version", "topic", "product_url"])
    change_items = data.get("change_items")
    if not isinstance(change_items, list) or not change_items:
        raise ValueError("`change_items` must be a non-empty array.")

    product_name = str(data.get("product_name", "产品平台")).strip() or "产品平台"
    intro = str(data.get("intro", "")).strip() or f"{product_name}，新功能发布"

    lines: list[str] = []
    lines.extend(render_metadata(data))
    lines.extend(["", intro, "", f"产品地址： {data['product_url']}", "", str(data["version"]), ""])
    lines.extend(render_table(change_items))
    lines.extend([""])
    lines.extend(render_sections(build_sections(data)))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    payload = load_payload(Path(args.input_path))
    rendered = render_markdown(payload)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(rendered, encoding="utf-8")
        print(output_path)
        return

    print(rendered, end="")


if __name__ == "__main__":
    main()
