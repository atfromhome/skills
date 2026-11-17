# Decision ticket types

Every ticket is **HITL** (worked with a human who answers for themselves) or **AFK** (agent alone).

| Type | Mode | Use when | Resolve by |
|---|---|---|---|
| `grilling` | HITL | Default: the question can be settled by talking it through | Ask one focused question at a time, short, with your recommended answer and why; pin down domain terms (update the repo glossary if it has one). Use a `grilling`/`domain-modeling` skill if installed. |
| `prototype` | HITL | "How should it look/behave" cannot be settled by talk | Build a cheap throwaway artifact (outline, stub, UI mock, logic sketch) and link it. **vflow option:** for "how should this flow/state machine behave" questions, a tiny TLA+ sketch plus statechart (`prove` assets and scripts, scratch folder) is an excellent prototype: TLC shows the bad orders in minutes. The human picks among variants, never the agent. |
| `research` | AFK | A fact outside the repo blocks a decision (docs, third-party API limits, webhook semantics, provider retry policy) | Subagent reads sources and records findings with links on a throwaway `research/<name>` branch (no PR). Parallel at charting time. |
| `task` | either | Manual work must happen before a decision (get API access, sign up, move sample data) | Do it if possible; otherwise give the human a precise checklist. Record resulting facts. Never product code. |

Research is the only type that may be resolved several per session.

## Verification-flavoured questions worth ticketing early
- Which entities have a lifecycle, and who/what can move them (users, webhooks, crons, workers)?
- What can arrive twice, late, or out of order? What does the provider guarantee? (research)
- What must happen exactly once (charges, payouts, notifications), and what is the idempotency key?
- What is the correct end state after a crash mid-operation?
Answers feed the spec's verification level and invariants directly.
