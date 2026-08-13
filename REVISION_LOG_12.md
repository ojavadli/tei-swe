# REVISION_LOG_12 — final academic visual + typography + consistency pass

Numbers macro-generated from canonical JSON (`make_assets.py`); figures from
`make_figures.py` with in-generator canonical-value assertions. PDF passes
`consistency_audit.py` (7 surfaces), `pdf_qa.py` (all 176 pages), and a
grayscale legibility check. Build: 0 errors, 0 undefined refs, 0 overfull
boxes > 5 pt, 176 pp.

## Visual language — restrained academic, data-dominant
Replaced the dashboard/KPI aesthetic (giant numbers, teal, promo callouts) with
a restrained scientific style: white ground, charcoal/gray default, one muted
steel-blue accent for TEI used sparingly, standard marks (strip/line/staircase/
dumbbell/bar), printed fonts ~7.5--10 pt, grayscale-legible by tone **and**
shape/pattern. Every figure carries evidence (>~65\% data area); interpretation
is in the captions.

- **Fig. 1 Deployed improvement** (was a 3-panel KPI dashboard): now a
  per-system strip at the three stages + the deployed mean trajectory
  ($\swAppBase\!\to\!\swAppStruct\!\to\!\swAppFinal$, +0.079 / 13.0\%) + a faint
  best-proposed ceiling; $n{=}26$ population labelled. Table~6 renamed
  \emph{Study summary} as its numeric companion (no duplication).
- **Fig. 2 Validation ladder** (was a boxed \texttt{fbox} panel): a clean
  four-rung staircase (rubric $\to$ blinded $\to$ static $\to$ execution),
  increasing evidence strength and cost.
- **Fig. 3 How TEI works**: muted flow, accent only on the two IMPROVE stages;
  the zero-executed-rollout point is a one-line note, not a promo box.
- **Fig. 4 Population trajectories**: all 30 systems + mean; population stated
  and the mean correctly ends at the \emph{all-30} deployed final (0.675), not
  the $n{=}26$ headline (0.684) --- the four flat lines are the zero-patch
  systems.
- **Fig. 5 Dimensions**: muted dumbbell (open baseline / filled deployed).
- **Fig. 6 Validation and controls**: four-panel bars in one grammar; the
  cross-provider judge is shown honestly (does not reproduce; four
  baseline-preferring systems shown).

## Comparator: one artifact, not two
Deleted the infographic comparator figure. The single main-text comparison is
now a compact **Yes / no / n.r.** characteristics matrix (Table~10): 12
characteristics $\times$ 6 methods, TEI bold only where a primary source
supports a lead, n.r.\ never encoded as no, and \emph{no} cross-substrate
performance comparison (end-task percentages omitted as incommensurable).

## Readability
- **Table 5** (per-agent, 14 columns) is now a full-page **landscape**
  (\texttt{sidewaystable}) at footnotesize --- every column legible, no microtext.
- **Tables 3--4** (spend / costs): wrapping \texttt{p\{\}} description columns
  and shortened labels; render at true footnotesize without shrink-to-fit.
- **Appendix curves** (30 mini-panels): split into two **landscape** full pages
  (agents 1--15 / 16--30), each panel readable; the mini-ablation moved off its
  near-empty page.
- Removed the per-agent \texttt{\textbackslash clearpage} in the appendix
  (agents flow with a rule separator): eliminated stray blank pages and tightened
  the appendix (186 $\to$ 176 pp).

## Links / typography
Bright-blue hyperlinks $\to$ \texttt{hidelinks} (print-black); \texttt{\textbackslash urlstyle\{same\}}
so URLs inherit body type; author emails de-monospaced. \texttt{monospace}
reserved for code / paths / identifiers.

## Consistency (recomputed / verified from canonical artifacts)
- **Table 8 rounding**: the deployed gains now derive from the same live
  unrounded $n{=}26$ means as the contrasts table, under one \texttt{.3f} policy
  --- +0.062 / +0.017 / +0.079 agree everywhere (was +0.061 vs +0.062).
- **Call ledger**: one decomposition --- frozen original study \$14.12 / 1{,}271
  calls; whole-study totals \swLLMCombined{} / \swCallsCanon{} calls; each
  accounting universe labelled precisely.
- **Cost**: canonical \$53.66 LLM subtotal (not the round-then-sum \$53.67);
  grand total \$75.02.
- **Declared-dimension denominator**: verified from the census --- 0 of 6{,}000
  versions lack scored dimensions, 17 lack a machine-readable declared target;
  denominator $= 6000-17 = 5{,}983$ (footnote count corrected from ``6'').
- Figures assert canonical values at generation (n=26 final 0.684, all-30 final
  0.675, ceiling 0.691, +13.0\%).

## Automated QA
Added `pdf_qa.py`: per-page median glyph height (rotation-invariant via
$\min(w,h)$, so landscape tables are not false-flagged), with separate main-text
vs.\ appendix thresholds; raw-LaTeX-fragment scan; text-coverage / blank-page
detection; duplicate-caption detection. Result over 176 pages: **PASS**, no hard
flags. Grayscale rasters of the evidence pages confirm all distinctions survive
without colour.

## Integrity
Zero Phase-C 200-rollout content: every banned token occurs 0 times in the PDF.
No new experiments; no raw outcomes modified; Phase-C raw files and git history
untouched on disk.
