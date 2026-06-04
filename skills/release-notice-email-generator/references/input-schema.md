# Input Schema

Use this reference when the request includes scattered notes, changelog text, screenshots, or a partially structured release brief.

## Supported Input Modes

### Mode A: Standard structured mode

- `version`: release version shown in the subject and body
- `topic`: main theme or module name shown in the subject
- `product_url`: URL exposed in the email body
- `change_items`: array with at least one row

### Mode B: Screenshot-first mode

- `version`: release version shown in the subject and body
- `screenshot_paths`: non-empty array of absolute local image paths

In screenshot-first mode, infer these fields from screenshots whenever possible:

- `topic`
- `change_items`
- `sections`
- `product_name`
- `product_url` only if a visible domain or URL appears in the screenshots

### Mode C: Screenshot-directory mode

- `version`: release version shown in the subject and body
- `screenshot_dir`: absolute local directory path containing screenshots

In screenshot-directory mode:

- expand the directory into ordered image paths first
- ignore non-image files
- infer `topic`, `change_items`, `sections`, and `product_name` from the collected screenshots
- infer `product_url` only if a visible domain or URL appears in the screenshots

## Optional Fields

- `subject_tag`: default `发版通知`
- `product_name`: default `产品平台`
- `intro`: short summary sentence shown at the top
- `recipients`: array of recipient labels or email addresses
- `release_date`: date or timestamp string
- `screenshot_paths`: array of absolute local image paths
- `screenshot_dir`: absolute local directory path
- `sections`: detailed sections shown after the table

## `change_items` Shape

Each item should contain:

- `module`
- `type`
- `feature`
- `description`

## `sections` Shape

Each section may contain:

- `title`
- `body`
- `images`: array of image paths or objects with `path` and optional `caption`

## Screenshot Inference Rules

- Read screenshots in the given order unless filenames indicate a clearer workflow.
- If a directory is provided, sort filenames naturally before reading.
- Use visible page titles, menu labels, button labels, tabs, and table headers to infer `module`, `feature`, and section titles.
- Infer `description` from the user-visible result, such as `支持创建、删除、编辑 ACL`, not from guessed implementation details.
- Group adjacent screenshots into one section when they describe the same action path.
- If no visible URL exists, keep `product_url` unresolved and ask once instead of inventing it.
- If the topic is still ambiguous, choose the most prominent repeated capability name and note that it was inferred from screenshots.
- If the directory contains no usable images, ask the user for a correct directory path or explicit screenshot paths.

## Missing-Key-Info Rule

Before drafting the email, ask the user for the minimum missing inputs using one fixed sentence.

Required minimum package:

- `topic + version`
- `screenshot_dir`

Do not ask for `product_url`, `change_items`, or other fields in the follow-up.

## Fixed Follow-Up Template

When key information is missing, ask in exactly one Chinese sentence:

`请补充主题+版本号 / 截图目录。`

## YAML Example

```yaml
version: "hulk.2602.01"
topic: "网络ACL"
product_name: "智汇云平台"
product_url: "https://hulk.qihoo.net/"
intro: "智汇云平台，新功能发布"
change_items:
  - module: "VPC"
    type: "新增"
    feature: "网络ACL能力"
    description: "支持子网级访问控制"
  - module: "网络ACL"
    type: "新增"
    feature: "ACL创建与管理"
    description: "支持创建、删除、编辑 ACL"
sections:
  - title: "网络ACL功能入口"
    body: "在云网络的专有网络 VPC 中新增 ACL 管理能力，可创建和管理网络访问控制策略。"
    images:
      - path: "/absolute/path/to/acl-entry.png"
        caption: "网络ACL菜单入口"
```

## YAML Example: Screenshot-First

```yaml
version: "hulk.2602.01"
screenshot_paths:
  - "/absolute/path/to/01-menu.png"
  - "/absolute/path/to/02-create-acl.png"
  - "/absolute/path/to/03-rule-config.png"
```

## YAML Example: Screenshot Directory

```yaml
version: "hulk.2602.01"
screenshot_dir: "/absolute/path/to/release-screenshots"
```

## JSON Example

```json
{
  "version": "hulk.2602.01",
  "topic": "网络ACL",
  "product_name": "智汇云平台",
  "product_url": "https://hulk.qihoo.net/",
  "change_items": [
    {
      "module": "VPC",
      "type": "新增",
      "feature": "网络ACL能力",
      "description": "支持子网级访问控制"
    }
  ]
}
```

## Rendering Notes

- Keep `version` and `topic` stable across every section.
- Use absolute local image paths as structured input; render output images as base64 data URIs so copied Markdown/email content preserves images when pasted into a document.
- Omit `sections` if the email only needs a summary and table.
- In screenshot-first mode, infer content first, then convert it into the standard table and section structure.
- In screenshot-directory mode, collect image paths first, then follow the same inference flow as screenshot-first mode.
