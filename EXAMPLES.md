# Examples

These are the canonical patterns for dev-flow. Subagents and workflow steps replicate these exactly. When in doubt, follow these examples — do not invent new ones.

---

## 1. Verification Evidence (The Iron Law in Practice)

The Iron Law: Every claim requires evidence. "Done" means shown, not told.

### CORRECT — Verification Evidence Provided

```
After implementing the feature, I ran:
$ pytest tests/unit/test_auth.py -v

Output:
tests/unit/test_auth.py::test_returns_fake_user PASSED
tests/unit/test_auth.py::test_auth_port_delegates_to_adapter PASSED
2 passed in 0.03s

Verification: both tests pass with real output shown. Implementation complete.
```

### INCORRECT — Claim Without Evidence

```
Tests pass. Implementation complete.
```

The first version shows the actual output. The second makes a claim with no proof. When a subagent reports "done" without evidence, the workflow rejects it.

---

## 2. Fake Adapter Pattern

Always introduce external dependencies through the fake-first sequence. The fake adapter lets the skeleton walk before credentials exist.

### CORRECT — Fake First Sequence

```
Step 1: Define port interface in layers/notifications/ports/NotificationPort.ts
Step 2: Create fake adapter layers/notifications/adapters/FakeNotificationAdapter.ts (in-memory)
Step 3: Wire fake adapter into port — skeleton walks
Step 4: Verify skeleton walks on fake adapter
Step 5: THEN create real adapter layers/notifications/adapters/SMTPNotificationAdapter.ts
```

### INCORRECT — Real First (Blocks Verification)

```
Started by implementing the real SendGrid adapter directly.
Tests fail because we don't have SendGrid credentials.
Can't verify anything without credentials.
```

Real-first leaves you unable to verify. Fake-first lets the skeleton walk immediately.

### Proving the Pattern Works

To swap from fake to real, change ONE line in the port:

```typescript
// Skeleton phase — fake adapter
import { FakeNotificationAdapter } from 'layers/notifications/adapters/FakeNotificationAdapter'
const adapter: NotificationPort = new FakeNotificationAdapter()

// Production phase — real adapter
import { SMTPNotificationAdapter } from 'layers/notifications/adapters/SMTPNotificationAdapter'
const adapter: NotificationPort = new SMTPNotificationAdapter()
```

Nothing else changes. The interface is the contract.

---

## 3. Spec Compliance

When a task spec defines what to build, compliance means following every requirement. Deviation requires explicit approval.

### Example Task

> "Add a `useWelcomePort.ts` port that returns a welcome message"

### COMPLIANT — Follows the Spec Exactly

```
- Created layers/welcome/ports/WelcomePort.ts
- Port imports from types/welcome.ts only
- Port delegates to adapter (no fetch inside port)
- Fake adapter returns realistic welcome message
- Component uses the port, never imports adapter directly
```

### NOT COMPLIANT — Violates the Pattern

```
- Added fetch() call directly inside composable
- Component importing from adapters/ directly
- No types file, no interface defined
```

### Why Compliance Matters

The port/adapter pattern exists so:
- Components never know about external services
- Adapters are swappable without changing components
- Testing uses in-memory fakes, not mocks

Violations break this. A composable with `fetch()` inside it cannot be tested without network. A component importing an adapter directly cannot have its adapter swapped.

---

## 4. Task Done Report Format

When a subagent finishes a task, it reports using this exact format:

### Required Format

```markdown
## Done Report

**Status:** DONE

**Verification Evidence:**
```
$ pytest tests/path/test_feature.py -v
tests/path/test_feature.py::test_it_works PASSED
1 passed in 0.12s
```

**What was implemented:**
- Created `layers/orders/ports/FeaturePort.ts` (port with typed interface)
- Created `layers/orders/adapters/FakeFeatureAdapter.ts` (in-memory, same interface)
- Created `layers/orders/components/FeatureCard.vue` (component uses port only)

**Files changed:** 3 new files
**Tests:** 1 test, passing
**Deviations from spec:** None
**Fake adapter verified:** Yes — skeleton walks on fake data
```

### Key Elements

| Field | Required | Purpose |
|---|---|---|
| Status | Yes | Must be DONE or BLOCKED |
| Verification Evidence | Yes | Real command + real output |
| What was implemented | Yes | Bullet list of what changed |
| Files changed | Yes | Count + nature of changes |
| Tests | Yes | Count + pass/fail |
| Deviations from spec | Yes | None, or explicit list |
| Fake adapter verified | Yes | Confirms skeleton walks |

### If Blocked

```markdown
## Done Report

**Status:** BLOCKED

**Blocker:** Cannot create real adapter without credentials

**What was implemented:**
- Created port interface
- Created fake adapter

**What is waiting:**
- DevOps to provision SMTP credentials
- Credentials will be stored in .env

**Verification Evidence:**
```
$ pytest tests/path/test_feature.py -v
tests/path/test_feature.py::test_fake_adapter PASSED
1 passed in 0.08s
```
```

---

## 5. ADR Format (Canonical)

Architecture Decision Records document significant choices. Every ADR uses this format.

### Required Fields

```markdown
# 0003. Deferred SQLite for Postgres

Date: 2026-03-28
Status: Accepted

## Context
The walking skeleton used SQLite as the simplest option. Now the skeleton walks. We need to decide whether to keep SQLite or swap to Postgres.

## Decision
Keep SQLite for now. Deferred decisions are only swapped when the cost of the simple option exceeds the cost of the swap. SQLite is still cheap enough.

## Options Considered
- **SQLite**: Simple, zero config, no credentials — kept for now
- **Postgres**: Production-grade, recommended for production — deferred

## Consequences
- Keeps iteration speed high during skeleton phase
- Swap to Postgres requires: write Postgres adapter, run full test suite, update connection config
- Adapter interface already defined — swap is one import line change

## Auto-Selected
Yes — YOLO context, fewest dependencies, most reversible
```

### Field Definitions

| Field | Purpose |
|---|---|
| Date | ISO date of decision |
| Status | Accepted, Deprecated, or Superseded |
| Context | The situation that requires a decision |
| Decision | What was decided and why |
| Options Considered | Alternatives with pros/cons |
| Consequences | Benefits and costs of the decision |
| Auto-Selected | Why this was the right call for YOLO mode |

### Numbering

ADRs are numbered sequentially: 0001, 0002, 0003. The number is permanent even if the ADR is deprecated.

---

## 6. Phase Gate — Hard Gates vs Soft Gates

Phase gates validate that prerequisites are met before proceeding. HARD-GATE failures block execution until fixed.

### HARD-GATE PASS

```
[Phase 5b Pre-Implementation Gate]
✅ Plan exists at .dev-flow/plans/implementation.md with tasks
✅ Phase 5 complete (all phases 1-5 in completedPhases)
✅ User approved plan at Phase 5 checkpoint (recorded in state.json)
✅ Execution mode: Sequential Subagents (only mode)
✅ YOLO confirmed (session flag set)

GATE PASSED — proceeding to Phase 6
```

### HARD-GATE FAIL (Blocks Phase 6)

```
[Phase 5b Pre-Implementation Gate]
❌ Plan does not exist at .dev-flow/plans/implementation.md
❌ Phase 4 not in completedPhases

GATE FAILED — cannot proceed to Phase 6
Fix failures and re-run gate before continuing.
```

### Soft Gate (Warning Only)

```
[Phase 3 Pre-Execution Gate]
⚠ No plan found at .dev-flow/plans/planning.md
⚠ Execution can proceed in YOLO mode

Press ENTER to continue or Ctrl+C to abort
```

Soft gates warn but do not block. Hard gates fail and stop.

### Gate Checklist by Phase

| Phase | Gate Type | What It Checks |
|---|---|---|
| 2 (Specification) | Soft | Plan file exists |
| 3 (Planning) | Soft | Tasks are defined |
| 5b (Pre-Implementation) | HARD | All prior phases complete, user approved plan |
| 6 (Execution) | HARD | All phase 5b checks pass |
| 7 (Verification) | HARD | Tests exist and pass |
| 8 (Completion) | Soft | User confirms acceptance |

---

## Quick Reference: What Good Looks Like

| Pattern | Correct | Wrong |
|---|---|---|
| Verification | Real command + real output | "It works" |
| New dependency | Fake adapter first, then real | Real adapter without fake |
| Task reporting | Done report with evidence | "Done" with no proof |
| ADR | All required fields filled | Missing Context or Consequences |
| Phase gate | Hard gates block on failure | Ignoring gate failures |
| Spec compliance | Follows every requirement | Skips steps or invents alternatives |
