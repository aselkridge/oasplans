---
name: project-tracker
description: Reconcile arch-site/TRACKER.md — the single source of truth for the architecture-website/HubSpot project — against work that has actually been completed. Use this whenever work on that project finishes, a decision gets made, a question gets answered, or a new blocker appears; whenever the user asks "where are we", "what's left", "what's the status", or asks to update/check the tracker; whenever a [tracker check] reminder appears; and right after a compaction, to verify nothing was lost. Also use it before ending a work session on this project. Prefer running it a little too often over letting the tracker drift — a tracker nobody trusts is worse than no tracker.
---

# Project tracker maintenance

`arch-site/TRACKER.md` is the sole source of truth for the architecture-firm
website project. Everything else — chat history, memory, a summary that survived
compaction — is lossy. This skill exists to keep the file worth trusting, because
the moment it's out of date, people go back to trusting chat history, and then
compaction quietly eats the project.

Your job is the part a script can't do: deciding what actually changed and what
it means. A PreCompact hook already records the mechanical facts (branch, HEAD,
dirty files) in the AUTOSNAPSHOT block. Don't duplicate that work, and don't
edit that block.

## How to run it

**1. Read the tracker first.** Always. Reconciling from memory is how a tracker
starts describing a project that no longer exists.

**2. Work out what actually changed** since the file was last written. Useful
signals, roughly in order of reliability:

```bash
git log --oneline -15
git status --short
git diff --stat HEAD
```

Then look at the conversation for the things git can't see: decisions Aaron
made, questions he answered, new constraints, things that turned out harder
than expected.

**3. Apply the changes.** In rough priority order — a wrong Status line is worse
than a missing checkbox:

- **Status at a glance** — phase, what's blocking, next deliverable. If this
  table is stale, everything below it reads as untrustworthy.
- **Open questions** — mark answered ones ✅ and fold the answer into the right
  place (usually Decisions locked, sometimes a work item). An answered question
  that's still sitting in the Open table will get asked again, which is
  irritating for Aaron and makes the tracker look unread.
- **Decisions locked** — add new ones with a real rationale and a date. The
  rationale is the point: in three weeks nobody remembers *why*, and without it
  the decision gets relitigated. If a locked decision is being reopened, move it
  back to Open questions rather than silently editing it.
- **Work items** — tick off completed items, move things between Now / Next /
  Later, add anything newly discovered. Move finished items into **Done** with a
  date rather than deleting them; the Done list is how a resumed session sees
  momentum.
- **Risks / watch-list** — add newly discovered ones, strike through retired
  ones with a note on how they were resolved.

**4. Keep it honest.** Only tick something that's actually done and verified.
"Scaffolded but never run" is not done — that's the failure mode that makes a
tracker actively harmful, because it hides work that still needs doing. If
something is half-finished, say so in the item text.

**5. Don't announce it.** Update the file and get back to the work. A short line
like "tracker updated — Q4 answered, moved image pipeline to Next" is plenty.
When this runs from a `[tracker check]` reminder and nothing has actually
changed, change nothing and say nothing.

## Things worth preserving

- **Keep it readable by Aaron's dad.** He is a non-technical stakeholder on this
  project. That's why the Glossary exists and why work items are written in
  plain language. Resist letting it drift into jargon.
- **Boxed items are deliberate.** 📦 means "deferred on purpose", not "forgotten".
  Don't promote a boxed question to blocking just because it's unanswered — but
  do promote it the moment it genuinely starts blocking something, and say so.
- **Don't let it sprawl.** The SessionStart hook injects this file after every
  compaction and has a ~9k character budget. Past that it gets trimmed and the
  project loses exactly the context it was trying to keep. If the file is
  growing, compress the Done list into summary lines rather than dropping
  sections.

## When the project moves repos

The tracker currently lives inside `aarons-portfolio` (see risk R1 — it should
get its own repo before real site code lands). If it moves, update
`TRACKER_REL` in `.claude/hooks/tracker_lib.py`; every hook reads the path from
that one constant.
