# Map and ticket format

## Map issue (label `wayfinder:map`)
```markdown
## Destination
<what reaching the end looks like; one or two lines>

## Notes
<domain; skills every session should consult; standing preferences>
<Verification flags: likely level-A areas (states / concurrency / money), likely level-B rules>

## Decisions so far
- [<closed ticket title>](link): <one-line gist>

## Not yet specified
<fog: in scope but not sharp enough to ticket; coarser than tickets>

## Out of scope
- [<closed ticket title>](link): <gist> — <why out of scope>
```
The map is an index, not a store: a decision lives only in its ticket.

## Decision ticket (child of the map)
```markdown
## Question
<the decision or investigation this ticket resolves>
```
Label: exactly one `wayfinder:<type>`. No triage/ready labels; these are decisions, not implementation work. The answer is posted on resolution as a comment; assets are linked, not pasted.

## Fog or ticket?
Ticket when you can state the question precisely now (even if blocked). Fog when you cannot yet phrase it sharply. Do not pre-slice fog.

## Tracker mechanics
Parent/child = the tracker's sub-issue link; blocking = native "blocked by" (fallback: `## Blocked by` section, supervise by hand). See the `flow` skill's `references/tracker.md`. With no tracker, local markdown under `.scratch/<effort>/map.md` and `.scratch/<effort>/tickets/NN-<slug>.md`.
