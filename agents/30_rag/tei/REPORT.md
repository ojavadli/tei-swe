# TEI v7 — RAG + Claude 3 Opus

**Rank 30 of 30** · SWE-bench verified · officially resolved
35 (7.0%) · repo [https://github.com/SWE-bench/SWE-bench](https://github.com/SWE-bench/SWE-bench) @ `cd37836ffe`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.21** |
| Best structural version (struct-10) | **0.26** |
| Best final version (prompt-12) | **0.2725** |
| Shipped | **prompt-12** |

Baseline dimensions: `{"target_alignment": 0.24, "reasoning_soundness": 0.2, "execution_accuracy": 0.08, "output_integrity": 0.32}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Low instance-level solve reliability** — The system resolves only 35 verified instances, a 7.0% rate, indicating that successful issue understanding does not consistently become a correct repository change. (evidence: django__django-16116, pydata__xarray-3677)
- **Weak cross-instance generalization** — It resolves one Django instance but fails another, showing that success on a repository or framework does not reliably transfer to a different issue in the same codebase. (evidence: django__django-10914, django__django-16116)
- **Inconsistent cross-repository execution** — The system succeeds on the SymPy probe but fails on the Xarray probe, indicating unreliable adaptation to repository-specific code, tests, and conventions. (evidence: sympy__sympy-21847, pydata__xarray-3677)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 8 |
| B — prompt | 12 | 4 |
| **total** | **24** | **12** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.4875,
  "ref_mean": 0.435,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.21, 0.21, 0.2125], "noise_floor": 0.0025}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-12 — Mandatory patch verification loop** (targets _Weak cross-instance generalization_, score 0.2725, Δ +0.0625, proposed_not_applied)
   > The verification loop combines falsifiable diagnosis, full-diff requirement review, focused testing, and failure interpretation, giving the broadest practical improvement across reliability and generalization. Gains remain modest because it depends on the preceding analysis being accurate and may impose substantial process overhead.

2. **struct-10 — Impose an iterative validation-and-repair loop, requiring focused tests first, inspection of failures, a patch correction, and then a broader regression check.** (targets _Low instance-level solve reliability_, score 0.26, Δ +0.05, proposed_not_applied)
   > The focused-test, failure-inspection, repair, and regression sequence most directly improves solve reliability and catches implementation mistakes before completion. It is the strongest candidate, though requiring a regression test can add friction when the repository has unusual test setup or the reported failure is difficult to reproduce.

3. **prompt-06 — Patch-integrity and regression audit** (targets _Inconsistent cross-repository execution_, score 0.2575, Δ +0.0475, proposed_not_applied)
   > A minimal-root-cause plan followed by patch and regression auditing most directly reduces accidental edits, missed regressions, and incomplete final reporting. It gives the strongest execution and output-integrity improvement, though its extra audit steps provide only modest additional target and reasoning gains.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
