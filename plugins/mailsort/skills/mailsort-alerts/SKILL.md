---
name: mailsort-alerts
description: >
  The "Alerts" category — machine-generated notifications from systems and services (CI, deploys,
  monitoring, repo activity, agent automations, device and account notices). Provider- and
  platform-neutral; part of the `mailsort` family. Use when triaging mail or when someone asks to
  quiet system noise, file alerts, or find out what a service keeps emailing about. It files and
  counts; it never unsubscribes or deletes.
---

# mailsort-alerts

Usually the single largest source of mail volume and the smallest source of value per message. The
job is to make alerts **countable** rather than readable.

## Identify

Machine test from `mailsort` passes, AND the sender is a service the owner uses (not a publisher).
Typical shapes: build/CI results, deploy notices, repo activity, monitoring and uptime, backup
results, cron and agent runs, quota and rate-limit warnings, device sign-ins.

**Outranked by Don't Miss:** any alert about the owner's own account security or a failed payment is
Don't Miss, not Alerts. Check that first.

## File by source, not by severity

Give each service its own sub-category (`Alerts/<Service>`), then archive. Severity in the subject is
the vendor's opinion and is wrong often enough to be useless; the service name is stable and lets the
owner mute one source without muting all.

## Report as counts

Never list alerts individually. `GitHub 412 · CI 38 · Vercel 15` is the entire useful report. The one
exception: a **new** state worth a sentence — a service that has never emailed before, or a failure
that has repeated more than 20 times.

## The repetition rule

Count consecutive failures per automation. **Past ~20 identical failures, the alert is not
information — it is a broken generator.** Say so explicitly and name the source. No filing rule fixes
a job that has failed dozens of times; the fix is upstream, in the service that sends it.

## Escalation

Surface an alert to the owner only when: it is a first-ever from that source; it reports data loss,
billing failure, or a security change; or it breaks a streak (first failure after a long green run).
Everything else waits for the count.

## Never

Unsubscribe, mute at the vendor, or delete. Changing a service's notification settings is the owner's
call — propose it, with the numbers that justify it.
