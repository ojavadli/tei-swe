# TEI v7 — live-SWE-agent + Claude 4.5 Opus medium (20251101)

**Rank 1 of 30** · SWE-bench verified · officially resolved
396 (79.2%) · repo [https://github.com/OpenAutoCoder/live-swe-agent](https://github.com/OpenAutoCoder/live-swe-agent) @ `8d7dd86345`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (no source code in linked repo). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.8475** |
| Best structural version (struct-15) | **0.885** |
| Best final version (prompt-04) | **0.89** |
| Shipped | **prompt-04** |

Baseline dimensions: `{"target_alignment": 0.86, "reasoning_soundness": 0.84, "execution_accuracy": 0.79, "output_integrity": 0.9}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incomplete or incorrect implementation on difficult issues** — The system has recorded unresolved outcomes on three probes, indicating that correct issue understanding does not consistently translate into a working patch. (evidence: mwaskom__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602)
- **Insufficient robustness across project-specific edge cases** — Failures span Seaborn, SymPy, and Sphinx, suggesting difficulty adapting implementation and validation to differing library conventions and edge cases. (evidence: mwaskom__seaborn__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602)
- **Uneven cross-repository generalization** — Although the system resolves representative scikit-learn, SymPy, and Django tasks, it fails other repositories in the same benchmark, showing non-uniform performance across codebases. (evidence: mwaskom__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 0 |
| B — prompt | 30 | 24 |
| **total** | **60** | **24** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 6,
  "cand_mean": 0.6883,
  "ref_mean": 0.615,
  "delta": 0.0733,
  "wins": 6,
  "losses": 0,
  "sign_p": 0.031,
  "margin_hoeffding": 0.554,
  "mde": 0.242,
  "insufficient_n": false,
  "accept": true,
  "reason": "mean not below reference; 6W/0L paired (sign p=0.031)",
  "preflight": "Power check: with 6 eval queries, only mean-score changes >= ~0.24 are statistically meaningful; smaller deltas are within judge noise. (~36 queries would certify a 0.10 gain.)"
}
```

Paraphrase noise floor: `{"paraphrase_aggregates": [0.8475, 0.8475, 0.8475], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-04 — Invariant preservation and differential inspection** (targets _Insufficient robustness across project-specific edge cases_, score 0.89, Δ +0.0425, applied)
   > Identifying and checking invariants across types, ordering, mutation, exceptions, serialization, and performance gives the strongest protection against subtle regressions and incomplete fixes. It improves reasoning, execution, and output fidelity, though it may add analysis burden on simple issues.

2. **prompt-20 — Invariant-first implementation planning** (targets _Incomplete or incorrect implementation on difficult issues_, score 0.89, Δ +0.0425, applied)
   > Invariant-first planning materially improves reasoning quality and caller coverage, with a modest execution benefit. It can become overly analytical and still depends on correctly identifying the invariant, so difficult edge cases improve only slightly.

3. **prompt-24 — Tooling- and compatibility-aware completion protocol** (targets _Uneven cross-repository generalization_, score 0.89, Δ +0.0425, applied)
   > The completion protocol improves practical execution by enforcing repository tooling, discovery, formatting, compatibility, and a disciplined final report. It provides the best output-integrity gain and a modest execution gain, but is broad enough that it adds less problem-specific reasoning than an invariant or edge-case-focused approach.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
