# TEI v7 — SWE-Fixer (Qwen2.5-7b retriever + Qwen2.5-72b editor)

**Rank 24 of 30** · SWE-bench verified · officially resolved
164 (32.8%) · repo [https://github.com/InternLM/SWE-Fixer](https://github.com/InternLM/SWE-Fixer) @ `7871693672`

> **All scores below are PROXY** — `gpt-5.6-luna` rubric scores against diagnosed
> failure modes and fixed probe instances. This agent was not executed
> (cli entry point plausible; execution still requires SWE-bench task infra). PROXY scores are not
> resolve-rate gains and must not be reported as such.

## Score trajectory

| Stage | Aggregate |
|---|---|
| Baseline (default agent) | **0.48** |
| Best structural version (struct-10) | **0.55** |
| Best final version (struct-10) | **0.55** |
| Shipped | **struct-10** |

Baseline dimensions: `{"target_alignment": 0.52, "reasoning_soundness": 0.46, "execution_accuracy": 0.36, "output_integrity": 0.58}`
Weakest dimension: **execution_accuracy**

## Diagnosed failure modes

- **Incorrect or incomplete repository modification** — The system was unresolved on both probes below, indicating a recurring failure to turn its analysis into a patch that satisfies the benchmark tests. (evidence: sphinx-doc__sphinx-9230, django__django-13279)
- **Insufficient issue-specific reasoning** — The unresolved outcomes on both a Sphinx issue and a Django issue suggest difficulty reliably grounding the solution in the repository-specific requirements rather than producing a generally plausible response. (evidence: sphinx-doc__sphinx-9230, django__django-13279)
- **Insufficient validation before submission** — Because the system resolves only 32.8% of verified instances overall and failed these two recorded probes, it appears to lack reliable test-driven verification or correction of its generated changes. (evidence: sphinx-doc__sphinx-9230, django__django-13279)

## Proposals

| Phase | Versions | Applied as real commits |
|---|---|---|
| A — structural | 18 | 13 |
| B — prompt | 18 | 0 |
| **total** | **36** | **13** |

All 36 versions with their scores and why-records are in `tei/candidates.jsonl`.

## Do-no-harm confirmation (tei_loop.gate.verify_candidate)

```json
{
  "n_queries": 4,
  "cand_mean": 0.5,
  "ref_mean": 0.44,
  "delta": 0.06,
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

Paraphrase noise floor: `{"paraphrase_aggregates": [0.48, 0.4775, 0.4825], "noise_floor": 0.0025}`
The best shipped gain is ABOVE the paraphrase noise floor.

## Top 3 why-records

1. **struct-10 — Add a self-review gate for patch completeness before allowing output** (targets _Incorrect or incomplete repository modification_, score 0.55, Δ +0.07, proposed_not_applied)
   > A completeness review specifically targets omitted call sites, edge cases, imports, and patches that only alter tests or documentation. This most directly improves patch integrity and execution accuracy, but the self-review is still model-generated and can cause overly conservative rejection of legitimate narrow fixes.

2. **struct-17 — Introduce an adversarial reviewer pass before emitting the JSON** (targets _Incorrect or incomplete repository modification_, score 0.54, Δ +0.06, proposed_not_applied)
   > The adversarial pass checks several concrete failure modes, including stale paths, API assumptions, missing files, and non-matching edits. This materially improves patch completeness and output integrity, though it is still self-review and does not provide the same confidence as running tests.

3. **struct-08 — Inject an issue-to-code localization workflow into the editor request** (targets _Insufficient issue-specific reasoning_, score 0.5375, Δ +0.0575, applied)
   > The localization workflow directly addresses issue-specific reasoning by requiring behavioral-contract inference, code-path tracing, and relevant-test identification. It should help most on the two weak probes, though prompting alone cannot ensure the model actually edits every required location or validates the patch.


## Trajectory availability

SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.
