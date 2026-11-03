# codex-pm-skills

面向中文产品、文档和发版协作场景的 Codex skills 集合。

本仓库用于分享可直接安装到 Codex 的本地 skill，适合产品经理、技术写作、研发协作和发布管理流程。

## Included Skills

| Skill | 用途 | 安装路径 |
| --- | --- | --- |
| `prd-product-manager` | 根据原型、截图和需求附件生成或修订产品需求规格，默认交付可离线打开的 `spec.html`。 | `skills/prd-product-manager` |
| `release-notice-email-generator` | 根据版本号、更新列表、产品链接和截图，生成中文发版通知邮件。 | `skills/release-notice-email-generator` |
| `help-manual-generator` | 根据产品截图目录生成中文帮助手册、产品手册、操作指南或知识库文档。 | `skills/help-manual-generator` |
| `gitlab-self-hosted` | 连接自托管 GitLab，管理项目、仓库、Issue、合并请求和 CI/CD。 | `skills/gitlab-self-hosted` |

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

## prd-product-manager：产品需求规格

根据原型 URL、HTML 或项目路径，由 Agent 操作并采集截图；也可直接提供粘贴或上传的截图、图片目录和需求附件。两种方式可混用。技能会梳理功能、规则、权限与验收，按需求 ID 建立截图和验收的对应关系，形成供研发拆解 `plan.md` 的规格。

默认交付单个中文 `spec.html`，图片内嵌，可离线打开，支持目录、打印、截图放大和窄屏阅读。用户可指定文件名、位置、语言或其他格式；修订现有规格时保留已确认内容。复制到其他编辑器后图片是否保留取决于目标编辑器。

使用示例：

```text
使用 $prd-product-manager，根据这个原型地址和需求附件生成产品需求规格，输出 spec.html。
```

```text
使用 $prd-product-manager，根据我上传的截图和说明修订现有规格；缺失的信息请标明。
```

技能通过 [章节规范](skills/prd-product-manager/references/prd-template.md)、[截图输入与核验规范](skills/prd-product-manager/references/screenshot-inputs.md)和 [HTML 模板](skills/prd-product-manager/assets/spec-template.html)组织内容，并使用 [校验脚本](skills/prd-product-manager/scripts/validate_spec.py)检查结构、锚点、图片内嵌和验收标识。脚本不能代替业务判断及浏览器视觉检查；关键素材不足时，结果应标为未完成草稿并说明缺口。

## 更新说明

### 2026-11-03：prd-product-manager

- 将默认交付更新为可离线打开、截图内嵌的单文件 HTML 产品需求规格，支持修订既有规格。
- 支持 Agent 操作原型截图及用户提供截图两种输入，补充截图匹配、缺失材料和事实来源的核验要求。
- 按功能建立需求 ID、截图、规则和可验证验收的对应关系，补充权限、状态和研发计划拆解要求。
- 新增 HTML 模板、截图规范及结构校验脚本，并更新技能展示名称和默认提示词。

## First Release Notes

### v1.0.1

以下为历史发布记录；`prd-product-manager` 的现行行为以上方更新说明和技能文件为准。

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


## gitlab-self-hosted：自托管 GitLab 协作

通过 GitLab REST API 连接用户自己的 GitLab 实例，适用于项目和仓库查询、分支与提交查看、Issue 管理、合并请求以及流水线和任务管理。该技能默认面向自托管 GitLab，不用于 GitHub；GitLab.com 需要用户明确配置。

### 安装

在 Codex 中输入：

```text
请从这个 GitHub 地址安装 Codex skill：
https://github.com/gengjie007/codex-pm-skills/tree/main/skills/gitlab-self-hosted
```

或在克隆本仓库后，手动复制：

```bash
cp -R /tmp/codex-pm-skills/skills/gitlab-self-hosted ~/.codex/skills/gitlab-self-hosted
```

### 连接配置

在运行 Codex 的环境中设置 `GITLAB_URL`（实例根地址，例如 `https://gitlab.example.com`）和 `GITLAB_TOKEN`（访问令牌）。如果实例使用私有 CA，可设置 `GITLAB_CA_BUNDLE` 指向 PEM 证书文件。

令牌应通过本机安全方式配置，不要粘贴到聊天、写入仓库或放入命令参数。脚本从环境变量读取凭据，不保存凭据，不关闭 TLS 校验。按任务使用最小必要权限：只读操作通常使用 `read_api`，写入操作通常需要 `api`，同时受项目角色和实例策略限制。

### 使用示例

```text
使用 $gitlab-self-hosted 查看我的自托管 GitLab 项目和最近提交。
```

```text
使用 $gitlab-self-hosted 查询指定项目中未关闭的 Issue，并整理优先处理清单。
```

```text
使用 $gitlab-self-hosted 检查指定项目最近失败的流水线和任务。
```

技能会先核验实例版本及当前身份，读取目标状态，再执行请求并复核结果。删除资源、强制更新引用、修改可见性或成员权限、轮换凭据及触发生产部署等高风险操作需要明确确认。

### 文件说明

- [SKILL.md](skills/gitlab-self-hosted/SKILL.md)：触发条件、连接方式和操作流程。
- [scripts/gitlab_api.py](skills/gitlab-self-hosted/scripts/gitlab_api.py)：基于 Python 3 标准库的 REST API 客户端，支持分页、JSON 请求和项目 ID 查询。
- [references/api-guide.md](skills/gitlab-self-hosted/references/api-guide.md)：常用接口、参数编码、分页及权限说明。
- [agents/openai.yaml](skills/gitlab-self-hosted/agents/openai.yaml)：Codex 展示名称和默认提示词。
