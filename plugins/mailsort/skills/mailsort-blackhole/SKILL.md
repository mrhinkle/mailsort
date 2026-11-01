---
name: mailsort-blackhole
description: >
  The "Black Hole" — senders the owner never wants to see again, filed out of sight but never
  deleted. Provider- and platform-neutral; part of the `mailsort` family. Use when triaging mail, when
  someone says "never show me this again", "block this sender", or wants to purge persistent noise.
  It files and remembers; it never deletes mail or reports senders as spam.
---

# mailsort-blackhole

The relief valve. Its value is that it is **cheap to add to and reversible**, which is what makes an
owner willing to use it instead of tolerating noise.

## Add a sender when

- The owner says so — always sufficient, no other test.
- Third templated pitch from the same company after two Later dispositions.
- A list the owner never joined that ignores unsubscribes.
- A sender whose mail has gone unread for 90+ days at volume.

## Action

`FILE` to Black Hole and archive. **Never delete, never mark as spam.** Deleting loses evidence;
marking spam damages a sender's deliverability globally and can misfire on legitimate business.
Filing is enough — the owner stops seeing it, and it remains findable by search.

## Scope carefully

Block the **address** by default, the **domain** only when every address at that domain is noise.
Blocking a domain that also carries invoices or a real account manager is the classic own-goal here.
Check for prior correspondence with any address at that domain before a domain-level block.

## Review

Quarterly, list what the Black Hole caught and its volume. Two useful signals fall out: senders worth
a real unsubscribe instead (it stops the mail at the source), and mistakes — anything the owner
searched for and found here was wrongly blocked. Remove it and record why.
