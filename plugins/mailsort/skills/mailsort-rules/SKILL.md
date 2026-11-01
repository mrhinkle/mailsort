---
name: mailsort-rules
description: >
  Compile the owner's stable triage rules (Black Hole list, aggregate-only senders, Alerts sources,
  dated learned rules that have held for 30+ days) into an importable client-side filter file —
  Gmail filter XML for Settings → Filters → Import, or Microsoft 365 rules as a human table plus
  Graph messageRules JSON — so routing happens in the mail client before any agent runs and the
  agent only triages the residue. Part of the `mailsort` family. Use when someone asks to "export
  my rules", "make Gmail filters from this", "move routing client-side", "set up Outlook rules",
  "stop the agent re-filing the same senders", or when a connector cannot create filters (Gmail
  filter creation needs a settings scope most OAuth apps lack). It writes a file and prints import
  steps; it never creates filters or rules directly.
---

# mailsort-rules

A rule the agent applies every morning is a rule the mail client could have applied at delivery.
Moving stable rules client-side is the cheapest speed-up in the system: less for the agent to read,
and routing that keeps working when no agent runs.

## What qualifies as stable

Export only rules that are safe without judgment. A rule qualifies when it is one of:

- A **Black Hole** entry (address or domain) → label Black Hole, archive, mark read.
- An **aggregate-only sender** → its count-only label, archive.
- An **Alerts source** that passes the machine test on headers alone (`List-Id`, a `noreply`
  envelope) → `Alerts/<Service>`, archive.
- A **News** sender with a `List-Unsubscribe` header the owner has kept for 90+ days → News label,
  leave unread.
- A **learned rule** in the override layer dated 30+ days ago whose signal is a header, sender, or
  exact subject token — not prose.

Never export: anything that depends on reply history, thread state, the VIP list, or "a human asked
something". Those need the agent. Never export a rule that deletes or marks spam.

## Compile

0. **List what already exists** (`GMAIL_LIST_FILTERS` on Gmail, `/me/mailFolders/inbox/messageRules`
   on Graph; both are read-only). Skip any candidate the client already routes, and note filters
   that label without archiving when the owner's policy is to archive. This call also tells you
   whether the connection has the settings scope at all.
1. Load the override layer. Collect candidates by the tests above.
2. Collapse duplicates: several addresses on one domain with the same action become one domain
   rule only if every sender on that domain has the same category; otherwise keep them separate.
3. Resolve each rule's target label to the mailbox's real label name (Gmail filters reference
   names, not ids). For Outlook, resolve to a folder id with `OUTLOOK_LIST_MAIL_FOLDERS`.
4. Order: Black Hole first, then Alerts, then aggregate-only, then News, then learned rules.

## Gmail output — `mailFilters.xml`

Gmail imports an Atom feed of filter entries. One `<entry>` per rule. Properties Gmail honors:
`from`, `to`, `subject`, `hasTheWord`, `doesNotHaveTheWord`, `label`, `shouldArchive`,
`shouldMarkAsRead`, `shouldNeverSpam`, `shouldAlwaysMarkAsImportant`, `shouldStar`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:apps="http://schemas.google.com/apps/2006">
  <title>Mail Filters</title>
  <entry>
    <category term="filter"/>
    <title>Mail Filter</title>
    <content/>
    <apps:property name="from" value="alerts@service.example"/>
    <apps:property name="label" value="Alerts/Service"/>
    <apps:property name="shouldArchive" value="true"/>
    <apps:property name="shouldMarkAsRead" value="false"/>
  </entry>
</feed>
```

Rules: a domain match is `from` = `@domain.example` (Gmail treats it as a substring); multiple
addresses in one rule are joined with ` OR ` inside `from`; nested labels use `/`; a label that does
not exist yet is created on import, so say which labels are new. Escape `&`, `<`, `>` in values.

Import steps to print: Gmail → Settings → See all settings → Filters and Blocked Addresses →
Import filters → choose file → Open file → tick the filters → Create filters. Offer the checkbox
"Apply new filters to matching conversations" as the owner's choice; it is a bulk backfill.

## Microsoft 365 output

Two artifacts, same rules:

1. A **human table** (name, condition, action) the owner can enter in Outlook → Settings → Mail →
   Rules, for people who prefer the UI.
2. A **Graph JSON array**, one `messageRule` body per rule, for `POST
   /me/mailFolders/inbox/messageRules`:

```json
{
  "displayName": "mailsort: Alerts/Service",
  "sequence": 10,
  "isEnabled": true,
  "conditions": { "senderContains": ["alerts@service.example"] },
  "actions": { "moveToFolder": "<folder-id>", "markAsRead": true, "stopProcessingRules": true }
}
```

Use `fromAddresses` for exact senders, `senderContains` for domains, `subjectContains` for subject
tokens, `headerContains` for `List-Id`. The owner (or an agent with `MailboxSettings.ReadWrite`)
posts them; this skill does not.

## Output and report

- Write to `~/.claude/mailsort/exports/<mailbox-alias>-filters.<xml|json>` (and `.md` for the
  Outlook table) unless `--out` is given. Overwrite only after showing the previous file's date.
- Print: number of rules exported by category, the labels that will be created on import, and the
  rules **not** exported because they need judgment (so the owner knows what the agent still does).
- Append to the override layer's learned rules: `YYYY-MM-DD | rules exported: N | client-side`.
- After the owner imports, the next `/mailsort:triage` should see those senders already filed;
  if it still sees them in the inbox, say so — the import did not take.
