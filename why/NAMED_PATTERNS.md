# Named Patterns

Named patterns are reusable solutions to recurring problems. Using canonical names makes communication precise, failure mode analysis concrete, and risk documentation searchable.

---

## Architecture Patterns

### Hexagonal / Ports & Adapters

**One-line description:** Architecture that separates core business logic from external concerns via explicit ports and adapters.

**When to use:** Whenever you need to isolate domain logic from infrastructure (databases, HTTP clients, file system). Essential for testability.

**Reference:** `references/testing-pyramid.md` — Integration Test section

---

### CQRS (Command Query Responsibility Segregation)

**One-line description:** Separate read models from write models; commands mutate state, queries read it.

**When to use:** When read and write workloads have very different performance, scaling, or consistency requirements. Common in event-driven systems.

**Reference:** `phases/03-design.md`

---

### Event Sourcing

**One-line description:** Persist state as a sequence of immutable domain events rather than current-state snapshots.

**When to use:** When you need a full audit trail, temporal queries, or the ability to replay history. Pairs naturally with CQRS.

**Reference:** `phases/03-design.md`

---

### Repository Pattern

**One-line description:** Abstract collection interface for accessing aggregates, hiding the details of persistence technology.

**When to use:** When domain logic should not know whether data lives in a SQL database, document store, or in-memory cache.

**Reference:** `references/testing-pyramid.md` — Integration Test Fixture Strategy

---

### Unit of Work

**One-line description:** Groups a set of related operations into a single atomic transaction with change tracking.

**When to use:** When multiple aggregates must be saved in a single atomic operation. Coordinates with the Repository pattern.

**Reference:** `phases/03-design.md`

---

## Domain Patterns / DDD Building Blocks

### Entity

**One-line description:** An object with a stable identity that persists across changes to its attributes.

**When to use:** When an object must be distinguishable from others of the same type, even if all attributes are identical.

**Reference:** `phases/03-design.md`

---

### Value Object

**One-line description:** An immutable object defined by its attribute values, not by a persistent identity.

**When to use:** For descriptors that have no independent identity: money amounts, addresses, colors. Enables rich domain modeling without mutation.

**Reference:** `phases/03-design.md`

---

### Aggregate

**One-line description:** A cluster of related entities and value objects with a single root aggregate root that enforces invariants.

**When to use:** To define transaction boundaries. All changes to objects inside an aggregate must go through the aggregate root.

**Reference:** `phases/03-design.md`

---

### Domain Event

**One-line description:** An immutable record of something significant that happened in the domain, published asynchronously.

**When to use:** When you need to trigger side effects in other parts of the system without creating tight coupling.

**Reference:** `phases/03-design.md`

---

### Domain Service

**One-line description:** A stateless operation that orchestrates multiple aggregates or performs logic that does not belong to a single entity.

**When to use:** When an operation involves multiple aggregates or represents a process the domain is responsible for but no single entity owns.

**Reference:** `phases/03-design.md`

---

### Factory

**One-line description:** Encapsulates complex logic for creating aggregates or entities, ensuring they are always created in a valid state.

**When to use:** When aggregate construction has non-trivial rules or involves multiple steps that must succeed atomically.

**Reference:** `phases/03-design.md`

---

### Specification

**One-line description:** A composable, named predicate that encapsulates a business rule about whether an object satisfies a criterion.

**When to use:** For complex validation or selection rules that need to be combined (`and`, `or`, `not`), reused, or documented as business language.

**Reference:** `phases/03-design.md`

---

## Distributed Systems Patterns

### Saga

**One-line description:** A sequence of local transactions coordinated across services, where each step has a compensating transaction for rollback.

**When to use:** When a business process spans multiple services or databases and ACID transactions are not available. Two styles: choreography (events) and orchestration (central controller).

**Reference:** `phases/04-premortem.md` — Failure Modes section

---

### Outbox Pattern

**One-line description:** Write domain events and business data to the same database transaction; an outbox relay publishes them to the message broker asynchronously.

**When to use:** To guarantee exactly-once delivery of domain events without distributed transactions or two-phase commit.

**Reference:** `phases/04-premortem.md` — Integration Risks section

---

### Idempotent Consumer

**One-line description:** A message consumer that can safely process the same message multiple times without producing duplicate side effects.

**When to use:** When integrating with external message brokers or webhooks that may deliver messages more than once.

**Reference:** `phases/04-premortem.md` — Integration Risks section

---

## Testing Patterns

### Fake Adapter as Test Fixture

**One-line description:** An in-memory implementation of a port interface used exclusively in tests, replacing real infrastructure (database, HTTP, clock).

**When to use:** For every integration test. The fake must exist before the integration test is written. See Tree 2 in `references/decision-trees.md`.

**Reference:** `references/testing-pyramid.md` — Integration Test Fixture Strategy

---

### Test Pyramid

**One-line description:** A layered testing strategy prioritizing many fast unit tests at the base, fewer integration and component tests in the middle, and a small number of slow E2E tests at the top.

**When to use:** As the default strategy for any new test suite. Balances confidence, speed, and maintenance cost.

**Reference:** `references/testing-pyramid.md`

---

### Property-Based Testing

**One-line description:** A testing technique that verifies a rule holds true across hundreds of randomly generated inputs using a library like `fast-check`.

**When to use:** When you can articulate a rule (e.g., "sorting is deterministic", "serialization is reversible") but cannot enumerate all valid inputs.

**Reference:** `references/testing-pyramid.md` — Type 6

---

### Invariant Testing

**One-line description:** A test that verifies a condition must always be true for an aggregate or domain object, regardless of input or history.

**When to use:** To protect core domain rules: "total >= 0", "status transitions are valid", "id is never empty". Write one whenever you discover a rule that must never be broken.

**Reference:** `references/testing-pyramid.md` — Type 5

---

## Pattern Name Usage in Phase 4

When documenting failure modes in Phase 4 (Pre-Mortem), use named patterns to make risks concrete and testable. Named patterns translate generic risks into specific, addressable concerns.

### Example Phase 4 Entry

In `phases/04-premortem.md`, the **Integration Risks** table supports a **Named Pattern** column. Example entries:

| # | Risk | Named Pattern | Component | Mitigation |
|---|------|-------------|-----------|------------|
| 3 | Order placed but payment failed silently — order stuck in pending | Saga choreography failure | OrderService, PaymentGateway | Add timeout watcher + compensating `markOrderFailed` transaction; add idempotency key to payment call |
| 7 | Domain events lost between aggregate and broker | Outbox Pattern failure | EventBus, OrderAggregate | Ensure outbox relay commits event atomically with aggregate; add dead-letter queue |
| 12 | Duplicate payment processed on message retry | Idempotent Consumer failure | PaymentConsumer | Implement idempotency token check on consumer side |

**Why use named patterns:**
- They make the risk **specific** — "Saga compensation failure" tells an engineer exactly what to look for
- They make the risk **testable** — you can write a regression test specifically for "Saga choreography failure on timeout"
- They enable **searchability** — a codebase search for "Outbox Pattern" immediately surfaces all related risks and mitigations
- They create a **shared vocabulary** across the team

*Last updated: 2026-03-28*
