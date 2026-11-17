# Tracker issue #188: Order refunds — spec

**Labels:** spec, verification:a, formal-gate:pending
**Last edited:** 2026-11-15 (spec revision `9f2c4a1e7b03`)

## Problem Statement
Customers ask for refunds by email and staff refund them by hand in the payment provider's dashboard. Order status never shows the refund, and twice this year a customer was refunded twice because two staff members handled the same email.

## Solution
Staff request a refund from the order page. The system sends it to the provider once, follows the provider's webhooks, and shows the order as partially refunded or refunded.

## User Stories
1. As staff, I want to refund an order in full or in part from the order page, so that I do not use the provider dashboard.
2. As staff, I want a second refund request for the same order to be rejected while one is pending, so that customers are never refunded twice.
3. As a customer, I want my order to show "Refunded" once the money is back, so that I know it is done.
4. As finance, I want every succeeded refund to appear once in the ledger, so that reconciliation matches the provider.

## Implementation Decisions
- Refund statuses: requested → pending → succeeded | failed; requested → rejected.
- Order refund status: paid → partially_refunded → refunded, derived from succeeded refunds.
- Each refund carries an idempotency key sent to the provider.
- A sweep marks refunds still pending after 48 hours as failed and alerts staff.

## Testing Decisions
**Verification level:** A
**Why:** Q1 yes (refund and order refund statuses). Q2 yes (webhooks arrive twice, late, or out of order; the sweep runs alongside webhooks; two staff can click at once). Q3 yes (money: a duplicate refund pays a customer twice). Q4 yes (refunded total never exceeds the captured amount).

**Seams:** the refund service (request, apply webhook, sweep) and the provider webhook endpoint.

### Invariants
- INV-1 (safety): the total of succeeded refunds for an order never exceeds its captured amount.
- INV-2 (safety): requests with the same idempotency key create at most one refund at the provider.
- INV-3 (safety): the order's refund status always matches its succeeded refunds.
- INV-4 (safety): a refund in a final status (succeeded, failed, rejected) never changes.
- INV-5 (liveness, fairness: the sweep eventually runs): every pending refund eventually reaches a final status.

### Gate
Level A only: this spec cannot be split into tickets until `prove` records a passed (or human-waived) gate on this issue.

## Out of Scope
Refunds to a different payment method; store credit.

## Further Notes
Formal gate: not run yet.

---
**Comments on #188:** none. There is no `<!-- vflow:formal-gate -->` comment on this issue.
