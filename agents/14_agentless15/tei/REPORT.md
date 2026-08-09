# TEI v7 — Agentless-1.5 + Claude-3.5 Sonnet (20241022)

**Rank 14 of 30** · SWE-bench verified · officially resolved
254 (50.8%) · repo [https://github.com/OpenAutoCoder/Agentless](https://github.com/OpenAutoCoder/Agentless) @ `5ce5888b9f`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.59** |
| Best structural version (struct-05) | **0.665** |
| Best final version (struct-05) | **0.665** |
| Shipped | **struct-05** |

Baseline dimensions: `{"target_alignment": 0.62, "reasoning_soundness": 0.55, "execution_accuracy": 0.51, "output_integrity": 0.68}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Localization and repair failure on repository-specific behavior** — The system can complete some fixes, but its unresolved outcomes on pytest and seaborn indicate recurring difficulty mapping issue descriptions to the correct implementation and producing a behaviorally correct patch. (evidence: pytest-dev__pytest-6197, mwaskom__seaborn-3069)
- **Insufficient regression-test or reproduction-test guidance** — The explicit test-selection and reproduction-generation stages do not reliably prevent incorrect or incomplete fixes, particularly for the unresolved pytest and seaborn issues. (evidence: pytest-dev__pytest-6197, mwaskom__seaborn-3069)
- **Brittle end-to-end patch validation across projects** — The pipeline's validation can succeed on selected instances but does not generalize reliably across the benchmark's varied repositories, as shown by two unresolved probes despite the successful astropy and django cases. (evidence: pytest-dev__pytest-6197, mwaskom__seaborn-3069, astropy__astropy-13453, django__django-15104)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 5 |
| B — prompt | 18 | 11 |
| **total** | **36** | **16** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5675,
  "ref_mean": 0.5,
  "delta": 0.0675,
  "wins": 4,
  "losses": 0,
  "sign_p": 0.125,
  "margin_hoeffding": 0.679,
  "mde": 0.297,
  "insufficient_n": false,
  "accept": true,
  "reason": "mean not below reference; 4W/0L paired (sign p=0.125)",
  "preflight": "Power check: with 4 eval queries, only mean-score changes >= ~0.30 are statistically meaningful; smaller deltas are within judge noise. (~36 queries would certify a 0.10 gain.)"
}
```

Paraphrase noise floor: `{"paraphrase_aggregates": [0.59, 0.59, 0.59], "noise_floor": 0.0}`


## Top 3 why-records

1. **struct-05 — Constrain generated reproductions to repository APIs and test conventions** (targets _Localization and repair failure on repository-specific behavior_, score 0.665, Δ +0.075, applied)
   > Requiring repository-present APIs, fixtures, and conventions most directly addresses repository-specific localization and repair failures, especially on the weak probes; the strict constraint can still block legitimate internal or less obvious entry points.

2. **prompt-16 — Executable behavior-contract reproduction** (targets _Insufficient regression-test or reproduction-test guidance_, score 0.6625, Δ +0.0725, applied)
   > The executable behavior contract forces explicit trigger conditions, pre-fix behavior, intended behavior, and boundaries before implementation. This is the strongest candidate for reducing reproduction ambiguity and improving project-specific reasoning, though it adds process overhead and still does not require independent end-to-end validation.

3. **prompt-18 — Validation gate with independent evidence** (targets _Brittle end-to-end patch validation across projects_, score 0.655, Δ +0.065, proposed_not_applied)
   > The two-stage unmodified-versus-patched gate and exact-command reporting materially improve validation reliability and output integrity, directly addressing brittle end-to-end checks. It does less to improve initial localization or repair reasoning, and requiring clean baseline execution can be impractical in repositories with unrelated failures.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
