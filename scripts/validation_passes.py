#!/usr/bin/env python3
"""A5 + A3 + A2 measurement passes. Sequential, resumable, budget-metered.

A5  measured-noise MDE : k=5 rubric re-scores of the baseline on a fixed
    5-agent subsample -> per-probe test-retest sd -> mde_queries(measured sd).
A3  second judge       : gpt-5.6-terra rescore of a fixed-seed 150-candidate
    sample (correlation, sign agreement, optimism) + the blinded A/B protocol
    on a fixed 10-agent subsample.
A2  TRAJ rung          : score REAL in-repo trajectories (4 agents) on the four
    dimensions; report TRAJ-vs-PROXY baseline agreement.

Outputs: validation_passes.json (all raw records + summaries).
"""
import glob
import json
import os
import random
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
sys.path.insert(0, os.path.expanduser("~/Documents/STANFORD/tei-loop"))
import tei_pipeline as T
from tei_pipeline import call_json, BUDGET, DIMS, clamp_score, aggregate, evidence_pack
from tei_loop.gate import mde_queries

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
OUT = os.path.join(ROOT, "validation_passes.json")
TERRA = "gpt-5.6-terra"

state = json.load(open(OUT)) if os.path.isfile(OUT) else {}


def save():
    state["budget"] = BUDGET.as_dict()
    json.dump(state, open(OUT, "w"), indent=1)


def agent_dirs():
    return sorted(d for d in os.listdir(AGENTS) if os.path.isdir(os.path.join(AGENTS, d)))


def load_tei(d, name):
    return json.load(open(os.path.join(AGENTS, d, "tei", name)))


# ------------------------------------------------------------------ A5
def a5_measured_noise():
    if "a5" in state:
        print("A5 cached"); return
    rng = random.Random(0)
    subsample = [agent_dirs()[i] for i in (0, 6, 12, 18, 24)]  # fixed spread by rank
    recs = []
    for d in subsample:
        ob = load_tei(d, "onboarding.json")
        base = load_tei(d, "baseline_eval.json")
        probes = base["probes"]
        repeats = []
        for k in range(5):
            try:
                ev = T.baseline_eval(os.path.join(AGENTS, d), ob, probes)
            except Exception as e:
                print(f"  A5 {d} repeat {k}: {e}"); continue
            repeats.append({"aggregate": ev["aggregate"],
                            "probe_scores": ev.get("probe_scores", [])})
            print(f"  A5 {d} repeat {k}: agg={ev['aggregate']}", flush=True)
        # per-probe test-retest sd
        per_probe = {}
        for r in repeats:
            for p in r["probe_scores"]:
                if p.get("score") is not None:
                    per_probe.setdefault(p["instance_id"], []).append(p["score"])
        sds = [np.std(v, ddof=1) for v in per_probe.values() if len(v) >= 3]
        agg_sd = float(np.std([r["aggregate"] for r in repeats], ddof=1)) if len(repeats) >= 3 else None
        recs.append({"agent": d, "n_repeats": len(repeats),
                     "aggregates": [r["aggregate"] for r in repeats],
                     "aggregate_sd": agg_sd,
                     "per_probe_sds": [float(x) for x in sds]})
    pooled = float(np.sqrt(np.mean([x**2 for r in recs for x in r["per_probe_sds"]]))) \
        if any(r["per_probe_sds"] for r in recs) else None
    pooled_agg = float(np.sqrt(np.mean([r["aggregate_sd"]**2 for r in recs
                                        if r["aggregate_sd"] is not None])))
    mde4 = mde_queries(4, per_query_sd=pooled) if pooled is not None else None
    mde6 = mde_queries(6, per_query_sd=pooled) if pooled is not None else None
    state["a5"] = {"subsample": subsample, "records": recs,
                   "pooled_per_probe_sd": pooled, "pooled_aggregate_sd": pooled_agg,
                   "mde_measured_n4": mde4, "mde_measured_n6": mde6,
                   "mde_assumed_note": "original MDE used per_query_sd=0.15 (gate default)"}
    save()
    print(f"A5 done: pooled per-probe sd={pooled:.4f} agg sd={pooled_agg:.4f} "
          f"MDE(n=4)={mde4:.4f} MDE(n=6)={mde6:.4f}")


# ------------------------------------------------------------------ A3
def a3_second_judge():
    if "a3" not in state:
        state["a3"] = {}
    # --- 150-candidate rescore
    if "rescore" not in state["a3"]:
        rng = random.Random(0)
        pool = []
        for d in agent_dirs():
            cj = os.path.join(AGENTS, d, "tei", "candidates.jsonl")
            if not os.path.isfile(cj):
                continue
            for i, line in enumerate(open(cj)):
                pool.append((d, i))
        rng.shuffle(pool)
        sample = sorted(pool[:150])
        rows = []
        by_agent = {}
        for d, i in sample:
            by_agent.setdefault(d, []).append(i)
        for d, idxs in by_agent.items():
            cands = [json.loads(l) for l in open(os.path.join(AGENTS, d, "tei", "candidates.jsonl"))]
            base = load_tei(d, "baseline_eval.json")
            ob = load_tei(d, "onboarding.json")
            for i in idxs:
                c = cands[i]
                prompt = f"""Strictly score this candidate VERSION of a SWE-bench agent on the TEI rubric.

SYSTEM: {ob['system']} ({ob['resolve_rate']}% resolved on {ob['split']}). Phase: {c['phase']}.
BASELINE dimensions: {json.dumps(base.get('dimensions'))} (aggregate {base.get('aggregate')})
DIAGNOSED FAILURE MODES: {json.dumps([f.get('name') for f in base.get('failure_modes', [])])}

CANDIDATE: technique={c.get('technique')!r}, targets={c.get('target_failure_mode')!r},
change: {(str(c['patch_or_prompt'].get('replace'))[:300] if c['patch_or_prompt'].get('replace') else (c.get('why') or ''))[:300]}

Be strict and differentiating: most targeted changes move a dimension by ±0.01-0.06; some make
things worse and MUST score below baseline. No value may exceed 0.99.

JSON: {{"dimensions":{{"target_alignment":0.0,"reasoning_soundness":0.0,"execution_accuracy":0.0,"output_integrity":0.0}},"why":"one sentence"}}"""
                try:
                    v = call_json(prompt, max_out=1500, model=TERRA)
                except Exception as e:
                    print(f"  A3 {d}#{i}: {e}"); continue
                dims = {k: clamp_score(x) for k, x in (v.get("dimensions") or {}).items()}
                agg = aggregate(dims)
                if agg is None:
                    continue
                rows.append({"agent": d, "idx": i, "vid": c["version_id"],
                             "luna": c["aggregate"], "terra": agg,
                             "luna_delta": c["delta_vs_baseline"],
                             "terra_delta": round(agg - base["aggregate"], 4)})
            print(f"  A3 rescore {d}: {len(idxs)} candidates done "
                  f"[${BUDGET.conservative:.2f}]", flush=True)
        state["a3"]["rescore"] = rows
        save()
    rows = state["a3"]["rescore"]
    if rows and "summary" not in state["a3"]:
        from scipy import stats as st
        ld = np.array([r["luna_delta"] for r in rows])
        td = np.array([r["terra_delta"] for r in rows])
        pear = st.pearsonr(ld, td)
        spear = st.spearmanr(ld, td)
        sign_agree = float(np.mean(np.sign(np.round(ld, 6)) == np.sign(np.round(td, 6))))
        state["a3"]["summary"] = {
            "n": len(rows), "pearson_r": float(pear[0]), "pearson_p": float(pear[1]),
            "spearman_rho": float(spear[0]), "sign_agreement": sign_agree,
            "terra_optimism": float(np.mean(td >= -1e-12)),
            "luna_optimism_sample": float(np.mean(ld >= -1e-12))}
        save()
        print("A3 rescore summary:", json.dumps(state["a3"]["summary"], indent=1))

    # --- blinded protocol with terra on 10 fixed agents
    if "blind" not in state["a3"]:
        import blind_reval as BR
        rng = random.Random(1)
        patched = [d for d in agent_dirs()
                   if load_tei(d, "result.json").get("n_applied", 0) > 0]
        ten = sorted(rng.sample(patched, 10))
        out = []
        for d in ten:
            repo = os.path.join(AGENTS, d)
            ob = load_tei(d, "onboarding.json")
            files = BR.changed_files(repo, ob["repo_sha"])
            pairs = [(p, *e) for p in files if (e := BR.excerpt_pair(repo, ob["repo_sha"], p))]
            probes = [p["instance_id"] for p in load_tei(d, "baseline_eval.json").get("probes", [])][:4]
            votes = []
            for k in range(5):
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

Which version is more likely to resolve such issues correctly end-to-end? If too trivial or
ambiguous, say tie.

Return ONLY JSON: {{"better": "1" | "2" | "tie", "confidence": 0.0, "reason": "one sentence"}}"""
                try:
                    v = call_json(prompt, max_out=1200, model=TERRA)
                except Exception as e:
                    votes.append({"error": str(e)[:60]}); continue
                pick = str(v.get("better", "")).strip()
                votes.append({"vote": ("patched" if pick == ("1" if flip else "2") else
                                       "baseline" if pick in ("1", "2") else "tie")})
            pv = sum(1 for v in votes if v.get("vote") == "patched")
            bv = sum(1 for v in votes if v.get("vote") == "baseline")
            out.append({"agent": d, "patched": pv, "baseline": bv,
                        "tie": len(votes) - pv - bv})
            print(f"  A3 blind(terra) {d}: {pv}/{bv} [${BUDGET.conservative:.2f}]", flush=True)
        state["a3"]["blind"] = out
        save()
        maj = sum(1 for r in out if r["patched"] > r["baseline"] + r["tie"])
        print(f"A3 blinded(terra): strict-majority patched {maj}/10")


# ------------------------------------------------------------------ A2
def a2_traj():
    if "a2" in state:
        print("A2 cached"); return
    rng = random.Random(0)
    spec = {"08_sweagent": "**/*.traj", "16_darsagent": "**/*.traj",
            "27_agentless": "**/*.traj", "28_coder": "**/trajs/**/*"}
    recs = []
    for d, pat in spec.items():
        repo = os.path.join(AGENTS, d)
        ob = load_tei(d, "onboarding.json")
        base = load_tei(d, "baseline_eval.json")
        files = sorted(f for f in glob.glob(os.path.join(repo, pat), recursive=True)
                       if os.path.isfile(f) and "/.git/" not in f and "/tei/" not in f)
        rng.shuffle(files)
        picks = files[:6]
        traj_scores = []
        for f in picks:
            try:
                raw = open(f, errors="ignore").read()
            except OSError:
                continue
            excerpt = raw[:7000]
            prompt = f"""You are scoring ONE REAL recorded trajectory of the agent system {ob['system']}
(officially {ob['resolve_rate']}% resolved on SWE-bench {ob['split']}). This is an actual execution
trace from the project's own repository, not a description.

TRACE (head, file {os.path.basename(f)}):
{excerpt}

Score the four TEI dimensions for THIS trace, strictly (max 0.99): did it pursue the right target,
reason soundly, execute accurately, and produce well-formed output?

JSON: {{"dimensions":{{"target_alignment":0.0,"reasoning_soundness":0.0,"execution_accuracy":0.0,"output_integrity":0.0}},"why":"one sentence"}}"""
            try:
                v = call_json(prompt, max_out=1500)
            except Exception as e:
                print(f"  A2 {d} {os.path.basename(f)}: {e}"); continue
            dims = {k: clamp_score(x) for k, x in (v.get("dimensions") or {}).items()}
            agg = aggregate(dims)
            if agg is not None:
                traj_scores.append({"file": os.path.relpath(f, repo), "dims": dims,
                                    "aggregate": agg, "why": str(v.get("why", ""))[:200]})
        mean_traj = round(float(np.mean([t["aggregate"] for t in traj_scores])), 4) \
            if traj_scores else None
        recs.append({"agent": d, "n_traces_scored": len(traj_scores),
                     "traj_mean": mean_traj, "proxy_baseline": base["aggregate"],
                     "diff_traj_minus_proxy": (round(mean_traj - base["aggregate"], 4)
                                               if mean_traj is not None else None),
                     "traces": traj_scores, "label": "TRAJ"})
        print(f"  A2 {d}: {len(traj_scores)} traces, TRAJ mean={mean_traj} "
              f"vs PROXY {base['aggregate']} [${BUDGET.conservative:.2f}]", flush=True)
    state["a2"] = {"records": recs}
    save()


if __name__ == "__main__":
    a5_measured_noise()
    a3_second_judge()
    a2_traj()
    save()
    print("\nALL PASSES DONE. budget:", json.dumps(BUDGET.as_dict()))
