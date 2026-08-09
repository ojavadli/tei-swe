# TEI: Target--Evaluate--Improve (TEI-SWE)

**TEI: Target--Evaluate--Improve --- A Cost-Efficient Self-Improving Loop for
Agentic Systems via Sequential Decision Gating (TEI-SWE)**
Orkhan Javadli (MIT, ojavadli@mit.edu) and Anni Zimina (Stanford,
zimina@stanford.edu).

Headline (canonical convention): Pre-repair confirmatory result: 24/26 patched agents (118/130 votes); after defect repair, the adaptive retest shows 26/26 strict majorities, 24 unanimous (128/130 votes).
Certification: pre-registered sham placebo (tag `prereg-sham`) draws 26.9% of
votes, rejecting the generic changed-code/style explanation for the primary
judge's preference; TEI beats budget-matched unguided generation on 10/10
agents; execution micro-arm confirms do-no-harm (SWE-agent, 6 paired
instances, 0 losses). All numbers macro-generated from the JSON in this repo.

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
