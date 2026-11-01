# Lessons log — the plugin's memory

This file is how `mailsort` gets better for everyone, not just for the person who hit the problem.
It is **generic by rule**: nothing here names a person, address, label id, account id or company.
Those facts belong in your overrides layer (`~/.claude/mailsort/overrides.md` or a downstream skill
that declares `mailsort override layer: yes`), which has its own dated log.

**How to use it**

1. Read this file before a run. It is short on purpose.
2. After the owner corrects a classification or a draft, write the *rule*, not the instance:
   `YYYY-MM-DD | signal → rule | why`. If it can be a header test or a query, write it that way.
3. Keep it in your overrides log first. When the same rule would hold on a stranger's mailbox,
   move it here and open a pull request — that is the promotion step in the core skill's
   self-improvement protocol.
4. Monthly, count entries per section. The section growing fastest has the weakest rule in the
   skill that owns it; fix that skill and note the change here.

Sections mirror the skills. Newest entry last within a section.

## Core triage

- 2026-11-01 | connector default account changed between runs → list connections first and pass an
  explicit account on every call | a bare call silently hit a different mailbox
- 2026-11-01 | the same label name maps to a different id in each mailbox, and ids drift when a
  label is deleted and recreated → re-list labels every run, never hardcode | a cached id filed
  mail under the wrong label for weeks
- 2026-11-01 | "clear my inbox" means archive closed, handled, machine and promotional threads and
  leave every open human ask where it is → done is "only actionable mail remains", not zero | the
  owner's own hard rule is that over-filing a waiting person is the one expensive mistake
- 2026-11-01 | thread whose last message is the owner's or a named delegate's → Waiting + archive |
  the ball is in the other party's court; the inbox is for the owner's moves
- 2026-11-01 | a reader replying to the owner's own newsletter is a human even when the message
  carries the newsletter's bulk label → Needs Reply, never aggregate | the label is for signups,
  replies ride under it
- 2026-11-01 | fetching thread state at scale: pull every thread behind the inbox and the drafts in
  one parallel pass (12 workers ≈ 150 threads in ~10 s), then classify offline | one call per
  thread in series blows the step timeout

## Draft audit (`mailsort-draftreply`)

- 2026-11-01 | draft whose thread has a later SENT message from the owner or a delegate →
  SUPERSEDED; propose deletion, never delete | writing into a closed loop replies twice
- 2026-11-01 | draft whose body, after stripping the signature block and any quoted header, is
  under ~25 characters → EMPTY leftover (reply clicked, nothing written) | these are the most
  common stale draft; they look like pending work
- 2026-11-01 | two or more drafts on one thread → keep the newest one with a body, propose the rest
- 2026-11-01 | same recipient drafted from two mailboxes → keep the one in the mailbox that owns
  the relationship (overrides say which), propose the other
- 2026-11-01 | draft carrying another tool's marker (a generated-body attribute, a rewrite id
  prefix) → report, never edit or delete | two writers on one draft collide
- 2026-11-01 | trashed drafts still appear in a thread fetch with `DRAFT` + `TRASH` → a thread has
  a live draft only when a `DRAFT` message lacks `TRASH` | otherwise you skip a thread that needs
  a reply because "it already has a draft"
- 2026-11-01 | a same-day batch of drafts awaiting approval that is more than 7 days old → report
  as one batch with its age; do not re-draft any of them | stale drafts look like progress
- 2026-11-01 | deleting a draft is the owner's action, done in the mail client → the agent's
  deliverable is a list with compose links, grouped by reason | there is no DELETE verb in the
  adapter contract, and there should not be

## Standing rules

- 2026-11-01 | a form submission that fits an approved template but adds one extra question →
  draft the template, flag the extra question for the owner; never invent the answer
- 2026-11-01 | a form type with no rule → propose a rule row with status draft instead of drafting
  ad hoc | ad hoc drafts are not auditable and never become a rule

## Multiple runs per day

- 2026-11-01 | before creating any draft, read the shared memory (or the log) for runs earlier the
  same day → a thread an earlier run flagged for the owner is never drafted by a later run | two
  runs disagreed on a form whose sender domain did not match its name; the second one drafted it
