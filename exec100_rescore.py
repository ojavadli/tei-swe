#!/usr/bin/env python3
"""Corrected Phase-C scoring (the finisher ran the harness under base python3,
which lacks the swebench module, so it silently returned 0/0 — a broken
instrument, not a result). This re-runs the OFFICIAL SWE-bench Docker harness
with the swebench-equipped venv on the already-assembled 200 genuine preds,
then recomputes the preregistered paired result and fires the branch.

Deterministic: the 200 genuine trajectories/patches are frozen on disk; only
scoring is re-run. Detached; writes exec100_result.json (the real one).
"""
import glob
import json
import os
import subprocess
import sys
import time

ROOT = os.path.expanduser("~/swebench-agents")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from exec100_finish import sign_test, clopper_pearson  # verified stats helpers
VENV_PY = os.path.join(ROOT, "_venv_a1", "bin", "python")
INSTANCES = json.load(open("_exec100_instances.json"))


def log(m):
    print(f"[rescore {time.strftime('%H:%M:%S')}] {m}", flush=True)


def prune_sweb():
    subprocess.run("docker images --format '{{.ID}} {{.Repository}}' | grep sweb | "
                   "awk '{print $1}' | xargs -r docker rmi -f", shell=True, capture_output=True)


def score(arm):
    preds = os.path.join(ROOT, f"_exec100_{arm}_preds.json")
    run_id = f"exec100_{arm}"
    log(f"scoring {arm} (official harness, venv python, max_workers 2, cache_level none)...")
    r = subprocess.run([VENV_PY, "-m", "swebench.harness.run_evaluation",
                        "--dataset_name", "princeton-nlp/SWE-bench_Verified",
                        "--predictions_path", preds,
                        "--cache_level", "none", "--max_workers", "2",
                        "--run_id", run_id], capture_output=True, text=True)
    tail = (r.stdout or "")[-400:] + (r.stderr or "")[-400:]
    log(f"{arm} harness rc={r.returncode}; tail: {tail[-300:]}")
    resolved = set()
    reports = sorted(glob.glob(os.path.join(ROOT, f"*{run_id}*.json")))
    for rp in reports:
        try:
            d = json.load(open(rp))
        except Exception:
            continue
        rid = d.get("resolved_ids") or d.get("resolved") or []
        if isinstance(rid, list):
            resolved.update(rid)
    log(f"{arm}: {len(resolved)} resolved (from {reports})")
    return resolved, reports


def cost_exits(arm):
    from exec100_ledger import classify
    spend = exits = 0
    for inst in INSTANCES:
        for tp in glob.glob(f"_exec100_{arm}/{inst}/*.traj"):
            if classify(tp)[0] == "genuine":
                info = json.load(open(tp)).get("info", {})
                spend += (info.get("model_stats") or {}).get("instance_cost") or 0
                if "cost" in str(info.get("exit_status", "")):
                    exits += 1
                break
    return round(spend, 4), exits


def main():
    bpreds = json.load(open("_exec100_baseline_preds.json"))
    ppreds = json.load(open("_exec100_patched_preds.json"))
    prune_sweb()
    b_res, b_rep = score("baseline")
    prune_sweb()
    p_res, p_rep = score("patched")

    paired = [i for i in INSTANCES if i in bpreds and i in ppreds]
    n = len(paired)
    bset, pset = b_res & set(paired), p_res & set(paired)
    wins = sorted(i for i in paired if i in pset and i not in bset)
    losses = sorted(i for i in paired if i in bset and i not in pset)
    ties = [i for i in paired if (i in pset) == (i in bset)]
    b_spend, b_exit = cost_exits("baseline")
    p_spend, p_exit = cost_exits("patched")
    res = {
        "design": "Phase C funded execution arm (prereg-exec2 + amend1 + amend2); RE-SCORED with venv "
                  "python after the finisher's base-python scoring silently returned 0/0",
        "backbone": "gpt-5.6-luna", "per_instance_ceiling_usd": 3.0, "n_paired": n,
        "baseline_resolved": len(bset), "patched_resolved": len(pset),
        "baseline_resolve_rate": round(len(bset) / n, 4) if n else None,
        "patched_resolve_rate": round(len(pset) / n, 4) if n else None,
        "paired_wins": wins, "paired_losses": losses,
        "n_wins": len(wins), "n_losses": len(losses), "n_ties": len(ties),
        "exact_sign_p": sign_test(len(wins), len(losses)),
        "patched_rate_CP95": clopper_pearson(len(pset), n),
        "baseline_rate_CP95": clopper_pearson(len(bset), n),
        "cost": {"baseline": {"spend_usd": b_spend, "cost_limit_exits": b_exit},
                 "patched": {"spend_usd": p_spend, "cost_limit_exits": p_exit}},
        "phase_c_rollout_spend_usd": round(b_spend + p_spend, 4),
        "report_files": [os.path.basename(x) for x in (b_rep + p_rep)],
        "empty_patch_baseline": sum(1 for v in bpreds.values() if not (v.get("model_patch") or "").strip()),
        "empty_patch_patched": sum(1 for v in ppreds.values() if not (v.get("model_patch") or "").strip()),
    }
    if res["n_wins"] > res["n_losses"] and res["exact_sign_p"] < 0.05:
        branch = "POSITIVE: execution-rung gain (patched wins > losses, sign p<0.05)"
    elif res["n_losses"] > res["n_wins"] and res["exact_sign_p"] < 0.05:
        branch = "NEGATIVE: patched worse (losses > wins, sign p<0.05)"
    else:
        branch = "NULL: no significant paired execution-rung difference at this configuration"
    res["prereg_branch_fired"] = branch
    json.dump(res, open("exec100_result.json", "w"), indent=1)
    log(f"BRANCH: {branch}")
    log(f"RESULT: patched {res['patched_resolved']} vs baseline {res['baseline_resolved']} of {n}; "
        f"{res['n_wins']}W/{res['n_losses']}L; sign p={res['exact_sign_p']}")
    print("=== EXEC100-RESCORE-COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
