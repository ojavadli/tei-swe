# TEI v7 — CodeShellAgent + Gemini 2.0 Flash (Experimental)

**Rank 17 of 30** · SWE-bench verified · officially resolved
221 (44.2%) · repo [https://github.com/WisdomShell/codeshell](https://github.com/WisdomShell/codeshell) @ `09d1adc88c`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (gpu/local-weights required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.4975** |
| Best structural version (struct-11) | **0.5425** |
| Best final version (prompt-10) | **0.5525** |
| Shipped | **prompt-10** |

Baseline dimensions: `{"target_alignment": 0.56, "reasoning_soundness": 0.47, "execution_accuracy": 0.44, "output_integrity": 0.52}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Inconsistent end-to-end task resolution** — The system resolves some repository tasks but fails to produce a successful outcome on other instances. (evidence: django__django-15916, sphinx-doc__sphinx-9673)
- **Weak generalization across repositories and issue types** — Success on SymPy and one Django instance does not carry over reliably to another Django task or a Sphinx task. (evidence: django__django-11880, django__django-15916, sphinx-doc__sphinx-9673)
- **Insufficient patch verification or correction** — The unresolved outcomes indicate that execution and final validation are not consistently completed, despite demonstrated successes on two probes. (evidence: django__django-15916, sphinx-doc__sphinx-9673)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 0 |
| B — prompt | 12 | 0 |
| **total** | **24** | **0** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6075,
  "ref_mean": 0.49,
  "delta": 0.1175,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.4975, 0.495, 0.4975], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-10 — Failure-driven validation loop** (targets _Insufficient patch verification or correction_, score 0.5525, Δ +0.055, proposed_not_applied)
   > The explicit failure-classification and rerun loop is the strongest direct response to insufficient verification, improving correction of initially incomplete patches. Its gains are bounded because it can misclassify environment failures or overrun the available execution budget.

2. **prompt-07 — Explicit end-to-end completion contract** (targets _Inconsistent end-to-end task resolution_, score 0.545, Δ +0.0475, proposed_not_applied)
   > The explicit completion contract directly addresses premature stopping and modestly improves implementation follow-through and final-state reporting. It does not substantially improve repository-specific diagnosis, so gains on the hard probes remain limited.

3. **struct-11 — Use a structured per-instance state machine with explicit states for issue understanding, localization, patching, testing, repair, and submission, including a failure transition instead of allowing the model to terminate after editing.** (targets _Inconsistent end-to-end task resolution_, score 0.5425, Δ +0.045, proposed_not_applied)
   > Explicit phase transitions reduce premature termination and improve end-to-end consistency, but a rigid state machine can add overhead and still lacks concrete repository-specific repair logic.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
