---
name: flow
description: "Verified-flow orchestrator: take a feature from idea to merge-ready tickets with verification decided BEFORE code. Routes work through wayfinding (big, foggy efforts), a spec with a mandatory verification level, a formal pre-implementation gate (TLA+/TLC model plus statechart) for state machines, concurrency, or money, and tracer-bullet tickets; also tells implementers and QA how to honour the verified design. Use whenever someone wants to plan, spec, ticket, implement, or QA a feature through an issue tracker, mentions FSMs, status transitions, race conditions, payments, invariants, formal verification, or asks 'where are we in the flow' on a spec or ticket, even if they do not name this skill."
license: "MIT. Derived from mattpocock/skills and cursor/plugins pstack; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# flow: verified flow

One workflow, five skills. This one decides **where a piece of work is** and **which skill runs next**. The others do the work:

| Phase | Skill | Output |
|---|---|---|
| 0. Orientation (only for big, foggy efforts) | `chart` | A map of decision tickets that ends in a clear destination |
| 1. Spec | `spec` | Spec issue with a **verification level** and plain-language invariants/properties |
| 2. Formal gate (level A only) | `prove` | TLA+ model + statechart that TLC passes, attached to the spec |
| 3. Tickets | `slice` | Vertical slices, prefactor first, published as sub-issues in dependency order |
| 4. Implement / QA | this skill, `references/roles.md` | Code that follows the verified design; QA reruns verification on the same SHA |

Load the next skill by name when you reach its phase. Do not copy its steps here.

## Ground rules (apply in every phase)

1. **The issue tracker is the source of truth.** Specs, gate records, tickets and their status live there. An orchestrator (Multica, Linear automations, a CI bot) only drives the flow and may keep a *mirror* that holds a title and a pointer. On conflict, the tracker wins. See `references/tracker.md`.
2. **Find the tracker before you write anything.** Resolve it with the lookup order in `references/tracker.md`: a repo tracker doc, then a vflow config, then GitHub Issues via `gh`, then local markdown. Use the repo's own labels and conventions when it has them; fall back to the defaults in `references/config.md`.
3. **Verification is decided in the spec, before code.** Every spec carries one level:
   - **A — formal:** state machines, status transitions, retries, concurrency, idempotency, money or anything that must not happen twice. TLA+ model checked by TLC plus a statechart, **passed before the spec is split into tickets**.
   - **B — property:** rules or calculations without a state machine. Property-based tests in the repo's language, properties written in the spec first.
   - **C — example:** simple UI/CRUD. Regular tests plus QA.
   If unsure, choose A. Levels can combine (A covers the flow, B covers a calculation inside it).
4. **Stop for a human at the two pause points:** the seams check in `spec` and the ticket quiz in `slice`. Also stop when the formal gate is blocked or fails. Never answer the human's side yourself.
5. **Never push to or merge into the default branch** (`main`, `master`, `trunk`, `*/trunk`, or whatever the repo protects). Work on branches; humans merge.
6. **Never skip a gate silently.** Missing tools, a failing check, or a stale model are reported on the spec/ticket and to the human. Only a human can waive a gate, and the waiver is recorded with a reason.

## Route the request

Read the issue (or conversation) and pick the first row that matches:

1. The effort is larger than one session and the route is unclear → `chart`. A cleared map hands off to step 2.
2. The deciding is done but there is no spec issue, or the spec lacks a verification level → `spec`.
3. Spec is level A and has no current **passed** (or human-waived) gate record → `prove` in **gate** mode.
4. Spec is ready (level B/C, or level A with a current gate record) and has no tickets → `slice`.
5. A ticket is being implemented or reviewed → `references/roles.md`.
6. Code or design changed under an existing model, or QA reports the model no longer matches the code → `prove` in **maintain** mode.

"Current" gate record: its recorded spec revision matches the spec's current Testing Decisions and invariants. If the invariants changed after the gate, the gate is stale; go back to row 3.

## Status reporting

When asked "where are we", answer with: the spec (by title, with link), its verification level, gate status (`pending`, `passed`, `failed`, `blocked`, `waived`, `stale`, or n/a), tickets open/closed with the frontier, and the next skill to run. Refer to issues by title, with the id inside the link, never as a bare `#123` list.

## References

- `references/tracker.md`: tracker lookup order, the operations every phase needs, adapters (GitHub, GitLab, Linear, Jira, local markdown), and mirroring into an orchestrator.
- `references/config.md`: optional repo config (labels, paths, default branch, PBT library, toolchain) with defaults.
- `references/roles.md`: implementer and QA hooks, branch rules, drift handling.
- `NOTICE.md`: upstream attribution and licenses.
