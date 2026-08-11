#!/usr/bin/env python3
"""Adaptive concurrency controller for the Phase-C scale-out (owner directive
sections F/G/I). Spawns detached sidecar workers up to an adaptive target,
never kills healthy workers (scale-down = don't replace), releases the
original runner's patched claims when its patched phase ends, releases stale
claims, and writes exec100_parallel_status.json + LEDGER lines every cycle.
"""
import glob
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.expanduser("~/swebench-agents")
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from exec100_ledger import arm_stats  # noqa: E402

KEYS = [f"key{i:02d}" for i in range(1, 21) if i != 9]   # key09 = duplicate of key08
# The binding constraint is the pre-existing colima Docker VM (4 vCPU / 7 GB
# RAM / ~59 GB docker disk), NOT the 20-key pool. Every rollout runs a
# CPU/RAM-heavy container in that one VM, which cannot be resized without
# restarting colima and killing the protected runner's in-flight containers.
# So concurrency is capped by VM health, and the "2 workers/key" target is
# infeasible locally (it would be ~38 containers on 4 vCPU). Keys still remove
# any LLM-side TPM ceiling and enable pair-affinity; parallelism is bounded by
# the VM. Sidecars run ALONGSIDE the original runner's 3 concurrent rollouts.
MAX_TARGET = 8           # sidecar ceiling: ~8 + runner's 3 on a 4-vCPU VM (rollouts idle on LLM I/O)
START_TARGET = 3
VM_CPUS = 4
VM_RAM_GB = 7
DOCKER_DISK_MIN_GB = 10  # colima /var/lib/docker reserve
HOST_LOAD_MAX = 24.0     # 14 host cores; VM load shows here too
SWAP_MAX_MB = 6144


def sh(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True).stdout


def workers_alive():
    out = sh("ps", "-eo", "pid,command")
    ws = {}
    for l in out.splitlines():
        m = re.search(r"exec100_worker\.sh (\d+) (key\d\d)", l)
        if m and "grep" not in l:
            ws[int(m.group(1))] = m.group(2)
    return ws


def count_429(path_glob):
    n = 0
    for p in glob.glob(path_glob):
        try:
            n += open(p, errors="ignore").read().count("429")
        except OSError:
            pass
    return n


def host():
    load = float(sh("sysctl", "-n", "vm.loadavg").split()[1])
    swap = sh("sysctl", "-n", "vm.swapusage")
    used_mb = float(re.search(r"used = ([\d.]+)M", swap).group(1)) if "used" in swap else 0.0
    # colima VM docker-disk free (the binding disk), not host /
    vm = sh("colima", "ssh", "--", "df", "-BG", "/var/lib/docker")
    m = re.search(r"\s(\d+)G\s+\d+%", vm)
    docker_disk_gb = int(m.group(1)) if m else 999
    docker_ok = subprocess.run(["docker", "info"], capture_output=True).returncode == 0
    return load, used_mb, docker_disk_gb, docker_ok


def safe_docker_cleanup(disk_gb):
    """Non-racing: only when the VM docker disk is genuinely low, remove images
    with NO container and untagged layers older than 20m. Never touches an
    image backing a running container, so it cannot evict a mid-use rollout."""
    if disk_gb > DOCKER_DISK_MIN_GB + 6:
        return
    subprocess.run(["docker", "container", "prune", "-f"], capture_output=True)
    subprocess.run(["docker", "image", "prune", "-af", "--filter", "until=20m"],
                   capture_output=True)


def pending_left():
    import sqlite3
    c = sqlite3.connect(os.path.join(ROOT, "execution_scheduler.sqlite"), timeout=60)
    rows = dict(c.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall())
    per_arm = dict(c.execute("SELECT arm || ':' || state, COUNT(*) FROM jobs GROUP BY arm, state").fetchall())
    c.close()
    return rows, per_arm


def main():
    target = START_TARGET
    next_wid = 1
    spawned = {}
    prev_gen, prev_t = None, time.time()
    released_patched = False
    key_cursor = 0
    while True:
        # release stale claims each cycle
        sh("python3", "exec100_claim.py", "release-stale")
        # hand patched leftovers to the fleet once the original runner leaves its patched phase
        if not released_patched:
            log = open("exec100_v2.log", errors="ignore").read()
            orig_alive = "exec100_arm_v2.sh" in sh("ps", "-eo", "command")
            if "ARM-patched-ROLLOUTS-DONE" in log or not orig_alive:
                sh("python3", "exec100_claim.py", "release-original-patched")
                released_patched = True
        rows, per_arm = pending_left()
        outstanding = rows.get("PENDING", 0) + rows.get("ERROR_RETRYABLE", 0) + \
            sum(v for k, v in rows.items() if k == "CLAIMED")
        ws = workers_alive()
        p, b = arm_stats("patched"), arm_stats("baseline")
        genuine = p["genuine"] + b["genuine"]
        load, swap_mb, disk_gb, docker_ok = host()
        safe_docker_cleanup(disk_gb)
        e429 = count_429("_exec100_sidecar/*/worker_run.log") + \
            count_429("_exec100_sidecar_failed/*/worker_run.log")

        # adaptive target — capped by VM health, +1 at a time (gentle on 4 vCPU)
        rate = None
        if prev_gen is not None and time.time() > prev_t:
            rate = (genuine - prev_gen) / ((time.time() - prev_t) / 3600)
        healthy = (load < HOST_LOAD_MAX and swap_mb < SWAP_MAX_MB
                   and disk_gb > DOCKER_DISK_MIN_GB and docker_ok and e429 < 25)
        if healthy and len(ws) >= target:
            target = min(MAX_TARGET, target + 1)
        elif not healthy:
            target = max(2, target - 2)
        prev_gen, prev_t = genuine, time.time()

        # spawn up to target (only if fleet-claimable work exists)
        claimable = rows.get("PENDING", 0) + rows.get("ERROR_RETRYABLE", 0)
        while len(ws) < min(target, max(claimable, 0)) and claimable > 0:
            key = KEYS[key_cursor % len(KEYS)]
            key_cursor += 1
            wid = next_wid
            next_wid += 1
            subprocess.run(["python3", "spawn_detached.py",
                            f"_exec100_sidecar_w{wid}.log", "zsh",
                            "exec100_worker.sh", str(wid), key])
            spawned[wid] = key
            time.sleep(3)
            ws = workers_alive()

        per_key = {}
        for wid, key in ws.items():
            per_key[key] = per_key.get(key, 0) + 1
        status = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "GENUINE_COMPLETE": f"{genuine}/200",
            "BASELINE_COMPLETE": f"{b['genuine']}/100",
            "PATCHED_COMPLETE": f"{p['genuine']}/100",
            "RUNNING_CLAIMS": rows.get("CLAIMED", 0),
            "PENDING": rows.get("PENDING", 0),
            "RETRYABLE": rows.get("ERROR_RETRYABLE", 0),
            "scored_pairs": "0/100 (scoring runs at freeze)",
            "luna_calls": p["api_calls"] + b["api_calls"],
            "tokens_in": p["tokens_in"] + b["tokens_in"],
            "tokens_out": p["tokens_out"] + b["tokens_out"],
            "spend_usd": round(p["spend_usd"] + b["spend_usd"], 2),
            "events_429": e429,
            "active_workers": len(ws), "target": target,
            "workers_per_key": per_key,
            "host": {"load": load, "swap_mb": swap_mb, "vm_docker_disk_gb": disk_gb,
                     "docker_ok": docker_ok, "vm_cpus": VM_CPUS, "vm_ram_gb": VM_RAM_GB},
            "genuine_per_hour": round(rate, 1) if rate is not None else None,
            "original_runner_alive": "exec100_arm_v2.sh" in sh("ps", "-eo", "command"),
            "patched_released_to_fleet": released_patched,
        }
        json.dump(status, open("exec100_parallel_status.json", "w"), indent=1)
        print(f"LEDGER {status['ts']}: genuine {genuine}/200 (b {b['genuine']} p {p['genuine']}) "
              f"| claimed {status['RUNNING_CLAIMS']} pending {status['PENDING']} "
              f"retry {status['RETRYABLE']} | workers {len(ws)}/{target} | 429s {e429} "
              f"| load {load:.1f} swap {swap_mb:.0f}MB disk {disk_gb}GB "
              f"| spend ${status['spend_usd']}", flush=True)

        if genuine >= 200:
            print("CONTROLLER: 200 genuine reached — freeze point", flush=True)
            break
        if outstanding == 0 and len(ws) == 0:
            print("CONTROLLER: no outstanding fleet work; exiting "
                  f"(genuine={genuine}; original runner owns the rest)", flush=True)
            break
        time.sleep(60)


if __name__ == "__main__":
    main()
