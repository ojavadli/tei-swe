#!/usr/bin/env python3
"""Post-pass over completed agents.

1. Recompute the paraphrase noise floor with the corrected, baseline-anchored
   prompt (the first version elicited scores on a different scale, which made the
   floor meaningless).
2. Add the two honesty flags the methodology's own diagnostics imply:
   - gain_vs_noise_floor : exceeds_noise_floor | within_noise_floor
   - below_mde           : is the shipped delta smaller than the power preflight's
                           minimum detectable effect for this n?
"""
import json
import os
import sys

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
import tei_pipeline as T  # noqa: E402

AGENTS = T.AGENTS


def main():
    updated = 0
    for d in sorted(os.listdir(AGENTS)):
        tei = os.path.join(AGENTS, d, "tei")
        rp = os.path.join(tei, "result.json")
        if not os.path.isfile(rp):
            continue
        res = json.load(open(rp))
        base = json.load(open(os.path.join(tei, "baseline_eval.json")))
        ob = json.load(open(os.path.join(tei, "onboarding.json")))
        probes = base.get("probes") or []

        nf = T.noise_floor(ob, base, probes, os.path.join(AGENTS, d))
        res["noise_floor"] = nf
        res["noise_floor_method"] = ("baseline-anchored orbit; identical calibration to "
                                     "candidate scoring")

        delta = round((res.get("best_final") or 0) - (res.get("baseline") or 0), 4)
        floor = (nf or {}).get("noise_floor")
        res["shipped_delta"] = delta
        res["gain_vs_noise_floor"] = (
            "no_floor_measured" if floor is None else
            "exceeds_noise_floor" if delta > floor else "within_noise_floor")

        mde = (res.get("confirmation") or {}).get("mde")
        res["below_mde"] = None if mde is None else bool(delta < mde)
        res["mde_note"] = (
            None if mde is None else
            f"shipped delta {delta} vs MDE {mde} at n={res['confirmation'].get('n_queries')}: "
            + ("BELOW the minimum detectable effect - not statistically meaningful at this n"
               if delta < mde else "at or above the MDE"))

        json.dump(res, open(rp, "w"), indent=2)
        updated += 1
        print(f"{d:30s} delta={delta:+.4f} floor={floor} -> {res['gain_vs_noise_floor']:20s} "
              f"below_mde={res['below_mde']}", flush=True)
    print(f"\nupdated {updated} agents | budget this pass: {json.dumps(T.BUDGET.as_dict())}")
    return T.BUDGET.as_dict()


if __name__ == "__main__":
    b = main()
    p = os.path.join(T.ROOT, "_post_pass_budget.json")
    json.dump(b, open(p, "w"), indent=2)
