# Changelog

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
