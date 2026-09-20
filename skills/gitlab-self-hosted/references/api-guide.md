# GitLab REST API guide

All paths below are relative to `/api/v4`, which the helper adds automatically.

## Common endpoints

- Identity/version: `GET /user`, `GET /version`
- Projects: `GET /projects`, `GET|PUT|DELETE /projects/:id`
- Project search: `GET /projects?search=term`
- Branches/tags: `/projects/:id/repository/branches`, `/projects/:id/repository/tags`
- Commits: `/projects/:id/repository/commits`
- Repository tree/files: `/projects/:id/repository/tree`, `/projects/:id/repository/files/:file_path`
- Issues: `/projects/:id/issues`, `/projects/:id/issues/:issue_iid`
- Merge requests: `/projects/:id/merge_requests`, `/projects/:id/merge_requests/:merge_request_iid`
- MR notes/discussions: append `/notes` or `/discussions` to an MR path
- Pipelines: `/projects/:id/pipelines`, `/projects/:id/pipelines/:pipeline_id`
- Jobs: `/projects/:id/jobs`, `/projects/:id/jobs/:job_id`
- Groups/members: `/groups`, `/groups/:id/members`, `/projects/:id/members`

Project-scoped issue and merge-request URLs use the project-local `iid`, not the global database `id`.

## Request encoding

Use `--query key=value` for URL query parameters and `--field key=value` for JSON bodies. Repeating a field creates a JSON array. Values are strings unless prefixed with `json:`, for example `--field assignee_ids='json:[12,34]'` or `--field remove_source_branch=json:true`.

Repository file paths and namespace/project paths embedded in a URL segment must be percent-encoded. Prefer numeric project IDs after resolving them with the helper's `project-id` command.

For full JSON control, pass `--data-file /absolute/path/payload.json`. Use `--data-file -` only when the payload contains no secrets that could be retained in shell history or logs.

## Pagination and versions

GitLab list endpoints commonly default to 20 results. Use `--paginate`; the helper follows `X-Next-Page` and emits one combined JSON array. Avoid pagination on non-list endpoints.

Self-managed GitLab versions differ. If a request returns 400 or 404 despite a valid target, inspect `GET /version` and consult the matching GitLab REST API documentation for that server version. Do not assume a GitLab.com-only or newly introduced field exists.

## Authentication and scopes

The helper sends `PRIVATE-TOKEN: $GITLAB_TOKEN`. Typical personal access token scopes are `read_api` for reads and `api` for writes, but project/group tokens and instance policy may differ. A 401 usually means invalid authentication; 403 may mean insufficient scope, role, protected-resource policy, or instance policy.

Never work around permission failures with a broader token unless the user deliberately chooses to grant it.
