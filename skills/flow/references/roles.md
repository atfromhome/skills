# Implementer and QA rules

`ship` (implementation) and `check` (QA) carry these out step by step. This page is the short checklist behind them, for an agent working a ticket without those skills installed.

## Implementer (`ship`)

Before code:
1. Read the ticket, its parent spec, and (level A) the latest gate record on the spec. If the gate is not `passed`/`waived` or is `stale`, stop and send the spec back to `prove`.
2. Ticket 01, the prefactor, is done first; level A runs `prove` bind mode in it.
3. Follow the repo's claim rule if it has one (assign yourself, claim command, progress label).
4. Branch per the repo's convention (default ticket branch `<spec-slug>/NN-<topic>`, integration branch `<spec-slug>/integration`). Never commit to a protected branch.

While coding:
- **Level A:** the verified statechart is the design. Each model action maps to one atomic step in code (one transaction, one compare-and-set, one lock scope). If the code needs a state, transition, or interleaving the model does not have, stop: either the design changes (back to the gate) or the code is wrong. Do not "just add" a transition, and never edit the model silently.
- **Level A/B:** the prefactor ticket's property tests and (A) model are the acceptance oracle. Do not weaken a property or invariant to go green; a failing property is a finding to report.
- **Level C:** regular tests for the acceptance criteria.
- Tests first, from the acceptance criteria and the `INV-n`/`PROP-n` they cite, at the spec's seams.

## QA (`check`)

1. Record the exact head SHA. Every result is for that SHA.
2. Rerun on it: the verify skill (A), the property tests (A/B), the regular tests (all), and each acceptance criterion with its evidence. Map every `INV-n`/`PROP-n` to a test.
3. Level A: does each changed function still map to the model's actions and atomic steps? If not, that is **drift**: reject with "model drift" and point to maintain mode, even if TLC passes (a pass on a stale model proves nothing).
4. A TLC counterexample or failing property is replayed against the real code before calling it a bug. Impossible step in code → the model is wrong (drift); every step possible → bug.
5. Report findings and stop for the human before fixing. Fixes go back to the implementer.
6. When clean: PR body (`pr` skill) with commands, tool versions, SHA, results, and the INV/PROP coverage; link it so merging closes the ticket ("closes spec" only where the repo's convention says). Never merge your own PR; never push to protected branches.

## Drift at any time

Signs: a merged change touched covered files without a model update, the verify skill's sync commit is older than changes to covered files, or a counterexample does not replay. Run `prove` in **maintain** mode. Verification updates go in their own change, separate from product fixes.
