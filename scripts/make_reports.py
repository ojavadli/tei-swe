#!/usr/bin/env python3
"""Write PROVENANCE.md, per-agent tei/REPORT.md, and the master TEI_SWEBENCH_REPORT.md."""
import json
import os
from datetime import date

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")

ARCHIVE_SHA = "2f15350cd32becc4569e0d826361048555b605c0"
ACCESS_DATE = "2026-08-08"
TEIBENCH_SHA = "626b455ff662c185f17396411a839759d663c8c9"
TEILOOP_SHA = "e02931354d5e311cac20cd0c43b0fef04cb8ffa8"


def total_budget():
    """Sum every process's metered spend: the run was executed as several shards
    plus a post-pass, so a single state file under-counts it."""
    import glob
    tot = {"calls": 0, "input_tokens": 0, "output_tokens": 0,
           "cost_nominal_usd": 0.0, "cost_conservative_usd": 0.0, "scale_downs": []}
    for f in sorted(glob.glob(os.path.join(ROOT, "_state*.json")) +
                    glob.glob(os.path.join(ROOT, "_run_state.json")) +
                    glob.glob(os.path.join(ROOT, "_post_pass_budget.json")) +
                    glob.glob(os.path.join(ROOT, "blind_reval.json")) +
                    glob.glob(os.path.join(ROOT, "validation_passes.json")) +
                    glob.glob(os.path.join(ROOT, "sham_arm.json")) +
                    glob.glob(os.path.join(ROOT, "sham_rearm.json")) +
                    glob.glob(os.path.join(ROOT, "random_arm.json"))):
        try:
            d = json.load(open(f))
        except (OSError, json.JSONDecodeError):
            continue
        b = d.get("budget", d)
        if not isinstance(b, dict) or "calls" not in b:
            continue
        for k in ("calls", "input_tokens", "output_tokens"):
            tot[k] += b.get(k, 0) or 0
        for k in ("cost_nominal_usd", "cost_conservative_usd"):
            tot[k] += b.get(k, 0) or 0
        tot["scale_downs"] += b.get("scale_downs") or []
        if os.path.basename(f) == "validation_passes.json":
            for xb in (d.get("budgets_extra") or []):
                for k in ("calls", "input_tokens", "output_tokens"):
                    tot[k] += xb.get(k, 0) or 0
                for k in ("cost_nominal_usd", "cost_conservative_usd"):
                    tot[k] += xb.get(k, 0) or 0
    extra = None
    try:
        extra = json.load(open(os.path.join(ROOT, "extra_budgets.json")))
    except (OSError, json.JSONDecodeError):
        pass
    for b in (extra or {}).get("passes", []):
        for k in ("calls", "input_tokens", "output_tokens"):
            tot[k] += b.get(k, 0) or 0
        for k in ("cost_nominal_usd", "cost_conservative_usd"):
            tot[k] += b.get(k, 0) or 0
    tot["cost_nominal_usd"] = round(tot["cost_nominal_usd"], 4)
    tot["cost_conservative_usd"] = round(tot["cost_conservative_usd"], 4)
    return tot


def load(p, default=None):
    try:
        return json.load(open(p))
    except (OSError, json.JSONDecodeError):
        return default


def agent_records():
    out = []
    for d in sorted(os.listdir(AGENTS)):
        p = os.path.join(AGENTS, d, "tei")
        if not os.path.isdir(p):
            continue
        ob = load(os.path.join(p, "onboarding.json"))
        if not ob:
            continue
        base = load(os.path.join(p, "baseline_eval.json"))
        res = load(os.path.join(p, "result.json"))
        cands = []
        cp = os.path.join(p, "candidates.jsonl")
        if os.path.isfile(cp):
            for line in open(cp):
                try:
                    cands.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        out.append({"dir": d, "ob": ob, "base": base, "res": res, "cands": cands})
    return out


def write_provenance(recs):
    manifest = load(os.path.join(ROOT, "manifest.json"), [])
    budget = total_budget()
    rows = "\n".join(
        f"| {m['rank']} | {m['system']} | {m['split']} | {m['resolve_rate']} | "
        f"{m['resolved']} | [{m['repo_url'].split('github.com/')[-1]}]({m['repo_url']}) | "
        f"`{m['repo_sha'][:10]}` |" for m in manifest)
    scale = budget.get("scale_downs") or []
    scale_txt = "\n".join(f"- {s}" for s in scale) or "- none: the run completed at the full 30+30 setting"
    txt = f"""# PROVENANCE

## Source

We use 30 agent systems drawn from the official SWE-bench leaderboard submission
archive (SWE-bench/experiments), covering the SWE-bench Lite and SWE-bench Verified
splits, frozen at commit {ARCHIVE_SHA}, accessed {ACCESS_DATE}.

- Archive: https://github.com/SWE-bench/experiments @ `{ARCHIVE_SHA}`
- Benchmark: SWE-bench, Jimenez et al., ICLR 2024.
- Resolve rates use the archive's own denominators (`analysis/get_leaderboard.py`):
  lite = 300, verified = 500 instances.

## Selection rule (pre-registered; applied unchanged)

1. Parse every submission folder in `evaluation/lite/` and `evaluation/verified/`.
2. Deduplicate into unique systems: lowercase the entry name, strip parentheticals
   and model/version suffixes, collapse whitespace. Keep the **highest-scoring**
   submission per system.
3. Keep only systems whose **kept** submission names a `github.com` repository in its
   own metadata (`info.site` / `info.report`). No URL was ever guessed or inferred
   from a third-party page.
4. Verify every candidate URL with `git ls-remote` before counting it.
5. Rank survivors by resolve rate descending.

## Counts

| Stage | Count |
|---|---|
| Submissions parsed (lite 84 + verified 134) | 218 |
| Unique systems after dedupe | 101 |
| Systems whose kept submission names a GitHub repo | 30 |
| Repo URLs verified with `git ls-remote` | 30 / 30 |
| **Final set** | **30** |

### Why 30 and not 31

The target was 31. The strict filter yielded 30. The pre-approved remedy — widening
the universe with `evaluation/multilingual/` — was executed and added **zero**
sourceable systems: 0 of its 13 entries name a repository in metadata, and all 13 are
the same system (mini-swe-agent v2.0.0a0) evaluated across different models, so they
are one system under the dedupe rule, not thirteen.

One alternative reading of step 3 was identified and **rejected**: if a system were
allowed to qualify when *any* of its submissions names a repo (rather than the kept
top-scoring one), `autocoderover` and `patchpilot` would enter, giving 32 and allowing
a top-31. That reading was discovered only after observing that the strict rule gives
30, so adopting it would have been selection tuned to the desired count. The owner
elected to report the honest 30. **The set is not padded.**

Two systems in the set (`codeshellagent`, `codeshelltester`) share one repository
(WisdomShell/codeshell); they are distinct leaderboard entries under the name-based
dedupe rule and are kept as such.

## Recorded trajectories: not available

`SWE-bench/experiments` ships aggregate `results/` only. There are **zero** `logs/`
and **zero** `trajs/` directories in the archive at this commit. The archive README
states those assets live in an S3 bucket requiring an AWS account; anonymous listing
returns HTTP 403. Per owner directive no AWS access was used, so **no recorded
trajectory was read for any agent**, and `recorded_trajectories_available = 0` in
every `tei/onboarding.json`. What *is* available and was used: the archive's
per-instance resolved/unresolved outcomes for each system.

## TEI v7 application

Methodology applied as deployed and frozen; nothing in it was reimplemented here.

- Harness: `tei-bench` @ `{TEIBENCH_SHA}` (`teibench/gate.py`, `optimize_v7`).
- Product gate: `tei-loop` @ `{TEILOOP_SHA}` (`tei_loop/gate.py` —
  `verify_candidate` do-no-harm confirmation, `preflight_power` MDE preflight).

Per agent, on a local `tei-v7` branch (never pushed): baseline evaluation → 30
structural-fix versions → select the best → 30 prompt-optimization versions on top →
best overall, confirmed with `tei_loop.gate.verify_candidate` before being declared
the winner, with the paraphrase noise floor and MDE recorded.

### Score substrate — read this before citing any number

- **VERIFIED** — real execution outcomes on a fixed paired instance set.
- **PROXY** — `gpt-5.6-luna` rubric scores of a version against the diagnosed failure
  modes and fixed probe instances.

Every score in this study is **PROXY**. No agent in the set could be executed
end-to-end. Deciding whether a patch *resolves* an instance requires SWE-bench's
evaluation harness, which imports `docker_build` / `docker_utils` / `dockerfiles`;
**Docker is not installed on this machine** (`which docker` → not found), so there is
no ground-truth resolved/unresolved signal to score against. Independently, the
mission's own Tier-A definition excludes Docker orchestration and GPUs, and four
linked repositories contain no runnable source at all. PROXY scores measure judged
plausibility of a change, **not** resolve-rate improvement. They must not be read as,
or converted into, SWE-bench gains.

Every shipped delta in this study is **below the MDE** reported by the gate's own
`preflight_power` at the probe count used (4-6 paired queries). The gains do clear the
paraphrase noise floor (rewordings scored +0.000 to +0.0075), but "clears the floor and
does no harm" is the strongest claim the evidence supports.

All experiment LLM calls used OpenAI `gpt-5.6-luna` exclusively (judge, structural-fix
generation, prompt optimization). No fallback model was used at any point.

### Budget and scale-down

Hard cap $25. This API key lacks the `api.usage.read` scope, so billed cost could not
be read back; tokens are metered exactly and priced under a stated assumption
(nominal $1.25/$10.00 per Mtok; a 2x conservative bound of $2.50/$20.00 enforces the
cap). Recorded spend: **{budget.get('calls', 0)} calls, {budget.get('input_tokens', 0):,} input +
{budget.get('output_tokens', 0):,} output tokens, ${budget.get('cost_nominal_usd', 0):.2f} nominal /
${budget.get('cost_conservative_usd', 0):.2f} conservative.**

Scale-downs applied (pre-registered order: fewer instances per evaluation first, then
fewer iterations per phase, applied uniformly to all remaining agents):

{scale_txt}

## The final 30

| Rank | System | Split | Resolve % | Resolved | Repo | Cloned SHA |
|---|---|---|---|---|---|---|
{rows}

## Reproduction

```bash
mkdir -p ~/swebench-agents && cd ~/swebench-agents
git clone --depth 1 https://github.com/SWE-bench/experiments.git archive
git -C archive checkout {ARCHIVE_SHA}
python3 build_manifest.py --splits lite verified   # parse + dedupe + extract repo URLs
python3 stage_clones.py                            # shallow-clone every sourceable repo
python3 finalize_manifest.py                       # rank, manifest.csv/json, onboarding
python3 find_prompt_surface.py                     # content-based prompt-surface scan
export OPENAI_API_KEY=...                          # ask the owner; never commit it
python3 tei_pipeline.py --struct-iters 30 --prompt-iters 30 --batch 6 --probes 6
python3 make_reports.py
```

_Generated {date.today().isoformat()}._
"""
    open(os.path.join(ROOT, "PROVENANCE.md"), "w").write(txt)


def write_agent_report(r):
    ob, base, res, cands = r["ob"], r["base"], r["res"], r["cands"]
    p = os.path.join(AGENTS, r["dir"], "tei", "REPORT.md")
    if not base:
        open(p, "w").write(f"# TEI v7 — {ob['system']}\n\nNot evaluated in this run.\n")
        return
    sc = sorted(cands, key=lambda c: -c["aggregate"])[:3]
    why = "\n".join(
        f"{i+1}. **{c['version_id']} — {c.get('technique')}** (targets _{c.get('target_failure_mode')}_, "
        f"score {c['aggregate']}, Δ {c['delta_vs_baseline']:+}, {c['decision']})\n"
        f"   > {c.get('why')}\n" for i, c in enumerate(sc)) or "_no versions recorded_"
    fm = "\n".join(f"- **{f.get('name')}** — {f.get('description')} "
                   f"(evidence: {', '.join(f.get('evidence_instance_ids') or []) or 'n/a'})"
                   for f in base.get("failure_modes", [])) or "_none recorded_"
    conf = (res or {}).get("confirmation", {})
    nf = (res or {}).get("noise_floor") or {}
    ns = sum(1 for c in cands if c["phase"] == "structural")
    npm = sum(1 for c in cands if c["phase"] == "prompt")
    na = sum(1 for c in cands if c["decision"] == "applied")
    txt = f"""# TEI v7 — {ob['system']}

**Rank {ob['rank']} of 30** · SWE-bench {ob['split']} · officially resolved
{ob['resolved']} ({ob['resolve_rate']}%) · repo [{ob['repo_url']}]({ob['repo_url']}) @ `{ob['repo_sha'][:10]}`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> ({(res or {}).get('runnability', {}).get('reason', 'n/a')}). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **{base.get('aggregate')}** |
| Best structural version ({(res or {}).get('best_structural_id')}) | **{(res or {}).get('best_structural')}** |
| Best final version ({(res or {}).get('best_final_id')}) | **{(res or {}).get('best_final')}** |
| Shipped | **{(res or {}).get('shipped')}** |

Baseline dimensions: `{json.dumps(base.get('dimensions'))}`
Weakest dimension: **{base.get('weakest_dimension')}**

## Diagnosed failure modes

{fm}

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | {ns} | {sum(1 for c in cands if c['phase'] == 'structural' and c['decision'] == 'applied')} |
| B — prompt | {npm} | {sum(1 for c in cands if c['phase'] == 'prompt' and c['decision'] == 'applied')} |
| **total** | **{len(cands)}** | **{na}** |

All {len(cands)} versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{json.dumps(conf, indent=2)}
```

Paraphrase noise floor: `{json.dumps(nf)}`
{"" if not nf.get("noise_floor") else
 f"The best shipped gain is {'ABOVE' if ((res or {}).get('best_final', 0) - base.get('aggregate', 0)) > nf['noise_floor'] else 'WITHIN'} the paraphrase noise floor."}

## Top 3 why-records

{why}

## Trajectory availability

{ob.get('trajectory_note')}
"""
    open(p, "w").write(txt)


def write_diagnosis(r):
    ob, base = r["ob"], r["base"]
    p = os.path.join(AGENTS, r["dir"], "tei", "DIAGNOSIS.md")
    if not base:
        open(p, "w").write(f"# Diagnosis — {ob['system']}\n\nNot evaluated in this run.\n")
        return
    dims = base.get("dimensions") or {}
    dim_rows = "\n".join(f"| {k} | {v} |" for k, v in dims.items())
    fm = "\n".join(
        f"### {i+1}. {f.get('name')}\n\n{f.get('description')}\n\n"
        f"_Evidence instances:_ {', '.join(f.get('evidence_instance_ids') or []) or 'n/a'}\n"
        for i, f in enumerate(base.get("failure_modes", []))) or "_none recorded_"
    probes = "\n".join(f"| `{p_['instance_id']}` | {p_.get('archive_outcome', '?')} | {p_.get('score')} |"
                       for p_ in (base.get("probes") or [])
                       for p_ in [dict(p_, **{"score": next(
                           (s["score"] for s in base.get("probe_scores", [])
                            if s.get("instance_id") == p_["instance_id"]), None)})])
    open(p, "w").write(f"""# Diagnosis — {ob['system']}

Rank {ob['rank']}/30 · SWE-bench {ob['split']} · {ob['resolved']} resolved ({ob['resolve_rate']}%)
Repo `{ob['repo_url']}` @ `{ob['repo_sha'][:10]}`

> Substrate: **{base.get('score_label', 'PROXY')}** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
{dim_rows}

**Aggregate {base.get('aggregate')} · weakest dimension: {base.get('weakest_dimension')}**

{base.get('why', '')}

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
{probes}

## Recurring failure modes

{fm}

## Evidence availability

- Recorded trajectories from the archive: **{ob.get('recorded_trajectories_available', 0)}**
  ({ob.get('trajectory_note', '')})
- Trajectories committed in this agent's own repo: **{ob.get('in_repo_trajectory_files', 0)}**
- Prompt-surface files identified: **{ob.get('n_prompt_surface_files', 0)}**
""")


def write_master(recs):
    done = [r for r in recs if r["res"]]
    b = total_budget()
    rows = []
    for r in sorted(done, key=lambda r: r["ob"]["rank"]):
        res, base, ob = r["res"], r["base"], r["ob"]
        ns = sum(1 for c in r["cands"] if c["phase"] == "structural")
        npm = sum(1 for c in r["cands"] if c["phase"] == "prompt")
        na = sum(1 for c in r["cands"] if c["decision"] == "applied")
        delta = round(res["best_final"] - res["baseline"], 4)
        floor = (res.get("noise_floor") or {}).get("noise_floor")
        rows.append(
            f"| {ob['rank']} | {ob['system'][:34]} | {ob['split']} | {ob['resolve_rate']} | "
            f"{base.get('weakest_dimension', '')} | {res['baseline']} | {res['best_structural']} | "
            f"{res['best_final']} | {delta:+} | {ns}/{npm} | {na} | "
            f"{'✓' if res.get('confirmation', {}).get('accept') else '✗'} | "
            f"{'yes' if res.get('below_mde') else 'no' if res.get('below_mde') is not None else '?'} | "
            f"{(res.get('gain_vs_noise_floor') or '?').replace('_noise_floor', '')} | "
            f"{res['score_label']} |")
    skipped = [r for r in recs if not r["res"]]
    NQ = (done[0]["res"].get("confirmation", {}).get("n_queries", "n") if done else "n")
    n_below = sum(1 for r in done if r["res"].get("below_mde"))
    all_c = [c for r in done for c in r["cands"]]
    above = sum(1 for r in done for c in r["cands"] if c["aggregate"] >= r["res"]["baseline"])
    pct = round(100 * above / len(all_c), 1) if all_c else 0
    JUDGE_STAT = (f"{above} of {len(all_c)} scored versions ({pct}%) landed at or above their "
                  f"agent's baseline. A proposal process that almost never makes anything worse "
                  f"is not credible; it indicates the rubric judge is optimistic and weakly "
                  f"discriminating, so the ranking within a phase carries more signal than the "
                  f"absolute deltas.")
    txt = f"""# TEI v7 applied to 30 SWE-bench leaderboard agents

Frozen set: 30 systems from the official SWE-bench submission archive
(`SWE-bench/experiments` @ `{ARCHIVE_SHA}`, accessed {ACCESS_DATE}), Lite + Verified.
Methodology: `tei-bench` @ `{TEIBENCH_SHA}`, `tei-loop` @ `{TEILOOP_SHA}`.
All experiment LLM calls: OpenAI **gpt-5.6-luna** (no fallback).

> ## Read this first
> **Every score in this table is PROXY**, not a measured SWE-bench outcome. No agent
> was executed: deciding whether a patch resolves an instance needs SWE-bench's Docker
> harness, and **Docker is not installed on this machine**; four linked repos also ship
> no runnable source. PROXY = `gpt-5.6-luna` rubric scores of a version against that
> agent's diagnosed failure modes and fixed probe instances.
> **A PROXY delta is not a resolve-rate gain.** Zero agents reached VERIFIED.
>
> **Every Δ in this table is below the MDE** (`Δ below MDE` column is `yes` for all 30):
> at 4-6 paired probe queries the gate's own power preflight says only changes an order
> of magnitude larger are distinguishable from judge noise. The `✓` in *Confirmed* means
> the do-no-harm gate found no evidence of harm — **not** that the gain is real.

## Master table

| Rank | System | Split | Resolve % | Weakest dim | Baseline | Best struct | Best final | Δ | Struct/Prompt versions | Applied commits | Confirmed | Δ below MDE | vs noise floor | Label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Three limitations that bound every number above

1. **All PROXY, zero VERIFIED.** No agent was executed; see below.
2. **Every shipped delta sits below the power preflight's MDE.** With {NQ} paired
   probe queries the gate's own `preflight_power` reports that only changes of roughly
   the MDE magnitude are distinguishable from judge noise, and the observed deltas are
   an order of magnitude smaller. The do-no-harm gate accepting a candidate therefore
   means "not harmful," **not** "measurably better."
3. **The judge barely discriminates.** {JUDGE_STAT} Undirected paraphrases were also
   scored, and the `vs noise floor` column reports whether each shipped gain clears the
   best lucky rewording. Treat any "exceeds" as weak evidence given (2).

## Spend

| | |
|---|---|
| LLM calls | {b.get('calls', 0)} |
| Input tokens | {b.get('input_tokens', 0):,} |
| Output tokens | {b.get('output_tokens', 0):,} |
| Cost (nominal assumption) | ${b.get('cost_nominal_usd', 0):.2f} |
| Cost (conservative bound, cap enforced here) | ${b.get('cost_conservative_usd', 0):.2f} |
| Cap | $25.00 |

Billed cost could not be read back: the key lacks the `api.usage.read` scope. Tokens
are exact; dollars are an assumption, stated in PROVENANCE.md.

Scale-downs: {("; ".join(b.get('scale_downs') or [])) or "none"}

## What the diagnosis found across 30 real systems

See each agent's `tei/DIAGNOSIS`-equivalent section in `agents/<rank>_<slug>/tei/REPORT.md`
and the full per-version why-records in `tei/candidates.jsonl`.

## What could not be verified, and why

1. **No recorded trajectories.** The archive ships aggregate results only; `logs/` and
   `trajs/` require an AWS account (archive README; anonymous S3 listing returns 403).
   No trajectory was read, so no trajectory was scored.
2. **No end-to-end execution — 0 VERIFIED, established by test, not assumed.**
   A static screen over all 30 repos left 3 with no blocker (`08_sweagent`,
   `12_kgcompass`, `29_aider`; full table in `tier_a_assessment.txt`). Tier A still
   fails for a reason upstream of any of them: **Docker is not installed on this
   machine** (`which docker` → not found), and SWE-bench's own evaluation harness
   imports `docker_build` / `docker_utils` / `dockerfiles` to decide whether a patch
   resolves an instance. Without it there is no ground-truth resolved/unresolved
   signal to score, so no paired VERIFIED measurement is possible here. The mission's
   own Tier-A definition also excludes Docker orchestration, so these agents are out
   of Tier A by definition as well. The remaining 27 fail earlier: 22 have no obvious
   entry point, 11 require Docker, 6 require GPU/local weights, 4 ship no source.
3. **Four repos contain no source code at all** (`livesweagent`, `sonarfoundationagent`,
   `acoder`, `coder` — README/config/report assets only), so Phase A had nothing to
   patch for them; recorded rather than worked around.

{("**Agents not completed this run:** " + ", ".join(r["dir"] for r in skipped)) if skipped else "All 30 agents completed."}

## Reproduction

See PROVENANCE.md § Reproduction.

_Generated {date.today().isoformat()}._
"""
    open(os.path.join(ROOT, "TEI_SWEBENCH_REPORT.md"), "w").write(txt)


if __name__ == "__main__":
    recs = agent_records()
    write_provenance(recs)
    for r in recs:
        write_agent_report(r)
        write_diagnosis(r)
    write_master(recs)
    done = sum(1 for r in recs if r["res"])
    print(f"wrote PROVENANCE.md, {len(recs)} agent reports, TEI_SWEBENCH_REPORT.md "
          f"({done}/{len(recs)} agents have results)")
