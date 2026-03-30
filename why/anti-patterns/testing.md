# Testing Anti-Patterns

Anti-patterns related to test quality, mocking practices, test isolation, and verification strategies.

---

## Test-Only Pass

**What it is:** Tests that assert nothing meaningful — they run without errors but never verify any behavior. The test body might be empty or contain only a trivial assertion like `expect(result).toBeDefined()`.

**Why it looks right:** The test runs. No errors. CI passes. Having the test file provides "coverage." The pattern was copied from elsewhere in the codebase where it supposedly works.

**The actual problem:** A passing test with no assertions provides zero confidence. The code could do anything — return correct results, return wrong results, throw exceptions, or corrupt state — and the test would still pass. This anti-pattern is worse than no tests because it creates an illusion of safety while providing none.

**Likelihood in autonomous context:** High

**How to detect it:**
- Test files contain only `expect(result).toBeDefined()` or `expect(result).toBeTruthy()`
- Test files are 3 lines long (describe + it + one assertion)
- Multiple tests have identical bodies
- `git diff` shows tests added in bulk with no logic changes

**The fix:** Every test must verify a meaningful outcome; if the behavior isn't worth asserting, the test shouldn't exist.

---

## Assertion-Less Tests (Tautological)

**What it is:** Tests that assert something trivially true — `expect(result).toBe(result)`, `expect(x).toEqual(x)`, or `expect(() => fn()).not.toThrow()` with no expectation that the function could throw.

**Why it looks right:** The test runs. It feels like it's checking something. Adding assertions seems like "over-specifying" when the code is obviously correct. Noting that a function doesn't throw is still testing something, right?

**The actual problem:** A tautological assertion passes regardless of what the code does. `expect(x).toBe(x)` passes whether x is correct, wrong, or mutated. The test provides the same confidence as flipping a coin — 50% chance of passing if the code is broken. `not.toThrow()` is particularly dangerous because most production code doesn't throw for the happy path.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Both sides of `toBe` or `toEqual` are the same variable
- Only `not.toThrow()` is asserted in a test that doesn't exercise error paths
- Assertions are copied from other tests without adapting to the current context
- The test could be replaced with `console.log` and provide the same information

**The fix:** Assert on specific outcomes with specific expected values; verify error handling explicitly, not just "it doesn't throw."

---

## Test Ordering Dependency

**What it is:** Tests that must run in a specific order to pass — test B depends on state created by test A, test C must run after B, etc.

**Why it looks right:** Setting up shared state once and reusing it across tests saves time. The tests work when run in order. This pattern appears common in legacy codebases.

**The actual problem:** Test runners in random order produce different failures each run. Tests cannot be run individually or in parallel. When a test fails, it may not be clear whether the failure is in the test or in the system. Debugging requires running the entire suite from the beginning. CI pipelines become flaky and slow.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- `vitest` random-order mode produces different failures on each run
- A test imports state from another test file
- Test suite cannot be split across multiple CI jobs
- Running a single test file fails, but running the full suite passes
- `beforeAll` or `beforeEach` sets up shared state that tests don't reset

**The fix:** Each test must set up its own required state; tests should be order-independent and capable of running in isolation.

---

## Over-Mocking

**What it is:** Mocking so extensively that the test verifies almost nothing real — most of the test is mock setup, the actual system under test is never called, and the assertions check mock interactions rather than outcomes.

**Why it looks right:** Mocking external dependencies (databases, APIs, file systems) ensures tests run fast and don't depend on external systems. Complete control over dependencies means deterministic tests. This is "professional" testing practice.

**The actual problem:** The test verifies that the code calls mocks correctly, not that it solves the actual problem. When a mock doesn't match the real behavior, the test passes but production fails. The code under test becomes impossible to test without writing complex mock setups. The test and the production code drift apart.

**Likelihood in autonomous context:** Medium-High

**How to detect it:**
- Mock setup exceeds the test logic in line count
- `vi.mock()` or `vi.spyOn()` appears in more than 50% of test files
- Tests check `expect(mock).toHaveBeenCalledWith(...)` but never assert on the actual return value
- The test could pass even if the implementation were replaced with a no-op function

**The fix:** Mock at the boundary of the system (external dependencies); test actual behavior for code within the system boundary.

---

## Skipped Tests

**What it is:** Tests that are commented out or marked with `test.skip()`, `test.skip()`, `it.skip`, `xit`, `xtest`, or `describe.skip` and left in the codebase.

**Why it looks right:** The test is temporarily disabled while working on something else. It will be fixed "later." The test represents valuable work that shouldn't be deleted. CI passes because skipped tests don't fail.

**The actual problem:** Skipped tests rot — the code they test changes, and the skipped test becomes increasingly irrelevant. Developers learn to ignore skipped tests, so real failures blend into the noise. The test surface area decreases silently. Eventually, skipped tests are deleted without being fixed, wasting the original effort.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- `git grep -E "skip|todo|xit|xtest" -- "*.test.ts"` finds disabled tests
- Test suite reports "N tests skipped"
- Commented-out test blocks exist in test files
- A test file has a `describe.skip` at the top with a note "re-enable after fixing X"

**The fix:** Either fix the test or delete it; never commit skipped tests; track skipped work in issue trackers, not in code.

---

## Golden Path Only Testing

**What it is:** Tests that only verify the happy path — they assert on successful execution with valid inputs but never test error handling, edge cases, or invalid states.

**Why it looks right:** The happy path is the most important path. Testing every error condition feels like writing tests for the test suite. Valid inputs produce valid outputs, which is what matters.

**The actual problem:** The test suite provides false confidence. When the code receives unexpected input, corrupted data, or edge cases, the tests don't catch it. Error paths are the most likely places for bugs, and they go untested. Production incidents occur in the "impossible" error conditions that weren't tested.

**Likelihood in autonomous context:** High

**How to detect it:**
- Test files contain only assertions for the success case
- No tests exercise `throw` paths or error branches
- Tests use only "golden" input values (e.g., valid email formats, positive numbers)
- Code coverage is high but edge case coverage is low

**The fix:** Identify error paths and add tests for each; verify that exceptions are thrown and caught correctly under adverse conditions.

---

## Copy-Paste Test Patterns

**What it is:** Test files that are copies of other test files with minor modifications, producing duplicated logic without duplicated understanding.

**Why it looks right:** The existing test works, so copying it is faster than writing from scratch. The pattern is proven. It would take too long to understand the existing tests well enough to write new ones from scratch.

**The actual problem:** If the original test had a bug, the bug is copied. If the domain logic changes, multiple test files must be updated. The test suite grows without improving coverage. It becomes impossible to know which test file is authoritative.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Two test files have identical `beforeEach` blocks or setup logic
- Test file names differ only by number (e.g., `service.test.ts`, `service2.test.ts`)
- A bug fix requires editing multiple test files with the same change
- `git log` shows test files added with messages like "copy of X"

**The fix:** Extract shared test utilities and fixtures; write tests from scratch based on the specification rather than copying existing tests.
