# Diagnosis — SWE-agent + Claude 4 Sonnet

Rank 8/30 · SWE-bench verified · 333 resolved (66.6%)
Repo `https://github.com/SWE-agent/SWE-agent` @ `3ea751c087`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.74 |
| reasoning_soundness | 0.69 |
| execution_accuracy | 0.64 |
| output_integrity | 0.76 |

**Aggregate 0.7075 · weakest dimension: execution_accuracy**

The two resolved probes show strong task targeting and usable output, but the two unresolved probes directly demonstrate substantial gaps in execution accuracy and reasoning reliability. Those failures are consistent with, and calibrated to, the system's approximately 66.6% overall resolve rate rather than near-perfect performance.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `sphinx-doc__sphinx-10449` | resolved | 0.84 |
| `matplotlib__matplotlib-24570` | resolved | 0.81 |
| `django__django-13112` | unresolved_by_this_system | 0.32 |
| `pydata__xarray-6599` | unresolved_by_this_system | 0.29 |

## Recurring failure modes

### 1. Incorrect or incomplete repository changes

The system can fail to turn an otherwise plausible approach into a patch that resolves the issue, as shown by unresolved outcomes on both Django and xarray.

_Evidence instances:_ django__django-13112, pydata__xarray-6599

### 2. Insufficient validation and iteration

The retry/tool-driven setup does not reliably detect and repair remaining defects before submission, evidenced by two unresolved probe instances despite the system's generally capable agent configuration.

_Evidence instances:_ django__django-13112, pydata__xarray-6599

### 3. Difficulty with repository-specific edge cases

Performance is not uniformly reliable across projects: Sphinx and Matplotlib were resolved, while Django and xarray were not, indicating recurring sensitivity to project semantics and edge-case behavior.

_Evidence instances:_ django__django-13112, pydata__xarray-6599


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **22**
- Prompt-surface files identified: **20**
