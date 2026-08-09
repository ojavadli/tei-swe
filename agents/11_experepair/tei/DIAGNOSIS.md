# Diagnosis — ExpeRepair-v1.0 + Claude 4 Sonnet

Rank 11/30 · SWE-bench lite · 181 resolved (60.33%)
Repo `https://github.com/ExpeRepair/ExpeRepair` @ `5594f2c02c`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.74 |
| reasoning_soundness | 0.68 |
| execution_accuracy | 0.61 |
| output_integrity | 0.79 |

**Aggregate 0.705 · weakest dimension: execution_accuracy**

The observed 2/4 probe success rate is consistent with a system that has useful issue analysis and repair capability but substantial execution failures, and it is compatible with the reported 60.33% overall resolve rate. The explicit search, reproduction, and validation stages support the identified failure modes, while the two resolved SymPy probes show that the workflow can succeed on some instances.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `sympy__sympy-13647` | resolved | 0.82 |
| `sympy__sympy-16792` | resolved | 0.82 |
| `django__django-11620` | unresolved_by_this_system | 0.24 |
| `django__django-12497` | unresolved_by_this_system | 0.24 |

## Recurring failure modes

### 1. Incorrect repository localization

The search stage must select relevant editable files from the repository structure; failures on both Django probes are consistent with localization errors or incomplete cause analysis.

_Evidence instances:_ django__django-11620, django__django-12497

### 2. Unreliable reproduction or validation judgment

The system relies on generated reproduction tests and an LLM validation stage, creating a failure mode when tests are invalid, incomplete, or misinterpreted.

_Evidence instances:_ django__django-11620, django__django-12497

### 3. Patch generation or execution failure

The unresolved outcomes indicate that analysis did not consistently produce and successfully apply a correct repository-level fix, despite the multi-agent repair workflow.

_Evidence instances:_ django__django-11620, django__django-12497


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
