"""bb intake: start a manager for every ticket that is ready.

Runs as a bb script automation on the bb server. Every Todo task of the tracker
project TRACKER is dispatched to the delegation preset PRESET (default
"Manager"); with LABEL set, only Todo tasks with that label. Delegation moves a
task to In progress, so the next run does not dispatch it again.

Prints nothing when there is nothing to start, so a quiet run is recorded as a
silent tick. Exits 1 if any dispatch failed; the other tasks are still tried.
"""

import json
import os
import subprocess
import sys


def bb(*args: str) -> str:
    result = subprocess.run(["bb", *args], capture_output=True, text=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"bb {' '.join(args[:2])} failed: {message}")
    return result.stdout


def main() -> int:
    tracker = os.environ.get("TRACKER", "").strip()
    if not tracker:
        print("TRACKER is not set: pass it with --env-json", file=sys.stderr)
        return 1
    preset = os.environ.get("PRESET", "").strip() or "Manager"
    label = os.environ.get("LABEL", "").strip()

    query = ["tasks", "list", "--project", tracker, "--status", "todo"]
    query += ["--limit", "50", "--json"]
    if label:
        query += ["--label", label]
    tasks = json.loads(bb(*query))["tasks"]

    failed = 0
    for task in tasks:
        key = task["key"]
        try:
            bb("tasks", "dispatch", key, "--preset", preset)
            print(f"{key}: dispatched to {preset}")
        except RuntimeError as error:
            failed += 1
            print(f"{key}: {error}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
