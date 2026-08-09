# TEI v7 — SWE-Exp

**Rank 20 of 30** · SWE-bench verified · officially resolved
210 (42.0%) · repo [https://github.com/YerbaPage/SWE-Exp](https://github.com/YerbaPage/SWE-Exp) @ `6b5c92ed0a`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.5175** |
| Best structural version (struct-07) | **0.57** |
| Best final version (prompt-11) | **0.5875** |
| Shipped | **prompt-11** |

Baseline dimensions: `{"target_alignment": 0.58, "reasoning_soundness": 0.5, "execution_accuracy": 0.43, "output_integrity": 0.56}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **End-to-end repair failure** — The system did not produce a verified resolution for these benchmark instances, consistent with execution accuracy being the principal weakness. (evidence: django__django-14122, django__django-14351)
- **Unreliable transfer across issue types and repositories** — Despite an experience-learning and retrieval design, the fixed probes show successful handling on some tasks but failure on two Django tasks, indicating inconsistent generalization. (evidence: django__django-13109, sympy__sympy-17655, django__django-14122, django__django-14351)
- **Insufficiently robust completion under difficult cases** — The unresolved outcomes indicate that the default trajectory, reasoning, or validation process can terminate without a correct patch even when the system is aimed at issue resolution. (evidence: django__django-14122, django__django-14351)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 10 |
| B — prompt | 12 | 0 |
| **total** | **24** | **10** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5175,
  "ref_mean": 0.46,
  "delta": 0.0575,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.5175, 0.5225, 0.5125], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-11 — Behavioral invariant decomposition** (targets _End-to-end repair failure_, score 0.5875, Δ +0.07, proposed_not_applied)
   > Explicit current-versus-intended behavior, distinguishing inputs, invariants, and regression risks gives the strongest improvement in target alignment and reasoning. It can improve difficult repairs, though decomposition alone cannot ensure the patch is correctly executed.

2. **prompt-07 — Test-first repair contract** (targets _End-to-end repair failure_, score 0.5725, Δ +0.055, proposed_not_applied)
   > The test-first contract improves requirement extraction, localization, and verification, directly reducing incomplete repairs. Gains are modest because it does not itself provide stronger recovery for difficult or misleading issues.

3. **prompt-12 — Mandatory completion and verification checklist** (targets _Insufficiently robust completion under difficult cases_, score 0.5725, Δ +0.055, proposed_not_applied)
   > The completion checklist directly improves verification, production-path correctness, and final-diff integrity, making it valuable for end-to-end completion. It is less effective at discovering the right behavioral hypothesis, so reasoning and target gains remain limited.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
