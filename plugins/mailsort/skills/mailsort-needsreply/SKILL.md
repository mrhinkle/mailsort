---
name: mailsort-needsreply
description: >
  The "Needs Reply" category — mail where a human being is actually waiting on the owner, plus the
  waiting-on-them mirror. Provider- and platform-neutral; part of the `mailsort` family. Use when
  triaging mail or when someone asks "what needs a reply", "who am I ignoring", "what am I owed", or
  "who's waiting on me". It classifies and can draft; it never sends.
---

# mailsort-needsreply

The category that protects relationships. Getting this wrong in the filing direction is the one
expensive mistake in the whole system.

## The test — all three must hold

1. **A person wrote it.** Fails the machine test in `mailsort` (no `List-*` headers, no bulk
   precedence, not a noreply envelope).
2. **It asks or expects something** — a question, a request, a proposal awaiting yes/no, a document
   to review, a meeting to confirm. Mere information is FYI, not a reply.
3. **The ball is on the owner's side** — the last message in the thread is inbound, and the owner has
   not replied since.

## Strong positive signals

- The owner has replied to that address before (reply history is the best importance signal there is).
- Question marks in the last inbound paragraph.
- A direct address by name in the opening line.
- "let me know", "thoughts?", "can you", "would you", "confirm", "sign", "approve", "by when".
- A calendar invitation awaiting response.

## Not Needs Reply

- The owner already replied after the last inbound message — that is **Waiting**, below.
- Newsletters that end in a question ("what do you think?" to a list of 40,000).
- Automated "reply to this email" from a ticketing robot — that is Alerts.
- Cc-only mail, unless the last inbound explicitly names the owner with an ask.

## The mirror: Waiting

When the **owner** sent the last message and asked for something, categorize the thread as
**Waiting** instead. Then chase it: if there has been no inbound reply after **5 business days**,
surface it as "you are owed a reply" — with the original ask and the date. Most dropped balls are
the owner's own, and nothing else in a mailbox tracks this.

## Aging

Report Needs Reply sorted by **age of the oldest unanswered inbound**, never by arrival time. Include
the wait in the line item: `— waiting 6 days`. Past 10 business days, mark it `STALE` and suggest
either a reply or an explicit decline; silence is itself an answer, and usually the wrong one.

## Draft tiers — what may be drafted unattended

The risk in automated drafting is not a bad draft, it is a **plausible** one: a well-formatted wrong
answer invites a send-without-reading. So drafting is tiered, and the tier is a claim to be measured,
not a truth.

**Safe to draft unattended** — replies that are mostly protocol, where the words are not the deal:
scheduling and confirmations; "got it, looking this week" acknowledgements; routine vendor, receipt
and account questions; speaker/CFP acknowledgements; polite declines to screener senders;
introductions the owner would accept anyway.

**Never draft unattended** — where the words themselves carry the risk: negotiation and pricing;
anything legal, contractual, or in dispute; money owed or disputed; first contact with a VIP;
personal or sensitive matters; and any reply that would commit the owner to a date, a number, or
another person. These get a "needs you" line with a suggested angle instead — a nudge, never a draft.

**Prefer a proposal queue to a live draft.** A draft sitting in the mailbox is one tap from being
sent, from a phone, unread. A proposal the owner approves before it becomes a draft adds a deliberate
step exactly where the risk is. Where the platform supports it, queue the proposal; where it does
not, create the draft but never mark it ready.

**Measure the tier, then move it.** Track per draft whether it was sent unchanged, edited, or
discarded. High "sent unchanged" means the tier can widen. Mostly edited or discarded means drafting
costs more than it saves — narrow the tier, or stop drafting and keep classification. Review after
two weeks of real traffic.

**Watch the queue itself.** A proposal or draft nobody acts on is worse than none: it looks like
progress while the sender waits. Report anything pending more than 72 hours by name and age, every
day, until it is resolved.

## Drafting

Hand the writing to `mailsort-draftreply`. It runs a context check on each thread first — is the
loop still open, what is the history with this sender, what do the calendar and knowledge sources
say — and refuses to draft without it. This skill decides which threads need a reply and which
tier they fall in; that one owns how each draft is researched and written. Never send.
