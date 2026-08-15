# REVISION_LOG_16 — font consistency: table/figure math now matches the body typeface

Owner directive: "font name of the text in table should be the same as font of
the passage." Build: 0 errors, 0 undefined refs, max overfull 0.97 pt (< 5 pt),
176 pp. pdf_qa PASS (7/7 vector figures); consistency PASSED (7 surfaces);
check_typography PASS; 0 Phase-C tokens in the PDF text.

## Root cause
Body prose is Latin Modern, but under the XeTeX default any `$...$` (inline and
in-table math — confidence intervals, `d_z`, p-value exponents) fell back to
**Computer Modern**, and the matplotlib figures emitted **Computer Modern Type-3**
glyphs from their mathtext. So numbers in tables/figures were set in a visibly
different face than the surrounding text.

## Fixes
1. **`\usepackage{lmodern}`** (main.tex). Redefines the legacy math families to
   Latin Modern, so all document math (table CIs, `d_z`, `<10^{-12}` exponents,
   Greek, arrows) renders in the same typeface as the prose. `pdffonts` now shows
   the math as `LMMathItalic*` / `LMMathSymbols*` — **zero Computer Modern** in
   the whole document.
2. **Figures: mathtext removed** (make_figures.py). Numeric labels are plain
   Latin Modern text ("n = 26", "+0.105", "+0.0630") instead of `$...$`. The six
   `fig_*.pdf` no longer embed `Cmr/Cmmi/Cmsy` Type-3 fonts — only Latin Modern.
3. **Contrasts table CI** (make_assets.py `crow`): the 95% CI is now plain
   Latin Modern text `[+0.055,+0.068]` rather than math-mode brackets.
4. **Cost table overfull** (make_assets.py): the "Per-model token split" and
   "Syntax pre-gate savings" rows put descriptive prose in the right (`r`) value
   column, over-widening it by 63.9 pt. Descriptions moved to the left column,
   value column left numeric, first column tightened `0.72\linewidth -> 0.70`.
   Overfull gone.
5. **check_typography.py rotation fix**: the auditor read the two `sidewaysfigure`
   caption pages (Figs 8-9) as 2.8x-oversized because `pdftotext -bbox` reports a
   rotated word's *width* as its height. The per-word size proxy is now
   `min(width, height)` for multi-char words — rotation-invariant, so horizontal
   text still reports its height and sideways captions report their true size.
   No more false OVERSIZED flags.

No new experiments; raw data, outcomes, and git history untouched.
