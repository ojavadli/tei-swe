# TEI v7 — CodeShellTester + GPT 4o (2024-05-13)

**Rank 25 of 30** · SWE-bench lite · officially resolved
94 (31.33%) · repo [https://github.com/WisdomShell/codeshell](https://github.com/WisdomShell/codeshell) @ `09d1adc88c`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (gpu/local-weights required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.3925** |
| Best structural version (struct-05) | **0.4525** |
| Best final version (struct-05) | **0.4525** |
| Shipped | **struct-05** |

Baseline dimensions: `{"target_alignment": 0.43, "reasoning_soundness": 0.37, "execution_accuracy": 0.32, "output_integrity": 0.45}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to produce a correct repository patch** — The system did not resolve the xarray and SymPy instances, indicating repeated inability to translate its analysis into a patch that satisfies the repository tests. (evidence: pydata__xarray-4094, sympy__sympy-17139)
- **Weak generalization across project ecosystems** — Performance was successful on the two Django probes but failed on both non-Django probes, suggesting limited robustness when adapting to different codebases and conventions. (evidence: django__django-11620, django__django-11583, pydata__xarray-4094, sympy__sympy-17139)
- **Insufficient debugging and validation** — The unresolved outcomes on two probes provide evidence that diagnosis, test-driven iteration, or final validation was not reliable enough for consistent SWE-bench completion. (evidence: pydata__xarray-4094, sympy__sympy-17139)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 0 |
| B — prompt | 12 | 0 |
| **total** | **24** | **0** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.415,
  "ref_mean": 0.395,
  "delta": 0.02,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.3925, 0.4, 0.3925], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **struct-05 — Require semantic diff validation before submission, including checking that the diff is non-empty, touches the diagnosed code path, preserves public APIs, and contains no unrelated edits** (targets _Failure to produce a correct repository patch_, score 0.4525, Δ +0.06, proposed_not_applied)
   > Semantic diff checks most directly improve output integrity by detecting empty, unrelated, or API-breaking patches. They are post-edit safeguards rather than a solution to diagnosis or ecosystem differences, and the repository exposes no submission validator to execute them.

2. **prompt-10 — Test-first failure reproduction loop** (targets _Insufficient debugging and validation_, score 0.4525, Δ +0.06, proposed_not_applied)
   > The mandatory reproduce-edit-rerun loop directly addresses the diagnosed debugging and validation failure, producing the strongest execution gains, especially on the weak xarray and SymPy probes. It may add friction when tests are difficult to isolate, and it does not substantially improve repository interpretation by itself.

3. **prompt-12 — Final patch audit with executable acceptance criteria** (targets _Failure to produce a correct repository patch_, score 0.4525, Δ +0.06, proposed_not_applied)
   > The final diff and acceptance-criteria gate most directly improves patch translation and reporting integrity, reducing cases where analysis is not reflected in the submitted change. It provides moderate execution gains through required tests, but is weaker than test-first reproduction for discovering the actual defect.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
