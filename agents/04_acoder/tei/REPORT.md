# TEI v7 — ACoder

**Rank 4 of 30** · SWE-bench verified · officially resolved
382 (76.4%) · repo [https://github.com/ACoder-AI/ACoder](https://github.com/ACoder-AI/ACoder) @ `63325725b6`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (no source code in linked repo). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.775** |
| Best structural version (struct-18) | **0.845** |
| Best final version (struct-18) | **0.845** |
| Shipped | **struct-18** |

Baseline dimensions: `{"target_alignment": 0.78, "reasoning_soundness": 0.77, "execution_accuracy": 0.75, "output_integrity": 0.8}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incomplete task resolution** — The system failed to produce a resolved outcome on two fixed repository tasks, indicating substantial tail risk despite the aggregate success rate. (evidence: pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124)
- **Insufficient repository-specific debugging or implementation accuracy** — Failures on both a Pylint task and a scikit-learn task suggest difficulty converting repository analysis into a correct, project-specific change. (evidence: pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124)
- **Unreliable end-to-end verification and completion** — The recorded unresolved outcomes indicate that exploration and reasoning do not consistently culminate in a validated patch, even though two other probes were resolved. (evidence: pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 0 |
| B — prompt | 30 | 0 |
| **total** | **60** | **0** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5725,
  "ref_mean": 0.5,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.775, 0.78, 0.78], "noise_floor": 0.005}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **struct-18 — Use a two-pass patch review architecture: have the implementation subagent produce a patch and rationale, then have an independent reviewer compare the patch against the issue, surrounding repository conventions, edge cases, and tests; automatically send rejected patches back for revision.** (targets _Insufficient repository-specific debugging or implementation accuracy_, score 0.845, Δ +0.07, proposed_not_applied)
   > Independent review directly targets subtle project-specific implementation mistakes and edge cases, giving this the strongest reasoning and execution improvement among the candidates. It remains dependent on the first subagent producing a viable patch and can add latency or reviewer disagreement, so the difficult probes improve meaningfully but remain far from reliable.

2. **struct-12 — Implement a hard completion gate that accepts a task only when a non-empty intended diff exists, the focused regression test passes, relevant broader tests pass or have recorded justified exceptions, and the final response reports changed files and verification commands.** (targets _Unreliable end-to-end verification and completion_, score 0.8425, Δ +0.0675, proposed_not_applied)
   > The hard completion gate most directly prevents unresolved, empty, or unverifiable submissions and gives the strongest improvement to end-to-end integrity. It does not itself produce a correct patch, and strict gating can reject partially successful work when broader tests are unavailable.

3. **struct-05 — Add a completion gate with a structured checklist requiring: changed files are present, the patch is non-empty, the issue behavior is covered by a test or justified existing test, focused tests passed, and the final response accurately reports the resulting diff and verification evidence.** (targets _Incomplete task resolution_, score 0.84, Δ +0.065, proposed_not_applied)
   > The completion gate is tightly aligned with incomplete task resolution and gives the strongest improvement to patch presence, test evidence, and final-response accuracy. It is primarily a rejection mechanism, so it raises weak behavioral outcomes only modestly without stronger debugging.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
