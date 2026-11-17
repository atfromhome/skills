# skills

Agent skills (Agent Skills format: a folder with `SKILL.md`) for planning and shipping features with verification decided **before** code. Generic by default: any repo, any language, any issue tracker (GitHub Issues by default).

## The vflow family

| Skill | Role |
|---|---|
| [`flow`](skills/flow) | Orchestrator: where is this work in the flow, what runs next, tracker adapters, implementer and QA rules |
| [`chart`](skills/chart) | Optional on-ramp for big, foggy, multi-session efforts: a map of decision tickets (adapted from wayfinder) |
| [`spec`](skills/spec) | Spec with a mandatory verification level A/B/C and plain-language invariants (adapted from to-spec) |
| [`prove`](skills/prove) | Formal gate before implementation: TLA+ model checked by TLC plus a statechart; bind and maintain modes |
| [`slice`](skills/slice) | Tracer-bullet tickets, prefactor first, published as sub-issues (adapted from to-tickets) |

```
[chart] → spec → (level A) prove: gate → slice (01 = prefactor, prove: bind)
        → implement → QA reruns verification on the PR SHA → drift → prove: maintain
```

Verification levels: **A** state machines, status transitions, concurrency, money (TLA+ gate first); **B** rules and calculations (property-based tests); **C** simple UI/CRUD (regular tests). When unsure, A.

## Install

Copy all five folders from `skills/` side by side into your agent's skills directory (for example `.agents/skills/`, `.claude/skills/`, or `.cursor/skills/`). They refer to each other by name.

## Requirements (level A only)

- Java 11+ (17/21 recommended) and `tla2tools.jar`: `bash skills/prove/scripts/check_toolchain.sh --fetch-tla2tools`
- `gh` authenticated for the default GitHub Issues tracker
- Python 3 (standard library) for the statechart fallback
- Optional: pstack `statechart` skill (Node 22.18+, mise)

Without Java or TLC the gate is recorded as `blocked`, never skipped silently.

## Configuration

Zero config works. A repo can override defaults with `.vflow.yml` or a `## vflow` section in `AGENTS.md`; a repo tracker doc such as `docs/agents/issue-tracker.md` wins over both. See [`skills/flow/references/config.md`](skills/flow/references/config.md).

## Repo layout

- `skills/`: the installable skills
- `evals/`: trigger and behaviour evals per skill (not installed)
- `.github/workflows/validate.yml`: frontmatter check and TLC run on the example model

## License

MIT. Derived from [mattpocock/skills](https://github.com/mattpocock/skills) and [pstack](https://github.com/cursor/plugins); see [NOTICE.md](NOTICE.md).
