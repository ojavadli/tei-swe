# Pre-registration: funded execution arm at the luna backbone (Phase C)

Registered 2026-08-10, AFTER Phase B completed (release `7f0a667`) and BEFORE
any Phase-C rollout. Tagged `prereg-exec2` in the public release repository so
the timestamp is externally verifiable.

## Design

**System: SWE-agent** (`agents/08_sweagent`) — the one system that runs
end-to-end on this hardware; same worktree mechanics as the 36-instance arm.

- Arms: **baseline** (frozen submission SHA, `_sweagent_base`) vs **patched**
  (tei-v7 branch tip after Phase B and its B3 repairs =
  **`7b1f047d382358ab8eb2756bfa43f9b2f61f5e72`**, shipped best =
  **`prompt-60`**, rubric 0.81, 154 applied versions); identical
  configuration otherwise. The tei-v7 history of this agent carries no
  placebo commit (verified 2026-08-10: sham-v1 is a separate branch), and the
  working tree is grep-verified free of "routine maintenance annotation"
  lines.
- Backbone (both arms): **`gpt-5.6-luna`**; per-instance termination ceiling
  **$3.00** (`--agent.model.per_instance_cost_limit 3.00`) — an experimental
  design parameter so runs terminate, stated here as such; NOT a study cost
  cap (the study has none).
- Instances: **100 fixed-seed stratified** SWE-bench Verified instances
  (50 archive-resolved / 50 archive-unresolved for this system, RNG seed 0,
  drawn from the archive's recorded outcomes; pools 329/133 after
  exclusions), excluding the six §10 pilot instances, per the standing pilot
  exclusion; the frozen list ships as `_exec100_instances.json`. Overlap with
  the 36-instance gpt-4o-mini arm is 36 instances — permitted and disclosed
  (different backbone and ceiling; the arms answer different questions).
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
