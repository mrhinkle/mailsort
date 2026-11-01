---
name: mailsort-receipts
description: >
  The "Receipts" category — payment confirmations, invoices, orders, statements and renewal notices,
  kept as proof and optionally posted to a ledger or budget. Provider- and platform-neutral; part of
  the `mailsort` family. Use when triaging mail, at expense or tax time, when reconciling spend, or
  when someone asks what a service is costing them. It files and extracts; it never pays anything.
---

# mailsort-receipts

Proof, not action. The value is in retrieval a year later and in the totals, not in reading any one
message.

## What counts

An actual transaction record: payment confirmation, invoice, paid receipt, order confirmation,
shipping notice tied to an order, bank/card statement, subscription renewal **that charged**.

**Not receipts:** renewal *reminders* ("your plan renews in 7 days"), usage summaries, price-change
announcements, payout notices, failed-payment notices. A failed payment is **Don't Miss** — money did
not move and someone must act.

## Extract

Pull and record, per message: vendor, amount, currency, date, category, invoice/order number, and
whether it is recurring. Take the amount from the message body, not the subject — subjects round,
omit tax, and lie. If the preview truncates before the amount, fetch the full body; if it still
cannot be found, record the receipt with a blank amount and say so rather than guessing.

## Ledger posting

When the owner keeps a spreadsheet or ledger, post to it and cite the source message. Rules that
prevent corruption:

- **Never overwrite a non-empty cell** with an inferred value; surface the conflict instead.
- **Match the sheet's own period convention** — bill date vs payment date, whichever the existing
  rows use. Check an existing row before writing a new one.
- **Duplicates:** a vendor often sends both an invoice and a payment confirmation for the same
  charge. Post once, keyed on invoice number, and prefer the **payment confirmation**.
- Recurring charges that stop appearing are worth a line in the report — a cancelled service or a
  failed card usually shows up as silence, not as mail.

## Report

Monthly totals by vendor and category, plus: new recurring charges, amounts that changed, and
subscriptions that appear to have lapsed. Individual receipts are never listed.
