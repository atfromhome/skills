# Tracker: lookup, operations, adapters, mirroring

## Contents
1. Lookup order
2. Operations every phase needs
3. Adapters
4. Mirroring into an orchestrator

## 1. Lookup order

Stop at the first hit.

1. A pointer in `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or `.cursor/rules` to a tracker doc. Follow it.
2. A tracker doc at a conventional path: `docs/agents/issue-tracker.md`, `docs/issue-tracker.md`, `.github/ISSUE_TRACKER.md`.
3. A vflow config: `.vflow.yml` / `.vflow.yaml` at the repo root, or a `## vflow` section in `AGENTS.md` (see `config.md`).
4. Default: **GitHub Issues** for the `origin` remote, through `gh` (check `gh auth status`).
5. If there is no GitHub remote or `gh` is not authenticated: tell the human, then fall back to **local markdown** under `.scratch/<feature-slug>/` only if they agree.

When the repo's doc defines its own labels, title formats, claim commands, branch naming, or sub-issue mechanics, **those win over every default in this family.** Example: a repo may name specs "<Feature> — spec" with label `spec`, tickets "<Feature> NN — <topic>" with label `ticket`, and require a claim command before work. Follow it verbatim.

## 2. Operations every phase needs

| Operation | Used by |
|---|---|
| Read issue body + comments | all |
| Create issue with labels | spec, slice, chart |
| Edit issue body | spec (revisions), chart (map index) |
| Add comment (with a hidden marker such as `<!-- vflow:formal-gate -->` or `<!-- vflow:decision-summary -->`) | grill, prove, QA |
| Add/remove label | all (status axes) |
| Link sub-issue to parent | slice, chart |
| Native "blocked by" edge | slice, chart |
| Query children / frontier (open, unblocked, unassigned) | slice, chart, status |
| Assign (claim) | chart, implementer |

If an operation is missing on the tracker, use a body convention (a `## Parent` or `## Blocked by` section listing linked issues) and say so; the human must then check the graph by hand.

## 3. Adapters

### GitHub (default, via `gh`)
- Create: `gh issue create --title "..." --body-file body.md --label spec`
- Comment: `gh issue comment N --body-file gate.md`
- Labels: `gh issue edit N --add-label x --remove-label y` (create missing labels with `gh label create` only if the repo has no equivalent, and tell the human)
- Database id (needed for sub-issues/dependencies): `gh api repos/{owner}/{repo}/issues/N --jq .id`
- Sub-issue: `gh api --method POST repos/{owner}/{repo}/issues/PARENT/sub_issues -F sub_issue_id=CHILD_DB_ID`
- Blocked-by: `gh api --method POST repos/{owner}/{repo}/issues/CHILD/dependencies/blocked_by -F issue_id=BLOCKER_DB_ID`
- If the sub-issue or dependency endpoints return 404/403 (older GHES, permissions), fall back to body sections and report it.
- Attachments: GitHub issues have no file upload API. Put models in fenced code blocks in the gate comment; if too long (>60k chars), push them on a throwaway branch `vflow/model/<slug>` (never the default branch, never opened as a PR) and link the blob at its commit SHA.

### GitLab (`glab`)
Issues + `glab issue note`; child items via tasks or "related/blocks" links (`/blocks #N` quick action in a note). Labels the same.

### Linear / Jira / others (MCP connector or CLI)
Use the connector's create/comment/label/relations tools. Sub-issue = parent/child; blocked-by = "blocks" relation. Attach the model as a file if the tracker supports attachments, otherwise inline.

### Local markdown (last resort)
`.scratch/<feature-slug>/spec.md`, `.scratch/<feature-slug>/gate.md`, `.scratch/<feature-slug>/issues/NN-<slug>.md` numbered in dependency order with `Blocked by:` lines. Labels (spec, level, gate status, ready) are a `**Labels:**` line under the title, edited in place; the gate record is a new `<!-- vflow:formal-gate -->` section appended to `gate.md` per run. Warn that repo-stored planning files persist by accident; keep `.scratch/` git-ignored unless the repo says otherwise.

## 4. Mirroring into an orchestrator

When an orchestrator such as Multica drives agents, it may hold a mirror issue per tracker issue. Rules:

- Mirror body: the title plus `Mirror of <tracker ref>. Source of truth: <tracker>.` Nothing else; no copied spec text, no status the tracker does not also hold.
- Before acting on a mirror, read the tracker issue. If they disagree (status, labels, body), the tracker wins; update the mirror, not the other way round.
- Orchestrator columns map to tracker labels/state (for example: Refinement → spec in progress; Gate → `formal-gate:pending`; Ready → tickets published; In progress / In review → tracker progress labels). Record the mapping in the repo config, not in this skill.
- Mirrors are created after the tracker issue exists, never before.
