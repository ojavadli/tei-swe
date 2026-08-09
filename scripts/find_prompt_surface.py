#!/usr/bin/env python3
"""Content-based prompt-surface detection, rewritten into each agent's tei/onboarding.json.

Filename heuristics alone miss real surfaces (e.g. SWE-agent keeps system_template
in config/*.yaml), so this scans file *content* for prompt-defining markers and
ranks candidates by marker density.
"""
import json
import os
import re

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")

MARKERS = [
    r"system_template", r"instance_template", r"system_prompt", r"SYSTEM_PROMPT",
    r"user_prompt", r"USER_PROMPT", r"prompt_template", r"PROMPT_TEMPLATE",
    r"\bYou are (an?|the) ", r"role\"?\s*[:=]\s*\"?system", r"<\|im_start\|>system",
    r"ChatPromptTemplate", r"SystemMessage", r"instructions\s*[:=]\s*[\"']",
]
MARK_RE = re.compile("|".join(MARKERS))
EXT_OK = {".py", ".yaml", ".yml", ".json", ".j2", ".jinja", ".jinja2", ".txt", ".md", ".toml", ".ts", ".js"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
             ".mypy_cache", ".pytest_cache", "test_data", "tests", "docs"}
MAX_BYTES = 400_000


def scan(root, limit=20):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if "/tei" in dirpath:
            continue
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in EXT_OK:
                continue
            fp = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(fp) > MAX_BYTES:
                    continue
                text = open(fp, "r", errors="ignore").read()
            except OSError:
                continue
            n = len(MARK_RE.findall(text))
            if n:
                hits.append({
                    "path": os.path.relpath(fp, root),
                    "markers": n,
                    "bytes": len(text),
                    "sample": (MARK_RE.search(text).group(0) or "")[:40],
                })
    hits.sort(key=lambda h: (-h["markers"], h["bytes"]))
    return hits[:limit]


def main():
    total_with = 0
    for d in sorted(os.listdir(AGENTS)):
        p = os.path.join(AGENTS, d)
        ob = os.path.join(p, "tei", "onboarding.json")
        if not os.path.isfile(ob):
            continue
        data = json.load(open(ob))
        hits = scan(p)
        data["prompt_surface"] = hits
        data["n_prompt_surface_files"] = len(hits)
        data["prompt_surface_method"] = "content-marker scan (system_template/system_prompt/'You are a'/...)"
        json.dump(data, open(ob, "w"), indent=2)
        total_with += bool(hits)
        top = hits[0]["path"] if hits else "-- none found --"
        print(f"{d:30s} files={len(hits):3d}  top={top[:56]}")
    print(f"\nagents with an identified prompt surface: {total_with}/30")


if __name__ == "__main__":
    main()
