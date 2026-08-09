# REVISION_LOG_5 — mathematics-naming + eight consistency defects

Spend: $0 (no LLM calls; no fetches needed).

| Item | Landed |
|---|---|
| A1 | Abstract mechanism sentence names the toolkit in one breath: exact futility bounds → Jeffreys Beta–Binomial posterior early kills over discordant pairs → Wilson lower-confidence-bound Pareto selection → final Bayesian do-no-harm confirmation. |
| A2 | Intro method paragraph gives one-clause definitions: exact futility (win arithmetically impossible), Jeffreys kills (McNemar/discordant-pair view), MDE preflight before verdicts, Wilson-LCB certified Pareto, exact sign tests + Hoeffding distribution-free margins (verify_candidate), agent-level Clopper–Pearson. §Method (5) expanded to define the identical terms — intro ⊆ method verified. |
| B1 | One canonical accounting, single source (total_budget now sums every pass incl. sham/random/traj-extras): **1,271 calls = 1,071 Luna + 200 Terra = 538 core optimization (18/agent) + 733 validation/replication (global)**. Table 9 cell auto-corrected via \swCalls; R1(c) rewritten with the three-way split; "968" and "32 LLM calls" grep-zero in the PDF. |
| B2 | Bound-only cost language everywhere: study list bound **$1.78 (all-Luna) – $17.79 (all-Terra)** (recomputed over the full-pass token base); per-agent **$0.06–$0.59**; costs-table row is a labeled range; page-10 "whole study is $1.52" and contributions' "$0.05 at list prices" replaced. Abstract keeps \swCostListLo–\swCostListHi. |
| B3 | "two to three orders of magnitude lower cost per system" → "substantially lower reported optimization/evaluation call volume — noting that model calls and executed agent rollouts are not equivalent computational units." |
| B4 | All 30 appendix records now show "Trajectories used during the original optimization run: 0" + "Trajectories retrieved in the post-hoc validation pass: N" (N from _traj_downloads.json); onboarding.json notes (both fields) rewritten ×30; REPORT/DIAGNOSIS regenerated ×30; generator constants and PROVENANCE/master swept — "credentialed" grep-zero across paper, records, and live docs. |
| B5 | "compile-clean" → "syntax-parse-clean (ast.parse)"; residual "compile audit/pre-gate/Compile-Level" in live docs → syntax-parse wording. |
| B6 | Abstract execution phrasing verbatim: "a six-instance execution micro-arm observed no paired regression (baseline 1/6; patched 1/6)". |
| B7 | Table 9 row 1 → "Reported optimization/evaluation scope" with per-method units as stated in each abstract (TEI 30 third-party systems; GEPA 6 tasks; MIPROv2 7 LM programs; Maestro 2 benchmarks + 2 applications; ACE agent+finance benchmarks; HiveMind 1 multi-agent trading scenario). |
| B8 | README opening/comparison paragraphs mirror the new abstract (named math, bounded costs, canonical call split, B6 exec sentence); repo About rewritten within the 350-char limit with bounded costs + calibrated absence claim; tei-loop README verified canonical (1 match); RELEASE_CHECKSUM regenerated; repo ≡ this PDF. |
| C | consistency_audit.py extended with the banned strings ("968 calls", "32 LLM calls", "orders of magnitude", "compile-clean", "credentialed", "$0.05 at", "whole study is $1.52") and made ligature-safe for PDF extraction (it had false-positived on "aſter"); **PASSED over 7 surfaces**; compile 0 errors / 0 undefined. |
