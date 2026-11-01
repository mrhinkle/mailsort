---
name: mailsort-cc
description: >
  The "CC" category — mail where the owner is copied rather than addressed. Provider- and
  platform-neutral; part of the `mailsort` family. Use when triaging mail or when someone asks to cut
  down on being copied, wants to know what they were looped into, or asks whether a cc'd thread needs
  them. It files and flags the exceptions; it never replies.
---

# mailsort-cc

Being copied means someone wants the owner to *know*, not to *act*. Treat it as ambient awareness and
get it out of the inbox — but with one important exception below.

## Identify

Owner's address appears in Cc (or Bcc) and not in To. A distribution list in To that includes the
owner counts as Cc for this purpose.

## The exception that matters

Escalate to **Needs Reply** when the owner is cc'd *and* the last inbound message names them with a
direct ask — "adding Alex for the pricing", "Alex can you confirm", "@alex thoughts?". This is how
real requests hide in cc threads, and it is the main reason cc filtering gets abandoned: one missed
ask and people stop trusting it. Scan the last inbound message for the owner's first name, address,
or handle within a sentence containing a request.

## Action

Otherwise `FILE` to CC and archive. Keep the thread intact — if the owner is later added to To, the
thread is reclassified on the next run.

## Patterns worth reporting

- **Serial copiers:** senders who cc the owner on more than ~20 threads a month without ever
  addressing them. Report the count; the fix is a conversation, not a filter.
- **Threads that went quiet** after the owner was added — often a decision waiting on them that
  nobody restated.
- **Threads where the owner is the only external party** — those usually deserve a direct ask.
