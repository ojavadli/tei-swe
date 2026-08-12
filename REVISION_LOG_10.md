# REVISION_LOG_10 — main-paper rebuild (scope + correctness)

All numbers macro-generated from canonical JSON via `make_assets.py`; the
compiled PDF passes `consistency_audit.py` over 7 surfaces.

## Scope change
- Large-scale execution validation was moved **outside the scope of the present
  manuscript**; it will be studied in a separate dedicated paper. The paper now
  reads as if end-task execution at large scale is simply future work. No raw
  data was deleted, no git history rewritten, no tags removed; those artifacts
  simply cease to be evidence, cost, or narrative belonging to this paper.
- Kept as this paper's execution evidence: the $n{=}6$ micro-arm and the
  preregistered $n{=}36$ \texttt{gpt-4o-mini} paired arm (tag `prereg-exec`),
  both null.

## Primary result correction — applied vs. proposed
- The headline is now the **deployed/applied** artifact (best change actually
  committed to each branch), not the best merely-proposed candidate. Recomputed
  from raw `candidates.jsonl`:
  - Deployed ($n{=}26$ patched): Default $0.606 \to$ Structural $0.667 \to$
    Final $0.684$; absolute $+0.079$, **relative $+13.0\%$** (\textsc{rubric}).
  - Best-proposed search ceiling reported separately: Final $0.690$,
    **$+14.0\%$**.
  - Zero-patch systems (no commit) now show **exactly $+0.000$** deployed gain,
    sharpening the within-study null control.

## Numerical/table corrections (all verified from records)
- **MDE:** stale "3 of 30" replaced by the recomputed count of deployed deltas
  clearing the measured MDE $0.074$: **15/30** (proposed-delta count 21/30
  noted). Four MDE narrative macros rewritten.
- **Technique table:** the false "$n\le4$ / maximum 4 of 6{,}000" disclaimer
  removed; the table now reports **technique families** over all 6{,}000
  records (largest family $n{=}1{,}557$), descriptive only, no causal claim.
- **Zero-patch proposals:** "120" corrected to the true count — 200 null
  proposals per zero-patch system, **800** total.
- **Table 8 (dimensions):** baseline and final columns now on the **same
  $n{=}26$** population (final uses the best applied version); caption states it.
- **Prefix vs. final:** limitations no longer say "the full budget is 60";
  it now distinguishes the initial capped prefix from the preregistered
  extension that brought all 30 to the same 100$+$100 (=200) endpoint.
- **Algorithm 1:** iteration bound corrected $k=1..30 \to k=1..100$, with the
  prefix/extension provenance noted.
- **Cost reconciliation (Phase-C $=\$0$):** LLM optimization subtotal
  **\$53.66**; retained grand total **\$75.02**; cost/system **\$1.79**,
  cost/candidate **\$0.009**, cost/applied **\$0.016**, candidates/\$ **111.8**.

## Typesetting/production
- Fixed raw-LaTeX rendering in the spend table (`\{}\$25`, literal
  `\texttt{...}`), the missing p-value operator ("p0.001" $\to$ "$p{=}0.001$"),
  and dead Appendix-D fields (`+0.0000 (below MDE: no)`, empty `()`); the
  latter now shows the real per-agent deployed delta and a non-empty
  parenthetical only when present.
- Rebuilt: **0 errors, 0 undefined references, 0 overfull boxes $>5$pt**, no
  raw-LaTeX escaping visible in the PDF.

## Blinded language
- "every patched agent" removed; the paper states **22 of 26** patched systems
  received a strict blinded majority (110/130 votes, 17 unanimous, 4
  baseline-majority).

## 2026 comparator rebuild (primary sources only)
- Each comparator resolved to a primary source before inclusion: GEPA
  (arXiv:2507.19457, ICLR 2026 Oral), MIPROv2 (arXiv:2406.11695, 2024, legacy),
  Maestro (arXiv:2509.04642), ACE (arXiv:2510.04618, ICLR 2026), HiveMind
  (arXiv:2512.06432); additional resolved methods MASS (arXiv:2502.02533) and
  MASPOB (arXiv:2603.02630) recorded in `comparison_qualification.md`. No new
  comparator experiments were run; the comparison is a literature audit only.
  TEI's distinguishing, verified axes: 30 third-party-system coverage,
  zero-executed-rollout selection, and bias-controlled validation
  (placebo + blinded + random) — none of which the audited papers report.

## Title / abstract
- Title changed to a delivered-capability form (dropping "self-improving"):
  "TEI-SWE: Low-Cost Population-Scale Optimization and Blinded Validation of 30
  Third-Party Agent Systems."
- Abstract rebuilt to 224 words, value-first, leading with the deployed
  $+13.0\%$ gain, the zero-executed-rollout selection architecture, blinded
  22/26, and the controls; zero Phase-C content.
