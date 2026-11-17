# Optional repo config

vflow works with zero config. A repo can override defaults in `.vflow.yml` at the root, or in a `## vflow` section of `AGENTS.md` written as the same YAML in a fenced block. A repo tracker doc (see `tracker.md`) still wins over this file for anything it defines.

```yaml
tracker: github            # github | gitlab | linear | jira | local | <name of connector>
tracker_doc: docs/agents/issue-tracker.md   # optional pointer
default_branch_protect:    # agents never push/merge here
  - main
  - master
  - trunk
  - "*/trunk"
labels:
  spec: spec               # applied to spec issues
  ticket: ready-for-agent  # applied to published tickets
  level: "verification:{a|b|c}"
  gate: "formal-gate:{pending|passed|failed|blocked|waived|stale}"
  map: "wayfinder:map"
  map_ticket: "wayfinder:{research|prototype|grilling|task}"
titles:
  spec: "{feature} — spec"
  ticket: "{feature} {NN} — {topic}"
branches:
  ticket: "{spec-slug}/{NN}-{topic}"
  integration: "{spec-slug}/integration"
commands:                  # optional; otherwise discovered from AGENTS.md, CONTRIBUTING.md, README, task runner files
  typecheck: ""            # e.g. the repo's build or type check
  test_one: ""             # run one test file or test name
  test: ""                 # full suite
  property: ""             # property tests, if separate
paths:
  models: verification/{area}/          # where the prefactor ticket commits TLA+ models
  verify_skill: .agents/skills/verify-{area}/   # project-local verify skill (match the repo's skills dir)
property_testing:          # auto-detected when absent; see spec references
  library: auto            # e.g. rapid | gopter | hypothesis | fast-check | jqwik | proptest | QuickCheck
toolchain:
  java: java               # >= 11; 17+ recommended
  tla2tools: ~/.cache/vflow/tla2tools.jar
  use_pstack_statechart: auto   # auto | yes | no
orchestrator:
  name: multica            # optional; only drives the flow
  mirror: true
  column_map: {}           # orchestrator column -> tracker label/state
```

## Defaults when nothing is configured

- Tracker: GitHub Issues through `gh` on `origin`.
- Labels: as above. Before creating a label, look for an existing equivalent (`gh label list`) and reuse it.
- Spec title: `<Feature> — spec`. Ticket title: `<Feature> NN — <topic>`.
- Models: `verification/<area>/` in the repo, committed by the prefactor ticket (never during the spec phase; then they live in a scratch folder and on the spec issue).
- Protected branches: the repo's default branch plus `main`, `master`, `trunk`, `*/trunk`.
- Branches: ticket `<spec-slug>/NN-<topic>`, integration `<spec-slug>/integration` (whole-spec mode in `ship`).
- Commands: discovered from the repo's docs and task runner files; `ship` and `check` run each once to confirm it works, and ask if none is documented.
