# Decision summary (handoff to spec)

Draft it when the frontier is empty, show it to the human, and change nothing after they confirm. Keep each line short; the spec expands it.

```markdown
<!-- vflow:decision-summary -->
## Decision summary: <feature>

**Source:** grill session, <date>. **Tracker issue:** <title with link, or "none">. **Confirmed by:** <human>, <date>.

### Problem and goal
<one or two lines: the problem, for whom, how we know it worked>

### Settled decisions
- D1. <decision>: <why, one line> (Q<n>)
- D2. ...
<If a design fork existed: "Approach: <chosen>. Rejected: <option>: <reason>.">

### Open assumptions
None.
<Otherwise list each with who decides and by when. Spec must not start while any remain unless the human says so.>

### Deferred or out of scope (decided by the human)
- <item>: <reason>

### Glossary terms touched
- **<Term>**: added | changed | flagged conflict (<file>)

### ADRs written
- <docs/adr/NNNN-slug.md: title> | none

### Facts looked up
- <fact>: <source (file, doc link)>

### Verification-level hint (provisional; spec makes the final call)
**Level:** A | B | C | A + B
- Q1 named states/statuses: <yes/no + which>
- Q2 concurrency, duplicate, late, or out-of-order events: <yes/no + which>
- Q3 money or exactly-once effects: <yes/no + which>
- Q4 rule or calculation with a law for all inputs: <yes/no + which>
**Reason:** <one line>. Candidate invariants or properties: <plain-language seeds, not numbered yet>.

### Next
Run `spec` with this summary.
```

Rules:
- The level definitions are the `spec` skill's `references/verification-levels.md`: any yes to Q1–Q3 means A; Q4 alone means B; none means C; unsure means A.
- Do not number invariants (`INV-n`) or properties (`PROP-n`); `spec` assigns ids.
- No file paths or code in decisions, except a state list that encodes a decision.
- Posting: on the tracker issue as a comment (same lookup order and adapters as the rest of the family) when one exists; otherwise in the conversation.
