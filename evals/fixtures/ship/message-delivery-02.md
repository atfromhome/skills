# Tracker issue #142: Message delivery status — spec

**Labels:** spec, verification:a, formal-gate:passed
**Spec revision:** `c41d9e0a2b77`

## Testing Decisions (excerpt)
**Verification level:** A
**Seams:** the delivery service (send, apply provider report, cleanup sweep). Prior art: the stateful property test `TestDeliveryModel`.

### Level A — model scope
- States: queued, sending, delivered, read, failed
- Transitions: send (queued → sending); provider report (sending → delivered | read | failed); cleanup sweep (sending → failed after 30 minutes); late report (failed → delivered | read, only when the failure came from the sweep)

### Invariants
- INV-1 (safety): status never moves backwards, except that a late delivered/read report corrects a failed set by the cleanup sweep.
- INV-2 (liveness, fairness: the sweep eventually runs): every message in sending eventually reaches a final status.
- INV-3 (safety): applying the same provider report twice leaves the same status as applying it once.
- INV-4 (safety): once the provider's delivery report has been applied, the message is never shown as failed.

**Comment (latest `<!-- vflow:formal-gate -->`):** Formal gate: PASSED. Spec revision `c41d9e0a2b77`. Model MessageDelivery.tla, TLC 2.19 on Java 21, 18,204 distinct states, all four invariants hold; broken variant without the late-report rule → TLC reports INV-4 broken.

---

# Tracker issue #144: Message delivery 01 — model, property tests, and verify skill
**State:** closed, merged into `message-delivery/integration` by PR #150.
Left `TestDeliveryModel`'s LateReport action pending (`t.Skip("ticket 02")`).

---

# Tracker issue #145: Message delivery 02 — late delivery report corrects a sweep failure

**Labels:** ready-for-agent. **Parent:** #142. **Blocked by:** #144 (closed).

## What to build
When a delivered or read report arrives for a message the cleanup sweep already marked failed, the message moves to delivered or read. A failure reported by the provider itself is never overridden.

## Acceptance criteria
- AC1: a delivered report that arrives after the sweep marked the message failed sets it to delivered (INV-1, INV-4).
- AC2: a delivered report never revives a message the provider itself reported failed (INV-1).
- AC3: the LateReport action in `TestDeliveryModel` is turned on and passes (INV-1, INV-4).

## Commands (from AGENTS.md)
typecheck `go vet ./...` · single test `go test ./internal/delivery -run <Name>` · full suite `make test` · verify skill `verify-message-delivery`
