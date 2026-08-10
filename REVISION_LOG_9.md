# REVISION_LOG_9 — Phase B: the 100+100 extension with the Bayesian Credit Ledger

Part B of the four-phase finalization (Phase A: layout/wording/staleness/consistency —
shipped earlier; Phases C/D appended below when executed). Everything here is derived
from recorded JSON; sources named per item.

## B0 — the Bayesian Credit Ledger (committed before the prereg tag)

`scripts/bcl.py` + wiring in `scripts/tei_pipeline.py` (`--extend`, `--ablation-arm`);
canonical reference port in tei-bench `teibench/optimizer.py`
(`optimize_v7(use_bcl=True)`, commit `ece3a0b`; parity-tested — identical Bayesian-surprise
sequences and Thompson draws vs `bcl.py` on fixed seeds). Release commits `f093125` (BCL)
then `73167f1` (prereg) — implementation strictly before the tag, per mandate.
Mechanism: L0 immutable candidates store; L1 two-head bandit credit (Jeffreys
Beta(1/2,1/2) reliability head + Normal–Inverse-Gamma magnitude head, var0=0.00043609
from the 1,140 prefix deltas; n<3 cells borrow the technique aggregate — shrinkage, not
hierarchical), Thompson selection per slot with posterior-hash draw logs; closed-form
Bayesian surprise stored on every record at insertion; L2 ≤12 falsifiable lessons via
delta ops only; L3 evidence-prioritized submodular facility-location retrieval over
`text-embedding-3-small` why-record embeddings; L4 recency; render ≤2,000 tokens under
"HOW ALL PRIOR CANDIDATES SCORED AND WHY (posterior-guided)".

## B1 — preregistration

`BUDGET_100.md`, tag **`prereg-100`** = `73167f17405e`, pushed and verified live on
github.com/ojavadli/tei-swe BEFORE any Phase-B call. Fixed in the tag: 100+100 targets
continuing the prefix; identical instrument and gates; BCL spec incl. seeds (Thompson
seed = agent rank; ablation selection seed 42; sham re-anchor subsample seed 21);
5-agent BCL-off +30/+30 worktree ablation with the pre-committed comparison; no
study-level cost cap; reporting published whatever it shows.

## B2 — the run (source: `_b2_spend.json`, `run100_*.log`, `_state100_*.json`)

- **30/30 agents at exactly 100 structural + 100 prompt = 6,000 scored versions
  (3,373 applied)**; ablation arm 5/5 complete. `verify_integrity.py`: all 30 pass
  (maintenance commits — `tei-v7 repair:`/`tei-v7 sham-cleanup:` — now excluded from
  the applied-count comparison; the flagged "+1"s were exactly those).
- Operational events, all disclosed: (i) one harness reaping event killed all 8
  background processes ~40 min in — relaunched fully detached
  (`scripts/spawn_detached.py`, double-fork+setsid); zero corrupt lines (per-record
  flush); loader now quarantines a truncated final line; (ii) shard D crashed once on
  luna emitting bare-string candidates — hardened (dict filter + widened retry set +
  per-agent exception isolation), release `9178a73`, run resumed losslessly.
- **Phase-B spend: $38.56 nominal / $77.11 conservative** for the run
  (+ $0.84 blinded re-runs + $0.15 sham re-anchor = **$39.54 nominal total**); exact
  cumulative token meters; 1,819 calls in sessions with recorded final counts (killed
  sessions' calls not individually recorded; their tokens/costs are in the meters).

## B3 — re-validation at the new bests

- **Sham-in-tei-v7 repair (pre-step):** the historical placebo arm's `git checkout -B`
  had failed on 7 agents, leaving the sham commit inside tei-v7 (and force-adding
  excluded `tei/` files on 4). Reverted (3 clean reverts; 4 surgical
  annotation-strips + `tei/` untrack); 0 annotations remain; ast-clean
  (`sham_revert_log.json`).
- **Syntax audit:** 46 changed `.py` files across 30 agents, **0 parse failures**
  (`syntax_audit_100.json`) — the contributed pre-gate ran inline throughout.
- **Blinded A/B re-run** (identical protocol, k=5, all 26 patched agents; 06/13/23
  re-voted because Phase B changed their diffs): **pre-repair 21/26 strict majorities
  (105/130 votes, 16 unanimous; 5 baseline majorities)**.
- **Defect audits (`defect_audit_100.json`, `nameerror_sweep_100.json`):** every
  baseline-majority agent objectively audited before any repair decision. 07/12/15 =
  preference-style verdicts (stand as honest losses); 19 = FALSE ALARM (an import
  *rename* whose removal half alone fit the 2,600-char excerpt window — instrument
  limitation, documented); **13_swerizzo = CONFIRMED import-time NameError** (proposer
  misspelled its own import alias; all five votes independently flagged it; a uniform
  module-level static sweep of all 30 agents confirmed it as the ONLY defect of its
  class). Repaired as `tei-v7 repair:` commit `c37579a`.
- **Adaptive retest** (13_swerizzo, k=5): 5/0 patched. **NEW CANONICAL SENTENCE**
  (`canonical_blinded_100.json`): "Pre-repair confirmatory result: 21/26 patched agents
  (105/130 votes); after repairing the one import-time defect (a misspelled alias
  flagged independently by all five of that agent's votes and confirmed by a uniform
  static sweep of all 30 agents as the only such defect), the adaptive retest shows
  22/26 strict majorities, 17 unanimous (110/130 votes), with 4 agents preferring the
  baseline."
- **Sham re-anchor** (preregistered seed 21, 10-agent subsample, identical protocol,
  branch-verification guard): **0/45 sham votes (share 0.0%), 0/9 majorities** — the
  placebo now draws essentially all ties at the new bests (`sham_rearm.json`).

## B4 — full recompute (all numbers macro-generated)

- Rubric (PROXY): applied-26 primary **0.606→0.675→0.690**; all-30 0.607→0.678→0.692;
  final−base **+0.0845** (CI [+0.0777,+0.0929], t=21.4, p=2.4e−19, d_z=3.92, 30W/0L);
  do-no-harm confirmation 30/30.
- R2f null control recomputed: final−base +0.083 zero-applied vs +0.085 patched
  (structural phase still inverts: +0.081 vs +0.069) — the rubric-rung conclusion
  stands unchanged.
- **Preregistered ablation fired its NULL branch**: BCL 2W/3L at the matched window end
  (exact sign p=1.000; mean per-iteration best-so-far difference +0.0053) — all ledger
  claims scoped to this; no GEPA-superiority claim (`curves_data.json`).
- New assets: `figures/curves_grid.png` (30-agent best-vs-iteration curves, both
  phases), `figures/ablation_curves.png`, `tables/ledger_exhibit.tex` +
  `ledger_exhibit.json` (posterior tables + lesson-op counts before/after, 3 agents);
  appendix "Ledger Evolution and Extension Curves" (`app:ledger`).
- Accounting: original-study totals frozen as published (fcc0ff1) — the merged blinded
  protocol overwrote `blind_reval.json`'s budget field, so the original constants are
  no longer file-derivable; Phase-B spend ledgered separately; combined LLM $53.66;
  grand $75.02 incl. both execution arms and the historical cross-provider bucket.
  The Phase-A grand-total row (which visually excluded two rows above it) is fixed:
  the grand total now sums every row above it.
- Paper rebuilt: **0 errors, 0 undefined references, 1 overfull box at 0.97pt**
  (<5pt threshold; pre-existing). Canonical sentence sites (abstract, intro, ladder,
  R2, comparison table, conclusion) all macro-composed; the original 30+30 campaign's
  24/26→26/26 record is retained as labeled history inside R2.
