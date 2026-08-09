# TEI v7 — AgentScope

**Rank 9 of 30** · SWE-bench verified · officially resolved
317 (63.4%) · repo [https://github.com/modelscope/agentscope](https://github.com/modelscope/agentscope) @ `29b592358c`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.6375** |
| Best structural version (struct-06) | **0.705** |
| Best final version (prompt-10) | **0.715** |
| Shipped | **prompt-10** |

Baseline dimensions: `{"target_alignment": 0.68, "reasoning_soundness": 0.62, "execution_accuracy": 0.6, "output_integrity": 0.65}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Cross-repository generalization failure** — The system resolved both Django probes but failed on the Sphinx and Seaborn probes, indicating inconsistent transfer across repository ecosystems. (evidence: sphinx-doc__sphinx-8056, mwaskom__seaborn-3187)
- **Insufficient issue-specific patch execution** — The unresolved Sphinx and Seaborn outcomes suggest that identifying or implementing the required repository-specific changes is unreliable. (evidence: sphinx-doc__sphinx-8056, mwaskom__seaborn-3187)
- **Weak validation of completed fixes** — The two unresolved outcomes indicate that the default workflow does not consistently produce a verified, task-complete result outside the successful Django cases. (evidence: sphinx-doc__sphinx-8056, mwaskom__seaborn-3187)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 13 |
| B — prompt | 18 | 7 |
| **total** | **36** | **20** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6375,
  "ref_mean": 0.545,
  "delta": 0.0925,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.6375, 0.645, 0.6375], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-10 — Reproduction-first and test-driven patching** (targets _Insufficient issue-specific patch execution_, score 0.715, Δ +0.0775, proposed_not_applied)
   > Reproduction-first patching most directly addresses the diagnosed execution failure: it ties the change to observed behavior and creates a regression guard, with especially large expected gains on the weaker repositories. It still lacks the explicit final validation and adversarial diff review of later variants.

2. **struct-06 — Diff-and-regression audit** (targets _Weak validation of completed fixes_, score 0.705, Δ +0.0675, applied)
   > The final diff and regression audit gives the strongest output integrity and catches unintended edits, compatibility problems, missing tests, and ambiguous validation claims. It improves execution and the weak probes, but is slightly less forceful than the iterative barrier about repairing a failing implementation.

3. **prompt-11 — Explicit validation gate** (targets _Weak validation of completed fixes_, score 0.7025, Δ +0.065, proposed_not_applied)
   > The explicit validation gate materially improves output integrity by requiring narrow regression tests, broader relevant tests, and inspection of failures before completion. It does less to improve initial issue interpretation or patch construction, so execution gains are smaller than with reproduction-first patching.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
