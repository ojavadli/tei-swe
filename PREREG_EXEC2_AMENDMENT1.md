# Amendment 1 to PREREG_EXEC2 (correction only; original prereg and tag unchanged)

Registered 2026-08-10, AFTER the initial Phase-C launch failed at the integration
layer and BEFORE any successful Phase-C experimental rollout. Tagged
`prereg-exec2-amend1`. The original `PREREG_EXEC2.md` and its tag `prereg-exec2`
are preserved unchanged; every scientific design element there (system, arms,
artifacts, backbone, instance set, seeds, endpoints, interpretation branches)
remains in force.

## What happened (recorded evidence)

The initial launch produced **zero experimental observations and zero scored
outcomes**: every produced trajectory file is a startup-error stub —
`exit_status=exit_error`, **0 successful OpenAI API calls, 0 input tokens,
0 output tokens, $0.00 model spend, empty submissions** (census:
`_exec100_stub_census.json` — 58 patched-arm stubs, 0 baseline trajectories;
stub directories preserved verbatim as `_exec100_stubs_launch1_patched/`,
`_exec100_stubs_launch1_baseline/`, log `exec100_stubs_launch1.log`). These
files are historical diagnostic artifacts of a failed launch and are never
counted as rollouts. A secondary fault (colima VM disk exhaustion causing
DockerPullError fast-fails) was remediated during diagnosis with an image
pruning daemon; it is moot to the primary fault below.

## Root cause and the integration correction (the ONLY change)

Every model call was rejected by the API:
`OpenAIException — Function tools with reasoning_effort are not supported for
gpt-5.6-luna in /v1/chat/completions`.

Live diagnostic probes with the study key (2 calls, gpt-5.6-luna, 64-token cap,
recorded here as diagnostic — not experimental — usage) established:

- **P1 — omitting `reasoning_effort` entirely: still rejected** with the same
  400. The server applies an implicit reasoning mode to this model on
  `/v1/chat/completions` and rejects function tools in that mode, so omission
  cannot fix it.
- **P2 — explicit `reasoning_effort="none"`: succeeds** (47 input / 17 output
  tokens, 1 function tool call executed).

The Responses API route was evaluated and ruled out on the preregistered
stack: the installed SWE-agent (1.4.0) drives its tool loop exclusively
through `litellm.completion` (no Responses support); adopting it would be an
invasive behavioral change to the agent under test.

**Correction adopted:** both arms run Chat Completions with
`--agent.model.completion_kwargs '{"reasoning_effort": "none"}'` — the API's
documented value that disables the implicit reasoning mode and re-enables
function tools. Identical in baseline and patched arms. The model remains
`gpt-5.6-luna` for every call. No change to the task set, artifacts, seeds,
harness, endpoints, or interpretation branches.

## Ceiling (unchanged) and the measured-cost report trigger

The **$3.00 per-instance termination ceiling is unchanged**. It is
per-instance, is ~10x the published §10 arms ($0.30–$0.35 per instance), and
was never binding: all 57+ exits were startup errors; zero were cost-cap
exits. No additional or replacement termination rule is introduced. Per the
owner's standing instruction: the smoke test below reports the measured
per-instance cost of a COMPLETED luna rollout; if it exceeds $1.50 (half the
ceiling), the full arm is NOT launched until the owner decides on measured
evidence; if at or below $1.50, the $3.00 ceiling stands and nothing further
is preregistered.

## Smoke test (not an experimental observation)

One designated instance — `astropy__astropy-14096`, the first of the frozen
set — runs once with the exact repaired configuration on the PATCHED artifact,
into the separate directory `_exec100_smoke/` (never merged with experimental
outputs; the full arm re-runs this instance fresh). Pass requires: ≥1
successful gpt-5.6-luna response; nonzero input and output tokens; ≥1
successfully executed tool call; no 400 involving reasoning_effort/tools.

## Instrumentation corrections (defect was the progress ledger itself)

1. **Genuine-rollout ledger:** progress counts a rollout ONLY if its
   trajectory shows successful model usage (`api_calls ≥ 1` AND input and
   output tokens > 0). Status reports separately: genuine completed
   rollouts/200, error stubs, successful luna calls, input tokens, output
   tokens, measured spend, baseline vs patched counts, and harness-scored
   pairs. A `.traj` file's existence proves nothing.
2. **Retry-loop fix:** round cleanup now clears instance directories whose
   trajectory is missing, is a zero-usage stub, or exited `exit_error`, so
   failed instances actually re-run (the original loop cleared only
   trajectory-less directories and would have skipped every stub).

All 100 baseline + 100 patched rollouts run fresh from the preregistered
instance set (zero genuine rollouts existed before this amendment); both arms
under identical execution conditions; resumable per-instance records; scoring
exactly as preregistered.
