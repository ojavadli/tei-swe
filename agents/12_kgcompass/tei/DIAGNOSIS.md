# Diagnosis — KGCompass + Claude 4 Sonnet (20250514)

Rank 12/30 · SWE-bench lite · 175 resolved (58.33%)
Repo `https://github.com/GLEAM-Lab/KGCompass` @ `b74a584e6d`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.68 |
| reasoning_soundness | 0.62 |
| execution_accuracy | 0.57 |
| output_integrity | 0.64 |

**Aggregate 0.6275 · weakest dimension: execution_accuracy**

The system resolved 2 of the 4 fixed probes, consistent with its recorded 58.33% overall resolve rate, so its dimensions should remain materially below near-perfect performance. The repository shows a capable but layered pipeline—KG localization, LLM localization, strict edit parsing, syntax checking, and patch application—whose unresolved probes most strongly expose execution and reliability weaknesses.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-15213` | resolved | 0.9 |
| `django__django-12747` | resolved | 0.9 |
| `django__django-13768` | unresolved_by_this_system | 0.2 |
| `django__django-11964` | unresolved_by_this_system | 0.2 |

## Recurring failure modes

### 1. Fault-localization or context-selection misses

The system depends on KG-derived locations and an additional LLM localization stage; the unresolved outcomes indicate that this pipeline does not reliably identify sufficient repair context.

_Evidence instances:_ django__django-13768, django__django-11964

### 2. Patch generation and application failures

The repair path relies on generated edit commands, diff parsing, syntax checks, and patch application, creating multiple opportunities for a plausible repair to fail execution or tests.

_Evidence instances:_ django__django-13768, django__django-11964

### 3. Brittle output and orchestration handling

The default system uses separate localization and repair scripts with strict structured parsing and multi-API/configuration plumbing; failures in formatting, parsing, or workflow coordination can prevent otherwise useful model output from becoming a valid submission.

_Evidence instances:_ django__django-13768, django__django-11964


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **4**
