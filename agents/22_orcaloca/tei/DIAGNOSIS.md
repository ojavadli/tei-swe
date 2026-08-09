# Diagnosis — OrcaLoca + Agentless-1.5 + Claude-3.5 Sonnet (20241022)

Rank 22/30 · SWE-bench lite · 123 resolved (41.0%)
Repo `https://github.com/fishmingyu/OrcarLLM` @ `341de75336`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.63 |
| reasoning_soundness | 0.56 |
| execution_accuracy | 0.42 |
| output_integrity | 0.84 |

**Aggregate 0.6125 · weakest dimension: execution_accuracy**

The system resolved 41.0% of the SWE-bench Lite instances, so its target alignment and reasoning are only moderate and its execution accuracy is substantially weaker, despite a relatively strong structured-output interface. The probes show two successful cases but two unresolved SymPy cases, supporting good potential on some tasks but inconsistent localization-to-resolution performance.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `psf__requests-863` | resolved | 0.82 |
| `sympy__sympy-18621` | resolved | 0.78 |
| `sympy__sympy-18698` | unresolved_by_this_system | 0.2 |
| `sympy__sympy-14396` | unresolved_by_this_system | 0.18 |

## Recurring failure modes

### 1. Failure to convert localization into a correct end-to-end resolution

The system can produce structured search and bug-location outputs, but unresolved outcomes indicate that localization or subsequent execution did not reliably yield a correct solution.

_Evidence instances:_ sympy__sympy-18698, sympy__sympy-14396

### 2. Insufficient robustness on difficult SymPy issues

Both recorded SymPy probes were unresolved, suggesting weak generalization or reasoning robustness on technically complex repository issues.

_Evidence instances:_ sympy__sympy-18698, sympy__sympy-14396

### 3. Inconsistent issue-specific prioritization and context selection

The framework relies on LLM-guided action decomposition, relevance scoring, and context pruning, yet the mixed probe outcomes show that these mechanisms do not consistently identify the actionable code path.

_Evidence instances:_ sympy__sympy-18621, sympy__sympy-18698, sympy__sympy-14396


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **4**
