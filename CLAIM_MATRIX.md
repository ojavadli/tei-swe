# Final paper claim matrix (internal audit)

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | 30 heterogeneous third-party systems | `manifest.json` (30 systems / 29 repos) | SUPPORTED |
| 2 | 6,000 candidate versions (3,000 struct + 3,000 prompt) | `_paper_recompute.json` census; `agents/*/tei/candidates.jsonl` | SUPPORTED |
| 3 | 3,373 applied commits | apply taxonomy over 6,000 records | SUPPORTED |
| 4 | Deployed Default→Structural→Final = 0.606→0.667→0.684 (n=26) | `_paper_recompute.json` APPLIED | SUPPORTED |
| 5 | Relative applied improvement +13.0% (ceiling +14.0% proposed) | recompute arithmetic | SUPPORTED |
| 6 | Zero-patch deployed gain = +0.000 (null control) | recompute zeropatch_applied | SUPPORTED |
| 7 | 22/26 blinded strict majorities, 110/130 votes, 17 unanimous | `blind_reval.json` / `canonical_blinded_100.json` | SUPPORTED |
| 8 | Sham placebo separation (full 26.9%; re-anchor 0/45) | `sham_arm.json`, `sham_rearm.json` | SUPPORTED |
| 9 | Budget-matched random control: TEI 10/10 | `random_arm.json` | SUPPORTED |
| 10 | 15/30 deployed deltas clear measured MDE 0.074 | recompute MDE_applied | SUPPORTED |
| 11 | LLM subtotal $53.66; grand $75.02 (all retained arms) | cost reconciliation to cents | SUPPORTED |
| 12 | Cost/system $1.79, /candidate $0.009, /applied $0.016 | recompute cost | SUPPORTED |
| 13 | Zero executed benchmark rollouts as the selection signal | pipeline uses rubric/blinded/static only | SUPPORTED |
| 14 | Credit-ledger ablation null (2W/3L, p=1.0) | `curves_data.json` | SUPPORTED |
| 15 | Execution arm null (n=36, 3/36 vs 3/36, sign p=1.0) | `exec36_result.json` | SUPPORTED |
| 16 | TEI leads on third-party coverage | `comparison_qualification.md` (all comparators optimize own systems) | SUPPORTED |
| 17 | TEI unique on zero-executed-rollout selection | comparator audit (all use executed substrate) | SUPPORTED |
| 18 | TEI unique on placebo+blinded+random validation | comparator audit (none report it) | SUPPORTED |
| 19 | "lowest comparable cost/system" | comparator audit: most report no comparable $ | INSUFFICIENT REPORTING (not claimed as headline) |
| 20 | technique family n up to 1,557 (kills n≤4 disclaimer) | recompute technique_top | SUPPORTED |

Headline claims (abstract/conclusion) are limited to rows marked SUPPORTED.
Row 19 is explicitly NOT claimed as a headline (stated as: complete accounting
released while most comparators report none comparable).
