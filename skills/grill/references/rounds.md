# Rounds

## Format

```
Round <n>. <one line: what this round settles>

❓ **Q1 - <question title>**: <question body; may be several paragraphs; may list options a/b/c with trade-offs>

➡️ <recommended answer, worded so "yes" accepts it, plus a one-line reason>

---

❓ **Q2 - <question title>**: ...

➡️ ...

Looking up (not asking): <fact> → <where you are checking>. Questions that depend on it come next round.
Answer in shorthand, e.g. "1 yes, 2 b, 3 no: weekly".
```

- Number questions continuously across rounds (Round 2 starts at Q5 if Round 1 ended at Q4) so answers stay unambiguous.
- One decision per question. Split compound questions.
- Keep the round to the true frontier. Size follows the tree, not a quota; 3–7 questions is typical.
- After the answers, restate in one line each what was settled before asking the next round.

## Seed branches for the design tree

Not a checklist to recite; drop branches that do not apply and add ones that do.

| Branch | Typical questions |
|---|---|
| Goal | What problem, for whom, and how do we know it worked? |
| Actors | Who or what acts: users, admins, crons, webhooks, workers, other services? |
| Domain terms | Which words are new, overloaded, or in conflict with the glossary? |
| Lifecycle | Does an entity gain or change named states? Which transitions, triggered by whom? |
| Concurrency and ordering | What can happen at once, twice, late, or out of order? |
| Exactly-once effects | Money, stock, credits, messages: what must never be duplicated or lost? |
| Failure | What happens on crash, timeout, provider outage, partial success? |
| Rules and calculations | Totals, rounding, schedules, limits: what law must hold for all inputs? |
| Permissions | Who may see or do what? |
| Data | New fields, migration or backfill of existing records, retention? |
| UX | Where does it show up, what copy, what empty and error states? |
| Rollout | Flag, gradual rollout, compatibility with old clients? |
| Out of scope | What are we explicitly not doing now? |

## Worked example (abridged)

Feature: "Add a payment reminder status to donation pledges." Context dump done; the code shows a `Pledge` with statuses `active`, `fulfilled`, `cancelled`, a monthly payment webhook, and a daily cron. The glossary defines **Pledge** and **Pledge status**.

```
Round 1. Settle what "payment reminder status" means and who triggers it.

❓ **Q1 - Status or separate field**: The glossary says Pledge status is the pledge's lifecycle (active, fulfilled, cancelled). A reminder is about one overdue installment, not the whole pledge. Should reminders live on a separate Installment reminder state instead of a new Pledge status?

➡️ Yes: keep Pledge status as the lifecycle and track reminders per overdue installment. Adding "reminded" to Pledge status would mix two lifecycles.

---

❓ **Q2 - Trigger**: Should the existing daily cron send reminders for installments overdue by N days, rather than staff sending them by hand?

➡️ Yes, the daily cron, so reminders are consistent; staff can still resend manually.

---

❓ **Q3 - Channel**: Should reminders go by email only for now?

➡️ Yes, email only; other channels are out of scope.

Looking up (not asking): whether the payment webhook can arrive after the due date for a payment made on time → reading the webhook handler and provider docs. The race question (reminder sent for an installment that was actually paid) comes next round.
```

Round 2 would then ask the grace period (N days), the maximum number of reminders, what happens when a payment webhook lands while a reminder is being sent, and whether a cancelled pledge stops pending reminders. The level hint ends as **A**: installments gain named reminder states (Q1 of the levels table), the cron and the payment webhook can act on the same installment at once (Q2), and a duplicate or wrong reminder is a message that must happen at most once (Q3). The glossary gains **Installment** and **Payment reminder**; no ADR, because the choice is easy to reverse.
