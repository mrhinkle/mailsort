---
description: Backlog cleanup in bulk — mark dead archives read, file by sender or domain, collapse tool digests; always with before/after counts and re-query verification
argument-hint: "<dead-archive | by-sender <address|domain> | digests> [mailbox] [--dry-run]"
allowed-tools: Read, Skill
---

Load `mailsort` (resolve the override layer) and `mailsort-sweep`. Parse `$ARGUMENTS` for the mode,
an optional mailbox, and `--dry-run`. If no mode is given, list the three modes with one line each
and stop. Follow the skill: measure first (counts per label or sender), show the plan and the exact
counts it will touch, wait for the owner's yes in chat unless `--dry-run`, run in ≤1000-id batches
with page tokens persisted, verify every batch by re-query, and finish with a before/after table.
Archive and mark-read only; never delete, never mark spam, never touch labels another tool owns.
