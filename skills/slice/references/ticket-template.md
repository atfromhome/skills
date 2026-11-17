# Ticket template

Title per repo convention (default `<Feature> NN — <topic>`, numbered from 01 in dependency order).

```markdown
## Parent
<link to the spec issue>

## What to build
The end-to-end behaviour this ticket makes work, from the user's perspective. Not a layer-by-layer list.
(Level A) Implements statechart transitions: <state> → <state> on <trigger>; …

## Acceptance criteria
- [ ] <behaviour>. Satisfies INV-1.
- [ ] <behaviour>. Satisfies PROP-2.
- [ ] Verification on the PR head SHA: `verify-<area>` passes (A), property tests pass with pending tests for this ticket turned on (A/B), regular tests pass; results pasted in the PR.
- [ ] (A) No new state, transition, or interleaving outside the verified model; if one is needed, the model was updated and re-gated first.

## Blocked by
<links, or "None (can start immediately)". Omit when native blocking edges are set.>
```

## Prefactor ticket example (level A)

**Message delivery 01 — Model, property tests, and verify skill**
- What to build: commit the gated model, map each action to the code that performs it, add stateful tests that replay random orders of send / provider reports / duplicates / sweep and assert INV-1..3, and generate `verify-message-delivery`.
- Acceptance: the verify skill catches a scratch break (rank-only merge) and passes after it is dropped; property tests exist (pending where behaviour is unbuilt); no product behaviour change.
- Blocks: every other ticket of this spec.

## Local markdown variant
Same sections in `.scratch/<feature-slug>/issues/NN-<slug>.md`, plus `**Status:** ready-for-agent` and `**Blocked by:**` lines.

Avoid file paths and code snippets except a state table or type shape from a prototype that encodes a decision precisely.
