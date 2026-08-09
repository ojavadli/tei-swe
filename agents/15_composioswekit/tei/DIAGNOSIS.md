# Diagnosis — Composio SWE-Kit (2024-10-25)

Rank 15/30 · SWE-bench verified · 243 resolved (48.6%)
Repo `https://github.com/ComposioHQ/composio` @ `13cba53b1d`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.66 |
| reasoning_soundness | 0.61 |
| execution_accuracy | 0.56 |
| output_integrity | 0.68 |

**Aggregate 0.6275 · weakest dimension: execution_accuracy**

The system demonstrates meaningful task understanding and can produce successful changes, as shown by two resolved probes, but the 48.6% official resolve rate and two unresolved fixed probes require materially sub-perfect scores. Execution accuracy is weakest because the failures are end-to-end benchmark failures, while the available repository surfaces show substantial tooling and test infrastructure but do not establish consistently reliable completion.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `astropy__astropy-14096` | resolved | 0.85 |
| `django__django-13410` | resolved | 0.84 |
| `django__django-14351` | unresolved_by_this_system | 0.14 |
| `django__django-14534` | unresolved_by_this_system | 0.12 |

## Recurring failure modes

### 1. Incomplete end-to-end task execution

The system resolves only two of the four fixed probes, with both failures representing inability to deliver an accepted repository change.

_Evidence instances:_ django__django-14351, django__django-14534

### 2. Inconsistent performance across similar framework tasks

Performance is not reliably transferable even within Django: one Django probe is resolved while two others remain unresolved.

_Evidence instances:_ django__django-13410, django__django-14351, django__django-14534

### 3. Limited robustness across repository and task variations

The resolved outcomes do not generalize across the heterogeneous benchmark workload, consistent with the system's reported 48.6% overall resolve rate.

_Evidence instances:_ astropy__astropy-14096, django__django-14351, django__django-14534


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
