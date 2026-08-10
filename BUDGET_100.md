# Pre-registration: Phase B — the 100+100 extension with the Bayesian Credit Ledger

Registered 2026-08-10, BEFORE any Phase-B optimization call. Tagged `prereg-100` in the
public release repository so the timestamp is externally verifiable. The BCL
implementation (`scripts/bcl.py`, `scripts/tei_pipeline.py`, and the canonical
reference in the tei-bench harness's `teibench/optimizer.py`) is committed in the
same repository BEFORE this tag, per the B0 mandate.

## Design

All **30 agents** are extended to **100 structural + 100 prompt iterations** (200
scored versions per agent, ~6,000 total), **continuing the existing runs as a
prefix**: the 1,140 already-recorded versions keep their records and numbering
(`struct-01…`, `prompt-01…`); new versions continue the sequence; each agent's
repository continues from its current HEAD (patches remain cumulative, as in the
original run). Nothing recorded is deleted or re-scored.

**Identical instrument and gates (unchanged from the original v7 run):**
- Baseline anchors are REUSED verbatim from each agent's `tei/baseline_eval.json`
  (same dimensions, same per-probe scores, same fixed probe instances, seed 0).
- Judge, optimizer, and proposer model: `gpt-5.6-luna` exclusively
  (embeddings: `text-embedding-3-small`). Batch scoring prompt unchanged.
- Patch application unchanged: exact-match single-file replace, `ast.parse`
  compile pre-gate, single-file staging, one commit per applied version.
- Do-no-harm confirmation unchanged: `tei_loop.gate.verify_candidate` (sequential
  paired evaluation with exact futility bounds and Jeffreys Beta–Binomial
  posterior kills over discordant pairs) + `preflight_power` MDE diagnostics,
  run on the final best against the stored baseline probe scores.
- Noise floors are baseline-anchored and unchanged; they are NOT re-elicited.
- Per-version why-records are mandatory (every record carries a non-empty `why`).
- Score substrate remains PROXY and is labeled as such everywhere. The rubric
  rung's limits established by the within-study null control (R2f) stand; claims
  from this phase go through the same blinded/syntax/sham re-validation ladder.

## The Bayesian Credit Ledger (BCL) proposer — B0, frozen before this tag

Deterministic code (no LLM in the credit model), per **technique family ×
weakest-dimension cell** (10 families: verification-tests, patch-format,
localization, retrieval-context, prompt-structure, invariants-guards,
retry-recovery, output-contract, decomposition-planning, other):

- **L0 immutable store:** `tei/candidates.jsonl` stays lossless (all scores + whys).
- **L1 two-head credit model.** Reliability head: Jeffreys Beta(1/2,1/2)
  posterior on P(Δ>0), updated per scored candidate. Magnitude head: conjugate
  Normal posterior on the cell's mean Δ via Normal–Inverse-Gamma update with
  prior (μ₀=0, κ₀=1, α₀=2, β₀=2·var₀), **var₀ = 0.00043609** = the empirical
  global variance of `delta_vs_baseline` over the 1,140 prefix records
  (`_b100_plan.json`). **Shrinkage:** cells with n<3 borrow the technique-level
  aggregate posterior — Bayesian shrinkage (empirical-prior smoothing),
  explicitly NOT full hierarchical modeling (hierarchical partial pooling
  across agents is named future work).
- **Selection per proposal slot = Thompson sampling over both heads:** sample
  p̃ from the Beta head and δ̃ from the Normal head for each family; choose
  argmax of s = p̃ · max(δ̃, 0). Seeded RNG (seed = agent rank); every draw,
  the posterior snapshot hash, and the chosen family are logged per slot to
  `tei/ledger_log.jsonl`. Exploration is inherent to Thompson sampling; no
  epsilon hacks.
- **Bayesian surprise** computed at insertion for every scored candidate — the
  closed-form KL divergence (Beta KL + Normal KL) between the cell's posterior
  before and after the observation — stored on the record (`bayesian_surprise`).
- **L2 lessons (ACE-style):** at most 12 falsifiable bullets with evidence
  counters, updated by ONE small luna call per batch emitting DELTA OPERATIONS
  only (add / increment / refute / merge; ≤3 ops per batch); every operation
  appended to `tei/ledger_log.jsonl`.
- **L3 evidence-prioritized historical retrieval:** per proposal batch, 8
  why-records from L0 maximizing z(Bayesian surprise) + z(|Δ|) + z(embedding
  cosine relevance to the current diagnosis) + recency decay, subject to
  diversity via greedy submodular facility-location over why-record embeddings
  (`text-embedding-3-small`). No DPP, no PCA/JL — parsimony is a design
  principle. Selected version_ids logged per batch.
- **L4 recency:** last 4 records verbatim.
- **Rendering:** L1 posterior table (mean Δ, P(Δ>0), n per family) + L2 bullets
  + L3 selections + L4, hard budget ≤2,000 tokens, under the heading
  "HOW ALL PRIOR CANDIDATES SCORED AND WHY (posterior-guided)".
- **Generation contract:** the technique family for each slot is CHOSEN by
  L1's Thompson draw and stated to luna; luna instantiates the concrete fix
  (file/find/replace or prompt rewrite). The mathematics steers, the model writes.
- **Bootstrap:** at process start the ledger deterministically replays the
  agent's full `candidates.jsonl` prefix (assigned family where recorded,
  keyword-inferred family for prefix records).

Terminology (binding for all paper text): Bayesian **bandit** credit
assignment, not Gaussian-process "Bayesian optimization"; **retrieval**, not
attention; **shrinkage**, not hierarchical modeling.

## Mini-ablation (mandatory, preregistered here)

**5 fixed-seed agents** — `random.Random(42).sample(sorted(slugs), 5)` =
`01_livesweagent, 04_acoder, 09_agentscope, 21_swerl, 24_swefixer` — additionally
run a **parallel +30 structural / +30 prompt arm with the simple best-so-far
proposer (BCL off)**, i.e., the original run's proposer, from the SAME frozen
prefix. Isolation: a detached git worktree per agent under `ablation/<agent>/`,
created (with the prefix `candidates.jsonl`, `baseline_eval.json`, and prefix
counts frozen) BEFORE any main-arm extension call runs. Identical judge,
probes, gates, and apply pipeline.

**Pre-committed comparison:** best-so-far aggregate trajectories, BCL-on vs
BCL-off, over the first +30/+30 extension iterations past the shared prefix
(matched offsets, per agent); summarized by per-iteration mean best-so-far
difference and the end-of-window best delta, with an exact paired sign test
over the 5 agents at window end (exploratory; n=5). **All paper claims about
the BCL are scoped to this ablation's result, whatever it shows.** No
GEPA-superiority claim beyond it. Both arms are published.

## Execution plan

- 6 main shards by rank (01-05, 06-10, 11-15, 16-20, 21-25, 26-30), separate
  state files `_state100_[A-F].json`, plus one ablation shard
  (`_state100_abl.json`). Resumable: skip-if-exists by recounting each agent's
  `candidates.jsonl` per phase; a batch that fails 3× stops that agent's phase
  for the invocation and is retried on re-invocation; persistent shortfalls
  are reported plainly, never backfilled.
- Running spend is printed per batch, per agent, and per shard (exact token
  meters; dollars are the stated list-price assumption — nominal
  $1.25/$10.00 per Mtok in/out, embeddings $0.02/Mtok; the key lacks
  `api.usage.read`, so billed dollars cannot be read back).
- **No study-level cost cap** (owner authorization). The original run's $25
  cap and its scale-down ladder do NOT apply to this phase; extension targets
  are fixed at 100+100.
- Integrity: `verify_integrity.py` (lines-on-disk == n_versions) after
  completion; contaminated agents (if any) are discarded and re-run, as in the
  original protocol.

## Pre-committed reporting (published whatever they show)

1. Per-agent best-score-vs-iteration curves for both phases (all 30 agents,
   full 100+100 range), plus the 5-agent ablation curves (both arms).
2. B3 re-validation at the new bests: blinded A/B (luna, k=5, identical
   randomized narrative-free protocol) and the syntax audit for every agent
   whose shipped best changed; re-anchored sham-placebo comparison on a
   fixed-seed 10-agent subsample (`random.Random(21).sample(sorted(slugs), 10)`)
   at the new bests.
3. B4 full recompute from completed records only: the NEW canonical blinded
   sentence derived from the new recorded votes (same pre/post-repair
   convention), every table/macro/figure regenerated ("all 30 agents: 100
   structural + 100 prompt" — no "up to"), R2f and zero-applied analyses
   recomputed, REVISION_LOG_9 part B with exact spend, the curves, the
   ablation result, and 2–3 ledger-evolution exhibits (posterior table +
   lessons before/after) as a new appendix.

No interpretation branch is suppressed; negative or null ablation results are
reported with the same prominence as positive ones.
