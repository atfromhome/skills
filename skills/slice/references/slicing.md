# Slicing rules

## Vertical slices (tracer bullets)
- Cut through schema, API, UI, and tests for one narrow behaviour; never "all the DB work" as one ticket.
- A slice is done when it can be demoed or verified on its own.
- One fresh agent session per ticket. If it needs a long preamble, split it.
- Prefactoring first.

## The prefactor ticket (level A/B)
Purpose: make the oracle exist before the behaviour, so every later ticket has an objective done-check.
- A: model committed + action→code map + stateful property tests + `verify-<area>` skill, proven to catch a scratch break.
- B: PBT library + one property test per `PROP-n`, with generators covering the spec's edge cases.
- Tests for unbuilt behaviour are committed in the language's pending form (skip/xfail/`t.Skip` with the ticket reference). The ticket that builds the behaviour turns them on; turning them on is in its acceptance criteria.

## Coverage check before the quiz
Make a small table: each `INV-n`/`PROP-n` → ticket(s) that satisfy it. Every row needs at least one ticket. Each level-A transition in the statechart → the ticket that implements it.

## Wide refactors
One mechanical change with a large blast radius (rename a column, retype a shared symbol): expand (new beside old) → migrate in batches sized by blast radius, each blocked by expand → contract (delete old), blocked by every batch. If batches cannot stay green alone, share an integration branch that blocks a final integrate-and-verify ticket.

## Blocking edges
Only real gates. Parallelizable tickets should not block each other. Everything is blocked by the prefactor.
