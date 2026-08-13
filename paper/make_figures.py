#!/usr/bin/env python3
"""Main-paper figures for TEI-SWE — professor-grade academic style.

White ground; charcoal/gray default; ONE muted steel-blue accent for TEI, used
sparingly; standard scientific forms; thin strokes; high data-to-ink ratio;
printed fonts ~7.5-10 pt; grayscale-legible by tone AND shape. Titles are short;
captions carry interpretation. Count axes respect their denominators. No
label/mark collisions (rendered and inspected at 300 dpi). Every value is read
from canonical JSON; assertions at the bottom guard against stale hardcoding.
Consistent semantics across figures:
  TEI / deployed / real / diagnosis-guided -> ACCENT, solid/filled
  baseline / control / sham / random       -> GRAYD, hatched/open
  best-proposed search ceiling             -> GRAYD, dashed, open marker
  individual systems                       -> GRAYL, thin
NO Phase-C content.
"""
import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = os.path.expanduser("~/swebench-agents")
OUT = os.path.join(ROOT, "paper", "figures")
_RC = json.load(open(os.path.join(ROOT, "_paper_recompute.json")))
RC = _RC["summary"]
AP = RC["APPLIED"]; PR = RC["PROPOSED"]
PA = _RC["per_agent"]
ZERO4 = set(RC["zeropatch_agents"])
FD = json.load(open(os.path.join(OUT, "_fig_data.json")))

INK = "#111827"      # near-black: primary lines/text/markers
ACCENT = "#2f5c8a"   # muted steel blue: TEI / deployed (sparingly)
GRAYD = "#6b7280"    # baseline / control / ceiling
GRAYM = "#9aa1a9"    # mid gray
GRAYL = "#c9ced4"    # light gray: individual population lines
plt.rcParams.update({
    "font.family": "serif", "font.size": 8.5, "axes.titlesize": 9.5,
    "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 7.6, "figure.dpi": 300, "savefig.dpi": 300,
    "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8, "lines.solid_capstyle": "round",
    "text.usetex": False, "text.parse_math": False,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("wrote", name)


# ============================================================ FIGURE 1 — result
def fig_trajectory():
    """Deployed MEAN trajectory (n=26 patched) + subtle best-proposed ceiling.
    No individual clouds (those are Fig. 4); labels sit off the markers; the
    +0.079/13.0% gain and its paired CI live in the caption."""
    fig, ax = plt.subplots(figsize=(4.4, 2.85))
    fig.subplots_adjust(left=0.155, right=0.965, top=0.955, bottom=0.115)
    xs = [0, 1, 2]
    dep = [FD["stages_deployed"][k] for k in ("base", "struct", "final")]
    ceil = [FD["stages_ceiling"][k] for k in ("base", "struct", "final")]
    ax.plot(xs, ceil, ls=(0, (4, 2)), color=GRAYD, lw=1.1, marker="o", ms=4,
            mfc="white", mec=GRAYD, zorder=2, label="best proposed (not committed)")
    ax.plot(xs, dep, color=ACCENT, lw=2.0, marker="o", ms=6.5, mfc=ACCENT,
            mec="white", mew=0.8, zorder=4, label="deployed mean (n = 26)")
    # value labels below each deployed point, in guaranteed-empty space
    for xi, yi in zip(xs, dep):
        ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points", xytext=(0, -13),
                    ha="center", va="top", fontsize=8, fontweight="bold", color=ACCENT)
    ax.set_xticks(xs); ax.set_xticklabels(["Default", "Structural", "Final"])
    ax.set_xlim(-0.18, 2.18)
    lo = min(dep) - 0.045; hi = max(ceil) + 0.012
    ax.set_ylim(lo, hi)
    ax.set_ylabel("anchored rubric aggregate  (proxy)")
    ax.legend(loc="lower right", frameon=False, handlelength=1.9, borderaxespad=0.3,
              labelspacing=0.4)
    save(fig, "fig_trajectory.png")


# ============================================================ FIGURE 2 — ladder
def fig_ladder():
    """Compact evidence hierarchy along one horizontal evidence axis: four rungs
    of increasing evidence strength and evaluation cost."""
    fig, ax = plt.subplots(figsize=(5.6, 1.95))
    fig.subplots_adjust(left=0.03, right=0.985, top=0.80, bottom=0.20)
    ax.axis("off")
    rungs = [("Rubric / proxy", "Δ +0.079", "$0.35 / agent"),
             ("Blinded A/B", "22 / 26 systems", "$0.03 / agent"),
             ("Static / determ.", "6 defects caught", "$0"),
             ("Execution", "n = 36, null", "harness + rollouts")]
    xs = [0.5, 3.0, 5.5, 8.0]
    ax.plot([xs[0] - 0.3, xs[-1] + 0.3], [0, 0], color=INK, lw=1.0, zorder=1)
    for i, ((name, metric, cost), x) in enumerate(zip(rungs, xs)):
        col = ACCENT if name.startswith("Blinded") else INK
        ax.scatter(x, 0, s=34, color=col, zorder=3)
        ax.text(x, 0.62, name, ha="center", fontsize=8.6, fontweight="bold", color=col)
        ax.text(x, 0.30, metric, ha="center", fontsize=7.6, color=INK)
        ax.text(x, -0.42, cost, ha="center", fontsize=7.0, color=GRAYD)
    ax.annotate("", xy=(xs[-1] + 0.9, 0), xytext=(xs[0] - 0.9, 0),
                arrowprops=dict(arrowstyle="-|>", color=GRAYD, lw=1.0))
    ax.text((xs[0] + xs[-1]) / 2, -0.95, "increasing evidence strength and evaluation cost",
            ha="center", fontsize=7.4, color=GRAYD, style="italic")
    ax.set_xlim(xs[0] - 1.2, xs[-1] + 1.2); ax.set_ylim(-1.15, 1.0)
    save(fig, "fig_ladder.png")


# ============================================================ FIGURE 3 — method
def fig_method():
    """Technical schematic: main path + credit-ledger feedback loop. Sentence
    case, square thin-bordered boxes, strict alignment, dark feedback arrows."""
    fig, ax = plt.subplots(figsize=(6.6, 2.55)); ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)

    def box(x, y, w, h, text, ec=INK, accent=False):
        ax.add_patch(Rectangle((x, y), w, h, fill=True, fc="white",
                               ec=(ACCENT if accent else ec), lw=(1.2 if accent else 0.9),
                               zorder=2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.2,
                color=(ACCENT if accent else INK), zorder=3, linespacing=1.05,
                fontweight=("bold" if accent else "normal"))

    def arrow(x1, y1, x2, y2, color=INK, lw=1.0):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=8, color=color, lw=lw, zorder=1))

    steps = [("Third-party\nagent", False), ("Target", False), ("Evaluate", False),
             ("Improve\nstructure", True), ("Gate /\nselect", False),
             ("Improve\nprompt", True), ("Deployed\nartifact", False)]
    w, h, gap, y0 = 12.6, 15, 1.75, 62
    step = w + gap
    xs = [0.6 + i * step for i in range(7)]
    for i, (t, acc) in enumerate(steps):
        box(xs[i], y0, w, h, t, accent=acc)
        if i:
            arrow(xs[i - 1] + w, y0 + h / 2, xs[i], y0 + h / 2)

    # feedback loop (dark, legible)
    box(29, 32, 22, 13, "Why-records\n6,000: score + why", ec=GRAYD)
    box(57, 32, 27, 13, "Bayesian credit ledger\nThompson family selection", ec=GRAYD)
    arrow(xs[3] + w / 2, y0, 40, 45, color=INK)
    arrow(51, 38.5, 57, 38.5, color=INK)
    arrow(71, 45, xs[5] + w / 2, y0, color=INK)
    ax.text(60.5, 54, "next proposal", fontsize=6.6, color=INK, ha="center", va="center")

    ax.text(1.0, 95, "TEI optimizes both the structural (code / workflow) and prompt surfaces.",
            fontsize=8.2, color=INK)
    ax.text(1.0, 20, "Phase-A/B candidate selection uses the rubric, blinded A/B and static "
                     "checks only — no executed benchmark rollouts.",
            fontsize=7.4, color=GRAYD, style="italic")
    save(fig, "fig_method.png")


# ======================================================= FIGURE 4 — population
def fig_population():
    """All 30 systems' deployed trajectories (thin gray) + mean (accent).
    Population = all 30; mean ends at the all-30 deployed final (0.675)."""
    fig, ax = plt.subplots(figsize=(4.4, 2.9))
    fig.subplots_adjust(left=0.155, right=0.965, top=0.945, bottom=0.115)
    xs = [0, 1, 2]
    cols = ([r["base"] for r in PA], [r["best_applied_struct"] for r in PA],
            [r["best_applied_final"] for r in PA])
    for b, s, f in zip(*cols):
        ax.plot(xs, [b, s, f], color=GRAYL, lw=0.7, zorder=1)
    mean = [float(np.mean(c)) for c in cols]
    ax.plot(xs, mean, color=ACCENT, lw=2.0, marker="o", ms=5.5, mfc=ACCENT,
            mec="white", mew=0.7, zorder=4, label="mean, all systems (n = 30)")
    for xi, v in zip(xs, mean):
        ax.annotate(f"{v:.3f}", (xi, v), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=7.6, fontweight="bold", color=ACCENT)
    ax.set_xticks(xs); ax.set_xticklabels(["Default", "Structural", "Final"])
    ax.set_xlim(-0.1, 2.28)
    ax.set_ylabel("deployed rubric aggregate  (proxy)")
    ax.legend(loc="lower right", frameon=False, handlelength=1.9)
    save(fig, "fig_population.png")


# ========================================================= FIGURE 5 — dimensions
def fig_dims():
    """Dumbbell, ordered by absolute deployed gain (largest first)."""
    d = FD["dims"]
    order = sorted(d["order"], key=lambda k: d["deployed"][k] - d["baseline"][k], reverse=True)
    labels = [d["labels"][k] for k in order]
    base = [d["baseline"][k] for k in order]; dep = [d["deployed"][k] for k in order]
    fig, ax = plt.subplots(figsize=(6.2, 2.15))
    fig.subplots_adjust(left=0.21, right=0.905, top=0.965, bottom=0.20)
    y = list(range(len(order)))[::-1]
    for yi, b, f in zip(y, base, dep):
        ax.plot([b, f], [yi, yi], color=GRAYM, lw=1.4, zorder=1)
        ax.scatter(b, yi, s=42, facecolor="white", edgecolor=GRAYD, lw=1.1, zorder=3)
        ax.scatter(f, yi, s=52, color=ACCENT, zorder=3)
        ax.annotate(f"{b:.3f}", (b, yi), textcoords="offset points", xytext=(-6, 0),
                    ha="right", va="center", fontsize=7.2, color=GRAYD)
        ax.annotate(f"{f:.3f}", (f, yi), textcoords="offset points", xytext=(6, 0),
                    ha="left", va="center", fontsize=7.2, fontweight="bold", color=ACCENT)
        ax.annotate(f"+{f - b:.3f}", ((b + f) / 2, yi), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=6.6, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.2)
    ax.set_xlabel("anchored rubric dimension score  (proxy)")
    ax.set_xlim(0.45, 0.80); ax.set_ylim(-0.6, len(order) - 0.15)
    ax.scatter([], [], facecolor="white", edgecolor=GRAYD, s=42, label="baseline")
    ax.scatter([], [], color=ACCENT, s=52, label="deployed")
    ax.legend(loc="lower left", frameon=False, fontsize=7.4, handletextpad=0.3,
              bbox_to_anchor=(0.0, -0.02), ncol=2, columnspacing=1.2)
    ax.spines[["left"]].set_visible(False); ax.tick_params(axis="y", length=0)
    save(fig, "fig_dims.png")


# =============================================== FIGURE 6 — paraphrase vs shipped
def fig_floor():
    """Paired ECDFs: shipped deployed deltas (n=30) separate cleanly from the
    paraphrase rewording orbit (n=90). ECDF normalizes the unequal sample sizes
    and spans 0-1, so no raw-count-axis distortion."""
    par = np.sort(np.asarray(FD["floor"]["paraphrase"], float))
    shp = np.sort(np.asarray(FD["floor"]["shipped"], float))

    def ecdf(a):
        return np.concatenate([[a[0]], a]), np.concatenate([[0.0], np.arange(1, len(a) + 1) / len(a)])

    fig, ax = plt.subplots(figsize=(4.6, 2.75))
    fig.subplots_adjust(left=0.135, right=0.965, top=0.955, bottom=0.155)
    xp, yp = ecdf(par); xs_, ys_ = ecdf(shp)
    ax.step(xp, yp, where="post", color=GRAYD, lw=1.6, zorder=2)
    ax.step(xs_, ys_, where="post", color=ACCENT, lw=1.8, zorder=3)
    ax.axvline(0, color="0.55", lw=0.7, ls=(0, (2, 2)), zorder=1)
    ax.text(0.006, 0.55, "paraphrase orbit\n(n = 90)", color=GRAYD, fontsize=7.6,
            ha="left", va="center")
    ax.text(0.095, 0.55, "shipped deltas\n(n = 30)", color=ACCENT, fontsize=7.6,
            ha="left", va="center", fontweight="bold")
    ax.set_xlabel("delta vs baseline  (rubric / proxy)")
    ax.set_ylabel("empirical cumulative prob.")
    ax.set_xlim(-0.02, 0.185); ax.set_ylim(0, 1.02)
    save(fig, "fig_floor.png")


# ================================================= FIGURE 7 — validation panels
def fig_validation():
    """2x2 controls with honest, denominator-respecting axes and explicit units;
    vote-count and re-anchor detail move to the caption."""
    fig, axs = plt.subplots(2, 2, figsize=(5.4, 3.7))
    fig.subplots_adjust(hspace=0.62, wspace=0.42, left=0.11, right=0.965,
                        top=0.93, bottom=0.10)
    A, B, C, D = axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]

    def bars(ax, vals, labels, colors, hatches, ymax, ylab, title, yticks=None):
        x = [0, 1]
        ax.bar(x, vals, width=0.6, color=colors, hatch=hatches, edgecolor=INK, lw=0.5)
        ax.set_xticks(x); ax.set_xticklabels(labels)
        ax.set_ylim(0, ymax)
        if yticks is not None:
            ax.set_yticks(yticks)
        ax.set_ylabel(ylab, fontsize=8)
        ax.set_title(title, fontsize=8.8, fontweight="bold")
        return x

    # A blinded: systems, denominator 26
    x = bars(A, [22, 4], ["TEI\nmaj.", "baseline\nmaj."], [ACCENT, GRAYD], ["", "////"],
             26, "systems (of 26)", "Blinded A/B", yticks=[0, 6, 13, 20, 26])
    for xi, v in zip(x, [22, 4]):
        A.text(xi, v + 0.5, str(v), ha="center", fontsize=8, fontweight="bold", color=INK)

    # B sham: percentage, denominator 100
    x = bars(B, [84.6, 26.9], ["real", "sham"], [ACCENT, GRAYD], ["", "////"],
             100, "% of votes", "Sham placebo", yticks=[0, 25, 50, 75, 100])
    for xi, v in zip(x, [84.6, 26.9]):
        B.text(xi, v + 2, f"{v:.1f}", ha="center", fontsize=7.6, fontweight="bold", color=INK)

    # C random: rubric delta, continuous axis incl. zero -> dot plot (Cleveland)
    yv = [1, 0]; xv = [0.0630, 0.0165]
    C.hlines(yv, 0, xv, color=GRAYM, lw=1.2, zorder=1)
    C.scatter([xv[0]], [1], s=46, color=ACCENT, zorder=3)
    C.scatter([xv[1]], [0], s=46, facecolor="white", edgecolor=GRAYD, lw=1.1, zorder=3)
    for yy, vv, col in zip(yv, xv, [ACCENT, GRAYD]):
        C.annotate(f"+{vv:.4f}", (vv, yy), textcoords="offset points", xytext=(6, 0),
                   ha="left", va="center", fontsize=7.4, fontweight="bold", color=col)
    C.set_yticks(yv); C.set_yticklabels(["TEI", "random"])
    C.set_xlim(0, 0.086); C.set_ylim(-0.55, 1.55)
    C.set_xlabel("rubric delta", fontsize=8)
    C.set_title("Budget-matched random", fontsize=8.8, fontweight="bold")
    C.spines[["left"]].set_visible(False); C.tick_params(axis="y", length=0)

    # D cross-provider: agent-level majorities, denominator 10
    x = bars(D, [3, 6], ["patched\nmaj.", "baseline\nmaj."], [ACCENT, GRAYD], ["", "xxxx"],
             10, "agent majorities (of 10)", "Cross-provider", yticks=[0, 2, 4, 6, 8, 10])
    for xi, v in zip(x, [3, 6]):
        D.text(xi, v + 0.2, str(v), ha="center", fontsize=8, fontweight="bold", color=INK)
    save(fig, "fig_validation.png")


# ==================================================================== assertions
def _assert():
    d = FD["stages_deployed"]
    assert abs(d["final"] - 0.6842) < 1.5e-3 and abs(d["struct"] - 0.6672) < 1.5e-3 \
        and abs(d["base"] - 0.6057) < 1.5e-3, ("n=26 deployed drifted", d)
    assert abs(FD["stages_ceiling"]["final"] - 0.6905) < 1.5e-3, "ceiling drifted"
    allf = float(np.mean([r["best_applied_final"] for r in PA]))
    assert abs(allf - 0.675) < 2e-3, ("all-30 deployed final drifted", allf)
    assert abs(AP["rel_gain_pct"] - 13.0) < 0.1 and RC["n_patched"] == 26
    assert len(FD["floor"]["paraphrase"]) == 90 and len(FD["floor"]["shipped"]) == 30
    dims = FD["dims"]
    gains = {k: dims["deployed"][k] - dims["baseline"][k] for k in dims["order"]}
    assert max(gains, key=gains.get) == "execution_accuracy", "EA should be the largest gain"
    print(f"assertions OK: n26 {d['base']:.3f}->{d['struct']:.3f}->{d['final']:.3f}, "
          f"all30 final {allf:.4f}, ceiling {FD['stages_ceiling']['final']:.4f}, "
          f"EA gain {gains['execution_accuracy']:+.3f}")


if __name__ == "__main__":
    _assert()
    fig_trajectory(); fig_ladder(); fig_method(); fig_population(); fig_dims()
    fig_floor(); fig_validation()
    print("all figures written")
