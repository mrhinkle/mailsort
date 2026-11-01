# mailsort overrides — TEMPLATE (copy to overrides.md; never commit real values upstream)

Everything private lives here. The `mailsort*` skills stay generic and shareable; this file is what
makes them yours. Load it before classifying.

mailsort override layer: yes

## Mailboxes
| Alias | Address | Provider | Path | Account id | Policy |
|---|---|---|---|---|---|
| work | you@example.com | gmail | composio | gmail_xxxx-xxxx | full triage |
| personal | you@example.net | m365 | native | — | aggressive auto-file |

Path is `composio` (recommended) or `native`; see `references/adapters.md`. Account id is the
connected-account id to pass on every write. Policy is one of: full triage, file only, aggressive
auto-file, report only.

## Briefing sections enabled
`devreport: no` · `contentreport: no` · `email delivery: ask` (never default to sending)

## Label / folder names actually used in this mailbox
Map the categories to names that already exist. Do not create parallel labels.
| Category | This mailbox calls it |
|---|---|
| Don't Miss | |
| Needs Reply | |
| To Do | |
| Later | |
| News | |
| Alerts | |
| Receipts | |
| CC | |
| Screener | |
| Black Hole | |

## VIP list (drives Don't Miss)
addresses, domains, and why — e.g. `counsel@firm.com — attorney, statutory clocks`

## Known correspondents (drives Needs Reply)
addresses the owner has replied to before

## Black Hole list
address/domain | date | reason

## Aggregate-only senders (count, never list)
signup notifications, ticket sales, CI, vendor alerts

## Tools that own labels here — read, never write
e.g. SaneBox `@Sane*`, Superhuman `[Superhuman]/*`, Meco, vendor add-ins

## Learned rules (append-only)
`YYYY-MM-DD | signal → category | why`
