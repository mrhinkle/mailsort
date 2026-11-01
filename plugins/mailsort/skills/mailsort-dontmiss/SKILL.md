---
name: mailsort-dontmiss
description: >
  The "Don't Miss" category and its daily digest — the small set of messages it would be expensive to
  miss: named VIPs, money, legal, deadlines, security, and replies on threads the owner started.
  Provider- and platform-neutral; part of the `mailsort` family. Use when triaging mail, when someone
  asks "what can't I miss today", "anything urgent", "what did I miss", or when building a daily
  must-see digest. It surfaces and flags; it never replies or deletes.
---

# mailsort-dontmiss

The highest-cost category. Everything else is a filing decision; this one is a **miss** decision.
Err toward including — a false positive costs one line in a digest, a false negative costs a deal, a
deadline, or a compromised account.

## Include when any of these hold

1. **Named VIP** — sender address or domain is on the VIP list in `overrides.md`.
2. **Money in motion** — invoice due, payment failed, chargeback, wire/ACH detail, refund, contract,
   renewal or cancellation notice. Bills that are merely *paid* are Receipts, not Don't Miss;
   **failed** payments are always Don't Miss.
3. **Legal or compliance** — attorney, court, regulator, tax authority, subpoena, notice of claim,
   anything with a statutory clock.
4. **Security** — credential/token created, OAuth app added, MFA changed, new device, breach
   notification, domain or DNS change, expiring certificate. These arrive from robots and would
   otherwise be filed as Alerts; this rule outranks the machine test.
5. **A stated deadline inside the horizon** — "by Friday", "expires in 3 days", "final notice",
   "respond by". Parse the date; if it falls within 7 days, it qualifies.
6. **Reply on a thread the owner started** — the owner opened the conversation, so a reply is owed
   back to them.
7. **Escalation language from a known correspondent** — "second attempt", "following up again",
   "still waiting", "are you there".

## Exclude — these masquerade as urgent

- Marketing urgency: "act now", "last chance", "24 hours only" from a bulk sender. The
  `List-Unsubscribe` header settles it.
- Automated renewal *reminders* with no action required and no failure.
- Vendor security *newsletters* (as opposed to alerts about the owner's own account).
- Anything already answered — check whether the owner replied after the last inbound message.

## Action

`FLAG` the message, `CATEGORIZE` as Don't Miss, and **leave it in the inbox**. Never file it away —
the whole point is that it stays visible.

## The Don't Miss digest

One message per day, composed as a draft for the owner — never auto-sent. Rules that keep it read:

- **Cap it at 7 items.** A digest that lists everything is the inbox again. If more than 7 qualify,
  include the top 7 by deadline proximity, then say "+N more" with a link to the category.
- **One line per item:** who, what they want, and the clock — `your attorney — needs the
  signed doc — asked 3 days ago`.
- **Lead with the oldest unanswered**, not the newest arrival. Age is the risk.
- **Say "nothing today"** when nothing qualifies. A digest that only appears when it matters gets
  opened; a daily wall of noise does not.
- **Never include anything the owner already answered.** Re-check reply state at compose time.

If the platform cannot draft mail, render the digest in chat instead — the content is the deliverable,
the channel is not.
