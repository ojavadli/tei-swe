# Diagnosis — Lingxi-v1.5_claude-4-sonnet-20250514

Rank 6/30 · SWE-bench verified · 373 resolved (74.6%)
Repo `https://github.com/nimasteryang/Lingxi` @ `1f2e5dc4c8`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.79 |
| reasoning_soundness | 0.75 |
| execution_accuracy | 0.72 |
| output_integrity | 0.81 |

**Aggregate 0.7675 · weakest dimension: execution_accuracy**

The two resolved probes show that the default multi-agent workflow can produce effective repository-level repairs, but the two unresolved probes demonstrate substantial brittleness on more difficult instances. Scores are therefore kept materially below 1.0 and calibrated to the reported 74.6% Pass@1 rate, with execution accuracy weakest because successful analysis does not consistently translate into a validated, correct patch.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-13089` | resolved | 0.93 |
| `sympy__sympy-24213` | resolved | 0.9 |
| `django__django-13794` | unresolved_by_this_system | 0.27 |
| `sphinx-doc__sphinx-9229` | unresolved_by_this_system | 0.22 |

## Recurring failure modes

### 1. Incomplete issue localization and scope control

The system can fail to identify all relevant files or the precise behavioral contract, leading to unresolved patches on repository-specific issues.

_Evidence instances:_ django__django-13794, sphinx-doc__sphinx-9229

### 2. Insufficient framework-specific diagnosis

Multi-agent analysis and historical guidance do not reliably produce a sound explanation for harder Django and Sphinx behaviors, resulting in incorrect or incomplete fixes.

_Evidence instances:_ django__django-13794, sphinx-doc__sphinx-9229

### 3. Weak implementation validation and iteration

The default workflow does not consistently catch failed assumptions through tests, focused reproduction, or follow-up edits; this is reflected by unresolved outcomes despite the available repository and editing tools.

_Evidence instances:_ django__django-13794, sphinx-doc__sphinx-9229


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **16**
