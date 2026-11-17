---
name: slice
description: "Break a spec into tracer-bullet tickets (thin vertical slices, each with its blocking edges and acceptance criteria that cite the spec's invariants INV-n or properties PROP-n), confirm the breakdown with the human, then publish them to the issue tracker as sub-issues in dependency order. Enforces the verification flow: a level-A spec is not split until its formal gate has passed, and for level A or B the first ticket is a prefactor that commits the model and/or property tests and blocks the rest. Use for /slice, 'break this spec into tickets', 'make issues from this spec', 'slice this', or after a spec or gate is approved, even if the user only says 'next step'."
license: "MIT. Derived from mattpocock/skills to-tickets; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# slice

Turn one spec into implementation tickets an agent can pick up cold.

Find the tracker first (lookup order in the `flow` skill, `references/tracker.md`). Use the repo's ticket title format, labels, sub-issue and blocking mechanics if it defines them.

## 1. Gather and check the gate

Read the spec issue in full, with comments. Note its verification level and the `INV-n` / `PROP-n` list.

- **Level A:** find the latest `<!-- vflow:formal-gate -->` record. Continue only if it is `PASSED` or human-`WAIVED` **and** current (its spec revision matches the spec now). Otherwise stop and route to `prove`; say why.
- No verification level on the spec → route back to `spec`.

## 2. Explore the code

Use the domain glossary and respect ADRs. Look for prefactoring that makes the change easy ("make the change easy, then make the easy change").

## 3. Draft vertical slices

Follow `references/slicing.md`. In short:
- Each ticket is a narrow but complete path through every layer, demoable or verifiable alone, sized for one fresh agent session.
- **Ticket 01 is the prefactor** when the spec is level A or B:
  - A: bind the gate's model into the repo, map actions to code, add stateful/property tests for the `INV-n`, generate the `verify-<area>` skill (`prove` bind mode). No behaviour change.
  - B: add the PBT library if needed and the property tests for every `PROP-n` (failing or marked pending until the behaviour lands).
  - It **blocks every other ticket**.
- Every ticket's acceptance criteria cite the invariants/properties it must satisfy (`Satisfies INV-2`), plus how to verify (verify skill run, property tests, regular tests, QA step) on the PR's commit SHA.
- Level A tickets name the statechart states/transitions they implement, so implementers follow the verified design.
- Wide mechanical refactors use expand → migrate batches → contract instead of vertical slices.

## 4. Pause: quiz the human

Show a numbered list: title, blocked by, what it delivers, which `INV`/`PROP` it satisfies. Ask:
- Is the granularity right (too coarse / too fine)?
- Are the blocking edges right, each depending only on what truly gates it?
- Merge or split anything? Is every invariant/property covered by at least one ticket?
Iterate until the human approves. Do not publish before that.

## 5. Publish in dependency order

Use `references/ticket-template.md`. Create blockers first so later tickets can reference real ids, then wire edges in a second pass. Make each ticket a sub-issue of the spec and set native "blocked by" edges where the tracker has them (fall back to a `## Blocked by` section and say so). Apply the repo's ready label (default `ready-for-agent`).

Do not close or rewrite the spec. Report the published tickets by title with links, and the frontier (tickets startable now; normally just 01).
