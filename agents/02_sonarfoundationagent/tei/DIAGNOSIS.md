# Diagnosis — Sonar Foundation Agent + Claude 4.5 Opus

Rank 2/30 · SWE-bench verified · 396 resolved (79.2%)
Repo `https://github.com/AutoCodeRoverSG/sonar-foundation-agent` @ `394c58819e`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.82 |
| reasoning_soundness | 0.79 |
| execution_accuracy | 0.78 |
| output_integrity | 0.84 |

**Aggregate 0.8075 · weakest dimension: execution_accuracy**

The 79.2% verified resolve rate supports solid but clearly imperfect scores, with execution accuracy weakest because two of the four fixed probes were unresolved. The probe outcomes show strong success on two instances but near-failure on two others, and the absence of a prompt surface limits any stronger claim about the specific internal causes.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `scikit-learn__scikit-learn-15100` | resolved | 0.91 |
| `sympy__sympy-19954` | resolved | 0.89 |
| `pydata__xarray-6599` | unresolved_by_this_system | 0.12 |
| `sympy__sympy-14248` | unresolved_by_this_system | 0.14 |

## Recurring failure modes

### 1. End-to-end issue non-resolution

The archived outcomes show complete failure on two of four fixed probes, indicating that the agent does not reliably turn analysis into an accepted repository resolution.

_Evidence instances:_ pydata__xarray-6599, sympy__sympy-14248

### 2. Cross-repository robustness gap

The system succeeds on the scikit-learn and one SymPy probe but fails on the xarray and another SymPy probe, showing inconsistent handling across repositories and issue instances.

_Evidence instances:_ scikit-learn__scikit-learn-15100, sympy__sympy-19954, pydata__xarray-6599, sympy__sympy-14248

### 3. Instance-level reliability variance

The mixed resolved and unresolved archive outcomes, together with a 79.2% overall resolve rate, indicate meaningful variance rather than uniformly dependable behavior.

_Evidence instances:_ scikit-learn__scikit-learn-15100, sympy__sympy-19954, pydata__xarray-6599, sympy__sympy-14248


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **0**
