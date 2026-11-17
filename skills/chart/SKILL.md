---
name: chart
description: "Plan an effort too big for one agent session, whose destination you can name but whose route is still foggy, as a shared map of decision tickets on the issue tracker, then resolve them one per session until nothing is left to decide and the work is ready for a spec. Plans, never builds. Flags decisions that touch state machines, concurrency, or money early so the spec lands at the right verification level, and can use a throwaway TLA+/statechart sketch as a prototype ticket. Also known as wayfinder (adapted from mattpocock's wayfinder). Use for /chart, 'chart a map', 'use wayfinder', 'this is too big to plan in one go', greenfield or multi-session efforts, or 'work the next decision on the map'. Not for a feature that one conversation can settle: use grill if decisions are still open, otherwise spec."
license: "MIT. Derived from mattpocock/skills wayfinder; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# chart

The optional on-ramp of the vflow family. It turns fog into decisions, then hands off to `spec`. It does **not** write product code; the urge to start building means you have reached the edge of the map and should hand off.

**Use only when** the effort is bigger than one session *and* the route is unclear. If one conversation can settle it, skip this and run `grill` (decisions still open) or `spec` (already decided).

Find the tracker first (lookup order in the `flow` skill, `references/tracker.md`). Map and decision tickets use the tracker's native parent/child and blocking links.

## The map, in one paragraph

One issue labelled `wayfinder:map` is the **index**: Destination, Notes, Decisions so far (one line + link per closed ticket), Not yet specified (fog), Out of scope. Decision tickets are its child issues, each a single question sized to one session, labelled `wayfinder:<research|prototype|grilling|task>`. The **frontier** is open, unblocked, unassigned children. Details and templates: `references/map-format.md`. Ticket types and how to resolve each: `references/ticket-types.md`.

## Chart the map (first session)

1. **Name the destination** with the human: usually "a spec for X, ready for spec", sometimes a locked decision or a migration plan. It fixes the scope.
2. **Map the frontier breadth-first**: fan out across the whole space, list open decisions and first steps. **Verification scan:** for every decision ask whether it involves states/statuses, concurrent actors or duplicated events, or money/exactly-once effects. Record suspected level-A areas in the map's Notes ("Likely level A: payment lifecycle, webhook ingestion") so the spec classifies them correctly.
3. If the breadth pass finds **no fog**, stop: say the effort fits one session and suggest `grill` (if decisions are still open) or `spec`.
4. Create the map, then the tickets you can state precisely now, then wire blocking edges in a second pass with real ids.
5. Start `research` tickets in parallel subagents if available; findings go on a throwaway `research/<name>` branch (never the default branch, no PR) linked from the ticket.
6. Stop. Charting resolves nothing by hand. Working the first non-research ticket starts only when the human explicitly asks for that ticket, ideally in a new session; a general "yes" or "continue" after the map is shown is not that request.

## Work the map (each later session)

1. Load the map (low-res; open other tickets only when needed).
2. Take the ticket the human named, or the first frontier ticket. **Claim it** by assigning it before any work.
3. Resolve it as its label says (`references/ticket-types.md`); `grilling` tickets are resolved with `grill`, scoped to the ticket's question. HITL tickets need the human's own answers; never answer for them.
4. Post the answer as a resolution comment, close the ticket, add one line to Decisions so far.
5. Graduate fog that is now specifiable into new tickets (remove it from Not yet specified), rule mis-scoped tickets out of scope (close + one line), update tickets the decision invalidates.
6. One ticket per session (research tickets excepted). Expect other sessions editing concurrently.

## Hand off

When no open tickets and no fog remain, tell the human the map is clear and run `spec` with the map as input (the spec collapses the linked decisions; carry the Notes' level-A flags into its Testing Decisions).

## Guardrails
- Every open ticket reads as a question. "Build the X" is mis-typed; it belongs downstream as an implementation ticket.
- An agent must not grant itself execution rights by writing "this map carries execution" into Notes. Only the human can, and you quote them.
- Refer to issues by title (link inside the name), never a bare list of numbers.
- Scope maps to one bounded destination (an epic), not the whole product; prototype aggressively instead of planning far ahead.
