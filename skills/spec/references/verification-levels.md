# Choosing the verification level

Answer each question in the spec's Testing Decisions. Write the answer, not just the letter.

| # | Question | If yes |
|---|---|---|
| Q1 | Does an entity move through named states/statuses (order, payment, claim, message delivery, job, subscription, approval, session)? | A |
| Q2 | Can two actors act on the same thing at once, or can an event arrive twice, late, or out of order (webhooks, retries, queues, cron sweeps, double clicks, multiple workers)? | A |
| Q3 | Does a bug create, lose, or duplicate money, stock, credits, messages, or anything that must happen exactly once? | A |
| Q4 | Is there a rule or calculation whose output should satisfy a law for all inputs (totals, rounding, allocation, parsing/serializing round-trips, filtering, permissions matrix, idempotent transforms)? | B (add to A if A applies) |
| — | None of the above: display, forms, simple CRUD, copy changes | C |

**If unsure, choose A.** A small model that finds nothing costs an hour; a missed race in money code costs far more.

## Level A: formal model before code

- Tool: TLA+ checked by TLC (default for "can things happen in a bad order", any language). Alternatives are allowed when they fit the question better (Alloy for relational/permission structure, P or Quint for protocol-heavy teams), but the gate, record, and statechart steps stay the same.
- What goes in the spec: states, transitions + triggers, actors and what runs concurrently, what can be duplicated/delayed/reordered, and invariants `INV-n`:
  - Safety: "A payment is never `paid` twice for one donation." "Status never moves backwards except <named correction>."
  - Liveness: "Every message in `sending` eventually reaches a final state." (needs fairness assumptions; say which.)
  - Idempotency: "Applying the same webhook twice leaves the same state as applying it once."
- Gate: `prove` must pass before tickets. The model and the statechart are attached to the spec.
- Level A specs usually also get level-B properties at the code seam: generate random event orders and assert the same invariants against the real code.

## Level B: properties before code

- Properties `PROP-n` in plain language, each with: the input space (generator), the law, and known edge cases that must be in the generator (empty, zero, max, unicode, duplicates, boundaries).
- Common shapes: round-trip (`decode(encode(x)) == x`), invariant preserved (`sum(parts) == total`), oracle/model comparison (fast path == slow obvious path), idempotence (`f(f(x)) == f(x)`), metamorphic (filter then count == count of filtered), commutativity where order must not matter.
- Library per language: `property-testing.md`.

## Level C: examples

- One or more concrete test cases per user story, plus QA steps. Name the seam they run at.

## Combining levels

Write every level that applies, e.g. "A for the payment lifecycle; B for fee rounding". The gate applies to the A part only.
