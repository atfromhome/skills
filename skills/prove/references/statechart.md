# Drawing the statechart

The chart shows how the system moves between states in the words of the person who decides whether the behaviour is right (product owner, reviewer). Variable and action names stay out of labels.

## With pstack `statechart` (preferred when installed)
Load the `statechart` skill and follow it: it checks each rule, gives the shortest path to every broken rule, and draws the chart from a view module. Write the view in reader words (`assets/view.example.mjs`). Do not copy its commands into the spec or into generated skills; refer to it by name.

## Fallback: `dot2mermaid.py`
1. `scripts/tlc.sh Model.tla -o out --dot`  (writes `out/states.dot`)
2. Write a words file (`assets/MessageDelivery.words.json`): reader names for states and actions, and `hide` for steps the reader does not need (environment steps that change nothing visible).
3. `python3 scripts/dot2mermaid.py out/states.dot --vars <state vars> --words words.json [--trace out/tlc.out] --title "..." > chart.mmd`
   - `--vars` projects model states onto chart states (e.g. just `status`).
   - `--trace` with a violating `tlc.out` marks the counterexample's chart states `bugPath` and the last one `breaks`. Because of projection, `breaks` means "a model state behind this chart state breaks the rule", not every one; say so.
4. Show `chart.mmd` as a ```mermaid block.

## Reading rules (both paths)
- Aim for about 20 arrows. Coarsen labels first; hide only whole arrows; keep every chart state reachable; say which steps you hid.
- Never merge two states that break different rules.
- A state with no arrow out that is not a final state is a stuck state; call it out.
- Compare the chart to the spec's transition list. Any arrow the spec did not list, or listed arrow that is missing, is a finding to discuss with the human before the gate passes.
