# Diagnosis — SWE-Exp

Rank 20/30 · SWE-bench verified · 210 resolved (42.0%)
Repo `https://github.com/YerbaPage/SWE-Exp` @ `6b5c92ed0a`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.58 |
| reasoning_soundness | 0.5 |
| execution_accuracy | 0.43 |
| output_integrity | 0.56 |

**Aggregate 0.5175 · weakest dimension: execution_accuracy**

The archive reports a 42.0% verified resolve rate, so the default system warrants middling rather than near-perfect scores, with execution accuracy lowest. Two probes resolved and two remained unresolved, showing meaningful capability but substantial reliability and generalization failures.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-13109` | resolved | 0.8 |
| `sympy__sympy-17655` | resolved | 0.8 |
| `django__django-14122` | unresolved_by_this_system | 0.12 |
| `django__django-14351` | unresolved_by_this_system | 0.12 |

## Recurring failure modes

### 1. End-to-end repair failure

The system did not produce a verified resolution for these benchmark instances, consistent with execution accuracy being the principal weakness.

_Evidence instances:_ django__django-14122, django__django-14351

### 2. Unreliable transfer across issue types and repositories

Despite an experience-learning and retrieval design, the fixed probes show successful handling on some tasks but failure on two Django tasks, indicating inconsistent generalization.

_Evidence instances:_ django__django-13109, sympy__sympy-17655, django__django-14122, django__django-14351

### 3. Insufficiently robust completion under difficult cases

The unresolved outcomes indicate that the default trajectory, reasoning, or validation process can terminate without a correct patch even when the system is aimed at issue resolution.

_Evidence instances:_ django__django-14122, django__django-14351


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
