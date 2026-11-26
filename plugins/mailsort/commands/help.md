---
description: Menu-driven guide to the mailsort plugin — what it does, what each command runs, and a numbered menu to pick from
argument-hint: "[topic: categories | commands | safety | setup | adapters]"
allowed-tools: Read, Skill
---

Load the `mailsort` skill (read `SKILL.md` only; do not triage anything).

If `$ARGUMENTS` names a topic, answer that topic only, in under 25 lines, then show the menu.
Otherwise present this, in this order, with no preamble:

**What mailsort does, in three lines.** It sorts a Gmail or Microsoft 365 inbox into ten stable
categories, surfaces only what a human must answer, and can draft replies, brief you each morning,
sweep a backlog, and export filter rules. It never sends, deletes, marks spam, or unsubscribes unless
you say so in chat. Unread is not a queue; categories and reply history decide.

**Menu.** Number each line exactly as below and end with "Reply with a number, or type the command."

1. `/mailsort:setup` — first run: connect a mailbox, map your existing labels, write your overrides, dry-run 50 messages.
2. `/mailsort:triage [mailbox|all] [--dry-run]` — sort new mail since the last run and report what needs you.
3. `/mailsort:needsreply [mailbox]` — who is waiting on you, and who you are waiting on.
4. `/mailsort:draft [thread|all]` — context-checked reply drafts, saved to Drafts, never sent.
5. `/mailsort:brief` — the morning brief: schedule, can't-wait mail, priority list.
6. `/mailsort:sweep <dead-archive|by-sender|digests> [mailbox]` — backlog cleanup in bulk, with before/after counts.
7. `/mailsort:rules [gmail|outlook]` — export your learned rules as an importable filter file so routing happens client-side.
8. `/mailsort:learn [--bootstrap]` — learn your reply style from the edits you make to drafts; `--bootstrap` builds style files from your sent mail.
9. Categories — explain the ten categories and the decision order.
10. Safety — what mailsort will never do, and why drafting is allowed but sending is not.
11. Adapters — Composio (recommended) versus native connectors, and what each can write.

When the user replies with a number 1–8, run that command with no arguments (ask for a mailbox only
if the override layer lists more than one). For 9–11, answer from `SKILL.md` and
`references/adapters.md` in under 25 lines, then show the menu again.
