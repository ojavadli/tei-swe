# Diagnosis — Agentless + RepoGraph + GPT-4o

Rank 27/30 · SWE-bench lite · 89 resolved (29.67%)
Repo `https://github.com/ozyyshr/RepoGraph` @ `6c3977d878`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.46 |
| reasoning_soundness | 0.39 |
| execution_accuracy | 0.33 |
| output_integrity | 0.58 |

**Aggregate 0.44 · weakest dimension: execution_accuracy**

The repository shows substantial support for context retrieval, structured editing, parsing, syntax checks, and patch postprocessing, so target alignment and output integrity are stronger than semantic execution. However, the recorded 29.67% overall resolve rate and two unresolved fixed probes require low-to-moderate scores for reasoning and especially execution accuracy; the two resolved probes indicate useful but inconsistent capability rather than dependable repair performance.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-11815` | resolved | 0.78 |
| `django__django-11583` | resolved | 0.74 |
| `sphinx-doc__sphinx-10451` | unresolved_by_this_system | 0.18 |
| `django__django-14016` | unresolved_by_this_system | 0.15 |

## Recurring failure modes

### 1. Incorrect or incomplete patch implementation

The system can generate a plausible repair but fails to produce a patch that fully satisfies the issue, as shown by unresolved outcomes.

_Evidence instances:_ sphinx-doc__sphinx-10451, django__django-14016

### 2. Insufficient repository-level localization and reasoning

Despite RepoGraph-supported context retrieval and relevant-file prompting, the agent does not reliably identify and reason through the complete set of affected code paths.

_Evidence instances:_ sphinx-doc__sphinx-10451, django__django-14016

### 3. Weak validation against behavioral requirements

The pipeline includes syntax, lint, and diff postprocessing, but these mechanical checks do not ensure semantic correctness, reflected in the unresolved probes.

_Evidence instances:_ sphinx-doc__sphinx-10451, django__django-14016


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **15**
- Prompt-surface files identified: **17**
