# Good and bad tests

Adapted from mattpocock/skills `tdd/tests.md`. Pseudocode; translate to the repo's test framework.

## Good: behaviour through the public interface

```text
test "a donor can check out with a valid cart"
  cart = new_cart()
  cart.add(item)
  result = checkout(cart, payment_method)
  assert result.status == "confirmed"
```

- Describes what callers care about, not how it is done.
- Uses the public interface only and survives internal refactors.
- One logical assertion per test.

## Bad: coupled to implementation

```text
test "checkout calls the payment service"
  payment = mock(payment_service)
  checkout(cart, payment)
  assert payment.process was called with cart.total
```

Red flags: mocking internal collaborators, testing private functions, asserting call counts or order, a test name that says how instead of what, breaking on a refactor that keeps behaviour.

## Bad: checking through a side channel

```text
# bad
test "create_user saves to the database"
  create_user(name = "Alice")
  assert db.query("select ... where name = 'Alice'") exists

# good
test "a created user can be fetched"
  user = create_user(name = "Alice")
  assert get_user(user.id).name == "Alice"
```

## Bad: tautological

```text
# bad: expected value computed the way the code computes it
test "total sums the line items"
  items = [10, 5]
  assert total(items) == sum(items)

# good: an independent, known value
test "total sums the line items"
  assert total([10, 5]) == 15
```

## Level A: mirror an invariant

```text
property "a delivered message is never shown as failed"   # INV-4
  for any sequence of: send, provider_report(delivered|read|failed), duplicate_report, sweep
    run the sequence against the real service
    if a delivered or read report was applied:
      assert status(message) != failed
```

## Level B: a property with real edge cases

```text
property "CSV round-trips every field"   # PROP-3
  for any list of records whose names include commas, quotes, newlines, non-ASCII
    assert parse_csv(export_csv(records)) == records
```
