# TEI v7 — Agentless Lite + O3 Mini (20250214)

**Rank 19 of 30** · SWE-bench verified · officially resolved
212 (42.4%) · repo [https://github.com/sorendunn/Agentless-Lite](https://github.com/sorendunn/Agentless-Lite) @ `01900cec17`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.5775** |
| Best structural version (struct-12) | **0.63** |
| Best final version (prompt-06) | **0.6375** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.66, "reasoning_soundness": 0.55, "execution_accuracy": 0.48, "output_integrity": 0.62}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **repository-specific localization and diagnosis failures** — Both unresolved scikit-learn probes indicate recurring difficulty identifying the relevant code paths and accurately diagnosing the issue in unfamiliar repository contexts. (evidence: scikit-learn__scikit-learn-25747, scikit-learn__scikit-learn-12973)
- **incomplete or incorrect patch execution** — The two unresolved outcomes are consistent with the RAG-only system failing to translate retrieved context into a correct, applicable repository change. (evidence: scikit-learn__scikit-learn-25747, scikit-learn__scikit-learn-12973)
- **insufficient validation of proposed fixes** — The unresolved scikit-learn results suggest weak confirmation that edits satisfy the task's behavioral requirements, especially where repository-specific edge cases matter. (evidence: scikit-learn__scikit-learn-25747, scikit-learn__scikit-learn-12973)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 6 |
| B — prompt | 12 | 11 |
| **total** | **24** | **17** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.57,
  "ref_mean": 0.495,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.585, 0.575, 0.5725], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-06 — Post-patch proof obligation** (targets _insufficient validation of proposed fixes_, score 0.6375, Δ +0.06, proposed_not_applied)
   > The proof obligation links the diagnosis to tests before editing and requires post-patch control-flow coverage, neighboring-call-site checks, and regression validation. It addresses the diagnosed validation gap while also catching some incomplete patches, though it cannot fully substitute for repository-specific localization.

2. **prompt-08 — Concrete execution-path tracing** (targets _repository-specific localization and diagnosis failures_, score 0.6375, Δ +0.06, applied)
   > Concrete execution-path tracing is a stronger diagnostic intervention than a static repository map because it ties the requirement to an actual branch, transformation, and divergence. This improves target alignment and reasoning most, with a small downstream execution benefit, but it still does not impose a complete patch or validation protocol.

3. **struct-12 — Behavioral acceptance-checklist gate** (targets _insufficient validation of proposed fixes_, score 0.63, Δ +0.0525, proposed_not_applied)
   > The acceptance checklist covers the trigger, edge cases, caller regressions, and repository tests, directly addressing the diagnosed validation failure and improving confidence in the final claim. It depends on a sound issue contract and may still miss hidden repository-specific paths, so target alignment improves only slightly.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
