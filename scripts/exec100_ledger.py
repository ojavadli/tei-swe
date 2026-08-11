#!/usr/bin/env python3
"""Phase-C execution ledger (prereg-exec2-amend1): progress counts ONLY genuine
rollouts — trajectories with successful model usage (api_calls >= 1 AND input
and output tokens > 0). A .traj file's existence proves nothing.

Usage: exec100_ledger.py [--clean-stubs ARMDIR]
  default: print the running status ledger (JSON line + human line)
  --clean-stubs: remove instance dirs whose traj is missing, zero-usage, or
                 exit_error, so the retry round re-runs them
"""
import glob
import json
import os
import sys

ROOT = os.path.expanduser("~/swebench-agents")


def classify(tp):
    try:
        t = json.load(open(tp))
    except Exception:
        return "unparseable", {}
    info = t.get("info", {})
    ms = info.get("model_stats") or {}
    ok = (ms.get("api_calls") or 0) >= 1 and (ms.get("tokens_sent") or 0) > 0 \
        and (ms.get("tokens_received") or 0) > 0
    if not ok:
        return "stub", ms
    if str(info.get("exit_status", "")) == "exit_error":
        return "genuine_but_errored", ms
    return "genuine", ms


def arm_stats(arm):
    d = os.path.join(ROOT, f"_exec100_{arm}")
    out = {"genuine": 0, "genuine_but_errored": 0, "stub": 0, "unparseable": 0,
           "api_calls": 0, "tokens_in": 0, "tokens_out": 0, "spend_usd": 0.0,
           "cost_cap_exits": 0}
    for tp in glob.glob(os.path.join(d, "*", "*.traj")):
        kind, ms = classify(tp)
        out[kind] += 1
        out["api_calls"] += ms.get("api_calls") or 0
        out["tokens_in"] += ms.get("tokens_sent") or 0
        out["tokens_out"] += ms.get("tokens_received") or 0
        out["spend_usd"] += ms.get("instance_cost") or 0
        try:
            ex = json.load(open(tp)).get("info", {}).get("exit_status", "")
            if "cost" in str(ex):
                out["cost_cap_exits"] += 1
        except Exception:
            pass
    out["spend_usd"] = round(out["spend_usd"], 2)
    return out


def scored_pairs():
    n = 0
    for arm in ("patched", "baseline"):
        for rp in glob.glob(os.path.join(ROOT, f"*exec100f*_{arm}.json")) + \
                glob.glob(os.path.join(ROOT, f"_exec100_{arm}.exec100_{arm}.json")):
            try:
                json.load(open(rp))
                n += 1
            except Exception:
                pass
    return n


def clean_stubs(armdir):
    removed = []
    for inst_dir in glob.glob(os.path.join(armdir, "*/")):
        trajs = glob.glob(os.path.join(inst_dir, "*.traj"))
        if not trajs:
            removed.append(os.path.basename(inst_dir.rstrip("/")))
            import shutil
            shutil.rmtree(inst_dir)
            continue
        kind, _ = classify(trajs[0])
        if kind in ("stub", "unparseable", "genuine_but_errored"):
            removed.append(os.path.basename(inst_dir.rstrip("/")))
            import shutil
            shutil.rmtree(inst_dir)
    print(f"cleaned {len(removed)} non-genuine instance dirs in {armdir}")
    return removed


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--clean-stubs":
        clean_stubs(sys.argv[2])
        return
    p, b = arm_stats("patched"), arm_stats("baseline")
    total_genuine = p["genuine"] + b["genuine"]
    ledger = {"genuine_completed_rollouts": f"{total_genuine}/200",
              "patched": p, "baseline": b,
              "harness_report_files": scored_pairs()}
    print(json.dumps(ledger))
    print(f"LEDGER: genuine {total_genuine}/200 (patched {p['genuine']}, baseline "
          f"{b['genuine']}) | stubs p:{p['stub'] + p['genuine_but_errored']} "
          f"b:{b['stub'] + b['genuine_but_errored']} | luna calls "
          f"{p['api_calls'] + b['api_calls']} | tokens "
          f"{p['tokens_in'] + b['tokens_in']}/{p['tokens_out'] + b['tokens_out']} | "
          f"spend ${p['spend_usd'] + b['spend_usd']:.2f} | cost-cap exits "
              f"p:{p['cost_cap_exits']} b:{b['cost_cap_exits']}", flush=True)


if __name__ == "__main__":
    main()
