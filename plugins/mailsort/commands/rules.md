---
description: Export learned triage rules as an importable client-side filter file (Gmail filter XML or Outlook rules JSON) so routing happens before the agent runs
argument-hint: "[gmail | outlook] [--out <path>]"
allowed-tools: Read, Write, Skill
---

Load `mailsort` (resolve the override layer) and `mailsort-rules`. Provider: `$ARGUMENTS`, else
the provider recorded for the mailbox in the override layer. Compile the Black Hole list,
aggregate-only senders, Alerts sources and stable learned rules into filters per the skill, write the
file to `--out` (default `~/.claude/mailsort/exports/<mailbox>-filters.<xml|json>`), and print the
import instructions plus a table of which rules moved client-side. Never create filters or rules
directly, even if a connector could; the owner imports the file.
