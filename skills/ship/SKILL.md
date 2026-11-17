---
name: ship
description: "Implement vflow tickets test-first on a ticket or integration branch, then hand off to check. Single-ticket mode fetches one ticket from the tracker and builds it. Whole-spec mode treats the spec's tickets as a task graph and works the frontier with a fresh subagent per ticket, each in its own worktree, merged into one integration branch with a draft PR. Prefactor ticket 01 goes first (level A runs prove bind there); refuses a level-A spec without a current passed or human-waived formal gate. Tests come from the acceptance criteria and the INV-n/PROP-n they cite, at the spec's seams, red before green; level B uses property tests. Stops and routes to prove maintain if the code must leave the verified model. Never pushes to or merges into main. Use for /ship, 'implement this ticket', 'build ticket 03', 'implement the spec', 'work the frontier', 'start coding the tickets'. Not for breaking a spec into tickets (slice), writing a spec (spec), interviewing (grill), or reviewing a finished branch (check)."
license: "MIT. Derived from mattpocock/skills implement, implement-spec, tdd and diagnosing-bugs; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# ship

The implementation step of the vflow family. It takes tickets made by `slice` and turns them into tested commits on a branch. It does not review its own work and does not open the final PR: that is `check`.

Find the tracker first (lookup order in the `flow` skill, `references/tracker.md`). Use the repo's claim rule, labels, and branch naming if it defines them; otherwise the defaults in `flow`'s `references/config.md`.

## 0. Preconditions (both modes)

1. **Read the ticket(s), the parent spec, and its comments.** Note the verification level, the seams in Testing Decisions, and the `INV-n` / `PROP-n` list.
2. **Level A gate check.** Find the latest `<!-- vflow:formal-gate -->` record on the spec. Start only if it says `PASSED` (or `WAIVED` by a human) **and** is current: its spec revision matches the spec now, and the gate label agrees (`formal-gate:passed` / `waived`, or the repo's equivalent). Anything else (`pending`, `failed`, `blocked`, `stale`, no record, or a label and record that disagree): **refuse to start**, say which, and route to `prove` gate mode.
3. **Prefactor first.** For a level A or B spec, ticket 01 (the prefactor from `slice`) blocks every other ticket. If it is not closed or merged into the integration branch, it is the only ticket you may start.
4. **Find the commands.** Discover the typecheck, single-test, full-suite, and property-test commands from the repo's docs (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, README, task runner files such as a Makefile or package scripts) or the vflow config `commands:`. Run each once to confirm it works before you rely on it. If none is documented, say so and ask.
5. **Branch.** Never work on a protected branch (`main`, `master`, `trunk`, `*/trunk`, the repo's default). Ticket branch default `<spec-slug>/NN-<topic>`; integration branch default `<spec-slug>/integration`.

## 1. Single-ticket mode

Use when given one ticket reference. If the reference is ambiguous, ask.

1. Fetch the ticket and **state its title** before starting. Check its blockers are done.
2. Claim it per the repo's rule. Branch from the integration branch if the spec has one, otherwise from the default branch.
3. **Ticket 01 of a level-A spec:** run `prove` in **bind** mode as the body of this ticket. It commits the model, maps actions to code, adds the stateful property tests, and generates the repo-local `verify-<area>` skill. No product behaviour change.
   **Ticket 01 of a level-B spec:** add the property-testing library if missing (the human confirms the choice first) and one property test per `PROP-n`, pending where the behaviour is unbuilt (see `spec`'s `references/property-testing.md`).
4. **Other tickets:** build with the test-first loop in `references/tdd.md`. Turning on the pending property tests this ticket owns is part of the ticket.
5. Run typecheck and single test files often; run the full suite (plus `verify-<area>` for level A) once at the end.
6. Commit to the ticket branch with messages that name the ticket. Push the ticket branch if the repo works through PRs.
7. Hand off to `check` with: ticket, branch, base (fixed point), commands run.

## 2. Whole-spec mode

Use when asked to implement a whole spec. Details in `references/whole-spec.md`. In short:

1. Read the spec and every ticket; build the task graph from the blocking edges. The **frontier** is every open ticket whose blockers are done.
2. Create the integration branch from the default branch.
3. Run ticket 01 first, alone. After its merge into the integration branch, push it and open a **draft PR** from the integration branch to the default branch that references the spec and every ticket (closing keywords per the tracker; `check` finalises them).
4. Then, for each frontier ticket, start a **fresh implementer subagent** (background, parallel where possible) in its own worktree on its own ticket branch, based on the integration branch tip. Pass pointers (spec, ticket, notes path, commits), not copied text. Each runs single-ticket steps 3 to 6 and merges the integration tip into its branch before reporting.
5. Merge each finished ticket branch into the integration branch (a merger subagent if available), run the full suite on the result, then recompute the frontier and start the newly unblocked tickets.
6. Without subagents: do the same sequentially, one ticket at a time, one branch each.
7. When every ticket is merged: clean up worktrees, then hand the integration branch to `check`.

## While coding (both modes)

- **Level A: the verified statechart is the design.** Each model action maps to one atomic step in code. If the code needs a state, transition, or interleaving the model does not have, or an `INV-n` looks wrong, **stop**. Report it and route to `prove` (maintain for drift; gate if the spec's design changes). Never edit the model, an invariant, or a property silently, and never weaken one to go green.
- **A test fails and the cause is unclear:** stop guessing and follow `references/debugging.md`.
- **Evidence:** do not say "done", "fixed" or "passing" without fresh command output from this session.
- **Never** push to or merge into a protected branch, merge a PR, or close a ticket by hand. Only ticket and integration branches.

## Hand off to `check`

Report per ticket: title (linked), branch, commits, the commands you ran with their last result, pending tests turned on, and anything you stopped on. Then load `check`. Fixes that `check` asks for come back here as new commits on the same branch.

## References
- `references/tdd.md`: the test-first loop, seams, first tests from criteria and invariants, anti-patterns.
- `references/tests.md`: good and bad tests, in pseudocode.
- `references/mocking.md`: mock only at system boundaries.
- `references/debugging.md`: the diagnosis loop for unclear failures.
- `references/whole-spec.md`: task graph, subagents, worktrees, merging, draft PR.
- `scripts/hitl-loop.template.sh`: a structured loop when a human must perform the repro steps.
- `NOTICE.md`: attribution and licenses.
