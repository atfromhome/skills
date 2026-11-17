# When to mock

Adapted from mattpocock/skills `tdd/mocking.md`.

Mock only at **system boundaries**:
- external services (payment, email, messaging providers)
- time and randomness
- the database or file system, only when a real test instance is impractical (prefer the real thing)

Do not mock your own modules, internal collaborators, or anything you control.

## Designing boundaries that are easy to fake

- **Inject dependencies.** Pass the external client in instead of building it inside the function, so a test can hand in a fake.
- **One function per external operation** (`get_user`, `create_order`) rather than one generic `request(endpoint, options)`. Each fake then returns one known shape, needs no branching, and shows which operations a test touches.
- For level A, a fake of the external actor (provider, webhook sender) must be able to do everything the model's environment actions do: duplicate, delay, and reorder.
