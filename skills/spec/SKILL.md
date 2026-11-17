---
name: spec
description: "Turn an agreed feature (the current conversation, a grill Decision summary, a cleared wayfinder map, or an issue) into a spec on the issue tracker, with a mandatory verification level and plain-language invariants or properties written BEFORE any code. Classifies the work as A (state machine, status transitions, concurrency, retries, money: formal TLA+ gate first), B (rules or calculations: property-based tests), or C (simple UI/CRUD: regular tests). Use for /spec, 'write the spec', 'turn this into a spec', 'refine this issue', or whenever a feature is ready to be written down before ticketing, even if the user does not mention verification. Does not interview: if key decisions are still open, run grill first."
license: "MIT. Derived from mattpocock/skills to-spec; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# spec

Synthesize a spec from what is already known. Do not run a fresh interview: the deciding should already be done. If it is not, hand off and come back: to `chart` when the effort is big and foggy, to `grill` when it fits one session but decisions are still open or fuzzy.

Find the tracker first (lookup order in the `flow` skill, `references/tracker.md`: repo tracker doc → `.vflow.yml` → GitHub Issues via `gh` → local markdown). Use the repo's labels, title format, and glossary.

## Process

1. **Start from the Decision summary** if one exists (from `grill`, in the conversation or as a `<!-- vflow:decision-summary -->` comment on the issue). Its settled decisions are inputs, not questions to reopen; its level hint is provisional, so still answer the four questions below. If it lists open assumptions, settle them with the human (or send them back to `grill`) before writing.

2. **Explore.** Read the code and docs in the area: domain glossary, ADRs, existing tests and test helpers, and every place the affected entity changes status. List the states and the code that moves between them; that list feeds the classification.

3. **Sketch the test seams.** Prefer existing seams, the highest one possible, as few as possible (ideally one).

4. **Classify the verification level.** Follow `references/verification-levels.md`. Answer its four questions in writing. Any "yes" to Q1–Q3 means **A**; if unsure, **A**. Then draft:
   - Level A: a state list, the transitions with their triggers, and **invariants** `INV-1..n` in plain language (safety: "never…", "at most one…"; liveness: "every X eventually…"). Note which actors run concurrently and what can arrive twice, late, or out of order.
   - Level B: **properties** `PROP-1..n` in plain language plus the generators they need, and the PBT library for this language (`references/property-testing.md`).
   - Level C: the example cases that prove each user story.

5. **Pause: seams and level check with the human.** Show the seams, the level with the one-line reason, and the invariants/properties. Ask whether they match expectations. Stop until the human answers. Never answer for them.

6. **Write and publish the spec** with `references/spec-template.md`. Label it with the spec label and the level label. For level A also add the gate label `formal-gate:pending` (or the repo's equivalent) and say in Further Notes that the spec cannot be split into tickets until the formal gate passes.

7. **Hand off.**
   - Level A → `prove` (gate mode) with the spec reference.
   - Level B/C → `slice`.

## Revisions

If the spec's invariants, properties, states, or transitions change after a gate passed, edit the spec, mark the gate `stale`, and route back to `prove`. Keep a short "Revision" line in Further Notes with what changed.

## Writing rules

- No file paths or code snippets in the spec; they go stale. Exception: a state table, transition list, or type shape that encodes a decision more precisely than prose. Keep it to the decision-rich part.
- Invariants and properties are sentences a product person can judge. Each gets a stable id (`INV-3`, `PROP-2`) that tickets and tests cite.
- Never weaken an invariant to make the design easier. If the human relaxes one, record that as a decision.
