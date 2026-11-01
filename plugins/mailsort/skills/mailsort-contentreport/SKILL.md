---
name: mailsort-contentreport
description: >
  The content-pipeline section of a daily briefing — what publishes today, where each piece is in the
  pipeline, and what is blocking the next ship date. Platform- and tool-neutral (works against any
  content calendar, CMS, or newsletter platform). Part of the `mailsort` family and designed to slot
  into `mailsort-briefing` alongside `mailsort-devreport`. Use when someone asks for a content
  status, editorial pipeline, publishing calendar check, "what ships today", or "what's late". It
  reports status; it never publishes, schedules, or sends anything.
---

# mailsort-contentreport

Content has something engineering status does not: **an unmovable ship date**. A newsletter that goes
out Tuesday goes out Tuesday or it does not go out. That makes the pipeline report a countdown, not a
progress log — and it belongs high in the briefing, above anything that can slip a day without cost.

## Pipeline stages

Track every piece through a fixed ladder, and always name the stage rather than a percentage:

`idea → researched → drafted → reviewed → metadata/art → staged → scheduled → published`

The stage plus the ship date is the whole status. "60% done" two days before a send tells the reader
nothing; "drafted, not reviewed, ships in 26 hours" tells them whether to worry.

## The three questions to answer

1. **What ships today?** Title, channel, send time, current stage. If it is not yet *scheduled*, this
   is the top line of the whole briefing — a piece that ships today and is not staged is the single
   most time-critical thing on the list.
2. **What ships next, and is it on track?** Each upcoming slot with its stage and a plain call: on
   track / at risk / will miss. Base the call on stage-versus-deadline, never on effort spent.
3. **What is blocked and on whom?** Waiting on a quote, an image, an approval, a fact-check, a
   sponsor asset — with the owner's name and how long it has been waiting.

## Recurring slots are the backbone

When publishing runs on a fixed weekly cadence, report the **slots**, not the ideas. Every slot for
the next 7 days appears in the report whether or not anything exists for it yet — an empty Thursday
slot showing "no idea selected" four days out is exactly the warning that gets missed otherwise. A
slot with nothing in it is a red row, not an absent row.

## Countdown, not activity

Order by time-to-publish, soonest first. Each row carries the hours or days remaining. Never order by
recency of edits, and never report activity ("worked on the draft") — the stage already carries that,
more honestly.

## Chase the dependencies, not the writing

The writing is rarely what slips. What slips: an unanswered sponsor email, a missing headshot, an
unapproved subject line, an image still generating, a link that 404s. Pull these forward explicitly —
each one is a one-line ask that unblocks a whole piece, and most of them are sitting unanswered in the
mailbox this briefing is already reading.

## Post-publish, keep it to two numbers

For anything published since the last report: the one metric that drives the next decision (opens,
click rate, or subscriber delta) and its direction against the recent norm. No dashboards, no tables.
Anything deeper belongs in a weekly review, not a morning briefing.

## Never

Publish, schedule, send, or push anything live. Change a ship date. Approve a subject line or an
image on the owner's behalf. Report a piece as ready when only the draft exists.
