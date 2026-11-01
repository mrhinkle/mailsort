---
name: mailsort
description: >
  Portable email triage core — the upstream, generic ruleset that sorts any mailbox into a stable
  set of categories (Don't Miss, Needs Reply, To Do, Later, News, Alerts, Receipts, CC, Screener,
  Black Hole), mirroring the SaneBox model but provider- and platform-neutral. Runs on any AI
  platform and against Gmail or Microsoft 365 through a small adapter contract; it never hardcodes a
  vendor API. Routes each message to a nested `mailsort-*` subskill that owns that category. Use this
  skill whenever someone asks to triage, sort, file, or clean up an inbox, set up email rules, build
  an email assistant, or asks "what needs my attention" — and as the upstream any personal or
  company-specific triage skill imports rather than copying. It reads and organizes mail; it never
  sends, replies, deletes, or unsubscribes without the owner saying so in chat.
---

# mailsort — portable triage core

Upstream and generic. Nothing here names a person, company, vendor account, or private address.
Local facts (who the VIPs are, which senders are noise) live in a downstream skill or an overrides
file — see **Overrides**. That split is what lets this be shared, forked, and self-improved.

## The adapter contract

Implement these seven verbs on whatever platform you're running. Everything below is written in terms
of the verbs only, which is why the same rules work on Gmail and Microsoft 365.

| Verb | Gmail | Microsoft 365 / Graph |
|---|---|---|
| `FIND(query)` | `users.messages.list` with `q=` | `/messages?$search=` + `$filter=` |
| `CATEGORIZE(msg, category)` | apply label | apply category, or move to folder |
| `FILE(msg, category)` | apply label + remove `INBOX` | move to folder under the triage root |
| `FLAG(msg)` / `UNFLAG` | star | flag |
| `READ_STATE(msg, read?)` | add/remove `UNREAD` | set `isRead` |
| `CONTACT_UPSERT(person)` | People API | Graph `/contacts` |
| `DRAFT(thread, body)` | `drafts.create` | Graph `createReply` (saved, not sent) |

Rules: batch writes where the API allows; verify by re-querying rather than trusting a write
response; never call a verb not on this list. There is deliberately no `SEND` and no `DELETE`.

**Drafting is allowed; sending never is.** `DRAFT` saves a reply for the owner to review — it is not
a deferred send. Leave every factual unknown as `[TK]` rather than inventing a date, price, or
commitment. The owner sends, and only when they say so explicitly in that moment; prior permission to
draft is never permission to send.

## Categories

Ten, in priority order. First match wins; a message gets exactly one primary category.

| Category | Means | Owner subskill |
|---|---|---|
| **Don't Miss** | would be costly to miss: named VIP, money, legal, deadline, or a thread the owner started | `mailsort-dontmiss` |
| **Needs Reply** | a human is waiting on a reply from the owner | `mailsort-needsreply` |
| **To Do** | action required, but not a reply | `mailsort-todo` |
| **Screener** | first contact from an unknown sender — decide once, then remember | `mailsort-screener` |
| **Receipts** | payment, invoice, order, statement — proof, not action | `mailsort-receipts` |
| **Alerts** | machine-generated system/service notification | `mailsort-alerts` |
| **News** | newsletters, digests, subscribed reading | `mailsort-news` |
| **CC** | owner is copied, not addressed | `mailsort-cc` |
| **Later** | real mail, low priority, batch it | `mailsort-later` |
| **Black Hole** | sender the owner never wants to hear from again | `mailsort-blackhole` |

## Decision order

Run top-down; stop at the first match. Order matters more than any individual rule.

1. **Sender on the Black Hole list** → Black Hole. No further tests.
2. **Sender/domain on the VIP list, or subject matches a money/legal/deadline pattern** → Don't Miss.
3. **Owner is not in To/Cc (bulk headers present)** → News, Alerts or Receipts by the subskill tests.
4. **A human wrote it AND it asks or expects something AND the owner has replied to that address
   before** → Needs Reply.
5. **Owner addressed to himself** → To Do. (Self-addressed mail is task capture, not correspondence.)
6. **Owner in Cc but not To** → CC.
7. **Unknown human sender, no prior thread** → Screener.
8. **Anything left** → Later.

### Machine-vs-human test

Treat as machine-generated when any hold: `List-Unsubscribe` or `List-Id` header present;
`Auto-Submitted` not `no`; `Precedence: bulk|list|junk`; envelope sender is `noreply|no-reply|
donotreply|notifications?|alerts?|mailer|bounce`. **Never** classify on the display name alone —
vendors put human names on robots.

### The one expensive mistake

Over-filing a real person who is waiting. Every other error costs a few seconds of scrolling. When a
message is genuinely ambiguous, leave it in the inbox and list it for the owner. Under-filing is
recoverable; a missed customer is not.

## Anti-rules (learned the hard way)

- **Unread is not a queue.** Many people reach inbox zero by filtering, never by reading, so unread
  counts run to five and six figures while the inbox holds twenty items. Decide from category,
  sender and thread — never from the unread flag, and never report an unread count as a backlog.
- **Don't invent a taxonomy.** If the mailbox already has working labels/folders, adopt those names
  and map them to these categories. Ten new labels beside ten old ones is a worse inbox.
- **Don't touch labels another tool owns** (SaneBox `@Sane*`, Superhuman, Meco, vendor add-ins).
  Read them, don't write them.
- **Volume is not importance.** The loudest sender is usually the least important.

## Self-improvement protocol

This skill is meant to be corrected, and corrections are the point.

1. **Watch for reversals.** When the owner moves a message out of the category you chose, that is a
   labelled training example. Ask once: "what made that one different?"
2. **Write the rule, not the instance.** Append to `overrides.md` as
   `YYYY-MM-DD | signal → category | why`. A rule that names one message is worthless; a rule that
   names the signal generalizes.
3. **Promote upward.** A rule that holds for any mailbox belongs in this file. A rule true only of
   this owner stays in `overrides.md`. Never put a person's name or address in this file.
4. **Prefer a check to a paragraph.** If a rule can be expressed as a header test or query, write it
   that way — prose degrades, tests don't.
5. **Review on a cadence.** Monthly: count corrections per category. The category with the most
   corrections has the weakest rule — fix that one first, and record what changed.

## Overrides

Private facts never live in this file. They live in exactly one of these places, checked in order:

1. **A downstream skill that declares itself the override layer** — a personal or company skill
   whose header says `mailsort override layer: yes`. If one is loaded, use it and name it in the report.
2. **`~/.claude/mailsort/overrides.md`** — a file outside the plugin, so plugin updates never
   overwrite it. Create it from `overrides.example.md` (next to this file) or run `/mailsort:setup`.
3. **Neither** — run generically and say so in the first line of the report. Never guess at a VIP.

The override layer holds: mailbox list and per-mailbox policy, the mailbox's real label/folder names
mapped to the ten categories, the VIP list, known correspondents, the Black Hole list,
aggregate-only senders, tools that own labels, and the append-only dated learned-rules log.

## Fast path

Installed as a plugin, the family is driven by slash commands: `/mailsort:help` (menu),
`/mailsort:setup`, `/mailsort:triage`, `/mailsort:needsreply`, `/mailsort:draft`, `/mailsort:brief`,
`/mailsort:sweep`, `/mailsort:rules`. Each command loads the right subskill and this core.

## Run

1. Confirm mailbox(es), provider, and window (default: since last run, else 24h).
2. Resolve the override layer (see **Overrides**) and say which one you found.
3. `FIND` new mail; classify by the decision order; hand each message to its subskill for the
   category-specific test and action.
4. Batch the writes. Verify by re-query.
5. Report: **Don't Miss** and **Needs Reply** itemized one line each (who, what they want, how long
   they have waited); everything else as counts only. Then ask about anything genuinely ambiguous.
