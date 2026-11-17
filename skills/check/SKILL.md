---
name: check
description: "QA a vflow ticket or integration branch before it can merge: a three-axis review run as parallel subagents. Standards checks the diff against the repo's documented rules plus a Fowler code-smell baseline (repo rules win; smells are judgement calls). Spec finds missing or partial requirements, scope creep, and wrong implementations, quoting the spec line. Verification runs the repo-local verify skill, re-runs the model check when the model or code mapping changed, ticks every acceptance criterion with evidence, maps each INV-n/PROP-n to its test, and flags drift for prove maintain. Reports the axes side by side, stops for the human before any fix, never claims passing without fresh output. When clean, writes the PR body with pr, opens the PR or marks the draft ready, linked so it closes the ticket; never merges. Use for /check, 'review this branch', 'QA this PR', 'is ticket 03 done', 'review since main', or after ship. Not for writing a PR description alone (pr) or model-checking a design (prove)."
license: "MIT. Derived from mattpocock/skills code-review, with the evidence rule from obra/superpowers verification-before-completion; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# check

The QA step of the vflow family. It reviews what `ship` built, proves each acceptance criterion with evidence, and only then opens the PR. It never fixes code itself and never merges.

Find the tracker first (lookup order in the `flow` skill, `references/tracker.md`).

## The evidence rule

Never say done, fixed, or passing without fresh command output from **this session**. For every claim: name the command that proves it, run it in full, read the exit code and the failure count, then state the result with the output. A previous run, a subagent's "success", or "should pass" is not evidence.

## 1. Pin what is under review

1. **Fixed point.** The branch the work will merge into: the integration branch for a ticket in whole-spec mode, otherwise the default branch, or what the human names. Resolve it (`git rev-parse`) and capture `git diff <fixed-point>...HEAD` and `git log <fixed-point>..HEAD --oneline`. A bad ref or empty diff stops here.
2. **Head SHA.** Record the exact commit you check. Every result in the report is for that SHA.
3. **Spec source**, first hit wins: ticket and spec references in commits, the branch, or the PR; a path the human gives; a spec file matching the branch under `docs/`, `specs/`, or `.scratch/`. Read the ticket(s), the parent spec, and the latest `<!-- vflow:formal-gate -->` record. No spec at all: ask; if there is none, the Spec axis reports "no spec available".
4. **Standards sources:** every file that says how code is written (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `docs/agents/`, linters' configs). Keep the list.
5. **Commands:** typecheck, tests, property tests, and the repo-local `verify-<area>` skill (in the repo's skills directory, config `paths.verify_skill`), discovered from the repo's docs.

## 2. Run the three axes

Start each axis as a **parallel subagent with a fresh context** (issue all three together). Without subagents, run them one after another as separate passes, finishing and writing down each axis before starting the next. Prompts and limits: `references/axes.md`.

- **Standards:** each violation of a documented rule (cite file and rule) and each baseline smell from `references/smells.md` (named, hunk quoted). Repo rules always win over the baseline; smells are always judgement calls, never hard failures. Skip what tooling enforces.
- **Spec:** (a) requirements missing or partial, (b) behaviour nobody asked for, (c) requirements implemented wrongly. Each quotes the spec or ticket line.
- **Verification:** follow `references/verification.md`. Run the verify skill, the property tests, and the full suite on the head SHA; for level A, re-run the model check if the model files or the code they map to changed since the verify skill's sync commit; tick every acceptance criterion with evidence; map each `INV-n` / `PROP-n` to the test that covers it; flag drift.

## 3. Report, then pause

Present `## Standards`, `## Spec`, `## Verification` side by side, verbatim or lightly cleaned. **Do not merge or rerank findings across axes**: a change can pass one and fail another, and keeping them apart stops one from hiding the other. End with one line: findings per axis and the worst one within each axis.

**Pause point.** Stop and let the human decide what to fix, accept, or defer. Do not fix anything yourself. Fixes go back through `ship` on the same branch; then run `check` again from step 1 on the new SHA.

**Drift** (code no longer matches the model, or a counterexample does not replay in code) is always a stop: route to `prove` maintain, even if every test passes.

## 4. When everything passes

All hard findings are fixed or explicitly accepted by the human, every acceptance criterion is ticked with evidence on the current head SHA, and Verification has no open drift. Then:

1. Write the PR body with the `pr` skill (if it is not installed, use sections Summary, Evidence, Merge Danger, and Verification). Include the Verification table from `references/verification.md`.
2. Single ticket: open the PR from the ticket branch into its fixed point. Whole spec: update the draft PR's body and mark it ready for review.
3. Link the work so merging closes it in the tracker: the closing keyword per ticket (`Closes #N` on GitHub and GitLab, or the tracker's equivalent from `flow`'s `references/tracker.md`); the spec only where the repo's convention says. A PR into an integration branch does not auto-close on most forges; the whole-spec PR into the default branch carries every ticket's closing line.
4. Post the verdict on the ticket (SHA, commands, results, accepted findings) using the repo's labels if it has them.
5. **Never merge the PR, never push to a protected branch, never close tickets by hand.** Humans merge.

## References
- `references/axes.md`: subagent prompts for the three axes.
- `references/smells.md`: the code-smell baseline.
- `references/verification.md`: the Verification axis, evidence table, INV/PROP coverage, drift.
- `NOTICE.md`: attribution and licenses.
