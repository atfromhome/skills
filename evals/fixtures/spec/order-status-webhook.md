<!-- vflow:decision-summary -->
## Decision summary: Order status from payment webhooks

**Source:** grill session, 2026-11-10. **Tracker issue:** #142 Order status from payment webhooks. **Confirmed by:** Dina (product), 2026-11-10.

### Problem and goal
Orders are marked paid by hand after staff check the payment dashboard, and refunds and chargebacks are never reflected. Done when every order's status follows the payment provider's webhooks without staff action, and finance can trust the status for reconciliation.

### Settled decisions
- D1. An Order has four statuses: pending, paid, refunded, chargeback. pending is the only initial status (Q1)
- D2. Allowed transitions: pending → paid (settlement), paid → refunded (full refund), paid → chargeback (dispute opened). refunded and chargeback are final for this feature (Q2)
- D3. Only the payment provider's signed webhook moves an order out of pending; staff cannot set statuses by hand in this feature (Q3)
- D4. Each webhook carries a provider event id; an event id that was already applied is acknowledged with success and changes nothing (Q4)
- D5. Webhooks can arrive late, twice, or out of order (a refund before its settlement). An event whose transition is not allowed from the current status is stored and retried for 24 hours, then flagged for staff review; it never forces the status (Q5)
- D6. A webhook with an invalid signature is rejected and changes nothing (Q6)
- D7. Partial refunds leave the order paid and are flagged for staff review (Q7)
- D8. Each transition into paid, refunded, or chargeback writes exactly one ledger entry; the ledger is what finance reconciles against (Q8)

### Open assumptions
None.

### Deferred or out of scope (decided by the human)
- Partial refunds as their own status: needs amount tracking, later feature
- Chargeback outcomes (merchant wins or loses): provider sends them, but handling is a follow-up
- Multiple payment providers: one provider only (ADR-0004)

### Glossary terms touched
- **Order status**: changed: now includes refunded and chargeback (GLOSSARY.md)
- **Chargeback**: added: a dispute the buyer opens through their card issuer (GLOSSARY.md)
- **Webhook event**: added: one signed notification from the payment provider, identified by its event id (GLOSSARY.md)

### ADRs written
none

### Facts looked up
- Provider retries a webhook until it receives a success response, for up to 3 days: provider docs
- Provider does not guarantee event order: provider docs
- The current webhook handler only handles settlement and does not store event ids: payment webhook handler
- Ledger entries are created in the same place the order status changes today: order service

### Verification-level hint (provisional; spec makes the final call)
**Level:** A
- Q1 named states/statuses: yes, pending, paid, refunded, chargeback
- Q2 concurrency, duplicate, late, or out-of-order events: yes, webhooks repeat, arrive late, and arrive out of order; the retry sweep runs alongside new webhooks
- Q3 money or exactly-once effects: yes, ledger entries must be written exactly once per transition
- Q4 rule or calculation with a law for all inputs: no
**Reason:** a payment state machine driven by unordered, repeated events with an exactly-once ledger effect. Candidate invariants or properties: status never moves backwards; applying the same event twice equals applying it once; a refunded order was paid before; each transition writes exactly one ledger entry; every stored out-of-order event is eventually applied or flagged.

### Next
Run `spec` with this summary.
