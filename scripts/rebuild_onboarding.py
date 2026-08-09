#!/usr/bin/env python3
"""Regenerate tei/onboarding.json for any agent missing it.

Needed because an early version of the pipeline staged with `git add -A`, which
committed our own tei/ artifacts into the agent repositories; a later
`git reset --hard` to the pristine SHA then deleted them. The staging bug is
fixed; this restores the casualties.
"""
import glob
import json
import os
import sys

import yaml

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from find_prompt_surface import scan  # noqa: E402

ROOT = os.path.expanduser("~/swebench-agents")
ARCHIVE = os.path.join(ROOT, "archive")
AGENTS = os.path.join(ROOT, "agents")
TOTALS = {"lite": 300, "verified": 500}

TRAJ_NOTE = ("SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a "
             "credentialed S3 bucket (archive README). No AWS access per owner directive, so "
             "0 recorded trajectories were read.")
IN_REPO_NOTE = ("Trajectories committed to the agent's OWN repository (distinct from the archive's "
                "credentialed S3 assets). Not used for scoring in this run: the study applies one "
                "uniform PROXY substrate to all 30 agents.")


def find_submission(m):
    """Locate the archive submission folder this manifest row came from."""
    base = os.path.join(ARCHIVE, "evaluation", m["split"])
    total = TOTALS[m["split"]]
    for folder in sorted(os.listdir(base)):
        mp = os.path.join(base, folder, "metadata.yaml")
        if not os.path.isfile(mp):
            mp = os.path.join(base, folder, "metadata.yml")
        rp = os.path.join(base, folder, "results", "results.json")
        if not (os.path.isfile(mp) and os.path.isfile(rp)):
            continue
        md = yaml.safe_load(open(mp)) or {}
        name = (md.get("info") or {}).get("name")
        if name is None:
            name = folder.split("_", 1)[1] if "_" in folder else folder
        if name != m["system"]:
            continue
        r = json.load(open(rp))["resolved"]
        n = len(r) if isinstance(r, list) else r
        if abs(round(n * 100.0 / total, 2) - m["resolve_rate"]) < 0.01:
            return folder, (r if isinstance(r, list) else [])
    return None, []


def in_repo_trajs(p):
    n = 0
    for pat in ("**/*.traj", "**/trajs/**/*", "**/trajectories/**/*.json"):
        n += len([f for f in glob.glob(os.path.join(p, pat), recursive=True)
                  if os.path.isfile(f) and "/.git/" not in f and "/tei/" not in f])
    return n


def main():
    manifest = json.load(open(os.path.join(ROOT, "manifest.json")))
    rebuilt = 0
    for m in manifest:
        p = m["local_path"]
        ob_path = os.path.join(p, "tei", "onboarding.json")
        if os.path.isfile(ob_path):
            continue
        folder, ids = find_submission(m)
        if folder is None:
            print(f"  !! could not match archive submission for {m['slug']}; skipping")
            continue
        hits = scan(p)
        os.makedirs(os.path.join(p, "tei"), exist_ok=True)
        json.dump({
            "rank": m["rank"], "system": m["system"], "system_key": m["slug"], "slug": m["slug"],
            "split": m["split"], "submission_folder": folder, "date": m["date"], "model": m["model"],
            "resolved": m["resolved"], "resolve_rate": m["resolve_rate"],
            "repo_url": m["repo_url"], "repo_sha": m["repo_sha"],
            "site_urls": [m["site_url"]], "report_urls": [m["report_url"]],
            "archive_has_logs": False, "archive_has_trajs": False,
            "recorded_trajectories_available": 0, "trajectory_note": TRAJ_NOTE,
            "in_repo_trajectory_files": in_repo_trajs(p), "in_repo_trajectory_note": IN_REPO_NOTE,
            "resolved_instance_ids": ids, "n_resolved_ids": len(ids),
            "prompt_surface": hits, "n_prompt_surface_files": len(hits),
            "prompt_surface_method": "content-marker scan",
        }, open(ob_path, "w"), indent=2)
        rebuilt += 1
        print(f"  rebuilt {m['slug']:24s} folder={folder} ids={len(ids)} prompts={len(hits)}")
    print(f"rebuilt {rebuilt} onboarding files")


if __name__ == "__main__":
    main()
