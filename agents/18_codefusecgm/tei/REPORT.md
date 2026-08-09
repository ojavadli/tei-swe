# TEI v7 — CodeFuse-CGM

**Rank 18 of 30** · SWE-bench lite · officially resolved
132 (44.0%) · repo [https://github.com/codefuse-ai/CodeFuse-CGM](https://github.com/codefuse-ai/CodeFuse-CGM) @ `2c12754ade`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.5925** |
| Best structural version (struct-10) | **0.6425** |
| Best final version (struct-10) | **0.6425** |
| Shipped | **struct-10** |

Baseline dimensions: `{"target_alignment": 0.68, "reasoning_soundness": 0.56, "execution_accuracy": 0.49, "output_integrity": 0.64}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Repository localization or retrieval misses** — The graph-based retrieval and reranking pipeline does not consistently identify the files needed for the issue, as indicated by unresolved Django and SymPy probes. (evidence: django__django-15738, sympy__sympy-16503)
- **Issue-specific diagnosis is insufficiently reliable** — The system's general repository-level prompting and model reasoning do not reliably translate issue descriptions into a correct implementation diagnosis on harder instances. (evidence: django__django-15738, sympy__sympy-16503)
- **End-to-end patch execution or validation failure** — Despite an architecture aimed at repository-level code changes, the default system fails to produce an accepted solution on two of the four recorded probes, reflecting weak execution reliability. (evidence: django__django-15738, sympy__sympy-16503)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 11 |
| B — prompt | 12 | 11 |
| **total** | **24** | **22** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6175,
  "ref_mean": 0.545,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.5925, 0.595, 0.5925], "noise_floor": 0.0025}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **struct-10 — Counterexample and regression-contract reasoning** (targets _Issue-specific diagnosis is insufficiently reliable_, score 0.6425, Δ +0.05, applied)
   > Regression-contract and counterexample reasoning improves reproduction, invariant definition, test selection, and the completeness of the final plan. It raises execution and output integrity more than localization, while still depending on the initial diagnosis.

2. **struct-09 — Forced causal diagnosis before file ranking** (targets _Issue-specific diagnosis is insufficiently reliable_, score 0.64, Δ +0.0475, applied)
   > The explicit symptom-to-cause chain substantially improves issue-specific diagnosis and gives patch execution a clearer basis. It slightly improves localization and reporting, but causal hypotheses can still be wrong when repository evidence is ambiguous.

3. **prompt-08 — Contradiction-aware retrieval** (targets _Repository localization or retrieval misses_, score 0.6325, Δ +0.04, applied)
   > Competing localization hypotheses reduce premature commitment and are the strongest retrieval improvement, especially on ambiguous or difficult repositories, though the extra ranking step adds limited execution benefit.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
