# TEI v7 — Moatless Tools + Claude 4 Sonnet

**Rank 7 of 30** · SWE-bench verified · officially resolved
354 (70.8%) · repo [https://github.com/aorwall/moatless-tools](https://github.com/aorwall/moatless-tools) @ `011ead57a5`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.795** |
| Best structural version (struct-03) | **0.8425** |
| Best final version (prompt-18) | **0.85** |
| Shipped | **prompt-18** |

Baseline dimensions: `{"target_alignment": 0.83, "reasoning_soundness": 0.77, "execution_accuracy": 0.74, "output_integrity": 0.84}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to converge on repository-specific fixes** — The system can resolve some Django tasks but does not reliably translate investigation into a correct patch on other repositories. (evidence: pytest-dev__pytest-5840, mwaskom__seaborn-3187)
- **Insufficient iterative verification** — The strict single-action workflow supports controlled execution, but the unresolved probes indicate that investigation, editing, and validation do not consistently converge on passing behavior. (evidence: pytest-dev__pytest-5840, mwaskom__seaborn-3187)
- **Brittle cross-repository generalization** — The recorded outcomes show successful handling of both Django probes but failures on the pytest and seaborn probes, suggesting weaknesses that emerge across different codebase conventions and test ecosystems. (evidence: pytest-dev__pytest-5840, mwaskom__seaborn-3187)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 3 |
| B — prompt | 18 | 0 |
| **total** | **36** | **3** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6775,
  "ref_mean": 0.59,
  "delta": 0.0875,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.795, 0.795, 0.795], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-18 — Explicit completion contract** (targets _Insufficient iterative verification_, score 0.85, Δ +0.055, proposed_not_applied)
   > The explicit completion contract strongly improves execution accuracy and output integrity by requiring confirmation of the patch, targeted checks, and diff scope before completion. It helps prevent premature success declarations, though it contributes less to initial repository-specific diagnosis.

2. **struct-03 — Explicit post-edit convergence loop** (targets _Insufficient iterative verification_, score 0.8425, Δ +0.0475, proposed_not_applied)
   > The explicit post-edit test loop directly addresses non-convergence and weak verification, producing the strongest expected gains on the previously weak probes. The exactly-one-action constraint is somewhat rigid, preventing a larger improvement and occasionally adding overhead.

3. **prompt-10 — Patch-scope and invariant contract** (targets _Failure to converge on repository-specific fixes_, score 0.8375, Δ +0.0425, proposed_not_applied)
   > Requiring an explicit behavioral goal, preserved invariant, minimality rationale, and caller/subclass inspection should reduce repository-specific regressions and improve patch targeting. It raises reasoning and integrity more than execution because it still lacks a dedicated verification loop.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
