---
description: Triage new mail — classify by the mailsort decision order, file what is safe to file, and report only what a human must answer
argument-hint: "[mailbox|all] [--dry-run] [--since <window>]"
allowed-tools: Read, Skill
---

Load the `mailsort` core and resolve the override layer first; say which one you found in the first
line of the report (downstream skill, `~/.claude/mailsort/overrides.md`, or none → generic).

Parse `$ARGUMENTS`: a mailbox alias or address, `all`, `--dry-run`, `--since 24h|3d|<date>`. Default
is every mailbox in the override layer, since the last run or 24 hours.

Run the **Run** steps in `mailsort/SKILL.md`, handing each message to its category subskill
(`mailsort-dontmiss`, `-needsreply`, `-todo`, `-screener`, `-receipts`, `-alerts`, `-news`, `-cc`,
`-later`, `-blackhole`). With `--dry-run`, print the planned writes as a table and apply nothing.
Otherwise batch the writes through the adapter in `references/adapters.md`, then verify every touched
label by re-query and show before/after counts. Report in the `mailsort-briefing` shape: Don't Miss and
Needs Reply one line each, everything else as counts, then genuinely ambiguous items as questions.
Never send, delete, mark spam, or unsubscribe.
