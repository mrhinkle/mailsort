---
description: Learn reply style from the owner's edits — diff saved drafts against what was actually sent and write dated rules into the audience style files; --bootstrap builds the files from sent mail
argument-hint: "[--bootstrap] [audience]"
allowed-tools: Read, Edit, Write, Bash, Skill
---

Load `mailsort` (resolve the override layer) and `mailsort-replylearn`. Without flags, run its
*Learn* procedure over the open rows of the override layer's draft ledger (optionally only
`$ARGUMENTS`' audience) and report the per-audience table, rules added and stale drafts. With
`--bootstrap`, run its *Bootstrap from sent mail* procedure and write one style file per audience
into the override layer. Never send, edit or delete mail or drafts, and never commit the ledger.
