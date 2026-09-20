# codex-pm-skills

面向中文产品、文档和发版协作场景的 Codex skills 集合。

本仓库用于分享可直接安装到 Codex 的本地 skill，适合产品经理、技术写作、研发协作和发布管理流程。

## Included Skills

| Skill | 用途 | 安装路径 |
| --- | --- | --- |
| `prd-product-manager` | 根据原型截图、HTML 页面、UI 设计稿或简单描述，生成标准中文 PRD。 | `skills/prd-product-manager` |
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
