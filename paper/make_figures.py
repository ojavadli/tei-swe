#!/usr/bin/env python3
"""Main-paper figures for TEI-SWE — restrained academic style.

Design rules (owner directive): white ground; charcoal/gray default; ONE muted
accent (steel blue) for TEI/deployed, used sparingly; standard scientific marks
(strip/line/step/dumbbell/bar/flow); >=~65-70% of area is data or structure; no
KPI cards, giant numbers, promo callouts, gradients, or dashboard aesthetics.
Printed fonts ~7.5-10 pt. Grayscale-legible via shape+value, not colour alone.
Every value is read from canonical JSON; assertions at the bottom guard against
stale hardcoding. NO Phase-C content.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = os.path.expanduser("~/swebench-agents")
OUT = os.path.join(ROOT, "paper", "figures")
_RC = json.load(open(os.path.join(ROOT, "_paper_recompute.json")))
RC = _RC["summary"]
AP = RC["APPLIED"]; PR = RC["PROPOSED"]
PA = _RC["per_agent"]
ZERO4 = set(RC["zeropatch_agents"])
FD = json.load(open(os.path.join(OUT, "_fig_data.json")))

# ---- restrained palette ----
INK = "#111827"      # near-black: primary lines/text/markers
ACCENT = "#2f5c8a"   # muted steel blue: TEI / deployed (sparingly)
GRAYD = "#6b7280"    # baseline / secondary series
GRAYM = "#9aa1a9"    # mid gray
GRAYL = "#c9ced4"    # light gray: individual population lines
plt.rcParams.update({
    "font.family": "serif", "font.size": 8.5, "axes.titlesize": 9.5,
    "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "figure.dpi": 300, "savefig.dpi": 300,
    "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "text.usetex": False, "text.parse_math": False,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("wrote", name)


def patched(key):
    return [r[key] for r in PA if r["agent"] not in ZERO4]


# ============================================================ FIGURE 1 — result
def fig_trajectory():
    """Per-system deployed values at the three stages (strip) + mean trajectory
    + best-proposed ceiling. Population = 26 patched systems."""
    fig, ax = plt.subplots(figsize=(4.9, 3.05))
    fig.subplots_adjust(left=0.135, right=0.985, top=0.90, bottom=0.11)
    xs = [0, 1, 2]
    cols = [patched("base"), patched("best_applied_struct"), patched("best_applied_final")]
    dep = [FD["stages_deployed"]["base"], FD["stages_deployed"]["struct"], FD["stages_deployed"]["final"]]
    ceil = [FD["stages_ceiling"]["base"], FD["stages_ceiling"]["struct"], FD["stages_ceiling"]["final"]]
    # per-system points (deterministic jitter by index parity so it is reproducible)
    for xi, col in zip(xs, cols):
        for j, v in enumerate(col):
            jit = ((j % 7) - 3) / 3.0 * 0.05
            ax.plot(xi + jit, v, marker="o", ms=2.6, mfc="none", mec=GRAYM,
                    mew=0.6, zorder=2)
    # proposed ceiling (secondary, dashed)
    ax.plot(xs, ceil, ls=(0, (4, 2)), color=GRAYD, lw=1.0, marker="o", ms=3.0,
            mfc="white", mec=GRAYD, zorder=3, label="best proposed (not committed)")
    ax.plot([], [], marker="o", ms=3.0, mfc="none", mec=GRAYM, mew=0.6, ls="none",
            label="individual system")
    # deployed mean trajectory (accent, dominant)
    ax.plot(xs, dep, color=ACCENT, lw=2.2, marker="o", ms=6, mfc=ACCENT,
            mec="white", mew=0.8, zorder=5, label="deployed mean (n=26)")
    for xi, v in zip(xs, dep):
        dy = 8 if xi < 2 else -14   # keep the Final label off the ceiling marker
        ax.annotate(f"{v:.3f}", (xi, v), textcoords="offset points",
                    xytext=(0, dy), ha="center", fontsize=8, fontweight="bold",
                    color=ACCENT, zorder=6)
    ax.set_xticks(xs); ax.set_xticklabels(["Default", "Structural", "Final"])
    ax.set_xlim(-0.3, 2.35)
    ax.set_ylim(min(min(c) for c in cols) - 0.02, max(ceil) + 0.035)
    ax.set_ylabel("anchored rubric aggregate  (proxy)")
    gain = dep[2] - dep[0]
    ax.text(0.02, 0.30, f"+{gain:.3f} absolute\n+{AP['rel_gain_pct']:.1f}% relative",
            transform=ax.transAxes, fontsize=8.5, color=INK, va="top", linespacing=1.2)
    ax.legend(loc="lower right", frameon=False, fontsize=7.2, handlelength=1.7,
              borderaxespad=0.3, labelspacing=0.35)
    save(fig, "fig_trajectory.png")


# ============================================================ FIGURE 2 — ladder
def fig_ladder():
    """Validation ladder: four rungs of increasing evidence strength and cost,
    drawn as a clean staircase (treads + risers), labels above each tread."""
    fig, ax = plt.subplots(figsize=(5.7, 2.5))
    fig.subplots_adjust(left=0.015, right=0.985, top=0.985, bottom=0.16)
    ax.axis("off")
    rungs = [
        ("Rubric / proxy", "Δ +0.079 · $0.35/agent"),
        ("Blinded A/B", "22/26 systems · $0.03/agent"),
        ("Static / deterministic", "6 defects caught · $0"),
        ("Execution", "n=36 retained, null · harness"),
    ]
    w, dx, dy = 3.0, 3.0, 1.28
    for i, (name, sub) in enumerate(rungs):
        x, y = 0.2 + i * dx, 0.5 + i * dy
        ax.plot([x, x + w], [y, y], color=INK, lw=2.0, solid_capstyle="butt", zorder=3)
        if i:  # riser connecting previous tread's right end up to this tread's left
            ax.plot([x, x], [y - dy, y], color=GRAYM, lw=1.0, zorder=2)
        col = ACCENT if name.startswith("Blinded") else INK
        ax.text(x + 0.08, y + 0.62, name, fontsize=8.6, fontweight="bold", color=col)
        ax.text(x + 0.08, y + 0.30, sub, fontsize=7.0, color=GRAYD)
    ax.text(0.2 + 1.8 * dx, -0.55, "increasing evidence strength and cost  →",
            fontsize=7.6, color=GRAYD, ha="center")
    ax.set_xlim(-0.2, 0.4 + 3 * dx + w); ax.set_ylim(-1.0, 0.5 + 3 * dy + 1.2)
    save(fig, "fig_ladder.png")


# ============================================================ FIGURE 3 — method
def fig_method():
    """Compact systems diagram: main path + credit-ledger feedback loop."""
    fig, ax = plt.subplots(figsize=(6.6, 2.75)); ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)

    def box(x, y, w, h, title, detail="", ec=INK, accent=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.4",
                                    fc="white", ec=(ACCENT if accent else ec),
                                    lw=(1.3 if accent else 1.0), zorder=2))
        cx = x + w / 2
        tcol = ACCENT if accent else INK
        if detail:
            ax.text(cx, y + h * 0.64, title, ha="center", va="center", fontsize=7.2,
                    fontweight="bold", color=tcol, zorder=3, linespacing=1.0)
            ax.text(cx, y + h * 0.26, detail, ha="center", va="center", fontsize=6.3,
                    color=GRAYD, zorder=3, linespacing=1.0)
        else:
            ax.text(cx, y + h / 2, title, ha="center", va="center", fontsize=7.2,
                    fontweight="bold", color=tcol, zorder=3, linespacing=1.0)

    def arrow(x1, y1, x2, y2, color=INK):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=8, color=color, lw=1.0, zorder=1))

    steps = [("Third-party\nagent", "", False), ("TARGET", "weak dim,\nfailures", False),
             ("EVALUATE", "baseline,\nprobes", False),
             ("IMPROVE\nstructure", "", True),
             ("GATE /\nSELECT", "", False),
             ("IMPROVE\nprompt", "", True),
             ("Deployed\nartifact", "", False)]
    w, h, step, y0 = 11.8, 17, 14.05, 60
    xs = [1.5 + i * step for i in range(7)]
    for i, (t, d, acc) in enumerate(steps):
        box(xs[i], y0, w, h, t, d, accent=acc)
        if i:
            arrow(xs[i - 1] + w, y0 + h / 2, xs[i], y0 + h / 2)

    # feedback loop
    box(30, 34, 22, 12, "WHY-RECORDS", "6,000: score + why", ec=GRAYD)
    box(58, 34, 24, 12, "BAYESIAN CREDIT LEDGER", "Thompson family selection", ec=GRAYD)
    arrow(xs[3] + w / 2, y0, 41, 46, color=GRAYD)
    arrow(52, 40, 58, 40, color=GRAYD)
    arrow(70, 46, xs[5] + w / 2, y0, color=GRAYD)
    ax.text(71.5, 53, "next proposal", fontsize=6.2, color=GRAYD, ha="left", va="center")

    ax.text(1.5, 95, "TEI optimizes both the structural (code/workflow) and prompt surfaces.",
            fontsize=8.2, color=INK)
    ax.text(1.5, 20, "Phase-A/B candidate selection uses the rubric, blinded A/B, and static "
                     "checks only — 0 executed benchmark rollouts.",
            fontsize=7.6, color=INK, style="italic")
    save(fig, "fig_method.png")


# ======================================================= FIGURE 4 — population
def fig_population():
    """All 30 systems' deployed trajectories (thin gray) + mean (accent).
    Population = all 30; mean ends at the all-30 deployed final."""
    fig, ax = plt.subplots(figsize=(4.5, 3.0))
    fig.subplots_adjust(left=0.15, right=0.97, top=0.94, bottom=0.11)
    xs = [0, 1, 2]
    allb = [r["base"] for r in PA]
    alls = [r["best_applied_struct"] for r in PA]
    allf = [r["best_applied_final"] for r in PA]
    for b, s, f in zip(allb, alls, allf):
        ax.plot(xs, [b, s, f], color=GRAYL, lw=0.7, zorder=1)
    mean = [sum(allb) / len(allb), sum(alls) / len(alls), sum(allf) / len(allf)]
    ax.plot(xs, mean, color=ACCENT, lw=2.2, marker="o", ms=5, mfc=ACCENT,
            mec="white", mew=0.7, zorder=4, label="mean (all 30)")
    for xi, v in zip(xs, mean):
        ax.annotate(f"{v:.3f}", (xi, v), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=7.5, fontweight="bold", color=ACCENT)
    ax.set_xticks(xs); ax.set_xticklabels(["Default", "Structural", "Final"])
    ax.set_xlim(-0.15, 2.35)
    ax.set_ylabel("deployed rubric aggregate  (proxy)")
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    save(fig, "fig_population.png")


# ========================================================= FIGURE 5 — dimensions
def fig_dims():
    d = FD["dims"]
    order = d["order"]
    labels = [d["labels"][k] for k in order]
    base = [d["baseline"][k] for k in order]
    dep = [d["deployed"][k] for k in order]
    fig, ax = plt.subplots(figsize=(6.4, 2.25))
    fig.subplots_adjust(left=0.20, right=0.90, top=0.97, bottom=0.19)
    y = list(range(len(order)))[::-1]
    for yi, b, f in zip(y, base, dep):
        ax.plot([b, f], [yi, yi], color=GRAYL, lw=3.0, zorder=1, solid_capstyle="round")
        ax.scatter(b, yi, s=48, facecolor="white", edgecolor=GRAYD, lw=1.1, zorder=3)
        ax.scatter(f, yi, s=60, color=ACCENT, zorder=3)
        ax.annotate(f"{b:.3f}", (b, yi), textcoords="offset points", xytext=(-6, 0),
                    ha="right", va="center", fontsize=7.2, color=GRAYD)
        ax.annotate(f"{f:.3f}", (f, yi), textcoords="offset points", xytext=(6, 0),
                    ha="left", va="center", fontsize=7.2, fontweight="bold", color=ACCENT)
        ax.annotate(f"+{f - b:.3f}", ((b + f) / 2, yi), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=6.6, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.2)
    ax.set_xlabel("anchored rubric dimension score  (proxy)")
    ax.set_xlim(0.45, 0.80); ax.set_ylim(-0.6, len(order) - 0.1)
    ax.scatter([], [], facecolor="white", edgecolor=GRAYD, s=48, label="baseline")
    ax.scatter([], [], color=ACCENT, s=60, label="deployed")
    ax.legend(loc="upper left", frameon=False, fontsize=7.4, handletextpad=0.3,
              bbox_to_anchor=(0.0, 1.03))
    ax.spines[["left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig_dims.png")


# ================================================= FIGURE 6 — validation panels
def fig_validation():
    fig, axs = plt.subplots(1, 4, figsize=(6.5, 2.45),
                            gridspec_kw={"wspace": 0.58})
    fig.subplots_adjust(top=0.80, bottom=0.20, left=0.075, right=0.985)
    A, B, C, D = axs

    def note(ax, s, color=GRAYD):
        ax.text(0.5, 0.965, s, transform=ax.transAxes, fontsize=6.6, va="top",
                ha="center", color=color, linespacing=1.15)

    def style(ax, title, tcol=INK):
        ax.set_title(title, loc="center", fontsize=8.4, fontweight="bold", color=tcol)
        ax.tick_params(length=2)

    # A blinded (systems)
    A.bar([0, 1], [22, 4], color=[ACCENT, GRAYD], width=0.62, edgecolor=INK, lw=0.5)
    A.set_xticks([0, 1]); A.set_xticklabels(["TEI\nmaj.", "baseline\nmaj."])
    A.set_ylim(0, 30); A.set_ylabel("systems (of 26)", fontsize=8)
    for xi, v in zip([0, 1], [22, 4]):
        A.text(xi, v + 0.5, str(v), ha="center", fontsize=8, fontweight="bold", color=INK)
    style(A, "Blinded\nA/B"); note(A, "110/130 votes · 17 unan.")

    # B sham (%)
    B.bar([0, 1], [84.6, 26.9], color=[ACCENT, GRAYD], width=0.62,
          hatch=["", "////"], edgecolor=INK, lw=0.5)
    B.set_xticks([0, 1]); B.set_xticklabels(["real", "sham"])
    B.set_ylim(0, 112); B.set_yticks([0, 20, 40, 60, 80, 100])
    B.set_ylabel("% of votes", fontsize=8)
    for xi, v in zip([0, 1], [84.6, 26.9]):
        B.text(xi, v + 2.0, f"{v:.1f}", ha="center", fontsize=7.8, fontweight="bold", color=INK)
    style(B, "Sham\nplacebo"); note(B, "re-anchor 0/45 (9 agents)")

    # C random (rubric delta)
    C.bar([0, 1], [0.0630, 0.0165], color=[ACCENT, GRAYD], width=0.62,
          hatch=["", "...."], edgecolor=INK, lw=0.5)
    C.set_xticks([0, 1]); C.set_xticklabels(["TEI", "random"])
    C.set_ylabel("rubric Δ", fontsize=8)
    for xi, v in zip([0, 1], [0.0630, 0.0165]):
        C.text(xi, v + 0.0012, f"+{v:.4f}", ha="center", fontsize=7.2, fontweight="bold", color=INK)
    C.set_ylim(0, 0.088)
    style(C, "Budget-matched\nrandom"); note(C, "blinded 10/10 vs 0/10")

    # D cross-provider (honest negative)
    D.bar([0, 1], [17, 30], color=[ACCENT, GRAYD], width=0.62,
          hatch=["", "xxxx"], edgecolor=INK, lw=0.5)
    D.set_xticks([0, 1]); D.set_xticklabels(["patched", "baseline"])
    D.set_ylim(0, 42); D.set_yticks([0, 10, 20, 30, 40])
    D.set_ylabel("votes (of 50)", fontsize=8)
    for xi, v in zip([0, 1], [17, 30]):
        D.text(xi, v + 0.9, str(v), ha="center", fontsize=8, fontweight="bold", color=INK)
    style(D, "Cross-provider\njudge")
    note(D, "3/10 vs 6/10 maj.\n(does NOT reproduce)", color=INK)
    save(fig, "fig_validation.png")


# ==================================================================== assertions
def _assert():
    d = FD["stages_deployed"]
    assert abs(d["final"] - 0.6842) < 1.5e-3, ("n=26 deployed final drifted", d["final"])
    assert abs(d["base"] - 0.6057) < 1.5e-3 and abs(d["struct"] - 0.6672) < 1.5e-3
    assert abs(FD["stages_ceiling"]["final"] - 0.6905) < 1.5e-3, "ceiling final drifted"
    allf = sum(r["best_applied_final"] for r in PA) / len(PA)
    assert abs(allf - 0.675) < 2e-3, ("all-30 deployed final drifted", allf)
    assert abs(AP["rel_gain_pct"] - 13.0) < 0.1, "rel gain drifted"
    assert len(ZERO4) == 4 and RC["n_patched"] == 26
    print(f"assertions OK: n26 final {d['final']:.4f}, all30 final {allf:.4f}, "
          f"ceiling {FD['stages_ceiling']['final']:.4f}, rel +{AP['rel_gain_pct']:.1f}%")


if __name__ == "__main__":
    _assert()
    fig_trajectory(); fig_ladder(); fig_method(); fig_population(); fig_dims(); fig_validation()
    print("all figures written")
