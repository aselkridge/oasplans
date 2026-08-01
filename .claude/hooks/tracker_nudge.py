#!/usr/bin/env python3
"""Stop hook — the "runs regularly" part.

A tracker only stays true if something keeps asking whether it's still true.
Nobody wants to remember that, so this fires at the end of a turn and, when the
tracker has drifted behind the actual work, quietly asks Claude to reconcile it.

Two things keep this from becoming noise:
  - a turn-count cooldown, so it speaks up occasionally rather than constantly
  - a staleness test, so a quiet stretch of conversation never triggers it

The cooldown also guarantees termination: injecting context at Stop can produce
another turn, which fires Stop again, but the counter won't let it nudge twice.
"""

import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker_lib import TRACKER_REL, emit, git, project_dir, read_event, tracker_path  # noqa: E402

TURNS_BETWEEN_NUDGES = 12
STATE_REL = os.path.join(".claude", ".tracker-state.json")


def load_state(root):
    path = os.path.join(root, STATE_REL)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {"turns": 0, "last_nudge_turn": 0}


def save_state(root, state):
    path = os.path.join(root, STATE_REL)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
    except Exception:
        pass


def is_stale(root, path):
    """Has real work happened since the tracker was last written?

    Two signals, both cheap: commits newer than the file, and a dirty tree.
    Either means the file may no longer describe reality.
    """
    try:
        tracker_mtime = os.path.getmtime(path)
    except OSError:
        return False

    last_commit = git(root, "log", "-1", "--format=%ct")
    if last_commit.isdigit() and int(last_commit) > tracker_mtime:
        return True

    dirty = git(root, "status", "--porcelain")
    for line in dirty.splitlines():
        # Edits to the tracker itself don't make the tracker stale.
        if line.strip() and not line.strip().endswith(TRACKER_REL):
            return True
    return False


def main():
    event = read_event()
    root = project_dir(event)
    path = tracker_path(event)

    state = load_state(root)
    state["turns"] = state.get("turns", 0) + 1

    if not os.path.exists(path):
        save_state(root, state)
        emit({})

    due = state["turns"] - state.get("last_nudge_turn", 0) >= TURNS_BETWEEN_NUDGES
    if not (due and is_stale(root, path)):
        save_state(root, state)
        emit({})

    state["last_nudge_turn"] = state["turns"]
    save_state(root, state)

    emit({
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": (
                f"[tracker check] `{TRACKER_REL}` hasn't been updated since the last "
                "commits or working-tree changes. If anything has been completed, "
                "decided, or newly blocked since it was last written, run the "
                "`project-tracker` skill now to reconcile it. If the tracker is already "
                "accurate, say nothing and carry on — this is a routine check, not a "
                "request for a status report to the user."
            ),
        }
    })


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
