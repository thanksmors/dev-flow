# Why: Test-First (TDD)

## The Red/Green/Refactor Cycle

Test-driven development follows a three-step cycle:

1. **Red** — Write a test for the behavior you want. Run it. It must fail, because the code it tests doesn't exist yet.
2. **Green** — Write the minimal code needed to make the test pass. No more. The test is the spec; the code exists to satisfy it.
3. **Refactor** — With the test passing, now improve the code's structure, clarity, or performance. The test is your safety net.

This cycle is short. Minutes, not hours. Each iteration produces a small, tested, working piece of code.

---

## Why Writing the Test First Forces You to Define "Done"

When you write the test first, you have to answer a question before you write any code: what does "done" look like?

This sounds simple, but it is surprisingly powerful. Most bugs, misunderstandings, and rework come from starting implementation without a clear definition of success. When you write the test first:

- You think about the interface before the implementation. What should this function accept? What should it return? What should it be called?
- You think about the contract, not the mechanism. The test expresses what you want; the code figures out how.
- You have a precise "done" marker. The test passes = done. Not "I think it's done" or "it seems to work."

Without a test first, "done" is subjective. You decide you're done when you're tired of working on it, or when it looks right, or when you run out of time. Tests written after the fact codify whatever you built, whether or not it was what you meant to build.

---

## Why Tests Written After Are Always Worse

There is a fundamental difference between tests written before and tests written after:

**Tests written before** verify that your code does what you intended. They are specifications written in executable form.

**Tests written after** verify that your code does what it does. They document the implementation, not the intent.

When you write code first and tests after, you unconsciously code to the implementation rather than the specification. The test becomes a description of how the code works, not what problem it solves. This has two consequences:

1. **The tests miss the point.** They verify the mechanics (this function was called, this value was returned) but not the correctness (this is the right answer for this input).
2. **The tests don't catch regression usefully.** When a bug is fixed, the test that should have caught it was written to match the buggy behavior. It passes because it describes what the code does, not what it should do.

There is also a psychological effect: if the code already exists and the tests don't pass, most people adjust the tests rather than question the code. "The test must be wrong" is easier than "I need to rethink this." Test-first forces the code to prove itself against the spec, not the other way around.

---

## AI-First TDD Specifics

When an autonomous agent writes code, TDD is not just a best practice — it is the primary mechanism for maintaining architectural integrity and preventing drift.

**Tests as specifications.** For an AI agent, a passing test suite is the most precise specification available. The agent writes what it wants in the test, then writes code to satisfy it. This is faster than iterative human review and produces a more objective "done" signal.

**Property-based testing.** Beyond example-based tests (assert that X returns Y), AI agents can generate property-based tests that verify invariants across many inputs. For example: "after any sequence of operations, the system state is consistent." This catches edge cases that example-based tests would need hundreds of examples to cover.

**Regression suites.** The test suite produced during TDD becomes the regression suite for the lifetime of the code. When the agent makes changes in a future session, the test suite tells it immediately whether it broke something it didn't intend to. This is especially important in autonomous mode, where the agent may not have a human reviewing every change.

**Test coverage as a forcing function.** A minimum coverage threshold (e.g., 80% of branches) prevents the agent from writing tests that only cover the happy path. Edge cases and error conditions must be tested explicitly, or the coverage threshold is not met.

---

## When TDD Is Required vs When It's Optional

**Required: all production code.** Any code that will ship to users, run in production, or affect system behavior must be test-first. This includes:
- Business logic and domain rules
- Port interfaces and adapters
- Data transformations and validators
- Error handling paths
- Authentication and authorization logic

**Optional: prototypes and spikes.** When exploring an unfamiliar API, testing an architecture decision, or building a one-off proof-of-concept, the overhead of test-first may exceed the value. In these cases, the code is explicitly marked as prototype code and will be rewritten test-first when it becomes production code.

The key distinction: if the code will exist in the final system, it must be test-first from inception. Retrofitting tests onto production code produces worse tests and worse architecture than writing them first.

---

## What "Minimal Code to Make It Pass" Means

Green phase has one rule: write the smallest amount of code that makes the test pass. Do not implement features. Do not generalize. Do not prepare for future requirements.

Here is why this matters: the test is your spec. If the test says "this function returns the number 5 for input 2," then the minimal code is `return 5`. Even if the real function should handle all integers, even if there should be a database lookup, even if there is a more elegant algorithm. The test only says 5 for 2. So you return 5.

The power of this is that you are always working in small, verified increments. Each step is correct by construction. Generalization and feature expansion happen in the refactor phase, when you have passing tests and a clear reason to change the structure.

If you find yourself needing to implement a feature before the test passes, the test is underspecified. Write a more complete test first.

---

## Summary

Test-first is not about having a test suite for its own sake. It is a discipline that forces you to define success before you start, protects you from regression as the system grows, and provides an objective signal that work is done. For autonomous agents, TDD is especially critical: it is the mechanism that keeps the agent's output aligned with the intended architecture and prevents architectural drift that would be expensive to fix later.
