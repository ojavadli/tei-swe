# Diagnosis — JoyCode + Claude 4 Sonnet + GPT-4.1

Rank 5/30 · SWE-bench verified · 373 resolved (74.6%)
Repo `https://github.com/jd-opensource/joycode-agent` @ `1bace2ab9f`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.86 |
| reasoning_soundness | 0.81 |
| execution_accuracy | 0.76 |
| output_integrity | 0.88 |

**Aggregate 0.8275 · weakest dimension: execution_accuracy**

The system demonstrates strong but incomplete alignment and output handling, with a verified 74.6% resolution rate and two successful probes. Execution accuracy is weakest because two of the four fixed probes are explicitly unresolved, so the system should not receive near-perfect TEI scores.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-13023` | resolved | 0.93 |
| `sympy__sympy-24443` | resolved | 0.91 |
| `django__django-14170` | unresolved_by_this_system | 0.24 |
| `sphinx-doc__sphinx-9229` | unresolved_by_this_system | 0.21 |

## Recurring failure modes

### 1. Failure to complete repository-specific fixes

The system's patch-generation and execution pipeline did not resolve the Django 14170 and Sphinx 9229 tasks, showing residual failures despite the reported overall 74.6% resolution rate.

_Evidence instances:_ django__django-14170, sphinx-doc__sphinx-9229

### 2. Insufficient recovery from failed attempts

Although the repository emphasizes intelligent retries, test generation, and failure attribution, the recorded unresolved outcomes indicate that these mechanisms do not reliably recover from difficult instances.

_Evidence instances:_ django__django-14170, sphinx-doc__sphinx-9229

### 3. Cross-project generalization gap

The resolved Django and SymPy probes coexist with unresolved Django and Sphinx probes, indicating that success is not uniform across issue types and repository environments.

_Evidence instances:_ django__django-13023, sympy__sympy-24443, django__django-14170, sphinx-doc__sphinx-9229


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **12**
