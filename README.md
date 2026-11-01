# mailsort

A portable, provider-neutral email triage plugin for Claude Code and Cowork. Works against Gmail
and Microsoft 365. Sorts any inbox into ten stable categories, surfaces only what a human must
answer, drafts context-checked replies, briefs you each morning, sweeps backlogs, and exports your
learned rules as client-side filters.

**It reads and organizes mail. It never sends, deletes, marks spam, or unsubscribes unless you say
so in chat.** Drafting is allowed; sending is yours.

## Install

```
claude plugin marketplace add mrhinkle/mailsort
claude plugin install mailsort@mailsort
```

Then connect a mailbox. **Composio is the recommended connectivity layer** (one managed OAuth per
mailbox, write scope on Gmail and Outlook, batch operations):

```
claude plugin marketplace add https://github.com/ComposioHQ/composio-plugin-cc.git
claude plugin install composio@composio
/composio-connect gmail      # or: /composio-connect outlook
```

Native connectors (the Claude Gmail connector, a Microsoft 365 connector, a Google Workspace MCP)
also work, with the limits listed in
[`references/adapters.md`](plugins/mailsort/skills/mailsort/references/adapters.md).

## First run

```
/mailsort:help      # menu: what it does, what each command runs
/mailsort:setup     # detect connection, map your existing labels, write overrides, dry-run 50 messages
/mailsort:triage --dry-run
/mailsort:triage
```

Your private facts (mailboxes, VIPs, label names, learned rules) live in
`~/.claude/mailsort/overrides.md`, outside the plugin, so updates never overwrite them. Teams can
instead ship a private plugin whose skill declares `mailsort override layer: yes`.

## Commands

| Command | Does |
|---|---|
| `/mailsort:help` | Menu-driven guide; reply with a number to run an action |
| `/mailsort:setup` | First-run onboarding |
| `/mailsort:triage [mailbox\|all] [--dry-run]` | Classify new mail, file what is safe, report what needs you |
| `/mailsort:needsreply [mailbox]` | Who is waiting on you, who you are waiting on, stale items flagged |
| `/mailsort:draft [thread\|all]` | Context-checked reply drafts, saved to Drafts, never sent |
| `/mailsort:brief [--email]` | Morning brief: BLUF, schedule, can't-wait mail, priorities |
| `/mailsort:sweep <mode> [mailbox]` | Backlog cleanup in bulk with before/after counts |
| `/mailsort:rules [gmail\|outlook]` | Export learned rules as an importable filter file |

## The ten categories

Don't Miss · Needs Reply · To Do · Screener · Receipts · Alerts · News · CC · Later · Black Hole.
First match in that priority order wins. Each category is its own skill (`mailsort-dontmiss`,
`mailsort-needsreply`, …) with the test, the action, and the anti-rules for that class of mail.

Three ideas carry the design:

- **Unread is not a queue.** Categories, sender, and reply history decide; unread counts are never
  reported as a backlog.
- **Adopt the labels you already have.** Setup maps your existing names onto the categories rather
  than adding ten new labels beside ten old ones.
- **The one expensive mistake is over-filing a real person who is waiting.** When in doubt, the
  message stays in the inbox and shows up in the report.

## Self-improving

Every correction you make becomes a dated rule in your overrides (`signal → category | why`), never
a one-off exception. Rules that would hold for anyone's mailbox are candidates for this repo; open a
PR.

## Layout

```
plugins/mailsort/
  skills/mailsort/            core: adapter contract, categories, decision order, overrides
  skills/mailsort-*/          one skill per category, plus draftreply, briefing, devreport,
                              contentreport, contacts, setup, rules, sweep
  commands/                   the eight slash commands
```

MIT. Built by [Mark R. Hinkle](https://github.com/mrhinkle).
