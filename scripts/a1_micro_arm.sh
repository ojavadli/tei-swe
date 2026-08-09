#!/bin/zsh
# A1 execution micro-arm, attempt 1: SWE-agent baseline vs tei-v7 on real instances.
# Stages logged; any stage failure exits with a precise wall description.
set -x
cd ~/swebench-agents
source ~/.config/tei/openai.env

VENV=~/swebench-agents/_venv_a1
[ -d $VENV ] || python3 -m venv $VENV
source $VENV/bin/activate
pip -q install --upgrade pip

echo "=== STAGE 1: install swebench harness ==="
pip -q install swebench 2>&1 | tail -2 || { echo "WALL: swebench pip install failed"; exit 2; }
python -c "import swebench; print('swebench', swebench.__version__)" || { echo "WALL: swebench import"; exit 2; }

echo "=== STAGE 2: install SWE-agent (patched tree) + baseline worktree ==="
cd agents/08_sweagent
git worktree add ../../_sweagent_base $(python3 -c "import json;print(json.load(open('tei/onboarding.json'))['repo_sha'])") 2>/dev/null || true
cd ~/swebench-agents
pip -q install -e agents/08_sweagent 2>&1 | tail -2 || { echo "WALL: sweagent install (patched) failed"; exit 3; }
sweagent --help >/dev/null 2>&1 || { echo "WALL: sweagent CLI missing"; exit 3; }

echo "=== STAGE 3: pick 6 fixed-seed instances this system attempted ==="
python - <<'EOF'
import json, random
ob=json.load(open('agents/08_sweagent/tei/onboarding.json'))
base=json.load(open('agents/08_sweagent/tei/baseline_eval.json'))
probes=[p['instance_id'] for p in base['probes']]
rng=random.Random(0)
res=[i for i in ob['resolved_instance_ids'] if i not in probes]
rng.shuffle(res)
ids=probes+res[:max(0,6-len(probes))]
json.dump(ids[:6], open('_a1_instances.json','w'))
print("instances:", ids[:6])
EOF

echo "=== STAGE 4: run patched SWE-agent on instances (gpt-4o-mini) ==="
sweagent run-batch \
  --instances.type swe_bench --instances.subset verified --instances.split test \
  --instances.filter "$(python -c "import json;print('|'.join(json.load(open('_a1_instances.json'))))")" \
  --agent.model.name gpt-4o-mini --agent.model.per_instance_cost_limit 0.30 \
  --output_dir _a1_patched 2>&1 | tail -15 || { echo "WALL: sweagent run-batch (patched) failed"; exit 4; }

echo "=== STAGE 5: run baseline SWE-agent ==="
pip -q install -e _sweagent_base 2>&1 | tail -1
sweagent run-batch \
  --instances.type swe_bench --instances.subset verified --instances.split test \
  --instances.filter "$(python -c "import json;print('|'.join(json.load(open('_a1_instances.json'))))")" \
  --agent.model.name gpt-4o-mini --agent.model.per_instance_cost_limit 0.30 \
  --output_dir _a1_baseline 2>&1 | tail -15 || { echo "WALL: sweagent run-batch (baseline) failed"; exit 5; }

echo "=== STAGE 6: evaluate both with the real harness ==="
for arm in patched baseline; do
  python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Verified \
    --predictions_path _a1_${arm}/preds.json \
    --max_workers 2 --run_id a1_${arm} 2>&1 | tail -8 || { echo "WALL: harness eval ($arm) failed"; exit 6; }
done
echo "=== A1 COMPLETE ==="
