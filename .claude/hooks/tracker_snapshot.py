#!/usr/bin/env python3
"""PreCompact hook — freeze hard project state into the tracker.

Why this exists: a PreCompact hook can't ask Claude to do anything. It can only
run a command (or block compaction, which we never do — blocking a compaction
that fires because context is exhausted is a good way to wedge a session).

So this hook writes down the things that don't need judgment — branch, HEAD,
what's committed, what's still dirty — into the tracker's AUTOSNAPSHOT block.
That way, even if the conversation is compacted mid-thought and nobody
remembered to run /project-tracker, the mechanical facts survive in the file.

The judgment half — deciding what's actually *done* — belongs to the skill.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker_lib import BEGIN, END, git, now, project_dir, read_event, tracker_path  # noqa: E402


def build_snapshot(root, event):
    branch = git(root, "rev-parse", "--abbrev-ref", "HEAD") or "(unknown)"
    head = git(root, "log", "-1", "--format=%h %s") or "(no commits)"
    dirty = git(root, "status", "--porcelain")
    recent = git(root, "log", "-8", "--format=- `%h` %s")
    trigger = event.get("trigger") or event.get("matcher") or "compaction"

    lines = [
        BEGIN,
        "",
        "### Auto-snapshot — written by the PreCompact hook, do not hand-edit",
        "",
        f"_Captured {now(root)} (trigger: {trigger}). Mechanical git state only._",
        "",
        f"**Branch:** `{branch}`  ",
        f"**HEAD:** {head}",
        "",
    ]

    if dirty:
        entries = [ln for ln in dirty.splitlines() if ln.strip()]
        lines.append(f"**Uncommitted ({len(entries)}):**")
        lines.append("")
        for ln in entries[:25]:
            lines.append(f"- `{ln.strip()}`")
        if len(entries) > 25:
            lines.append(f"- …and {len(entries) - 25} more")
        lines.append("")
        lines.append("> Uncommitted work at compaction time — verify it wasn't lost.")
    else:
        lines.append("**Working tree:** clean.")

    lines += ["", "**Recent commits:**", "", recent or "- (none)", "", END]
    return "\n".join(lines)


def main():
    event = read_event()
    root = project_dir(event)
    path = tracker_path(event)

    if not os.path.exists(path):
        # Nothing to update. Silence is correct — the tracker may legitimately
        # not exist yet, or may have moved to its own repo.
        sys.exit(0)

    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()

    if BEGIN not in text or END not in text:
        sys.exit(0)

    head, _, rest = text.partition(BEGIN)
    _, _, tail = rest.partition(END)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(head + build_snapshot(root, event) + tail)

    # Reset the staleness clock — the tracker was just touched mechanically,
    # but the *reconciliation* still needs Claude, so don't mark it reconciled.
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never, under any circumstances, break compaction.
        sys.exit(0)
