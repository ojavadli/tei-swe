# TEI v7 — SWE-Rizzo

**Rank 13 of 30** · SWE-bench verified · officially resolved
283 (56.6%) · repo [https://github.com/brokespace/gen42-codemonkeys](https://github.com/brokespace/gen42-codemonkeys) @ `c6303b8710`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (docker required). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.725** |
| Best structural version (struct-18) | **0.7975** |
| Best final version (prompt-06) | **0.815** |
| Shipped | **prompt-06** |

Baseline dimensions: `{"target_alignment": 0.82, "reasoning_soundness": 0.7, "execution_accuracy": 0.57, "output_integrity": 0.81}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incomplete or incorrect issue fixes** — The system's iterative editing and testing workflow does not reliably produce a behaviorally correct patch on harder instances, as shown by unresolved outcomes. (evidence: django__django-12774, sympy__sympy-17630)
- **Insufficient test-feedback coverage** — Although the system explicitly generates and executes tests, the available evidence shows that this feedback loop can still fail to expose or resolve the cases required by the benchmark. (evidence: django__django-12774, sympy__sympy-17630)
- **Candidate convergence or selection failure** — Repeated sampling and test/model-based selection improve coverage but do not guarantee that a correct candidate is generated or selected, producing unresolved final outcomes. (evidence: django__django-12774, sympy__sympy-17630)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 30 | 26 |
| B — prompt | 30 | 25 |
| **total** | **60** | **51** |

All 60 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.6975,
  "ref_mean": 0.55,
  "delta": 0.1475,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.725, 0.725, 0.725], "noise_floor": 0.0}`


## Top 3 why-records

1. **prompt-06 — Minimal-patch differential verification** (targets _Candidate convergence or selection failure_, score 0.815, Δ +0.09, proposed_not_applied)
   > Baseline-versus-candidate differential verification gives comparable evidence for every viable patch and selects the smallest behaviorally effective change, directly addressing candidate selection failure. It is the strongest option overall, though minimality can under-correct issues whose requirements are broader than the focused reproducer.

2. **prompt-12 — Adversarial candidate discrimination** (targets _Candidate convergence or selection failure_, score 0.8025, Δ +0.0775, applied)
   > Active counterexample search across boundaries, invalid inputs, repeated calls, and ordering is a strong discriminator against superficially passing patches and improves convergence. The strict no-approval rule can overtest or block on ambiguous evidence, keeping execution below the strongest compatibility-focused variant.

3. **struct-18 — Evidence-first candidate handoff protocol** (targets _Candidate convergence or selection failure_, score 0.7975, Δ +0.0725, proposed_not_applied)
   > The ordered evidence-based handoff gives selection a concrete basis for comparing behavior coverage, reproduction, test results, regressions, and scope. It directly addresses convergence failure and improves integrity and execution, though it depends on upstream candidates actually producing the evidence.


## Trajectory availability

Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).
