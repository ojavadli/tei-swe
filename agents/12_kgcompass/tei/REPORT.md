# TEI v7 — KGCompass + Claude 4 Sonnet (20250514)

**Rank 12 of 30** · SWE-bench lite · officially resolved
175 (58.33%) · repo [https://github.com/GLEAM-Lab/KGCompass](https://github.com/GLEAM-Lab/KGCompass) @ `b74a584e6d`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.6275** |
| Best structural version (struct-30) | **0.6675** |
| Best final version (prompt-06) | **0.69** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.68, "reasoning_soundness": 0.62, "execution_accuracy": 0.57, "output_integrity": 0.64}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Fault-localization or context-selection misses** — The system depends on KG-derived locations and an additional LLM localization stage; the unresolved outcomes indicate that this pipeline does not reliably identify sufficient repair context. (evidence: django__django-13768, django__django-11964)
- **Patch generation and application failures** — The repair path relies on generated edit commands, diff parsing, syntax checks, and patch application, creating multiple opportunities for a plausible repair to fail execution or tests. (evidence: django__django-13768, django__django-11964)
- **Brittle output and orchestration handling** — The default system uses separate localization and repair scripts with strict structured parsing and multi-API/configuration plumbing; failures in formatting, parsing, or workflow coordination can prevent otherwise useful model output from becoming a valid submission. (evidence: django__django-13768, django__django-11964)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 28 |
| B — prompt | 30 | 0 |
| **total** | **60** | **28** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.625,
  "ref_mean": 0.55,
  "delta": 0.075,
  "wins": 2,
  "losses": 1,
  "sign_p": 1.0,
  "margin_hoeffding": 0.679,
  "mde": 0.297,
  "insufficient_n": false,
  "accept": true,
  "reason": "mean not below reference; 2W/1L paired (sign p=1.0)",
  "preflight": "Power check: with 4 eval queries, only mean-score changes >= ~0.30 are statistically meaningful; smaller deltas are within judge noise. (~36 queries would certify a 0.10 gain.)"
}
```

Paraphrase noise floor: `{"paraphrase_aggregates": [0.6275, 0.63, 0.6275], "noise_floor": 0.0025}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-06 — Canonical edit serialization with preflight constraints** (targets _Brittle output and orchestration handling_, score 0.69, Δ +0.0625, proposed_not_applied)
   > Canonical unified-diff serialization and preflight constraints directly reduce malformed or unapplied edits and provide the strongest output-integrity improvement. It does not improve diagnosis and can preserve an incorrect patch cleanly, so target alignment and reasoning remain slightly below baseline.

2. **prompt-04 — Test-oriented patch self-review** (targets _Patch generation and application failures_, score 0.6825, Δ +0.055, proposed_not_applied)
   > Focused mental execution and checks for control flow, types, imports, exceptions, and compatibility most directly address patch-generation failures. It produces the largest execution gain, though review is only as good as the initial diagnosis and does not fix orchestration format failures.

3. **prompt-18 — Parser-safe repair protocol with explicit failure signaling** (targets _Brittle output and orchestration handling_, score 0.6775, Δ +0.05, proposed_not_applied)
   > Parser-safe unified diffs directly address orchestration failures and explicit NO_SAFE_PATCH avoids fabricating unsafe edits. However, the conservative failure signal can forfeit solvable instances, and the protocol does not improve localization enough to resolve the hardest probes.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
