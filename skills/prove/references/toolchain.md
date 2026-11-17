# Toolchain

## Required for any level-A gate
- **Java 11+** (17 or 21 recommended): any JDK/JRE (Temurin, distro package, `mise use java@21`, `sdk install java`).
- **tla2tools.jar** (contains TLC and the SANY parser): https://github.com/tlaplus/tlaplus/releases. Point `TLA2TOOLS_JAR` at it, or let `scripts/check_toolchain.sh --fetch-tla2tools` put it in `~/.cache/vflow/`. Record the TLC version line in every gate record.

## Optional
- **pstack `statechart` skill** (cursor/plugins, `pstack/skills/statechart`): richer charts, rule-by-rule rechecks, shortest bug path per rule, parallel regions. Needs a runtime that executes TypeScript directly (Node **22.18+**) and installs TLC/Java with **mise** on first run (network). If present, prefer it for step 4 of gate mode; refer to it by name and follow its own SKILL.md, because its commands change between releases.
- **Python 3** for `scripts/dot2mermaid.py` (standard library only).
- **Pele** or any Mermaid renderer if the human wants an SVG; otherwise show Mermaid text.
- Alternatives when the question suits them better: Apalache (symbolic TLA+ checking for larger state spaces), Quint (TLA+-based, TypeScript-like syntax), Alloy (relational/permission structure), P. Keep the same gate record.

## Degrade gracefully, never silently

| Situation | Do |
|---|---|
| No Java or no jar, cannot install | Gate = `blocked`. Post the record with the problem and the model text you wrote. Ask the human to install, run it elsewhere (CI, a dev machine), or waive with a reason. |
| pstack statechart missing or Node < 22.18 | Use `scripts/tlc.sh --dot` + `scripts/dot2mermaid.py`. Say the fallback was used. |
| No Python | Use TLC's verdict and counterexample from `tlc.out`; draw the chart by hand from the spec's transition list and label it "hand-drawn, not generated from the state graph". |
| State space explodes | Shrink constants, add a CONSTRAINT, or use symmetry; say what you bounded in the record. Never report a pass from a run that was cut short. |
| Sandbox without network | Ask the human for the jar path or to run the check; mark `blocked` until then. |

## CI (optional, recommended once bind mode has run)
Run the verify skill's command in CI on PRs that touch covered files: `java -XX:+UseParallelGC -cp tla2tools.jar tlc2.TLC -workers 1 -config <Model>.cfg <Model>.tla`. Cache the jar by version.
