#!/usr/bin/env python3
"""Spawn a fully detached process: double-fork + setsid so the child lives in
its own session and survives the spawning process group being killed (the
harness reaps background handles and takes their process group with them;
macOS has no setsid(1) binary). Usage:

    spawn_detached.py LOGFILE CMD [ARG...]

Appends the child's stdout+stderr to LOGFILE; prints the detached PID."""
import os
import sys


def main():
    log, cmd = sys.argv[1], sys.argv[2:]
    pid = os.fork()
    if pid > 0:
        os.waitpid(pid, 0)          # reap the intermediate child
        return
    os.setsid()
    pid2 = os.fork()
    if pid2 > 0:
        print(f"DETACHED pid={pid2} log={log}", flush=True)
        os._exit(0)
    fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
