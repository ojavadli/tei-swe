# REVISION_LOG_2 — TEI-SWE value-certification revision

Maps every mission item to what was done. Control-arm results are quoted
verbatim from their recorded JSON; the paper renders the same values via
macros.

## P0 — desk-reject hygiene

| Item | Status | Notes |
|---|---|---|
| P0.1 citations/refs | ✅ | 7 missing BibTeX entries added with fetch-verified metadata (incl. arXiv:2605.05973 under its true title "Towards Reliable LLM Evaluation: Correcting the Winner's Curse in Adaptive Benchmarking"); dangling `\ref{tab:power}` → `\S power`; compile now **0 errors, 0 undefined** (grep of main.log). Root cause of the earlier false "0 undefined" check: scanning PDF text for `[?]` misses natbib log warnings — fixed by grepping the log. Also removed 3 stray bytes (`wha`) that had corrupted main.tex line 1. Checksum verification at reship. |
| P0.2 "up to 30+30" | ✅ | Abstract, intro, method sweeps; budget scaling stated as fixed a priori with 9/8/13 @ 60/36/24 macros. |
| P0.3 same-family judge wording | ✅ | All "second judge family" → "a second model within the same GPT-5.6 family"; threats updated. |
| P0.4 "syntax pre-gate (ast.parse)" | ✅ | Ladder figure, contributions, conclusion, ladder section renamed; no compile/lint claims. |
| P0.5 costs | ✅ | **List pricing verified** (developers.openai.com/api/docs/pricing, 2026-08-09): gpt-5.6-luna $0.20/$1.20, terra $2/$12 per Mtok → the $1.25/$10 rate is relabeled "a conservative accounting rate (~6× luna list)". Whole-study at list: $1.52–$15.20 model-mix bounds (true value near the low end; terra was ~20% of calls). Spend table split into optimization-run cap ($25 / $20.89 bound-spent) vs validation-passes cap ($15 / $4.54) vs micro-arm rollouts ($2.49, billed separately); "$26.80 vs $25" contradiction resolved. New prominent cost-efficiency table: **$0.49/agent all-in (accounting) · ~$0.05/agent at list · $0.013/version · $0.027/patch**. |
| P0.6 four zero-patch agents | ✅ | Standard wording in abstract & R2: rubric rose for all 30; 26 received shipped changes; blinded covers those 26. |

## P1 — certification controls

| Item | Status | Result (verbatim from JSON) |
|---|---|---|
| Pre-registration | ✅ | `PREREG_SHAM.md` committed & tagged **`prereg-sham`**, pushed to github.com/ojavadli/tei-swe at 2026-08-09T08:16:40Z, BEFORE any sham call. |
| Sham-patch placebo (26 agents, k=5, seed 7) | ✅ | `sham_arm.json`: sham votes **35/130 (26.9%)**, strict majorities **7/26** — vs real patches 128/130 (98.5%), 26/26. **Pre-registered branch fired: "CERTIFIED (share ≤ 60%)"** → the blinded preference is substantive; headline stated with full confidence per the pre-registration. |
| Random-proposal arm (10 agents, seed 13) | ✅ | `random_arm.json`: **TEI's rubric delta beats the random arm's best candidate on 10/10 agents** (means +0.0630 vs +0.0165); under blinding the random branch takes ≤1 vote on 9/10 agents (0 strict majorities) vs real patches 10/10 on the same subsample. Unguided arm applied 77/120 patches through the same pre-gate. |

## P3 — external judge (Anthropic, judging only, ≤$3)

| Item | Status | Result |
|---|---|---|
| Probe | ✅ | `claude-sonnet-5` responds; key from local settings; never used for generation/optimization. |
| ext_blind / ext_sham / ext_repair (seed 11) | ✅ — reported exactly as landed | `external_judge.json` (claude-sonnet-5, $1.19): **ext_sham 0/40 votes, 0/8 majorities — perfect cross-provider placebo rejection**; ext_blind 17/50 votes, 3/10 strict majorities (unanimous-for on 2, unanimous-against on 4, ties on rest) — preference reproduces partially; ext_repair 15/25 votes, 3/5. Abstract/threats state this verbatim: both providers reject every sham; per-agent preference strength is provider-dependent. |

## P4 — value-forward rewrite

| Item | Status | Notes |
|---|---|---|
| Title | ✅ | Default title locked by the sham CERTIFIED branch: "Blinded-Confirmed Improvements to 24 of 26 Patched SWE-bench Agents at About Half a Dollar Each: A Gated Target–Evaluate–Improve Loop with a Validation Ladder (TEI-SWE)". 24/26 = pre-repair confirmatory unit per P2.1. |
| Abstract | ✅ | P4.3 order; one limitation clause at the end; tei-audit invocation included. |
| Contributions | ✅ | Capability first; ladder+tooling second; pre-gate third; set fourth; stats+artifacts fifth. |
| Capability subsections | ✅ | R1(a) structural fixes incl. refuse-to-fabricate floor + apply-anatomy table; (b) optimization w/ pinned companion footnote; (c) efficiency (32 calls/agent, batching, $0 pre-gate); (d) cost-efficiency table + comparison hook. |
| R2 statistics (P2) | ✅ | Confirmatory = pre-repair 24/26 with exact CI [67%,97%] at agent level; pooled 128/130 descriptive w/ cluster-aware note; repair arc in the standard wording; post-repair 26/26 labeled adaptive retest; independent confirmation reserved for the external-judge fresh-seed run. |
| Trajectory claim correction | ✅ | **The original "requires AWS account" claim was WRONG** — the archive's own `analysis/download_logs.py` (boto3) retrieves logs+trajs anonymously; the 403 was ListBucket-only. Corrected in §set; TRAJ rung widened with downloaded submission traces: 6 submissions retrieved (livesweagent 500, trae 500, moatless 273, darsagent 300, orcaloca 300, experepair 1; swe-rizzo/aider/rag uploaded none). Scored 25 more traces: grounding holds on compact-trace systems (livesweagent −0.15, darsagent −0.13); slice-scoring breaks down on very long sessions (trae −0.50, orcaloca −0.58) — reported once as the TRAJ instrument's scope condition, not as agent quality. Two reader iterations were needed (first fed boilerplate heads → zeros; replaced, documented). |
| Prior art | ✅ | DGM (2505.22954), ADAS (2408.08435), Trace (2406.16218) fetch-verified and added, positioned on the population-scale/third-party/certified-selection axes. |
| tei-audit | ✅ | `tei_audit.py` one-command (syntax pre-gate + blinded A/B on any repo diff); invocation in abstract + README. |
| "pre-registered" sweep | ✅ | Only the sham arm retains "pre-registered" (it has the tag); budget scaling etc. now "fixed a priori in committed run scripts". |

## P5 — reship

Final compile: **0 errors, 0 undefined citations/references, 0 overfull boxes >100pt**;
main.pdf ≡ TEI-SWE.pdf (sha256 a33be131…); release rebuilt, secrets-audited, pushed.
Pre-registered branch that fired: **"CERTIFIED (share ≤ 60%)"** — quoted verbatim from
`sham_arm.json.prereg_branch_fired`.

## Spend (this mission, accounting rate)

| Stage | OpenAI nominal | Anthropic |
|---|---|---|
| Sham arm (130 calls) | $0.47 | — |
| Random arm (85 calls) | $0.77 | — |
| External judge (115 calls) | — | $1.19 |
| Traj-wide scoring (3 passes incl. 2 reader iterations) | $0.73 | — |
| **Mission total** | **$1.97 of ≤$18** | **$1.19 of ≤$3** |

At verified list prices the OpenAI portion is ≈$0.25.
