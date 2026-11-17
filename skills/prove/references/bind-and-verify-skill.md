# Bind mode: the prefactor ticket

The first ticket of a level-A spec (and of level B, for properties) makes the verification real in the repo **before** behaviour changes. Derived from pstack's create-formal-verification-skill, narrowed to a model that already passed the gate.

## Steps
1. Branch per repo convention. Never commit to a protected branch.
2. Copy the gate's model into the repo's model path (config `paths.models`, default `verification/<area>/`). Keep the gate's invariant names and `\* INV-n` comments.
3. **Map model to code.** For each action, name the function/handler/query that performs it, and confirm it is one atomic step in code (or will be, per the ticket plan). Write this mapping into the verify skill. If code already exists and does not match the model, that is a finding: report it on the spec; do not quietly change the model.
4. **Code-level properties.** Add stateful/property tests in the repo's PBT library (see `spec` references) that drive random sequences of the model's actions against the real code and assert the same `INV-n`. They may fail now if the behaviour is not built yet; mark them clearly (skipped/expected-fail per the language's idiom) and the ticket that builds the behaviour turns them on.
5. **Generate the project-local verify skill** in the repo's skills directory (config `paths.verify_skill`; match where the repo keeps agent skills: `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`…). Use the template below. Real commands, paths, nouns; no placeholders.
6. **Prove it.** Follow the generated skill once as a cold agent would, on a scratch change that breaks an invariant in real code (or in the model if the code does not exist yet). It must catch it. Drop the scratch change and confirm the check is back to its starting point.
7. Commit on the ticket branch and hand back to `ship`, which sends it to `check`. The PR (written with `pr`) carries the model, tests, verify skill, the run output, and the break you used. No product behaviour change.

## Verify skill template

```markdown
---
name: verify-<area>
description: "Check changes to <area> (<one line of what it promises>) against its TLA+ model and property tests. Use before opening or reviewing any PR that touches <covered paths or modules>, or when a counterexample or drift is suspected."
---

# verify-<area>

**Promise:** <INV-1 sentence>. <INV-2 sentence>. **Harm if broken:** <one sentence>.

## Covered code (sync commit: <full SHA>)
| Model action | Code | Atomic as |
|---|---|---|
| WebhookArrives | <module/function> | one DB transaction with conditional update |

## Run
- Model: `<exact TLC command>`  (expect: no error; ~<n> states, <seconds> s)
- Code properties: `<exact test command>`
- Read results with the `statechart` skill if installed; otherwise `<fallback command>`.

## Does my change touch this?
Yes if it edits covered code, adds a new writer of <guarded fields/tables>, adds a state or transition, or changes retry/timeout/concurrency around it.

## Real bug or modelling error?
Replay the counterexample step by step against the code. Any step impossible in code → the model is wrong: fix the model and say what was wrong. Every step possible → bug: report it with the steps in code words. Never weaken an invariant to pass.

## Intended change
Update the model from the code (not from the result), rerun, show a broken variant still fails, then move the sync commit to the commit you checked. Bigger drift: use the `prove` skill in maintain mode.
```
