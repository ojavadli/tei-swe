# Phase-C runner handoff — run-integrity record (2026-08-11)

**Event (5th operational finding, execution arm).** The protected single runner
`exec100_arm_v2.sh` (pid 5801) completed its **patched** arm
(`ARM-patched-ROLLOUTS-DONE`, 14 genuine patched rollouts) and entered its
**baseline** phase. That phase issues `docker rmi -f` on all `sweb` images at
every round start; because its own baseline rollouts were racing the parallel
fleet's pulls in the single shared containerd content store, its rounds
completed fast and re-pruned almost continuously. Result: **~5 hours with zero
new genuine rollouts** (frozen at 84/200 = baseline 70, patched 14) and **$0
spend** (failed builds make no LLM call). At diagnosis time **0 `sweb` images
existed** on the VM and every fleet build failed `NOT_GENUINE:missing`.
Genuine had climbed 50→84 *while the runner was in its patched phase* and froze
the instant it switched to baseline — isolating the cause to the runner's
baseline-phase pruning livelocking the fleet on one 4-vCPU Docker VM.

**Why the fleet could not simply wait it out.** The 86 remaining patched
instances can only be completed by the fleet (the runner is past its patched
phase and will not redo them), but the runner's continuous pruning livelocked
that fleet. On a single Docker VM one producer must own it.

**Resolution (owner-approved; overrides the standing "never kill the runner"
guard, which existed to protect genuine work — and that work is immutable on
disk).** Graceful `SIGTERM` of the finished runner script and its direct
`run-batch` child (identified by `--num_workers 3` + a direct
`_exec100_baseline`/`_exec100_patched` output dir, distinct from the fleet's
`--num_workers 1` + `_exec100_sidecar/...`). The fleet (fast pipx path, no
pruning) then owns the VM and completes both arms.

**Preservation.** All 84 genuine rollouts were verified unchanged before and
after the SIGTERM (baseline 70, patched 14). The runner's ≤3 in-flight,
not-yet-genuine baseline rollouts were discarded (they carry no genuine record
and are re-run by the fleet). No genuine rollout, commit, tag, or preregistration
was deleted or altered.

**Class of finding.** Same family as the earlier run-integrity items
(`timeout(1)` false negative, `git add -A` sweep, shard collision, and the
Phase-C progress-ledger-as-defective-instrument): a shared-resource contention
that presented as "still running" while producing nothing. The genuine-rollout
ledger correctly showed zero real progress throughout, which is what surfaced
the stall. The fix is orchestration (single owner of the Docker VM), not a
scientific change; the model, prompts, arms, seeds, task set, $3 ceiling, and
evaluation harness are all unchanged.
