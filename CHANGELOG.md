# Changelog

## 1.2.0 — 2026-11-26

- New `mailsort-replylearn` skill and `/mailsort:learn` command: diffs each saved draft against
  the reply the owner actually sent (`scripts/draft_diff.py`, deterministic, no network) and writes
  dated, evidence-counted rules into per-audience style files in the override layer.
  `--bootstrap` builds those files from 90–120 days of sent mail.
- New `skills/mailsort/references/reply-style-template.md`: the shape of an audience style file
  (length budget, shape, moves, avoid, examples, learned).
- `mailsort-draftreply` loads the audience style file before writing, treats its length budget as a
  ceiling (default under 60 words without one), and records every saved draft in a draft ledger.
- Lesson from the first bootstrap: the owner's own replies were several times shorter than agent
  drafts to the same audiences, so length budgets come from sent mail, signature stripped.

## 1.1.0 — 2026-11-01

- `mailsort-draftreply` gains a **Draft audit** procedure for existing drafts: SUPERSEDED, EMPTY,
  DUP, CROSS-MAILBOX DUP, THIRD-PARTY, STALE INBOUND, AGING, LIVE. Reports with compose links;
  deletion stays with the owner (no DELETE verb, on purpose).
- New `skills/mailsort/references/lessons.md`: the plugin's own dated, generic lessons log, with
  the promotion protocol (overrides log → lessons.md → pull request). Seeded from the first full
  three-mailbox audit (83 drafts, 28 stale).
- Core self-improvement protocol gains step 6: read and append the shared lessons file.

## 1.0.2 — 2026-11-01

Correction: a successful `GMAIL_LIST_FILTERS` does not prove `GMAIL_CREATE_FILTER` will work
(list uses the mail scope, create needs `gmail.settings.basic`). The export file is the default path.

## 1.0.1 — 2026-11-01

`mailsort-rules` now lists existing filters first (read-only) and skips what the client already
routes; adapters note that `GMAIL_LIST_FILTERS` is the scope test before any filter creation.

## 1.0.0 — 2026-11-01

First public release. Core + 15 category and report skills, `mailsort-setup`, `mailsort-rules`,
`mailsort-sweep`, adapter reference (Composio recommended, native connectors supported), and eight
slash commands including the `/mailsort:help` menu.
