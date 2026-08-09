#!/usr/bin/env python3
"""
Part 1: build the frozen agent set from the official SWE-bench submission archive.

Stage 1 (this script, --stage parse): parse every submission in the requested
splits, dedupe to unique systems, and extract *candidate* repo URLs.
Stage 2 (--stage select): consume git ls-remote verification results and emit
the final manifest.

No URL is ever guessed: a candidate repo URL must literally appear in the
submission's own metadata (info.site or info.report).
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

import yaml

ARCHIVE = os.path.expanduser("~/swebench-agents/archive")
SPLIT_TOTALS = {"lite": 300, "verified": 500}  # from archive analysis/get_leaderboard.py


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def load_metadata(path):
    mp = os.path.join(path, "metadata.yaml")
    if not os.path.isfile(mp):
        mp = os.path.join(path, "metadata.yml")
    return yaml.safe_load(open(mp)) or {}


def parse_submissions(splits):
    rows = []
    for split in splits:
        total = SPLIT_TOTALS[split]
        base = os.path.join(ARCHIVE, "evaluation", split)
        for folder in sorted(os.listdir(base)):
            p = os.path.join(base, folder)
            if not os.path.isdir(p):
                continue
            md = load_metadata(p)
            info = md.get("info") or {}
            tags = md.get("tags") or {}
            res = json.load(open(os.path.join(p, "results", "results.json")))["resolved"]
            n = len(res) if isinstance(res, list) else res
            date = folder.split("_", 1)[0]
            date = f"{date[:4]}-{date[4:6]}-{date[6:]}" if len(date) == 8 else ""
            name = info.get("name")
            name_from_folder = name is None
            if name_from_folder:  # honest fallback, recorded
                name = folder.split("_", 1)[1] if "_" in folder else folder
            rows.append({
                "split": split,
                "folder": folder,
                "date": date,
                "name": name,
                "name_from_folder": name_from_folder,
                "site_urls": [str(s) for s in as_list(info.get("site"))],
                "report_urls": [str(s) for s in as_list(info.get("report"))],
                "model": ", ".join(str(m) for m in as_list(tags.get("model"))),
                "resolved": n,
                "resolve_rate": round(n * 100.0 / total, 2),
                # The archive ships aggregate results only; logs/ and trajs/ live
                # in a credentialed S3 bucket (see archive README).
                "has_logs": os.path.isdir(os.path.join(p, "logs")),
                "has_trajs": os.path.isdir(os.path.join(p, "trajs")),
            })
    return rows


PAREN = re.compile(r"\([^)]*\)")
DATE_SUF = re.compile(r"[-_ ]?(v?\d{8}|\d{4}-\d{2}-\d{2})\b")
VER_SUF = re.compile(r"[-_ ]v\d+(\.\d+)*[a-z0-9]*\b")
NONWORD = re.compile(r"[^a-z0-9]+")


def normalize(name):
    """lowercase, strip parentheticals and model/version suffixes, collapse ws."""
    s = str(name).lower()
    s = PAREN.sub(" ", s)          # drop "(2025-05-22)", "(bash-only)"
    s = s.split("+")[0]            # "SWE-agent + Claude 4 Sonnet" -> system only
    s = s.split(" x ")[0]          # "Lingxi v1.5 x Kimi K2"
    s = re.split(r"[_](?=claude|gpt|gemini|qwen|deepseek|kimi|glm|llama|o\d)", s)[0]
    s = DATE_SUF.sub(" ", s)
    s = VER_SUF.sub(" ", s)
    s = NONWORD.sub(" ", s).strip()
    s = re.sub(r"\s+", " ", s)
    # Collapse whitespace entirely for the identity key, so that a system written
    # "SWE-Kit" and "SWEkit" resolves to one system rather than two.
    return s.replace(" ", "")


def github_repo(url):
    """Return canonical https://github.com/<org>/<repo> or None. Never guesses."""
    try:
        u = urlparse(url)
    except Exception:
        return None
    if u.netloc.lower() not in ("github.com", "www.github.com"):
        return None
    parts = [p for p in u.path.split("/") if p]
    if len(parts) < 2:
        return None
    org, repo = parts[0], parts[1]
    if org.lower() in ("orgs", "features", "about", "topics"):
        return None
    repo = re.sub(r"\.git$", "", repo)
    # Reject the archive itself: it is not the agent's source.
    if (org.lower(), repo.lower()) == ("swe-bench", "experiments"):
        return None
    return f"https://github.com/{org}/{repo}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", nargs="+", default=["lite", "verified"])
    ap.add_argument("--out", default=os.path.expanduser("~/swebench-agents/_candidates.json"))
    a = ap.parse_args()

    rows = parse_submissions(a.splits)
    print(f"submissions parsed: {len(rows)} from splits {a.splits}")

    # Dedupe: keep the highest-scoring submission per normalized system name.
    systems = {}
    for r in rows:
        key = normalize(r["name"])
        if not key:
            continue
        cur = systems.get(key)
        if cur is None or r["resolve_rate"] > cur["resolve_rate"]:
            systems[key] = r
    print(f"unique systems after dedupe: {len(systems)}")

    # Candidate repo URL strictly from the submission's own metadata.
    for key, r in systems.items():
        cands = []
        for u in r["site_urls"] + r["report_urls"]:
            g = github_repo(u)
            if g and g not in cands:
                cands.append(g)
        r["system_key"] = key
        r["repo_candidates"] = cands
    with_repo = [r for r in systems.values() if r["repo_candidates"]]
    print(f"systems with a github repo URL in metadata: {len(with_repo)}")

    json.dump(sorted(systems.values(), key=lambda r: -r["resolve_rate"]),
              open(a.out, "w"), indent=2)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
