---
name: prove
description: "Formally verify a design BEFORE implementation and keep the verification true afterwards. Gate mode models a level-A spec (state machine, status transitions, retries, webhooks, queues, concurrency, money) in TLA+, checks it with TLC, draws a statechart, and records pass/fail on the spec so tickets cannot start until it passes. Bind mode (prefactor ticket) commits the model, ties it to real code, and generates a project-local verify skill. Maintain mode brings the model back in line after code or design drift and says whether each failure is drift or a real bug. Use for /prove, 'model-check this', 'verify the state machine', 'check this race', 'is the model still true to the code', or whenever a spec is level A, even if TLA+ is not mentioned."
license: "MIT. Derived from cursor/plugins pstack (statechart, create-formal-verification-skill, maintain-formal-verification-skill); see NOTICE.md"
compatibility: "TLC needs Java 11+ (17+ recommended) and tla2tools.jar. Optional: pstack statechart skill (Node 22.18+, mise). Fallback scripts need bash and python3."
metadata:
  version: "0.1.0"
  family: vflow
---

# prove

A test checks the cases someone thought of. TLC checks every order of steps in a small model. This skill uses that **before code exists**, so design bugs (illegal transitions, races, double processing, stuck states) are fixed on paper, then keeps the model honest as code arrives.

Three modes. Pick by situation:

| Mode | When | Result |
|---|---|---|
| **gate** | A level-A spec has no current passed gate | Model + statechart + gate record on the spec |
| **bind** | Running the level-A prefactor ticket | Model committed in the repo, mapped to code, project-local `verify-<area>` skill |
| **maintain** | Code or design changed under an existing model; QA reports drift | Outcome per check: in sync / updated / bug / blocked |

## Before any mode: toolchain

Run `scripts/check_toolchain.sh` (add `--fetch-tla2tools` to download the jar into the user cache, with the human's consent in shared environments). Details in `references/toolchain.md`.
If TLC cannot run: **do not skip.** Record the gate as `blocked` on the spec with the exact problem, tell the human, and stop. Only a human may waive, and the waiver is recorded with their reason.

## Gate mode

1. **Read the spec**: states, transitions, concurrent actors, duplicated/late/reordered events, and the plain-language invariants `INV-n`. Model the *design*, not code; there may be no code yet. Name things in the spec's domain words.
2. **Write the model** in a scratch folder outside the repo, following `references/writing-the-model.md`: one INVARIANT per safety `INV-n` (never weakened to pass), properties with stated fairness for liveness `INV-n`, environment actions for everything that can arrive twice, late, or out of order, small constants.
3. **Prove the model can fail.** Make one deliberately broken variant (drop a guard, reorder two steps, remove a correction) and confirm TLC catches it. A check never seen failing proves nothing. Include the variant that reproduces the spec's Problem Statement (the bug the feature exists to prevent); if TLC passes it, the spec's invariants are incomplete: **pause**, propose the missing `INV-n` to the human, and revise the spec before gating.
4. **Check and draw.** Run TLC on the real design. Then draw the statechart in the reader's words (`references/statechart.md`): with the pstack `statechart` skill if it is installed (refer to it by name; do not copy its commands), otherwise `scripts/tlc.sh --dot` + `scripts/dot2mermaid.py`.
5. **Judge the result.**
   - Violation: tell the counterexample as numbered steps in domain words, say which `INV-n` breaks and the harm in one sentence. The fix is a **design** change in the spec (with the human), not a weaker invariant. Update spec and model, rerun.
   - Pass: say what the pass covers (constants, bounds, fairness, what the model leaves out).
6. **Record the gate on the spec** with `references/gate-record.md` (a comment with marker `<!-- vflow:formal-gate -->`): result, tool versions, model text, statechart Mermaid, invariant mapping, bounds, broken-variant evidence, spec revision. Set the gate label (`passed`, `failed`, `blocked`). **Pause** if failed or blocked: the human decides the design change or waiver.
7. Hand off: passed → `slice` (the first ticket will be **bind**).

## Bind mode (prefactor ticket)

Follow `references/bind-and-verify-skill.md`: commit the gate's model under the repo's model path, map every action to the code that performs it (one atomic step in code = one action), add the code-level property/stateful tests, generate a project-local `verify-<area>` skill with a coverage record and sync commit, and prove the skill catches a scratch break in real code. Product behaviour does not change in this ticket. Work on a branch; never push to a protected branch.

## Maintain mode

Follow `references/maintain.md`: find the verify skills, run them as-is, read every change to covered code since the sync commit, update the model from the code (not from the result), rerun, replay any counterexample against real code, and classify each check as in sync / updated / bug / blocked. Edit only verification files; product fixes go in a separate change. A spec-level design change also re-runs gate mode and refreshes the gate record.

## Never

- Weaken an invariant, shrink a bound, or delete an action to get a pass without saying so and getting the human's agreement.
- Mark a gate passed from memory or from an old run; every record cites a run you did on this spec revision.
- Change product code in gate or maintain mode unless the human asks.

## References
- `references/toolchain.md`: requirements, install options, graceful degradation.
- `references/writing-the-model.md`: TLA+ patterns for flows, webhooks, retries, workers, money.
- `references/statechart.md`: drawing the chart with pstack or the fallback, reader words, size budget.
- `references/gate-record.md`: the gate comment template and staleness rule.
- `references/bind-and-verify-skill.md`: prefactor ticket and the generated verify skill.
- `references/maintain.md`: drift loop and outcomes.
- `assets/MessageDelivery.tla` (+ `.cfg`, `Fixed.cfg`, `.words.json`, `view.example.mjs`): a worked example that fails with the rank-only merge and passes with the fix.
