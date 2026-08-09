#!/usr/bin/env python3
"""tei-audit: one-command blinded + syntax audit of ANY optimizer's changes.

Usage:
    python tei_audit.py --repo /path/to/repo --base <sha-or-ref> [--cand HEAD]
                        [--k 5] [--judge-model gpt-5.6-luna] [--task "one line"]

Runs the two cheapest rungs of the TEI-SWE validation ladder against the diff
base..cand:
  1. SYNTAX PRE-GATE  — ast.parse every changed .py file (deterministic, $0).
  2. BLINDED A/B      — a judge sees the real before/after hunks in randomized
                        order, k times, with no narrative and no direction.
Prints per-file syntax verdicts, the blinded vote, and an overall verdict.
Requires OPENAI_API_KEY for rung 2 only.
"""
import argparse
import ast
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tei_pipeline import call_json  # noqa: E402


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--cand", default="HEAD")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--task", default="a software system")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    repo = os.path.abspath(a.repo)

    # rung 1: syntax pre-gate
    names = sh(["git", "diff", "--name-only", f"{a.base}..{a.cand}"], repo).stdout.split()
    syn_bad = []
    for p in [n for n in names if n.endswith(".py")]:
        show = sh(["git", "show", f"{a.cand}:{p}"], repo)
        if show.returncode != 0:
            continue
        try:
            ast.parse(show.stdout)
        except SyntaxError as e:
            syn_bad.append((p, f"line {e.lineno}: {e.msg}"))
    print(f"[rung 1] syntax pre-gate: {len(syn_bad)} broken of "
          f"{sum(1 for n in names if n.endswith('.py'))} changed .py files")
    for p, e in syn_bad:
        print(f"    BROKEN {p}: {e}")

    # rung 2: blinded A/B
    num = sh(["git", "diff", "--numstat", f"{a.base}..{a.cand}"], repo).stdout
    rows = sorted((int(x) + int(y), p) for x, y, p in
                  (l.split("\t") for l in num.splitlines() if len(l.split("\t")) == 3)
                  if x.isdigit())
    pairs = []
    for _, p in rows[:4]:
        diff = sh(["git", "diff", "-U12", f"{a.base}..{a.cand}", "--", p], repo).stdout
        bef, aft = [], []
        for line in diff.splitlines():
            if line.startswith(("---", "+++", "diff ", "index ", "@@")):
                if line.startswith("@@"):
                    bef.append("  [...]"); aft.append("  [...]")
                continue
            (bef if line.startswith("-") else aft if line.startswith("+") else bef).append(line[1:])
            if not line.startswith(("-", "+")):
                aft.append(line[1:] if line else line)
        pairs.append((p, "\n".join(bef)[:2600], "\n".join(aft)[:2600]))
    votes = {"cand": 0, "base": 0, "tie": 0}
    for k in range(a.k):
        flip = rng.random() < 0.5
        blocks = [f"### file: {p}\n--- VERSION 1 ---\n{(x2 if flip else x1)}\n"
                  f"--- VERSION 2 ---\n{(x1 if flip else x2)}" for p, x1, x2 in pairs]
        prompt = (f"You are comparing two versions of {a.task}. Below, for each shown file, are the two "
                  f"versions' contents where they differ. You are NOT told which is older; judge only "
                  f"what you see.\n\n" + "\n".join(blocks) +
                  '\n\nWhich version is more likely to work correctly end-to-end? If too trivial or '
                  'ambiguous, say tie.\nReturn ONLY JSON: {"better": "1" | "2" | "tie"}')
        try:
            v = call_json(prompt, max_out=800)
        except Exception as e:
            print(f"    vote {k}: error {e}"); continue
        pick = str(v.get("better", "")).strip()
        votes["cand" if pick == ("1" if flip else "2") else
              "base" if pick in ("1", "2") else "tie"] += 1
    print(f"[rung 2] blinded A/B (k={a.k}): candidate {votes['cand']} / "
          f"baseline {votes['base']} / tie {votes['tie']}")
    verdict = ("FAIL: syntax-broken files" if syn_bad else
               "PASS: blinded-preferred" if votes["cand"] > votes["base"] + votes["tie"] else
               "INCONCLUSIVE: no blinded majority")
    print(f"[tei-audit] verdict: {verdict}")
    json.dump({"syntax_broken": syn_bad, "votes": votes, "verdict": verdict},
              open(os.path.join(os.getcwd(), "tei_audit_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
