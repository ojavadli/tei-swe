# TEI v7 — SWE-RL (Llama3-SWE-RL-70B + Agentless Mini) (20250226)

**Rank 21 of 30** · SWE-bench verified · officially resolved
206 (41.2%) · repo [https://github.com/facebookresearch/swe-rl](https://github.com/facebookresearch/swe-rl) @ `5aa10d67f1`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (gpu/local-weights required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.555** |
| Best structural version (struct-11) | **0.6075** |
| Best final version (struct-11) | **0.6075** |
| Shipped | **struct-11** |

Baseline dimensions: `{"target_alignment": 0.59, "reasoning_soundness": 0.55, "execution_accuracy": 0.46, "output_integrity": 0.62}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete code repair** — The system fails to produce a patch that resolves the issue on some repositories, indicating weak end-to-end repair accuracy. (evidence: django__django-17084, sphinx-doc__sphinx-9281)
- **Insufficient issue-to-code alignment** — Unresolved instances suggest that localization or interpretation of the requested behavioral change is not consistently reliable across projects. (evidence: django__django-17084, sphinx-doc__sphinx-9281)
- **Fragile generated-edit pipeline** — The repair path depends on extracting and splitting structured Python edit commands, so failures in producing applicable edits can prevent otherwise plausible reasoning from becoming a valid repository patch. (evidence: django__django-17084, sphinx-doc__sphinx-9281)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 12 | 10 |
| B — prompt | 12 | 0 |
| **total** | **24** | **10** |

All 24 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.55,
  "ref_mean": 0.5,
  "delta": 0.05,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.555, 0.555, 0.555], "noise_floor": 0.0}`


## Top 3 why-records

1. **struct-11 — Recognize common Markdown fence language labels and optional indentation around the fenced payload** (targets _Insufficient issue-to-code alignment_, score 0.6075, Δ +0.0525, proposed_not_applied)
   > This most directly broadens fallback recognition to realistic python, python3, and py fences with indentation and optional line breaks. It improves issue-to-code alignment and recovery coverage, though the permissive pattern can still accept malformed fence layouts.

2. **prompt-12 — Patch self-review against acceptance criteria** (targets _Incorrect or incomplete code repair_, score 0.6025, Δ +0.0475, proposed_not_applied)
   > The structured final review catches unmapped requirements, caller regressions, exception mistakes, and missing imports, producing broad but moderate gains; it is weaker than an actual test loop because it relies on the agent's own inspection.

3. **prompt-04 — Test-first validation and repair loop** (targets _Incorrect or incomplete code repair_, score 0.6, Δ +0.045, proposed_not_applied)
   > A reproduce-fix-targeted-test loop is the strongest direct defense against incorrect repairs and improves reasoning through observed feedback. It can be costly or brittle when tests are hard to run, so alignment and output integrity remain near baseline.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
