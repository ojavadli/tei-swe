# Diagnosis — Patched.Codes Patchwork

Rank 23/30 · SWE-bench lite · 111 resolved (37.0%)
Repo `https://github.com/patched-codes/patchwork` @ `21948cbec4`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.62 |
| reasoning_soundness | 0.57 |
| execution_accuracy | 0.46 |
| output_integrity | 0.54 |

**Aggregate 0.5475 · weakest dimension: execution_accuracy**

The official 37.0% resolve rate indicates broad unreliability, and the fixed probes show only the two SymPy tasks resolved while both Django tasks failed. The prompt, planning, and agentic-tool code provides substantial capability surface, but the observed Django failures warrant materially lower execution and reasoning scores rather than near-perfect ratings.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `sympy__sympy-20154` | resolved | 0.78 |
| `sympy__sympy-15011` | resolved | 0.76 |
| `django__django-11001` | unresolved_by_this_system | 0.18 |
| `django__django-11910` | unresolved_by_this_system | 0.16 |

## Recurring failure modes

### 1. Repository- and issue-type generalization failure

The system resolved both sampled SymPy instances but failed both sampled Django instances, indicating weak transfer across repository conventions and issue domains.

_Evidence instances:_ django__django-11001, django__django-11910

### 2. Unreliable multi-step patch execution

Although the repository exposes planning, agentic roles, and code-edit tools, both Django probes remained unresolved, suggesting that planning does not reliably become a correct, applied, and validated patch.

_Evidence instances:_ django__django-11001, django__django-11910

### 3. Insufficient completion or validation of final changes

The unresolved outcomes are consistent with failures to finish the requested task or verify the resulting behavior, especially on the Django probes despite the system's structured prompt and tool surfaces.

_Evidence instances:_ django__django-11001, django__django-11910


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **20**
