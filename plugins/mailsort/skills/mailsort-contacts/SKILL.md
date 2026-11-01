---
name: mailsort-contacts
description: >
  Turns correspondence into a contact record — adds anyone the owner replies to, then enriches the
  entry from signatures and thread context. Provider- and platform-neutral (Google People or
  Microsoft Graph contacts); part of the `mailsort` family. Use when triaging mail, after sending
  replies, or when someone says "add them to my contacts", "enrich my contacts", "who is this
  person", or "build my contact list from email". It writes contact records only — never mail.
---

# mailsort-contacts

The rule: **a reply is an endorsement.** If the owner wrote back to a human, that person belongs in
the address book. This one behavior builds a better CRM in a month than any import.

## Capture

Trigger on outbound mail from the owner. For each human recipient (To and Cc):

1. Skip if the address is a robot (`noreply`, `notifications`, `support+ticket`, bounce addresses),
   a distribution list, or the owner's own address/aliases.
2. Skip if a contact already exists for that address — go to **Enrich** instead.
3. Otherwise `CONTACT_UPSERT` with everything derivable from the thread.

Never add people the owner only *received* mail from. Receiving is not a relationship; replying is.
That single asymmetry is what keeps the address book from filling with strangers.

## Fields to capture

| Field | Source |
|---|---|
| Name | From display name, then signature block, then `firstname.lastname@` pattern |
| Email | Envelope address, lowercased |
| Company | Sender domain (skip free-mail domains), then signature |
| Title | Signature line under the name |
| Phone | Signature — keep the format as written |
| Website / social | Signature links |
| First contact date | Date of the earliest message in the thread |
| Source | `email:<mailbox>` plus the thread subject, so provenance is auditable |

## Enrich

On every later exchange with an existing contact, fill blanks — never overwrite a non-empty field
with a guess. When new data conflicts with old (new title, new company), **append with a date** and
keep the prior value; people change jobs, and the old value is how you recognize the history.

Enrichment sources, in order of trust: the person's own signature → their reply headers → the
company's public site. Do not scrape social profiles or third-party data brokers unless the owner
asks; it is slower, legally muddier, and less accurate than the signature they just sent you.

## Hygiene

- **One person, one record.** Match on email first, then on name+company; merge duplicates by
  keeping the record with the earliest first-contact date and folding the rest in.
- **Tag by relationship**, derived from the mail itself: `customer`, `vendor`, `press`, `speaker`,
  `sponsor`, `personal`. The label the owner's own folders use beats any inference.
- **Never invent** a title, company, or phone number. A blank field is data; a wrong field is damage.
- **Respect privacy**: contacts built this way are the owner's own correspondence. Do not export,
  share, or upload them anywhere the owner did not name.

## Report

After a run: how many contacts added, how many enriched, and any conflicts that need a human call
(same person at two companies, two people at one address). Never more than ten lines.
