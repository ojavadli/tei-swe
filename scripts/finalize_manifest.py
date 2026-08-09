#!/usr/bin/env python3
"""Finalize the frozen agent set (owner decision: the honest 30, strict reading).

Selection rule, applied exactly as pre-registered and NOT altered after seeing
results:
  4. parse every submission in evaluation/{lite,verified}
  5. dedupe by normalized entry name, keep the highest-scoring submission
  6. keep systems whose *kept* submission names a github.com repo in its own
     metadata, verified with `git ls-remote` (never guessed)
  7. rank by resolve rate desc

The multilingual widening was executed and added 0 sourceable systems, so the
set stands at 30. It is reported as 30; it is not padded.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from build_manifest import parse_submissions, normalize, github_repo  # noqa: E402

ROOT = os.path.expanduser("~/swebench-agents")
ARCHIVE = os.path.join(ROOT, "archive")
REPOS = os.path.join(ROOT, "_repos")
AGENTS = os.path.join(ROOT, "agents")

PROMPT_GLOBS = ("*prompt*.py", "*prompt*.yaml", "*prompt*.yml", "*prompt*.j2",
                "*prompt*.txt", "*prompt*.md", "*template*.yaml", "*template*.j2",
                "*system*.md", "*instructions*.md")


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def repos_of(r):
    out = []
    for u in r["site_urls"] + r["report_urls"]:
        g = github_repo(u)
        if g and g not in out:
            out.append(g)
    return out


def slugify(key):
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def find_prompt_surface(root, limit=25):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__", ".venv")]
        for fn in filenames:
            low = fn.lower()
            if any(re.fullmatch(g.replace("*", ".*"), low) for g in PROMPT_GLOBS):
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                try:
                    size = os.path.getsize(os.path.join(dirpath, fn))
                except OSError:
                    continue
                hits.append({"path": rel, "bytes": size})
    hits.sort(key=lambda h: -h["bytes"])
    return hits[:limit]


def main():
    rows = parse_submissions(["lite", "verified"])
    systems = {}
    for r in rows:
        systems.setdefault(normalize(r["name"]), []).append(r)

    kept = []
    for key, subs in systems.items():
        top = max(subs, key=lambda x: x["resolve_rate"])
        rp = repos_of(top)
        if not rp:
            continue
        rec = dict(top)
        rec["system_key"] = key
        rec["slug"] = slugify(key)
        rec["repo_url"] = rp[0]
        kept.append(rec)
    kept.sort(key=lambda r: (-r["resolve_rate"], r["system_key"]))
    print(f"unique systems: {len(systems)} | sourceable (strict): {len(kept)}")

    os.makedirs(AGENTS, exist_ok=True)
    manifest = []
    for i, rec in enumerate(kept, start=1):
        rank = f"{i:02d}"
        dest = os.path.join(AGENTS, f"{rank}_{rec['slug']}")
        src = os.path.join(REPOS, rec["slug"])
        if not os.path.isdir(dest):
            if not os.path.isdir(src):
                print(f"  !! missing clone for {rec['slug']}")
                continue
            shutil.copytree(src, dest, symlinks=True)
        sha = sh(["git", "rev-parse", "HEAD"], cwd=dest).stdout.strip()
        # local work branch; never pushed
        sh(["git", "checkout", "-B", "tei-v7"], cwd=dest)

        sub_dir = os.path.join(ARCHIVE, "evaluation", rec["split"], rec["folder"])
        res = json.load(open(os.path.join(sub_dir, "results", "results.json")))["resolved"]
        resolved_ids = res if isinstance(res, list) else []

        prompt_surface = find_prompt_surface(dest)
        os.makedirs(os.path.join(dest, "tei"), exist_ok=True)
        json.dump({
            "rank": i, "system": rec["name"], "system_key": rec["system_key"],
            "slug": rec["slug"], "split": rec["split"], "submission_folder": rec["folder"],
            "date": rec["date"], "model": rec["model"],
            "resolved": rec["resolved"], "resolve_rate": rec["resolve_rate"],
            "repo_url": rec["repo_url"], "repo_sha": sha,
            "site_urls": rec["site_urls"], "report_urls": rec["report_urls"],
            "archive_has_logs": rec["has_logs"], "archive_has_trajs": rec["has_trajs"],
            "recorded_trajectories_available": 0,
            "trajectory_note": ("SWE-bench/experiments ships aggregate results only; logs/ and "
                                "trajs/ are in a credentialed S3 bucket (archive README). No AWS "
                                "access per owner directive, so 0 recorded trajectories were read."),
            "resolved_instance_ids": resolved_ids,
            "n_resolved_ids": len(resolved_ids),
            "prompt_surface": prompt_surface,
            "n_prompt_surface_files": len(prompt_surface),
        }, open(os.path.join(dest, "tei", "onboarding.json"), "w"), indent=2)

        manifest.append({
            "rank": i, "system": rec["name"], "slug": rec["slug"], "split": rec["split"],
            "date": rec["date"], "model": rec["model"], "resolved": rec["resolved"],
            "resolve_rate": rec["resolve_rate"],
            "site_url": "; ".join(rec["site_urls"]), "report_url": "; ".join(rec["report_urls"]),
            "repo_url": rec["repo_url"], "repo_sha": sha,
            "local_path": dest, "has_logs": rec["has_logs"], "has_trajs": rec["has_trajs"],
        })
        print(f"  {rank} {rec['slug']:26s} {rec['resolve_rate']:6.2f} sha={sha[:8]} "
              f"prompts={len(prompt_surface):3d} resolved_ids={len(resolved_ids)}")

    json.dump(manifest, open(os.path.join(ROOT, "manifest.json"), "w"), indent=2)
    with open(os.path.join(ROOT, "manifest.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    print(f"\nwrote manifest.json / manifest.csv with {len(manifest)} systems")


if __name__ == "__main__":
    main()
