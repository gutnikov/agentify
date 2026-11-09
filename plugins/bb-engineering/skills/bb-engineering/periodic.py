"""bb periodic task: start a manager on a fresh ticket.

Runs as a bb script automation on the bb server, on the automation's schedule.
Each run creates a ticket in tracker project TRACKER, titled TITLE and the date,
with ASSIGNMENT as its description and LABEL as its label, and dispatches it to
the delegation preset PRESET (default "Manager").

While an earlier ticket with LABEL is still open, the run does nothing and
prints nothing, so runs never pile up. If the dispatch fails, the new ticket is
canceled, so that the next run tries again, and the run fails.
"""

import datetime
import json
import os
import subprocess
import sys

OPEN_STATUSES = "backlog,todo,in_progress,in_review"


def bb(*args: str) -> str:
    result = subprocess.run(["bb", *args], capture_output=True, text=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"bb {' '.join(args[:2])} failed: {message}")
    return result.stdout


def main() -> int:
    names = ("TRACKER", "TITLE", "ASSIGNMENT", "LABEL")
    env = {name: os.environ.get(name, "").strip() for name in names}
    missing = [name for name, value in env.items() if not value]
    if missing:
        print(f"{', '.join(missing)} not set: pass with --env-json", file=sys.stderr)
        return 1
    preset = os.environ.get("PRESET", "").strip() or "Manager"
    tracker, label = env["TRACKER"], env["LABEL"]

    open_tickets = json.loads(
        bb("tasks", "list", "--project", tracker, "--label", label,
           "--status", OPEN_STATUSES, "--limit", "1", "--json")
    )["tasks"]
    if open_tickets:
        return 0

    title = f"{env['TITLE']} · {datetime.date.today().isoformat()}"
    automation = os.environ.get("BB_AUTOMATION_ID", "")
    origin = f" (bb automation {automation})" if automation else ""
    description = (
        f"{env['ASSIGNMENT']}\n\n---\n"
        f"Started by the periodic task \"{env['TITLE']}\"{origin}."
    )
    ticket = json.loads(
        bb("tasks", "create", "--project", tracker, "--title", title,
           "--label", label, "--description", description, "--json")
    )["task"]
    key = ticket["key"]
    try:
        bb("tasks", "dispatch", key, "--preset", preset)
    except RuntimeError as error:
        print(f"{key}: {error}", file=sys.stderr)
        bb("tasks", "update", key, "--status", "canceled")
        return 1
    print(f"{key}: {title}, dispatched to {preset}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as error:
        print(error, file=sys.stderr)
        sys.exit(1)
