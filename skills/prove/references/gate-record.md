# Gate record

Post as a comment on the spec issue (or `gate.md` next to a local spec). One record per run; never edit an old record, post a new one. Set the gate label to match the result.

~~~markdown
<!-- vflow:formal-gate -->
## Formal gate: PASSED | FAILED | BLOCKED | WAIVED

**Spec revision:** <hash of the spec's Testing Decisions section, e.g. first 12 chars of sha256, or the issue's last-edited timestamp>
**Model:** <Model>.tla (+ .cfg)    **Tool:** TLC2 Version <x> on Java <y>    **Chart:** pstack statechart | vflow dot2mermaid fallback | hand-drawn
**Bounds / assumptions:** constants …, CONSTRAINT …, fairness …; out of model: …
**States explored:** <distinct states>

| Spec rule | TLA+ name | Result |
|---|---|---|
| INV-1 <sentence> | DeliveryReportWins | holds / broken |
| INV-2 … | … | … |

**Can fail (evidence):** broken variant <what was removed/reordered> → TLC reported <rule> broken.

**Counterexample** (if FAILED), in domain words:
1. We send the message.
2. The provider delivers it; the delivery report is in flight.
3. The cleanup sweep times out and marks it Failed.
4. The delivery report arrives; status stays Failed.
Harm: a delivered message is shown as failed forever.

**Statechart**
```mermaid
<chart.mmd>
```

<details><summary>Model source</summary>

```tla
<Model.tla>
```
```cfg
<Model.cfg>
```
</details>

**Rerun:** <exact command>
**Next step:** tickets may start (PASSED) | design change needed: … (FAILED) | needs: … (BLOCKED) | waived by <human>, reason: … (WAIVED)
~~~

## Rules
- **Current vs stale:** a record is current only if its spec revision matches the spec now. When states, transitions, or invariants in the spec change, post a new run; label `stale` until then.
- **Waivers** are written by or quoted from the human, with their reason and scope. An agent never waives.
- If the model is too long for one comment, push it to a throwaway branch (`vflow/model/<slug>`, never the default branch, no PR) and link the files at the commit SHA.
