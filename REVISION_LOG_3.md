# REVISION_LOG_3 — consistency-and-sync pass

Every P-item mapped to its change. No new experiments; no external-model
judging; spend this pass: **$0.00 LLM** (all edits + audits are local).

## Owner decisions
| Item | Landed |
|---|---|
| Title | `TEI: Target–Evaluate–Improve — A Cost-Efficient Self-Improving Loop for Agentic Systems via Sequential Decision Gating (TEI-SWE)` — exact, single line, no result numbers. |
| Authors | Orkhan Javadli (MIT, ojavadli@mit.edu) + Anni Zimina (Stanford, zimina@stanford.edu) — author block, new Author Contributions section, README citation block, `.zenodo.json`. |
| Terminology | §5 step (5) now defines **sequential decision gating** (sequential paired evaluation, exact futility bound, posterior early kills → Jeffreys Beta–Binomial do-no-harm confirmation); the validation ladder keeps its name. |
| Abstract sentence 1 | Cost-efficiency claim with both ledgers: \swCostPerAgent ($0.47, accounting) / \swCostPerAgentList ($0.05, list). |
| 2026-optimizer comparison | Retained. |

## P0 — one number convention
Canonical sentence (verbatim): *"Pre-repair confirmatory result: 24/26 patched
agents (118/130 votes); after defect repair, the adaptive retest shows 26/26
strict majorities, 24 unanimous (128/130 votes)."*
Applied to: abstract; intro §1 (old 26/26+128/130 line replaced); Fig. 1 ladder
box (now pre-with-pre: "24/26 pre-repair (118/130); 26/26 after repair
(128/130)"); R2 (labels per Table 5's Blind column: 24 agents 5/5, two 4/1);
conclusion; README; tei-loop README; repo description. Running header: N/A
(article class, no header; title carries no numbers). Table 5's Blind column
is the derivation source (emitter counts majorities/unanimous from it;
pre-repair constants documented in the emitter as recorded history).
Guard: `consistency_audit.py` greps PDF+README+PROVENANCE+reports for
cross-pairings — **PASSED over 6 surfaces**.

## P1 — cross-provider scoping
Removed from abstract; full result in new **Appendix "Supplementary
Cross-Provider Check"** with per-agent vote table. Facts stated from records
(mission's "4/10 baseline, 3 tied" did NOT match `external_judge.json` —
actual: **3/10 patched majorities, 6/10 baseline majorities (4 unanimous),
1/10 no strict majority (2/0/3)**; derived numbers used). One Limitations
sentence points to the appendix. Line-98 → "A second model of the same GPT-5.6
family concurs (blinded, 8/10 subsampled agents)"; line-703 → "all primary
judging by two sibling models of one provider (…appendix replicated the
placebo separation exactly and the patch preference partially)". Sonnet vote
files kept in `datasets/`. R2f deleted from Results.

## P2 — costs
Intro cost attachment fixed: "$0.35/agent for the rubric-rung optimization
run, plus $0.03/agent for the blinded confirmation". Table 3 (spend) rebuilt
as per-stage rows that sum: optimization $10.23 + noise-floor post-pass $0.22
+ blinded pass 1 $0.68 + adaptive retest $0.11 + validation passes $0.91 +
TRAJ widening $0.73 + sham $0.47 + random $0.77 = **LLM subtotal $14.12**;
execution rollouts $2.49 (own ledger); **grand $16.61** — each stage within
its cap; the old "$26.80 vs $25" ambiguity eliminated (that figure was a 2×
bound mixing stages). Provider ledger: luna 1,398 calls / terra 200 calls
(exact), per-model token split honestly marked not-separately-metered with
list bounds; sonnet ($1.19) listed in the appendix context only; abstract
quotes both ledgers. 1,134-vs-1,140 footnoted (6 versions lacked a
machine-readable declared dimension). `tei_audit` invocation now
`--repo R --base SHA --cand HEAD` everywhere.

## P3 — fact repairs (derived from records)
(a) Refuse-to-fabricate rewritten with the two DISTINCT sets: no-patchable-
surface = {Sonar, ACoder} (120/120 null proposals); zero-applied = those two
+ {CodeShellAgent, CodeShellTester} (also all-null); config-only-surface
{live-SWE-agent, CodeR} received 24 and 12 config patches — matches Appendix
records exactly. (b) New **§3.1 "Population defects the rule admitted"**:
rank 30 → SWE-bench/SWE-bench (benchmark repo), rank 27 → ozyyshr/RepoGraph,
30 systems → 29 distinct repos; frozen table now carries †/‡/§ markers.
(c) Table 2 caption footnote reconciles content-screen 16 clean /
entry-point-screen 3 / executed 1 (derived: 4 no-source, 6 docker, 4 gpu,
16 clean). (d) Techniques table moved to **Appendix "Proposal Technique
Frequencies"** with the n≤4 descriptive-only caveat.

## P4 — placebo language
All glosses now read "rejects the generic changed-code / style explanation
for the primary judge's preference" (abstract, R2d incl. the prereg-branch
recap, conclusion). The tag and its recorded branch text are untouched.

## P5 — release sync
`PROVENANCE.md`: trajectory-access claim corrected (downloader works
unsigned; exact object list: sweagent_gpt4 300 / livesweagent 500 / trae 500
/ moatless 273 / darsagent 300 / orcaloca 300 / experepair 1; swe-rizzo,
aider, rag uploaded none); "no agent could be executed" corrected (SWE-agent
executed, 1/6=1/6, 0W/0L); "luna exclusively" replaced with the full model
list (luna primary; terra 200 replication calls; sonnet 115 supplementary
judging calls; gpt-4o-mini execution rollouts). README: new title, authors,
canonical sentence, BibTeX, checksum pointer (`RELEASE_CHECKSUM`), audit
one-liner. `.zenodo.json` with both authors — DOI mint pending owner token.
tei-loop README results line updated in one README-only commit (`3b4cb2a`).

## P6 — guards and ship
`scripts/consistency_audit.py` added (fails on any pre/post cross-pairing or
missing canonical sentence) — caught one real regression during this pass (a
stale TEI-SWE.pdf produced by a `grep -c … && cp` short-circuit) before it
could ship. Final compile: **0 errors, 0 undefined, 0 PENDING/?? markers**,
89 pages; release checksum recorded; secrets audit clean.
