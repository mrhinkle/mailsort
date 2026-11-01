---
description: List who is waiting on the owner (Needs Reply) and who the owner is waiting on (Waiting), sorted by age, with stale items flagged
argument-hint: "[mailbox|all] [--days N]"
allowed-tools: Read, Skill
---

Load `mailsort` (resolve the override layer) and `mailsort-needsreply`. Scope: `$ARGUMENTS` mailbox
or all; look back `--days` (default 14). Apply the three-part test per thread, judge the thread not
the message, and produce two lists: **Needs Reply** (who, what they want, waiting how long, tier:
safe-to-draft or needs-you) and **Waiting** (who owes the owner, since when, chase suggested past 5
business days). Mark items past 10 business days `STALE`. Offer `/mailsort:draft` for the
safe-to-draft tier. Do not draft or send here.
