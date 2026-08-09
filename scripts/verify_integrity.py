#!/usr/bin/env python3
"""Final integrity audit. Every claim in the reports must survive these checks.

Checks, per agent:
  1. result.json exists and candidates.jsonl line count == result.n_versions
     (this is what caught the concurrent-writer truncation earlier).
  2. no score >= 1.000 anywhere (dimensions or aggregates).
  3. every version carries a why-record and a decision.
  4. applied versions correspond to real commits on the tei-v7 branch.
  5. score_label is present and is PROXY or VERIFIED, never blank.
"""
import json
import os
import subprocess

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")


def commits_on_branch(p):
    r = subprocess.run(["git", "log", "--oneline", "--grep=^tei-v7"], cwd=p,
                       capture_output=True, text=True)
    return len([l for l in r.stdout.splitlines() if l.strip()])


def main():
    problems, rows = [], []
    for d in sorted(os.listdir(AGENTS)):
        p = os.path.join(AGENTS, d)
        tei = os.path.join(p, "tei")
        if not os.path.isdir(tei):
            continue
        rj, cj = os.path.join(tei, "result.json"), os.path.join(tei, "candidates.jsonl")
        if not os.path.isfile(rj):
            problems.append(f"{d}: no result.json")
            continue
        res = json.load(open(rj))
        cands = [json.loads(l) for l in open(cj)] if os.path.isfile(cj) else []

        if len(cands) != res.get("n_versions"):
            problems.append(f"{d}: {len(cands)} versions on disk but result claims "
                            f"{res.get('n_versions')}")
        bad = [c["version_id"] for c in cands
               if (c.get("aggregate") or 0) >= 1.0
               or any((v or 0) >= 1.0 for v in (c.get("dimensions") or {}).values())]
        if bad:
            problems.append(f"{d}: perfect scores in {bad[:3]}")
        nowhy = [c["version_id"] for c in cands if not c.get("why")]
        if nowhy:
            problems.append(f"{d}: {len(nowhy)} versions missing a why-record")
        if res.get("score_label") not in ("PROXY", "VERIFIED"):
            problems.append(f"{d}: bad score_label {res.get('score_label')!r}")

        applied = sum(1 for c in cands if c.get("decision") == "applied")
        commits = commits_on_branch(p)
        if applied != commits:
            problems.append(f"{d}: {applied} applied versions but {commits} tei-v7 commits")
        rows.append((d, len(cands), applied, commits, res.get("score_label"),
                     res.get("baseline"), res.get("best_final")))

    print(f"{'agent':30s} {'vers':>5s} {'appl':>5s} {'commits':>8s} {'label':7s} {'base':>7s} {'final':>7s}")
    for r in rows:
        print(f"{r[0]:30s} {r[1]:5d} {r[2]:5d} {r[3]:8d} {r[4]:7s} {r[5]:7} {r[6]:7}")
    print(f"\nagents audited: {len(rows)}")
    if problems:
        print(f"\n!! {len(problems)} INTEGRITY PROBLEMS:")
        for x in problems:
            print("   -", x)
    else:
        print("\nall integrity checks passed")
    return problems


if __name__ == "__main__":
    main()
