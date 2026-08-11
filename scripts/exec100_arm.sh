#!/bin/zsh
# Phase C funded execution arm — exactly as preregistered (tag prereg-exec2).
set -x
cd ~/swebench-agents
source ~/.config/tei/openai.env
export OPENAI_API_KEY
source _venv_a1/bin/activate
IDS=$(python -c "import json;print('|'.join(json.load(open('_exec100_instances.json'))))")

for ARM in patched baseline; do
  if [ "$ARM" = "baseline" ]; then SRC=_sweagent_base; else SRC=agents/08_sweagent; fi
  for ROUND in 1 2 3 4 5 6; do
    N=$(python -c "import json;print(len(json.load(open('_exec100_${ARM}/preds.json'))))" 2>/dev/null || echo 0)
    [ "$N" = "100" ] && break
    # clear traj-less instance dirs so they re-run; prune docker to free disk
    python - <<PY
import glob, shutil
for d in glob.glob('_exec100_${ARM}/*/'):
    if not glob.glob(d + '*.traj'):
        shutil.rmtree(d)
PY
    docker ps -q | xargs -r docker rm -f
    docker images --format '{{.ID}} {{.Repository}}' | grep 'sweb' | awk '{print $1}' | xargs -r docker rmi -f 2>&1 | tail -1
    pip -q install -e $SRC 2>&1 | tail -1
    sweagent run-batch \
      --instances.type swe_bench --instances.subset verified --instances.split test \
      --instances.filter "$IDS" \
      --agent.model.name gpt-5.6-luna --agent.model.per_instance_cost_limit 3.00 \
      --output_dir _exec100_${ARM} --num_workers 3 2>&1 | tail -4
  done
  echo "ARM-${ARM}-ROLLOUTS-DONE: $(python -c "import json;print(len(json.load(open('_exec100_${ARM}/preds.json'))))" 2>/dev/null || echo 0)/100"
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
echo "=== EXEC100-COMPLETE ==="
