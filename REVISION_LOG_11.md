# REVISION_LOG_11 — value-forward visual rebuild, deployed-value consistency, typography

All numbers macro-generated from canonical JSON via `make_assets.py`;
figures from `make_figures.py`; the compiled PDF passes `consistency_audit.py`
(7 surfaces) and `check_typography.py`. Build: 0 errors, 0 undefined refs,
0 overfull boxes > 5 pt, 185 pp.

## Visual package (5 figures, one visual language)
One accent (teal), one neutral gray, one secondary (amber); grayscale-safe by
colour **and** shape/pattern; text-width; explicit fonts (labels/ticks/legend
6.5–9.5 pt); every number carries its substrate qualifier (no marketing).
- **Fig. 1 — TEI-SWE at a glance** (headline, p.2): scale/coverage, deployed
  improvement slope (0.606→0.667→0.684, +13.0%, dashed best-proposed ceiling
  secondary and labelled), bias-controlled confirmation (22/26 blinded).
- **Fig. 3 — How TEI works** (method): TARGET→EVALUATE→IMPROVE structure→
  GATE→SELECT→IMPROVE prompt→deployed, feedback loop (why-records→Bayesian
  credit ledger→next proposal), validation ladder, and the callout
  "0 executed benchmark rollouts used as the Phase-A/B selection signal."
- **Fig. 7 — Why the improvement is credible** (validation): blinded A/B,
  sham placebo, budget-matched random, and the honest cross-provider panel
  (does **not** reproduce; four baseline-preferring systems shown, not hidden).
- **Fig. 8 — Where TEI differs from 2026 optimizers**: primary-source dot
  matrix; n.r. (open amber diamond) is never encoded as "no"; teal = verified
  TEI advantage only.
- **Fig. 5 — dimension dumbbell** (replaces the old 4-row dims table): all four
  anchored rubric dimensions rise; execution accuracy has the largest gain
  (+0.105).

## Result consistency — DEPLOYED is primary everywhere (Task 0)
The core stage vectors now read the best-**applied** (committed) candidate per
agent from the canonical recompute; the best-**proposed** search ceiling is a
separate, explicitly-labelled series. Recomputed on deployed values:
- Stage contrasts (Table 8, $n{=}26$): Struct$-$base $+0.062$, Final$-$struct
  $+0.017$, Final$-$base $+0.079$; W/L/T $26/0/0$, $19/0/7$, $26/0/0$.
- Per-agent Table 5: Struct/Final/$\Delta$ are deployed; a new **Final$^{\ast}$**
  column carries the best-proposed ceiling (zero-patch systems now visibly
  deploy nothing, $\Delta=+0.000$, with their rubric ceiling shown for contrast).
- Slope figure, MDE-clear count, and dimension figure all on deployed values.
- **MDE:** the measured-MDE clear count is the deployed **15/30** everywhere
  (the proposed 21/30 no longer leaks into the delivered-performance narrative).
- **Null control (Table 9)** recomputed and re-framed on the anchored rubric:
  the four zero-patch systems' best rubric candidate (never deployed) moves the
  rubric $+0.081$ (structural) — *exceeding* the $+0.062$ the 26 patched
  systems' deployed artifacts gain (inversion $\approx+0.019$) — so rubric
  movement alone is not evidence of a deployable improvement.

## Typography (root cause + system fix)
Root cause: narrow tables were **enlarged** to text width by `\resizebox`,
while figures were geometrically reduced. Fix: every `\resizebox{\linewidth}`
on a table replaced by `\begin{adjustbox}{max width=\linewidth,center}`
(shrink-only — a narrow table keeps its natural size, never grows past body
prose); figures generated at physical text-width with explicit fonts. Added
`check_typography.py` (per-page median glyph-height vs. body prose; catches
resizebox-enlargement and microscopic blocks): **PASS** (body 10 pt; no page
median exceeds body prose; no oversized table type; no microscopic block).

## Carry-over fixes
- "preference survives on every patched agent" and "unanimous-or-near-unanimous
  on every patched agent" → **22 of 26** strict blinded majorities (17
  unanimous, 4 prefer the baseline), fixed at both occurrences.
- Appendix technique caption: dropped the false "maximum 4 of 6{,}000" / "means
  on $n\le4$"; the table reports technique **families** (largest $n{=}1{,}557$),
  descriptive only.
- **Canonical call ledger:** the frozen original-study decomposition is
  \$14.12 / 1{,}271 calls; the Phase-B extension adds 1{,}819 calls; the
  whole-study totals are now reported as **\$53.66 LLM subtotal / 3{,}090
  calls** (grand \$75.02). The original-study 1{,}271/\$14.12 is no longer
  labelled the "total."
- Table 4 labels corrected: "LLM cost per system, all passes" (\$1.79) and
  "Retained grand total per system (LLM + execution arms + cross-provider)"
  (\$2.50); judge-call split labelled "original-study decomposition."
- Footnote denominator: the targeting denominator is **5{,}983 = 6{,}000 − 17**
  versions lacking a machine-readable declared target dimension (0 versions lack
  scored dimensions); the stale "6" skip count was computed from the data.
- Limitations: execution scope stated as the retained $n{=}6$ micro-arm **and**
  the preregistered $n{=}36$ paired arm (both null), not "the micro-arm" only.
- Title/intro no longer say "self-improving" (systems are third-party):
  "population-scale optimization loop."
- Algorithm 1 endpoint $k=1..100$ (100 structural + 100 prompt); prefix/extension
  provenance preserved.

## Integrity
Manuscript and compiled PDF contain **zero** Phase-C 200-rollout content: every
banned token (prereg-exec2, 47/100, 50/100, Phase C/3, 200 rollout/genuine,
exec100, livelock, scoring\_instrument, 100-pair) occurs **0** times in the PDF.
No new experiments were run; no raw study outcomes were modified; raw Phase-C
files and git history remain on disk untouched for the separate future paper.
