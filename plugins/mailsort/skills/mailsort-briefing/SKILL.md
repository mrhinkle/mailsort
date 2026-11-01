---
name: mailsort-briefing
description: >
  The daily morning briefing — one email that opens with today's schedule, then the mail that can't
  wait, then the current priority list, every item deep-linked back to the message, event, or task it
  came from. Provider- and platform-neutral (Gmail/Google Calendar or Microsoft 365/Graph); part of
  the `mailsort` family. Use when someone asks for a morning brief, daily digest, "what's on today",
  "my priorities", a start-of-day email, or wants a scheduled recap delivered to their inbox. It
  reads and composes; it delivers the brief as the run's final message by default and emails it only to the owner's own address, only when the owner asks — never to anyone else.
---

# mailsort-briefing

One email, once a morning, that answers three questions in order: **where do I have to be, who is
waiting on me, and what did I say I'd do.** Default delivery is the run's final message (or a saved
draft). It is the only output in the system that may be emailed at all, and only to the owner's own
address, and only when the owner has asked for email delivery in chat. Never to anyone else.

## Open with BLUF

Bottom line up front, always — the conclusion goes in the first sentence, not after the setup. This
is Army correspondence doctrine (AR 25-50) and it is the single highest-value convention in briefing
practice. Three lines maximum:

1. The day in one sentence.
2. The single most important thing.
3. Whether a decision is required today — and if so, say it here **and** again at the close. A
   decision brief states the ask at the beginning and requests it explicitly at the end.

## Label every item by type

`FYI` · `DECISION REQUIRED` · `ACTION REQUIRED`. Uniform urgency is why briefings get skimmed: if
nothing is flagged, everything is noise. A decision item carries the ask, the options, your
recommendation, the deadline, and the cost of delay.

## Empty states are content

If a section is empty, say "none" in one line. Never pad. Inventing content for a quiet section
destroys the meaning of the section being full — and the roll-up line that proves the quiet parts
were checked ("42 others filed, nothing needed") is what makes the whole brief trustworthy.

## Order is the design

Schedule first — it is time-boxed and unmovable, and it determines how much room the rest of the day
has. Then mail that can't wait. Then the priority list, which is what fills the gaps. A briefing that
leads with a task list gets read at 11am, after the 9am meeting was missed.

## Section 1 — Today's schedule

From the calendar (`events.list` / Graph `/me/calendarView`) for the local day:

- Time, title, duration, and **who else is on it** (the names matter more than the title).
- Mark the first commitment of the day explicitly — "first: 9:00".
- Flag conflicts (overlaps) and anything with no agenda or no other attendee.
- Include video/location links inline so the row is clickable at the moment it's needed.
- Say "nothing scheduled" plainly when the day is clear; that is useful information, not an empty
  section to pad.

## Section 2 — Mail that can't wait

Pull from `mailsort-dontmiss` (flagged/Don't Miss) and `mailsort-needsreply`, deduplicated, capped at
**7 items**, ordered by **age of the oldest unanswered inbound** — not by arrival.

One line each: **who** · **what they want** · **how long they've waited**. Then the link.

Nothing else belongs here. No newsletters, no alerts, no counts of filed mail — those are a footer
line at most.

## Section 3 — Priority list

From `mailsort-todo` plus any connected task source, ordered by deadline, then by age:

- Anything **due today or overdue** goes at the top, marked.
- Dated items next, with the date.
- Undated items below, capped at 5 — an uncapped list is a guilt pile, not a plan.
- Include **what closed since yesterday**, in one line. Visible progress is why people keep reading.

## Linking — get this right or the briefing is useless

Every row must open the exact thing it names, in one click. Never paste a bare ID, never link to a
search that "should" find it, never link to the folder.

| Item | Gmail / Google | Microsoft 365 |
|---|---|---|
| Message | `https://mail.google.com/mail/u/0/#all/<messageId>` (the API's own `display_url` when available) | the message's Graph `webLink` |
| Thread | same, using the thread id | conversation `webLink` |
| Calendar event | the event's `htmlLink` | the event's `webLink` |
| Task | the task URL, else the source message link | same |

Rules: take the link from the API response rather than constructing it whenever the API supplies one;
verify one link per section before sending; if an item has no resolvable link, say so in the row
instead of shipping a dead one. A briefing whose links miss is worse than no briefing — it costs the
reader a search *and* their trust.

## Composition

- **Subject** carries the headline, because it is often all that gets read on a phone:
  `Fri Oct 3 — 4 meetings · 3 need a reply · 2 due today`.
- Plain, scannable, no preamble, no sign-off, no motivational line.
- Under one screen. If a section runs long, truncate and say "+N more" with a link to the category.
- **Send only to the owner's own address.** Never cc anyone, never forward, never include a recipient
  the owner did not configure.
- If nothing qualifies in a section, one short line — not an apology, not filler.

## Scheduling

The cadence is deployment-specific (host cron, a platform scheduler, or an agent runner). Whatever
runs it must:

- Fire **before the owner's first regular commitment**, in their local timezone, on a weekday
  schedule unless told otherwise.
- Be **idempotent**: one briefing per day. If a run repeats, update or skip — never send twice.
- **Fail loudly to the owner** if the calendar or mail source is unreachable. A silently missing
  briefing teaches the owner to stop relying on it, which is worse than an error line.
- Skip send on days the owner marks away, if such a setting exists.

## Never

Send to anyone but the owner. Reply to anything it summarizes. Take an action on a listed item.
Invent an attendee, a deadline, or a link.

## Conventions borrowed from briefing practice

- **"So what" on every item.** One clause of why it matters, or cut the item.
- **Likelihood is not confidence** (ICD 203). "Almost certainly" describes probability; confidence
  describes how good your sources are. State them separately and never blend them.
- **SITREP tail order** for anything ongoing: situation → what was done → what is next → issues and
  decisions. End on decisions, not on a summary.
- **Hard caps:** headline under 10 words, 5 mail items, one screen, ≤400 words above the fold, and a
  stated read time. Axios's Smart Brevity gets ~40% shorter with the same information by enforcing
  exactly this.
- **Stable section order, every single day.** Scanning depends on the structure never moving.
- **Closed since last brief** — short, but never omitted. It is the only proof the system is working.
- **Never close with "let me know if you have questions."** Close with the next step or the ask.
- **No stale carry-forwards.** An item repeated from yesterday must show its age and escalate, or be
  dropped.
