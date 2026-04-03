# TDD: AI-First Testing Methodology

## Core Principle

**NO production code without a failing test first.** This is non-negotiable.

## The TDD Cycle

### RED: Write a Failing Test

1. Write ONE test that describes the behavior you want
2. The test should be:
   - Clearly named (describes the expected behavior)
   - Testing real behavior (not implementation details)
   - Focused (one concept per test)
3. Run the test and verify it FAILS for the RIGHT reason
4. If it passes immediately, the test is wrong — fix or delete it

### GREEN: Make It Pass

1. Write the SIMPLEST code that makes the test pass
2. No extra features, no optimizations, no refactoring
3. Run the test and verify it passes
4. Run ALL tests — verify nothing is broken

### REFACTOR: Clean Up

1. Remove duplication
2. Improve names (variables, functions, files)
3. Extract helpers ONLY if there's actual duplication
4. Run ALL tests — must still pass

## AI-First Testing Enhancements

Beyond basic TDD, incorporate these testing strategies:

### Invariant Tests

Identify **invariants** — properties that must ALWAYS be true regardless of input.

**How to find invariants:**
- Ask: "What must always be true about this system?"
- Look for business rules that have no exceptions
- Find mathematical properties (commutativity, idempotency, etc.)

**Example:**
```javascript
// Invariant: A conversation always has at least one message
test("conversation always has at least one message", () => {
  const conversation = createConversation("Test");
  expect(conversation.messages.length).toBeGreaterThan(0);
});
```

### Property-Based Testing

For functions with clear input/output contracts, use property-based testing.

**When to use:**
- Pure functions with well-defined domains
- Data transformations
- Serialization/deserialization
- Validation logic

**How:**
1. Identify the function's properties (not specific examples)
2. Generate random inputs that satisfy the function's preconditions
3. Assert the property holds for all generated inputs

**Ask user before adding a property-based testing library.** Common options:
- JavaScript: `fast-check`
- Python: `hypothesis`
- Rust: `proptest` (built-in)

### Regression Tests

For every bug found during development:
1. Write a test that reproduces the bug
2. Verify the test fails (demonstrates the bug exists)
3. Fix the bug
4. Verify the test now passes
5. Keep the test forever — it prevents the bug from returning

### Automated Regression Testing

After the feature is complete:
1. Run the full test suite
2. Capture the output as a baseline
3. On future changes, run the suite and compare against baseline
4. Any new failure = potential regression

## Test Organization

Follow the project's existing test conventions (from Phase 2 exploration). If no conventions exist:

```
layers/{domain}/
  composables/
    useFeature.ts
  tests/
    unit/
    properties/
    regression/
    components/
tests/
  e2e/
  fixtures/fakes/
```

See `references/layer-scaffold.md` for the canonical test directory structure.

## Test Quality Checklist

Every test should pass these checks:

- [ ] Tests behavior, not implementation
- [ ] Has a clear, descriptive name
- [ ] Is independent (no test ordering dependencies)
- [ ] Has assertions that can fail (not just "doesn't throw")
- [ ] Covers the happy path AND at least one error case
- [ ] Runs fast (no unnecessary delays, I/O, or network)
- [ ] Is deterministic (same result every time)

## What NOT to Test

Don't write tests for:
- Third-party library behavior (trust the library)
- Simple getters/setters (unless they have logic)
- Framework boilerplate (trust the framework)
- Configuration files (unless they have validation logic)

Focus tests on:
- Business logic and rules
- Edge cases and boundary conditions
- Error handling paths
- Integration between components
- Invariants and properties

## Tests from Requirements, Not Implementations

Tests must derive from the requirement spec or acceptance criteria, not from the implementation code.

**Why this matters:** Tests derived from code encode the code's assumptions. The model writes code reflecting its understanding, writes tests reflecting the same understanding, and both pass — even if the understanding is wrong. Tests derived from requirements provide an independent check. They verify intent, not just behavior.

**How to apply in the TDD cycle:**

In the RED phase, the failing test should start from the requirement:

```javascript
// ✅ From requirement: "should reject expired sessions"
test("rejects expired sessions", () => {
  const session = { token: "abc", expiresAt: Date.now() - 1000 }
  expect(validate(session)).toBe(false)
})

// ❌ From implementation plan: "should check token.expiry > now"
test("checks expiry field", () => {
  const token = { expiry: pastDate }
  expect(isExpired(token)).toBe(true)
})
```

The first describes *what the user needs*. The second describes *how the code works*. The first catches wrong understanding. The second only catches wrong implementation of that understanding.

When writing TDD tests, always reference the task spec's acceptance criteria. If the task spec lacks acceptance criteria, define them before writing the test.

---

## Stack-Specific Tooling (Default Stack: bun + Nuxt Layers + Insforge)

When using the default devloop stack, apply this mapping:

### Tool Selection by Test Type

| Test type | Tool | Run command |
|-----------|------|-------------|
| Unit / business logic | bun test | `bun test` |
| Invariant | bun test | `bun test` |
| Property-based | fast-check + bun test | `bun test` |
| Regression | bun test | `bun test` |
| E2E | playwright | `bunx playwright test` |
| Coverage report | bun test --coverage | `bun test --coverage` |

### File Location Convention (Nuxt Layers)

```
layers/{domain}/
  composables/
    foo.ts
    foo.invariant.test.ts    ← invariant tests co-located
  tests/
    unit/                    ← bun test files
    properties/              ← fast-check + bun test
    regression/              ← bun test regression tests

tests/                       ← project root
  e2e/                       ← playwright (crosses layer boundaries)
  mocks/
    handlers/                ← MSW handlers (shared across unit + browser)
```

### Mocking Insforge

Use MSW (Mock Service Worker) to mock Insforge API calls at the network level.
Do NOT mock at the module import level — MSW mocks work in both unit tests and
Playwright browser tests using the same handler definitions.

```typescript
// tests/mocks/handlers/insforge.ts
import { http, HttpResponse } from 'msw'

export const insforgeHandlers = [
  http.get('https://api.insforge.dev/v1/user', () => {
    return HttpResponse.json({ id: 'test-user', email: 'test@example.com' })
  }),
]
```

### Coverage Thresholds

Set in `bunfig.toml`:
```yaml
coverage:
  thresholds:
    lines: 80       # business logic target
    functions: 80
    branches: 70
```

### Property-Based Testing with fast-check

```typescript
import { test } from 'bun/test'
import fc from 'fast-check'

test('slug is always lowercase and hyphenated', () => {
  fc.assert(
    fc.property(fc.string(), (input) => {
      const slug = toSlug(input)
      expect(slug).toMatch(/^[a-z0-9-]*$/)
    })
  )
})
```
