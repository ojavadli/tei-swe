# TEI v7 — Patched.Codes Patchwork

**Rank 23 of 30** · SWE-bench lite · officially resolved
111 (37.0%) · repo [https://github.com/patched-codes/patchwork](https://github.com/patched-codes/patchwork) @ `21948cbec4`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (gpu/local-weights required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.5475** |
| Best structural version (struct-09) | **0.5925** |
| Best final version (prompt-23) | **0.6175** |
| Shipped | **prompt-23** |

Baseline dimensions: `{"target_alignment": 0.62, "reasoning_soundness": 0.57, "execution_accuracy": 0.46, "output_integrity": 0.54}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Repository- and issue-type generalization failure** — The system resolved both sampled SymPy instances but failed both sampled Django instances, indicating weak transfer across repository conventions and issue domains. (evidence: django__django-11001, django__django-11910)
- **Unreliable multi-step patch execution** — Although the repository exposes planning, agentic roles, and code-edit tools, both Django probes remained unresolved, suggesting that planning does not reliably become a correct, applied, and validated patch. (evidence: django__django-11001, django__django-11910)
- **Insufficient completion or validation of final changes** — The unresolved outcomes are consistent with failures to finish the requested task or verify the resulting behavior, especially on the Django probes despite the system's structured prompt and tool surfaces. (evidence: django__django-11001, django__django-11910)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 27 |
| B — prompt | 30 | 0 |
| **total** | **60** | **27** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.545,
  "ref_mean": 0.47,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.5475, 0.555, 0.5475], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-23 — Evidence-based validation barrier** (targets _Insufficient completion or validation of final changes_, score 0.6175, Δ +0.07, proposed_not_applied)
   > The validation barrier most directly addresses premature completion, improving execution accuracy and output integrity through diff inspection and focused regression testing; it also helps expose wrong assumptions in low-performing Django cases.

2. **prompt-30 — Final completion gate** (targets _Insufficient completion or validation of final changes_, score 0.6075, Δ +0.06, proposed_not_applied)
   > The final completion gate checks behavior, full-diff integrity, and intended file changes, directly addressing incomplete or poorly validated submissions. It provides balanced gains across execution and output reliability, though it is less specific than the mandatory edit loop about how patches are produced.

3. **prompt-21 — Explicit inspect-edit-verify execution loop** (targets _Unreliable multi-step patch execution_, score 0.605, Δ +0.0575, proposed_not_applied)
   > The closed inspect-edit-verify loop materially improves multi-step patch reliability and final state awareness, while producing moderate secondary gains in reasoning and target alignment.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
