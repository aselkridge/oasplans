#!/usr/bin/env python3
"""SessionStart hook — put the tracker back into context.

This is the half that actually rescues the project from compaction. Unlike
PreCompact, SessionStart *does* support `additionalContext`, and it fires with
source="compact" immediately after a compaction. So the moment context is
squeezed, the tracker is re-injected and Claude wakes up holding the current
decisions, open questions and work items rather than a lossy summary of them.

It also fires on startup/resume, which is why the tracker is worth keeping
accurate: it is the thing a fresh session reads first.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker_lib import CONTEXT_LIMIT, TRACKER_REL, emit, read_event, tracker_path  # noqa: E402

# Dropped in this order when the doc outgrows the hook's output budget. The
# ordering is a judgment about what a resumed session most needs: decisions and
# open questions are load-bearing, the glossary is a courtesy.
DROPPABLE = ["## Glossary", "## Risks / watch-list"]


def trim(text):
    if len(text) <= CONTEXT_LIMIT:
        return text
    for heading in DROPPABLE:
        idx = text.find("\n" + heading)
        if idx == -1:
            continue
        end = text.find("\n## ", idx + 1)
        cut = text[idx:end] if end != -1 else text[idx:]
        text = text.replace(cut, f"\n{heading} — trimmed for length; read the file for it.\n")
        if len(text) <= CONTEXT_LIMIT:
            return text
    return text[:CONTEXT_LIMIT] + "\n\n…truncated. Read the tracker file for the rest."


def main():
    event = read_event()
    path = tracker_path(event)
    source = event.get("source", "startup")

    if not os.path.exists(path):
        emit({})

    with open(path, "r", encoding="utf-8") as fh:
        body = fh.read()

    if source == "compact":
        preamble = (
            "Context was just compacted. The architecture-site project tracker is "
            "reproduced below — it is the sole source of truth for this project, and "
            "it outranks anything that survived in the compaction summary. Before "
            "acting, reconcile: if work finished before the compaction isn't "
            "reflected here, run the `project-tracker` skill to record it."
        )
    else:
        preamble = (
            f"Architecture-site project tracker (`{TRACKER_REL}`) — the sole source of "
            "truth for to-dos, decisions and progress on this project. Keep it current "
            "with the `project-tracker` skill as work completes."
        )

    emit({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": f"{preamble}\n\n---\n\n{trim(body)}",
        }
    })


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
