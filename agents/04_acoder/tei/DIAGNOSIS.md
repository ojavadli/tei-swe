# Diagnosis — ACoder

Rank 4/30 · SWE-bench verified · 382 resolved (76.4%)
Repo `https://github.com/ACoder-AI/ACoder` @ `63325725b6`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.78 |
| reasoning_soundness | 0.77 |
| execution_accuracy | 0.75 |
| output_integrity | 0.8 |

**Aggregate 0.775 · weakest dimension: execution_accuracy**

ACoder's officially resolved rate is 76.4%, so its dimensions should reflect meaningful capability with nontrivial failure risk rather than near-perfect performance. The fixed probes show successful handling of django__django-14631 and scikit-learn__scikit-learn-15100, but failure on pylint-dev__pylint-7277 and scikit-learn__scikit-learn-13124; the repository also exposes no prompt surface for stronger evidence about alignment or output behavior.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-14631` | resolved | 0.95 |
| `scikit-learn__scikit-learn-15100` | resolved | 0.95 |
| `pylint-dev__pylint-7277` | unresolved_by_this_system | 0.05 |
| `scikit-learn__scikit-learn-13124` | unresolved_by_this_system | 0.05 |

## Recurring failure modes

### 1. Incomplete task resolution

The system failed to produce a resolved outcome on two fixed repository tasks, indicating substantial tail risk despite the aggregate success rate.

_Evidence instances:_ pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124

### 2. Insufficient repository-specific debugging or implementation accuracy

Failures on both a Pylint task and a scikit-learn task suggest difficulty converting repository analysis into a correct, project-specific change.

_Evidence instances:_ pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124

### 3. Unreliable end-to-end verification and completion

The recorded unresolved outcomes indicate that exploration and reasoning do not consistently culminate in a validated patch, even though two other probes were resolved.

_Evidence instances:_ pylint-dev__pylint-7277, scikit-learn__scikit-learn-13124


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **0**
