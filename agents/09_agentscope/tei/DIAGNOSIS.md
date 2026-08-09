# Diagnosis — AgentScope

Rank 9/30 · SWE-bench verified · 317 resolved (63.4%)
Repo `https://github.com/modelscope/agentscope` @ `29b592358c`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.68 |
| reasoning_soundness | 0.62 |
| execution_accuracy | 0.6 |
| output_integrity | 0.65 |

**Aggregate 0.6375 · weakest dimension: execution_accuracy**

The fixed probes show 2 of 4 resolved, while the broader verified split reports a 63.4% resolve rate, so the dimensions are kept moderate rather than near-perfect. The successful Django cases show useful task alignment, but failures on Sphinx and Seaborn materially reduce reasoning, execution, and output confidence for the unmodified system.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-14999` | resolved | 0.84 |
| `django__django-14580` | resolved | 0.82 |
| `sphinx-doc__sphinx-8056` | unresolved_by_this_system | 0.28 |
| `mwaskom__seaborn-3187` | unresolved_by_this_system | 0.24 |

## Recurring failure modes

### 1. Cross-repository generalization failure

The system resolved both Django probes but failed on the Sphinx and Seaborn probes, indicating inconsistent transfer across repository ecosystems.

_Evidence instances:_ sphinx-doc__sphinx-8056, mwaskom__seaborn-3187

### 2. Insufficient issue-specific patch execution

The unresolved Sphinx and Seaborn outcomes suggest that identifying or implementing the required repository-specific changes is unreliable.

_Evidence instances:_ sphinx-doc__sphinx-8056, mwaskom__seaborn-3187

### 3. Weak validation of completed fixes

The two unresolved outcomes indicate that the default workflow does not consistently produce a verified, task-complete result outside the successful Django cases.

_Evidence instances:_ sphinx-doc__sphinx-8056, mwaskom__seaborn-3187


## Evidence availability

- Recorded trajectories from the archive: **0**
  (SWE-bench/experiments ships aggregate results only; logs/ and trajs/ are in a credentialed S3 bucket (archive README). No AWS access per owner directive, so 0 recorded trajectories were read.)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
