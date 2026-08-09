# Diagnosis — SWE-RL (Llama3-SWE-RL-70B + Agentless Mini) (20250226)

Rank 21/30 · SWE-bench verified · 206 resolved (41.2%)
Repo `https://github.com/facebookresearch/swe-rl` @ `5aa10d67f1`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.59 |
| reasoning_soundness | 0.55 |
| execution_accuracy | 0.46 |
| output_integrity | 0.62 |

**Aggregate 0.555 · weakest dimension: execution_accuracy**

The archive shows only two of four fixed probes resolved, consistent with the system's broader 41.2% verified resolve rate rather than near-perfect performance. The two successful probes support moderately strong capability, but the Django and Sphinx failures indicate substantial weaknesses in alignment and, most clearly, executable patch correctness.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `sympy__sympy-16450` | resolved | 0.82 |
| `matplotlib__matplotlib-24627` | resolved | 0.8 |
| `django__django-17084` | unresolved_by_this_system | 0.2 |
| `sphinx-doc__sphinx-9281` | unresolved_by_this_system | 0.18 |

## Recurring failure modes

### 1. Incorrect or incomplete code repair

The system fails to produce a patch that resolves the issue on some repositories, indicating weak end-to-end repair accuracy.

_Evidence instances:_ django__django-17084, sphinx-doc__sphinx-9281

### 2. Insufficient issue-to-code alignment

Unresolved instances suggest that localization or interpretation of the requested behavioral change is not consistently reliable across projects.

_Evidence instances:_ django__django-17084, sphinx-doc__sphinx-9281

### 3. Fragile generated-edit pipeline

The repair path depends on extracting and splitting structured Python edit commands, so failures in producing applicable edits can prevent otherwise plausible reasoning from becoming a valid repository patch.

_Evidence instances:_ django__django-17084, sphinx-doc__sphinx-9281


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **1**
