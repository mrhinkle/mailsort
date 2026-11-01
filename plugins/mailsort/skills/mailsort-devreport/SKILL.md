---
name: mailsort-devreport
description: >
  The development status section of a daily briefing — what shipped, what is blocked, and what needs a
  decision across every active project, drawn from repo and issue-tracker activity rather than from
  mail. Platform-neutral (GitHub, GitLab, or any tracker). Part of the `mailsort` family and designed
  to slot into `mailsort-briefing`. Use when someone asks for a development report, engineering
  status, "what shipped", "what's blocked", a standup replacement, or a project roll-up. It reports
  outcomes; it never merges, closes, deploys, or comments.
---

# mailsort-devreport

Status reporting for someone who is not writing the code. The entire discipline is **reporting
outcomes, not activity** — commit counts, PR counts and "worked on X" are activity theater, and both
DORA and the SPACE framework name them as the classic failure.

## Three sections, in this order

### 1. What changed
Shipped and merged work only, one line each, linked. Group the way a changelog groups — Added,
Changed, Fixed, Removed, Security — not by commit and never by author. Machines draft this; the
skill curates it. A raw commit log is the canonical bad practice: "changelogs are for humans, not
machines."

### 2. What's blocked
Every blocked item carries three things or it does not belong here:
- **who owns the blocker** (a person, not a team),
- **how long it has been blocked** (age is the escalation signal),
- **what would unblock it** (one concrete condition).

"Blocked on review" is not a status; "blocked 6 days on code review, needs a second approver" is.

### 3. What needs a decision
Scope, schema, spend, and risk calls that only the owner can make. Each with the options and a
recommendation. This section is the reason the report exists — put it last so it is what the reader
leaves with, and surface the same asks in the briefing's BLUF.

## Progress signals that survive contact with reality

- **Uphill / downhill beats percent-done.** Uphill means the unknowns are still being resolved;
  downhill means the work is understood and is being executed. "90% done" for three days running tells
  you nothing; "still uphill on the auth model" tells you everything.
- **Confidence per milestone**, stated plainly: on track / at risk / will miss. Borrowed from async
  status practice — a status update without a confidence call is just a diary.
- **Flow and stability as health signals, never targets.** If reporting delivery metrics (lead time,
  deploy frequency, change-fail rate, recovery time), label them as signals with trend arrows. Never
  rank teams against each other and never set them as goals — measures that become targets get gamed.

## Scope and grouping

One block per active project, ordered by the owner's stated priority — never by activity volume, or
the noisiest repo wins. A project with nothing to report gets one line saying so; silence is
ambiguous between "quiet" and "not checked".

## Anti-patterns

Listing every commit or PR. Reporting bot activity as progress. Repeating yesterday's blockers
verbatim without aging them. Percent-complete with no uncertainty signal. Burying the decision ask at
the bottom of a wall of green checkmarks. Counting a merged PR as an outcome when nothing was
deployed.

## Never

Merge, close, comment, deploy, re-run CI, or change an issue's state. This skill reads and reports.
