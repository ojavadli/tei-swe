# Diagnosis — Moatless Tools + Claude 4 Sonnet

Rank 7/30 · SWE-bench verified · 354 resolved (70.8%)
Repo `https://github.com/aorwall/moatless-tools` @ `011ead57a5`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.83 |
| reasoning_soundness | 0.77 |
| execution_accuracy | 0.74 |
| output_integrity | 0.84 |

**Aggregate 0.795 · weakest dimension: execution_accuracy**

The default system officially resolves 70.8% of verified SWE-bench instances, so its aggregate capability is substantial but clearly not near-perfect. The fixed probes reinforce that split: both Django instances resolved, while the pytest and seaborn instances remained unresolved; the prompt and completion infrastructure support disciplined tool use and output handling, but execution accuracy is the main limiting factor.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-11276` | resolved | 0.9 |
| `django__django-14608` | resolved | 0.88 |
| `pytest-dev__pytest-5840` | unresolved_by_this_system | 0.28 |
| `mwaskom__seaborn-3187` | unresolved_by_this_system | 0.3 |

## Recurring failure modes

### 1. Failure to converge on repository-specific fixes

The system can resolve some Django tasks but does not reliably translate investigation into a correct patch on other repositories.

_Evidence instances:_ pytest-dev__pytest-5840, mwaskom__seaborn-3187

### 2. Insufficient iterative verification

The strict single-action workflow supports controlled execution, but the unresolved probes indicate that investigation, editing, and validation do not consistently converge on passing behavior.

_Evidence instances:_ pytest-dev__pytest-5840, mwaskom__seaborn-3187

### 3. Brittle cross-repository generalization

The recorded outcomes show successful handling of both Django probes but failures on the pytest and seaborn probes, suggesting weaknesses that emerge across different codebase conventions and test ecosystems.

_Evidence instances:_ pytest-dev__pytest-5840, mwaskom__seaborn-3187


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
