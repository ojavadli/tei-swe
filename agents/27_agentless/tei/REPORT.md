# TEI v7 — Agentless + RepoGraph + GPT-4o

**Rank 27 of 30** · SWE-bench lite · officially resolved
89 (29.67%) · repo [https://github.com/ozyyshr/RepoGraph](https://github.com/ozyyshr/RepoGraph) @ `6c3977d878`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.44** |
| Best structural version (struct-07) | **0.48** |
| Best final version (prompt-11) | **0.5025** |
| Shipped | **prompt-11** |

Baseline dimensions: `{"target_alignment": 0.46, "reasoning_soundness": 0.39, "execution_accuracy": 0.33, "output_integrity": 0.58}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete patch implementation** — The system can generate a plausible repair but fails to produce a patch that fully satisfies the issue, as shown by unresolved outcomes. (evidence: sphinx-doc__sphinx-10451, django__django-14016)
- **Insufficient repository-level localization and reasoning** — Despite RepoGraph-supported context retrieval and relevant-file prompting, the agent does not reliably identify and reason through the complete set of affected code paths. (evidence: sphinx-doc__sphinx-10451, django__django-14016)
- **Weak validation against behavioral requirements** — The pipeline includes syntax, lint, and diff postprocessing, but these mechanical checks do not ensure semantic correctness, reflected in the unresolved probes. (evidence: sphinx-doc__sphinx-10451, django__django-14016)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 6 |
| B — prompt | 12 | 2 |
| **total** | **24** | **8** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5325,
  "ref_mean": 0.4625,
  "delta": 0.07,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.44, 0.4425, 0.4425], "noise_floor": 0.0025}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-11 — Behavioral oracle and scenario validation** (targets _Weak validation against behavioral requirements_, score 0.5025, Δ +0.0625, proposed_not_applied)
   > Concrete behavioral scenarios and explicit oracles most directly address weak validation, improving implementation completeness and regression resistance; gains remain moderate because validation quality depends on correctly understanding the repository and issue semantics.

2. **prompt-06 — Adversarial patch review** (targets _Weak validation against behavioral requirements_, score 0.5, Δ +0.06, proposed_not_applied)
   > Adversarial counterexamples and pre/post behavioral comparison directly target weak validation while also exposing incomplete implementations. It provides the strongest execution and output gains, although it can overfocus on anticipated hidden cases without fully solving repository localization.

3. **prompt-12 — Patch-level regression and invariant audit** (targets _Weak validation against behavioral requirements_, score 0.495, Δ +0.055, proposed_not_applied)
   > A post-edit regression and invariant audit improves patch reliability and output integrity, but it is weaker than scenario-driven validation for discovering missing behavioral cases and does not materially improve initial localization.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
