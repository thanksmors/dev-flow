---
name: implementation
description: Execute the implementation plan using sequential subagents with TDD and quality review
---

# Phase 6: Implementation

**Objective**: Execute the implementation plan using the chosen execution mode, with TDD, quality review, per-task verification, and documentation checks at every step.

**Required skill:** @dev-flow:verification-before-completion

Every claim of success must be backed by fresh verification evidence. No "tests pass" without running the test command and showing output.

---

<HARD-GATE — Fake Adapters First>
Before any task involving an external dependency begins:
✅ A fake adapter interface MUST be defined first (port at `layers/{domain}/ports/`, fake at `layers/{domain}/adapters/FakeXyzAdapter.ts` — see `layer-scaffold.md`)
✅ The fake adapter MUST be wired and working (returns realistic data) before the real adapter is touched
✅ The real adapter MUST NOT be implemented until the fake adapter passes verification
✅ The fake adapter stays permanently — it is not deleted when the real adapter is added

If a task attempts to implement a real adapter before the fake adapter walks: BLOCK → send back to implementer to build the fake first.
</HARD-GATE>

<HARD-GATE — Dependency Approval>
Before adding any new package to the project (production or dev dependency):
✅ Stop and present to the user: "I need to add {package} because {reason}. Approve?"
✅ Wait for explicit user approval before running `bun add`
✅ This gate applies ALWAYS — even in YOLO mode, even for dev dependencies

No exceptions. Adding a dependency is an irreversible project decision that the user must own.
</HARD-GATE>

<HARD-GATE — Task Sizing>
Before implementing any task from the plan, validate its size against these criteria. A task is right-sized when:

✅ **One sentence, one verb** — the task can be described with a single sentence containing one verb
✅ **System stays consistent** — after this task alone, the code compiles and tests pass (even if the feature isn't complete)
✅ **One intention in the diff** — a reviewer would see a single coherent purpose
✅ **Typical size: 3-7 files changed, 50-200 lines net change**

**Too small** = leaves the system in an inconsistent state (e.g., adding a migration column without updating the ORM model). Fix: merge with the next related task.

**Too big** = bundles multiple independent decisions (e.g., "implement OAuth" is really: choose library, design token storage, implement flow, build UI, handle errors). Fix: split into independent right-sized tasks.

If a task fails sizing → adjust the plan before dispatching the implementer. Do not proceed with tasks that are too small or too big.
</HARD-GATE>

<HARD-GATE — Phase 0 Prerequisites>
Before Phase 6 begins, confirm Phase 0 prerequisites passed. If not yet run:
1. Read `dev-flow/preferences/defaults/prerequisites.md`
2. Execute each check
3. If ANY FAIL → block and print remediation instructions
4. Do NOT proceed until all checks pass
</HARD-GATE>

## 6.0 Pre-Flight Check (HARD-GATE)

**Before any task runs, run the gate script.**

Run: `python3 ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase6_start.py`

- Exit 0 → pre-flight passed. Show "✅ Pre-flight passed" and proceed to Step 6.1.
- Exit 1 → gate failed. Print the gate's full output. Then tell the user: "Gate failed — fix the issues above, then run `/dev-flow continue` to re-run."

This is a **HARD-GATE** — no implementer subagents dispatch until pre-flight passes.

## 6.1 Execution Mode

Only one mode exists:

**Sequential Subagents** — I dispatch one subagent per task in order. Each task gets a fresh context, spec review, and quality review before moving to the next.

Record in `state.json` → `executionMode`: `"sequential"`.

---

## 6.2 Sequential Subagents

Read the implementation plan from `docs/superpowers/plans/` (plans are saved here during the workflow).
Extract ALL tasks with their full text upfront (do not re-read the plan per task).

For each task, run the autonomous per-task loop:

### Per-Task Autonomous Loop

**Pre-task check — verify previous task is complete:**
- Has the previous task's changes been committed? (check `git status`)
- If previous task exists but is uncommitted → do NOT start this task until the prior task is verified and committed
- If this is the first task in a slice → record slice start in state.json

<HARD-GATE — Nuxt UI Component Lookup>
Before any task involving UI components or custom CSS:
✅ Search Nuxt UI v4 component registry for existing components
✅ If found: use Nuxt UI component, do not build custom
✅ If not found: document "No Nuxt UI equivalent: [reason]" in task notes
✅ If uncertain: ask before proceeding

Check: https://ui.nuxt.dev
</HARD-GATE>

**Domain Glossary Check:**
Before dispatching the implementer for any task that touches domain code:
1. Read `docs/domain-glossary.md` (if it exists)
2. Pass the relevant domain terms to the implementer as part of the scene-setting context
3. After implementation, flag any introduced synonyms for existing concepts

**1. Dispatch Implementer**

Dispatch the implementer agent (`${CLAUDE_PLUGIN_ROOT}/agents/implementer.md`) with:
- Full task text (objectives, files, steps)
- Scene-setting context: what phase we're in, what was built in previous tasks, relevant C4 architecture context (container/component this task modifies), relevant adapter interfaces from `docs/decisions/`, relevant file paths from `${CLAUDE_PLUGIN_ROOT}/references/layer-scaffold.md`
- Project tech stack and conventions
- **Fake Adapters First reminder**: For any task involving external dependencies (APIs, databases, auth, observability), the fake adapter MUST be implemented before the real adapter. The implementer must demonstrate the fake adapter works end-to-end before any real adapter is touched.

If the implementer asks questions → answer them, then re-dispatch.

**2. Verify (MANDATORY — @verification-before-completion)**

After implementer reports DONE:
- Run the test command for this task
- Log full output in state.json under `verificationLog`
- If tests FAIL → send back to implementer to fix, re-run tests until pass
- Only proceed when tests pass with evidence

**2a. Infrastructure Config Verification (if applicable)**

If this task changed any infrastructure config (docker-compose, .env, port mappings, nginx config, service URLs):
- Verify the service is actually responding at the expected endpoint/port
- Example: if docker-compose port changed from `8080:8080` to `3080:8080`, curl `http://localhost:3080` and confirm a response
- "Container up" ≠ "Container working." Config changes require post-change verification.
- Log the verification result in state.json under `verificationLog`

**3. workspace.dsl update needed?**
      - Does the task introduce a new component (processor, handler, entity, repository, event subscriber)?
      - Does the task change a component's relationships?
      - Does the task introduce a new external dependency (database, cache, message broker)?
      - If yes to any → update `docs/workspace.dsl` model block and views block
      - If no → proceed
      - Reference `references/component-identification.md` scoring matrix if unsure whether a class warrants a component

**4. Spec Compliance Review**

Dispatch the spec reviewer (`${CLAUDE_PLUGIN_ROOT}/agents/spec-reviewer.md`) with:
- The original task spec
- All files changed (with git diff or file contents)
- **Full plan context**: the complete task list for this slice (all tasks that belong to the same vertical slice), so the reviewer can check ordering — was this task executed at the right point in the slice sequence (e.g., adapter tasks before implementation tasks, skeleton before expansion)?

If NOT COMPLIANT → implementer fixes, go back to step 2, re-verify.
Loop until spec reviewer says COMPLIANT. Do NOT proceed to quality review until COMPLIANT.

**5. Code Quality Review**

Dispatch the quality reviewer (`${CLAUDE_PLUGIN_ROOT}/agents/quality-reviewer.md`) with:
- Files changed
- Tests written

If NEEDS WORK on Critical issues → implementer fixes, go back to step 2, re-verify.
Loop until quality reviewer says APPROVED (zero Critical issues).

**5.1 Per-Slice Design Review**

After completing all tasks within a vertical slice (detected when the next task belongs to a different slice, or when the slice's final task is marked done):

1. **Read the slice's design intent** — from `docs/superpowers/specs/` (the design spec for this project) and the slice's section in the implementation plan
2. **Review the slice's committed files** — all files changed across all tasks in this slice
3. **Verify design requirements** — check each requirement from the spec against what was built in this slice
4. **Check diagrams for this slice** — verify state diagrams (`.dev-flow/architecture/states/`) and sequence diagrams (`.dev-flow/architecture/sequences/`) exist for components built in this slice
5. **Verify task ordering** — confirm the slice followed the planned order (adapter/port first → walking skeleton → business logic → edge cases)
6. **Flag deviations** — note any place where this slice's implementation diverged from the design intent

If deviations found → create fix tasks and execute them before proceeding to the next slice.
Log the slice review result in state.json under `sliceReviews`.

**6. Self-Critique Pass**

After quality review approves, run a structured self-critique on the implemented code. Four passes, each producing a list of specific, actionable issues:

| Pass | Checks For | Example Finding |
|------|-----------|-----------------|
| **Correctness** | Null/edge cases, spec fulfillment, off-by-one | "This function doesn't handle the null case for the userId parameter" |
| **Style** | Codebase conventions — naming, imports, error handling | "This file uses fetchUser but the codebase convention is getUser" |
| **Performance** | N+1 queries, unbounded allocations, unnecessary re-renders | "This loop queries the database per iteration instead of batching" |
| **Security** | Injection, auth checks, exposed secrets | "This route handler accepts user input without validation" |

Issues are tagged **critical** (blocks progression — must fix now) or **minor** (queues for polish phase).

If critical issues found → implementer fixes, go back to step 2 (Verify), re-run the loop.
If only minor issues → proceed to next step, minor issues logged for later.

**7. Documentation Update Check**

After each task completes, check five things:

1. **ADR needed?** If this task involved a design pivot, technology swap, or any choice between alternatives with real trade-offs → write a new ADR file in `docs/decisions/` (next number in sequence, e.g. `0004-pivot-{name}.md`).

2. **ADR status update — superseded decisions?** If this task replaced a previous decision, update the old ADR's header:
   - Set `Status: Superseded`
   - Set `Superseded by: [ADR-NNN](000N-new-decision.md)`
   - Add a `Review notes:` entry explaining why the old decision was replaced.

3. **workspace.dsl update needed?** If new containers or components were introduced that differ from the Phase 3 design → update the model and views in `docs/workspace.dsl`.

4. **Docs section update needed?** If the implementation changes what a `docs/architecture/` section describes → update the relevant file (e.g. `02-containers.md` if a container changed).

5. **Fake adapter check?** If this task introduces a new external dependency (auth, API, observability, queue), verify a fake adapter was built before the real adapter. If not, create it now before proceeding.

**7.1 — LESSONS.md Write**
After the quality review loop for each task:
  - Did the implementer ask a clarifying question that revealed a gap in the workflow?
  - Did something "unexpected" happen that the workflow didn't handle?
  - If yes to either → append to `.dev-flow/lessons.md` using the standard format

**7.2 — Frontend Polish Check**

After Code Quality Review, if the task involved UI changes:
- Run `/frontend-normalize` to enforce design token consistency
- Run `/frontend-polish` to add micro-details before marking the task done
- Run `/frontend-animate` if motion was specified in the design

**7.3 — Debugging Escalation & Revert Protocol**

When a task fails (implementer reports failure, tests won't pass, or any blocking error), do NOT immediately rewrite code or guess the fix. Instead, escalate through coordinated hypothesis investigation.

### When Debugging Escalation Triggers

Debugging escalation activates when ANY of:
- The implementer subagent fails the **same task** (consecutive attempts)
- The full test suite becomes non-functional (cannot run — broken deps, corrupted config)
- Any error that blocks forward progress (unresolvable conflict, unhandled exception)

### Round 1 — 3 Hypothesis Agents

1. `git reset --hard` to last green commit
2. Create `.dev-flow/debug.md` with error context:
   ```markdown
   # Debug — {date} — {task name}

   ## Error
   {error message and failing test output}

   ## Task Context
   {task spec, files involved}
   ```
3. Dispatch 3 read-only investigation agents in parallel:
   - **Agent A (Data/State):** Data flow or state issue — wrong values, missing fields, race conditions, stale state
   - **Agent B (Integration/Wiring):** Integration issue — wrong adapter wired, port mismatch, missing dependency, import path error
   - **Agent C (Logic/Algorithm):** Logic error — wrong condition, off-by-one, missing edge case, incorrect transformation
4. Each agent reads code (no edits) and produces: hypothesis, investigation steps, findings, confidence (high/medium/low), recommended fix
5. Update `.dev-flow/debug.md` with all 3 reports
6. Coordinator reads reports, picks most promising path, dispatches implementer subagent to attempt fix
7. **If fix works** → append to `.dev-flow/lessons.md`, delete `.dev-flow/debug.md`, continue workflow
8. **If fix fails** → proceed to Round 2

### Round 2 — 5 Hypothesis Agents

1. `git reset --hard` to last green commit
2. Update `.dev-flow/debug.md` with Round 1 failure (what was tried, why it failed)
3. Dispatch 5 agents with error context PLUS all 3 Round 1 reports:
   - **Agent A (Data/State — deeper):** Serialization, async timing, caching, stale closures
   - **Agent B (Integration — deeper):** DI container, layer boundaries, cross-domain calls, module resolution
   - **Agent C (Environment/Config):** Runtime version mismatch, env var missing, config loading order, build system
   - **Agent D (External Dependency):** External API changed, dependency version conflict, MCP behavior
   - **Agent E (Architecture Violation):** Layering violation, circular dependency, boundary crossing, type mismatch
4. Update `.dev-flow/debug.md` with all 5 reports
5. Coordinator picks best path, dispatches implementer subagent
6. **If fix works** → append to `.dev-flow/lessons.md`, delete `.dev-flow/debug.md`, continue
7. **If fix fails** → proceed to Round 3

### Round 3 — 10 Hypothesis Agents

1. `git reset --hard` to last green commit
2. Update `.dev-flow/debug.md` with Round 1 and Round 2 failure context
3. Dispatch 10 agents with full context of all 8 prior investigations:
   - 5 agents: repeat most promising categories, going even deeper
   - 5 agents: explore entirely new angles (framework internals, timing/race conditions, encoding issues, platform-specific behavior, test infrastructure bugs)
4. Update `.dev-flow/debug.md` with all 10 reports
5. Coordinator picks best path, final fix attempt via implementer subagent
6. **If fix works** → append to `.dev-flow/lessons.md`, delete `.dev-flow/debug.md`, continue
7. **If fix fails** → write Final Report (see below)

### Final Report (after Round 3 fails)

Write to `.dev-flow/debug.md` (NOT deleted — persists for next session):

```markdown
# Debug Report — {date} — {task name}

## Error
{original error message and context}

## Attempts
### Round 1 (3 agents)
- {summary of each hypothesis and finding}
- Fix attempted: {what was tried}
- Result: {why it failed}

### Round 2 (5 agents)
- {summary}
- Fix attempted: {what was tried}
- Result: {why it failed}

### Round 3 (10 agents)
- {summary}
- Fix attempted: {what was tried}
- Result: {why it failed}

## Top Hypotheses (still unresolved)
1. {most likely root cause with evidence}
2. {second most likely}
3. {third most likely}

## Recommended Next Steps
1. {specific action for next session}
2. {specific action for next session}

## Files Involved
- {list of all files touched across all rounds}
```

This report becomes the input for the Phase 6 Adjustment Gate (section 6.9).

### File Lifecycle

| File | Created | Updated | Deleted |
|------|---------|---------|---------|
| `.dev-flow/debug.md` | Round 1 start | Each round (reports + failure context) | On successful fix. Persists if all rounds fail. |
| `.dev-flow/lessons.md` | First lesson ever | On successful fix after debugging | Never deleted — accumulates |

`.dev-flow/` is gitignored — both files survive `git reset --hard`.

### LESSONS.md Append Format (on successful fix)

```markdown
## {date} — {one-line title}

**Error:** {what went wrong}

**Root cause:** {what the winning hypothesis agent found}

**Fix:** {what actually worked}

**Hypotheses explored:** {N agents across R rounds before fix}

**Key insight:** {what made the difference — why earlier rounds missed it}

**Context:** Task {N} — {what was being attempted}
```

### 6.9 — Phase 6 Adjustment Gate

After Phases 1-5 complete and before any Phase 6 task begins (including on resume from revert):

1. Read `.dev-flow/lessons.md`
2. If entries exist:
   - Present to user (AskUserQuestion): "Lesson from last attempt: **{title}** — **{one-line summary}**. Adjust manually or let me auto-update the plan?"
     - **Manual** → pause, let user review lessons and modify tasks/plan before Phase 6 proceeds
     - **AI auto** → AI updates the current task/plan based on lessons, then proceeds
3. If no entries: proceed immediately

This gate is not a HARD-GATE — it's a choice presented to the user at the moment.

**8. Mark Task Complete**

Log in state.json: "Task N: DONE — tests verified, spec compliant, approved"
Proceed to next task.

---

## 6.3 C4 Workspace Sync

After each task that introduces architectural changes, update `docs/workspace.dsl`:

**When to update (per-task check):**
- New processor, handler, entity, repository, or event subscriber added? → update
- Component relationships changed? → update
- New external dependency (database, cache, message broker)? → update
- Component removed or renamed? → update

**How to update:**

1. Open `references/workspace-template.md` — copy the template structure
2. Open `references/dsl-relationship-patterns.md` — use standardized relationship labels
3. For CQRS patterns → see `examples/c4-cqrs-pattern.md`
4. For API endpoints → see `examples/c4-api-endpoint.md`
5. For refactoring → see `examples/c4-refactoring.md`
6. For component decisions → use `references/component-identification.md` scoring matrix

**After updating workspace.dsl:**
1. Run `docker compose up` (or standalone Structurizr Lite at http://localhost:8080)
2. Verify the diagram renders — no parse errors
3. Position components manually (left = entry points, right = external dependencies)
4. Click "Save workspace" in the Structurizr UI
5. Verify `workspace.json` was updated
6. Commit both `workspace.dsl` and `workspace.json` in the same commit as the code

**Relationship label reference:** `references/dsl-relationship-patterns.md`

**What NOT to document (component-identification scoring ≤ 1):**
- DTOs, value objects without validation, test classes, factories

## 6.4 Deferred-Decision Gate (HARD-GATE)

**After all Phase 6 tasks complete, before the Phase 7 checkpoint.**

Run: `python3 ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase6_end.py`

- Exit 0 → all deferred decisions resolved. Proceed directly to the Phase 7 checkpoint.
- Exit 1 → gate failed. Print the gate's full output. For each open item, present the user with: Resolve / Re-defer / Skip. After all items are handled, re-run the gate. Only proceed when the gate exits 0. Tell the user: "Gate failed — handle each open item above, then run `/dev-flow continue` to re-run."

This is a **HARD-GATE on the Phase 7 checkpoint.** The standard checkpoint options are NOT shown until the gate exits 0.

## 6.5 E2E Verification

<HARD-GATE — Playwright must be installed>
Before running expect, verify Playwright is installed:
- @playwright/test in devDependencies
- npx playwright install --with-deps chromium has been run
If not installed → run setup steps before proceeding.
</HARD-GATE>

**When:** After all implementation tasks are complete and all unit/integration tests pass. Before Phase 7 gap analysis.

**What:** Run `expect-cli` against the full branch diff to generate and execute browser smoke tests.

### 6.5.1 Setup (One-time per project)

```bash
npm install -D @playwright/test
npx -y expect-cli@latest init
npx playwright install --with-deps chromium
```

Add to `package.json` scripts:
```json
{
  "test:e2e": "expect-cli -y -t branch",
  "test:e2e:watch": "expect-cli -t branch"
}
```

### 6.5.2 Generate and Run

```bash
# Interactive (review plan before running)
expect-cli -t branch

# Headless (CI / verification pass)
expect-cli -t branch -y
```

**What happens:**
1. `expect-cli` reads the full branch diff (all changes since main)
2. An AI agent generates a test plan from the diff
3. You review the plan (or skip with `-y`)
4. Playwright tests are generated and executed in a real browser
5. Session is recorded for replay

### 6.5.3 Generated Test Location

Generated tests are saved to `tests/e2e/expect-[slug].ts` where `[slug]` is the flow name from the diff analysis. Each flow is a separate file.

**Commit generated tests.** They are regression tests — real browser coverage that prevents UI regressions. Without committing, the coverage disappears on the next run.

### 6.5.4 Re-running Existing Flows

To replay an existing flow without regenerating:
```bash
expect-cli -f [slug] -y
```

To update an existing flow (re-generate from current diff):
```bash
expect-cli -f [slug] -t branch -y
```

### 6.5.5 CI Integration

Add to CI pipeline after Phase 6 verification:

```yaml
# Example: GitHub Actions
- name: E2E Verification
  run: npm run test:e2e
  env:
    NO_TELEMETRY: 1
```

`expect-cli -y` exits 0 on success, 1 on failure — standard CI signal.

### 6.5.6 Relationship to TDD

E2E verification with `expect` does NOT replace TDD. The order is:

```
TDD (unit + integration tests written BEFORE implementation)
  → implementation tasks
  → Phase 6.5 E2E Verification (expect reads diff, generates browser smoke)
  → Phase 7 Gap Analysis
```

Unit and integration tests are written first (TDD). `expect` generates browser tests after the fact from what was actually built. Both are required for full coverage.

---

## 6.6 Design Compliance Review

**When:** After ALL implementation tasks are complete (after the per-task loop exits), before the Quality Gate and Checkpoint.

**What:** Read the design spec at `docs/superpowers/specs/` that corresponds to the plan being executed. Compare the full implementation against the spec:

1. **Find the matching design spec** — for each plan in `docs/superpowers/plans/`, there is a corresponding spec in `docs/superpowers/specs/` with the same date/topic
2. **Read the design spec** — understand the goals, principles, and specific requirements
3. **Read the implementation** — review all files changed across all tasks
4. **Check each design requirement** — verify it was implemented as specified
5. **Check design principles** — verify the implementation honors the architectural principles stated in the spec
6. **Check diagrams** — verify state diagrams (`.dev-flow/architecture/states/`), sequence diagrams (`.dev-flow/architecture/sequences/`), and C4 components were created as specified. Check `docs/workspace.dsl` — verify the C4 model (containers, components, relationships) matches the implementation and was enriched iteratively per container.
7. **Flag deviations** — note any place where implementation diverged from design intent

**Output:** Present a brief summary to the user:
- Which design requirements were met
- Any deviations or gaps
- Whether the design intent was honored
- State of all diagrams (created / missing / outdated)

**If deviations found:** Create a task to fix them before the Checkpoint, or document them as accepted divergences with reason.

---

## 6.7 Quality Gate

Before Phase 7, verify ALL of the following:

- [ ] ALL tasks have verification evidence (test output logged per task in state.json)
- [ ] ALL spec reviews: COMPLIANT (per task)
- [ ] ALL quality reviews: APPROVED (zero Critical issues per task)
- [ ] Full test suite passes (fresh run — show full output)
- [ ] No skipped tests or warnings
- [ ] All pre-mortem mitigations implemented and tested
- [ ] ADRs written for all implementation decisions (`docs/decisions/`)
- [ ] `docs/workspace.dsl` reflects what was actually built (new components added, relationships updated)
- [ ] workspace.dsl was iteratively enriched — each container enriched and committed before moving to the next
- [ ] Both workspace.dsl and workspace.json committed together
- [ ] State diagrams created in `.dev-flow/architecture/states/` for all components identified in Phase 3
- [ ] State diagrams referenced in `docs/architecture/04-key-flows.md`
- [ ] ALL slice design reviews done (per-slice checkpoints from step 5.1 — one per vertical slice)
- [ ] ALL slice reviews passed — deviations fixed or documented as accepted
- [ ] Per-task diagram check passed — each task that introduced a component has corresponding state/sequence diagrams
- [ ] `docs/architecture/` sections updated where implementation diverged from design
- [ ] `state.json` reflects completed work and verificationLog is populated
- [ ] ALL new external dependencies have fake adapters that walk before real adapters are introduced
- [ ] All UI tasks have Nuxt UI component lookup documented
- [ ] Self-critique pass completed for every task (correctness, style, performance, security)
- [ ] Domain glossary at `docs/domain-glossary.md` referenced during implementation (if domain code was touched)
- [ ] All 7 test types are represented in the test suite (check `references/testing-pyramid.md` for the complete list)
- [ ] All deferred decisions reviewed at Section 6.4 gate (hard gate passed)

---

## 6.8 Engram Save

```
mem_save key: {engramProjectKey}-phase6
content: implementation summary — tasks completed, total tests, key decisions made during implementation, any deviations from plan
```

## Documentation Update Check

"Review `docs/workspace.dsl` and `docs/architecture/` — does the model reflect what was actually built? Update any sections that diverged from the Phase 3 design. Write an ADR for any implementation decision not yet recorded in `docs/decisions/`."

## Phase 6 Checkpoint

Before presenting options:

1. Run Section 6.4 Deferred-Decision Gate — ALL open items must be resolved, re-deferred, or skipped before proceeding
2. Present Phase 7 checkpoint options:

Options: [Continue to Gap Analysis] [Pause] [End]
