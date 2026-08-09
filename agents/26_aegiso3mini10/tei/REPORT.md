# TEI v7 — Aegis - o3-mini_1.0

**Rank 26 of 30** · SWE-bench lite · officially resolved
91 (30.33%) · repo [https://github.com/evandiewald/aegis](https://github.com/evandiewald/aegis) @ `cd81da38f4`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.435** |
| Best structural version (struct-01) | **0.4825** |
| Best final version (prompt-06) | **0.4975** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.48, "reasoning_soundness": 0.43, "execution_accuracy": 0.37, "output_integrity": 0.46}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Failure to produce a correct end-to-end patch** — The system did not resolve the Django 12286 or SymPy 12236 probes, indicating that issue understanding did not reliably translate into executable, test-passing changes. (evidence: django__django-12286, sympy__sympy-12236)
- **Insufficient issue-specific reasoning on harder tasks** — The unresolved outcomes suggest weaknesses in diagnosing or planning solutions for at least some repository-specific issues despite the available browsing and editing workflow. (evidence: django__django-12286, sympy__sympy-12236)
- **Unreliable completion and validation of results** — The agent architecture exposes tools and result-saving infrastructure, but the unresolved probes show that the final submitted state was not consistently validated into a successful resolution. (evidence: django__django-12286, sympy__sympy-12236)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 7 |
| B — prompt | 12 | 12 |
| **total** | **24** | **19** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.44,
  "ref_mean": 0.4025,
  "delta": 0.0375,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.44, 0.435, 0.435], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-06 — Explicit completion gate** (targets _Failure to produce a correct end-to-end patch_, score 0.4975, Δ +0.0625, applied)
   > The explicit final-state gate directly addresses premature completion by requiring reproducible commands, results, and an evidenced environment block. It improves completion and reporting more than diagnosis; strict gating can also leave some environment-blocked tasks unresolved rather than producing a potentially usable patch.

2. **prompt-12 — Completion and diff verification gate** (targets _Unreliable completion and validation of results_, score 0.4925, Δ +0.0575, applied)
   > This most directly addresses unreliable completion: it separates product defects from harness failures, verifies the actual files and full diff, and requires focused plus regression testing. It therefore has the strongest output-integrity and execution gains, though it contributes less to issue-specific reasoning and may occasionally misclassify environment failures without a stronger diagnosis framework.

3. **prompt-01 — Root-cause-to-patch contract** (targets _Failure to produce a correct end-to-end patch_, score 0.4875, Δ +0.0525, applied)
   > The diagnosis-to-patch contract directly constrains scope and expected behavior, improving alignment and reducing incomplete or unrelated edits. It provides less help with discovering the correct root cause, so gains on the harder probes remain modest.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
