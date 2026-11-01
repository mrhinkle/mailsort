# mailsort adapters — how the seven verbs reach a real mailbox

`mailsort` is written against seven verbs, never against a vendor API. This file is the lookup table
from each verb to the concrete tool on each connectivity path. Pick one path per mailbox during
`/mailsort:setup` and record it in the override layer.

## Recommended path: Composio

Composio is the recommended connectivity layer: one managed OAuth per mailbox, write scope on both
Gmail and Outlook, batch operations, and the same call shape from any agent runtime (Claude Code,
Cowork, Codex, a cron job). Install the `composio` plugin, run `/composio-connect gmail` or
`/composio-connect outlook`, then **always pass the connected account id on every call** — Composio
otherwise targets whichever account it treats as default, which is a silent wrong-mailbox write.

Check what is connected with `COMPOSIO_MANAGE_CONNECTIONS` (`action: "list"`) through the Composio
MCP before declaring a mailbox missing. The `composio` CLI can show a different account set.

| Verb | Composio Gmail | Composio Outlook (Microsoft 365) |
|---|---|---|
| `FIND(query)` | `GMAIL_FETCH_EMAILS` (`query`, `label_ids`, `max_results ≤ 500`, `ids_only`, paginate `nextPageToken`; pass `include_spam_trash: true` for history checks) | `OUTLOOK_QUERY_EMAILS` / `OUTLOOK_LIST_MESSAGES` (`$search`, `$filter`, `$top`, `@odata.nextLink`) |
| `CATEGORIZE` | `GMAIL_BATCH_MODIFY_MESSAGES` add label id (≤1000 ids); single thread: `GMAIL_MODIFY_THREAD_LABELS` | `OUTLOOK_BATCH_UPDATE_MESSAGES` set `categories` |
| `FILE` | `GMAIL_BATCH_MODIFY_MESSAGES` add label id + remove `INBOX` | `OUTLOOK_BATCH_MOVE_MESSAGES` / `OUTLOOK_MOVE_MESSAGE` to a folder under the triage root (`OUTLOOK_LIST_MAIL_FOLDERS` to find ids) |
| `FLAG` / `UNFLAG` | add / remove `STARRED` | `OUTLOOK_UPDATE_EMAIL` `flag.flagStatus` = `flagged` / `notFlagged` |
| `READ_STATE` | add / remove `UNREAD` | `OUTLOOK_BATCH_UPDATE_MESSAGES` `isRead` |
| `CONTACT_UPSERT` | Google People API via Composio `GOOGLECONTACTS_*` (or report the contact for the owner to add) | `OUTLOOK_CREATE_CONTACT` / Graph `/me/contacts` |
| `DRAFT(thread, body)` | `GMAIL_CREATE_EMAIL_DRAFT` with `thread_id`, empty `subject`, `cc` as a list; read back with `GMAIL_FETCH_MESSAGE_BY_THREAD_ID` and confirm a `DRAFT`-labelled message | `OUTLOOK_CREATE_DRAFT_REPLY` (or `OUTLOOK_CREATE_REPLY_ALL_DRAFT`); read back with `OUTLOOK_GET_MESSAGE` and confirm `isDraft: true` |

Labels: `GMAIL_LIST_LABELS` to map names to ids (re-list every run; ids differ per mailbox);
`GMAIL_CREATE_LABEL` only with the owner's consent during setup. Outlook: `OUTLOOK_LIST_MAIL_FOLDERS`.

**Not on this path, by design:** `GMAIL_SEND_DRAFT`, `GMAIL_REPLY_TO_THREAD`, `OUTLOOK_SEND_DRAFT`,
any delete or spam call. The owner sends. Gmail *filters* need the `gmail.settings.basic` scope,
which a connection may or may not carry. Test read-only first with `GMAIL_LIST_FILTERS`: if it
returns the filter list, `GMAIL_CREATE_FILTER` will work on that connection (still ask the owner
before creating one, since a filter is standing configuration); if it returns 403, use
`/mailsort:rules` to export an import file instead.

Batch gotchas (both providers): a batch success response is acceptance-only and silently skips bad
ids, so verify by re-querying; persist page tokens across pages or you re-process page 1 forever;
a `-label:` exclusion under-matches, prefer positive `label_ids`; label names containing `@` break
Gmail query syntax, use `label_ids`; long sequential runs hit per-cell timeouts, so split more than
three 1000-id batches across cells and recount before re-running.

## Native connectors (work, with limits)

Use these when Composio is not available. Record the limit in the override layer so a run does not
try a write the path cannot do.

| Path | FIND / read | Writes | Notes |
|---|---|---|---|
| **Claude Gmail connector** (claude.ai / Cowork) | `search_threads`, `get_thread`, `get_message`, `list_labels` | `label_thread`, `unlabel_thread`, `create_label`, `create_draft`, `trash_*` exist but may return "requires additional permissions" depending on the grant | Read-only in many deployments. Fine for `/mailsort:needsreply` and `/mailsort:brief`; pair with Composio for `FILE`. Thread ids equal message ids for single-message threads, so they feed `GMAIL_BATCH_MODIFY_MESSAGES` directly. |
| **Microsoft 365 connector** (claude.ai) or Graph MCP | `/me/messages` search | `PATCH` categories/isRead/flag, `move`, `createReply` | Full verb coverage where the grant includes `Mail.ReadWrite`. |
| **Google Workspace MCP / `gws` CLI** | Gmail API `users.messages.list` | `users.messages.batchModify`, `users.drafts.create`, `users.labels.create`; `users.settings.filters.create` if the scope was granted | The only path that can create Gmail filters directly, when scoped. |
| **Microsoft Graph directly** (`az rest` / Graph Explorer) | `/me/messages?$search=` | `/me/messages/{id}` PATCH, `/move`, `/createReply`, `/me/mailFolders/inbox/messageRules` | Can create Outlook rules directly; `/mailsort:rules` emits the JSON body. |

## Which path during setup

1. Composio connected for this mailbox → use it for everything.
2. Only a native connector → use it for reads and whatever writes it allows; report the rest as
   "proposed, not applied" lines the owner can act on.
3. Nothing connected → `/mailsort:setup` stops and says which connector to add; it never asks for a
   password or token in chat.
