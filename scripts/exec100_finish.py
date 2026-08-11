#!/usr/bin/env python3
"""Autonomous Phase-C finisher: wait for 100 genuine baseline + 100 genuine
patched rollouts, freeze, assemble preds from the genuine trajectories, run the
official SWE-bench Docker harness per arm exactly as preregistered, and compute
the paired result (wins/losses, resolve rates, exact sign test, Clopper-Pearson
CI, cost-limit exits, spend). Self-contained so Phase C completes without
depending on the assistant being re-invoked.
"""
import glob
import json
import math
import os
import subprocess
import sys
import time

ROOT = os.path.expanduser("~/swebench-agents")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from exec100_ledger import classify, arm_stats  # noqa: E402

INSTANCES = json.load(open("_exec100_instances.json"))


def genuine_map(arm):
    out = {}
    for inst in INSTANCES:
        for tp in glob.glob(f"_exec100_{arm}/{inst}/*.traj"):
            if classify(tp)[0] == "genuine":
                out[inst] = tp
                break
    return out


def assemble_preds(arm):
    preds = {}
    for inst, tp in genuine_map(arm).items():
        info = json.load(open(tp)).get("info", {})
        preds[inst] = {"model_name_or_path": f"gpt-5.6-luna-{arm}",
                       "model_patch": info.get("submission") or "",
                       "instance_id": inst}
    path = os.path.join(ROOT, f"_exec100_{arm}_preds.json")
    json.dump(preds, open(path, "w"), indent=1)
    return path, preds


def cost_and_exits(arm):
    spend = exits = 0
    for inst, tp in genuine_map(arm).items():
        info = json.load(open(tp)).get("info", {})
        ms = info.get("model_stats") or {}
        spend += ms.get("instance_cost") or 0
        if "cost" in str(info.get("exit_status", "")):
            exits += 1
    return round(spend, 4), exits


def score(arm, preds_path):
    """Run the official harness; return the set of resolved instance ids."""
    run_id = f"exec100_{arm}"
    subprocess.run(["docker", "ps", "-q"], capture_output=True)
    subprocess.run("docker images --format '{{.ID}} {{.Repository}}' | grep sweb | "
                   "awk '{print $1}' | xargs -r docker rmi -f", shell=True, capture_output=True)
    subprocess.run([sys.executable, "-m", "swebench.harness.run_evaluation",
                    "--dataset_name", "princeton-nlp/SWE-bench_Verified",
                    "--predictions_path", preds_path,
                    "--cache_level", "none", "--max_workers", "2",
                    "--run_id", run_id], capture_output=True, text=True)
    # harness writes <model>.<run_id>.json in cwd
    resolved = set()
    for rp in glob.glob(os.path.join(ROOT, f"*{run_id}*.json")):
        try:
            d = json.load(open(rp))
        except Exception:
            continue
        r = d.get("resolved_ids") or d.get("resolved") or []
        if isinstance(r, list):
            resolved.update(r)
    return resolved, glob.glob(os.path.join(ROOT, f"*{run_id}*.json"))


def clopper_pearson(k, n, alpha=0.05):
    if n == 0:
        return (0.0, 0.0)
    lo = 0.0 if k == 0 else _beta_ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else _beta_ppf(1 - alpha / 2, k + 1, n - k)
    return (round(lo, 4), round(hi, 4))


def _beta_ppf(p, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if _beta_cdf(mid, a, b) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _beta_cdf(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    front = math.exp(a * math.log(x) + b * math.log(1 - x) - lbeta) / a
    f, c, num = 1.0, 1.0, 1.0
    m = 0
    while m < 300:
        num_term = (c * (b - m) * x) / ((a + 2 * m) * (a + 2 * m + 1)) if m else None
        if m == 0:
            f = 1.0
        m += 1
    # regularized incomplete beta via continued fraction (Lentz)
    return _betacf_cdf(x, a, b, front)


def _betacf_cdf(x, a, b, front):
    tiny = 1e-30
    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1)
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((a + m2 - 1) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delt = d * c
        h *= delt
        if abs(delt - 1.0) < 1e-12:
            break
    return front * h


def sign_test(wins, losses):
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, round(p, 5))


def main():
    log = lambda m: print(f"[finish {time.strftime('%H:%M:%S')}] {m}", flush=True)
    while True:
        b, p = arm_stats("baseline"), arm_stats("patched")
        log(f"waiting: baseline {b['genuine']}/100, patched {p['genuine']}/100")
        if b["genuine"] >= 100 and p["genuine"] >= 100:
            break
        time.sleep(120)
    log("200 genuine reached — freezing fleet")
    subprocess.run(["pkill", "-f", "exec100_controller.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "exec100_worker.sh"], capture_output=True)
    subprocess.run(["pkill", "-f", "exec100_arm_v2.sh"], capture_output=True)
    time.sleep(5)
    subprocess.run(["pkill", "-9", "-f", "sweagent run-batch"], capture_output=True)

    bpath, bpreds = assemble_preds("baseline")
    ppath, ppreds = assemble_preds("patched")
    log(f"assembled preds: baseline {len(bpreds)}, patched {len(ppreds)}")
    b_spend, b_exits = cost_and_exits("baseline")
    p_spend, p_exits = cost_and_exits("patched")

    log("scoring baseline arm ...")
    b_resolved, b_reports = score("baseline", bpath)
    log(f"baseline resolved {len(b_resolved)}")
    log("scoring patched arm ...")
    p_resolved, p_reports = score("patched", ppath)
    log(f"patched resolved {len(p_resolved)}")

    paired = [i for i in INSTANCES if i in bpreds and i in ppreds]
    wins = [i for i in paired if i in p_resolved and i not in b_resolved]
    losses = [i for i in paired if i in b_resolved and i not in p_resolved]
    ties = [i for i in paired if (i in p_resolved) == (i in b_resolved)]
    n_pair = len(paired)
    result = {
        "design": "Phase C funded execution arm (prereg-exec2 + amend1 + amend2)",
        "backbone": "gpt-5.6-luna", "per_instance_ceiling_usd": 3.0,
        "n_paired": n_pair,
        "baseline_resolved": len(b_resolved & set(paired)),
        "patched_resolved": len(p_resolved & set(paired)),
        "baseline_resolve_rate": round(len(b_resolved & set(paired)) / n_pair, 4) if n_pair else None,
        "patched_resolve_rate": round(len(p_resolved & set(paired)) / n_pair, 4) if n_pair else None,
        "paired_wins": sorted(wins), "paired_losses": sorted(losses),
        "n_wins": len(wins), "n_losses": len(losses), "n_ties": len(ties),
        "exact_sign_p": sign_test(len(wins), len(losses)),
        "patched_rate_CP95": clopper_pearson(len(p_resolved & set(paired)), n_pair),
        "baseline_rate_CP95": clopper_pearson(len(b_resolved & set(paired)), n_pair),
        "cost": {"baseline": {"spend_usd": b_spend, "cost_limit_exits": b_exits},
                 "patched": {"spend_usd": p_spend, "cost_limit_exits": p_exits}},
        "phase_c_rollout_spend_usd": round(b_spend + p_spend, 4),
        "report_files": [os.path.basename(x) for x in (b_reports + p_reports)],
    }
    if result["n_wins"] > result["n_losses"] and result["exact_sign_p"] < 0.05:
        branch = "POSITIVE: execution-rung gain (patched wins > losses, sign p<0.05)"
    elif result["n_losses"] > result["n_wins"] and result["exact_sign_p"] < 0.05:
        branch = "NEGATIVE: patched worse (losses > wins, sign p<0.05)"
    else:
        branch = "NULL: no significant paired execution-rung difference at this configuration"
    result["prereg_branch_fired"] = branch
    json.dump(result, open(os.path.join(ROOT, "exec100_result.json"), "w"), indent=1)
    log(f"BRANCH: {branch}")
    log(f"wrote exec100_result.json ({result['patched_resolved']} vs "
        f"{result['baseline_resolved']} of {n_pair}; {result['n_wins']}W/"
        f"{result['n_losses']}L; sign p={result['exact_sign_p']})")
    print("=== EXEC100-FINISH-COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
