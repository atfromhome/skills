# Maintain mode: drift loop

Derived from pstack's maintain-formal-verification-skill. Use after merges, refactors, or design changes that touched verified code without rechecking it, or when QA reports drift.

## Outcomes (one per check, say which)
- **in sync**: nothing since the sync commit changes what the check describes; it passes.
- **updated**: the code changed, the verification now describes it, and it passes.
- **bug**: the verification describes the current code and the code breaks the property.
- **blocked**: could not be brought in line or could not run; say exactly why.
A check can be both updated and bug.

## Edit scope
Only models, harnesses, property files, and the verify skill. Never product code, unless the human asks. Never weaken a property or model to pass.

## Pass
1. **Find the checks**: project skills that run a model checker, prover, or property suite against named code (e.g. `verify-*`). Collect property, covered code, bounds, command, sync commit. No verify skill → bind mode first. No sync commit → use the last commit that changed the verification files, and say so.
2. **Run as-is** and record the result. A pass only means the old description still holds.
3. **Read every change** to covered code from the sync commit to HEAD, plus moved/renamed code and new writers of guarded state. Classify each: no effect / verification no longer describes the code / promise changed on purpose (cite evidence: docs, tests, changelog, commit message) / promise may be broken.
4. **Update from the code**, not from the result. Keep one atomic step in code as one action. Change a property only for an intended promise change; write old wording, new wording, evidence. Keep bounds unless the change makes them wrong; report any reduction.
5. **Rerun and judge.** Pass → break the new code the way the property guards against and confirm the check catches it, then drop the break. Fail → replay the counterexample against real code: impossible step = verification wrong (fix it, say what); all steps possible = bug (name the introducing commit, steps in code words, harm in one sentence; a cheap repro test may go in the report, not in product code).
6. **Update the verify skill**: coverage, commands, bounds, assumptions, sync commit = the commit you checked (not for blocked checks). Follow it once as the next agent would.
7. If the **spec's** states, transitions, or invariants changed, also post a fresh gate record on the spec (gate mode) so the gate is not left stale.

## Report
Per check: outcome and commits read; what changed in the verification and why; rerun result and the break used; each bug in plain words with the introducing commit; what is still not covered. Say outright which failures were drift and which were bugs, and when an earlier pass was on a stale description. Put verification updates in their own change, separate from any product fix.
