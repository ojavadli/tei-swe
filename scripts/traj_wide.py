#!/usr/bin/env python3
"""P4.5 widened TRAJ rung: score REAL downloaded submission trajectories
(archive downloader output) for additional agents. Merges a2_wide into
validation_passes.json."""
import glob
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from tei_pipeline import call_json, BUDGET, clamp_score, aggregate

ROOT = os.path.expanduser("~/swebench-agents")
ARCH = os.path.join(ROOT, "archive")
rng = random.Random(0)


def main():
    dl = json.load(open(os.path.join(ROOT, "_traj_downloads.json")))
    vp = json.load(open(os.path.join(ROOT, "validation_passes.json")))
    recs = []
    for agent_dir, rel, n in dl:
        ob = json.load(open(os.path.join(ROOT, "agents", agent_dir, "tei", "onboarding.json")))
        base = json.load(open(os.path.join(ROOT, "agents", agent_dir, "tei", "baseline_eval.json")))
        files = sorted(glob.glob(os.path.join(ARCH, rel, "trajs", "**", "*"), recursive=True))
        files = [f for f in files if os.path.isfile(f) and os.path.getsize(f) > 2000]
        rng.shuffle(files)
        traj_scores = []
        for f in files[:6]:
            try:
                full = open(f, errors="ignore").read()
            except OSError:
                continue
            # extract the WORK, not the boilerplate head
            raw = None
            if f.endswith((".json", ".traj")) and full.lstrip()[:1] in "[{":
                try:
                    d = json.loads(full)
                    if isinstance(d, list):        # message array: take the last turns
                        msgs = [m for m in d if isinstance(m, dict) and m.get("role") != "system"]
                        parts = []
                        for m in msgs[-14:]:
                            parts.append(f"[{m.get('role','?')}] " + str(m.get('content', ''))[:900])
                        raw = "\n".join(parts)[-7000:]
                    elif isinstance(d, dict):      # live-swe-agent style: submission + tail
                        sub = str((d.get("info") or {}).get("submission", ""))[:2500]
                        traj = d.get("trajectory") or d.get("history") or []
                        tail = "\n".join(str(x)[:700] for x in traj[-8:])[-4000:]
                        raw = ("FINAL SUBMISSION DIFF:\n" + sub + "\n\nTRACE TAIL:\n" + tail)[:7000]
                except (json.JSONDecodeError, TypeError):
                    raw = None
            if raw is None or len(raw.strip()) < 400:
                raw = full[-7000:]                 # text logs: resolution happens at the END
            # always surface the final produced diff if one exists anywhere in the trace
            di = full.rfind("diff --git")
            if di != -1 and "diff --git" not in raw:
                raw = ("FINAL DIFF PRODUCED:\n" + full[di:di + 2500] + "\n\n") + raw[:4500]
            if len(raw.strip()) < 400:
                continue
            prompt = f"""You are scoring ONE REAL recorded trajectory of the agent system {ob['system']}
(officially {ob['resolve_rate']}% resolved on SWE-bench {ob['split']}). This is the actual submission
trace downloaded from the official leaderboard archive, not a description.

TRACE (head, file {os.path.basename(f)}):
{raw}

Score the four TEI dimensions for THIS trace, strictly (max 0.99): did it pursue the right target,
reason soundly, execute accurately, and produce well-formed output?

JSON: {{"dimensions":{{"target_alignment":0.0,"reasoning_soundness":0.0,"execution_accuracy":0.0,"output_integrity":0.0}},"why":"one sentence"}}"""
            try:
                v = call_json(prompt, max_out=1400)
            except Exception as e:
                print(f"  {agent_dir} {os.path.basename(f)}: {e}")
                continue
            agg = aggregate({k: clamp_score(x) for k, x in (v.get("dimensions") or {}).items()})
            if agg is not None:
                traj_scores.append({"file": os.path.join(rel, "trajs", os.path.basename(f)),
                                    "aggregate": agg, "why": str(v.get("why", ""))[:180]})
        mt = round(float(np.mean([t["aggregate"] for t in traj_scores])), 4) if traj_scores else None
        recs.append({"agent": agent_dir, "source": "archive submission download",
                     "n_traces_scored": len(traj_scores), "traj_mean": mt,
                     "proxy_baseline": base["aggregate"],
                     "diff_traj_minus_proxy": (round(mt - base["aggregate"], 4) if mt else None),
                     "traces": traj_scores})
        print(f"{agent_dir:26s} {len(traj_scores)} traces  TRAJ {mt} vs PROXY {base['aggregate']} "
              f"[${BUDGET.conservative:.2f}]", flush=True)
    vp["a2_wide"] = {"records": recs}
    vp.setdefault("budgets_extra", []).append(dict(BUDGET.as_dict(), pass_name="traj_wide"))
    json.dump(vp, open(os.path.join(ROOT, "validation_passes.json"), "w"), indent=1)
    print("merged a2_wide; budget:", json.dumps(BUDGET.as_dict()))


if __name__ == "__main__":
    main()
