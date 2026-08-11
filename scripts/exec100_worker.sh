#!/bin/zsh
# Sidecar rollout worker for Phase C (owner scale-out directive).
# Usage: exec100_worker.sh WID keyNN
# Scientifically identical to the validated smoke configuration: gpt-5.6-luna,
# completion_kwargs {"reasoning_effort":"none"}, $3.00 per-instance ceiling,
# same tools/config; only the preregistered baseline/patched artifact differs.
WID=$1
KEYFILE=$2
cd ~/swebench-agents
source ~/.config/tei/pool/${KEYFILE}.env

FAILSTREAK=0
while true; do
  JOB=$(python3 exec100_claim.py claim --worker "W$WID" --key "$KEYFILE" --pid $$ | tail -1)
  if [[ "$JOB" == "NONE" || -z "$JOB" ]]; then
    echo "W$WID: no pending work; exiting"
    break
  fi
  INSTANCE=${JOB%|*}
  ARM=${JOB#*|}
  if [ "$ARM" = "baseline" ]; then VENV=_venv_cb; else VENV=_venv_cp; fi
  IMG="swebench/sweb.eval.x86_64.$(echo $INSTANCE | sed 's/__/_1776_/'):latest"
  VERDICT="NOT_GENUINE:unset"
  # Up to 3 attempts per claim to ride through a concurrent `docker rmi sweb`
  # prune race (shared dockerd; the protected runner prunes at round bounds).
  for ATTEMPT in 1 2 3; do
    OUT="_exec100_sidecar/w${WID}_${ARM}_${INSTANCE}"
    rm -rf "$OUT" 2>/dev/null
    mkdir -p "$OUT"
    # GLOBAL PULL LOCK: concurrent pulls of images with shared base layers race
    # in containerd's content store ("failed commit on ref ... rename ... no such
    # file or directory"). Serialize the pull (the racy part, ~30-90s) with an
    # atomic mkdir spinlock; the rollout itself (minutes of agent work) stays
    # parallel. Once a layer is local it is cached, so races warm out.
    LOCK=/tmp/exec100_pull.lock
    if ! docker image inspect "$IMG" >/dev/null 2>&1; then
      WAIT=0
      while ! mkdir "$LOCK" 2>/dev/null; do
        sleep 3; WAIT=$((WAIT+3))
        # steal an abandoned lock (>10 min: a crashed holder)
        if [ $WAIT -gt 600 ]; then rm -rf "$LOCK" 2>/dev/null; fi
      done
      for P in 1 2 3; do docker pull -q "$IMG" >/dev/null 2>&1 && break; sleep 8; done
      rmdir "$LOCK" 2>/dev/null
    fi
    echo "W$WID $KEYFILE -> $INSTANCE ($ARM) attempt $ATTEMPT"
    # python_standalone_dir="" skips the per-instance from-source CPython compile
    # (swe-rex installs via pipx on the container's python instead). This is the
    # swerex command-relay shim's install method ONLY: swe-rex relays the agent's
    # bash commands during the rollout and is entirely absent when the SWE-bench
    # harness later scores the patch, so it is causally disconnected from resolve
    # outcomes. It collapses the ~10-min build (and its prune-race window) to
    # seconds, which is what makes fleet parallelism feasible on the 4-vCPU VM.
    $VENV/bin/python -m sweagent run-batch \
      --instances.type swe_bench --instances.subset verified --instances.split test \
      --instances.filter "$INSTANCE" \
      --agent.model.name gpt-5.6-luna --agent.model.per_instance_cost_limit 3.00 \
      --agent.model.completion_kwargs '{"reasoning_effort": "none"}' \
      --instances.deployment.python_standalone_dir="" \
      --output_dir "$OUT" --num_workers 1 > "$OUT/worker_run.log" 2>&1
    VERDICT=$(python3 exec100_finish_job.py "$OUT" "$INSTANCE" "$ARM" | tail -1)
    [[ "$VERDICT" == GENUINE* || "$VERDICT" == ALREADY_GENUINE ]] && break
    echo "W$WID $INSTANCE attempt $ATTEMPT: $VERDICT (retrying)"
    sleep 10
  done
  echo "W$WID $INSTANCE ($ARM): $VERDICT"
  if [[ "$VERDICT" == GENUINE* || "$VERDICT" == ALREADY_GENUINE ]]; then
    python3 exec100_claim.py complete --instance "$INSTANCE" --arm "$ARM" --worker "W$WID" --key "$KEYFILE" | tail -1
    rm -rf "$OUT" 2>/dev/null
    FAILSTREAK=0
  else
    python3 exec100_claim.py retry --instance "$INSTANCE" --arm "$ARM" --note "$VERDICT" | tail -1
    FAILSTREAK=$((FAILSTREAK+1))
    # Failed builds cost $0 (no LLM); the containerd pull race warms out as the
    # image cache fills, so persist through transient clusters rather than
    # churning. Only self-disable on a long streak (a genuinely bad key/host).
    if [ $FAILSTREAK -ge 10 ]; then
      echo "W$WID: 10 consecutive non-genuine results; self-disabling this worker"
      break
    fi
    sleep $((5 + FAILSTREAK * 5))   # graduated backoff
  fi
done
