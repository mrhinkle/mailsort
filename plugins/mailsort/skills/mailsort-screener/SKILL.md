---
name: mailsort-screener
description: >
  The "Screener" — first contact from an unknown sender, decided once and then remembered forever.
  Provider- and platform-neutral; part of the `mailsort` family. Use when triaging mail, when someone
  asks about cold outreach, pitches, or strangers in the inbox, or when setting up a gate for new
  senders. It classifies and proposes; the owner makes the keep-or-block call.
---

# mailsort-screener

Borrowed from the best idea in modern mail: **a stranger gets one decision, not one decision per
message.** Every sender the owner has never corresponded with lands here exactly once.

## Identify

No prior thread with that address, the owner has never replied to it, and it is not already
categorized by another rule (a first-time receipt is a Receipt, a first-time CI alert is an Alert).

## Sort the strangers

1. **Person writing personally** — mentions specifics only a human who did the reading would know:
   the owner's work by name, a mutual contact, a talk they gave, a specific article. Propose
   **Accept**; these are how opportunities arrive.
2. **Templated outreach** — merge-field phrasing ("Hi {First}, I came across your"), a pitch in
   paragraph one, a calendar link, an unsubscribe footer on a "personal" note. Propose **Later** on
   first contact and **Black Hole** on the third from the same company.
3. **Bulk enrollment** — the owner was added to a list they never joined. Propose **Black Hole**.

## Decide once, remember forever

Every decision writes a sender rule to `overrides.md` — `accepted`, `later`, or `blocked`, with the
date and one-line reason. The screener must never ask about the same sender twice; a screener that
re-asks is worse than no screener, because it adds a decision without removing one.

## Report

Batch screener decisions into a single ask — a numbered list of new senders, each with one line of
context and a proposed disposition, so the owner answers ten at once. Never interrupt per message.

## Never

Auto-block a first contact from a human, auto-reply to strangers, or let a screener decision override
Don't Miss — a first-time sender can still be a lawyer or a bank.
