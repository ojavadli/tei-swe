# TEI v7 — Aider + GPT 4o & Claude 3 Opus

**Rank 29 of 30** · SWE-bench lite · officially resolved
79 (26.33%) · repo [https://github.com/paul-gauthier/aider](https://github.com/paul-gauthier/aider) @ `5dc9490bb3`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.415** |
| Best structural version (struct-10) | **0.445** |
| Best final version (prompt-12) | **0.465** |
| Shipped | **prompt-12** |

Baseline dimensions: `{"target_alignment": 0.47, "reasoning_soundness": 0.4, "execution_accuracy": 0.34, "output_integrity": 0.45}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Complex semantic reasoning failure** — The system did not reach a resolved patch on the SymPy instance, indicating difficulty tracing and implementing nontrivial behavioral changes across a complex codebase. (evidence: sympy__sympy-16792)
- **Failure to satisfy behavioral edge cases** — The unresolved Pytest instance suggests insufficient attention to exact expected behavior and regression-test requirements. (evidence: pytest-dev__pytest-5413)
- **Insufficient iterative validation and recovery** — Both unresolved probes show that the system can fail to recover from an initially incomplete or incorrect edit through testing and follow-up corrections. (evidence: sympy__sympy-16792, pytest-dev__pytest-5413)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 9 |
| B — prompt | 12 | 0 |
| **total** | **24** | **9** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5475,
  "ref_mean": 0.49,
  "delta": 0.0575,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.415, 0.42, 0.4125], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-12 — Add a completion gate with diff, test, and scope checks** (targets _Insufficient iterative validation and recovery_, score 0.465, Δ +0.05, proposed_not_applied)
   > The completion gate materially improves diff discipline, test coverage, focused validation, and broader-suite verification. It is among the strongest changes for execution and output integrity and helps all probes, but it occurs late and cannot fully repair flawed initial semantic reasoning.

2. **prompt-09 — Mandate a failing-test-to-fix-to-regression-test loop** (targets _Insufficient iterative validation and recovery_, score 0.455, Δ +0.04, proposed_not_applied)
   > The mandated test-fix-regression loop directly addresses insufficient recovery and validation. It improves execution and output integrity most strongly and raises both difficult probes, though it does not substantially improve initial semantic targeting.

3. **prompt-11 — Require evidence-based navigation before selecting an edit location** (targets _Complex semantic reasoning failure_, score 0.4525, Δ +0.0375, proposed_not_applied)
   > Evidence-based navigation is a strong improvement over repository-name guessing: it requires callers, analogues, tests, control flow, and API confirmation before editing. This most directly improves reasoning on complex cases, while validation and edge handling remain incomplete.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
