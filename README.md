# TEI: Target--Evaluate--Improve (TEI-SWE)

**TEI: Target--Evaluate--Improve --- A Cost-Efficient Self-Improving Loop for
Agentic Systems via Sequential Decision Gating (TEI-SWE)**
Orkhan Javadli (MIT, ojavadli@mit.edu) and Anni Zimina (Stanford,
zimina@stanford.edu).

Headline (canonical convention): Pre-repair confirmatory result: 21/26 patched agents (105/130 votes); after repairing the one import-time defect, the adaptive retest shows 22/26 strict majorities, 17 unanimous (110/130 votes), with 4 agents preferring the baseline.

Automated optimization of LLM agents is typically shown on a few author-chosen
tasks, with candidates selected by biased judges. TEI is a self-improving loop
built on sequential decision gating -- sequential paired evaluation with exact
futility bounds and Jeffreys Beta-Binomial posterior early kills over discordant
pairs, Wilson-LCB Pareto selection, and a Bayesian do-no-harm confirmation, plus
a two-head Bayesian bandit credit ledger (Jeffreys-Beta reliability + Normal
magnitude heads with Thompson selection) steering which fix family each proposal
attempts. Applied to all 30 frozen leaderboard systems, TEI generated 6,000
audited candidate versions (100 structural + 100 prompt per system) and 3,373
committed patches, each scored and why-recorded, at ~$1.79/agent (combined
accounting rate). Contemporary optimizers -- GEPA, MIPROv2, Maestro, ACE,
HiveMind -- report hundreds to thousands of executed rollouts per single
benchmark where counts are reported, with no comparable placebo-plus-blinded
validation in our review.

Crucially, zero executed benchmark rollouts were used as the candidate-selection
signal: the 6,000-version search runs on anchored-rubric proxy evaluation,
sequential gating, blinding, and static checks. Honest nulls bound the claims: a
pre-registered credit-ledger ablation shows no detectable benefit over a simple
best-so-far proposer (2W/3L, sign p=1.0), and the pre-registered gpt-4o-mini
paired execution arm (n=36; 3/36 vs 3/36) shows no detectable execution-rung
difference at its measured power. Certification: the pre-registered sham placebo
(tag `prereg-sham`) draws 26.9% of votes, and re-anchored at the new bests draws
0/45; TEI beats budget-matched unguided generation on 10/10 agents. (Transfer to
end-task execution at larger scale is a separate future study, outside this
paper's scope.)
All numbers macro-generated from the JSON in this repo.

Compiled paper: `paper/TEI-SWE.pdf` (sha256 recorded in RELEASE_CHECKSUM).

## What is here

| Path | Contents |
|---|---|
| `paper/` | LaTeX source, compiled PDF, generators emitting every number from recorded JSON |
| `manifest.{json,csv}`, `PROVENANCE.md` | the frozen **TEI-SWE-30** set (30 systems, 29 distinct repos; defects documented in the paper, S3.1) |
| `agents/<rank>_<slug>/tei/` + `patches/` | per-agent records + format-patch series |
| `datasets/` | why-records (1,140), blinded votes (pre/post-repair), sham arm, random arm, cross-provider check (appendix data), audits, validation passes, PREREG_SHAM.md |
| `scripts/` | full pipeline + `tei_audit.py` + `consistency_audit.py` |

## Audit your own loop (one command)

```bash
python scripts/tei_audit.py --repo /path/to/repo --base <sha> --cand HEAD
```
Runs the two cheapest rungs of the validation ladder (syntax pre-gate +
blinded A/B) against any optimizer's diff.

## Cite

```bibtex
@misc{teiswe2026,
  title  = {TEI: Target--Evaluate--Improve --- A Cost-Efficient Self-Improving
            Loop for Agentic Systems via Sequential Decision Gating (TEI-SWE)},
  author = {Javadli, Orkhan and Zimina, Anni},
  year   = {2026},
  howpublished = {\url{https://github.com/ojavadli/tei-swe}},
  note   = {Zenodo DOI pending (see .zenodo.json)}
}
```

Zenodo DOI and Hugging Face mirrors: pending owner tokens (metadata ready in
`.zenodo.json`).
