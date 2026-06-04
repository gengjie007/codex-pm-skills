---
name: help-manual-generator
description: 帮助手册生成器。用于根据用户提供的产品截图目录生成中文产品帮助手册、产品手册、操作指南、使用说明或知识库文档；当用户要求生成帮助手册、产品文档、Markdown 手册或 Word 手册时使用。必须要求对话中提供产品截图目录；默认输出 .md，用户要求 Word/.doc/.docx 时输出 .docx；最终文档必须包含截图目录中的截图。
---

# 帮助手册生成器

## 强制要求

- Require a product screenshot directory from the current conversation. If no directory is provided, stop and ask for the directory before drafting or creating files.
- Use screenshots from that directory in the final manual. If no supported images are found, stop and report that the screenshot directory is empty or unsupported.
- Default output to `帮助手册.md` unless the user requests Word output. For Word requests, create `.docx` even if the user says `.doc`.
- Do not invent pricing, limits, product architecture, or feature capabilities that are not visible in screenshots or provided by the user. Mark missing business details as `待补充` only when the section is needed.
- Keep image paths working. For Markdown output, copy or reference images with relative paths from the manual file. For `.docx`, embed the actual image files.

## 资源

- Use `assets/help-manual-template.md` as the style and structure reference. It shows the expected Chinese cloud-product manual pattern: product overview, advantages, functions, scenarios, quick start, operation guides, numbered steps, tables, separators, and screenshots.
- Use `assets/help-manual-template.docx` only as a visual reference when Word output is requested; do not overwrite it.
- Run `scripts/collect_screenshots.py <screenshot-dir>` to inventory supported screenshot files before writing.
- Run `scripts/validate_manual.py <manual-path> --screenshot-dir <screenshot-dir>` before final delivery.

## 工作流

1. Confirm the screenshot directory exists and is a directory.
2. Run the screenshot inventory script:

```bash
python3 /path/to/help-manual-generator/scripts/collect_screenshots.py "/path/to/screenshots"
```

3. Inspect the screenshots. Prefer natural filename order first, then visual UI order. Use file names, visible page titles, breadcrumbs, forms, table headers, buttons, dialogs, and empty states to infer flows.
4. Decide the manual structure from the evidence:
   - Use `# 产品简介` when the screenshots or user input establish the product name and purpose.
   - Use `# 快速入门` for the shortest end-to-end path a new user should follow.
   - Use `# 操作指南` for task-based procedures such as create, edit, bind, enable, disable, view details, monitor, delete, import, export, or configure.
   - Add `# 常见问题` only when screenshots or user notes reveal errors, constraints, or confusing states.
   - Add `# 产品计费` only when pricing or billing details are provided by the user or visible in screenshots.
5. Write concise Chinese documentation in the template's style:
   - Start each operation section with a one-sentence purpose.
   - Use numbered steps for flows.
   - Put the screenshot immediately after the step it illustrates.
   - Use bullets for field explanations and tables for structured limits or parameter definitions.
   - Use exact visible UI labels when possible, wrapped with Chinese corner quotes or bold text, for example `点击「创建」` or `点击 **确定**`.
6. Generate the requested output:
   - Markdown: create `帮助手册.md` unless the user provided a target path. Use relative image links such as `![创建实例页面](screenshots/create-instance.png)`.
   - Word: create `.docx` with embedded screenshots, captions, headings, numbered steps, and tables. If document tooling is available, use it; otherwise create Markdown first and convert to `.docx` with a reliable local converter.
7. Validate the output with:

```bash
python3 /path/to/help-manual-generator/scripts/validate_manual.py "/path/to/帮助手册.md" --screenshot-dir "/path/to/screenshots"
```

For `.docx`, pass the `.docx` path. Fix any validation failure before final response.

## 质量标准

- The manual must be useful without the screenshots directory open beside it.
- Every major workflow must include at least one screenshot.
- Screenshot captions or alt text must describe the UI state, not generic names like `image1`.
- Do not leave TODO placeholders except explicit `待补充` items for missing user-provided business facts.
- Preserve the user's product terminology. Do not translate product names or UI labels unless the user asks.
