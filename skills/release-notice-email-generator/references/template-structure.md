# Template Structure

Use this reference when matching the bundled asset `assets/release-notice-template.pdf`.

## Canonical Outline

1. Subject line: `【发版通知】【版本号】主题`
2. Short intro paragraph:
   - announce the release in one sentence
   - keep the product or platform name near the start
3. Top metadata block inside the body:
   - `产品地址：<URL>`
   - standalone version line such as `hulk.2602.01`
4. `更新范围` table:
   - `序号`
   - `模块`
   - `类型`
   - `功能`
   - `说明`
5. Detailed walkthrough sections:
   - use numbered Chinese headings such as `一、网络ACL功能入口`
   - explain the entry point, value, or key operation in 1 to 3 short paragraphs
   - place screenshots after the related explanation

## Template Signals Taken from the User Asset

- The sample subject uses full-width brackets and embeds the version in the middle.
- The body starts with a short release sentence instead of a long background section.
- The update table mixes multiple modules but keeps one visible capability per row.
- Detailed sections appear below the table and use screenshot-driven walkthroughs.

## Writing Rules

- Keep the subject, intro, table, and detailed headings semantically aligned.
- Prefer concrete capability names over vague labels.
- Use `新增`, `优化`, and `修复` consistently in the `类型` column.
- Write `说明` as the user-facing outcome, not as an implementation detail.
- Keep feature details factual and short; let screenshots carry the visual explanation.

## Screenshot Handling

- Keep screenshots in the same order as the user flow.
- Put screenshots immediately after the paragraph they support.
- Add a short caption only when the screenshot needs context.
- Omit screenshots entirely if none are provided and the user only asked for email text.

## Mapping Raw Notes into the Template

- Map product area to `模块`.
- Map change category to `类型`.
- Map visible capability name to `功能`.
- Map benefit or supported action to `说明`.
- Promote only the most important items into detailed numbered sections.

## Mapping Screenshots into the Template

- Map the breadcrumb, left navigation, or page title to `模块`.
- Map the main button, tab, or page capability to `功能`.
- Map the observable user outcome to `说明`.
- Use one section for one coherent workflow, not one section per screenshot.
- If a screenshot sequence shows entry, creation, and configuration, keep them under one section with multiple embedded images.
- If screenshots come from a directory, keep adjacent files with the same workflow prefix or numeric sequence in one section.
