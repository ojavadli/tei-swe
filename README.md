# TEI-SWE: Blinded-Confirmed Improvements to 24/26 Patched SWE-bench Agents at ~$0.50 Each

Artifacts for **"Blinded-Confirmed Improvements to 24 of 26 Patched SWE-bench
Agents at About Half a Dollar Each: A Gated Target-Evaluate-Improve Loop with
a Validation Ladder (TEI-SWE)"**. Certification controls: pre-registered sham
placebo (tag `prereg-sham`; CERTIFIED branch fired at 26.9% sham share vs 98.5%
real), budget-matched random-proposal arm (TEI 10/10), external-provider judge
(0/40 sham votes), executed do-no-harm micro-arm.

## What is here

| Path | Contents |
|---|---|
| `paper/` | LaTeX source, compiled PDF, and the generators that emit every number from recorded JSON |
| `manifest.{json,csv}`, `PROVENANCE.md` | the frozen **TEI-SWE-30** agent set: 30 SWE-bench leaderboard systems, repo URLs + SHAs, selection funnel |
| `agents/<rank>_<slug>/tei/` | per-agent records: onboarding, baseline evaluation, `candidates.jsonl` (why-records), result, diagnosis, report |
| `agents/<rank>_<slug>/patches/` | the applied changes as `git format-patch` series against the recorded SHA (no third-party code is redistributed) |
| `datasets/tei-swe-30-why-records.jsonl` | all 1,140 candidate why-records (phase, technique, target failure mode, evidence, patch, scores, decision, rationale) |
| `datasets/tei-swe-30-blinded-votes.json` | every blinded A/B vote with reasons, pre- and post-repair |
| `datasets/syntax_audit*.json`, `validation_passes.json` | static audits; measured-noise, second-judge, and trajectory passes |
| `scripts/` | the full pipeline: set construction -> loop -> audits -> blinded validation -> paper |

## Reproduce

```bash
python scripts/build_manifest.py --splits lite verified
python scripts/stage_clones.py && python scripts/finalize_manifest.py
python scripts/find_prompt_surface.py
export OPENAI_API_KEY=...   # never committed
python scripts/tei_pipeline.py --struct-iters 30 --prompt-iters 30 --batch 6 --probes 4
python scripts/verify_integrity.py && python scripts/blind_reval.py
python scripts/validation_passes.py && python scripts/make_reports.py
cd paper && python make_assets.py && python make_narrative.py && tectonic main.tex
```

## Use this to audit your own loop

The two highest-value components transfer to any optimizer in an afternoon:

1. **Blinded A/B** (`scripts/blind_reval.py`): point it at any repo with a
   baseline SHA and a candidate branch. It shows a judge the real before/after
   hunks in randomized order -- no narrative, no direction -- k times, and
   reports votes. If your optimizer's "wins" do not survive this, they were
   narrative.
2. **Static pre-gate** (`tei_loop.gate.static_pregate` in the tei-loop repo,
   or the inline check in `scripts/tei_pipeline.py`): reject any candidate
   whose patch breaks `ast.parse` *before* spending a judge call. In this
   study that free check caught a patch-damage mode that anchored rubric
   scoring had scored as improvements.

Ladder rule of thumb: rubric < blinded A/B < static checks < execution.
Climb as high as your substrate allows; label every claim with its rung.

## Datasets

The two datasets are also intended for standalone use (LLM-judge bias,
optimization-under-weak-signals research): `tei-swe-30-why-records.jsonl`
(1,140 records) and `tei-swe-30-blinded-votes.json` (26 agents x 5 votes,
pre/post-repair). Hugging Face mirrors pending token availability; Zenodo DOI
pending token availability -- both blocked only on credentials, tracked in
REVISION_LOG.md.
