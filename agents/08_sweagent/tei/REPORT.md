# TEI v7 — SWE-agent + Claude 4 Sonnet

**Rank 8 of 30** · SWE-bench verified · officially resolved
333 (66.6%) · repo [https://github.com/SWE-agent/SWE-agent](https://github.com/SWE-agent/SWE-agent) @ `3ea751c087`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.7075** |
| Best structural version (struct-16) | **0.765** |
| Best final version (prompt-06) | **0.7675** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.74, "reasoning_soundness": 0.69, "execution_accuracy": 0.64, "output_integrity": 0.76}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete repository changes** — The system can fail to turn an otherwise plausible approach into a patch that resolves the issue, as shown by unresolved outcomes on both Django and xarray. (evidence: django__django-13112, pydata__xarray-6599)
- **Insufficient validation and iteration** — The retry/tool-driven setup does not reliably detect and repair remaining defects before submission, evidenced by two unresolved probe instances despite the system's generally capable agent configuration. (evidence: django__django-13112, pydata__xarray-6599)
- **Difficulty with repository-specific edge cases** — Performance is not uniformly reliable across projects: Sphinx and Matplotlib were resolved, while Django and xarray were not, indicating recurring sensitivity to project semantics and edge-case behavior. (evidence: django__django-13112, pydata__xarray-6599)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 11 |
| B — prompt | 18 | 11 |
| **total** | **36** | **22** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6125,
  "ref_mean": 0.565,
  "delta": 0.0475,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.7075, 0.7075, 0.7075], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-06 — Failure-triage and iterative repair protocol** (targets _Insufficient validation and iteration_, score 0.7675, Δ +0.06, proposed_not_applied)
   > Baseline establishment, narrow checks, explicit failure classification, and iterative repair provide the most complete response to insufficient validation. It can still misclassify environment or expectation failures and does not explicitly require comprehensive boundary analysis, so gains remain moderate.

2. **prompt-09 — Repository-convention reconnaissance** (targets _Difficulty with repository-specific edge cases_, score 0.7675, Δ +0.06, proposed_not_applied)
   > Reconnaissance is well matched to repository-specific edge cases and should improve API, compatibility, and error-handling decisions in the difficult probes. It can still lead to analysis without sufficient validation, so execution improvement is smaller than with the validation-gate candidate.

3. **prompt-11 — Minimal-diff semantic preservation** (targets _Incorrect or incomplete repository changes_, score 0.7675, Δ +0.06, applied)
   > Minimal, invariant-preserving changes reduce regressions and improve output integrity, particularly for already well-understood fixes. The conservative approach can under-address multi-branch or repository-specific requirements, so gains on the hardest xarray case are limited and execution remains only modestly above baseline.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
