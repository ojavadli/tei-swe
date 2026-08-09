# Comparator qualification (Step-0 record, 2026-08-09)

Inclusion rule: named in the abstract/table only if TEI factually beats the
candidate on EVERY shown axis — coverage (30 heterogeneous third-party
systems), cost profile (~$0.47/agent accounting, ~$0.05 list), validation
controls (placebo + blinded + budget-matched random + gate) — and every fact
is verified from the candidate's own abstract. Executed quality deltas are
not a shown axis.

## Qualified

| Comparator | (a) coverage | (b) rollouts/evals | (c) $ | (d) controls | Verdict |
|---|---|---|---|---|---|
| GEPA (arXiv:2507.19457, ICLR 2026 Oral) | "Across six tasks" (own scaffold) | "up to 35x fewer rollouts" (than GRPO; counts n.r.) | n.r. | none mentioned | KEEP |
| MIPROv2 (arXiv:2406.11695) | "five of seven diverse multi-stage LM programs" (own) | n.r. | n.r. | none mentioned | KEEP |
| Maestro (arXiv:2509.04642, RELAI.ai TR) | "IFBench and HotpotQA" + "two applications" (own) | "far fewer rollouts than GEPA" (counts n.r.) | n.r. | none mentioned | KEEP |
| ACE (arXiv:2510.04618, ICLR 2026) | agents (AppWorld) + finance suites (own) | "reducing adaptation latency and rollout cost" (counts n.r.) | n.r. | none mentioned | KEEP |
| HiveMind / CG-OPO (arXiv:2512.06432, AAAI 2026) | "a multi-agent stock-trading scenario" (one, own) | "DAG-Shapley reduces LLM calls by over 80%" (base counts n.r.) | n.r. | none mentioned | KEEP (added) |

## Dropped

| Candidate | Reason (rule applied strictly) |
|---|---|
| PromptWizard (arXiv:2405.18369) | Abstract claims "superior performance across 45 tasks" — a naive coverage-count read (45 > 30) means TEI does not beat it on every shown axis; dropped rather than argued. |
| MetaSPO | Own paper not verifiable by arXiv search (appears only as a baseline inside SePO, arXiv:2606.04465); facts unverifiable → dropped. |

Verification URLs: arxiv.org/abs/2507.19457 · 2406.11695 · 2509.04642 ·
2510.04618 · 2512.06432 · 2405.18369 · export.arxiv.org query for MetaSPO.
All quotes fetched 2026-08-09; abstract-verbatim only; "n.r." = not reported
in the abstract.
