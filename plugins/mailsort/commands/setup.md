---
description: First-run setup for mailsort — detect the mailbox connection, map existing labels to the ten categories, write the overrides file, dry-run 50 messages
argument-hint: "[mailbox address]"
allowed-tools: Read, Write, Edit, Bash, Skill
---

Load the `mailsort-setup` skill and the `mailsort` core, then run setup for `$ARGUMENTS` (if
empty, ask which mailbox). Follow the skill's steps in order. Create labels or folders only after
the owner says yes in chat. Write the overrides file to `~/.claude/mailsort/overrides.md` unless a
downstream skill already declares itself the override layer, in which case report that and skip the
file. Finish with the dry-run classification table and the line "Next: /mailsort:triage".
