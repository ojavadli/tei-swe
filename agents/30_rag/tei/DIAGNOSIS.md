# Diagnosis — RAG + Claude 3 Opus

Rank 30/30 · SWE-bench verified · 35 resolved (7.0%)
Repo `https://github.com/SWE-bench/SWE-bench` @ `cd37836ffe`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.24 |
| reasoning_soundness | 0.2 |
| execution_accuracy | 0.08 |
| output_integrity | 0.32 |

**Aggregate 0.21 · weakest dimension: execution_accuracy**

The two resolved probes show that RAG plus Claude 3 Opus can occasionally produce a correct result, but the official verified resolve rate is only 35 instances (7.0%), so execution accuracy and overall TEI must remain low. The two unresolved probes, including one from Django despite another Django success, provide direct evidence of substantial instance-level and cross-issue inconsistency.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-10914` | resolved | 0.82 |
| `sympy__sympy-21847` | resolved | 0.82 |
| `django__django-16116` | unresolved_by_this_system | 0.05 |
| `pydata__xarray-3677` | unresolved_by_this_system | 0.05 |

## Recurring failure modes

### 1. Low instance-level solve reliability

The system resolves only 35 verified instances, a 7.0% rate, indicating that successful issue understanding does not consistently become a correct repository change.

_Evidence instances:_ django__django-16116, pydata__xarray-3677

### 2. Weak cross-instance generalization

It resolves one Django instance but fails another, showing that success on a repository or framework does not reliably transfer to a different issue in the same codebase.

_Evidence instances:_ django__django-10914, django__django-16116

### 3. Inconsistent cross-repository execution

The system succeeds on the SymPy probe but fails on the Xarray probe, indicating unreliable adaptation to repository-specific code, tests, and conventions.

_Evidence instances:_ sympy__sympy-21847, pydata__xarray-3677


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **1**
