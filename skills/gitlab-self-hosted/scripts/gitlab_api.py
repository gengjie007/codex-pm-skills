#!/usr/bin/env python3
"""Small authenticated client for a self-hosted GitLab REST API."""

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request


def fail(message, code=2):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def scalar(value):
    if value.startswith("json:"):
        try:
            return json.loads(value[5:])
        except json.JSONDecodeError as exc:
            fail(f"invalid json: field value: {exc}")
    return value


def pairs(items):
    result = {}
    for item in items:
        if "=" not in item:
            fail(f"expected key=value, got {item!r}")
        key, value = item.split("=", 1)
        value = scalar(value)
        if key in result:
            result[key] = result[key] if isinstance(result[key], list) else [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result


def connection():
    base = os.environ.get("GITLAB_URL", "").rstrip("/")
    token = os.environ.get("GITLAB_TOKEN", "")
    if not base:
        fail("GITLAB_URL is not set")
    if not token:
        fail("GITLAB_TOKEN is not set")
    parsed = urllib.parse.urlparse(base)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        fail("GITLAB_URL must be an absolute http(s) URL")
    ca_bundle = os.environ.get("GITLAB_CA_BUNDLE")
    context = ssl.create_default_context(cafile=ca_bundle) if parsed.scheme == "https" else None
    return base, token, context


def request(method, path, query, payload, context):
    base, token, _ = connection()
    if not path.startswith("/"):
        path = "/" + path
    url = f"{base}/api/v4{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query, doseq=True)
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {
        "Accept": "application/json",
        "PRIVATE-TOKEN": token,
        "User-Agent": "codex-gitlab-self-hosted/1",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        return urllib.request.urlopen(req, context=context, timeout=60)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        print(f"GitLab API HTTP {exc.code}: {body}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as exc:
        fail(f"cannot reach GitLab: {exc.reason}", 1)


def parse_body(response):
    raw = response.read()
    if not raw:
        return None
    text = raw.decode("utf-8", "replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    api = sub.add_parser("request", aliases=["GET", "POST", "PUT", "PATCH", "DELETE"])
    api.add_argument("path")
    api.add_argument("--method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    api.add_argument("--query", action="append", default=[], metavar="KEY=VALUE")
    api.add_argument("--field", action="append", default=[], metavar="KEY=VALUE")
    api.add_argument("--data-file")
    api.add_argument("--paginate", action="store_true")

    project = sub.add_parser("project-id", help="resolve namespace/project to a numeric project ID")
    project.add_argument("project_path")

    args = parser.parse_args()
    _, _, context = connection()

    if args.command == "project-id":
        encoded = urllib.parse.quote(args.project_path, safe="")
        body = parse_body(request("GET", f"/projects/{encoded}", {}, None, context))
        print(body["id"])
        return

    method = args.method or args.command
    query = pairs(args.query)
    if args.data_file and args.field:
        fail("use either --data-file or --field, not both")
    if args.data_file:
        stream = sys.stdin if args.data_file == "-" else open(args.data_file, encoding="utf-8")
        try:
            payload = json.load(stream)
        finally:
            if stream is not sys.stdin:
                stream.close()
    else:
        payload = pairs(args.field) if args.field else None
    if args.paginate and method != "GET":
        fail("--paginate is only valid for GET")

    if args.paginate:
        combined = []
        page = 1
        while page:
            page_query = dict(query)
            page_query.setdefault("per_page", 100)
            page_query["page"] = page
            response = request(method, args.path, page_query, payload, context)
            body = parse_body(response)
            if not isinstance(body, list):
                fail("--paginate requires an endpoint returning a JSON array", 1)
            combined.extend(body)
            next_page = response.headers.get("X-Next-Page", "")
            page = int(next_page) if next_page else 0
        body = combined
    else:
        body = parse_body(request(method, args.path, query, payload, context))

    if body is not None:
        print(json.dumps(body, ensure_ascii=False, indent=2) if not isinstance(body, str) else body)


if __name__ == "__main__":
    main()
