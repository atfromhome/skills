# The Verification axis

New in vflow. It answers one question with evidence: does this SHA do what the ticket promised, under the rules the spec set?

## Steps

1. **Check out the head SHA** and record it. Every result below is for this SHA.
2. **Run the oracle:**
   - the repo-local `verify-<area>` skill, as written (its model command and its code-property command);
   - the property tests (level A and B), with any pending tests this ticket owns now turned on;
   - typecheck and the full test suite.
   Record each command, its exit code, and its pass/fail counts.
3. **Level A model check.** Compare the diff with the verify skill's covered code and sync commit. If the model files changed, or code mapped to a model action changed, re-run the model check (TLC command in the verify skill) and say so. If the spec is level A and no verify skill exists, that is a finding: ticket 01 (`prove` bind) is missing or incomplete.
4. **Tick every acceptance criterion** with one piece of evidence on this SHA:
   - a test name plus its output line, or
   - a command plus its output, or
   - a screenshot for visible UI behaviour.
   A criterion with no evidence stays unticked and is a finding. "Tests pass" is not evidence for a specific criterion. For a prefactor criterion such as "the verify skill catches a scratch break", repeat the break yourself in a scratch worktree, show the failing run, drop the break, and show the clean run.
5. **Map coverage.** Each `INV-n` / `PROP-n` the ticket cites → the test (or model invariant) that covers it. An unmapped rule is a finding.
6. **Look for drift.** Does each changed function still map to one model action and one atomic step? A new writer of guarded state, a new state or transition, or a counterexample that cannot be replayed in code means drift: report "model drift" and route to `prove` maintain, even if TLC and every test pass (a pass on a stale model proves nothing).
7. **Counterexamples and failing properties** are replayed against the real code before calling them bugs. Impossible step in code → the model is wrong (drift). Every step possible → a bug.

## Tables for the report and the PR body

```markdown
**Checked SHA:** <full sha>

| Acceptance criterion | Evidence | Result |
|---|---|---|
| Late delivery report corrects a sweep failure. Satisfies INV-1 | `delivery_test: late_report_corrects_sweep` → ok | ✅ |
| Duplicate webhook is a no-op. Satisfies INV-3 | `make test-one T=webhook_idempotent` → 1 passed | ✅ |

| Rule | Covered by | Result |
|---|---|---|
| INV-4 Delivered is never shown as failed | model `DeliveryReportWins`; property `delivery_state_machine` | holds |

| Command | Exit | Result |
|---|---|---|
| `<verify skill model command>` | 0 | no error, <n> states |
| `<full suite command>` | 0 | <n> passed, 0 failed |
```
