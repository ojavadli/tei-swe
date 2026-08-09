# Diagnosis — live-SWE-agent + Claude 4.5 Opus medium (20251101)

Rank 1/30 · SWE-bench verified · 396 resolved (79.2%)
Repo `https://github.com/OpenAutoCoder/live-swe-agent` @ `8d7dd86345`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.86 |
| reasoning_soundness | 0.84 |
| execution_accuracy | 0.79 |
| output_integrity | 0.9 |

**Aggregate 0.8475 · weakest dimension: execution_accuracy**

The recorded 79.2% resolve rate supports generally strong but clearly imperfect scores, with execution accuracy weakest because 20.8% of benchmark instances remain unresolved. The probes show successful handling of scikit-learn, one SymPy issue, and Django, but failures on Seaborn, another SymPy issue, and Sphinx demonstrate meaningful project- and task-specific brittleness.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `scikit-learn__scikit-learn-25102` | resolved | 0.94 |
| `sympy__sympy-19783` | resolved | 0.93 |
| `django__django-16569` | resolved | 0.92 |
| `mwaskom__seaborn-3187` | unresolved_by_this_system | 0.3 |
| `sympy__sympy-15875` | unresolved_by_this_system | 0.28 |
| `sphinx-doc__sphinx-9602` | unresolved_by_this_system | 0.32 |

## Recurring failure modes

### 1. Incomplete or incorrect implementation on difficult issues

The system has recorded unresolved outcomes on three probes, indicating that correct issue understanding does not consistently translate into a working patch.

_Evidence instances:_ mwaskom__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602

### 2. Insufficient robustness across project-specific edge cases

Failures span Seaborn, SymPy, and Sphinx, suggesting difficulty adapting implementation and validation to differing library conventions and edge cases.

_Evidence instances:_ mwaskom__seaborn__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602

### 3. Uneven cross-repository generalization

Although the system resolves representative scikit-learn, SymPy, and Django tasks, it fails other repositories in the same benchmark, showing non-uniform performance across codebases.

_Evidence instances:_ mwaskom__seaborn-3187, sympy__sympy-15875, sphinx-doc__sphinx-9602


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **3**
