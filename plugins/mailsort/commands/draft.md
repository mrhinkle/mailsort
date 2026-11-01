---
description: Draft context-checked replies for threads that need one — stop checks, context lookups, sourced facts, saved to Drafts, never sent
argument-hint: "[thread id | sender | all]"
allowed-tools: Read, Skill
---

Load `mailsort` (resolve the override layer), `mailsort-needsreply` (to pick threads and tiers)
and `mailsort-draftreply` (to research and write). Target: `$ARGUMENTS` — a thread id, a sender,
or `all` for the current safe-to-draft tier. For each thread run stop checks S1–S7, then context
checks C1–C7 against the sources listed in the override layer, then write the draft with every fact
sourced or left as `[TK: question]`. Save through the adapter `DRAFT` verb and read it back. Output one
context card per thread: DRAFTED / NEEDS YOU / SKIPPED, with the reason. Never send, schedule, or mark
a draft ready.
