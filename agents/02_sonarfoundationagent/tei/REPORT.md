# TEI v7 — Sonar Foundation Agent + Claude 4.5 Opus

**Rank 2 of 30** · SWE-bench verified · officially resolved
396 (79.2%) · repo [https://github.com/AutoCodeRoverSG/sonar-foundation-agent](https://github.com/AutoCodeRoverSG/sonar-foundation-agent) @ `394c58819e`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (no source code in linked repo). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.8075** |
| Best structural version (struct-23) | **0.86** |
| Best final version (prompt-07) | **0.8625** |
| Shipped | **prompt-07** |

Baseline dimensions: `{"target_alignment": 0.82, "reasoning_soundness": 0.79, "execution_accuracy": 0.78, "output_integrity": 0.84}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **End-to-end issue non-resolution** — The archived outcomes show complete failure on two of four fixed probes, indicating that the agent does not reliably turn analysis into an accepted repository resolution. (evidence: pydata__xarray-6599, sympy__sympy-14248)
- **Cross-repository robustness gap** — The system succeeds on the scikit-learn and one SymPy probe but fails on the xarray and another SymPy probe, showing inconsistent handling across repositories and issue instances. (evidence: scikit-learn__scikit-learn-15100, sympy__sympy-19954, pydata__xarray-6599, sympy__sympy-14248)
- **Instance-level reliability variance** — The mixed resolved and unresolved archive outcomes, together with a 79.2% overall resolve rate, indicate meaningful variance rather than uniformly dependable behavior. (evidence: scikit-learn__scikit-learn-15100, sympy__sympy-19954, pydata__xarray-6599, sympy__sympy-14248)

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
  "cand_mean": 0.6,
  "ref_mean": 0.515,
  "delta": 0.085,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.8075, 0.8075, 0.8075], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-07 — Explicit issue-to-acceptance loop** (targets _End-to-end issue non-resolution_, score 0.8625, Δ +0.055, proposed_not_applied)
   > The explicit acceptance loop directly addresses stopping after diagnosis and should improve completion and verification. It raises target alignment and execution accuracy substantially, with modest gains on the previously failing probes, but it does not by itself solve repository-specific investigation.

2. **prompt-26 — Evidence-gated implementation loop** (targets _End-to-end issue non-resolution_, score 0.8625, Δ +0.055, proposed_not_applied)
   > This is the strongest end-to-end intervention: reproduction, focused validation, broader testing, and revision directly address non-resolution and prevent unverified hypotheses from surviving. It still cannot eliminate repository-specific ambiguity, so gains on the hardest probes remain bounded.

3. **struct-23 — Add a semantic diff and regression-review gate after implementation: compare the patch against the issue's requested behavior, inspect public API and compatibility impact, and require at least one test demonstrating the reported bug plus one test protecting unchanged behavior.** (targets _End-to-end issue non-resolution_, score 0.86, Δ +0.0525, proposed_not_applied)
   > The semantic diff and regression-review gate strongly improves alignment with requested behavior, compatibility awareness, and final patch integrity. It is especially effective after a basically correct implementation, producing the best scores on the easy probes, but it is downstream of diagnosis and therefore gives only limited benefit on the unresolved cross-repository failures.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
