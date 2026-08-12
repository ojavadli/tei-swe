#!/usr/bin/env python3
"""Publication figures for TEI-SWE (value-forward, deployed-value, substrate-labeled).
Four figures, one coherent visual language: one accent (teal), one neutral gray,
one secondary (amber). Grayscale-safe (color + shape). Text-width, explicit fonts.
NO Phase-C content anywhere.

Rendering note: matplotlib runs with text.usetex=False and text.parse_math=False,
so every string is literal. Use plain text and unicode (Δ · ≈ %), never LaTeX
markup (\\textbf, \\textsc, \\&, \\%, $...$, {,}); use fontweight= for bold.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = os.path.expanduser("~/swebench-agents")
OUT = os.path.join(ROOT, "paper", "figures")
RC = json.load(open(os.path.join(ROOT, "_paper_recompute.json")))["summary"]
AP = RC["APPLIED"]; PR = RC["PROPOSED"]
FD = json.load(open(os.path.join(OUT, "_fig_data.json")))  # canonical dims/stages (make_assets)

ACCENT = "#0f766e"      # teal (TEI)
GRAY = "#6b7280"        # neutral (baseline)
AMBER = "#b45309"       # secondary (control / not-reported)
LIGHT = "#e5e7eb"
plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.titlesize": 9.5,
    "axes.labelsize": 9, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "legend.fontsize": 8.5, "figure.dpi": 300, "savefig.dpi": 300,
    "axes.spines.top": False, "axes.spines.right": False,
    "text.usetex": False, "text.parse_math": False,
})
TW = 6.9  # text width in inches


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("wrote", name)


# ==================================================================== FIGURE 1
def fig_value():
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(TW, 2.5),
                                  gridspec_kw={"width_ratios": [1.0, 1.18, 1.0],
                                               "wspace": 0.55})
    fig.subplots_adjust(left=0.02, right=0.995, top=0.90, bottom=0.14)
    # --- Panel A: scale / coverage ---
    a.axis("off")
    a.set_title("Scale & coverage", loc="left", fontweight="bold")
    rows = [("30", "third-party systems"),
            ("6,000", "audited candidates"),
            ("3,373", "committed patches"),
            ("$1.79", "LLM cost / system")]
    y = 0.94
    for big, small in rows:
        a.text(0.0, y, big, fontsize=15.5, fontweight="bold", color=ACCENT, va="top")
        a.text(0.0, y - 0.105, small, fontsize=7.6, color="#374151", va="top")
        y -= 0.235
    a.text(0.0, -0.02, "3,000 struct + 3,000 prompt\n≈$0.009 / candidate",
           fontsize=7.0, color=GRAY, va="top", linespacing=1.35)
    a.set_xlim(0, 1); a.set_ylim(0, 1)

    # --- Panel B: deployed improvement (slope) ---
    stages = ["Default", "Structural", "Final"]
    dep = [AP["base"], AP["struct"], AP["final"]]
    ceil = [PR["base"], PR["struct"], PR["final"]]
    x = [0, 1, 2]
    b.plot(x, ceil, "--", color=GRAY, lw=1.1, marker="o", ms=3, zorder=2,
           label=f"best proposed (ceiling +{PR['rel_gain_pct']:.0f}%)")
    b.plot(x, dep, "-", color=ACCENT, lw=2.4, marker="o", ms=6, zorder=3,
           label="deployed / committed")
    for xi, yi in zip(x, dep):
        off = (13, 2) if xi == 0 else (0, 9)
        ha = "left" if xi == 0 else "center"
        b.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points",
                   xytext=off, ha=ha, fontsize=8.5, fontweight="bold", color=ACCENT)
    b.legend(loc="lower right", fontsize=6.6, frameon=False,
             handlelength=1.6, borderaxespad=0.2)
    b.set_xticks(x); b.set_xticklabels(stages)
    b.set_ylim(min(dep) - 0.03, max(ceil) + 0.045)
    b.set_ylabel("anchored rubric aggregate")
    b.set_title("Deployed improvement", loc="left", fontweight="bold")
    b.text(0.02, 0.99, f"+{AP['abs_gain']:.3f} abs    +{AP['rel_gain_pct']:.1f}% rel",
           transform=b.transAxes, fontsize=9, color=ACCENT, va="top", fontweight="bold")
    b.text(0.02, 0.86, "committed artifact · anchored RUBRIC / proxy substrate",
           transform=b.transAxes, fontsize=6.4, color="#374151", va="top")

    # --- Panel C: bias-controlled confirmation ---
    c.axis("off")
    c.set_title("Bias-controlled confirmation", loc="left", fontweight="bold")
    pairs = [("22 / 26", "strict blinded majorities"),
             ("110 / 130", "patched votes"),
             ("17", "unanimous"),
             ("4", "prefer baseline")]
    y = 0.92
    for big, small in pairs:
        col = ACCENT if big != "4" else AMBER
        c.text(0.0, y, big, fontsize=15, fontweight="bold", color=col, va="top")
        c.text(0.0, y - 0.095, small, fontsize=8, color="#374151", va="top")
        y -= 0.235
    c.text(0.0, -0.03, "preferred with direction, score, and rationale hidden (blinded A/B)",
           fontsize=6.8, color=GRAY, va="top", wrap=True)
    c.set_xlim(0, 1); c.set_ylim(0, 1)
    save(fig, "fig_value.png")


# ==================================================================== FIGURE 2
def fig_method():
    fig, ax = plt.subplots(figsize=(TW, 4.0)); ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)

    def box(x, y, w, h, title, detail="", fc="white", ec=ACCENT, tfs=6.7, dfs=5.7,
            tcol="#111827"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.6",
                                    fc=fc, ec=ec, lw=1.1, zorder=2))
        cx = x + w / 2
        if detail:
            ax.text(cx, y + h * 0.66, title, ha="center", va="center", fontsize=tfs,
                    fontweight="bold", zorder=3, color=tcol, linespacing=1.0)
            ax.text(cx, y + h * 0.24, detail, ha="center", va="center", fontsize=dfs,
                    zorder=3, color="#374151", linespacing=1.05)
        else:
            ax.text(cx, y + h / 2, title, ha="center", va="center", fontsize=tfs,
                    fontweight="bold", zorder=3, color=tcol, linespacing=1.0)

    def arrow(x1, y1, x2, y2, color=ACCENT, lw=1.2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=9, color=color, lw=lw, zorder=1))

    ax.text(2, 97.5, "TEI optimizes both the structural (code/workflow) and prompt surfaces",
            fontsize=8.6, color="#111827", fontweight="bold", va="top")

    # ---- main path row (7 stages) ----
    teal_fc = "#f0fdfa"; gray_fc = "#f3f4f6"
    steps = [
        ("Third-party\nagent", "", GRAY, gray_fc),
        ("TARGET", "weak dim ·\nfailure modes", ACCENT, teal_fc),
        ("EVALUATE", "baseline ·\nfixed probes", ACCENT, teal_fc),
        ("IMPROVE\nstructure", "code / workflow", ACCENT, teal_fc),
        ("GATE →\nSELECT", "kill · do-no-harm", ACCENT, teal_fc),
        ("IMPROVE\nprompt", "instr. · retrieval", ACCENT, teal_fc),
        ("Deployed\nartifact", "", ACCENT, teal_fc),
    ]
    w, h, step, y0 = 11.6, 15, 14.05, 66
    xs = [2 + i * step for i in range(7)]
    for i, (t, d, ec, fc) in enumerate(steps):
        box(xs[i], y0, w, h, t, d, fc=fc, ec=ec,
            tcol=(ACCENT if (i in (3, 5, 6)) else "#111827"))
        if i:
            arrow(xs[i - 1] + w, y0 + h / 2, xs[i], y0 + h / 2)

    # ---- feedback loop ----
    box(30, 42, 22, 12, "WHY-RECORDS", "6,000 records: score + why",
        ec=GRAY, fc="#f9fafb", tfs=6.6, dfs=5.6)
    box(58, 42, 24, 12, "BAYESIAN CREDIT LEDGER", "Thompson family selection",
        ec=ACCENT, fc=teal_fc, tfs=6.4, dfs=5.6)
    # improve stages -> why-records (down); ledger -> next proposal (up into prompt stage)
    arrow(xs[3] + w / 2, y0, 41, 54, color=GRAY)
    arrow(52, 48, 58, 48, color=GRAY)
    arrow(70, 54, xs[5] + w / 2, y0, color=GRAY)
    ax.text(71.5, 60.5, "next proposal", fontsize=5.8, color=GRAY, ha="left", va="center")

    # ---- validation ladder (bottom strip) ----
    ax.text(2, 30, "VALIDATION\nLADDER", fontsize=6.8, fontweight="bold", color="#111827",
            va="center", linespacing=1.05)
    lad = [("RUBRIC", ACCENT), ("BLINDED A/B", ACCENT), ("STATIC pre-gate", ACCENT),
           ("EXECUTION\n(n=36, retained)", GRAY)]
    lw_, lh, lstep, lx0, ly0 = 17, 10, 20, 17, 24
    for i, (s, ec) in enumerate(lad):
        lx = lx0 + i * lstep
        box(lx, ly0, lw_, lh, s, ec=ec, fc=(teal_fc if ec == ACCENT else gray_fc), tfs=6.2)
        if i:
            arrow(lx0 + (i - 1) * lstep + lw_, ly0 + lh / 2, lx, ly0 + lh / 2, color=GRAY)
    ax.text(lx0, ly0 - 2.4, "increasing evidence strength  →", fontsize=5.6, color=GRAY, va="top")

    # ---- callout band (amber, prominent) ----
    ax.add_patch(FancyBboxPatch((2, 3.5), 96, 10, boxstyle="round,pad=0.4,rounding_size=1.6",
                                fc="#fffbeb", ec=AMBER, lw=1.3, zorder=2))
    ax.text(50, 10.2, "0 executed benchmark rollouts", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#7c2d12", zorder=3)
    ax.text(50, 6.0, "used as the Phase-A/B candidate-selection signal  ·  selection uses rubric / blinded / static only",
            ha="center", va="center", fontsize=6.8, color="#7c2d12", zorder=3)
    save(fig, "fig_method.png")


# ==================================================================== FIGURE 3
def fig_validation():
    fig, axs = plt.subplots(1, 4, figsize=(TW, 2.55),
                            gridspec_kw={"wspace": 0.62})
    fig.subplots_adjust(top=0.80, bottom=0.20, left=0.07, right=0.985)
    A, B, C, D = axs

    def note(ax, s, color="#374151"):
        ax.text(0.5, 0.965, s, transform=ax.transAxes, fontsize=6.2, va="top",
                ha="center", color=color, linespacing=1.15)

    # A blinded
    A.bar([0, 1], [22, 4], color=[ACCENT, AMBER], width=0.62)
    A.set_xticks([0, 1]); A.set_xticklabels(["TEI\nmajority", "baseline\nmajority"])
    A.set_ylim(0, 30); A.set_ylabel("systems (of 26)", fontsize=8)
    for xi, v in zip([0, 1], [22, 4]):
        A.text(xi, v + 0.5, str(v), ha="center", fontsize=8.5, fontweight="bold")
    A.set_title("Blinded\nA/B", loc="center", fontsize=8.3, fontweight="bold")
    note(A, "110/130 votes · 17 unan.")

    # B sham
    B.bar([0, 1], [84.6, 26.9], color=[ACCENT, GRAY], width=0.62, hatch=["", "//"])
    B.set_xticks([0, 1]); B.set_xticklabels(["real\npatches", "sham\nplacebo"])
    B.set_ylim(0, 112); B.set_yticks([0, 20, 40, 60, 80, 100])
    B.set_ylabel("% of votes", fontsize=8)
    for xi, v in zip([0, 1], [84.6, 26.9]):
        B.text(xi, v + 2.0, f"{v:.1f}%", ha="center", fontsize=8, fontweight="bold")
    B.set_title("Sham\nplacebo", loc="center", fontsize=8.3, fontweight="bold")
    note(B, "re-anchor 0/45 (9 agents)")

    # C random (rubric delta)
    C.bar([0, 1], [0.0630, 0.0165], color=[ACCENT, GRAY], width=0.62, hatch=["", ".."])
    C.set_xticks([0, 1]); C.set_xticklabels(["TEI\ndiagnosis", "random\nproposals"])
    C.set_ylabel("rubric Δ", fontsize=8)
    for xi, v in zip([0, 1], [0.0630, 0.0165]):
        C.text(xi, v + 0.0012, f"+{v:.4f}", ha="center", fontsize=7.5, fontweight="bold")
    C.set_ylim(0, 0.088)
    C.set_title("Budget-matched\nrandom", loc="center", fontsize=8.3, fontweight="bold")
    note(C, "blinded 10/10 vs 0/10")

    # D cross-provider (honest)
    D.bar([0, 1], [17, 30], color=[ACCENT, GRAY], width=0.62, hatch=["", "xx"])
    D.set_xticks([0, 1]); D.set_xticklabels(["patched", "baseline"])
    D.set_ylim(0, 42); D.set_yticks([0, 10, 20, 30, 40])
    D.set_ylabel("votes (of 50)", fontsize=8)
    for xi, v in zip([0, 1], [17, 30]):
        D.text(xi, v + 0.9, str(v), ha="center", fontsize=8.5, fontweight="bold")
    D.set_title("Cross-provider\njudge", loc="center", fontsize=8.3, fontweight="bold", color=AMBER)
    note(D, "3/10 vs 6/10 maj.\n(does NOT reproduce)", color=AMBER)
    save(fig, "fig_validation.png")


# ==================================================================== FIGURE 4
def fig_compare():
    methods = ["TEI-SWE", "GEPA", "ACE", "Maestro", "HiveMind", "MIPROv2"]
    axes = ["structural\nopt.", "prompt\nopt.", "struct+\nprompt",
            "0 exec.\nfor select.", "blinded\nvalid.", "placebo\ncontrol",
            "random\ncontrol", "static\npre-gate", "per-cand.\nscore+why", "$ cost\nreported"]
    # Y=yes(1), N=no(0), R=n.r.(0.5)
    Y, N, R = 1, 0, 0.5
    grid = [
        [30, Y, Y, Y, Y, Y, Y, Y, Y, Y, Y],          # TEI (first col = #systems)
        [6,  N, Y, N, N, N, N, N, N, N, R],           # GEPA
        [1,  N, Y, N, N, N, N, N, N, N, R],           # ACE
        [1,  Y, Y, Y, N, N, N, N, N, N, R],           # Maestro (graph+config)
        [1,  N, Y, N, N, N, N, N, N, N, R],           # HiveMind
        [7,  N, Y, N, N, N, N, N, N, N, R],           # MIPROv2
    ]
    fig, ax = plt.subplots(figsize=(TW, 2.6))
    ncol = len(axes)
    for i, row in enumerate(methods):
        # systems count as text in col 0
        ax.text(-0.9, len(methods) - 1 - i, str(grid[i][0]), ha="center", va="center",
                fontsize=8, fontweight="bold", color=(ACCENT if i == 0 else "#374151"))
        for j in range(ncol):
            v = grid[i][j + 1]
            yy = len(methods) - 1 - i
            if v == Y:
                ax.scatter(j, yy, s=95, marker="o", color=ACCENT if i == 0 else "#374151", zorder=3)
            elif v == R:
                ax.scatter(j, yy, s=70, marker="D", facecolor="white", edgecolor=AMBER, lw=1.2, zorder=3)
            else:
                ax.scatter(j, yy, s=55, marker="x", color="#9ca3af", lw=1.4, zorder=3)
    ax.set_xticks(range(ncol)); ax.set_xticklabels(axes, fontsize=6.6)
    ax.set_yticks(range(len(methods))); ax.set_yticklabels(methods[::-1], fontsize=8.2)
    ax.text(-0.9, len(methods) - 0.35, "#sys", ha="center", fontsize=6.6, color="#374151")
    ax.set_xlim(-1.6, ncol - 0.5); ax.set_ylim(-0.6, len(methods) - 0.3)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    # legend
    ax.scatter([], [], marker="o", s=80, color="#374151", label="yes")
    ax.scatter([], [], marker="x", s=55, color="#9ca3af", label="no")
    ax.scatter([], [], marker="D", s=60, facecolor="white", edgecolor=AMBER, label="n.r.")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=3, frameon=False)
    ax.set_title("Method characteristics (primary-source audit; teal = TEI verified advantage)",
                 loc="left", fontsize=8, fontweight="bold")
    save(fig, "fig_compare.png")


# ==================================================================== FIGURE 5 (dims)
def fig_dims():
    d = FD["dims"]
    order = d["order"]
    labels = [d["labels"][k] for k in order]
    base = [d["baseline"][k] for k in order]
    dep = [d["deployed"][k] for k in order]
    fig, ax = plt.subplots(figsize=(TW, 2.35))
    fig.subplots_adjust(left=0.20, right=0.90, top=0.86, bottom=0.17)
    y = list(range(len(order)))[::-1]
    for yi, b, f in zip(y, base, dep):
        ax.plot([b, f], [yi, yi], color=LIGHT, lw=3.2, zorder=1, solid_capstyle="round")
        ax.scatter(b, yi, s=64, color=GRAY, zorder=3)
        ax.scatter(f, yi, s=92, color=ACCENT, zorder=3)
        ax.annotate(f"{b:.3f}", (b, yi), textcoords="offset points", xytext=(-7, 0),
                    ha="right", va="center", fontsize=7.3, color=GRAY)
        ax.annotate(f"{f:.3f}", (f, yi), textcoords="offset points", xytext=(7, 0),
                    ha="left", va="center", fontsize=7.3, fontweight="bold", color=ACCENT)
        ax.annotate(f"+{f - b:.3f}", ((b + f) / 2, yi), textcoords="offset points",
                    xytext=(0, 6.5), ha="center", fontsize=6.6, color="#374151")
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.6)
    ax.set_xlabel("anchored rubric dimension score  (RUBRIC / proxy)", fontsize=8)
    ax.set_xlim(0.45, 0.80); ax.set_ylim(-0.6, len(order) - 0.1)
    ax.scatter([], [], color=GRAY, s=64, label="baseline")
    ax.scatter([], [], color=ACCENT, s=92, label="deployed")
    ax.legend(loc="upper left", frameon=False, fontsize=7.4, handletextpad=0.3,
              bbox_to_anchor=(0.0, 1.02))
    ax.set_title("Deployed artifacts raise all four rubric dimensions (largest: execution accuracy)",
                 loc="left", fontsize=8.4, fontweight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(length=0)
    save(fig, "fig_dims.png")


if __name__ == "__main__":
    fig_value(); fig_method(); fig_validation(); fig_compare(); fig_dims()
    print("all figures written")
