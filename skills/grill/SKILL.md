---
name: grill
description: "Interview the human before a spec is written: deepen the context on a feature that fits one session but still has open or fuzzy decisions, until there is a shared understanding. Opens with a context dump and a scope check, then works a design tree in rounds that ask every answerable question at once, numbered, each with a recommended answer; looks facts up in the code instead of asking; challenges domain terms against the glossary and records them; offers ADRs only for hard-to-reverse trade-offs. Writes no code and no spec. Ends with a Decision summary and a provisional verification level (A, B, C) that the spec skill consumes. Use for /grill, 'grill me', 'stress-test this plan', 'interview me before the spec', 'help me think this through', 'what am I missing', or when a request is too vague to spec. Not for writing the spec once decisions are made (spec), multi-session efforts with a foggy route (chart), or breaking a spec into tickets (slice)."
license: "MIT. Derived from mattpocock/skills grilling and domain-modeling, with ideas from obra/superpowers brainstorming and anthropics/skills doc-coauthoring; see NOTICE.md"
metadata:
  version: "0.1.0"
  family: vflow
---

# grill

The context-deepening step of the vflow family. It sits **before `spec`**: it turns a fuzzy, one-session feature into settled decisions, then hands a Decision summary to `spec`. It does not write the spec, tickets, or code.

<HARD-GATE>
No code, no scaffolding, no spec, no tickets, no implementation of any kind until the human confirms the shared understanding at the end. Even then, the next step is `spec`, not code. The only files this skill may write are the glossary and ADRs (see Domain language), and only in the working tree on a non-protected branch.

The only tracker write this skill makes is the Decision summary comment in step 5. No other issues, labels, or comments, even for a bug you find along the way: list it under follow-ups in the summary. A general "agree, continue" is not permission to create anything on the tracker.
</HARD-GATE>

## 1. Gather context

1. **Find what already exists.** If the work is tied to a tracker issue, read it and its comments (tracker lookup order: the `flow` skill's `references/tracker.md`). Read `GLOSSARY.md` (or `GLOSSARY-MAP.md` for multi-context repos), `docs/adr/`, and the code in the area: the entities involved and every place they change state.
2. **Invite a context dump.** Unless the conversation already holds it, ask the human to dump everything they know, unordered and in shorthand: the problem and who has it, constraints and deadlines, why the obvious alternatives are not used, related issues, docs, or threads, past incidents, and stakeholder concerns. Say the questions come after the dump. Read any links or files they point to.
   If the request already carries enough to start (the sufficiency test below passes, or the human brings a concrete design fork), do not wait: send the dump invite, the scope verdict, and round 1 in the same message, and say the dump can still change the round.
3. **Sufficiency test.** You are ready for rounds when you can ask about edge cases and trade-offs without needing the basics explained. If not, the first round asks for the basics.

## 2. Scope check (pause point)

Before detailed questions, judge the size and say what you see:

- **Too big:** several independent subsystems ("chat, file storage, billing and analytics"), decisions that need days of research or prototypes, or more deciding than one session can hold. Recommend `chart` (or splitting into sub-features, each grilled separately) and **stop until the human answers**. Do not spend questions on details of something that must be decomposed first. If the human picks `chart`, grill ends here: tell them to run `chart`. Do not build the map, labels, or tickets inside grill.
- **Already settled:** nothing is open. Say so and suggest `spec` directly.
- **Fits:** say so in one line and start the rounds. If the human disagrees with your call, follow theirs and note it.

When grill resolves a `wayfinder:grilling` ticket from a `chart` map, the map already scoped the question: skip this check and grill only that ticket's question.

## 3. Work the design tree in rounds

Map the work as a **design tree**: every decision branches into the decisions that hang off it. Seed the branches from `references/rounds.md` (goal, actors, domain terms, lifecycle, concurrency, exactly-once effects, failure, permissions, data, UX, rollout, out of scope).

- The **frontier** is every decision whose prerequisites are settled: the questions you can ask now without guessing at answers you have not heard. **Ask the whole frontier in one round**, numbered, each with your recommended answer. Then wait.
- **One decision per numbered question.** Word each question so "yes" accepts your recommendation; for a fork, name the recommended option in the question and list the alternatives after it.
- **Word each question so "yes" accepts your recommendation.** The human can answer in shorthand ("1 yes, 2 no: monthly, 3 see #42").
- A question that depends on another question still open in this round belongs to a later round.
- Each answer reshapes the tree. Recompute the frontier and ask the next round.
- **Facts are your job; decisions are the human's.** When a question needs a fact from the code, docs, or tools, look it up yourself, with a subagent that has a fresh context if available. Do not block on it: only the questions downstream of a running lookup wait; ask the rest of the frontier now. Never ask the human for something you could look up, and never answer a decision for them.
- **Real design fork:** when there are genuinely different ways to build it, make it one frontier question with 2–3 approaches, their trade-offs, and your recommendation first, with the reason. When the human named the fork themselves, it is question 1 of round 1. Never treat it as decided before they answer.
- **Domain language, not implementation.** Ask and recommend in terms of behaviour and the domain ("a reminder is sent at most once per due installment"), not code, SQL, or schema. How to build it belongs to `spec` and `ship`.
- **Verification questions are part of the tree.** Ask, as decisions or facts: does an entity move through named states, can actors act at once or events arrive twice, late, or out of order, and does a bug create, lose, or duplicate money or anything that must happen exactly once? The answers become the level hint.

Round format and a worked example: `references/rounds.md`.

## 4. Domain language (during the rounds)

- **Challenge against the glossary.** When the human uses a term that conflicts with `GLOSSARY.md`, say so at once: "The glossary defines *cancellation* as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy terms.** Propose one canonical term for vague or overloaded words ("account: the Customer or the User?").
- **Test with scenarios.** Invent concrete edge cases that force the boundaries between concepts to be precise.
- **Cross-check the code.** When the human states how something works, check whether the code agrees and surface contradictions.
- **Update the glossary inline and lazily.** When a term is resolved, write it to the glossary right then, not in a batch; create the file only when the first term is resolved. No implementation details in it. Format: `references/glossary-format.md`.
- **Offer an ADR only when all three hold:** hard to reverse, surprising without context, and the result of a real trade-off. Offer it as a numbered question in the very next round after the decision is settled, alongside that round's frontier; never save it for an extra round once the frontier is otherwise empty. Write it only if the human accepts. Format: `references/adr-format.md`.

Follow the repo's own glossary and ADR locations if it has them. Do not commit to or push a protected branch; tell the human which files changed.

## 5. Finish (pause point)

The session is done when the frontier is empty: every branch visited, decided, or explicitly deferred or ruled out of scope **by the human**. Nothing is silently assumed.

1. Draft the **Decision summary** with `references/decision-summary.md`: settled decisions, open assumptions (should be none), out of scope, glossary terms touched, ADRs written, facts looked up, and a **provisional verification-level hint** (A, B, C, or a combination) with the reason, using the same definitions as the `spec` skill's `references/verification-levels.md` (A: named states, concurrency or duplicate events, money or exactly-once; B: a rule or calculation with a law for all inputs; C: none of these; unsure means A).
2. **Ask the human to confirm the shared understanding.** Stop until they answer. If they correct anything, update the tree, ask any new frontier, and redraft. Send the summary only when the frontier is empty; never bundle a draft summary with a round whose answers it depends on. Once the human confirms, go straight to steps 3 and 4 without asking again.
3. **Record it.** If the work is tied to a tracker issue, post the confirmed summary as a comment with the marker `<!-- vflow:decision-summary -->`; for a chart grilling ticket it is the resolution comment, and chart closes the ticket. Otherwise it stays in the conversation. Do not create an issue just to hold it; `spec` creates the spec issue.
4. **Hand off to `spec`** with the summary as input: say plainly that grill is done and the next step is `spec`. Do not write the spec inside grill.

## References

- `references/rounds.md`: round format, seed branches for the design tree, a worked example.
- `references/decision-summary.md`: the handoff template `spec` consumes.
- `references/glossary-format.md`: glossary format and single vs multi-context repos.
- `references/adr-format.md`: ADR format and the three-criteria test.
- `NOTICE.md`: upstream attribution and licenses.
