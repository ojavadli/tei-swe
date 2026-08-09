# Diagnosis — CodeFuse-CGM

Rank 18/30 · SWE-bench lite · 132 resolved (44.0%)
Repo `https://github.com/codefuse-ai/CodeFuse-CGM` @ `2c12754ade`

> Substrate: **PROXY** — judged by `gpt-5.6-luna` against repository
> evidence and the archive's recorded per-instance outcomes. Not an executed measurement.

## Baseline dimensions

| Dimension | Score |
|---|---|
| target_alignment | 0.68 |
| reasoning_soundness | 0.56 |
| execution_accuracy | 0.49 |
| output_integrity | 0.64 |

**Aggregate 0.5925 · weakest dimension: execution_accuracy**

The system is clearly aligned with SWE-bench repository-level repair and resolved both recorded Django probes, but its official 44.0% resolve rate and two unresolved probes show that successful reasoning does not generalize reliably. The strongest evidence of weakness is end-to-end execution accuracy, while the structured reranker prompts support only moderate output integrity rather than near-perfect reliability.

## Probe instances (fixed seed, from this system's recorded archive outcomes)

| Instance | Archive outcome | Baseline probe score |
|---|---|---|
| `django__django-15814` | resolved | 0.92 |
| `django__django-11049` | resolved | 0.9 |
| `django__django-15738` | unresolved_by_this_system | 0.2 |
| `sympy__sympy-16503` | unresolved_by_this_system | 0.16 |

## Recurring failure modes

### 1. Repository localization or retrieval misses

The graph-based retrieval and reranking pipeline does not consistently identify the files needed for the issue, as indicated by unresolved Django and SymPy probes.

_Evidence instances:_ django__django-15738, sympy__sympy-16503

### 2. Issue-specific diagnosis is insufficiently reliable

The system's general repository-level prompting and model reasoning do not reliably translate issue descriptions into a correct implementation diagnosis on harder instances.

_Evidence instances:_ django__django-15738, sympy__sympy-16503

### 3. End-to-end patch execution or validation failure

Despite an architecture aimed at repository-level code changes, the default system fails to produce an accepted solution on two of the four recorded probes, reflecting weak execution reliability.

_Evidence instances:_ django__django-15738, sympy__sympy-16503


## Evidence availability

- Recorded trajectories from the archive: **0**
  (Trajectories were not used during the original optimization run. The archive's logs/ and trajs/ are retrievable for frozen submissions with its own unsigned downloader (analysis/download_logs.py); the post-hoc validation pass retrieved and, where sampled, scored them (see validation_passes.json).)
- Trajectories committed in this agent's own repo: **0**
- Prompt-surface files identified: **6**
