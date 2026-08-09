# TEI v7 — JoyCode + Claude 4 Sonnet + GPT-4.1

**Rank 5 of 30** · SWE-bench verified · officially resolved
373 (74.6%) · repo [https://github.com/jd-opensource/joycode-agent](https://github.com/jd-opensource/joycode-agent) @ `1bace2ab9f`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.8275** |
| Best structural version (struct-04) | **0.8675** |
| Best final version (prompt-19) | **0.885** |
| Shipped | **prompt-19** |

Baseline dimensions: `{"target_alignment": 0.86, "reasoning_soundness": 0.81, "execution_accuracy": 0.76, "output_integrity": 0.88}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to complete repository-specific fixes** — The system's patch-generation and execution pipeline did not resolve the Django 14170 and Sphinx 9229 tasks, showing residual failures despite the reported overall 74.6% resolution rate. (evidence: django__django-14170, sphinx-doc__sphinx-9229)
- **Insufficient recovery from failed attempts** — Although the repository emphasizes intelligent retries, test generation, and failure attribution, the recorded unresolved outcomes indicate that these mechanisms do not reliably recover from difficult instances. (evidence: django__django-14170, sphinx-doc__sphinx-9229)
- **Cross-project generalization gap** — The resolved Django and SymPy probes coexist with unresolved Django and Sphinx probes, indicating that success is not uniform across issue types and repository environments. (evidence: django__django-13023, sympy__sympy-24443, django__django-14170, sphinx-doc__sphinx-9229)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 22 |
| B — prompt | 30 | 24 |
| **total** | **60** | **46** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6125,
  "ref_mean": 0.5725,
  "delta": 0.04,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.8275, 0.835, 0.82], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-19 — Requirement-to-diff closure gate** (targets _Failure to complete repository-specific fixes_, score 0.885, Δ +0.0575, applied)
   > Strongly targets incomplete repository-specific fixes by forcing issue-to-code-path closure and explicit diff coverage. It improves difficult cases, though the checklist can become procedural without ensuring the chosen implementation is correct.

2. **prompt-22 — Verified-path execution contract** (targets _Failure to complete repository-specific fixes_, score 0.885, Δ +0.0575, applied)
   > Best execution-oriented change: it requires proof that verification imports the changed symbol and would fail before the patch, reducing false-positive test results. It improves both easy and hard probes, though it may miss behavior not covered by a narrowly chosen path.

3. **prompt-05 — Requirement-to-diff completeness gate** (targets _Failure to complete repository-specific fixes_, score 0.88, Δ +0.0525, proposed_not_applied)
   > A final requirement-to-diff gate directly catches omitted behaviors, missing tests, and unsupported acceptance criteria, producing the largest output-integrity improvement. It is primarily a verification mechanism, so it offers only modest execution gains and cannot repair an incorrect implementation by itself.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
