# TEI v7 — OrcaLoca + Agentless-1.5 + Claude-3.5 Sonnet (20241022)

**Rank 22 of 30** · SWE-bench lite · officially resolved
123 (41.0%) · repo [https://github.com/fishmingyu/OrcarLLM](https://github.com/fishmingyu/OrcarLLM) @ `341de75336`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.6125** |
| Best structural version (struct-30) | **0.66** |
| Best final version (prompt-18) | **0.6775** |
| Shipped | **prompt-18** |

Baseline dimensions: `{"target_alignment": 0.63, "reasoning_soundness": 0.56, "execution_accuracy": 0.42, "output_integrity": 0.84}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to convert localization into a correct end-to-end resolution** — The system can produce structured search and bug-location outputs, but unresolved outcomes indicate that localization or subsequent execution did not reliably yield a correct solution. (evidence: sympy__sympy-18698, sympy__sympy-14396)
- **Insufficient robustness on difficult SymPy issues** — Both recorded SymPy probes were unresolved, suggesting weak generalization or reasoning robustness on technically complex repository issues. (evidence: sympy__sympy-18698, sympy__sympy-14396)
- **Inconsistent issue-specific prioritization and context selection** — The framework relies on LLM-guided action decomposition, relevance scoring, and context pruning, yet the mixed probe outcomes show that these mechanisms do not consistently identify the actionable code path. (evidence: sympy__sympy-18621, sympy__sympy-18698, sympy__sympy-14396)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 26 |
| B — prompt | 30 | 23 |
| **total** | **60** | **49** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5675,
  "ref_mean": 0.495,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.6125, 0.62, 0.615], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-18 — Evidence-preserving final decision protocol** (targets _Inconsistent issue-specific prioritization and context selection_, score 0.6775, Δ +0.065, proposed_not_applied)
   > The evidence table and rejection of weakly supported candidates most directly improve context selection, traceability, and final decision quality. It slightly outperforms the baseline on alignment and integrity, but its strict acceptance protocol can reject workable repairs or add overhead, limiting execution gains and leaving the deepest SymPy reasoning cases below the semantic-tracing version.

2. **prompt-04 — Executable causal-chain scoring** (targets _Failure to convert localization into a correct end-to-end resolution_, score 0.67, Δ +0.0575, proposed_not_applied)
   > The executable causal-chain requirement best addresses the diagnosed localization-to-resolution gap by connecting reproduction, invariant, call path, minimal patch, and validation. It has the strongest end-to-end gains, but its strict chain can reject otherwise valid fixes when repository tests or environmental observations are imperfect.

3. **prompt-23 — Post-edit behavioral verification and regression expansion** (targets _Failure to convert localization into a correct end-to-end resolution_, score 0.6675, Δ +0.055, applied)
   > Diff inspection plus reproducer, regression, nearby-case, and existing-test verification most directly closes the baseline resolution gap. It substantially improves execution and output integrity, while only indirectly helping difficult diagnosis; weak hypotheses can still survive the verification set.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
