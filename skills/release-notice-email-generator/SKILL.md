---
name: release-notice-email-generator
description: Generate and refine structured Chinese release announcement emails, version update notices,上线通知, and feature release mails from version info, change lists, screenshot file paths, screenshot directory paths, and template assets. Use when Codex needs to draft, rewrite, standardize, or output 发版通知邮件 based on release notes, update tables, product links, screenshot walkthroughs, screenshot directories, or existing release email examples. This skill should also trigger when the user only provides version information plus local screenshot file paths or a local screenshot directory and expects Codex to infer modules, features, detailed sections, and update tables from the screenshots.
---

# Release Notice Email Generator

## Overview

Generate Chinese release-notice emails that match the bundled PDF template's structure and tone.
Use the template asset as a formatting anchor, the references for field mapping, and the script for deterministic Markdown output when the user wants a reusable file.

## Workflow

### 1. Collect the release package

Require enough information to identify the release:

- `version`
- one of:
  - `topic` or main module name
  - screenshot file paths that make the topic inferable
  - a screenshot directory that makes the topic inferable
- one of:
  - `product_url`
  - a screenshot that visibly includes the product domain or entry name
  - a screenshot directory whose images visibly include the product domain or entry name
- one of:
  - at least one release item in the update table
  - screenshots that are sufficient to infer release items
  - a screenshot directory that is sufficient to infer release items

Prefer these additional inputs when available:

- `product_name`
- `release_date`
- `recipients`
- screenshots or a screenshot directory
- feature-by-feature detail notes
- an existing release note, PRD, or changelog

Read [references/input-schema.md](references/input-schema.md) when the source material is unstructured.

If the user provides screenshot file paths plus `version`, inspect the screenshots directly before asking for more text input.

If the user provides a screenshot directory, expand it into ordered image paths before analysis. Use `scripts/collect_screenshot_paths.py` when deterministic directory scanning is helpful.

If no usable screenshots are found in the provided directory, stop and ask for a valid directory path or direct screenshot file paths.

Ask for key information before drafting whenever any of these are still missing after inspection:

- `topic + version`
- source screenshots, preferably a screenshot directory

Keep the follow-up concise and use the fixed sentence below instead of dynamic field lists.

Use a fixed single-sentence Chinese follow-up template. Do not explain the reason unless the user asks.

Use exactly this sentence:

- `请补充主题+版本号 / 截图目录。`

Do not ask for `产品地址`, `更新项`, `截图文件地址`, or other fields in the follow-up. Infer or omit them later if unavailable.

### 2. Normalize the source material

- When screenshot paths are provided, inspect them in path order unless the filenames imply a user flow.
- When a screenshot directory is provided, collect image files first, sort them naturally, then inspect them in that order unless subfolders or filenames imply a clearer workflow.
- Extract visible module names, menu paths, page titles, button labels, and capability names from the screenshots.
- Infer the release `topic` from the most repeated or most prominent capability label.
- Group screenshots that belong to the same workflow into one detailed section.
- Preserve exact product names, URLs, module names, and version strings.
- Deduplicate repeated release items.
- Merge tiny changes into a stable feature group when the raw notes are too granular.
- Convert informal notes into the update table columns `序号 | 模块 | 类型 | 功能 | 说明`.
- Use `新增`, `优化`, or `修复` unless the user requires a different taxonomy.
- When a screenshot clearly shows a new menu, form, table, or rule configuration page, prefer `新增`.
- When inference confidence is low, choose conservative wording and explicitly say the content was inferred from screenshots instead of inventing precise implementation details.

Read [references/template-structure.md](references/template-structure.md) before drafting if the request explicitly mentions the bundled template or provides screenshots from earlier release emails.

### 3. Draft the email

- Use the subject format `【发版通知】【<version>】<topic>`.
- Open with a short release summary, usually one sentence.
- Add a `产品地址` line and a standalone version line near the top.
- Render the update scope as a five-column table.
- Expand major items into numbered Chinese sections such as `一、功能入口`, `二、规则配置`.
- Place screenshots after the paragraph they support.
- Keep the tone factual and release-oriented rather than promotional.

### 4. Choose the output mode

- Reply inline with the finished email body by default.
- Generate a reusable Markdown file when the user asks for a file artifact or repeatable rendering.
- Run `scripts/render_release_notice_email.py` when the source data is already structured or when deterministic output is more important than prose flexibility.
- Draft in Markdown first even if the final destination is HTML email, then convert carefully without changing wording or table content.

### 5. Validate before sending

- Check that the subject, body, and table all use the same version and topic.
- Ensure every detailed section maps to at least one update-table row.
- Avoid inventing recipients, release timestamps, screenshots, or product URLs.
- If only screenshots and version were provided, allow inferred module and feature names, but do not fabricate backend logic or unsupported claims.
- If only a screenshot directory and version were provided, apply the same inference rule after expanding the directory into image paths.
- Omit mail-client reply headers unless the user explicitly wants them reproduced.
- When a follow-up is required, output only `请补充主题+版本号 / 截图目录。`

## Resources

- `assets/release-notice-template.pdf`: original release-email template provided by the user.
- [references/template-structure.md](references/template-structure.md): extracted structure, phrasing conventions, and field mapping rules from the template.
- [references/input-schema.md](references/input-schema.md): required and optional fields plus YAML and JSON examples for structured input.
- `scripts/collect_screenshot_paths.py`: collect and naturally sort image files from a screenshot directory.
- `scripts/render_release_notice_email.py`: render a Markdown release-notice email from YAML or JSON.

## Output Rules

- Write in Simplified Chinese unless the user requests another language.
- Keep terminology consistent across subject, table, and detail sections.
- Prefer concise business writing over marketing copy.
- Use screenshots only when they add value; omit them in chat output if the user did not provide any.
- Every output image in inline, Markdown, or HTML-style email content must be embedded as a base64 data URI, for example `![规则配置页面](data:image/png;base64,...)`. Do not output local file paths, relative paths, remote URLs, or `file://` links for images. The user must be able to `Ctrl+A` copy the rendered email and paste it into a document with images preserved.
- Use `[待补截图]` only in draft files that are clearly incomplete.

## Example Requests

- `用这个版本说明生成发版通知邮件，主题是网络ACL，版本 hulk.2602.01。`
- `把下面的更新列表整理成标准发版通知邮件，并按模板生成更新范围表格。`
- `根据 release notes 和截图，输出一封可以直接发送的中文发版通知邮件。`
- `我只给你版本号和几张功能截图，帮我自动补全一封发版通知邮件。`
- `我给你一个截图目录和版本号，自动批量读取目录里的截图并生成发版通知邮件。`
