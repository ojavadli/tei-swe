#!/usr/bin/env python3
"""Post-rollout classification + atomic promotion for sidecar workers.

If the rollout is GENUINE (preregistered criterion: api_calls >= 1 and nonzero
tokens both directions), move its instance dir into the canonical arm
directory — never overwriting existing genuine work. Otherwise archive the
attempt under _exec100_sidecar_failed/ for the retry queue.
"""
import glob
import os
import shutil
import sys

sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from exec100_ledger import classify  # noqa: E402

out, instance, arm = sys.argv[1], sys.argv[2], sys.argv[3]
src = os.path.join(out, instance)
trajs = glob.glob(os.path.join(src, "*.traj"))
kind = classify(trajs[0])[0] if trajs else "missing"
if kind == "genuine":
    dst = os.path.join(f"_exec100_{arm}", instance)
    if os.path.isdir(dst):
        dtr = glob.glob(os.path.join(dst, "*.traj"))
        if dtr and classify(dtr[0])[0] == "genuine":
            print("ALREADY_GENUINE")      # never overwrite genuine work
            raise SystemExit
        shutil.rmtree(dst)
    os.makedirs(f"_exec100_{arm}", exist_ok=True)
    shutil.move(src, dst)
    print("GENUINE")
else:
    os.makedirs("_exec100_sidecar_failed", exist_ok=True)
    tag = os.path.join("_exec100_sidecar_failed", os.path.basename(out))
    shutil.rmtree(tag, ignore_errors=True)
    shutil.move(out, tag)
    print(f"NOT_GENUINE:{kind}")
