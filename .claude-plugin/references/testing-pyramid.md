# Testing Pyramid

The testing pyramid is a conceptual model that organizes tests by scope, speed, and fidelity. The shape reflects both the proportion of tests expected at each level and the order in which to consider test types when writing.

```
                    / E2E (few) \
                  /  Integration  \
              /─────────────────────\
            /  Unit + Invariant +     \
          /   Property-based + Regression  \
        /      Architecture Tests          \
      /─────────────────────────────────────\
```

**Principle:** Write the smallest, fastest, most focused test that gives you confidence. Move up the pyramid only when lower-level tests cannot catch the class of bug you fear.

---

## The 7 Test Types in Detail

### Type 1 — Unit

| Attribute | Detail |
|-----------|--------|
| **What it tests** | Pure business logic: transformations, calculations, validation rules, state machine transitions — no I/O |
| **Ratio target** | ~40% of total test suite |
| **Key rule** | If a function touches a port (file system, network, clock), it is not a unit test. Extract a port first. |
| **Location** | `tests/unit/` or co-located `*.spec.ts` next to the domain module |
| **Example** | `calculateTax(subtotal, rate)` returns `15.0` for inputs `(100, 0.15)` |

### Type 2 — Integration

| Attribute | Detail |
|-----------|--------|
| **What it tests** | Port-and-adapter wiring — that domain logic correctly consumes and produces through ports, using real or fake adapters |
| **Ratio target** | ~15% of total test suite |
| **Key rule** | A fake adapter must exist for every port before writing integration tests. Hard-gate: no integration test without a fake. |
| **Location** | `tests/integration/` using `tests/fixtures/fakes/` |
| **Example** | `OrderRepository` port is wired to a `FakeOrderRepository`; verify that `placeOrder()` persists the aggregate correctly |

### Type 3 — E2E (End-to-End)

| Attribute | Detail |
|-----------|--------|
| **What it tests** | Complete user journeys through the full stack, from UI to database and external services |
| **Ratio target** | ~5% of total test suite |
| **Key rule** | Test only the handful of journeys that, if broken, halt the product. Every E2E test is expensive. Use `expect-cli` (Phase 6.6) to auto-generate browser tests from branch diffs. |
| **Location** | `tests/e2e/` <br>For auto-generated E2E from branch diffs, see Phase 6.6. |
| **Example** | "User signs up, completes onboarding, creates a resource, and receives a confirmation email" |

### Type 4 — Invariant

| Attribute | Detail |
|-----------|--------|
| **What it tests** | A condition that must be true regardless of input — e.g., "order total >= 0" or "id is always a non-empty string" |
| **Ratio target** | ~5% of total test suite |
| **Key rule** | Invariant tests are the cheapest way to find bugs in core domain rules. Write them whenever you discover a rule that must never be broken. |
| **Location** | `tests/invariant/` or co-located with the aggregate they protect |
| **Example** | `invariant: order.status cannot transition from 'shipped' back to 'pending'` |

### Type 5 — Property-Based

| Attribute | Detail |
|-----------|--------|
| **What it tests** | A rule that holds across many randomly generated inputs (using `fast-check`) |
| **Ratio target** | ~5% of total test suite |
| **Key rule** | Use when you can articulate a rule but not enumerate all valid inputs. Generate hundreds of inputs automatically. |
| **Location** | `tests/property/` or co-located with the rule they test |
| **Example** | "Reversing a string twice returns the original string" — run against 1,000 random UTF-8 strings |

### Type 6 — Regression

| Attribute | Detail |
|-----------|--------|
| **What it tests** | A bug that was fixed and must never regress. Written AFTER a bug is discovered and fixed. |
| **Ratio target** | ~10% of total test suite |
| **Key rule** | Regression tests are temporary by design. Mark them with a `// TODO: remove if no longer needed after v2` comment and review on each major release. |
| **Location** | `tests/regression/` |
| **Example** | `// Regression: NullRef thrown when orderId is UUID v7 and itemCount > 99` |

### Type 7 — Architecture

| Attribute | Detail |
|-----------|--------|
| **What it tests** | Layer dependency rules, module boundaries, and architectural constraints (e.g., "domain may not import infrastructure") |
| **Ratio target** | ~5% of total test suite |
| **Key rule** | Architecture tests are specifications, not tests. They document the invariant structure of the codebase. Run them in CI. |
| **Location** | `tests/architecture/` or `tests/ts-arch.spec.ts` |
| **Example** | `expect(project).to adhereTo(layers(['domain', 'application', 'infrastructure']))` |

---

## Decision: Which Test Type First?

When you need to decide which test type to write, follow **Tree 1** in `references/decision-trees.md`.

Quick reference:

```
Pure business logic, no I/O?           → Unit (Type 1)
Port ↔ adapter wiring?                  → Integration (Type 2)
Critical cross-layer user journey?     → E2E (Type 3)
Property true regardless of input?    → Invariant (Type 4)
Rule across many random inputs?         → Property-Based (Type 5)
Bug fix that must not regress?          → Regression (Type 6)
Layer dependency rules?                 → Architecture (Type 7)
Anything unusual or ambiguous?         → Human decision
```

---

## Integration Test Fixture Strategy

Every integration test requires a **fake adapter** as a test fixture. The fake must implement the same port interface as the real adapter.

```
tests/
└── fixtures/
    └── fakes/
        ├── FakeOrderRepository.ts    # implements OrderRepository port
        ├── FakePaymentGateway.ts     # implements PaymentGateway port
        └── FakeEventBus.ts           # implements EventBus port
```

**Rule:** The fake must be created and verified BEFORE writing the integration test. See Tree 2 in `references/decision-trees.md` for the full decision flow.

---

## Coverage Targets

| Layer | Test Type(s) | Target Coverage | Notes |
|-------|-------------|-----------------|-------|
| Domain logic | Unit (Type 1) | 90%+ | Pure functions, validation, state transitions |
| Domain invariants | Invariant (Type 4) | 100% of known invariants | Every aggregate root invariant has a test |
| Port/adapter wiring | Integration (Type 2) | 80%+ | Every port has at least one integration test |
| Critical user journeys | E2E (Type 3) | 3–7 key journeys | Expensive; keep to an absolute minimum |
| Random-input rules | Property-Based (Type 5) | Key domain rules | Use fast-check; 100+ iterations |
| Regression | Regression (Type 6) | 100% of fixed bugs | Review for removal on major releases |
| Layer boundaries | Architecture (Type 7) | 100% of declared layers | Enforce in CI |

*Last updated: 2026-03-30*
