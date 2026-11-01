---
name: mailsort-news
description: >
  The "News" category — newsletters, digests, industry mail and other subscribed reading. Provider-
  and platform-neutral; part of the `mailsort` family. Use when triaging mail, when someone asks to
  tame newsletters, wants a reading queue, or asks which subscriptions are worth keeping. It files and
  measures; it never unsubscribes without being told.
---

# mailsort-news

Subscribed reading the owner chose once and keeps receiving forever. It is never urgent, which is
exactly why it must never sit in the inbox.

## Identify

`List-Unsubscribe` or `List-Id` present, bulk precedence, or a known publisher domain — and the
content is editorial rather than transactional. A vendor's product announcement is News; that same
vendor's invoice is Receipts and its outage notice is Alerts.

## Action

`FILE` to News and archive, always. Keep unread state intact — unread here means "not yet read",
which is the one place in the mailbox where that flag still means something.

## Measure what is actually read

Track per publication over a rolling 90 days: received, opened, clicked. Then report the honest
version:

- **Zero opens in 90 days** → propose unsubscribing, and list them oldest-first. Say the number:
  "The Information: 61 received, 0 opened."
- **High volume, low opens** → propose the digest/weekly option if the publisher offers one.
- **Read nearly every time** → promote the sender to a `News/Favorites` sub-category so it is easy to
  find. These are not noise, and treating them as noise is why people abandon triage systems.

## Unsubscribing

Only on the owner's say-so, and prefer the `List-Unsubscribe` header (one-click POST or mailto) over
clicking marketing links in the body, which are tracked and sometimes hostile. Report what was
unsubscribed; never unsubscribe silently.

## Never

Treat a person's individual mail as News because it mentions a newsletter, or file a publication the
owner writes or sells — the owner's own publishing is business mail, not reading.
