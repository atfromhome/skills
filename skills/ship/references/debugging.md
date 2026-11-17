# Diagnosing an unclear failure

Adapted from mattpocock/skills `diagnosing-bugs`. Use when a test fails, or code misbehaves, and the cause is not obvious. Skip a phase only with a stated reason.

**Redact secrets** in every command, output, and artifact you show (`<REDACTED>`). Keep credentials in environment variables, not in the loop's text.

## 1. Build a feedback loop (most of the work)

You need **one command** that goes red on this exact symptom and green once fixed. Ways to get one, roughly in order: a failing test at a seam that reaches the bug; an HTTP script against a dev server; a CLI run diffed against a known-good output; a headless browser script; replaying a captured payload or event log; a throwaway harness around the code path; a property or fuzz loop for "sometimes wrong"; a bisection harness for "it used to work" (`git bisect run`); a differential run of old against new. Last resort, when a human must click: copy `scripts/hitl-loop.template.sh`, edit the steps, and run it so the human's observations come back as `KEY=VALUE` lines.

Then tighten it: faster (narrow scope, skip setup), sharper (assert the exact symptom, not "did not crash"), deterministic (pin time, seed randomness, isolate files and network). For flaky bugs, aim for a higher reproduction rate: loop, parallelise, add stress.

Done when the command has been run at least once and is red-capable, deterministic, fast, and runs without a human (except through the template). If no loop is possible, stop, list what you tried, and ask for access, a redacted artifact, or permission to instrument. **No loop, no hypotheses.**

## 2. Reproduce and minimise

Confirm the loop shows the symptom that was reported, not a neighbouring failure, and that it repeats. Then cut inputs, steps, config, and data one at a time until every remaining part is needed for red.

## 3. Hypothesise

Write 3–5 ranked, falsifiable hypotheses: "If X is the cause, changing Y makes it go away." Show the list to the human (they may re-rank it at once), but keep going if they are away.

## 4. Instrument

One probe per prediction; change one thing at a time. Prefer a debugger, then targeted logs at the boundaries that separate hypotheses. Tag every debug log with a unique prefix (`[DEBUG-a4f2]`) so cleanup is one search. For performance, measure a baseline and bisect instead of logging.

## 5. Fix with a regression test

Write the regression test first, at a seam that reproduces the real bug pattern. Watch it fail, fix, watch it pass, then rerun the original loop. If no correct seam exists, that is a finding: say so instead of adding a shallow test.

**vflow:** if the loop shows the code breaking an `INV-n` the model says holds, replay the steps against the model. A step the model does not allow means the code left the design: stop and route to `prove` maintain. Never change the model or invariant to make the failure go away.

## 6. Clean up

- [ ] the original loop is green
- [ ] the regression test passes, or the missing seam is written down
- [ ] every tagged debug line is removed (search the prefix)
- [ ] throwaway harnesses are deleted
- [ ] the confirmed hypothesis is in the commit message
