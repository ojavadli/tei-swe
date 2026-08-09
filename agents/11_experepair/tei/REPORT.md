# TEI v7 — ExpeRepair-v1.0 + Claude 4 Sonnet

**Rank 11 of 30** · SWE-bench lite · officially resolved
181 (60.33%) · repo [https://github.com/ExpeRepair/ExpeRepair](https://github.com/ExpeRepair/ExpeRepair) @ `5594f2c02c`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.705** |
| Best structural version (struct-06) | **0.775** |
| Best final version (struct-06) | **0.775** |
| Shipped | **struct-06** |

Baseline dimensions: `{"target_alignment": 0.74, "reasoning_soundness": 0.68, "execution_accuracy": 0.61, "output_integrity": 0.79}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect repository localization** — The search stage must select relevant editable files from the repository structure; failures on both Django probes are consistent with localization errors or incomplete cause analysis. (evidence: django__django-11620, django__django-12497)
- **Unreliable reproduction or validation judgment** — The system relies on generated reproduction tests and an LLM validation stage, creating a failure mode when tests are invalid, incomplete, or misinterpreted. (evidence: django__django-11620, django__django-12497)
- **Patch generation or execution failure** — The unresolved outcomes indicate that analysis did not consistently produce and successfully apply a correct repository-level fix, despite the multi-agent repair workflow. (evidence: django__django-11620, django__django-12497)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 0 |
| B — prompt | 18 | 13 |
| **total** | **36** | **13** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.605,
  "ref_mean": 0.53,
  "delta": 0.075,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.705, 0.705, 0.705], "noise_floor": 0.0}`


## Top 3 why-records

1. **struct-06 — Minimal-diff, regression-aware patch selection** (targets _Patch generation or execution failure_, score 0.775, Δ +0.07, proposed_not_applied)
   > Requiring an exact root cause, minimal repository-consistent changes, regression awareness, and validation combines useful safeguards against speculative or oversized patches. It improves execution and reasoning more than the baseline, but depends on earlier localization and reproduction being correct, so it is not a complete remedy.

2. **struct-05 — Patch application and changed-file integrity gate** (targets _Patch generation or execution failure_, score 0.7625, Δ +0.0575, proposed_not_applied)
   > Clean-application, changed-file, and test-integrity checks directly reduce patch execution failures and improve output integrity. They do not establish that the selected location or behavioral hypothesis is correct, so reasoning and the low-performing Django cases improve only modestly.

3. **prompt-06 — Patch application and semantic integrity checklist** (targets _Patch generation or execution failure_, score 0.7625, Δ +0.0575, applied)
   > The checklist directly addresses syntactic coherence, file existence, clean application, and semantic path coverage, producing the clearest improvement against patch execution failure. It does less to improve initial localization or issue interpretation than the evidence-first variants.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
