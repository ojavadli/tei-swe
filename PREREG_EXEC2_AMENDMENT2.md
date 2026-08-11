# Amendment 2 to PREREG_EXEC2 (operational scheduling change; no scientific-design change)

Registered 2026-08-10, during Phase-C execution, to document — transparently and
before broad parallel scale-out — an OPERATIONAL implementation change made to
increase throughput on the owner's 20-key pool. The original `PREREG_EXEC2.md`
(tag `prereg-exec2`) and Amendment 1 (`prereg-exec2-amend1`) are preserved
unchanged. Tagged `prereg-exec2-amend2`.

## What changed (scheduling/infrastructure only)

1. **Parallel execution across an API-key pool.** The remaining Phase-C rollouts
   are executed concurrently by sidecar workers drawing from a 20-key OpenAI
   pool (19 unique credentials; KEY09 duplicates KEY08), coordinated by an
   atomic SQLite work-claim scheduler (`execution_scheduler.sqlite`) so no
   instance x arm is ever run twice concurrently and no genuine rollout is
   reclaimed. The originally-running single runner (`exec100_arm_v2.sh`, pid at
   snapshot 5801) is NOT killed or modified; it continues to own the patched arm
   until it completes, after which the controller releases any remaining patched
   jobs to the fleet. Snapshot: `PARALLEL_SCALEOUT_SNAPSHOT.json`.

2. **swe-rex install method: `python_standalone_dir=""` for fleet workers.**
   SWE-agent's swe_bench loader defaults `python_standalone_dir` to `/root`,
   which makes each rollout compile a standalone CPython from source inside a
   `docker build` (~10 min, CPU/RAM-heavy) before the agent runs. On the
   pre-existing colima VM (4 vCPU / 7 GB RAM), concurrent compiles are
   infeasible and, worse, the long build keeps the base image referenced for
   ~10 min, during which the protected runner's inter-round `docker rmi -f`
   deletes it and the build fails. Setting `python_standalone_dir=""` (the
   documented bypass, per the loader's own comment) installs swe-rex via pipx on
   the container's existing Python instead — seconds, not minutes — which
   collapses both the compute cost and the prune-race window and is what makes
   fleet parallelism feasible.

## Why this is not a scientific-design change (causal argument)

swe-rex is the **command-relay shim**: during a rollout it runs an RPC server
inside the task container and executes the agent's bash/edit commands. The
resolve outcome is determined LATER and SEPARATELY by the official SWE-bench
evaluation harness, which takes the agent's final `model.patch`, applies it to a
fresh container built from the instance's base image, and runs the test suite.
**swe-rex is not present at scoring time.** The choice between a standalone
CPython and a pipx-installed swe-rex changes only which Python interpreter hosts
the relay server process; it does not change the model (gpt-5.6-luna), the
prompts, the tools, the task instance, the base repository/test environment the
agent observes, the seeds, the $3.00 per-instance ceiling, the arms, or the
evaluation harness. It is therefore causally disconnected from the resolve label
and introduces no bias, even where it correlates with arm.

Unchanged and binding: model `gpt-5.6-luna` for every call;
`completion_kwargs={"reasoning_effort":"none"}` (Amendment 1); task set
(`_exec100_instances.json`, seed 0, 50/50); baseline (`_sweagent_base`) vs
patched (`agents/08_sweagent` @ 7b1f047d, shipped prompt-60) artifacts; $3.00
per-instance ceiling; official Docker harness scoring; endpoints and
interpretation branches. No branch is suppressed.

## Config heterogeneity, recorded for full transparency

The protected runner's genuine rollouts (patched arm) used the standalone
(`/root`) method; those instances are locked and never reclaimed. All fleet
rollouts use the pipx (`""`) method. The final scored set will therefore contain
a minority of standalone-method patched rollouts (those the runner completed)
alongside pipx-method rollouts; per the causal argument above this does not
affect resolve outcomes. The exact per-instance method provenance is recorded
(worker/key labels in the scheduler; standalone vs pipx inferable from each
rollout's producer) and reported in REVISION_LOG_9.

## Validation before broad scale-out (directive F)

A single-instance pipx rollout (`django__django-13023`) completed genuine — 10
luna calls, 21,606 input / 77 output tokens, real submitted patch, measured cost
**$0.0024**, wall-clock 2:50. Two-sidecar validation then confirms atomic
non-duplicate claims and genuine completions before the full pool is activated.
Measured per-instance cost ($0.0024–$0.006) is far below the owner's $1.50
report trigger, so the $3.00 ceiling stands unchanged.

## Ledger integrity (unchanged from Amendment 1)

Progress counts a rollout ONLY when its trajectory shows successful model usage
(api_calls >= 1 AND nonzero input and output tokens); file existence never
implies completion. Reported live in `exec100_parallel_status.json`.
