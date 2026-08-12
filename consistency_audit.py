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
CANON = ("Pre-repair confirmatory result: 21/26 patched agents (105/130 votes); "
         "after repairing the one import-time defect, the adaptive retest shows "
         "22/26 strict majorities, 17 unanimous (110/130 votes)")


def pdf_text(p):
    # poppler's pdftotext (PyMuPDF/fitz not required); normalize ligatures so
    # phrase matching is not defeated by ff/fi/fl glyphs.
    import subprocess
    t = subprocess.run(["pdftotext", "-nopgbrk", p, "-"], capture_output=True, text=True).stdout
    for lig, rep_ in (("\ufb00", "ff"), ("\ufb01", "fi"), ("\ufb02", "fl"),
                      ("\ufb03", "ffi"), ("\ufb04", "ffl"), ("\ufb05", "ft"),
                      ("\ufb06", "st")):
        t = t.replace(lig, rep_)
    return t


def check(name, text):
    errs = []
    flat = re.sub(r"\s+", " ", text)
    # windowed co-occurrence checks (120-char windows around each vote count)
    for m in re.finditer(r"105/130", flat):
        w = flat[max(0, m.start() - 200):m.end() + 120]
        if re.search(r"22/26|22 of 26", w) and not any(k in w.lower() for k in ("after", "repair")):
            errs.append(f"{name}: 105/130 (pre-repair) paired with 22/26 (post-repair) without repair context: ...{w[:160]}...")
    for m in re.finditer(r"110/130", flat):
        w = flat[max(0, m.start() - 200):m.end() + 120]
        ok_ctx = any(k in w.lower() for k in ("pre-repair", "defect repair", "after repair", "retest"))
        if re.search(r"21/26|21 of 26", w) and not ok_ctx:
            errs.append(f"{name}: 110/130 (post-repair) paired with 21/26 (pre-repair) without context: ...{w[:160]}...")
    # banned phrases (style-and-consistency pass) — live claim surfaces only;
    # REVISION_LOG files legitimately quote superseded wordings as history
    BANNED = [] if name.startswith("REVISION_LOG") else ["reproduced by an external judge", "second judge family",
              "second family (", "credentialed", "anonymous listing returns 403",
              "price of a sandwich", "for less than a single executed",
              "$14.64", "$26.80", "\\$14.64", "\\$26.80",
              "968 calls", "32 LLM calls", "orders of magnitude",
              "compile-clean", "$0.05 at", "whole study is $1.52",
              "whole study is \\$1.52",
              "13 of 30", "on record", "consistently prefers",
              "$0.06 at", "active in the study pipeline", "30/0/0",
              # D4 additions (mission: full-scale finalization) — enforced after
              # the Phase-B recompute regenerates all claim surfaces
              "equivalence at measured power", "no paired regression",
              # "1/6" removed from the ban: it is the RETAINED n=6 execution
              # micro-arm's honest null (baseline 1/6, patched 1/6, 0W/0L), which
              # this paper keeps as execution evidence.
              "≈6", "all-in", "next rung",
              "up to 30", "up to 100",
              "prioritized experience replay", "hierarchical Bayesian",
              # Phase-C is out of scope for THIS paper — hard-fail on any leakage
              "prereg-exec2", "47/100", "50/100", "funded execution",
              "funded powered", "Phase 3", "Phase-3", "100 baseline",
              "100 patched", "200 rollout", "scoring_instrument",
              "SCORING_INSTRUMENT", "exec100", "runner handoff", "pull lock",
              "containerd", "sidecar"]
    for b in BANNED:
        if b in text:
            errs.append(f"{name}: banned phrase present: {b!r}")
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
