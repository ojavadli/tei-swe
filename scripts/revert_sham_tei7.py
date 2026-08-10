#!/usr/bin/env python3
"""B3 pre-step: revert the historical sham-v1 placebo commit that landed INSIDE
tei-v7 history for 7 agents (a failed `git checkout -B` during the sham arm
committed the annotations onto tei-v7 instead of the sham-v1 branch).

The annotations are semantically-null EOF comment lines; both Phase-B arms
shared them identically, so arm comparisons are unaffected. They must still be
removed before the B3 blinded re-run, whose excerpts come from base..HEAD repo
diffs. Reverting (not rewriting) preserves history; every repo is ast-verified
after the revert. Run ONLY after all Phase-B shards have exited.
"""
import ast
import json
import os
import subprocess
import sys

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
AFFECTED = ["01_livesweagent", "03_trae", "05_joycode", "12_kgcompass",
            "20_sweexp", "22_orcaloca", "23_patchedcodespatchwork"]


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    if sh(["pgrep", "-f", "tei_pipeline.py"], None).stdout.strip():
        sys.exit("REFUSING: tei_pipeline.py processes still running")
    out = []
    for d in AFFECTED:
        repo = os.path.join(AGENTS, d)
        br = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()
        if br != "tei-v7":
            out.append({"agent": d, "status": f"SKIP: on branch {br}, expected tei-v7"})
            continue
        shas = [l.split()[0] for l in sh(["git", "log", "--oneline", "tei-v7"], repo).stdout.splitlines()
                if "sham-v1:" in l]
        if len(shas) != 1:
            out.append({"agent": d, "status": f"SKIP: {len(shas)} sham commits found, expected 1"})
            continue
        r = sh(["git", "revert", "--no-edit", shas[0]], repo)
        if r.returncode != 0:
            sh(["git", "revert", "--abort"], repo)
            out.append({"agent": d, "status": f"REVERT-FAILED: {(r.stderr or r.stdout)[-160:]}"})
            continue
        # ast-verify every tracked .py the revert touched
        touched = sh(["git", "diff", "--name-only", "HEAD~1..HEAD"], repo).stdout.split()
        bad = []
        for p in touched:
            if p.endswith(".py") and os.path.isfile(os.path.join(repo, p)):
                try:
                    ast.parse(open(os.path.join(repo, p), errors="ignore").read())
                except SyntaxError as e:
                    bad.append(f"{p}: line {e.lineno} {e.msg}")
        out.append({"agent": d, "status": "reverted", "sham_sha": shas[0],
                    "revert_sha": sh(["git", "rev-parse", "HEAD"], repo).stdout.strip()[:12],
                    "files_touched": len(touched), "ast_failures": bad})
        print(f"{d:28s} reverted {shas[0]} -> {out[-1]['revert_sha']} "
              f"({len(touched)} files, ast_failures={len(bad)})", flush=True)
    json.dump({"affected": AFFECTED, "results": out},
              open(os.path.join(ROOT, "sham_revert_log.json"), "w"), indent=1)
    print("wrote sham_revert_log.json")


if __name__ == "__main__":
    main()
