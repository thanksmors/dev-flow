# Why: Deferred Decisions

## What Makes a Good Deferred Decision

A deferred decision is a choice you postpone intentionally, not one you forget or avoid. The distinguishing characteristic of a good deferred decision is that it has a clearly defined trigger — a point in time or a set of conditions that will force the decision.

A deferred decision is worth making later when:
- The options have similar cost today, but different uncertainty profiles
- You expect to have more information later that will make the choice clearer
- Deferring does not make the choice more expensive when you finally make it

A deferred decision is a mistake when:
- The options have different costs today, and deferring means paying the higher cost for longer
- You are deferring because the decision is hard, not because timing matters
- The trigger for making the decision is undefined, so it never gets made

---

## Why "Just in Time" Beats "Just in Case"

" Just in case" thinking leads to over-engineering. You implement Postgres because you might need it, you add Redis because you might need it, you build a message queue because you might need it. Each "might need" adds complexity, dependencies, and maintenance burden. Most of the time, the "case" never arrives, and you're stuck with infrastructure you don't need.

"Just in time" thinking is the opposite. You defer a decision until you have a concrete reason to make it. At that point, you have real requirements (not imagined ones), real constraints (not guessed ones), and real performance data (not estimates).

The cost of waiting is low if:
- The decision is reversible (you can swap one adapter for another without rewriting business logic)
- The deferral does not block other work (your architecture allows both options to be swapped in later)

Both conditions are met when you follow the port/adapter pattern. The port defines the interface. The adapter implements it. Swapping adapters is a one-line import change. You can defer which database to use, which queue to use, which auth provider to use — because all of them are behind the same interface.

---

## What Cannot Be Deferred

Deferring decisions is a discipline, not a license to avoid hard problems. Some decisions are architecture boundaries, and deferring them means deferring clarity about the system's structure.

**Core domain model cannot be deferred.** What is the fundamental unit of work in your system? What are the entities, their properties, and their relationships? Getting this wrong ripples through every layer. The domain model must be understood early, even if details are filled in later.

**Architecture boundaries cannot be deferred.** Where does the system stop and the outside world begin? What are the ports? Which adapters exist and which are planned? These decisions shape every piece of code that follows. You must define the ports before you can write any meaningful code.

**Technology choices that constrain the domain model cannot be deferred.** If you're building a system that processes financial transactions, you need to understand the constraints of your database's transaction model early. You cannot defer "does this database support ACID transactions?" because the answer changes how you model the domain.

The rule of thumb: if the decision affects how you model the problem domain, it cannot be deferred. If the decision affects how you implement a solution that already has a correct model, it can be deferred.

---

## Swap Protocol: Fake to Real

When a fake adapter is ready to be replaced with a real implementation, follow this explicit protocol. See `dev-flow/phases/06-implementation.md` Section 6.5 for the full procedure.

### WHEN — Explicit Trigger Points

The swap from fake to real adapter happens at any of these three trigger points. One is sufficient:

| Trigger | Condition | Who initiates |
|---------|-----------|---------------|
| **Task-level** | Feature works end-to-end with fake, tests pass, spec approved, quality approved. The swap is a natural follow-on micro-step within the task. | Implementer |
| **Phase 6 end (6.5)** | All tasks complete. Section 6.5 runs "Deferred Decision Swaps." | Orchestrator |
| **Phase 7 gap analysis** | Gap flagged: "fake adapter still wired in production code path." | Gap analysis loop |

### WHERE — Exact Change Locations

| # | File | Action |
|---|------|--------|
| 1 | `layers/{domain}/adapters/FakeXyzAdapter.ts` | **Never deleted.** Mark `@deprecated use XyzAdapter`. Stays as regression reference. |
| 2 | `layers/{domain}/adapters/XyzAdapter.ts` | **Created.** Implements the same port interface as the fake. |
| 3 | `app/diComposition.ts` | **One-line change.** Swap the adapter binding. |

### HOW — Step-by-Step

1. Mark the fake as `@deprecated use XyzAdapter`
2. Create the real adapter implementing the same port interface
3. Swap the DI binding (one line in composition root)
4. Run full test suite — all must pass
5. Update the deferred-decisions tracker: set **Status** to `swapped`, **Swapped On** to today's date
6. Write an ADR if the port interface required adjustment

**Adapter Status values:** `fake` (not yet swapped) | `swapped` (real adapter is wired) | `not deferred` (real was used from the start)

See: `dev-flow/phases/06-implementation.md` Section 6.5 for the full protocol including the Deferred-Decisions Tracker template.

---

## Why Deferred Does Not Mean Ignored

The worst kind of deferred decision is the one that lives in a comment: `// TODO: replace this with real auth`. Nobody knows when, why, or under what conditions to make that swap. The TODO is not a deferral — it is a abandonment.

A deferred decision is documented with:
- **The decision that is pending** — the specific choice that needs to be made
- **The criteria for making it** — how you will know which option is better
- **The trigger** — what event, time, or condition will prompt the decision
- **The cost of the decision** — what it will cost (in time, code changes, migration) to make the swap when the time comes

Without this documentation, deferred decisions are invisible. Future developers — including future-you — have no way of knowing that a choice was made by default rather than by design.

---

## Examples: Decisions We Defer in dev-flow

**SQLite → Postgres.** During the walking skeleton phase, SQLite is the right choice: zero setup, zero configuration, works offline, no credentials needed. We defer Postgres because we don't yet know if we need concurrent writes, row-level locking, or multi-server deployment. When we hit those requirements, we will have concrete criteria to choose between them.

**Fake auth → Real auth.** We start with a fake auth adapter that returns a hard-coded user. We defer real auth because we don't yet know which auth provider to use, what the user model looks like in detail, or what the organization's identity requirements are. The trigger is "when we need real user authentication for a production deployment."

**In-memory queue → Real message queue.** We start with an in-memory queue (an array of functions). We defer a real message queue because we don't yet know our throughput requirements, durability needs, or failure handling expectations. The trigger is "when the in-memory queue becomes a bottleneck or when we need message persistence across restarts."

**Fake observability → Real observability.** We start with a fake observability adapter that logs to the console. We defer a real observability provider (Datadog, Grafana, etc.) because we don't yet know what metrics matter most, what our alerting requirements are, or what the organization already uses. The trigger is "when we need production-grade observability with alerting and dashboards."

In every case, the decision is deferred because the information needed to make it well does not exist yet — and the architecture (specifically, the port/adapter pattern) allows us to defer it without blocking current work.

---

## Summary

Deferred decisions are a tool, not a philosophy. The goal is to make decisions at the last responsible moment, when you have the most information and the lowest cost of change — not to avoid hard decisions forever. The port/adapter pattern makes deferral safe by ensuring that the decision is encapsulated in a single adapter that can be swapped without rewriting the business logic. When you defer a decision, document it, set a trigger, and commit to revisiting it.
