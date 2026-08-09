# TEI v7 applied to 30 SWE-bench leaderboard agents

Frozen set: 30 systems from the official SWE-bench submission archive
(`SWE-bench/experiments` @ `2f15350cd32becc4569e0d826361048555b605c0`, accessed 2026-08-08), Lite + Verified.
Methodology: `tei-bench` @ `626b455ff662c185f17396411a839759d663c8c9`, `tei-loop` @ `e02931354d5e311cac20cd0c43b0fef04cb8ffa8`.
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
| 1 | live-SWE-agent + Claude 4.5 Opus m | verified | 79.2 | execution_accuracy | 0.8475 | 0.885 | 0.89 | +0.0425 | 30/30 | 24 | ✓ | yes | exceeds | PROXY |
| 2 | Sonar Foundation Agent + Claude 4. | verified | 79.2 | execution_accuracy | 0.8075 | 0.86 | 0.8625 | +0.055 | 30/30 | 0 | ✓ | yes | exceeds | PROXY |
| 3 | TRAE + Doubao-Seed-Code | verified | 78.8 | execution_accuracy | 0.835 | 0.885 | 0.89 | +0.055 | 30/30 | 39 | ✓ | yes | exceeds | PROXY |
| 4 | ACoder | verified | 76.4 | execution_accuracy | 0.775 | 0.845 | 0.845 | +0.07 | 30/30 | 0 | ✓ | yes | exceeds | PROXY |
| 5 | JoyCode + Claude 4 Sonnet + GPT-4. | verified | 74.6 | execution_accuracy | 0.8275 | 0.8675 | 0.885 | +0.0575 | 30/30 | 46 | ✓ | yes | exceeds | PROXY |
| 6 | Lingxi-v1.5_claude-4-sonnet-202505 | verified | 74.6 | execution_accuracy | 0.7675 | 0.805 | 0.835 | +0.0675 | 18/18 | 24 | ✓ | yes | exceeds | PROXY |
| 7 | Moatless Tools + Claude 4 Sonnet | verified | 70.8 | execution_accuracy | 0.795 | 0.8425 | 0.85 | +0.055 | 18/18 | 3 | ✓ | yes | exceeds | PROXY |
| 8 | SWE-agent + Claude 4 Sonnet | verified | 66.6 | execution_accuracy | 0.7075 | 0.765 | 0.7675 | +0.06 | 18/18 | 22 | ✓ | yes | exceeds | PROXY |
| 9 | AgentScope | verified | 63.4 | execution_accuracy | 0.6375 | 0.705 | 0.715 | +0.0775 | 18/18 | 20 | ✓ | yes | exceeds | PROXY |
| 10 | EntroPO + R2E + Qwen3-Coder-30B-A3 | verified | 60.4 | execution_accuracy | 0.63 | 0.6825 | 0.69 | +0.06 | 18/18 | 17 | ✓ | yes | exceeds | PROXY |
| 11 | ExpeRepair-v1.0 + Claude 4 Sonnet | lite | 60.33 | execution_accuracy | 0.705 | 0.775 | 0.775 | +0.07 | 18/18 | 13 | ✓ | yes | exceeds | PROXY |
| 12 | KGCompass + Claude 4 Sonnet (20250 | lite | 58.33 | execution_accuracy | 0.6275 | 0.6675 | 0.69 | +0.0625 | 30/30 | 28 | ✓ | yes | exceeds | PROXY |
| 13 | SWE-Rizzo | verified | 56.6 | execution_accuracy | 0.725 | 0.7975 | 0.815 | +0.09 | 30/30 | 51 | ✓ | yes | exceeds | PROXY |
| 14 | Agentless-1.5 + Claude-3.5 Sonnet  | verified | 50.8 | execution_accuracy | 0.59 | 0.665 | 0.665 | +0.075 | 18/18 | 16 | ✓ | yes | exceeds | PROXY |
| 15 | Composio SWE-Kit (2024-10-25) | verified | 48.6 | execution_accuracy | 0.6275 | 0.665 | 0.685 | +0.0575 | 12/12 | 18 | ✓ | yes | exceeds | PROXY |
| 16 | DARS Agent | lite | 47.0 | execution_accuracy | 0.58 | 0.6275 | 0.645 | +0.065 | 12/12 | 18 | ✓ | yes | exceeds | PROXY |
| 17 | CodeShellAgent + Gemini 2.0 Flash  | verified | 44.2 | execution_accuracy | 0.4975 | 0.5425 | 0.5525 | +0.055 | 12/12 | 0 | ✓ | yes | exceeds | PROXY |
| 18 | CodeFuse-CGM | lite | 44.0 | execution_accuracy | 0.5925 | 0.6425 | 0.6425 | +0.05 | 12/12 | 22 | ✓ | yes | exceeds | PROXY |
| 19 | Agentless Lite + O3 Mini (20250214 | verified | 42.4 | execution_accuracy | 0.5775 | 0.63 | 0.6375 | +0.06 | 12/12 | 17 | ✓ | yes | exceeds | PROXY |
| 20 | SWE-Exp | verified | 42.0 | execution_accuracy | 0.5175 | 0.57 | 0.5875 | +0.07 | 12/12 | 10 | ✓ | yes | exceeds | PROXY |
| 21 | SWE-RL (Llama3-SWE-RL-70B + Agentl | verified | 41.2 | execution_accuracy | 0.555 | 0.6075 | 0.6075 | +0.0525 | 12/12 | 10 | ✓ | yes | exceeds | PROXY |
| 22 | OrcaLoca + Agentless-1.5 + Claude- | lite | 41.0 | execution_accuracy | 0.6125 | 0.66 | 0.6775 | +0.065 | 30/30 | 49 | ✓ | yes | exceeds | PROXY |
| 23 | Patched.Codes Patchwork | lite | 37.0 | execution_accuracy | 0.5475 | 0.5925 | 0.6175 | +0.07 | 30/30 | 27 | ✓ | yes | exceeds | PROXY |
| 24 | SWE-Fixer (Qwen2.5-7b retriever +  | verified | 32.8 | execution_accuracy | 0.48 | 0.55 | 0.55 | +0.07 | 18/18 | 13 | ✓ | yes | exceeds | PROXY |
| 25 | CodeShellTester + GPT 4o (2024-05- | lite | 31.33 | execution_accuracy | 0.3925 | 0.4525 | 0.4525 | +0.06 | 12/12 | 0 | ✓ | yes | exceeds | PROXY |
| 26 | Aegis - o3-mini_1.0 | lite | 30.33 | execution_accuracy | 0.435 | 0.4825 | 0.4975 | +0.0625 | 12/12 | 19 | ✓ | yes | exceeds | PROXY |
| 27 | Agentless + RepoGraph + GPT-4o | lite | 29.67 | execution_accuracy | 0.44 | 0.48 | 0.5025 | +0.0625 | 12/12 | 8 | ✓ | yes | exceeds | PROXY |
| 28 | CodeR + GPT 4 (1106) | lite | 28.33 | execution_accuracy | 0.4625 | 0.5025 | 0.5075 | +0.045 | 12/12 | 12 | ✓ | yes | exceeds | PROXY |
| 29 | Aider + GPT 4o & Claude 3 Opus | lite | 26.33 | execution_accuracy | 0.415 | 0.445 | 0.465 | +0.05 | 12/12 | 9 | ✓ | yes | exceeds | PROXY |
| 30 | RAG + Claude 3 Opus | verified | 7.0 | execution_accuracy | 0.21 | 0.26 | 0.2725 | +0.0625 | 12/12 | 12 | ✓ | yes | exceeds | PROXY |

## Three limitations that bound every number above

1. **All PROXY, zero VERIFIED.** No agent was executed; see below.
2. **Every shipped delta sits below the power preflight's MDE.** With 6 paired
   probe queries the gate's own `preflight_power` reports that only changes of roughly
   the MDE magnitude are distinguishable from judge noise, and the observed deltas are
   an order of magnitude smaller. The do-no-harm gate accepting a candidate therefore
   means "not harmful," **not** "measurably better."
3. **The judge barely discriminates.** 1072 of 1140 scored versions (94.0%) landed at or above their agent's baseline. A proposal process that almost never makes anything worse is not credible; it indicates the rubric judge is optimistic and weakly discriminating, so the ranking within a phase carries more signal than the absolute deltas. Undirected paraphrases were also
   scored, and the `vs noise floor` column reports whether each shipped gain clears the
   best lucky rewording. Treat any "exceeds" as weak evidence given (2).

## Spend

| | |
|---|---|
| LLM calls | 568 |
| Input tokens | 727,172 |
| Output tokens | 953,779 |
| Cost (nominal assumption) | $10.45 |
| Cost (conservative bound, cap enforced here) | $20.89 |
| Cap | $25.00 |

Billed cost could not be read back: the key lacks the `api.usage.read` scope. Tokens
are exact; dollars are an assumption, stated in PROVENANCE.md.

Scale-downs: iters 30->18 (projected $6.01) before 06_lingxi; iters 30->18 (projected $7.46) before 14_agentless15; iters 18->12 (projected $5.83) before 15_composioswekit; iters 30->18 (projected $8.10) before 24_swefixer; iters 18->12 (projected $6.04) before 25_codeshelltester; iters 30->18 (projected $10.23) before 13_swerizzo

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

All 30 agents completed.

## Reproduction

See PROVENANCE.md § Reproduction.

_Generated 2026-08-08._

## Addendum (post-run): blinded A/B validation + compile audit

Two follow-up measurements sharpen the PROXY verdict (`blind_reval.json`, `syntax_audit.json`):

1. **Blinded A/B (bias-controlled judge):** for the 26 agents with applied patches, the judge was shown real before/after code states, randomized order, no narrative, 5 repeats each. Result: **patched preferred 118/130 votes; 24/26 agents strict majority** (sign p≈1e-5); **2 agents (JoyCode 0/5, Agentless 1/5) blinded-preferred the ORIGINAL** — the judge cited visibly malformed strings/indentation in the patched files.
2. **Compile audit (deterministic, no LLM):** `ast.parse` over all 41 changed `.py` files: **6 files in 5 agents (JoyCode×2, Moatless Tools, SWE-Exp, OrcaLoca, Agentless) have syntax errors introduced by applied patches.** All 5 agents had been scored "+improved" by the narrative rubric.

Corrected reading: most applied changes carry bias-controlled (still non-executed) evidence of genuine improvement; five agents were provably damaged; the rubric pass detected none of the damage. Verdict hierarchy demonstrated: rubric < blinded A/B < compile check < execution.

### Post-repair update (final)

All 6 syntax-broken files were repaired as recorded `tei-v7 repair:` commits (intent of the
original patches preserved); the full `ast.parse` audit is now **0 errors across 41 changed
files (30/30 agents clean)**, and the blinded A/B was re-run for the 5 affected agents — each
flipped to 5/0 for the patched state. **Post-repair blinded record: 26/26 patched agents,
128/130 votes.** A zero-cost compile pre-gate (`tei_loop.gate.static_pregate`, also inline in
`tei_pipeline.py`) now rejects parse-breaking candidates before any judge call, closing this
failure mode permanently. Additional validation: measured judge test-retest noise sd=0.037 →
measured MDE₈₀=0.074 (n=4), which 2/30 rubric deltas clear individually (per-agent statistical
weight therefore rests on the blinded votes); second model within the same GPT-5.6 family (gpt-5.6-terra): 87.3% sign
agreement, ρ=0.50, optimism 88.7% (family-general), blinded subsample 8/10 agents / 40/50
votes; TRAJ rung: 19 real recorded trajectories across 4 systems, mean |TRAJ−PROXY| baseline
difference 0.024 (max 0.132). See `validation_passes.json`, `blind_reval.json`,
`REVISION_LOG.md`, and the revised paper.
