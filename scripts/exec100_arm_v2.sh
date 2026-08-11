#!/bin/zsh
# Phase C funded execution arm, v2 — per prereg-exec2 + amendment prereg-exec2-amend1.
# Changes vs v1 (both preregistered in the amendment): identical
# completion_kwargs {"reasoning_effort":"none"} in BOTH arms; round cleanup
# clears error-stub dirs (not just traj-less); progress via the genuine-rollout
# ledger, never file existence.
set -x
cd ~/swebench-agents
source ~/.config/tei/openai.env
export OPENAI_API_KEY
source _venv_a1/bin/activate
IDS=$(python -c "import json;print('|'.join(json.load(open('_exec100_instances.json'))))")

for ARM in patched baseline; do
  if [ "$ARM" = "baseline" ]; then SRC=_sweagent_base; else SRC=agents/08_sweagent; fi
  for ROUND in 1 2 3 4 5 6; do
    python3 exec100_ledger.py
    G=$(python3 - <<PY
import glob, json, os, sys
sys.path.insert(0, os.path.expanduser("~/swebench-agents"))
from exec100_ledger import classify
n = 0
for tp in glob.glob("_exec100_${ARM}/*/*.traj"):
    if classify(tp)[0] == "genuine":
        n += 1
print(n)
PY
)
    [ "$G" = "100" ] && break
    python3 exec100_ledger.py --clean-stubs _exec100_${ARM}
    docker ps -q | xargs -r docker rm -f
    docker images --format '{{.ID}} {{.Repository}}' | grep 'sweb' | awk '{print $1}' | xargs -r docker rmi -f 2>&1 | tail -1
    pip -q install -e $SRC 2>&1 | tail -1
    sweagent run-batch \
      --instances.type swe_bench --instances.subset verified --instances.split test \
      --instances.filter "$IDS" \
      --agent.model.name gpt-5.6-luna --agent.model.per_instance_cost_limit 3.00 \
      --agent.model.completion_kwargs '{"reasoning_effort": "none"}' \
      --output_dir _exec100_${ARM} --num_workers 3 2>&1 | tail -4
  done
  echo "ARM-${ARM}-ROLLOUTS-DONE"
  python3 exec100_ledger.py
done

# official harness scoring with per-arm cache discipline (keeps VM disk low)
for ARM in patched baseline; do
  docker ps -q | xargs -r docker rm -f
  docker images --format '{{.ID}} {{.Repository}}' | grep 'sweb' | awk '{print $1}' | xargs -r docker rmi -f 2>&1 | tail -1
  python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Verified \
    --predictions_path _exec100_${ARM}/preds.json \
    --cache_level none \
    --max_workers 2 --run_id exec100_${ARM} 2>&1 | tail -5 || echo "WALL: eval ${ARM}"
done
python3 exec100_ledger.py
echo "=== EXEC100-V2-COMPLETE ==="
