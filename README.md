# codex-pm-skills

面向中文产品、文档和发版协作场景的 Codex skills 集合。

本仓库用于分享可直接安装到 Codex 的本地 skill，适合产品经理、技术写作、研发协作和发布管理流程。

## Included Skills

| Skill | 用途 | 安装路径 |
| --- | --- | --- |
| `prd-product-manager` | 根据原型截图、HTML 页面、UI 设计稿或简单描述，生成标准中文 PRD。 | `skills/prd-product-manager` |
| `release-notice-email-generator` | 根据版本号、更新列表、产品链接和截图，生成中文发版通知邮件。 | `skills/release-notice-email-generator` |
| `help-manual-generator` | 根据产品截图目录生成中文帮助手册、产品手册、操作指南或知识库文档。 | `skills/help-manual-generator` |

## Install With Codex

在 Codex 中让它从 GitHub 安装对应 skill。例如：

```text
请从这个 GitHub 地址安装 Codex skill：
https://github.com/gengjie007/codex-pm-skills/tree/main/skills/prd-product-manager
```

也可以分别安装：

```text
请从这个 GitHub 地址安装 Codex skill：
https://github.com/gengjie007/codex-pm-skills/tree/main/skills/release-notice-email-generator
```

```text
请从这个 GitHub 地址安装 Codex skill：
https://github.com/gengjie007/codex-pm-skills/tree/main/skills/help-manual-generator
```

安装完成后，重启 Codex 才能在新会话中加载这些 skills。

## Manual Install

如果要手动安装，复制单个 skill 目录到本机 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/gengjie007/codex-pm-skills.git /tmp/codex-pm-skills
cp -R /tmp/codex-pm-skills/skills/prd-product-manager ~/.codex/skills/prd-product-manager
cp -R /tmp/codex-pm-skills/skills/release-notice-email-generator ~/.codex/skills/release-notice-email-generator
cp -R /tmp/codex-pm-skills/skills/help-manual-generator ~/.codex/skills/help-manual-generator
```

如果只需要其中一个 skill，只复制对应目录即可。

## First Release Notes

### v1.0.1

更新 3 个 skills 的强制输出格式要求：

- 禁止在输出图片中使用本地路径、相对路径、远程 URL 或 `file://` 链接。
- 目标是让用户可以 `Ctrl+A` 复制渲染内容并粘贴到文档中，同时保留图片。

### v1.0.0

首版包含 3 个 Codex skills：

- `prd-product-manager`：把截图、原型或简单需求描述整理成结构化 PRD，默认中文输出，适合 Web 产品、SaaS 和内部平台。
- `release-notice-email-generator`：把版本信息、更新项和截图整理成标准中文发版通知邮件，支持从截图目录推断模块和功能点。
- `help-manual-generator`：根据产品截图目录生成中文帮助手册，支持 Markdown 和 Word 输出，并要求最终文档包含截图证据。

安装路径均位于 `skills/<skill-name>`。朋友安装后需要重启 Codex，才能在新会话中触发这些 skills。

## License

No license file is provided. All rights are reserved by default unless the repository owner adds a license later.
