# TEI v7 — CodeR + GPT 4 (1106)

**Rank 28 of 30** · SWE-bench lite · officially resolved
85 (28.33%) · repo [https://github.com/NL2Code/CodeR](https://github.com/NL2Code/CodeR) @ `d63468344b`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (no source code in linked repo). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.4625** |
| Best structural version (struct-12) | **0.5025** |
| Best final version (prompt-02) | **0.5075** |
| Shipped | **prompt-02** |

Baseline dimensions: `{"target_alignment": 0.48, "reasoning_soundness": 0.43, "execution_accuracy": 0.38, "output_integrity": 0.56}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete fault localization** — The system's localization stage is prompt-driven and the unresolved Astropy and Django probes indicate that it often fails to identify the correct edit locations or relevant call paths. (evidence: astropy__astropy-14995, django__django-11848)
- **Patch implementation and test-execution failures** — Despite dedicated reproducer and verifier roles, the low overall 28.33% resolve rate and both unresolved probes indicate frequent failures converting understanding into a correct patch that passes the relevant tests. (evidence: astropy__astropy-14995, django__django-11848)
- **Insufficient validation or generalization** — The one-submission setting and unresolved probes suggest that verification does not reliably catch incomplete fixes, regressions, or behavior outside the reproduced case. (evidence: astropy__astropy-14995, django__django-11848)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 0 |
| B — prompt | 12 | 12 |
| **total** | **24** | **12** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5,
  "ref_mean": 0.4475,
  "delta": 0.0525,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.4625, 0.4675, 0.46], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-02 — Issue-to-code trace with localization stopping criteria** (targets _Incorrect or incomplete fault localization_, score 0.5075, Δ +0.045, applied)
   > Tracing from the public entry point to the observed failure with an explicit stopping criterion is a more concrete localization improvement than candidate ranking alone. It modestly raises target alignment and reasoning, but provides little direct protection against implementation and validation failures.

2. **prompt-06 — Post-fix regression matrix with independent confirmation** (targets _Insufficient validation or generalization_, score 0.5075, Δ +0.045, applied)
   > Independent confirmation across the reproducer, regression tests, and neighboring cases best addresses insufficient validation and generalization. The indentation warning also reduces edit-format failures. Gains are strongest on probes requiring regression confidence, though the matrix adds time and can expose unrelated test instability.

3. **prompt-11 — Behavioral boundary matrix** (targets _Insufficient validation or generalization_, score 0.505, Δ +0.0425, applied)
   > The behavioral contract and boundary matrix improve validation, regression awareness, and output integrity, with moderate reasoning gains. The approach depends on constructing reliable reproducers and does not itself ensure accurate patch execution, so execution remains only modestly above baseline.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
