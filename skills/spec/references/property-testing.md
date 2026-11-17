# Property-based testing libraries

Detect the language from the repo (build files, majority of source) and prefer a PBT library already in the dependency tree. Otherwise suggest the common one below and let the human confirm before the prefactor ticket adds it.

| Language | Library (common choice first) |
|---|---|
| Go | `pgregory.net/rapid`, `gopter`, stdlib `testing/quick` (basic) |
| Python | Hypothesis |
| TypeScript / JavaScript | fast-check |
| Java / Kotlin | jqwik, Kotest property testing |
| Scala | ScalaCheck |
| C# / F# | FsCheck, CsCheck |
| Rust | proptest, quickcheck |
| Haskell | QuickCheck, Hedgehog |
| Elixir / Erlang | StreamData, PropEr |
| Ruby | rantly, prop_check |
| PHP | Eris, PhpQuickCheck |
| Swift | SwiftCheck |
| Dart | glados |

Stateful testing (a model of commands run against the real system) is the bridge from a level-A model to code: `rapid` state machines (`t.Repeat`), Hypothesis `RuleBasedStateMachine`, fast-check `commands`, proptest-state-machine, jqwik stateful. Use it when the spec is level A to replay random event orders against the real implementation and assert the same `INV-n`.
