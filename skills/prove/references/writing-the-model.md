# Writing the model

Goal: the smallest TLA+ model in which every spec invariant can break if the design is wrong.

## Shape
- One module per area. `VARIABLES` for what the system stores **and** what the outside world does (in-flight messages, provider ground truth, worker state). If an invariant has no variable to talk about, add one.
- `Next` is a disjunction of named actions (`WeSend \/ SweepTimesOut \/ WebhookArrives`), each named after something that happens in the domain. TLC names counterexample steps after them.
- **Atomicity:** one action = one step that cannot be interrupted in the design (one DB transaction, one compare-and-set, one lock scope, one message handler). If the design reads, then decides, then writes in separate steps, model them as separate actions; that is where races live.
- Correct end states would trip TLC's deadlock check. Add `Done == <final condition> /\ UNCHANGED vars` to `Next` rather than disabling deadlock checking, so real stuck states are still found.
- Keep constants tiny (2 workers, 2 items, amounts in {0,1,2}). Bugs show up in small worlds; add a `CONSTRAINT` if a counter can grow forever.

## Invariants (from the spec's INV-n)
- One `INVARIANT` per safety rule, named after it, with a comment `\* INV-n: <spec sentence>`.
- `TypeOK` first, so modelling mistakes fail loudly.
- Liveness ("eventually") goes in `PROPERTY` and needs fairness on the actions that must eventually happen (`WF_vars(SweepTimesOut)`); write the fairness assumption back into the spec.
- "Never moves backwards" is an action property: `[][Rank[status'] >= Rank[status] \/ <allowed correction>]_vars` as a `PROPERTY`.
- Never weaken a rule to make it pass. If the human agrees the rule was wrong, change the spec first, then the model.

## Environment patterns
| Real-world behaviour | Model it as |
|---|---|
| Webhook/event can arrive late | Producer adds to an `inflight` set; a separate action applies it at any later point |
| Event can arrive twice | An apply action that does **not** remove it from `inflight` (`WebhookDuplicate`) |
| Out-of-order delivery | `inflight` as a set (any element can be applied next) |
| Retry after timeout | A timeout action enabled while waiting, which re-sends or re-enqueues |
| Multiple workers / double click | A set of process ids `Workers == {w1, w2}` and per-worker local state `pc[w]` |
| Crash mid-operation | An action that resets a worker's local state without finishing its writes |
| Cron sweep / reconciler | An action enabled by a condition on stored state, firing at any time |
| Money / stock | A ledger set or sum; invariants like "sum of debits = sum of credits", "at most one capture per order" |

## Prove it can fail
Before trusting a pass, run a broken variant (a constant `Fixed`/`Buggy`, or a temporary edit) that drops a guard or reorders two steps, and confirm TLC reports the expected invariant. Record which break you used. `assets/MessageDelivery.tla` shows the pattern with `CONSTANT Fixed`.

## Run
`scripts/tlc.sh <Model>.tla [-c <Model>.cfg] [-o outdir] [--dot]` prints a JSON summary (`PASS` / `VIOLATION` with rule / `ERROR`) and the counterexample. Exit 0/1/2.
