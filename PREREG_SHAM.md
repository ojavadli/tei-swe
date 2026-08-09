# Pre-registration: sham-patch placebo arm (committed BEFORE execution)

Registered: 2026-08-09, before any sham-arm LLM call. Tagged `prereg-sham` in the
public release repository (github.com/ojavadli/tei-swe) so the timestamp is
externally verifiable.

## Design

For each of the 26 patched agents in TEI-SWE-30:

1. Create branch `sham-v1` from the agent's frozen baseline SHA.
2. For every file changed on `tei-v7` (relative to the same SHA), insert a
   **semantically-null, syntax-clean** sham edit into the SAME file:
   comment-only lines ("routine maintenance annotation; no functional change"),
   count matched to the number of added lines the real patches made to that
   file (±10%). Python/YAML/Markdown files receive comment lines valid for
   their format; files whose format admits no comments (e.g. JSON) are skipped
   and logged. All sham files must pass `ast.parse` where applicable.
3. Run the IDENTICAL blinded protocol used for the real patches: judge
   `gpt-5.6-luna`, k=5 randomized, narrative-free A/B of baseline vs `sham-v1`
   changed-region excerpts, fresh RNG seed 7.

## Pre-registered metrics

- Per-agent sham majority (sham preferred strictly more than baseline+tie).
- Pooled sham vote share = sham votes / all votes.

## Pre-registered interpretation branches (chosen before any result is seen)

- **Sham pooled share ≤ 60%**: the blinded preference for real patches is
  substantive (not an artifact of "changed code looks newer/busier").
  → The improvement headline is CERTIFIED and stated with full confidence.
- **60% < share < 85%**: partial style sensitivity. → Report real-vs-sham
  shares side by side wherever the blinded result is claimed.
- **Share ≥ 85%**: the blinded rung is measuring change-styling, not
  substance. → Reframe the blinded claims accordingly; the rubric and
  execution rungs carry what they can.

Comparison anchor (recorded before the sham run): real patches' pooled blinded
share = 128/130 = 98.5% (post-repair), 24/26 agents strict-majority
(pre-repair confirmatory).

## Budget

≤ $2 at the accounting rate ($1.25/$10 per Mtok); one pass; no re-rolls. A
sham vote is never re-run because of its outcome.
