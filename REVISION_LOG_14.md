# REVISION_LOG_14 — vector-native figure pipeline

Root cause of the "pasted-in" look, verified with `pdfimages -list`: every main
figure was an embedded raster PNG (233--332 PPI) sitting beside crisp Latin
Modern body text. Fixed the pipeline, then the figures.

## Pipeline
The manuscript compiles with **tectonic (XeTeX)** using **Latin Modern**; there
is no standalone `xelatex`/`pdflatex` on this machine, so matplotlib's PGF
backend (which must shell out to a LaTeX binary to measure text) is unavailable.
Two vector routes were used instead:

- **Data plots (Figs 1, 4, 5, 6, 7)** — new shared module `figstyle.py` loads the
  manuscript's own `lmroman*.otf` (from the tectonic bundle cache) into
  matplotlib and emits **true vector PDF** (`\includegraphics{...pdf}`). Figure
  text is now Latin Modern vector glyphs, the same family as the body.
  Verification: `pdfimages -list` shows **0 raster images on pages 1--20**;
  `pdffonts` shows LMRoman subsets embedded in the figures.
- **Schematics (Figs 2 ladder, 3 method)** — rebuilt **natively in TikZ** inside
  the manuscript (`positioning`, `arrows.meta`, `calc`; one node style, one arrow
  style, one accent). They compile as document-native graphics with document
  fonts.

## Figure redesigns
- **Fig 1** — plain regular-weight black value labels (no bold accent); focused
  honest $y$-range; ceiling thin light-gray dashed and secondary; gain and paired
  CIs in the caption; no individual-system clouds (those are Fig 4).
- **Fig 2** — categorical TikZ evidence hierarchy; spatial order encodes evidence
  strength ONLY. The false "increasing marginal cost" implication is removed
  (no cost axis; caption states cost is non-monotonic --- the static rung is free).
- **Fig 3** — compact TikZ systems schematic; sentence case; accent only on the
  two Improve stages; the zero-rollout statement lives in the caption.
- **Fig 4** — all 30 systems; mean ends at the all-30 deployed final $0.675$
  (not the $n{=}26$ headline); population stated.
- **Fig 5** — dumbbell ordered by absolute gain (execution accuracy $+0.105$ top).
- **Fig 6** — restored the distribution-shape view as **two stacked histograms**
  sharing one $x$-axis and bin grid (paraphrase $n{=}90$ to its true max; shipped
  $n{=}30$ to its true max), different $y$-scales labelled, no mass hidden; the
  ECDF moved to the appendix (Fig.~\ref{fig:floorecdf}) as the cumulative view.
- **Fig 7** — 2$\times$2 with denominator-respecting axes and explicit units
  (A systems/26, B \%/100, C Cleveland dot plot on a continuous rubric-delta axis
  incl.\ zero, D agent majorities 3 vs 6 of 10); adverse cross-provider direction
  fully visible; vote totals in the caption.

## Text consistency
- `p0.001` (missing operator) $\to$ **$p<0.001$** in both the narrative macro and
  the discussion (the agent-level sign test is $22$ vs $4$ of $26$, true
  $p\approx0.0005<0.001$).
- §6 no longer calls 1{,}271 "the study total": **1{,}271 = original-study
  decomposition**, **3{,}090 = full Phase-A/B model-call total**, scoped explicitly.
- Unchanged by design: declared-dimension denominator $5{,}983 = 6000-17$; Table 8
  structural delta $+0.062$ from the canonical unrounded mean $0.0615$.

## Verification
`pdfimages` (0 raster on main figure pages), `pdffonts` (LMRoman in figures),
`pdf_qa.py` (176 pages, PASS), `consistency_audit.py` (7 surfaces, PASS),
grayscale rasters of the evidence pages (all distinctions survive), Phase-C token
count in the PDF **0**. Build: 0 errors, 0 undefined refs, 0 overfull boxes
$>5$pt, 176 pp; PDF shrank from 1.5 to 1.07 MiB as the rasters were removed. The
only remaining rasters are the appendix per-agent grids and the ablation figure,
which the directive permits. No new experiments; raw data and history untouched.
