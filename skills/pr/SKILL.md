---
name: pr
description: "Write a pull request (or merge request) body a reviewer can judge in a minute: a Summary built around the smallest visual that makes the point (pseudocode, call tree, component or file tree, Mermaid, or a diff sketch), Evidence that shows before and after (screenshot, output, or the test that failed and now passes), and Merge Danger (one-way or two-way door, blast radius). Works for any PR in any repo; when the change comes from a vflow ticket it also links the ticket and spec and lists the INV-n/PROP-n covered. Can open the PR on request, never merges. Use whenever someone asks to write a PR body, write or improve a PR description, fill in a PR template, summarise a branch for review, or open a PR, even if they do not name this skill. Not for reviewing or QA-ing the code itself (check)."
license: "MIT. Derived from mattpocock/skills pr, whose Summary visuals come from HumanLayer show-me by Dex Horthy; see NOTICE.md"
metadata:
  version: "0.1.0"
  credits:
    skill: show-me
    author: Dex Horthy
    organisation: HumanLayer
    url: "https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md"
---

# pr

A PR body that shows, not tells. Skip preambles, keep prose short, and use the repo's domain words (its glossary if it has one).

## Gather first

- `git log <base>..HEAD --oneline` and `git diff <base>...HEAD` for what changed; the base is the branch the PR targets.
- The issue or ticket it resolves, and any test, build, or screenshot output **from this session**. Do not invent evidence; if there is none, say what is missing.
- The repo's PR template (`.github/pull_request_template.md` or similar). If one exists, fill its headings and fit the sections below inside them.

## Template

```markdown
## Summary

<one or two sentences, then the smallest visual that makes the point>

## Evidence

- **Before:** <screenshot / output / failing test run>
  **After:** <screenshot / output / passing test run>

## Merge Danger

**Door:** <one-way | two-way>
<optional: why>

**Blast radius:** <one word>
<optional: what could break if this merges>
```

## Sections

**Summary.** Pick one view, occasionally two: pseudocode for logic, a call tree for runtime flow, a component tree for UI structure, a shallow file tree for a refactor, Mermaid for interactions or data flow, a diff sketch when the surrounding shape already exists, or the full block when most of it is new. Put each visual next to the sentence it supports and keep only the parts needed to judge this change. Menu with examples: `references/visuals.md`.

**Evidence.** Before and after. A screenshot is best when the change is visible and the environment can produce one. Next best is execution output: the exact test that failed and now passes, or a command's output. Quote only the lines that carry the signal and redact secrets.

**Merge Danger.** A two-way door is cheap to roll back; a one-way door is not (destructive migrations, deleted data, published APIs, sent messages). The blast radius is everything the change could touch: consumers, data, layout, mobile, performance. Think through all of them; write the one that matters.

## If the change comes from a vflow ticket (optional)

Add after Evidence:

```markdown
## Verification

Ticket: <link>   Spec: <link>   Level: A | B | C   Checked SHA: <sha>

| Rule | Covered by | Result |
|---|---|---|
| INV-1 … | <test or model invariant> | holds |
```

Paste the acceptance-criteria table from `check` if it ran. Put the tracker's closing keyword for the ticket (for example `Closes #123`) on its own line; close the spec only where the repo's convention says.

## Opening the PR

Only when asked. Write the body to a file and open it with the forge's tool (for example `gh pr create --base <base> --body-file body.md`, `--draft` if unfinished; `glab mr create` on GitLab). Never push to a protected branch and never merge.
