---
name: mailsort-sweep
description: >
  Backlog mode for the mailsort family — bulk cleanup separate from daily triage: mark dead archives
  read (labels with thousands unread and no new mail in months), file everything from a sender or
  domain to its home label, and collapse tool digests, always measured first and verified by
  re-query with before/after counts. Use when someone says "clean up my backlog", "I have 90,000
  unread", "file everything from X", "mark that label read", "sweep the archive", "bulk archive",
  or when triage finds a label that is frozen history rather than a queue. Archives and marks read
  only; never deletes, never marks spam, never touches labels another tool owns, and never acts on
  the inbox of a mailbox whose policy is "file only" or "report only".
---

# mailsort-sweep

Daily triage handles the inflow. Sweep handles the pile that was there before triage existed. The
two must stay separate: a sweep run never touches today's mail, and triage never bulk-acts.

## Measure first, always

Before any write, produce the table the owner will approve:

| Label / sender | Total | Unread | Newest message | Proposed action | Messages touched |

Nothing moves until the owner says yes in chat to that exact table. With `--dry-run`, the table is
the whole output.

## Modes

### `dead-archive`
A label is dead archive when it has unread > 0 **and** no message newer than N days (default 90).
Unread there is not a backlog; it is frozen history that inflates every count. Action: remove
`UNREAD` on every message under the label. Do not archive (they are already out of the inbox) and do
not remove the label. Report the account-level unread before and after.

### `by-sender <address|domain>`
File every message from the sender or domain to its home label and remove `INBOX`. The home label
comes from the override layer; if none, propose one from the existing vocabulary and wait. If the
sender fails the machine test and the volume is high, suggest adding it to aggregate-only senders
and running `/mailsort:rules` so the client does this next time.

### `digests`
Collapse notification digests from tools that own their own labels (SaneBox digests, Superhuman
summaries, vendor weekly roll-ups): mark read and archive the digests only, never the labels those
tools own. Report the count per tool.

## Batch mechanics (both providers)

- **Batches of at most 1000 ids** (`GMAIL_BATCH_MODIFY_MESSAGES`; `OUTLOOK_BATCH_UPDATE_MESSAGES`
  / `OUTLOOK_BATCH_MOVE_MESSAGES`).
- **A success response is acceptance only.** It silently skips bad ids and returns no per-message
  status. After every batch, re-query the count and compare. Report the re-query, never the response.
- **Discovery by fresh query, not by paging where possible:** when the write removes the thing the
  query matches (`UNREAD`, `INBOX`), loop fetch-500 → modify-500 → fetch again; each pass returns
  fresh rows. When the write does not change the match, persist the page token across calls or
  page 1 is re-processed forever.
- **Positive label ids over exclusions:** a `-label:` exclusion under-matches; query with
  `label_ids` and filter locally. Label names containing `@` break query syntax; use ids.
- **Per-cell timeouts:** a remote workbench cell dies around 180 seconds and the already-accepted
  jobs keep completing. Split more than three 1000-id batches across cells, and after a timeout
  recount before re-running rather than assuming failure.
- **Trash is not an anomaly** if the override layer says another tool or the owner routinely
  trashes filed mail in this mailbox. Count it as a verified write; never untrash.

## Report

Before/after table per label or sender, account-level unread before/after when the mode changed
read state, the number of batches run, and any count that did not reconcile (re-query ≠ expected)
as a named discrepancy, not a success. Append one learned-rules line per sweep:
`YYYY-MM-DD | sweep <mode> <target> | N touched`.

## Anti-rules

- Never sweep the inbox of a "file only" or "report only" mailbox.
- Never delete, never mark spam, never unsubscribe.
- Never write a label another tool owns.
- Never report "done" from a write response.
