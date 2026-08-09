#!/usr/bin/env python3
"""Stage shallow clones for every sourceable system under either selection reading.

Clones into ~/swebench-agents/_repos/<slug>/ (no rank in the path) because the
rank depends on which selection reading the owner approves. The final ranked
layout under agents/<rank>_<slug>/ is created once that is decided.
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from build_manifest import parse_submissions, normalize, github_repo  # noqa: E402

ROOT = os.path.expanduser("~/swebench-agents")
REPOS = os.path.join(ROOT, "_repos")


def repos_of(r):
    out = []
    for u in r["site_urls"] + r["report_urls"]:
        g = github_repo(u)
        if g and g not in out:
            out.append(g)
    return out


def slugify(key):
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def build_selection():
    rows = parse_submissions(["lite", "verified"])
    systems = {}
    for r in rows:
        systems.setdefault(normalize(r["name"]), []).append(r)

    recs = {}
    for key, subs in systems.items():
        top = max(subs, key=lambda x: x["resolve_rate"])
        top_repos = repos_of(top)
        any_sub = next((s for s in sorted(subs, key=lambda x: -x["resolve_rate"]) if repos_of(s)), None)
        if not (top_repos or any_sub):
            continue
        rec = dict(top)
        rec["system_key"] = key
        rec["slug"] = slugify(key)
        rec["repo_url"] = top_repos[0] if top_repos else repos_of(any_sub)[0]
        rec["repo_url_from_submission"] = top["folder"] if top_repos else any_sub["folder"]
        rec["qualifies_reading_A"] = bool(top_repos)
        rec["qualifies_reading_B"] = True
        recs[key] = rec

    ordered = sorted(recs.values(), key=lambda r: (-r["resolve_rate"], r["system_key"]))
    json.dump(ordered, open(os.path.join(ROOT, "_selection.json"), "w"), indent=2)
    return ordered


def clone(rec):
    dest = os.path.join(REPOS, rec["slug"])
    if os.path.isdir(os.path.join(dest, ".git")):
        return rec["slug"], "exists"
    os.makedirs(REPOS, exist_ok=True)
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/bin/true")
    try:
        p = subprocess.run(["git", "clone", "--depth", "1", rec["repo_url"], dest],
                           capture_output=True, timeout=900, env=env)
        return rec["slug"], "ok" if p.returncode == 0 else f"FAIL {p.stderr.decode()[:120]}"
    except subprocess.TimeoutExpired:
        return rec["slug"], "FAIL timeout"


if __name__ == "__main__":
    sel = build_selection()
    print(f"sourceable systems staged: {len(sel)} "
          f"(reading A: {sum(r['qualifies_reading_A'] for r in sel)}, reading B: {len(sel)})")
    with ThreadPoolExecutor(max_workers=6) as ex:
        for slug, status in ex.map(clone, sel):
            print(f"{status:10s} {slug}", flush=True)
