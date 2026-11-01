---
name: mailsort-setup
description: >
  First-run onboarding for the mailsort family — detect which mailbox connections exist (Composio
  recommended; native Gmail or Microsoft 365 connectors supported), list the labels or folders the
  mailbox already uses, map them to the ten mailsort categories without inventing a parallel
  taxonomy, create missing labels only with consent, write the owner's overrides file, and dry-run
  the last 50 inbox messages so the owner can correct the first classifications. Use when someone
  installs mailsort, says "set up mailsort", "connect my inbox", "map my labels", "start triaging my
  email", or when a triage run reports it found no override layer. Reads and writes labels and the
  overrides file only; never sends, deletes, or asks for a password or token in chat.
---

# mailsort-setup

Setup is one conversation that ends with a working override layer. Every later run depends on the
facts gathered here, so the order matters: connection, then vocabulary, then people, then a dry run.

## 1. Find the connection

1. Through the Composio MCP, list connections (`COMPOSIO_MANAGE_CONNECTIONS`, `action: "list"`).
   Collect every ACTIVE Gmail and Outlook connection with its account id and address.
2. If none, check for a native connector (a Gmail or Microsoft 365 MCP tool set in the session).
3. If still none: stop. Say which to add (recommended: install the `composio` plugin and run
   `/composio-connect gmail` or `/composio-connect outlook`) and that setup resumes after. Never ask
   for credentials in chat and never type a password.
4. Record for each mailbox: alias, address, provider, path (`composio` or `native`), account id.
   Ask the owner one question: **which policy per mailbox** — full triage, file only, aggressive
   auto-file, or report only. Explain each in one line.

## 2. Adopt the vocabulary that already exists

1. List labels (`GMAIL_LIST_LABELS`) or folders (`OUTLOOK_LIST_MAIL_FOLDERS`).
2. Propose a mapping from the ten categories to **existing** names. Match on meaning, not spelling:
   a label called "Reply", "Respond", "Action" maps to Needs Reply; "Reading", "Newsletters" to News;
   "Receipts", "Orders", "Finance" to Receipts. Show the table with blanks where nothing fits.
3. For each blank, ask: create a new label with the category name, or leave the category unused
   (messages fall through to Later). Create only after a yes, one `GMAIL_CREATE_LABEL` per label, then
   re-list to capture the ids.
4. Note labels owned by other tools (SaneBox `@Sane*`, Superhuman, Meco, vendor add-ins). They go in
   the "read, never write" list.

## 3. People

1. **Known correspondents:** `FIND` the owner's sent mail for the last 90 days; the set of To
   addresses is the known-correspondent list. Show the top 20 by count and ask if any should be VIP.
2. **VIP list:** ask for the people whose mail must never be filed (family, counsel, key clients,
   the boss). Addresses or domains, with a one-word reason each.
3. **Aggregate-only senders:** from the last 14 days, the senders with the highest volume that fail
   the machine-vs-human test. Propose them as count-only; the owner strikes any that matter
   individually.
4. Black Hole starts empty unless the owner names senders.

## 4. Write the override layer

If a downstream skill already declares `mailsort override layer: yes`, do not write a file; report
that the skill is the layer and offer the gathered facts as a diff for the owner to paste in.
Otherwise write `~/.claude/mailsort/overrides.md` from `overrides.example.md` with every section
filled from steps 1–3, and the first learned-rules line: `YYYY-MM-DD | setup | initial mapping`.

## 5. Dry run

1. `FIND` the last 50 inbox messages in the primary mailbox.
2. Classify with the `mailsort` decision order. Apply nothing.
3. Print a table: sender, subject (truncated), category, the one rule that decided it.
4. Ask for corrections. Each correction becomes a dated learned rule written as the signal, not the
   instance ("`List-Id` from vendor X → Alerts", never "this one message").
5. Finish: "Next: `/mailsort:triage --dry-run`, then `/mailsort:triage`."

## Anti-rules

- Never create ten new labels beside ten old ones.
- Never mark anything read, archive anything, or send anything during setup.
- Never guess a VIP. An empty VIP list is honest; a wrong one files a real person.
