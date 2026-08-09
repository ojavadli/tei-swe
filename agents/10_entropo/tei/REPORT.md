# TEI v7 — EntroPO + R2E + Qwen3-Coder-30B-A3B-Instruct

**Rank 10 of 30** · SWE-bench verified · officially resolved
302 (60.4%) · repo [https://github.com/sherdencooper/R2E-Gym](https://github.com/sherdencooper/R2E-Gym) @ `eee9f6f00a`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.63** |
| Best structural version (struct-12) | **0.6825** |
| Best final version (prompt-06) | **0.69** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.66, "reasoning_soundness": 0.61, "execution_accuracy": 0.58, "output_integrity": 0.67}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete patch implementation** — The system failed to resolve two of the four fixed probes, indicating recurring difficulty translating the task requirements into a correct, complete repository change. (evidence: django__django-15930, django__django-11820)
- **Insufficient test-driven verification and iteration** — The unresolved outcomes are consistent with failures to validate the proposed change against the relevant regression behavior before finishing; the repository exposes bash, execution, and submission tools, but successful tool availability does not ensure accurate verification. (evidence: django__django-15930, django__django-11820)
- **Long-horizon context degradation** — The verifier explicitly condenses older execution-result blocks once the Qwen context exceeds 31,000 tokens, creating a recurring risk that debugging evidence or prior assumptions are lost during multi-turn repair attempts. (evidence: django__django-15930, django__django-11820)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 9 |
| B — prompt | 18 | 8 |
| **total** | **36** | **17** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.615,
  "ref_mean": 0.545,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.63, 0.6375, 0.6325], "noise_floor": 0.0075}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **prompt-06 — Evidence-prioritized context recovery** (targets _Long-horizon context degradation_, score 0.69, Δ +0.06, proposed_not_applied)
   > Re-grounding in the issue, current diff, source, and fresh command evidence is a strong long-horizon recovery strategy and improves the reliability of reported state. It helps expose stale hypotheses and hidden failures, but it is less directly prescriptive about implementing every requirement than the coverage contract.

2. **struct-12 — Make the condensed-history instruction explicitly require regression-test revalidation before accepting a patch** (targets _Incorrect or incomplete patch implementation_, score 0.6825, Δ +0.0525, proposed_not_applied)
   > The stronger condensation instruction directly counters incomplete patches by requiring inspection and task-specific regression testing before submission, making it the most relevant change for execution accuracy while still helping long-horizon reasoning.

3. **prompt-12 — State-restoration protocol** (targets _Long-horizon context degradation_, score 0.68, Δ +0.05, proposed_not_applied)
   > Reconstructing the current diff, unmet requirements, failures, and passing tests on every resumed turn directly mitigates context degradation while retaining repository-grounded state. It is stronger than a passive ledger, but repeated reconstruction adds overhead and still lacks the explicit test expansion of candidates 2 and 3.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
