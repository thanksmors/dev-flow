# Dev Flow — Core Principles

These principles are non-negotiable. Every subagent, every phase, and every workflow dispatch operates under these rules. They override everything else.

---

## 1. Iron Law: Verification Before Completion

**No completion claims without running verification commands and showing fresh evidence.**

This is the single most important principle. Every time a claim is made that work is done, the claim must be backed by live output from a verification command.

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | Actual test runner output (not a summary) |
| "Implemented" | Show the code that was written |
| "Works" | Show a successful run with real output |
| "Refactored" | Show before/after with evidence of equivalent behavior |
| "Deployed" | Show the deployment command output and health check |

### Examples

**WRONG:**
> "All tests pass. Implementation is complete."

**RIGHT:**
> "Tests pass. Here is the output:
> ```
> ✓ 12 tests passed in 234ms
> ✓ 5 tests passed in 89ms
> All 17 tests passing.
> ```"

**WRONG:**
> "I've added the user authentication module."

**RIGHT:**
> "I've added the user authentication module. Here is the key file at `layers/auth/composables/useAuth.ts`:
> ```typescript
> export async function authenticateUser(token: string): Promise<User> {
>   // ...
> }
> ```"

### Reference

See `skills/verification-before-completion/SKILL.md` for the full verification methodology.

---

## 2. Fake Adapters First

**Every external dependency gets a fake adapter before the real one.**

External dependencies include: APIs, databases, authentication services, observability platforms, file storage, message queues, and any other system you do not control.

### The Rule

1. **Define the interface first** — what does your code call?
2. **Build a fake that satisfies the same interface** — in-memory data, hardcoded responses, or a stub that logs what it would have done
3. **Make the skeleton walk on the fake** — run the full flow using the fake adapter
4. **Only then** — build or integrate the real adapter

### Why Fakes First?

- Fakes expose interface mismatches before you have a working system
- Fakes make it impossible to accidentally call a real dependency during development
- Fakes enable offline work and fast test runs
- Fakes force you to think about the interface, not the implementation

### Examples

**Building a payment processor:**

```
WRONG:  Write real Stripe integration → test against Stripe → ship
RIGHT:  Define PaymentAdapter interface → write InMemoryPaymentAdapter → run all flows → then write StripeAdapter
```

**Building an LLM client:**

```
WRONG:  Call OpenAI directly → handle errors → iterate
RIGHT:  Define LLMClient interface → write FakeLLMClient → run all flows → then write OpenAIClient
```

### The Fake Adapter Contract

A fake adapter must:
- Satisfy the **exact same interface** as the real adapter (same method signatures, same return types)
- Use **in-memory or hardcoded data** — no network calls
- Produce **deterministic, fast** responses suitable for test runs
- Log its invocations so you can verify the skeleton is calling it correctly

### Non-Negotiable

No real adapter is introduced until:
1. The fake adapter is complete and passes all tests
2. The skeleton runs end-to-end on the fake
3. The real adapter's interface is identical to the fake's interface

---

## 3. Agents Are First-Class Citizens

**Subagents use the same interfaces and ports as humans — no backdoor access.**

Every workflow operation available to a human must be available to a subagent through the same APIs and routes. Subagents must never bypass user-facing interfaces.

### The Rule

- Subagents interact through the **same APIs** that the UI or CLI uses
- Every **user-facing operation** must also be agent-compatible
- Agents operate with the **same permissions** as the triggering user (no elevated privileges)
- No **special routes, internal endpoints, or debug interfaces** that agents use but humans cannot

### Examples

**WRONG:**
> Agent bypasses the task creation API and writes directly to the database to "move faster"

**RIGHT:**
> Agent creates tasks through the same `TaskCreate/TaskUpdate` tools that a human uses, writing to the same state files and APIs.

**WRONG:**
> Agent uses an internal `/admin/fix-errors` endpoint that is not exposed to users

**RIGHT:**
> All operations go through user-facing interfaces. If a capability is needed for agents, it is first designed as a proper interface and then made available to both agents and humans.

### Why It Matters

- Agents and humans must see the **same behavior** and get the **same results**
- Backdoor access creates hidden coupling that breaks in production
- First-class agent compatibility forces good API design
- It prevents the "works for me" problem where agents produce outputs that humans cannot replicate or audit

---

## 4. Swappability Is the Goal

**Every external dependency must be swappable without touching the core.**

External dependencies include: backend services, authentication providers, LLM providers, observability platforms, databases, file storage, and any integration point.

### The Rule

1. **Design adapter interfaces from day one** — even when only a fake exists
2. **Never hardcode a dependency** — always route through an adapter
3. **Isolate the boundary** — the core knows nothing about the outside world
4. **Make swapping trivial** — changing from Postgres to SQLite, or OpenAI to Anthropic, should take minutes, not days

### The Boundary Test

Ask: *"If I ripped out X and replaced it with Y, how much code would I have to change?"*

- If the answer is "almost nothing in the core" — the boundary is correct
- If the answer is "half the codebase" — a boundary was crossed

### Examples

**Database swapping:**

```
WRONG:  Repository class directly calls pg.connect() from 'pg' package
RIGHT:  Repository class calls DatabaseAdapter interface → InMemoryDatabaseAdapter in dev → PostgresAdapter in prod
```

**LLM swapping:**

```
WRONG:  Code imports openai directly and calls openai.chat.completions.create()
RIGHT:  Code calls LLMClient interface → FakeLLMClient in tests → OpenAIClient or AnthropicClient in prod
```

**Observability swapping:**

```
WRONG:  Code calls console.log and process.emit('warning')
RIGHT:  Code calls ObservabilityAdapter interface → ConsoleAdapter in dev → DatadogAdapter or OTelAdapter in prod
```

### Non-Negotiable

If swapping X requires changing Y, something crossed a boundary it should not have. Redesign the interface.

---

## 5. TDD Discipline

**No production code without a failing test first.**

TDD is not optional. It is the discipline that keeps the codebase verifiable and the refactoring ability intact.

### The Cycle

```
1. Write a failing test   →  Verify RED
2. Write minimal code    →  Verify GREEN
3. Refactor              →  Verify GREEN still holds
4. Repeat
```

### Rules

- **RED before GREEN** — a test must fail before you write code to make it pass. If the test passes before you wrote the code, the test is not testing what you think it is.
- **Minimal code** — write only the code needed to make the failing test pass. No speculation, no "I'll add it later."
- **Tests are never skipped** — no `skip`, no `.only`, no "I'll fix the test later."
- **One concept per test** — if a test checks multiple things, split it.

### What Counts as a Test?

- Unit tests with assertions
- Integration tests that verify component interaction
- End-to-end tests that verify user-facing behavior
- Property-based tests that verify invariants across many inputs

### When TDD Is Not Required

- Prototyping and spike explorations (clearly marked as temporary)
- Configuration files and infrastructure-as-code
- Documentation files

Once a prototype becomes real code, the TDD cycle begins.

---

## 6. Strict Phase Gates

**No phase begins until the previous phase's gate is fully verified and logged.**

Phase gates are hard barriers. Skipping a gate is not an option.

### The Gates

| Gate | Requirement |
|------|-------------|
| Phase 5b (Pre-Implementation Gate) | All Phase 5 deliverables complete. All Phase 1-4 artifacts reviewed and approved. No blocking issues. HARD-GATE — Phase 6 cannot start without passing this. |
| Phase 7 (Gap Analysis Gate) | Phase 6 implementation complete. All tests passing. All ADRs written. Phase 7 cannot start until Phase 6 quality gate is verified. |
| Phase 8 (Completion Gate) | All Phase 7 gaps resolved. Quality review complete. Final verification run. Phase 8 cannot start until all Phase 7 gaps are closed. |

### Gate Verification

Before crossing any gate:

1. **Read the gate criteria** in the phase file
2. **Verify each criterion** with live output (test results, build output, file existence)
3. **Log the gate result** in `state.json` under the phase's quality gate section
4. **If the gate fails** — do not proceed. Fix the issues first.

### Gate Failure Protocol

If a gate check fails:

1. Document which criteria failed and why
2. Present the failures to the user
3. Ask: "Retry the gate, pause the workflow, or end?"
4. Never proceed past a failed gate — no exceptions

### Why Gates Exist

Without gates, small problems compound into large ones. Phase 5b gate prevents entering implementation with a flawed design. Phase 7 gate ensures quality before review. Phase 8 gate ensures completeness before reporting. Gates are the discipline that keeps every phase's output honest.

---

## Summary

| # | Principle | Core Message |
|---|-----------|--------------|
| 1 | Iron Law | Show evidence, not claims |
| 2 | Fake Adapters First | Walk on fakes before real infrastructure |
| 3 | Agents Are First-Class | Same APIs for agents and humans |
| 4 | Swappability Is the Goal | Design for replacement from day one |
| 5 | TDD Discipline | Red before green, always |
| 6 | Strict Phase Gates | No skipping, no shortcuts |
