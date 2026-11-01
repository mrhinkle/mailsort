---
name: mailsort-todo
description: >
  The "To Do" category — mail that requires an action but not a reply, including the owner's own
  self-addressed notes. Provider- and platform-neutral; part of the `mailsort` family. Use when
  triaging mail, when someone asks "what do I owe", "what's on my plate from email", or wants tasks
  extracted from a mailbox. It extracts and tracks; it never completes tasks on the owner's behalf.
---

# mailsort-todo

Action without correspondence. The distinction from Needs Reply is who is waiting: nobody is waiting
on a To Do, so it will rot silently unless it is tracked.

## Identify

- **Self-addressed mail.** Many people email themselves as task capture — treat every self-addressed
  message as a To Do, using the subject as the task. This is one of the highest-signal rules in the
  whole system and is almost always missed.
- A form, document, or renewal the owner must complete, with no human awaiting a response.
- A commitment the owner made in their own outbound mail ("I'll send that Friday") — extract it.
- An event requiring registration or travel action.

## Extract a task, not a message

Each To Do gets: the verb, the object, the due date if stated, and a link back to the source message.
`Sign the vendor engagement letter — due Fri Oct 3 — [thread]`. A category full of subject lines is
not a task list.

## Deadlines

Parse dates from the body and rank by them. Undated To Dos sink and die, so give anything without a
date an explicit review date 7 days out, and say that is what you did.

## Report

Sorted by deadline, then age. Include what was completed since the last run (detectable when the
owner replied, paid, or the thread closed) — visible progress is what keeps the category trusted.

## Never

Complete the action, submit a form, make a payment, or accept an invitation. Extract and present.
