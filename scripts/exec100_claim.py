#!/usr/bin/env python3
"""Atomic work-claim scheduler for the Phase-C scale-out (owner directive).

SQLite (execution_scheduler.sqlite, OUTSIDE scientific outputs) holds one row
per instance x arm with exactly one state: PENDING / CLAIMED /
GENUINE_COMPLETE / ERROR_RETRYABLE / SCORED. Claims are atomic (BEGIN
IMMEDIATE). Genuine completion (per the preregistered ledger criterion)
always overrides scheduler state. Patched jobs start CLAIMED by
'original-runner' — the untouched exec100_arm_v2.sh owns that arm until its
patched phase ends; the controller releases leftovers to the fleet then.

Commands:
  init                    seed DB from _exec100_instances.json + disk truth
  claim  --worker W --key KEYxx [--pid N]     -> prints "instance|arm" or "NONE"
  complete --instance I --arm A --worker W --key KEYxx
  retry    --instance I --arm A [--note S]
  release-stale           free CLAIMED rows whose pid is dead and no genuine traj
  release-original-patched  move original-runner patched claims -> PENDING
  status                  print state counts
"""
import argparse
import glob
import json
import os
import sqlite3
import sys
import time

ROOT = os.path.expanduser("~/swebench-agents")
DB = os.path.join(ROOT, "execution_scheduler.sqlite")
sys.path.insert(0, ROOT)
from exec100_ledger import classify  # noqa: E402


def conn():
    c = sqlite3.connect(DB, timeout=60)
    c.execute("PRAGMA busy_timeout=60000")
    return c


def genuine_on_disk(instance, arm):
    for tp in glob.glob(os.path.join(ROOT, f"_exec100_{arm}", instance, "*.traj")):
        if classify(tp)[0] == "genuine":
            return True
    return False


def init():
    c = conn()
    c.execute("""CREATE TABLE IF NOT EXISTS jobs(
        instance TEXT, arm TEXT, state TEXT, worker TEXT, key_label TEXT,
        pid INTEGER, claimed_at REAL, completed_at REAL, note TEXT,
        PRIMARY KEY (instance, arm))""")
    inst = json.load(open(os.path.join(ROOT, "_exec100_instances.json")))
    with c:
        for i in inst:
            for arm in ("baseline", "patched"):
                if genuine_on_disk(i, arm):
                    state, worker = "GENUINE_COMPLETE", "pre-scaleout"
                elif arm == "patched":
                    state, worker = "CLAIMED", "original-runner"
                else:
                    state, worker = "PENDING", None
                c.execute("INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?,?)",
                          (i, arm, state, worker, None, None, time.time(), None, "seed"))
        # refresh rows that were seeded earlier but have since completed on disk
        for i, arm, st in c.execute("SELECT instance, arm, state FROM jobs").fetchall():
            if st != "GENUINE_COMPLETE" and genuine_on_disk(i, arm):
                c.execute("UPDATE jobs SET state='GENUINE_COMPLETE', completed_at=? "
                          "WHERE instance=? AND arm=?", (time.time(), i, arm))
    print("scheduler initialized:", dict(c.execute(
        "SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall()))


def claim(worker, key, pid):
    c = conn()
    with c:
        c.execute("BEGIN IMMEDIATE")
        # pair-affinity preference: a PENDING/RETRYABLE job whose sibling arm was
        # completed under MY key; else any pending; retryables last
        row = c.execute("""
            SELECT j.instance, j.arm FROM jobs j
            LEFT JOIN jobs s ON s.instance = j.instance AND s.arm != j.arm
            WHERE j.state IN ('PENDING','ERROR_RETRYABLE')
            ORDER BY (s.key_label IS NOT NULL AND s.key_label = ?) DESC,
                     j.state = 'PENDING' DESC, j.instance
            LIMIT 1""", (key,)).fetchone()
        if not row:
            print("NONE")
            return
        i, arm = row
        if genuine_on_disk(i, arm):   # disk truth overrides
            c.execute("UPDATE jobs SET state='GENUINE_COMPLETE' WHERE instance=? AND arm=?", (i, arm))
            print("NONE")
            return
        c.execute("UPDATE jobs SET state='CLAIMED', worker=?, key_label=?, pid=?, "
                  "claimed_at=? WHERE instance=? AND arm=?",
                  (worker, key, pid, time.time(), i, arm))
    print(f"{i}|{arm}")


def complete(instance, arm, worker, key):
    ok = genuine_on_disk(instance, arm)
    c = conn()
    with c:
        if ok:
            c.execute("UPDATE jobs SET state='GENUINE_COMPLETE', worker=?, key_label=?, "
                      "completed_at=? WHERE instance=? AND arm=?",
                      (worker, key, time.time(), instance, arm))
        else:
            c.execute("UPDATE jobs SET state='ERROR_RETRYABLE', note='completed-not-genuine' "
                      "WHERE instance=? AND arm=?", (instance, arm))
    print("GENUINE_COMPLETE" if ok else "ERROR_RETRYABLE")


def retry(instance, arm, note):
    c = conn()
    with c:
        c.execute("UPDATE jobs SET state='ERROR_RETRYABLE', note=? WHERE instance=? AND arm=?",
                  (note or "worker-retry", instance, arm))
    print("ERROR_RETRYABLE")


def release_stale():
    c = conn()
    n = 0
    with c:
        for i, arm, pid in c.execute("SELECT instance, arm, pid FROM jobs WHERE "
                                     "state='CLAIMED' AND worker != 'original-runner'").fetchall():
            alive = pid and os.path.exists(f"/proc/{pid}")
            if not alive and pid:
                try:
                    os.kill(pid, 0)
                    alive = True
                except (ProcessLookupError, PermissionError):
                    alive = False
            if alive:
                continue
            if genuine_on_disk(i, arm):
                c.execute("UPDATE jobs SET state='GENUINE_COMPLETE', completed_at=? "
                          "WHERE instance=? AND arm=?", (time.time(), i, arm))
            else:
                c.execute("UPDATE jobs SET state='ERROR_RETRYABLE', note='stale-claim-released' "
                          "WHERE instance=? AND arm=?", (i, arm))
                n += 1
    print(f"released {n} stale claims")


def release_original_patched():
    c = conn()
    with c:
        for i, arm in c.execute("SELECT instance, arm FROM jobs WHERE state='CLAIMED' "
                                "AND worker='original-runner'").fetchall():
            if genuine_on_disk(i, arm):
                c.execute("UPDATE jobs SET state='GENUINE_COMPLETE', completed_at=? "
                          "WHERE instance=? AND arm=?", (time.time(), i, arm))
            else:
                c.execute("UPDATE jobs SET state='PENDING', worker=NULL "
                          "WHERE instance=? AND arm=?", (i, arm))
    print("original-runner patched claims resolved against disk and released")


def status():
    c = conn()
    print(dict(c.execute("SELECT state, COUNT(*) FROM jobs GROUP BY state").fetchall()))
    print(dict(c.execute("SELECT arm || ':' || state, COUNT(*) FROM jobs "
                         "GROUP BY arm, state").fetchall()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--worker")
    ap.add_argument("--key")
    ap.add_argument("--pid", type=int, default=0)
    ap.add_argument("--instance")
    ap.add_argument("--arm")
    ap.add_argument("--note")
    a = ap.parse_args()
    {"init": init, "status": status, "release-stale": release_stale,
     "release-original-patched": release_original_patched,
     "claim": lambda: claim(a.worker, a.key, a.pid),
     "complete": lambda: complete(a.instance, a.arm, a.worker, a.key),
     "retry": lambda: retry(a.instance, a.arm, a.note)}[a.cmd]()
