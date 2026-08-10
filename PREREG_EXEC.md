# Pre-registration: powered execution arm (committed BEFORE any run)

Registered 2026-08-09, before any Phase-2 rollout. Tagged `prereg-exec` in the
public release repository so the timestamp is externally verifiable.

## Design

**Primary system: SWE-agent** (the one system that ran end-to-end in the §10
micro-arm).

- Instances: **36 fixed-seed** SWE-bench Verified instances drawn from those
  SWE-agent attempted per the archive record, **stratified 18 resolved / 18
  unresolved** (by the archive's recorded outcome for this system), RNG seed
  0, drawn from `tei/onboarding.json` ids; the six §10 micro-arm instances
  are excluded so this arm is independent of the pilot.
- Arms: **baseline** (frozen SHA worktree) vs **patched** (`tei-v7` HEAD,
  post-repair), identical configuration.
- Agent model: `gpt-4o-mini`; per-instance cost cap **$0.35**; official
  SWE-bench Docker harness (colima, Rosetta) for scoring.
- Resumable per-instance JSON records; no instance re-run because of its
  outcome; cost-limit exits recorded per arm.

**Secondary onboarding attempts (45-minute timebox each):** KGCompass
(requires Neo4j — attempt via `docker run neo4j`) and aider (separate runner
repository). If either onboards inside its timebox, it receives the same
36-instance stratified design (its own archive-attempted instances); if not,
the exact wall is documented and reported.

## Endpoints

Paired resolve wins/losses over the 36 instances; exact sign test;
Clopper–Pearson 95% CI on the patched-arm resolve rate; per-arm cost-limit
exit counts; per-arm total rollout cost.

## Interpretation branches (committed before any result is seen)

- **Positive & significant** (patched wins > losses, exact sign test p<0.05):
  reported as the first execution-rung gain; the abstract's execution
  sentence is upgraded to state it.
- **Null** (no significant difference): reported as execution-rung
  equivalence at the measured power (CI printed); all other claims unchanged.
- **Negative** (losses > wins, p<0.05): reported plainly; the do-no-harm
  discussion is updated accordingly.

No branch may be suppressed; the fired branch is quoted verbatim in the
paper and REVISION_LOG_6.

## Budget

Hard cap **$40** total for Phase 2 (rollouts, both arms, all systems).
Worst case for SWE-agent alone: 72 rollouts × $0.35 = $25.20. If projections
exceed $40, instance counts scale down uniformly — never below 36 for
SWE-agent — and the scale-down is recorded here and in the log.
