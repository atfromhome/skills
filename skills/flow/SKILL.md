---
name: flow
description: "Verified-flow orchestrator: take a feature from idea to a reviewed PR with verification decided BEFORE code. Routes work through wayfinding (big, foggy efforts), a grilling interview (small but fuzzy features), a spec with a mandatory verification level, a formal pre-implementation gate (TLA+/TLC model plus statechart) for state machines, concurrency, or money, tracer-bullet tickets, implementation (ship) and three-axis QA (check) that ends in a PR. Use when someone wants to drive a feature through the whole flow, asks 'where are we', 'what's next' or 'what runs now' on a feature, spec or ticket, mentions FSMs, status transitions, race conditions, payments, invariants or formal verification without naming a step, or when it is unclear which vflow skill applies, even if they do not name this skill."
license: "MIT. Derived from mattpocock/skills and cursor/plugins pstack; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# flow: verified flow

One workflow, eight skills (plus the standalone `pr` for PR bodies). This one decides **where a piece of work is** and **which skill runs next**. The others do the work:

| Phase | Skill | Output |
|---|---|---|
| 0. Orientation (only for big, foggy efforts) | `chart` | A map of decision tickets that ends in a clear destination |
| 0b. Deepen context (fits one session, decisions still open or fuzzy) | `grill` | A confirmed Decision summary with a provisional verification level |
| 1. Spec | `spec` | Spec issue with a **verification level** and plain-language invariants/properties |
| 2. Formal gate (level A only) | `prove` | TLA+ model + statechart that TLC passes, attached to the spec |
| 3. Tickets | `slice` | Vertical slices, prefactor first, published as sub-issues in dependency order |
| 4. Implement | `ship` | Tested commits on ticket branches (prefactor first; level A runs `prove` bind there), merged into an integration branch for a whole spec |
| 5. QA | `check` | Standards, Spec, and Verification findings side by side; every acceptance criterion ticked with evidence on one SHA |
| 6. PR | `pr` (called by `check`) | PR body with summary, evidence, merge danger, and INV/PROP coverage; linked to close the ticket; humans merge |

Load the next skill by name when you reach its phase. Do not copy its steps here.

## Ground rules (apply in every phase)

1. **The issue tracker is the source of truth.** Specs, gate records, tickets and their status live there. An orchestrator (Multica, Linear automations, a CI bot) only drives the flow and may keep a *mirror* that holds a title and a pointer. On conflict, the tracker wins. See `references/tracker.md`.
2. **Find the tracker before you write anything.** Resolve it with the lookup order in `references/tracker.md`: a repo tracker doc, then a vflow config, then GitHub Issues via `gh`, then local markdown. Use the repo's own labels and conventions when it has them; fall back to the defaults in `references/config.md`.
3. **Verification is decided in the spec, before code.** Every spec carries one level:
   - **A — formal:** state machines, status transitions, retries, concurrency, idempotency, money or anything that must not happen twice. TLA+ model checked by TLC plus a statechart, **passed before the spec is split into tickets**.
   - **B — property:** rules or calculations without a state machine. Property-based tests in the repo's language, properties written in the spec first.
   - **C — example:** simple UI/CRUD. Regular tests plus QA.
   If unsure, choose A. Levels can combine (A covers the flow, B covers a calculation inside it).
4. **Stop for a human at the pause points:** the scope check and the shared-understanding confirmation in `grill`, the seams check in `spec`, the ticket quiz in `slice`, and the findings review in `check` (before any fix). Also stop when the formal gate is blocked or fails, and when `ship` finds the code must leave the verified model. Never answer the human's side yourself.
5. **Never push to or merge into the default branch** (`main`, `master`, `trunk`, `*/trunk`, or whatever the repo protects). Work on branches; humans merge.
6. **Evidence before claims.** Nobody says done, fixed, or passing without fresh command output from the current session.
7. **Never skip a gate silently.** Missing tools, a failing check, or a stale model are reported on the spec/ticket and to the human. Only a human can waive a gate, and the waiver is recorded with a reason.

## Route the request

Read the issue (or conversation) and pick the first row that matches:

1. The effort is larger than one session and the route is unclear → `chart`. A cleared map hands off to step 3.
2. The effort fits one session but key decisions are still open or fuzzy (no confirmed Decision summary, or the human asks to be grilled) → `grill`. A confirmed summary hands off to step 3.
3. The deciding is done but there is no spec issue, or the spec lacks a verification level → `spec`.
4. Spec is level A and has no current **passed** (or human-waived) gate record → `prove` in **gate** mode.
5. Spec is ready (level B/C, or level A with a current gate record) and has no tickets → `slice`.
6. `ship` or `check` reported drift (the code no longer matches the model), or code or design changed under an existing model without a recheck → `prove` in **maintain** mode.
7. Tickets are published and the frontier has open tickets (or the human names one to build) → `ship` (single ticket, or whole spec).
8. A ticket or integration branch has commits to review, or a PR needs QA → `check`. Fixes it asks for go back to `ship`; a clean check ends with a PR body from `pr`.

"Current" gate record: its recorded spec revision matches the spec's current Testing Decisions and invariants. If the invariants changed after the gate, the gate is stale; go back to row 4.

## Status reporting

When asked "where are we", answer with: the spec (by title, with link), its verification level, gate status (`pending`, `passed`, `failed`, `blocked`, `waived`, `stale`, or n/a), tickets open/closed with the frontier, open PRs and their check verdict, and the next skill to run. Refer to issues by title, with the id inside the link, never as a bare `#123` list.

## References

- `references/tracker.md`: tracker lookup order, the operations every phase needs, adapters (GitHub, GitLab, Linear, Jira, local markdown), and mirroring into an orchestrator.
- `references/config.md`: optional repo config (labels, paths, default branch, PBT library, toolchain) with defaults.
- `references/roles.md`: the implementer and QA rules that `ship` and `check` carry out, as a short checklist for agents that have neither installed.
- `NOTICE.md`: upstream attribution and licenses.
