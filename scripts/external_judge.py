#!/usr/bin/env python3
"""P3: external non-OpenAI judge (Anthropic claude-sonnet-5), JUDGING ONLY.
Owner-authorized for <=$3 Anthropic spend via the revision mission.

Passes (all blinded, identical protocol, fresh seed 11):
  ext_blind : 10-agent fixed subsample (same as terra's), real tei-v7 diffs
  ext_sham  : same 10 agents, sham-v1 diffs (placebo cross-check)
  ext_repair: the 5 repaired agents, fresh-seed independent confirmation

Meters Anthropic tokens; prices at list ($3/$15 per Mtok for sonnet-5 assumed
accounting; recorded per call).
"""
import json
import os
import random
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
import blind_reval as BR

ROOT = os.path.expanduser("~/swebench-agents")
AGENTS = os.path.join(ROOT, "agents")
MODEL = "claude-sonnet-5"
K = 5
rng = random.Random(11)
USAGE = {"calls": 0, "in": 0, "out": 0}


def akey():
    return json.load(open(os.path.expanduser(
        "~/.claude/settings.json")))["env"]["ANTHROPIC_API_KEY"]


def call_claude(prompt, max_tokens=900, retries=4):
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = None
    for a in range(retries):
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages", data=body,
            headers={"x-api-key": akey(), "anthropic-version": "2023-06-01",
                     "content-type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.loads(r.read())
            USAGE["calls"] += 1
            USAGE["in"] += d.get("usage", {}).get("input_tokens", 0)
            USAGE["out"] += d.get("usage", {}).get("output_tokens", 0)
            txt = "".join(b.get("text", "") for b in d.get("content", []))
            if txt.strip():
                return txt
            last = "empty"
        except Exception as e:
            last = str(e)[:120]
        time.sleep(2 * (a + 1))
    raise RuntimeError(f"claude call failed: {last}")


def parse_json(txt):
    import re
    t = re.sub(r"^```(?:json)?|```$", "", txt.strip(), flags=re.M).strip()
    m = re.search(r"\{.*\}", t, re.S)
    return json.loads(m.group(0) if m else t)


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def blinded_votes(repo, ob, ref_new, probes, label_new):
    """k=5 blinded A/B of base vs ref_new using diff excerpts base..ref_new."""
    base_sha = ob["repo_sha"]
    num = sh(["git", "diff", "--numstat", f"{base_sha}..{ref_new}"], repo).stdout
    rows = sorted((int(a) + int(b), p) for a, b, p in
                  (l.split("\t") for l in num.splitlines() if len(l.split("\t")) == 3)
                  if a.isdigit())
    files = [p for _, p in rows[:4]]
    pairs = []
    for p in files:
        diff = sh(["git", "diff", "-U12", f"{base_sha}..{ref_new}", "--", p], repo).stdout
        if not diff:
            continue
        bef, aft = [], []
        for line in diff.splitlines():
            if line.startswith(("---", "+++", "diff ", "index ", "@@")):
                if line.startswith("@@"):
                    bef.append("  [...]"); aft.append("  [...]")
                continue
            if line.startswith("-"):
                bef.append(line[1:])
            elif line.startswith("+"):
                aft.append(line[1:])
            else:
                bef.append(line[1:] if line else line)
                aft.append(line[1:] if line else line)
        pairs.append((p, "\n".join(bef)[:2600], "\n".join(aft)[:2600]))
    votes = []
    for k in range(K):
        flip = rng.random() < 0.5
        blocks = [f"### file: {path}\n--- VERSION 1 ---\n{(aft if flip else bef)}\n"
                  f"--- VERSION 2 ---\n{(bef if flip else aft)}"
                  for path, bef, aft in pairs]
        prompt = f"""You are comparing two versions of the same software-engineering agent system
({ob['system']}; its job: resolve real GitHub issues, SWE-bench style). Below, for each shown file,
are the two versions' contents in the regions where they differ. You are NOT told which version is
older; judge only what you see.

Representative task instances this agent faces: {', '.join(probes)}.

{chr(10).join(blocks)}

Which version is more likely to resolve such issues correctly end-to-end? If too trivial or
ambiguous to matter, say tie.

Return ONLY JSON: {{"better": "1" | "2" | "tie", "confidence": 0.0, "reason": "one sentence"}}"""
        try:
            v = parse_json(call_claude(prompt))
        except Exception as e:
            votes.append({"error": str(e)[:60]}); continue
        pick = str(v.get("better", "")).strip()
        votes.append({"vote": (label_new if pick == ("1" if flip else "2") else
                               "baseline" if pick in ("1", "2") else "tie"),
                      "reason": str(v.get("reason", ""))[:140]})
    return votes


def run_set(agent_dirs, ref_new, label_new):
    out = []
    for d in agent_dirs:
        repo = os.path.join(AGENTS, d)
        ob = json.load(open(os.path.join(repo, "tei", "onboarding.json")))
        probes = [p["instance_id"] for p in json.load(
            open(os.path.join(repo, "tei", "baseline_eval.json"))).get("probes", [])][:4]
        # verify ref exists
        if sh(["git", "rev-parse", "--verify", ref_new], repo).returncode != 0:
            out.append({"agent": d, "skipped": f"no ref {ref_new}"}); continue
        votes = blinded_votes(repo, ob, ref_new, probes, label_new)
        pv = sum(1 for v in votes if v.get("vote") == label_new)
        bv = sum(1 for v in votes if v.get("vote") == "baseline")
        out.append({"agent": d, label_new: pv, "baseline": bv,
                    "tie": len(votes) - pv - bv, "votes": votes})
        cost = USAGE["in"] / 1e6 * 3 + USAGE["out"] / 1e6 * 15
        print(f"  ext[{label_new}] {d:28s} {pv}/{bv}  [${cost:.2f} anthropic]", flush=True)
        if cost > 2.90:
            print("  !! approaching $3 Anthropic cap; stopping this set")
            break
    return out


def main():
    ten = ['05_joycode', '06_lingxi', '07_moatlesstools', '09_agentscope',
           '11_experepair', '15_composioswekit', '18_codefusecgm',
           '19_agentlesslite', '22_orcaloca', '24_swefixer']  # = terra subsample
    repaired = ['05_joycode', '07_moatlesstools', '20_sweexp', '22_orcaloca', '27_agentless']
    res = {"model": MODEL, "seed": 11}
    print("=== ext_blind (real patches) ===", flush=True)
    res["ext_blind"] = run_set(ten, "tei-v7", "patched")
    print("=== ext_sham (placebo) ===", flush=True)
    res["ext_sham"] = run_set(ten, "sham-v1", "sham")
    print("=== ext_repair (fresh-seed independent confirmation) ===", flush=True)
    res["ext_repair"] = run_set(repaired, "tei-v7", "patched")
    res["usage"] = dict(USAGE, cost_usd=round(USAGE["in"] / 1e6 * 3 + USAGE["out"] / 1e6 * 15, 3))
    json.dump(res, open(os.path.join(ROOT, "external_judge.json"), "w"), indent=1)
    for k in ("ext_blind", "ext_sham", "ext_repair"):
        rows = [r for r in res[k] if "votes" in r]
        lab = "patched" if k != "ext_sham" else "sham"
        maj = sum(1 for r in rows if r[lab] > r["baseline"] + r["tie"])
        print(f"{k}: majority-{lab} {maj}/{len(rows)}, votes "
              f"{sum(r[lab] for r in rows)}/{sum(r[lab]+r['baseline']+r['tie'] for r in rows)}")
    print("anthropic usage:", res["usage"])


if __name__ == "__main__":
    main()
