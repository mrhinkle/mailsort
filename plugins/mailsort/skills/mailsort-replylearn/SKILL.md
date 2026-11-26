---
name: mailsort-replylearn
description: >
  Learn the owner's reply style from what they actually send. Compares each draft an agent saved
  with the reply the owner sent on that thread, turns every edit into a dated rule in the right
  audience style file, and reports which drafts went out unchanged, edited, rewritten or
  discarded. Also bootstraps the audience style files from sent mail when a deployment has none.
  Use when the owner says "learn from my edits", "what did I change in your drafts", "update my
  reply style", "study my sent mail", "build my reply styles", or at the end of any triage run
  that created drafts. Reads and writes only override files; it never sends, edits or deletes mail.
---

# mailsort-replylearn

The owner's edits are the best training signal a mail assistant gets: every draft they rewrite says
exactly what the assistant got wrong, for exactly that audience. This skill closes the loop that
`mailsort-draftreply` opens. It is generic; every fact about one owner lives in the override layer.

## What the override layer provides

| Thing | Purpose |
|---|---|
| **Audience style files** | one Markdown file per audience (sponsors, team, family, …) in the shape of `references/reply-style-template.md`. Each ends in a `## Learned` section this skill appends to. |
| **Audience router** | how to tell which audience a thread belongs to (sender domain, label, thread topic). |
| **Draft ledger path** | a JSONL file **outside any git repo** (it holds mail text), one line per saved draft. |
| **Signature start patterns** | regexes for the first line of each mailbox's signature, so the diff ignores it. |
| **Sent-mail locations** | which mailboxes to search for the sent reply (a reply sent from another owned mailbox still counts). |

If any of these is missing, say which, and run with what exists.

## 1. Record every draft (called by `mailsort-draftreply`)

After a draft is saved and read back, append one line to the ledger:

```json
{"draft_id": "...", "mailbox": "...", "thread_id": "...", "audience": "...",
 "created": "<ISO-8601>", "to": "...", "body": "<exact body saved>", "status": "open"}
```

Never write the ledger inside a repository, and never commit it.

## 2. Learn (`/mailsort:learn`)

1. Load the ledger; keep rows with `status: open` older than 2 hours.
2. For each row, fetch the thread from its mailbox (and the owner's other mailboxes if overrides say
   replies can come from there). Find the first message **from the owner** created after `created`.
   - Found → that body is `sent`.
   - Not found and the draft no longer exists → `sent: null` (discarded).
   - Not found and the draft still exists → leave it open; if older than 72 hours, report it as stale.
3. Run `scripts/draft_diff.py` once over the batch, passing the signature patterns with
   `--sig-start`. It returns a verdict per draft (`unchanged`, `light_edit`, `heavy_edit`,
   `rewrite`, `discarded`), length ratio, greeting and sign-off before/after, and the sentences
   removed and added.
4. Turn results into rules. **Write the rule, not the instance**:
   - Generalize from the pattern across drafts in the same audience, not from one edit. One edit is a
     hypothesis (`(1)`); the same edit twice is a rule (`(2+)`), and a rule at `(3+)` is promoted
     into the body of the style file and removed from `## Learned`.
   - Length: if `length_ratio` is under 0.6 on two or more drafts, lower that audience's length
     budget to the median of what was sent.
   - Removed sentences that share a kind (stats, pitches, pleasantries, offers) become an *Avoid*
     line. Added sentences that share a kind (a cc to a delegate, a link, a date) become a *Move*.
   - A changed greeting or sign-off on two or more drafts replaces the audience's default.
   - `discarded` twice for the same kind of thread means "don't draft these"; propose it as a stop
     rule for `mailsort-draftreply`.
   - Never copy third-party names, addresses, amounts or private facts into a rule.
5. Append each rule to the audience file's `## Learned` section as
   `YYYY-MM-DD | (n) signal → rule | evidence: <draft ids>`. Mark the ledger rows `learned` with the
   verdict.
6. Report one table: audience, drafts, unchanged / edited / rewritten / discarded, median length
   ratio, and the rules added. Then the stale drafts by name and age.

A rule that would hold for anyone's mail (not this owner's taste) goes upstream to
`../mailsort/references/lessons.md`.

## 3. Bootstrap from sent mail (`/mailsort:learn --bootstrap`)

When a deployment has no style files yet:

1. Fetch 90–120 days of sent mail per mailbox. Drop self-addressed mail, mail over ~4,000 words and
   HTML newsletters.
2. Strip quoted history and signatures (same cleaning as the script).
3. Classify each message: audience, and whether the owner typed it or an agent/template wrote it.
   Agent-written mail is evidence of **what to avoid**, never of the owner's style.
4. Per audience, from owner-typed mail only: greeting counts, sign-off counts, **body word count
   median and 75th percentile without the signature**, structure, 4–7 concrete moves, and 2–3 short
   examples with every name, company, address and amount replaced by a placeholder.
5. Write one file per audience from `references/reply-style-template.md`. Show the owner the length
   table before anything else; it is usually the biggest correction.

## Never

Send, edit or delete mail or drafts. Commit the ledger. Put a third party's name, address or
private detail in a style file. Change a rule the owner wrote by hand without saying so.
