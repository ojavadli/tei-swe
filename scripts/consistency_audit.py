#!/usr/bin/env python3
"""consistency_audit: fail if any surface mixes pre-repair agent counts with
post-repair vote counts (or vice versa), or drops the canonical sentence.

Canonical convention:
  pre-repair : 24/26 agents <-> 118/130 votes
  post-repair: 26/26 strict majorities, 24 unanimous <-> 128/130 votes

Checked surfaces: compiled PDF text, README.md, PROVENANCE.md,
TEI_SWEBENCH_REPORT.md, REVISION_LOG*.md.
"""
import os
import re
import sys

ROOT = os.path.expanduser("~/swebench-agents")
CANON = ("Pre-repair confirmatory result: 24/26 patched agents (118/130 votes); "
         "after defect repair, the adaptive retest shows 26/26 strict majorities, "
         "24 unanimous (128/130 votes)")


def pdf_text(p):
    import fitz
    return "\n".join(pg.get_text() for pg in fitz.open(p))


def check(name, text):
    errs = []
    flat = re.sub(r"\s+", " ", text)
    # windowed co-occurrence checks (120-char windows around each vote count)
    for m in re.finditer(r"118/130", flat):
        w = flat[max(0, m.start() - 120):m.end() + 120]
        if re.search(r"26/26|26 of 26", w) and "after" not in w.lower():
            errs.append(f"{name}: 118/130 paired with 26/26 without repair context: ...{w[:160]}...")
    for m in re.finditer(r"128/130", flat):
        w = flat[max(0, m.start() - 120):m.end() + 120]
        if re.search(r"24/26|24 of 26", w) and "pre-repair" not in w.lower():
            errs.append(f"{name}: 128/130 paired with 24/26 without pre-repair context: ...{w[:160]}...")
    # forbid the stale standalone claims
    if re.search(r"blinded[^.]{0,80}confirm[^.]{0,80}26 of 26(?![^.]*repair)", flat, re.I):
        errs.append(f"{name}: '26 of 26 blinded-confirmed' without repair qualifier")
    return errs


def main():
    surfaces = {}
    pdf = os.path.join(ROOT, "paper", "TEI-SWE.pdf")
    if os.path.isfile(pdf):
        surfaces["TEI-SWE.pdf"] = pdf_text(pdf)
    for f in ("README.md", "PROVENANCE.md", "TEI_SWEBENCH_REPORT.md",
              "REVISION_LOG.md", "REVISION_LOG_2.md", "REVISION_LOG_3.md"):
        p = os.path.join(ROOT, "release", f) if f == "README.md" else os.path.join(ROOT, f)
        if os.path.isfile(p):
            surfaces[f] = open(p, errors="ignore").read()

    errs = []
    for name, text in surfaces.items():
        errs += check(name, text)
    # canonical sentence must appear in the PDF abstract and the README
    for must in ("TEI-SWE.pdf", "README.md"):
        if must in surfaces and CANON.split(";")[0] not in re.sub(r"\s+", " ", surfaces[must]):
            errs.append(f"{must}: canonical sentence missing")
    if errs:
        print("CONSISTENCY AUDIT FAILED:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"consistency audit PASSED over {len(surfaces)} surfaces")


if __name__ == "__main__":
    main()
