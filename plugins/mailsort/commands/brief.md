---
description: The morning brief — BLUF, today's schedule, mail that can't wait, the priority list; delivered as the run's final message, emailed only if asked
argument-hint: "[--email]"
allowed-tools: Read, Skill
---

Load `mailsort` (resolve the override layer) and `mailsort-briefing`; pull items from
`mailsort-dontmiss`, `mailsort-needsreply` and `mailsort-todo`, and include `mailsort-devreport` /
`mailsort-contentreport` sections only if the override layer enables them. Compose per the briefing
skill: BLUF, typed items (FYI / DECISION REQUIRED / ACTION REQUIRED), at most 7 can't-wait items,
empty states stated, every item deep-linked, stated read time. Deliver as the final message. Email
it only if `$ARGUMENTS` contains `--email`, and only to the owner's own address from the override
layer; never to anyone else.
