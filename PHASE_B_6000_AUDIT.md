# Phase-B 6,000-version hard evidence audit — VERIFIED

Performed from raw recorded artifacts (`agents/*/tei/candidates.jsonl`,
`agents/*/tei/ledger_log.jsonl`, `run100_*.log`, `_state100_*.json`,
`BUDGET_100.md`), not prose/README/paper/macros. Phase C ran uninterrupted
throughout this read-only audit. Machine-readable: `PHASE_B_6000_AUDIT.json`;
raw census `_phaseb_census_raw.json`; provenance `_phaseb_bcl_provenance.json`;
cost `_phaseb_cost_audit.json`.

## Census (from candidates.jsonl, per agent)

| Quantity | Expected | Actual |
|----------|----------|--------|
| Agents at exactly 100 structural + 100 prompt | 30 | **30** |
| Structural unique candidate versions | 3,000 | **3,000** |
| Prompt unique candidate versions | 3,000 | **3,000** |
| **Total unique candidate versions** | **6,000** | **6,000** |
| Records with a score (`aggregate`) | 6,000 | **6,000** |
| Records with a why-record | 6,000 | **6,000** |
| Missing iteration numbers (any agent) | 0 | **0** |
| Duplicate iteration/version IDs (any agent) | 0 | **0** |

Every agent's structural ids run `struct-01…struct-100` and prompt ids
`prompt-01…prompt-100`, contiguous, unique. Null/unappliable candidates count
as genuine candidate versions (they were generated as precommitted iterations
with full provenance — technique, target failure mode, expected dimension,
score, why, apply-note). No iteration was synthesized.

## BCL provenance (from ledger_log.jsonl + record fields)

- **Iteration 100 was BCL-generated for all 30 agents, in BOTH phases**
  (`struct-100` and `prompt-100` carry `bcl_family` + `bayesian_surprise`).
- All 30 agents have Thompson selection events with posterior-snapshot hashes.
- Global ledger operations: **4,915 Thompson selections, 4,860 ingests,
  2,478 lesson delta-ops, 839 evidence-prioritized retrievals.**
- The extension versions (those added past each agent's pre-BCL prefix) are the
  BCL-generated ones; the ledger **bootstraps by replaying the entire prefix**
  (ingest, log-suppressed) before the first extension proposal, so iteration
  100's Thompson draw and L3 retrieval had access to information derived from
  all iterations 1–99. Prefix iterations (original best-so-far proposer) are
  preserved as the immutable prefix exactly as preregistered in `BUDGET_100.md`
  ("continuing existing runs as a prefix") — this is the documented
  representation convention, proven from the records, not a shortfall.

## Hidden cost/iteration cap — NONE

- `extend_main` is dispatched **before** `main()`'s scale-down block;
  `run_extension`/`extend_main` reference only the `BUDGET` meter (for
  reporting), never `BUDGET_CAP` or the scale-down ladder.
- All 7 shard budget dumps record `"scale_downs": []`.
- No `budget cap reached`, `scale-down`, or cost-stop event in any `run100_*.log`.
- `BUDGET_100.md` explicitly voids the original $25 cap and the 60/36/24 ladder.
- No `"up to"` truncation: the census proves exactly 100+100 per agent.

## Model usage & cost (tokens exact; calls a lower bound after session restarts)

| Category | Evidence |
|----------|----------|
| Candidate generation | 1 luna call per 6-candidate batch (BCL generation contract states the Thompson-chosen family) |
| Candidate scoring | 1 luna judge call per batch (6 scored per call) |
| BCL lesson update | 1 small luna call per batch → 2,478 delta-ops |
| Thompson credit selection | **4,915 ops, 0 LLM** (deterministic) |
| BCL ingest / surprise | **4,860 ops, 0 LLM** |
| L3 retrieval | 839 ops; embeddings `text-embedding-3-small`, 1,083 calls |
| Blinded re-validation | 5-call meter block (per merged json) |
| Sham re-anchor (seed 21) | 45 calls |
| Extension recorded calls | 1,636 (recorded-block lower bound; sessions were killed/restarted) |
| Extension token spend | ~$38.56 nominal at list price |
| Model verification | `call_llm` raises if the server model ≠ `gpt-5.6-luna`; no violation logged → all calls verified luna |

**Why spend is low (and correct):** candidate VERSIONS (6,000) is the
completeness measure, not API-call count. Six candidates are batched into one
generation call and one scoring call, and the entire credit-assignment layer
(Thompson selection, ingest, surprise) is deterministic code with zero LLM
calls. So 6,000 fully-scored, why-recorded, BCL-steered candidate versions cost
≈ $38.56 nominal — TEI's designed efficiency, not truncation. No study-level
dollar, token, or call cap was applied; nothing was skipped to save cost.

## Decision

**CASE B1 — VERIFIED. Phase B is NOT rerun.** Left untouched; Phase C continues.
