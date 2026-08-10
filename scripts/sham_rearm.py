#!/usr/bin/env python3
"""B3: re-anchored sham-placebo comparison at the NEW (post-100+100) bests, on
the fixed-seed 10-agent subsample preregistered in BUDGET_100.md
(`random.Random(21).sample(sorted(slugs), 10)`), k=5, vote-order seed 21.

Protocol identical to sham_arm.py (prereg-sham): mechanical length-matched
null annotations in the same files tei-v7 changed (now the full base..tei-v7
endpoint diff, in which the reverted historical annotations cancel), then the
identical randomized narrative-free blinded comparison.

Hardening vs the original: after `checkout -B sham-v1 <base>` the script
VERIFIES HEAD is the sham-v1 branch and the tree was clean, else it aborts
that agent — the failure mode that once committed shams onto tei-v7 cannot
recur. Run ONLY after revert_sham_tei7.py.
"""
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from tei_pipeline import BUDGET  # noqa: E402
import sham_arm as SA  # noqa: E402  (reuses build_sham + blinded prompt machinery)
import blind_reval as BR  # noqa: E402
from tei_pipeline import call_json  # noqa: E402

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
K = 5
SEED = 21


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    if sh(["pgrep", "-f", "tei_pipeline.py --extend"], None).stdout.strip():
        sys.exit("REFUSING: extension shards still running")
    rng = random.Random(SEED)
    dirs = sorted(d for d in os.listdir(AGENTS) if os.path.isdir(os.path.join(AGENTS, d)))
    subsample = sorted(rng.sample(dirs, 10))
    print("preregistered seed-21 subsample:", subsample, flush=True)
    results = []
    for d in subsample:
        repo = os.path.join(AGENTS, d)
        ob = json.load(open(os.path.join(repo, "tei", "onboarding.json")))
        res = json.load(open(os.path.join(repo, "tei", "result.json")))
        if res.get("n_applied", 0) == 0:
            results.append({"agent": d, "skipped": "zero applied versions"})
            continue
        base_sha = ob["repo_sha"]
        if sh(["git", "status", "--porcelain"], repo).stdout.strip():
            results.append({"agent": d, "skipped": "dirty tree (refusing sham build)"})
            continue
        cur = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()
        shammed, skipped = SA.build_sham(repo, base_sha)
        try:
            head_branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()
            if head_branch != "sham-v1":
                results.append({"agent": d, "skipped": f"guard: HEAD is {head_branch}, not sham-v1"})
                continue
            if not shammed:
                results.append({"agent": d, "skipped": "no shammable files"})
                continue
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
            back = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()
            if back != (cur or "tei-v7"):
                print(f"  !! {d}: RESTORE FAILED, on {back}", flush=True)

    done = [r for r in results if "votes" in r]
    sham_votes = sum(r["sham"] for r in done)
    all_votes = sum(r["sham"] + r["baseline"] + r["tie"] for r in done)
    maj = sum(1 for r in done if r["sham"] > r["baseline"] + r["tie"])
    share = sham_votes / all_votes if all_votes else float("nan")
    out = {"k": K, "seed": SEED, "subsample": subsample, "results": results,
           "pooled": {"sham_votes": sham_votes, "all_votes": all_votes,
                      "share": share, "agents_majority_sham": maj, "n_agents": len(done)},
           "budget": BUDGET.as_dict(),
           "design": "re-anchored at post-100+100 bests per BUDGET_100.md (tag prereg-100)"}
    json.dump(out, open(os.path.join(ROOT, "sham_rearm.json"), "w"), indent=1)
    print(f"\nSHAM RE-ANCHOR: share={share:.3f} ({sham_votes}/{all_votes}), "
          f"majorities={maj}/{len(done)}")
    print("budget:", json.dumps(BUDGET.as_dict()))


if __name__ == "__main__":
    main()
