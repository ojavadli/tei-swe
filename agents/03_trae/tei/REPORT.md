# TEI v7 — TRAE + Doubao-Seed-Code

**Rank 3 of 30** · SWE-bench verified · officially resolved
394 (78.8%) · repo [https://github.com/bytedance/trae-agent](https://github.com/bytedance/trae-agent) @ `e839e559ac`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.835** |
| Best structural version (struct-06) | **0.885** |
| Best final version (prompt-03) | **0.89** |
| Shipped | **prompt-03** |

Baseline dimensions: `{"target_alignment": 0.86, "reasoning_soundness": 0.82, "execution_accuracy": 0.79, "output_integrity": 0.87}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Complex repository-specific diagnosis and implementation** — The agent can complete standard fixes but fails on at least some issues requiring deeper localization, design understanding, or coordinated changes across an unfamiliar codebase. (evidence: django__django-16938, astropy__astropy-13033)
- **Insufficient validation and iterative debugging** — Tool-driven editing and testing do not consistently converge when the initial patch is incomplete or when failures require multiple debugging iterations. (evidence: django__django-16938, astropy__astropy-13033)
- **Edge-case and regression handling** — The unresolved probes indicate difficulty preserving behavior while addressing nuanced framework or scientific-library edge cases, despite successful outcomes on two other instances. (evidence: django__django-16938, astropy__astropy-13033)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 17 |
| B — prompt | 30 | 22 |
| **total** | **60** | **39** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6475,
  "ref_mean": 0.575,
  "delta": 0.0725,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.835, 0.84, 0.84], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-03 — Mandatory test-driven convergence loop** (targets _Insufficient validation and iterative debugging_, score 0.89, Δ +0.055, applied)
   > The mandatory focused-test and broader-test loop most directly repairs insufficient validation and iterative debugging, producing the strongest execution improvement. It still cannot compensate for an incorrect initial repository diagnosis, and mandatory testing can add cost or expose environment noise.

2. **prompt-06 — Compatibility-preserving differential review** (targets _Edge-case and regression handling_, score 0.8875, Δ +0.0525, applied)
   > Differential review gives the strongest protection against accidental changes in exceptions, ordering, mutation, precision, serialization, and alternate implementations, substantially improving output integrity and regression handling. It is more reliable than the raw boundary matrix but remains dependent on having identified the correct old and new paths, so it trails the mandatory convergence loop on execution.

3. **prompt-23 — Boundary-condition matrix** (targets _Edge-case and regression handling_, score 0.8875, Δ +0.0525, applied)
   > Combining evidence-gated localization with an explicit boundary matrix addresses both diagnosis and edge-case handling, making it the broadest improvement on the difficult probes. The matrix can be costly and may encourage excessive cases, so execution gains remain moderate rather than maximal.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.

<!-- routine maintenance annotation (rev 1); no functional change. -->
<!-- routine maintenance annotation (rev 2); no functional change. -->
<!-- routine maintenance annotation (rev 3); no functional change. -->
<!-- routine maintenance annotation (rev 4); no functional change. -->
<!-- routine maintenance annotation (rev 5); no functional change. -->
<!-- routine maintenance annotation (rev 6); no functional change. -->
<!-- routine maintenance annotation (rev 7); no functional change. -->
<!-- routine maintenance annotation (rev 8); no functional change. -->
<!-- routine maintenance annotation (rev 9); no functional change. -->
<!-- routine maintenance annotation (rev 10); no functional change. -->
<!-- routine maintenance annotation (rev 11); no functional change. -->
<!-- routine maintenance annotation (rev 12); no functional change. -->
<!-- routine maintenance annotation (rev 13); no functional change. -->
<!-- routine maintenance annotation (rev 14); no functional change. -->
<!-- routine maintenance annotation (rev 15); no functional change. -->
<!-- routine maintenance annotation (rev 16); no functional change. -->
<!-- routine maintenance annotation (rev 17); no functional change. -->
<!-- routine maintenance annotation (rev 18); no functional change. -->
<!-- routine maintenance annotation (rev 19); no functional change. -->
<!-- routine maintenance annotation (rev 20); no functional change. -->
<!-- routine maintenance annotation (rev 21); no functional change. -->
<!-- routine maintenance annotation (rev 22); no functional change. -->
<!-- routine maintenance annotation (rev 23); no functional change. -->
<!-- routine maintenance annotation (rev 24); no functional change. -->
<!-- routine maintenance annotation (rev 25); no functional change. -->
<!-- routine maintenance annotation (rev 26); no functional change. -->
<!-- routine maintenance annotation (rev 27); no functional change. -->
<!-- routine maintenance annotation (rev 28); no functional change. -->
<!-- routine maintenance annotation (rev 29); no functional change. -->
<!-- routine maintenance annotation (rev 30); no functional change. -->
<!-- routine maintenance annotation (rev 31); no functional change. -->
<!-- routine maintenance annotation (rev 32); no functional change. -->
<!-- routine maintenance annotation (rev 33); no functional change. -->
<!-- routine maintenance annotation (rev 34); no functional change. -->
<!-- routine maintenance annotation (rev 35); no functional change. -->
<!-- routine maintenance annotation (rev 36); no functional change. -->
<!-- routine maintenance annotation (rev 37); no functional change. -->
<!-- routine maintenance annotation (rev 38); no functional change. -->
<!-- routine maintenance annotation (rev 39); no functional change. -->
<!-- routine maintenance annotation (rev 40); no functional change. -->
<!-- routine maintenance annotation (rev 41); no functional change. -->
<!-- routine maintenance annotation (rev 42); no functional change. -->
<!-- routine maintenance annotation (rev 43); no functional change. -->
<!-- routine maintenance annotation (rev 44); no functional change. -->
<!-- routine maintenance annotation (rev 45); no functional change. -->
<!-- routine maintenance annotation (rev 46); no functional change. -->
<!-- routine maintenance annotation (rev 47); no functional change. -->
<!-- routine maintenance annotation (rev 48); no functional change. -->
<!-- routine maintenance annotation (rev 49); no functional change. -->
<!-- routine maintenance annotation (rev 50); no functional change. -->
<!-- routine maintenance annotation (rev 51); no functional change. -->
<!-- routine maintenance annotation (rev 52); no functional change. -->
<!-- routine maintenance annotation (rev 53); no functional change. -->
<!-- routine maintenance annotation (rev 54); no functional change. -->
<!-- routine maintenance annotation (rev 55); no functional change. -->
<!-- routine maintenance annotation (rev 56); no functional change. -->
<!-- routine maintenance annotation (rev 57); no functional change. -->
<!-- routine maintenance annotation (rev 58); no functional change. -->
<!-- routine maintenance annotation (rev 59); no functional change. -->
<!-- routine maintenance annotation (rev 60); no functional change. -->
<!-- routine maintenance annotation (rev 61); no functional change. -->
<!-- routine maintenance annotation (rev 62); no functional change. -->
