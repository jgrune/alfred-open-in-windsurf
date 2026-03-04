#!/usr/bin/env python3
import json
import os
import sys
import sqlite3
import subprocess
from urllib.parse import quote

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/Windsurf/User/globalStorage/state.vscdb"
)


def make_item(title, subtitle, arg, path=None, autocomplete=None):
    item = {
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": True,
    }
    if path and os.path.exists(path):
        item["icon"] = {"type": "fileicon", "path": path}
    if autocomplete is not None:
        item["autocomplete"] = autocomplete
    return item


def get_recents():
    if not os.path.exists(DB_PATH):
        return []
    try:
        conn = sqlite3.connect(f"file:{quote(DB_PATH)}?mode=ro", uri=True)
        cur = conn.execute(
            "SELECT value FROM ItemTable WHERE key = 'history.recentlyOpenedPathsList'"
        )
        row = cur.fetchone()
        conn.close()
    except Exception:
        return []

    if not row:
        return []

    try:
        data = json.loads(row[0])
        entries = data.get("entries", [])
    except Exception:
        return []

    items = []
    for entry in entries:
        uri = entry.get("folderUri") or entry.get("fileUri") or entry.get("workspace", {}).get("configPath")
        if not uri:
            continue
        # Strip file:// prefix
        if uri.startswith("file://"):
            path = uri[7:]
        else:
            path = uri
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            continue
        name = os.path.basename(path) or path
        items.append(make_item(name, path, path, path))
        if len(items) >= 20:
            break

    return items


def get_path_completions(query):
    expanded = os.path.expanduser(query)
    # Determine the directory to list
    if os.path.isdir(expanded) and query.endswith("/"):
        directory = expanded
        prefix = ""
    else:
        directory = os.path.dirname(expanded)
        prefix = os.path.basename(expanded).lower()

    if not os.path.isdir(directory):
        return []

    try:
        entries = os.listdir(directory)
    except PermissionError:
        return []

    items = []
    for name in sorted(entries):
        if prefix and not name.lower().startswith(prefix):
            continue
        if name.startswith("."):
            continue
        full_path = os.path.join(directory, name)
        is_dir = os.path.isdir(full_path)
        autocomplete = full_path + "/" if is_dir else full_path
        subtitle = "Directory" if is_dir else "File"
        items.append(make_item(name, full_path, full_path, full_path, autocomplete))
        if len(items) >= 20:
            break

    return items


def get_spotlight_results(query):
    try:
        result = subprocess.run(
            ["mdfind", "-name", query, "-onlyin", os.path.expanduser("~")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        paths = result.stdout.strip().split("\n")
    except Exception:
        return []

    items = []
    for path in paths:
        if not path or not os.path.exists(path):
            continue
        name = os.path.basename(path)
        items.append(make_item(name, path, path, path))
        if len(items) >= 20:
            break

    return items


def fallback_item(query):
    return [make_item(f'Open "{query}" in Windsurf', query, query)]


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    if not query:
        items = get_recents()
    elif query.startswith("/") or query.startswith("~"):
        items = get_path_completions(query)
    else:
        items = get_spotlight_results(query)

    if not items:
        items = fallback_item(query) if query else []

    print(json.dumps({"items": items}))


if __name__ == "__main__":
    main()
