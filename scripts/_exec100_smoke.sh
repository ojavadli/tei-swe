#!/bin/zsh
set -x
cd ~/swebench-agents
source ~/.config/tei/openai.env
export OPENAI_API_KEY
source _venv_a1/bin/activate
pip -q install -e agents/08_sweagent 2>&1 | tail -1
sweagent run-batch \
  --instances.type swe_bench --instances.subset verified --instances.split test \
  --instances.filter "astropy__astropy-14096" \
  --agent.model.name gpt-5.6-luna --agent.model.per_instance_cost_limit 3.00 \
  --agent.model.completion_kwargs '{"reasoning_effort": "none"}' \
  --output_dir _exec100_smoke --num_workers 1 2>&1 | tail -6
echo "=== SMOKE-RUN-DONE ==="
