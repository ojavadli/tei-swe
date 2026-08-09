# Diagnosis — CodeShellAgent + Gemini 2.0 Flash (Experimental)

Rank 17/30 · SWE-bench verified · 221 resolved (44.2%)
Repo `https://github.com/WisdomShell/codeshell` @ `09d1adc88c`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.56 |
| reasoning_soundness | 0.47 |
| execution_accuracy | 0.44 |
| output_integrity | 0.52 |

**Aggregate 0.4975 · weakest dimension: execution_accuracy**

The archived outcomes show only two of four fixed probes resolved, consistent with the system's broader 44.2% verified-split resolve rate. This supports moderate alignment and reasoning scores, but execution accuracy must remain the weakest dimension because more than half of instances fail, while output integrity is only moderately supported because the repository provides no prompt or patch-quality evidence.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `sympy__sympy-15017` | resolved | 0.9 |
| `django__django-11880` | resolved | 0.9 |
| `django__django-15916` | unresolved_by_this_system | 0.08 |
| `sphinx-doc__sphinx-9673` | unresolved_by_this_system | 0.08 |

## Recurring failure modes

### 1. Inconsistent end-to-end task resolution

The system resolves some repository tasks but fails to produce a successful outcome on other instances.

_Evidence instances:_ django__django-15916, sphinx-doc__sphinx-9673

### 2. Weak generalization across repositories and issue types

Success on SymPy and one Django instance does not carry over reliably to another Django task or a Sphinx task.

_Evidence instances:_ django__django-11880, django__django-15916, sphinx-doc__sphinx-9673

### 3. Insufficient patch verification or correction

The unresolved outcomes indicate that execution and final validation are not consistently completed, despite demonstrated successes on two probes.

_Evidence instances:_ django__django-15916, sphinx-doc__sphinx-9673


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **0**
