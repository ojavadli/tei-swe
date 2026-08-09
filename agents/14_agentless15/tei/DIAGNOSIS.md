# Diagnosis — Agentless-1.5 + Claude-3.5 Sonnet (20241022)

Rank 14/30 · SWE-bench verified · 254 resolved (50.8%)
Repo `https://github.com/OpenAutoCoder/Agentless` @ `5ce5888b9f`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.62 |
| reasoning_soundness | 0.55 |
| execution_accuracy | 0.51 |
| output_integrity | 0.68 |

**Aggregate 0.59 · weakest dimension: execution_accuracy**

The two resolved probes show that the default Agentless-1.5 system can align with an issue and execute a valid repair, but the two unresolved probes demonstrate substantial failures in localization, reasoning, or patch validation. The dimensions are therefore kept near—but not above—the system's reported 50.8% verified resolve rate, with execution accuracy weakest and output integrity somewhat higher because the pipeline generally produces structured patch artifacts even when they are incorrect.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `astropy__astropy-13453` | resolved | 0.78 |
| `django__django-15104` | resolved | 0.78 |
| `pytest-dev__pytest-6197` | unresolved_by_this_system | 0.22 |
| `mwaskom__seaborn-3069` | unresolved_by_this_system | 0.22 |

## Recurring failure modes

### 1. Localization and repair failure on repository-specific behavior

The system can complete some fixes, but its unresolved outcomes on pytest and seaborn indicate recurring difficulty mapping issue descriptions to the correct implementation and producing a behaviorally correct patch.

_Evidence instances:_ pytest-dev__pytest-6197, mwaskom__seaborn-3069

### 2. Insufficient regression-test or reproduction-test guidance

The explicit test-selection and reproduction-generation stages do not reliably prevent incorrect or incomplete fixes, particularly for the unresolved pytest and seaborn issues.

_Evidence instances:_ pytest-dev__pytest-6197, mwaskom__seaborn-3069

### 3. Brittle end-to-end patch validation across projects

The pipeline's validation can succeed on selected instances but does not generalize reliably across the benchmark's varied repositories, as shown by two unresolved probes despite the successful astropy and django cases.

_Evidence instances:_ pytest-dev__pytest-6197, mwaskom__seaborn-3069, astropy__astropy-13453, django__django-15104


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **4**
