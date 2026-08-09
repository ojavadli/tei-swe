# REVISION_LOG — TEI-SWE final revision

Maps every instruction of the revision mission to what was done, with evidence
paths. Numbers cited here are recorded values; the paper renders them via
macros from the same JSON.

## A. New evidence

| Instr | Status | What was done | Evidence |
|---|---|---|---|
| A0(i) repair + re-audit + re-blind | ✅ | 6 syntax-broken files across 5 agents repaired as `tei-v7 repair:` commits (splice/indent/f-string/JSON-block fixes, intent preserved); full `ast.parse` audit re-run → **0 errors on 41 changed files, 30/30 agents clean**; blinded A/B re-run for the 5 repaired agents → each flipped to **5/0 patched**; post-repair headline: **26/26 agents, 128/130 votes**. Pre-repair state preserved for the ladder narrative. | repair commits on each agent branch; `syntax_audit.json` (post, 0), `syntax_audit_prerepair.json` (6, reconstructed from the repair-commit list — the original file was overwritten by the post-repair audit; noted); `blind_reval.json` (merged, `post_repair: true` flags) |
| A0(ii) compile pre-gate | ✅ | `ast.parse` rejection before any judge call added to the study pipeline (`tei_pipeline.apply_patch`) and to the methodology (`tei_loop.gate.static_pregate`), committed. Note: the tei-loop commit also swept ~120 lines of pre-existing uncommitted gate edits that were in the working tree; bundled, not authored, by this revision. | `tei-loop@3154181`; `scripts/tei_pipeline.py` |
| A1 execution micro-arm | see paper §gap | Attempt 1: colima+docker installed, engine up; wall = `sweagent` default split. Attempt 2: split fixed; agents ran; wall = per-instance images are x86_64, VM was aarch64 (DockerPullError ×6). Attempt 3: colima restarted with `--vz-rosetta`, stale Docker-Desktop `credsStore` removed (`~/.docker/config.json`, backup kept); x86_64 images pull and run; **SWE-agent executed end-to-end in both arms** (6 fixed-seed paired instances, gpt-4o-mini, $0.30/inst cap): baseline 1/6 resolved, patched 1/6 resolved (same instance), 0W/0L → `verify_candidate` **accepts: do-no-harm confirmed at the execution rung**; no detectable gain at n=6 (MDE 0.24 on resolve scale). Patched arm hit 3 cost-limit exits vs 0 (its added verification consumes budget) — reported. KGCompass (needs Neo4j) and aider (separate runner repo) exceeded the timebox; walls documented in §gap. Title stays option-2 per B2 (no execution gains). | `a1_attempt{1,2,3}.log`, `a1_micro_arm.sh`, `a1_result.json` |
| A2 TRAJ rung | ✅ | 19 real recorded in-repo trajectories scored across 4 systems (sweagent 6, darsagent 1, agentless 6, coder 6). TRAJ vs anchored PROXY baselines: mean diff −0.024, max |diff| 0.132 (sweagent −0.132 the outlier; the paper reports the numbers as measured). | `validation_passes.json:a2` |
| A3 second judge | ✅ | `gpt-5.6-terra`, fixed-seed 150-candidate rescore: sign agreement 87.3%, Spearman ρ=0.50, Pearson r=0.28, terra optimism 88.7% (luna on same sample 98.7%) → optimism is family-general; blinded protocol on 10-agent subsample: **8/10 strict-majority patched, 40/50 votes** (dissents: composioswekit 1/4, orcaloca 1/4 — reported). | `validation_passes.json:a3` |
| A4 companion-run fact-check | ✅ | 0.644→0.879→0.889 traced to `FINAL_TABLE_band31_v2.md` (MEAN row 0.6444/0.8795/0.8891) with results in `results_cubic30_band31_v2/` + `results_struct_band31_v2/` at tei-bench@626b455f; paper cites exactly this in a pinned footnote. The mission's caution was right that `results_v7/_summary.json` is a different (delta-0) config; not cited. | footnote in §Results R1 |
| A5 measured-noise MDE | ✅ | 5 re-scores × 5 fixed agents → pooled per-probe test-retest sd **0.0374** (4× below the assumed 0.15); measured MDE₈₀ = **0.074** (n=4) / 0.060 (n=6). Honest outcome vs the mission's expectation: only **3/30** rubric deltas clear even the measured MDE individually — so the paper places per-agent statistical weight on the blinded votes (k=5, unanimity p=0.031/agent; pooled 128/130, p<10⁻⁷) and reports both MDE columns. No number was bent toward the expected outcome. | `validation_passes.json:a5`; §Power |

## B. Framing & citability

| Instr | Status | Notes |
|---|---|---|
| B1 named artifacts | ✅ | TEI-SWE-30, Validation Ladder, substrate-honesty protocol, both datasets named in abstract/contributions. |
| B2 retitle | ✅ | Option-2 family, post-repair numbers: "Improving 26 of 26 Patched SWE-bench Agents at About Half a Dollar Each…". Cost phrase uses full-study nominal (~$0.45–0.50/agent incl. all validation); exact figures in §repro. A1-conditional title swap applied only if execution gains land (see a1_result.json). |
| B3 abstract | ✅ | Ordered exactly as specified; ~250 words; every numeral a macro. |
| B4 ladder box | ✅ | Fig. 1 boxed checklist w/ cost+trust+this-study column per rung, page 2. |
| B5 related work adds | ✅ | All fetched & verified from arXiv abstract pages: 2605.05973 (title differs from the mission's "SIREN" shorthand — cited under its real title, "…Winner's Curse in Adaptive Benchmarking"), 2510.08413 (PAC-Bayes prompt bounds, EXAIT@ICML 2025), 2311.13628 (Prompt Risk Control, ICLR 2024), 2603.27403 (CFC, CVPR 2026), 2601.03493 (SESS). |
| B6 tone sweep | ✅ | "owner mandate" → "a fixed single-model design constraint"; home paths removed from title page; substrate labels and run-integrity disclosures kept. |
| B7 statistics polish | ✅ | Holm across the 3 stage contrasts (macros swHolm*); exact Clopper–Pearson CI on pooled blinded votes (swBlindShareCI); bootstrap CI on optimism (swGeBaseCI); exact binomial CI on unapplied-best (swBestUnappliedCI); per-agent blinded consistency (swBlindPerfect unanimous). |
| B8 release | GitHub ✅ / HF+Zenodo ⛔ | Public repo assembled by `build_release.py` (paper, manifest, tei records, patch series via format-patch, datasets, scripts, README w/ "audit your own loop"); secrets audit gate must pass before push. HF datasets + Zenodo DOI blocked on credentials that only the owner can provide (no HF_TOKEN/ZENODO_TOKEN on this machine); mirrors marked pending in README. |
| B9 comparison table | ✅ | §Compare + Table: coverage/cost/validation-depth axes measured on both sides; external numbers verbatim from fetched abstracts (GEPA "+10%+ vs MIPROv2", "+6% avg / up to 20% vs GRPO", "up to 35× fewer rollouts"; MIPROv2 "up to +13%", "5 of 7 programs"; Maestro "+12/4.9/4.86%" and "far fewer rollouts than GEPA", counts n.r.; ACE "+10.6% agents"). Mission-stated figures that the abstracts do NOT contain (GEPA 100–500 rollouts/task; Maestro 240–6,000+; GRPO ≈24,000) were **not** printed — "n.r." used instead. Mandatory substrate column present; no substrate-mismatched quality comparison. |
| B10 results restructure | ✅ | Ladder-first: R1 improvement, R2 blinded headline (+R2b terra, R2c TRAJ), R3 measured noise, single §Ladder section holding the discovery narrative (pre-repair 24/26+118/130, 2 flagged, 6 files/5 agents, repairs, pre-gate) exactly once. Per-agent table columns: rubric Δ | blinded k/5 | AST ✓ | floor | MDE. Power section rewritten around measured noise. |

## C. Consistency

- 124 numeric macros in `numbers.tex` + 12 narrative macros in `a1_result.tex`, all emitted by `make_assets.py`/`make_narrative.py` from recorded JSON.
- Substrate/rung labels at point of use in every table, figure, and results paragraph.
- Compile: tectonic, 0 errors; refs/citations verified (0 unresolved).

## D. Spend (this revision, nominal / conservative)

| Pass | Nominal | Conservative |
|---|---|---|
| Blinded re-run (5 repaired agents) | $0.11 | $0.23 |
| A5+A3+A2 passes (244 calls) | $0.91 | $1.82 |
| A1 agent rollouts (gpt-4o-mini, both arms, run ledgers) | $2.49 | $2.49 |
| **Revision total** | **$3.51** | **$4.54** — well under the $15 cap |
| **Whole study, all passes** | see paper §repro (macros) | |
