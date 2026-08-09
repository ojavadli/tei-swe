# TEI v7 — Composio SWE-Kit (2024-10-25)

**Rank 15 of 30** · SWE-bench verified · officially resolved
243 (48.6%) · repo [https://github.com/ComposioHQ/composio](https://github.com/ComposioHQ/composio) @ `13cba53b1d`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.6275** |
| Best structural version (struct-02) | **0.665** |
| Best final version (prompt-01) | **0.685** |
| Shipped | **prompt-01** |

Baseline dimensions: `{"target_alignment": 0.66, "reasoning_soundness": 0.61, "execution_accuracy": 0.56, "output_integrity": 0.68}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incomplete end-to-end task execution** — The system resolves only two of the four fixed probes, with both failures representing inability to deliver an accepted repository change. (evidence: django__django-14351, django__django-14534)
- **Inconsistent performance across similar framework tasks** — Performance is not reliably transferable even within Django: one Django probe is resolved while two others remain unresolved. (evidence: django__django-13410, django__django-14351, django__django-14534)
- **Limited robustness across repository and task variations** — The resolved outcomes do not generalize across the heterogeneous benchmark workload, consistent with the system's reported 48.6% overall resolve rate. (evidence: astropy__astropy-14096, django__django-14351, django__django-14534)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 12 |
| B — prompt | 12 | 6 |
| **total** | **24** | **18** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.54,
  "ref_mean": 0.4875,
  "delta": 0.0525,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.6275, 0.635, 0.625], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-01 — Explicit completion contract** (targets _Incomplete end-to-end task execution_, score 0.685, Δ +0.0575, applied)
   > Directly addresses incomplete end-to-end execution with a concrete implementation, testing, revision, and diff-verification contract. It should improve the weak Django outcomes, though it does not add much framework-specific guidance.

2. **prompt-02 — Test-first repair loop** (targets _Incomplete end-to-end task execution_, score 0.675, Δ +0.0475, applied)
   > A focused reproduce-edit-test loop is useful and improves validation discipline, but the requirement to reproduce behavior before editing can be brittle when tests are absent, expensive, or difficult to isolate.

3. **prompt-04 — Repository pattern triangulation** (targets _Inconsistent performance across similar framework tasks_, score 0.675, Δ +0.0475, applied)
   > Triangulating the issue, implementation, neighboring commands, and tests is a stronger contract-discovery method than relying on a single source. It improves consistency and interface preservation, but the fragment is somewhat cluttered and still lacks an explicit completion loop.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
