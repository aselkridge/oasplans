"""Shared helpers for the project-tracker hooks.

These hooks sit on the critical path of compaction and end-of-turn, so the
overriding rule is: never break the session. Every entry point wraps its work
and exits 0 no matter what goes wrong. A tracker that silently skips an update
is a nuisance; a hook that wedges compaction is a broken session.
"""

import json
import os
import subprocess
import sys

BEGIN = "<!-- AUTOSNAPSHOT:BEGIN -->"
END = "<!-- AUTOSNAPSHOT:END -->"

# Hook output strings are capped at 10k chars by the harness; stay under it.
CONTEXT_LIMIT = 9000

# Relative to the project root. Kept in one place so moving the tracker (e.g.
# into its own repo, see risk R1) is a one-line change.
TRACKER_REL = os.path.join("arch-site", "TRACKER.md")


def read_event():
    """Parse the hook payload from stdin, tolerating an empty or broken one."""
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def project_dir(event):
    """Best available guess at the project root.

    CLAUDE_PROJECT_DIR is set by the harness at hook time but isn't guaranteed,
    so fall back to the cwd the event carries, then to the actual cwd.
    """
    return (
        os.environ.get("CLAUDE_PROJECT_DIR")
        or event.get("cwd")
        or os.getcwd()
    )


def tracker_path(event):
    return os.path.join(project_dir(event), TRACKER_REL)


def git(root, *args):
    try:
        out = subprocess.run(
            ["git", "-C", root, *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def now(root):
    """Timestamp without importing datetime-in-a-sandbox concerns."""
    try:
        out = subprocess.run(
            ["date", "-u", "+%Y-%m-%d %H:%M UTC"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown time"


def emit(payload):
    """Print a hook JSON response and exit cleanly."""
    try:
        sys.stdout.write(json.dumps(payload))
    except Exception:
        pass
    sys.exit(0)
