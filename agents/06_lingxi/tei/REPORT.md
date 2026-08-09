# TEI v7 — Lingxi-v1.5_claude-4-sonnet-20250514

**Rank 6 of 30** · SWE-bench verified · officially resolved
373 (74.6%) · repo [https://github.com/nimasteryang/Lingxi](https://github.com/nimasteryang/Lingxi) @ `1f2e5dc4c8`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.7675** |
| Best structural version (struct-09) | **0.805** |
| Best final version (prompt-17) | **0.835** |
| Shipped | **prompt-17** |

Baseline dimensions: `{"target_alignment": 0.79, "reasoning_soundness": 0.75, "execution_accuracy": 0.72, "output_integrity": 0.81}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incomplete issue localization and scope control** — The system can fail to identify all relevant files or the precise behavioral contract, leading to unresolved patches on repository-specific issues. (evidence: django__django-13794, sphinx-doc__sphinx-9229)
- **Insufficient framework-specific diagnosis** — Multi-agent analysis and historical guidance do not reliably produce a sound explanation for harder Django and Sphinx behaviors, resulting in incorrect or incomplete fixes. (evidence: django__django-13794, sphinx-doc__sphinx-9229)
- **Weak implementation validation and iteration** — The default workflow does not consistently catch failed assumptions through tests, focused reproduction, or follow-up edits; this is reflected by unresolved outcomes despite the available repository and editing tools. (evidence: django__django-13794, sphinx-doc__sphinx-9229)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 13 |
| B — prompt | 18 | 11 |
| **total** | **36** | **24** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.655,
  "ref_mean": 0.58,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.7675, 0.7725, 0.7625], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-17 — Failing-reproducer-first validation loop** (targets _Weak implementation validation and iteration_, score 0.835, Δ +0.0675, applied)
   > A behavioral contract followed by a failing-reproducer-first loop directly improves validation, regression awareness, and API preservation. This is the largest execution and output-integrity improvement, though it can delay patching when the reproduction is difficult to isolate.

2. **prompt-18 — Layered test, diff, and regression iteration** (targets _Weak implementation validation and iteration_, score 0.8225, Δ +0.055, applied)
   > Ordered reproducer, focused-test, regression, and diff gates provide strong implementation validation and iteration. The duplicated evidence-recording requirement and potentially expensive layered test sequence reduce efficiency and do not materially improve initial localization or framework diagnosis.

3. **prompt-15 — Framework execution-model diagnosis before patch design** (targets _Insufficient framework-specific diagnosis_, score 0.8175, Δ +0.05, applied)
   > Reconstructing lifecycle, dispatch, registries, inheritance, normalization, and caching before patching is the strongest direct response to framework-specific misdiagnosis. It raises reasoning and execution accuracy, with some risk of excessive analysis before producing a fix.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
