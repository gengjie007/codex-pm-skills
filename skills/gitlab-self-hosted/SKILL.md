---
name: gitlab-self-hosted
description: Connect to and operate a user-owned self-hosted GitLab instance through its REST API. Use for projects, repositories, branches, commits, issues, merge requests, pipelines, jobs, and related GitLab administration; do not use for GitHub or GitLab.com unless the user explicitly configures that host.
---

# Self-hosted GitLab

Use `scripts/gitlab_api.py` as the authenticated GitLab REST API client. It reads connection details from the environment and never stores credentials.

## Connection

Require these environment variables in the shell running Codex:

```bash
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="..."
```

`GITLAB_TOKEN` may be a personal, project, or group access token. Use the narrowest scopes suitable for the request. For a private CA, set `GITLAB_CA_BUNDLE` to its PEM file. Do not disable TLS verification.

Before substantive work, verify the target instance and identity:

```bash
python3 scripts/gitlab_api.py GET /user
python3 scripts/gitlab_api.py GET /version
```

If configuration is absent, tell the user which variables are missing. Never ask them to paste a token into chat, print it, write it into files, or place it in command arguments.

## Workflow

1. Resolve names to numeric IDs with read-only requests. Project paths used in API URLs must be URL-encoded; `scripts/gitlab_api.py project-id 'group/project'` returns the ID.
2. Read current state before proposing or applying a change. Use `--paginate` for list endpoints when completeness matters.
3. For requested mutations, use the smallest applicable endpoint and preserve existing fields not being changed.
4. Re-read the affected object and report its web URL or stable identifier after a successful mutation.

The user's request authorizes ordinary mutations directly necessary for that request, such as creating an issue or retrying a named job. Obtain explicit confirmation immediately before destructive or hard-to-reverse actions: deleting projects/groups/branches/tags, force-updating refs, canceling broad sets of pipelines, changing visibility or membership, rotating/revoking credentials, or triggering production deployments. Resolve and display the exact targets first.

Do not retry mutations automatically after an ambiguous timeout; first check whether the server already applied them. Never expose token-bearing headers or URLs in output.

## API use

Examples:

```bash
python3 scripts/gitlab_api.py GET /projects/42/issues --query state=opened --paginate
python3 scripts/gitlab_api.py POST /projects/42/issues --field title='Bug title' --field description='Details'
python3 scripts/gitlab_api.py PUT /projects/42/merge_requests/7 --field add_labels=reviewed
```

Read [references/api-guide.md](references/api-guide.md) when selecting endpoints, permissions, pagination, repository file operations, or CI/CD actions. Prefer GitLab's instance-matched API documentation when an endpoint or field may differ by version.
