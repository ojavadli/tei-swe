# Diagnosis — TRAE + Doubao-Seed-Code

Rank 3/30 · SWE-bench verified · 394 resolved (78.8%)
Repo `https://github.com/bytedance/trae-agent` @ `e839e559ac`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.86 |
| reasoning_soundness | 0.82 |
| execution_accuracy | 0.79 |
| output_integrity | 0.87 |

**Aggregate 0.835 · weakest dimension: execution_accuracy**

The recorded outcomes show strong but imperfect capability: two of four fixed probes resolved, while two remained unresolved, consistent with the system's broader 78.8% verified resolve rate rather than near-perfect reliability. Its modular agent, tool, and patch-selection surfaces support good alignment and output integrity, but the unresolved Django and Astropy cases most directly lower execution accuracy and reasoning soundness.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `scikit-learn__scikit-learn-15100` | resolved | 0.95 |
| `pytest-dev__pytest-7432` | resolved | 0.95 |
| `django__django-16938` | unresolved_by_this_system | 0.22 |
| `astropy__astropy-13033` | unresolved_by_this_system | 0.18 |

## Recurring failure modes

### 1. Complex repository-specific diagnosis and implementation

The agent can complete standard fixes but fails on at least some issues requiring deeper localization, design understanding, or coordinated changes across an unfamiliar codebase.

_Evidence instances:_ django__django-16938, astropy__astropy-13033

### 2. Insufficient validation and iterative debugging

Tool-driven editing and testing do not consistently converge when the initial patch is incomplete or when failures require multiple debugging iterations.

_Evidence instances:_ django__django-16938, astropy__astropy-13033

### 3. Edge-case and regression handling

The unresolved probes indicate difficulty preserving behavior while addressing nuanced framework or scientific-library edge cases, despite successful outcomes on two other instances.

_Evidence instances:_ django__django-16938, astropy__astropy-13033


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **6**
