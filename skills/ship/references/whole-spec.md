# Whole-spec mode

Adapted from mattpocock/skills `implement-spec`. Goal: the whole spec on one integration branch, every ticket resolved the way the tracker closes work, nothing on a protected branch.

## The task graph

Tickets are not a list; they are a graph with blocking edges (native "blocked by" links, or `## Blocked by` sections). The **frontier** is every open ticket whose blockers are done (merged into the integration branch). Ticket 01, the prefactor, is the whole first frontier for a level A or B spec.

## Steps

1. **Read** the spec, its gate record (level A), and every ticket. Draw the graph and say the first frontier.
2. **Optional exploration.** An exploration subagent reads the code and docs the tickets need and saves notes in a folder outside the repo that later subagents can read. Implementers then build instead of explore.
3. **Integration branch** from the default branch (default name `<spec-slug>/integration`).
4. **Ticket 01 alone.** Level A: `prove` bind mode. Level B: property tests per `PROP-n`. Merge into the integration branch, run the full suite, push the branch.
5. **Draft PR** after that first merge (a branch with no commits ahead cannot open one): integration branch → default branch, titled after the spec, body listing the spec and every ticket with the tracker's closing keyword (see `flow`'s `references/tracker.md`). Mark it draft. Skip if the repo does not work through PRs and the human did not ask for one.
6. **Implementers.** For each frontier ticket, a fresh subagent with a clean context, in the background where possible:
   - its own worktree (`git worktree add`) on its own ticket branch based on the integration branch tip; it confirms the base before starting and resets onto it if wrong;
   - receives pointers only: spec link, ticket link, notes folder, relevant commits; no copied text;
   - runs `ship` single-ticket steps 3–6 (tests first from acceptance criteria and `INV-n`/`PROP-n`);
   - merges the integration tip into its branch and reruns tests before reporting;
   - reports sparsely: branch, commits, commands with results, blockers hit.
7. **Merge.** A merger subagent (or you) merges each finished ticket branch into the integration branch, resolves conflicts without changing tested behaviour, runs the full suite and, for level A, `verify-<area>`. Red after a merge: fix on a branch before merging anything else.
8. **Recompute the frontier** after every merge and start newly unblocked tickets. Parallel tickets must not touch the same verified action at once; if two do, run them in sequence.
9. **A stop from any implementer** (model gap, failing invariant, missing seam) pauses the tickets that depend on it. Report it; route to `prove` or the human.
10. **Finish:** every ticket merged, full suite green on the integration tip. Remove the worktrees. Hand the integration branch and draft PR to `check`.

## Without subagents

Same graph and branches, one ticket at a time, in frontier order. Keep each ticket on its own branch so `check` can map commits to tickets.
