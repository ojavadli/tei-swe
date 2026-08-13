# REVISION_LOG_13 — professor-grade figure redesign + visual QA

Figures rebuilt to a strong-2026-venue standard: scientifically truthful
encoding, high data-to-ink, honest denominator axes, zero label/mark collisions,
grayscale-legible. Figures regenerated from canonical JSON with in-generator
assertions. PDF passes `consistency_audit.py` (7 surfaces), `pdf_qa.py` (177
pages, no hard flags), and a grayscale legibility check. Build: 0 errors, 0
undefined refs, 0 overfull boxes > 5 pt, 177 pp.

## Figures
- **Fig. 1 (headline)** — removed the jittered individual-system clouds (those
  are Fig. 4); now the deployed mean trajectory ($0.606\!\to\!0.667\!\to\!0.684$,
  $n{=}26$) with a subtle dashed best-proposed ceiling, a focused honest y-range,
  and value labels placed off the markers (no collisions). The $+0.079$/13.0\%
  gain and the paired-contrast CIs (Table 8) moved to the caption.
- **Fig. 2 (ladder)** — replaced the canvas-wasting staircase with a compact
  horizontal evidence spectrum (rubric $\to$ blinded $\to$ static $\to$
  execution), increasing evidence strength and cost; reads as a taxonomy.
- **Fig. 3 (method)** — serious technical schematic: sentence case, square
  thin-bordered boxes, strict alignment, dark legible feedback arrows, accent
  only on the two Improve stages; the zero-rollout point is a light note.
- **Fig. 4 (population)** — unchanged intent: all 30 systems + mean; mean ends at
  the all-30 deployed final $0.675$ (not the $n{=}26$ headline), stated explicitly.
- **Fig. 5 (dimensions)** — dumbbell reordered by absolute deployed gain, largest
  first, so execution accuracy ($+0.105$) reads immediately as the top gain.
- **Fig. 6 (noise floor)** — replaced the count histogram (whose near-zero
  paraphrase pile-up distorted the axis) with **paired ECDFs**: paraphrase orbit
  ($n{=}90$) vs.\ shipped deltas ($n{=}30$), normalised to $0$--$1$, direct line
  labels; the distributional separation is unmistakable and denominator-free.
- **Fig. 7 (controls)** — recomposed as a $2\times2$ grid with honest,
  denominator-respecting axes and explicit per-panel units: (A) blinded, systems
  of 26; (B) sham, \% of votes 0--100; (C) budget-matched random as a
  Cleveland dot plot on a continuous rubric-delta axis including zero; (D)
  cross-provider at the **agent-majority** level (3 vs 6 of 10), the adverse
  direction fully visible. Vote counts / re-anchor detail moved to the caption.

Consistent semantics across all figures: TEI/deployed/real = accent solid/filled;
baseline/control/sham/random = gray hatched/open; search ceiling = gray dashed;
individual systems = light gray thin. One serif family; printed fonts ~7.5--10 pt.

## Canonical-value assertions (in make_figures.py)
Fig. 1 $n{=}26$ ends 0.684; Fig. 4 $n{=}30$ ends 0.675; ceiling 0.691 only where
labelled best-proposed; execution accuracy is the largest dimension gain; floor
arrays are $n{=}90$/$n{=}30$. Deployed gain is the canonical unrounded
$\approx+0.0786$, displayed $+0.079$, 13.0\% relative.

## Carry-over accounting
- Table 8 structural delta stays $+0.062$ (canonical unrounded 0.0615 under
  three-decimal rounding); not reverted to $+0.061$.
- Declared-dimension denominator $= 6000-17 = 5{,}983$ (0 lack scored dimensions,
  17 lack a machine-readable declared target); not changed to 5{,}994.
- Call ledger: 1{,}271 = original-study decomposition; 3{,}090 = full Phase-A/B
  model-call total; each scoped explicitly (never both "study total").
- Spend table notes that subtotals/grand total are computed from the unrounded
  ledger (per-row cents rounded independently); combined LLM subtotal \$53.66.

## QA
`pdf_qa.py` (rotation-invariant per-page font via $\min(w,h)$; main-vs-appendix
thresholds; raw-LaTeX, blank-page, and duplicate-caption checks): 177 pages,
**PASS**, no hard flags. Grayscale rasters of the evidence pages (Figs 1, 7)
confirm every distinction survives without colour. Zero Phase-C tokens in the PDF.
No new experiments; raw data and git history untouched.
