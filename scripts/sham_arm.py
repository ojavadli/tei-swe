#!/usr/bin/env python3
"""Sham-patch placebo arm, exactly as pre-registered in PREREG_SHAM.md
(tag prereg-sham). Mechanical sham construction (no LLM), then the identical
blinded protocol with fresh seed 7. One pass; no re-rolls."""
import ast
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from tei_pipeline import call_json, BUDGET
import blind_reval as BR

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
K = 5
rng = random.Random(7)

COMMENT = {"py": "# NOTE: routine maintenance annotation (rev {i}); no functional change.",
           "yaml": "# note: routine maintenance annotation (rev {i}); no functional change.",
           "yml": "# note: routine maintenance annotation (rev {i}); no functional change.",
           "md": "<!-- routine maintenance annotation (rev {i}); no functional change. -->",
           "txt": "routine maintenance annotation (rev {i}); no functional change.",
           "cfg": "# note: routine maintenance annotation (rev {i}); no functional change.",
           "toml": "# note: routine maintenance annotation (rev {i}); no functional change."}


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def build_sham(repo, base_sha):
    """Branch sham-v1 from base; insert length-matched comment lines into the
    same files tei-v7 changed. Returns (files_shammed, skipped)."""
    sh(["git", "checkout", "-q", "-B", "sham-v1", base_sha], repo)
    num = sh(["git", "diff", "--numstat", f"{base_sha}..tei-v7"], repo).stdout
    shammed, skipped = [], []
    for line in num.splitlines():
        parts = line.split("\t")
        if len(parts) != 3 or not parts[0].isdigit():
            continue
        added, path = int(parts[0]), parts[2]
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        fp = os.path.join(repo, path)
        if ext not in COMMENT or not os.path.isfile(fp) or added == 0:
            skipped.append(path)
            continue
        tmpl = COMMENT[ext]
        block = "\n" + "\n".join(tmpl.format(i=i + 1) for i in range(added)) + "\n"
        with open(fp, "a") as f:
            f.write(block)
        if ext == "py":
            try:
                ast.parse(open(fp, errors="ignore").read())
            except SyntaxError:
                # revert this file; comments at EOF cannot normally break parsing,
                # but the pre-registration requires ast-clean shams
                sh(["git", "checkout", "-q", "--", path], repo)
                skipped.append(path)
                continue
        shammed.append((path, added))
    sh(["git", "add", "-A"], repo)
    sh(["git", "commit", "-qm", "sham-v1: semantically-null length-matched annotations (placebo arm)"], repo)
    return shammed, skipped


def main():
    results = []
    dirs = sorted(d for d in os.listdir(AGENTS) if os.path.isdir(os.path.join(AGENTS, d)))
    for d in dirs:
        repo = os.path.join(AGENTS, d)
        res = json.load(open(os.path.join(repo, "tei", "result.json")))
        ob = json.load(open(os.path.join(repo, "tei", "onboarding.json")))
        if res.get("n_applied", 0) == 0:
            continue
        base_sha = ob["repo_sha"]
        cur = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()
        shammed, skipped = build_sham(repo, base_sha)
        try:
            if not shammed:
                results.append({"agent": d, "skipped": "no shammable files"})
                continue
            # identical blinded protocol, HEAD = sham-v1
            files = BR.changed_files(repo, base_sha)
            pairs = [(p, *e) for p in files if (e := BR.excerpt_pair(repo, base_sha, p))]
            probes = [p["instance_id"] for p in json.load(
                open(os.path.join(repo, "tei", "baseline_eval.json"))).get("probes", [])][:4]
            votes = []
            for k in range(K):
                flip = rng.random() < 0.5
                blocks = [f"### file: {path}\n--- VERSION 1 ---\n{(aft if flip else bef)}\n"
                          f"--- VERSION 2 ---\n{(bef if flip else aft)}"
                          for path, bef, aft in pairs]
                prompt = f"""You are comparing two versions of the same software-engineering agent system
({ob['system']}; its job: resolve real GitHub issues, SWE-bench style). Below, for each shown file,
are the two versions' contents in the regions where they differ. You are NOT told which version is
older; judge only what you see.

Representative task instances this agent faces: {', '.join(probes)}.

{chr(10).join(blocks)}

Which version is more likely to resolve such issues correctly end-to-end? Consider robustness,
verification behavior, and failure handling actually visible in the text. If the differences are
too trivial or ambiguous to matter, say tie.

Return ONLY JSON: {{"better": "1" | "2" | "tie", "confidence": 0.0, "reason": "one sentence"}}"""
                try:
                    v = call_json(prompt, max_out=1200)
                except Exception as e:
                    votes.append({"error": str(e)[:60]})
                    continue
                pick = str(v.get("better", "")).strip()
                votes.append({"vote": ("sham" if pick == ("1" if flip else "2") else
                                       "baseline" if pick in ("1", "2") else "tie"),
                              "reason": str(v.get("reason", ""))[:140]})
            pv = sum(1 for v in votes if v.get("vote") == "sham")
            bv = sum(1 for v in votes if v.get("vote") == "baseline")
            tv = sum(1 for v in votes if v.get("vote") == "tie")
            results.append({"agent": d, "files_shammed": len(shammed),
                            "skipped_files": skipped, "votes": votes,
                            "sham": pv, "baseline": bv, "tie": tv})
            print(f"{d:30s} sham {pv} / base {bv} / tie {tv}  "
                  f"[${BUDGET.conservative:.2f}]", flush=True)
        finally:
            sh(["git", "checkout", "-q", cur or "tei-v7"], repo)

    done = [r for r in results if "votes" in r]
    sham_votes = sum(r["sham"] for r in done)
    all_votes = sum(r["sham"] + r["baseline"] + r["tie"] for r in done)
    maj = sum(1 for r in done if r["sham"] > r["baseline"] + r["tie"])
    share = sham_votes / all_votes if all_votes else float("nan")
    branch = ("CERTIFIED (share <= 60%)" if share <= 0.60 else
              "side-by-side (60-85%)" if share < 0.85 else
              "style-reframe (>= 85%)")
    out = {"k": K, "seed": 7, "results": results,
           "pooled": {"sham_votes": sham_votes, "all_votes": all_votes,
                      "share": share, "agents_majority_sham": maj,
                      "n_agents": len(done)},
           "prereg_branch_fired": branch, "budget": BUDGET.as_dict()}
    json.dump(out, open(os.path.join(ROOT, "sham_arm.json"), "w"), indent=1)
    print(f"\nSHAM ARM: share={share:.3f} ({sham_votes}/{all_votes}), "
          f"majorities={maj}/{len(done)} -> {branch}")
    print("budget:", json.dumps(BUDGET.as_dict()))


if __name__ == "__main__":
    main()
