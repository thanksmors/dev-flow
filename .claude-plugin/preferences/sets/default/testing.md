# Testing Philosophy

## Fake Adapters as Test Fixtures

Fake adapters are the **primary integration test fixture** for this stack. They:
- Stay permanently (never deleted when a real adapter is added)
- Serve as in-memory stand-ins for all external dependencies
- Are co-located with the domain they serve
- Satisfy the exact same interface as the real adapter

When writing integration tests, import the fake adapter directly — do NOT use MSW for domain-level mocking. MSW is only appropriate for mocking external HTTP APIs that have no fake adapter.

```typescript
import { FakeTaskAdapter } from '~/layers/tasks/adapters/FakeTaskAdapter'
// Use directly in tests — no MSW handler needed
```

## Core Rule
TDD — no production code without a failing test first.
Cycle: RED (write failing test) → GREEN (minimal code to pass) → REFACTOR (clean up)

## Test Types & Tools

| # | Test Type | Tool | What It Tests | Location |
|---|-----------|------|---------------|----------|
| 1 | Unit | bun test | Pure business logic in isolation | Co-located with module (`.test.ts`) |
| 2 | Integration | bun test + fake adapter | Port adapter wiring, component interaction | `layers/{domain}/tests/integration/` |
| 3 | E2E | playwright | Critical cross-layer user journeys | `tests/e2e/` |
| 4 | Invariant | bun test | Properties always true regardless of input | Co-located (`.invariant.test.ts`) |
| 5 | Property-based | fast-check + bun test | Rules across many random inputs | `layers/{domain}/tests/properties/` |
| 6 | Regression | bun test | One test per bug, kept forever | `layers/{domain}/tests/regression/` |
| 7 | Architecture | ts-arch (or equivalent) | Dependency rule: layers point inward only | `layers/{domain}/tests/architecture/` |

**Why no component tests:** Vue/Nuxt component rendering tests require `@vue/test-utils` which is incompatible with the Bun runtime (WeakMap internals). Component behavior is verified visually and through E2E tests instead.

### Fake Adapters as Primary Integration Fixture

Fake adapters are the **primary integration test fixture**. They stay permanently, serve as in-memory stand-ins for all external dependencies, and satisfy the exact same interface as the real adapter. MSW is a last-resort option only for external HTTP APIs that have no port and no fake adapter available.

### Coverage Thresholds

```yaml
# bunfig.toml (business logic thresholds)
coverage:
  thresholds:
    lines: 80
    functions: 80
    branches: 70
```

Run coverage with: `bun test --coverage`

## Test Quality Rules
- Test behavior, not implementation
- Clear descriptive names ("should reject expired sessions", not "test1")
- Independent — no ordering dependencies between tests
- Must have assertions that can actually fail
- Cover happy path AND at least one error/edge case
- Deterministic — same result every run
