#!/usr/bin/env python3
"""Phase B pre-committed reporting (BUDGET_100.md): per-agent best-score-vs-
iteration curves for both phases, published whatever they show, plus the
5-agent BCL-on vs BCL-off ablation comparison over the matched +30/+30 window
with the preregistered summary statistics (per-iteration mean best-so-far
difference, end-of-window delta, exact paired sign test at window end).

Outputs:
  curves_data.json                 - all trajectories + ablation stats (number source)
  paper/figures/curves_grid.png    - 30-agent grid, best-so-far vs iteration
  paper/figures/ablation_curves.png- 5 agents x 2 arms, matched extension window
"""
import glob
import json
import math
import os

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
ABLATION = os.path.join(ROOT, "ablation")
ABLATION_AGENTS = ["01_livesweagent", "04_acoder", "09_agentscope", "21_swerl", "24_swefixer"]


def load(tei_dir):
    p = os.path.join(tei_dir, "candidates.jsonl")
    recs = []
    if os.path.isfile(p):
        for line in open(p):
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def best_so_far(recs, phase, baseline):
    xs, ys = [], []
    best = baseline
    seq = [r for r in recs if r.get("phase") == phase and r.get("aggregate") is not None]
    for i, r in enumerate(seq, 1):
        best = max(best, r["aggregate"])
        xs.append(i)
        ys.append(round(best, 4))
    return xs, ys


def trajectories(agent_root, dirs):
    out = {}
    for d in dirs:
        tei = os.path.join(agent_root, d, "tei")
        bp = os.path.join(tei, "baseline_eval.json")
        if not os.path.isfile(bp):
            continue
        base = json.load(open(bp))["aggregate"]
        recs = load(tei)
        sx, sy = best_so_far(recs, "structural", base)
        px, py = best_so_far(recs, "prompt", base)
        # prefix boundary: where the original run ended (arm field absent)
        pre_s = sum(1 for r in recs if r.get("phase") == "structural" and "arm" not in r)
        pre_p = sum(1 for r in recs if r.get("phase") == "prompt" and "arm" not in r)
        out[d] = {"baseline": base, "structural": sy, "prompt": py,
                  "prefix_structural": pre_s, "prefix_prompt": pre_p,
                  "n_versions": len([r for r in recs if r.get("aggregate") is not None])}
    return out


def sign_test_two_sided(wins, losses):
    """Exact two-sided sign test p-value over discordant pairs."""
    n = wins + losses
    if n == 0:
        return 1.0
    def binom(k):
        return math.comb(n, k) / 2 ** n
    k = min(wins, losses)
    p = sum(binom(i) for i in range(0, k + 1)) * 2
    return min(1.0, round(p, 4))


def ablation_stats(main, abl):
    """Preregistered comparison over matched +30/+30 extension offsets."""
    per_agent, diffs_by_offset = {}, {}
    wins = losses = 0
    for d in ABLATION_AGENTS:
        m, a = main.get(d), abl.get(d)
        if not m or not a:
            continue
        rows = {}
        for phase in ("structural", "prompt"):
            pre = m[f"prefix_{phase}"]
            on = m[phase][pre:pre + 30]     # BCL arm: first 30 extension iterations
            off = a[phase][pre:pre + 30]    # ablation arm: its 30 iterations past the same prefix
            k = min(len(on), len(off))
            rows[phase] = {"bcl_on": on[:k], "bcl_off": off[:k], "n": k}
            for i in range(k):
                diffs_by_offset.setdefault(i, []).append(on[i] - off[i])
        end_on = max([rows[p]["bcl_on"][-1] for p in rows if rows[p]["bcl_on"]] or [m["baseline"]])
        end_off = max([rows[p]["bcl_off"][-1] for p in rows if rows[p]["bcl_off"]] or [m["baseline"]])
        rows["end_of_window_best"] = {"bcl_on": end_on, "bcl_off": end_off,
                                      "delta": round(end_on - end_off, 4)}
        if end_on > end_off:
            wins += 1
        elif end_off > end_on:
            losses += 1
        per_agent[d] = rows
    mean_diff = {str(i): round(sum(v) / len(v), 5) for i, v in sorted(diffs_by_offset.items())}
    return {"per_agent": per_agent,
            "per_iteration_mean_best_so_far_difference": mean_diff,
            "end_of_window": {"bcl_wins": wins, "bcl_losses": losses,
                              "ties": len(per_agent) - wins - losses,
                              "exact_sign_test_p": sign_test_two_sided(wins, losses)}}


def main():
    dirs = sorted(d for d in os.listdir(AGENTS) if os.path.isdir(os.path.join(AGENTS, d)))
    main_traj = trajectories(AGENTS, dirs)
    abl_traj = trajectories(ABLATION, ABLATION_AGENTS) if os.path.isdir(ABLATION) else {}
    data = {"main": main_traj, "ablation": abl_traj,
            "ablation_comparison": ablation_stats(main_traj, abl_traj)}
    json.dump(data, open(os.path.join(ROOT, "curves_data.json"), "w"), indent=1)
    print(f"curves_data.json: {len(main_traj)} agents, {len(abl_traj)} ablation arms")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib unavailable; JSON written, figures skipped")
        return

    fig, axes = plt.subplots(6, 5, figsize=(16, 15), sharex=False)
    for ax, d in zip(axes.flat, dirs):
        t = main_traj.get(d)
        if not t:
            ax.axis("off")
            continue
        ax.plot(range(1, len(t["structural"]) + 1), t["structural"], lw=1.2,
                color="#1f77b4", label="structural")
        ax.plot(range(1, len(t["prompt"]) + 1), t["prompt"], lw=1.2,
                color="#d62728", label="prompt")
        ax.axhline(t["baseline"], color="gray", lw=0.7, ls=":")
        ax.axvline(t["prefix_structural"] + 0.5, color="#1f77b4", lw=0.6, ls="--", alpha=0.5)
        ax.axvline(t["prefix_prompt"] + 0.5, color="#d62728", lw=0.6, ls="--", alpha=0.5)
        ax.set_title(d, fontsize=7)
        ax.tick_params(labelsize=6)
    axes.flat[0].legend(fontsize=6)
    fig.suptitle("Best-so-far TEI aggregate vs iteration (PROXY substrate; dashed = prefix boundary)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    out1 = os.path.join(ROOT, "paper", "figures", "curves_grid.png")
    fig.savefig(out1, dpi=160)
    print("wrote", out1)

    if abl_traj:
        fig2, axes2 = plt.subplots(2, 5, figsize=(16, 6))
        comp = data["ablation_comparison"]["per_agent"]
        for col, d in enumerate(ABLATION_AGENTS):
            rows = comp.get(d, {})
            for row, phase in enumerate(("structural", "prompt")):
                ax = axes2[row][col]
                r = rows.get(phase)
                if not r:
                    ax.axis("off")
                    continue
                ax.plot(range(1, r["n"] + 1), r["bcl_on"], lw=1.4, color="#2ca02c", label="BCL on")
                ax.plot(range(1, r["n"] + 1), r["bcl_off"], lw=1.4, color="#7f7f7f", label="BCL off")
                if row == 0:
                    ax.set_title(d, fontsize=8)
                if col == 0:
                    ax.set_ylabel(f"{phase}\nbest-so-far", fontsize=7)
                ax.tick_params(labelsize=6)
        axes2[0][0].legend(fontsize=7)
        fig2.suptitle("Mini-ablation (preregistered): BCL-on vs BCL-off, matched +30/+30 window",
                      fontsize=11)
        fig2.tight_layout(rect=[0, 0, 1, 0.95])
        out2 = os.path.join(ROOT, "paper", "figures", "ablation_curves.png")
        fig2.savefig(out2, dpi=160)
        print("wrote", out2)


if __name__ == "__main__":
    main()
