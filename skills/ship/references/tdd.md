# The test-first loop

Adapted from mattpocock/skills `tdd`. The loop is red → green. These notes make it produce tests worth keeping. Read them before the first cycle and keep them in view during it.

Read the repo's glossary (`GLOSSARY.md` or its equivalent) so test names use the domain's words, and respect ADRs in the area.

## Where the first tests come from

1. **The ticket's acceptance criteria.** Each criterion becomes at least one test, named after the behaviour it promises.
2. **The `INV-n` / `PROP-n` the criterion cites.** The test checks that rule, not a nearby one.
   - **Level A:** tests mirror the invariants. The stateful property tests from ticket 01 replay random sequences of the model's actions against the real code and assert the same `INV-n`; example tests name the statechart transition they cover.
   - **Level B:** each `PROP-n` is a property test in the repo's property-testing library (see `spec`'s `references/property-testing.md`), with generators that include the edge cases the spec lists.
   - **Level C:** one or more example tests per user story.
3. **Pending tests from the prefactor.** If ticket 01 left tests marked skipped or expected-fail for this ticket, turning them on is your first red.

Expected values come from an independent source: the spec, a worked example, a known literal. Never from the code under test.

## Seams: where tests go

A seam is the public boundary where you observe behaviour without reaching inside. Test only at the seams recorded in the spec's Testing Decisions (agreed with the human at the spec's seams check). If the work seems to need a seam the spec does not list, stop and ask before writing a test there; note what it would catch and what it would miss.

## Anti-patterns

- **Implementation-coupled.** Mocks internal collaborators, tests private functions, or checks through a side channel (reading the database instead of calling the interface). Tell: it breaks on a refactor that keeps behaviour.
- **Tautological.** The assertion recomputes the expected value the way the code does, so it can never disagree with the code. Includes snapshots derived the same way and constants compared with themselves.
- **Horizontal slicing.** Writing all tests first, then all code. Bulk tests describe imagined behaviour and lock in a structure before you understand it. Work in vertical slices: one test, the code that passes it, repeat.

## Rules of the loop

- **Red before green.** Write the failing test, watch it fail for the expected reason, then write only enough code to pass it. No speculative features.
- **One slice at a time.** One seam, one test, one minimal change per cycle.
- **Refactoring is not part of the loop.** It belongs to review (`check`), not to red → green.
- **Never weaken a test, property, or invariant to get green.** A property that keeps failing is a finding: report it.

See `tests.md` for examples and `mocking.md` for when to mock.
