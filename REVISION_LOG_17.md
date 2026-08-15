# REVISION_LOG_17 — compliance repair: abstract, cost-ladder claim, Fig 7 grammar, Fig 5 legend

Targeted repair of a failed compliance pass. No science changed (datasets,
results, statistics, tables, costs, sample sizes, conclusions, scope all intact).
Build 176pp, 0 undefined refs, max overfull 0.97pt (<5pt).

## 1. Abstract — replaced VERBATIM
The old abstract ("typically shown on a few author-chosen tasks…") is gone,
replaced word-for-word with the owner-supplied paragraph. Verified by extracting
the compiled abstract and comparing (ligature/line-break-hyphen normalized):
identical. `$` and `%` escaped for LaTeX; en-dashes in "Target–Evaluate–Improve"
preserved. All numbers match the study (0.606→0.667→0.684, 13.0% / 14.0%,
3,373 patches, 22 of 26, 110/130, 17 unanimous, 26.9% vs 84.6%, all 10, $1.79 /
$0.009, six thousand).

## 2. Cost-ladder sentence — corrected to agree with Fig 2
Intro no longer claims "each rung cheaper than the next is trusted" (which
contradicted Fig 2's own caption). Now: "The ladder is ordered by evidentiary
strength, not cost; we use the cheapest applicable checks early, but marginal
cost is not monotonic across rungs." Matches the ladder figure exactly.

## 3. Figure 7 — one comparison grammar, no bars
Panels A, B, D were bar charts; all four panels now use the same horizontal
Cleveland lollipop as panel C (filled accent = TEI/real/patched, open gray =
control). Values and axes preserved exactly: blinded 22 vs 4 (0–26); sham 84.6%
vs 26.9% (0–100%); random +0.0630 vs +0.0165; cross-provider 3 vs 6 (0–10). The
adverse cross-provider panel is drawn at the same scale and prominence — the
accent "patched" lollipop (3) is visibly shorter than baseline (6), not softened.

## 4. Figure 5 — legend removed, states labelled directly
Dropped the corner legend; the two states are now labelled inline on the top row
("baseline" over the open dot, "deployed" over the filled dot). Cleveland/
dumbbell form and all values unchanged (+0.105 / +0.088 / +0.063 / +0.058).

## Verification (all pass)
abstract verbatim (normalized) = True; grep "typically shown on a few
author-chosen tasks" = 0; grep "each rung cheaper than the next" = 0; Fig 7 has
no bar rectangles (rendered); pdfimages -list = raster only on appendix pp
173/174/176, main fig pp 2/11/14/16/17 vector; pdffonts = 7 Type-3 fonts, all
Latin Modern (LMRoman, the matplotlib vector-figure glyphs), 0 Computer Modern.
pdf_qa PASS (7/7), consistency PASSED, check_typography PASS, 0 Phase-C.
