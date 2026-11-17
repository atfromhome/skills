# Spec template

Publish as one issue. Title per repo convention (default `<Feature> — spec`). Labels: spec label + level label (+ `formal-gate:pending` for A).

```markdown
## Problem Statement
The problem from the user's perspective.

## Solution
The solution from the user's perspective.

## User Stories
A long, numbered list covering every aspect of the feature.
1. As a <actor>, I want <feature>, so that <benefit>

## Implementation Decisions
Modules built or changed and their interfaces, architectural decisions, schema changes, API contracts, specific interactions. No file paths or code snippets (exception: a state table, transition list, or type shape that encodes a decision precisely).

## Testing Decisions
**Verification level:** A | B | C (combined: e.g. "A (lifecycle) + B (fee rounding)")
**Why:** Q1 … / Q2 … / Q3 … / Q4 … (one line each, see the classification questions)

**Seams:** where tests run (prefer the highest existing seam; ideally one). Prior art: similar tests already in the repo.
What makes a good test here: external behaviour only, not implementation details.

### Level A — model scope (only if A)
- States: …
- Transitions (trigger → from → to): …
- Concurrent actors / duplicated, delayed, or reordered events: …
- Out of model (and why): …

### Invariants (A) / Properties (B)
- INV-1 (safety): …
- INV-2 (liveness, fairness assumption: …): …
- PROP-1: <law> over <input space>; must include edge cases: …

### Example cases (C, or extra for A/B)
- …

### Gate
Level A only: this spec cannot be split into tickets until `prove` records a passed (or human-waived) gate on this issue. The model and statechart are attached in that record.

## Out of Scope
…

## Further Notes
Revisions, links to the wayfinder map or prototypes, open risks.
```

## Example (abridged, level A)

**Title:** Message delivery status — spec

- Verification level: A. Q1 yes (queued → sending → delivered/read/failed). Q2 yes (provider webhooks arrive late or twice; a cleanup sweep marks stuck messages failed). Q3 no. Q4 no.
- INV-1: Status never moves backwards, except that a late `delivered`/`read` report corrects a `failed` set by the cleanup sweep.
- INV-2: Every message in `sending` eventually reaches a final state (fairness: the sweep eventually runs).
- INV-3: Applying the same webhook twice leaves the same status as applying it once.
- INV-4: Once the provider's delivery report has been applied, the message is never shown as `failed`. (Without this rule INV-1..3 still hold for the buggy rank-only merge, so the gate could not catch the very problem the spec is about. Name the harm in the Problem Statement as an invariant.)

## Example (abridged, level B)

**Title:** Donation report CSV export — spec

- Verification level: B. Q1–Q3 no. Q4 yes (export must match the filtered report).
- PROP-1: Row count in the CSV equals the number of records matching the filter.
- PROP-2: Sum of the amount column equals the on-screen total for the same filter.
- PROP-3: Parsing the CSV back yields the original field values, including commas, quotes, newlines, and non-ASCII names.
