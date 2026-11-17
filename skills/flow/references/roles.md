# Implementer and QA hooks

## Implementer

Before code:
1. Read the ticket, its parent spec, and (level A) the latest gate record on the spec. If the gate is not `passed`/`waived` or is `stale`, stop and send the spec back to `prove`.
2. Follow the repo's claim rule if it has one (assign yourself, claim command, progress label).
3. Branch from the repo's integration branch using its naming convention (default `<spec-slug>/NN-<topic>`). Never commit to a protected branch.

While coding:
- **Level A:** the verified statechart is the design. Each model action maps to one atomic step in code (one transaction, one compare-and-set, one lock scope). If the code needs a state, transition, or interleaving the model does not have, stop: either the design changes (back to the gate, update the model, rerun TLC) or the code is wrong. Do not "just add" a transition.
- **Level A/B:** the prefactor ticket's property tests and (A) model are the acceptance oracle. Do not weaken a property or invariant to go green; a failing property is a finding to report.
- Level C: regular tests for the acceptance criteria.

Before opening the PR (or merge request):
- Run the project-local verify skill (level A; created by the prefactor ticket) and the property tests. Paste the command, tool versions, commit SHA, and result into the PR description.
- If your change touched code the verify skill covers and the model no longer describes it, update the model in the same PR with `prove` **maintain** mode, in a separate commit from product code.
- Reference the ticket in the PR. Put the "closes spec" keyword only where the repo's convention says (often the last ticket of the spec).
- Never merge your own PR; never push to protected branches.

## QA

1. Check out the PR head and record the exact SHA.
2. Rerun, on that SHA: the verify skill (A), the property tests (A/B), the regular tests (all), and each acceptance criterion. Each criterion should cite the spec invariant/property it proves (`INV-n`, `PROP-n`).
3. Compare model to code for level A: does each changed function still map to the model's actions and atomic steps? If not, that is **drift**: reject with "model drift" and point to maintain mode, even if TLC passes (a pass on a stale model proves nothing).
4. Verdict comment on the PR/ticket: SHA, commands, results, accepted/rejected with reasons. Use the repo's reject counters or labels if it has them.
5. A TLC counterexample or failing property is replayed against the real code before calling it a bug. If a step cannot happen in code, the model is wrong (drift); if every step can happen, it is a bug.

## Drift at any time

Signs: a merged change touched covered files without a model update, the verify skill's sync commit is older than changes to covered files, or a counterexample does not replay. Run `prove` in **maintain** mode. Verification updates go in their own change, separate from product fixes.
