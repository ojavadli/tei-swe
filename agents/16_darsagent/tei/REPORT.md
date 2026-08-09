# TEI v7 — DARS Agent

**Rank 16 of 30** · SWE-bench lite · officially resolved
141 (47.0%) · repo [https://github.com/darsagent/DARS-Agent](https://github.com/darsagent/DARS-Agent) @ `eab35168a9`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.58** |
| Best structural version (struct-06) | **0.6275** |
| Best final version (prompt-06) | **0.645** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.65, "reasoning_soundness": 0.52, "execution_accuracy": 0.47, "output_integrity": 0.68}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to complete repository changes on difficult instances** — Both SymPy probes were unresolved, indicating that the agent frequently fails to carry an issue through to a correct completed patch. (evidence: sympy__sympy-19007, sympy__sympy-16988)
- **Insufficient issue-specific reasoning or generalization** — The unresolved SymPy outcomes suggest weaker analysis of domain-specific behavior and edge cases than is needed for reliable SWE-bench performance. (evidence: sympy__sympy-19007, sympy__sympy-16988)
- **Inadequate validation of proposed fixes** — The two unresolved outcomes are consistent with trajectories that do not reliably validate and refine changes until the task is actually solved. (evidence: sympy__sympy-19007, sympy__sympy-16988)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 9 |
| B — prompt | 12 | 9 |
| **total** | **24** | **18** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.55,
  "ref_mean": 0.5,
  "delta": 0.05,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.58, 0.58, 0.58], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-06 — Acceptance-criteria checklist and final audit** (targets _Failure to complete repository changes on difficult instances_, score 0.645, Δ +0.065, applied)
   > The final checklist and diff audit most clearly improve output integrity, omission detection, and avoiding accidental edits. It is largely a finishing control rather than a mechanism for discovering the correct difficult fix, so reasoning and hard-instance gains remain limited.

2. **prompt-04 — Semantic oracle construction** (targets _Insufficient issue-specific reasoning or generalization_, score 0.635, Δ +0.055, applied)
   > Constructing an explicit semantic oracle is the strongest improvement for contract-sensitive and symbolic bugs, producing the best reasoning score. It is narrower than the validation and completion techniques, and can overemphasize pre-edit analysis, so execution falls below baseline.

3. **prompt-01 — Definition-of-done gate** (targets _Failure to complete repository changes on difficult instances_, score 0.6325, Δ +0.0525, applied)
   > The definition-of-done gate directly addresses premature termination and should improve completion, regression coverage, and final repository state. Its broad acceptance language adds useful execution discipline but only modestly improves issue-specific reasoning.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
