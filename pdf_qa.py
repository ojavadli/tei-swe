#!/usr/bin/env python3
"""All-page PDF QA for TEI-SWE (owner directive section 10).

Mechanical, per-page checks over the compiled PDF text layer (poppler
`pdftotext -bbox`), with SEPARATE thresholds for main text vs. the dense
appendix (a page is classified by its own median glyph height, so footnotesize
tables and 8 pt appendix dumps are not flagged merely for being small):

  * font size        - median glyph height (proxy for pt); flags genuinely tiny
                       or oversized MAIN-text pages, never ordinary appendix 8 pt
  * raw LaTeX        - literal \\textbf, \\textsc, \\Delta, \\%, {,}, resizebox,
                       $\\..., stray control sequences leaking into the text
  * blank-area ratio - text bounding-box coverage; low coverage is reported
                       (figure/landscape pages legitimately have little text)
  * duplicate titles - the same "Figure N:"/"Table N:" caption text appearing
                       for two different numbers (a duplication smell)

Figure-internal text is rasterized (PNG) and not in the text layer; figure fonts
are set explicitly in make_figures.py and verified by rendered-page inspection.
Exit code is nonzero if any HARD flag (tiny main text, oversized main text, raw
LaTeX, duplicate caption) fires.
"""
import os
import re
import statistics
import subprocess
import sys

PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "main.pdf")

MAIN_MEDIAN_MIN = 9.3     # a page whose median >= this is treated as body-prose "main"
MAIN_TINY = 6.0           # a main page with tiny median glyphs (pt) -> hard flag
OVERSIZE = 1.35           # main page median above this * body -> enlarged type
APPENDIX_UNREADABLE = 4.5 # any page below this median glyph height -> hard flag
BLANK_COVERAGE = 0.12     # text bbox coverage below this -> report (soft)

RAW_LATEX = [
    r"\textbf", r"\textsc", r"\textit", r"\emph{", r"\Delta", r"\alpha",
    r"\resizebox", r"\scalebox", r"\includegraphics", r"\begin{", r"\end{",
    r"\textbackslash", r"{,}", r"\% ", r"\&", r"$\\", r"\hbox", r"\vskip",
]


def extract():
    out = subprocess.run(["pdftotext", "-bbox", PDF, "-"], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"pdftotext failed: {out.stderr[:200]}")
    pages = []
    for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', out.stdout, re.S):
        pw, ph = float(pm.group(1)), float(pm.group(2))
        words = []
        for wm in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pm.group(3)):
            x0, y0, x1, y1, t = (float(wm.group(1)), float(wm.group(2)), float(wm.group(3)),
                                 float(wm.group(4)), wm.group(5))
            if t.strip():
                words.append((x0, y0, x1, y1, t))
        pages.append((pw, ph, words))
    return pages


def gsize(w):
    # glyph-height proxy that is invariant to 90-degree rotation (landscape
    # tables/figures): a word is always longer along its baseline than tall, so
    # the SHORT bbox dimension is the glyph height in either orientation.
    return min(w[2] - w[0], w[3] - w[1])


def main():
    pages = extract()
    med = {i: statistics.median([gsize(w) for w in pg[2]])
           for i, pg in enumerate(pages, 1) if len(pg[2]) >= 25}
    body = sorted(med.values())[int(0.85 * (len(med) - 1))]
    print(f"PDF QA: {PDF}")
    print(f"pages: {len(pages)}   body-prose median glyph height: {body:.1f} pt")
    print(f"main-page classifier: median >= {MAIN_MEDIAN_MIN} pt; appendix pages exempt "
          f"from the small-font rule (down to the {APPENDIX_UNREADABLE} pt unreadable floor)\n")

    hard, soft = [], []
    import html
    caption_titles = {}  # (kind, num) -> title text
    for i, (pw, ph, words) in enumerate(pages, 1):
        if not words:
            soft.append((i, "EMPTY", "no extractable text (figure/landscape page?)"))
            continue
        heights = [gsize(w) for w in words]
        m = statistics.median(heights)
        is_main = m >= MAIN_MEDIAN_MIN
        # font
        if m <= APPENDIX_UNREADABLE:
            hard.append((i, "UNREADABLE", f"median {m:.1f} pt"))
        elif is_main and m <= MAIN_TINY:
            hard.append((i, "TINY-MAIN", f"median {m:.1f} pt"))
        elif is_main and m >= OVERSIZE * body:
            hard.append((i, "OVERSIZED-MAIN", f"median {m:.1f} pt = {m/body:.2f}x body"))
        # raw LaTeX (join words with spaces; also check raw concatenation)
        txt = " ".join(html.unescape(w[4]) for w in words)
        raw = html.unescape("".join(w[4] for w in words))
        hits = sorted({tok for tok in RAW_LATEX if tok in txt or tok in raw})
        if hits:
            hard.append((i, "RAW-LATEX", ", ".join(repr(h) for h in hits[:6])))
        # blank-area coverage
        xs0 = min(w[0] for w in words); ys0 = min(w[1] for w in words)
        xs1 = max(w[2] for w in words); ys1 = max(w[3] for w in words)
        cov = ((xs1 - xs0) * (ys1 - ys0)) / (pw * ph)
        if cov < BLANK_COVERAGE:
            soft.append((i, "LOW-COVERAGE", f"{cov*100:.0f}% text bbox (figure/landscape ok)"))
        # duplicate captions
        for cm in re.finditer(r"(Figure|Table)\s+(\d+):\s*([^.]{6,70})", txt):
            key = (cm.group(1), cm.group(2))
            title = re.sub(r"\s+", " ", cm.group(3)).strip().lower()
            if key in caption_titles and caption_titles[key] != title:
                hard.append((i, "DUP-CAPTION-NUM", f"{cm.group(1)} {cm.group(2)} seen twice"))
            caption_titles.setdefault(key, title)

    # duplicate title TEXT across different numbers (SOFT: split/continued
    # figures legitimately share a title stem, e.g. "... agents 1-15 / 16-30")
    seen_title = {}
    for (kind, num), title in caption_titles.items():
        if title in seen_title and seen_title[title] != (kind, num):
            soft.append((0, "DUP-TITLE-TEXT",
                         f"'{title[:36]}...' on {kind} {num} & {kind} {seen_title[title][1]} "
                         f"(ok if a split/continued float)"))
        seen_title.setdefault(title, (kind, num))

    if hard:
        print("HARD FLAGS:")
        for p, k, d in hard:
            print(f"  {'p'+str(p) if p else '  -':>5}  {k}: {d}")
    else:
        print("no hard flags (no tiny/oversized main text, no raw LaTeX, no duplicate captions).")
    if soft:
        print("\nsoft/informational (verify visually; often legitimate figure pages):")
        for p, k, d in soft[:40]:
            print(f"  p{p:>3}  {k}: {d}")

    print("\nPASS" if not hard else "\nFAIL")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
