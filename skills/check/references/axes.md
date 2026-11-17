# Axis prompts

Give each subagent a fresh context and only what it needs. Each brief asks for under 400 words. Every axis reports for the same head SHA.

## Standards

Include: the diff command and commit list; the standards-source files found in step 1; the full text of `smells.md` (the subagent cannot see it otherwise).

Brief: "Report, per file or hunk: (a) each place the diff breaks a documented standard, citing the file and the rule; (b) any baseline smell, named and with the hunk quoted. Documented-standard breaches can be hard failures; baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip what tooling enforces. Note refactors worth doing now that the tests are green. Under 400 words."

## Spec

Include: the diff command and commit list; links to (or the text of) the ticket(s) and the parent spec.

Brief: "Report: (a) requirements in the ticket or spec that are missing or partial; (b) behaviour in the diff nobody asked for (scope creep); (c) requirements that look implemented but wrongly. Quote the spec or ticket line for each finding. For level A, also flag any state, transition, or interleaving in the code that the spec's state list does not have. Under 400 words."

No spec: skip this subagent and say "no spec available" in the report.

## Verification

Include: the head SHA; the ticket(s) with their acceptance criteria; the spec's level and `INV-n` / `PROP-n` list; the latest gate record (level A); the commands discovered; the path of the repo-local `verify-<area>` skill if one exists; the full text of `verification.md`.

Brief: "Follow verification.md on the head SHA. Run every command yourself in this session; do not reuse earlier output. Return: the acceptance-criteria table with evidence, the INV/PROP coverage table, the commands with exit codes and failure counts, the model check result (level A), and any drift. Under 400 words plus the tables."

## Without subagents

Run the same three briefs in sequence, one pass each. Write each axis's findings before reading the inputs of the next, so one axis does not colour another.
