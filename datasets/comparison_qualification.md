# 2026 optimizer comparison — primary-source qualification audit

Every comparator below was resolved to a primary source (arXiv/OpenReview) before
inclusion; unresolvable names were excluded. Quality numbers are the authors' own,
on their own executed substrate, and are NOT directly comparable to TEI's anchored
rubric / blinded proxy deltas (different measurement units — stated, never converted).

## MAIN TABLE — current (2025–2026) methods

| Method | Primary source | Venue | Optimizes | Systems optimized | Selection substrate |
|--------|----------------|-------|-----------|-------------------|---------------------|
| GEPA | arXiv:2507.19457 | ICLR 2026 (Oral) | prompts (reflective Pareto evolution) | authors' 6 tasks | executed rollouts |
| ACE | arXiv:2510.04618 | ICLR 2026 | context/playbook (delta lessons) | agent + finance benchmarks | executed rollouts |
| Maestro | arXiv:2509.04642 | 2025 | agent graph + config | authors' benchmarks (IFBench/HotpotQA) | executed rollouts |
| HiveMind (CG-OPO) | arXiv:2512.06432 | 2025 | MAS prompts (contribution-guided) | authors' multi-agent system | executed rollouts |
| MASS | arXiv:2502.02533 | 2025/26 | MAS prompts + topology | authors' multi-agent designs | executed rollouts |
| MASPOB | arXiv:2603.02630 | 2026 | MAS prompts (bandit + GNN) | authors' multi-agent systems | executed rollouts |

## SECONDARY TABLE — foundational / legacy baselines

| Method | Primary source | Optimizes |
|--------|----------------|-----------|
| MIPROv2 | arXiv:2406.11695 (2024) | instructions + demos (Bayesian) |
| OPRO | arXiv:2309.03409 (2023) | prompt as optimization target |
| DSPy/APE lineage | DSPy framework | prompt programs |

## Excluded (not resolvable to a primary source at audit time)
- "MASPO", "MARS" as agent-optimization methods: no primary paper resolved distinct from
  the above; excluded per the sourceability rule.

## Where TEI is distinct (verified against the above primary sources)
- **Third-party coverage:** all comparators optimize the authors' own systems/tasks; TEI
  applies ONE procedure across 30 independently developed leaderboard systems. TEI LEADS.
- **Selection substrate:** all comparators select candidates on executed rollouts; TEI's
  6,000-version search uses zero executed benchmark rollouts as the selection signal
  (anchored rubric + gating + blinding + static checks). TEI UNIQUE among those compared.
- **Bias-controlled validation:** none of the audited papers report a sham placebo + a
  direction-hidden blinded A/B + a budget-matched random control of the selection signal.
  TEI UNIQUE among those compared.
- **Per-candidate provenance:** TEI releases score+why for all 6,000 candidate versions.
  UNCOMMON among those compared.
- **Cost transparency:** most audited papers do not report a directly comparable dollar
  total; TEI reports a complete token/dollar ledger. Where dollars are reported at all,
  none is directly comparable (different units). TEI reports the most complete accounting.
- **Structural + prompt breadth:** TEI jointly searches structural (code/workflow) and
  prompt surfaces; several comparators optimize prompts or context only.

## Substrate honesty
TEI's improvement is an anchored-rubric / blinded proxy result; the comparators' are
executed end-task results. The comparison tables compare only axes measurable on both
sides (coverage, cost reporting, optimization surface, validation controls, auditability,
selection-rollout requirement, candidate scale) and never equate a rubric delta with an
executed-resolve delta.
