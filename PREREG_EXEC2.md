# Pre-registration: funded execution arm at the luna backbone (Phase C)

DRAFT — to be finalized and tagged `prereg-exec2` AFTER Phase B completes and
BEFORE any Phase-C rollout. The two placeholders marked {TBD} are filled at
tag time from recorded Phase-B outputs; every other design element is fixed now.

## Design

**System: SWE-agent** (`agents/08_sweagent`) — the one system that runs
end-to-end on this hardware; same worktree mechanics as the 36-instance arm.

- Arms: **baseline** (frozen submission SHA, `_sweagent_base`) vs **patched**
  (tei-v7 branch tip after Phase B and its B3 repairs = {TBD: SHA}, shipped
  best = {TBD: version id}); identical configuration otherwise. The tei-v7
  history of this agent carries no placebo commit (verified 2026-08-10:
  sham-v1 is a separate branch); the patched worktree is additionally
  grep-verified free of "routine maintenance annotation" lines before rollout.
- Backbone (both arms): **`gpt-5.6-luna`**; per-instance termination ceiling
  **$3.00** (`--agent.model.per_instance_cost_limit 3.00`) — an experimental
  design parameter so runs terminate, stated here as such; NOT a study cost
  cap (the study has none).
- Instances: **100 fixed-seed stratified** SWE-bench Verified instances
  (50 archive-resolved / 50 archive-unresolved for this system, RNG seed 0,
  drawn from the archive's recorded outcomes), excluding the six §10 pilot
  instances, per the standing pilot exclusion. Overlap with the 36-instance
  gpt-4o-mini arm is permitted and disclosed (different backbone and ceiling;
  the arms answer different questions). If fewer than 100 stratifiable
  instances remain, the maximum available is used and reported.
- Harness: `sweagent run-batch` (num_workers 3) for trajectories; official
  SWE-bench Docker harness (colima, Rosetta, `cache_level none`, image pruning
  between slices) for scoring. Resumable per-instance JSON records; no
  instance re-run because of its outcome; cost-limit exits recorded per arm.

## Endpoints

Paired resolve wins/losses over the instance set; exact two-sided sign test;
Clopper–Pearson 95% CI on each arm's resolve rate; per-arm cost-limit-exit
counts; per-arm total rollout spend (traj-summed, definitive).

## Interpretation branches (committed before any result is seen)

1. **Significant paired gain** (wins > losses, exact sign test p < 0.05): an
   execution-rung improvement result is added; abstract/conclusion upgraded,
   scoped to this configuration (SWE-agent, luna backbone, $3 ceiling).
2. **Null**: reported as a second preregistered null at the funded
   configuration, alongside the $0.35 gpt-4o-mini arm; CIs printed.
3. **Net negative** (losses > wins, p < 0.05): reported plainly; the
   do-no-harm discussion updated accordingly.

No branch is suppressed; the fired branch is quoted verbatim in the paper and
REVISION_LOG_9. §10 carries both configurations; Fig. 1's execution rung shows
both; Table 3 gains the Phase-C line.

## Spend

No study-level cap (owner authorization). Projection for termination-ceiling
worst case: 200 rollouts x $3.00 = $600 ceiling-bounded; actual spend is
expected far lower (most instances terminate well under the ceiling) and is
reported exactly from the recorded trajectories.
