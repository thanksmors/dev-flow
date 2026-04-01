---
name: planning
description: Create a detailed, bite-sized implementation plan with TDD tasks for each vertical slice
---

# Phase 5: Planning

**Objective**: Create a detailed, bite-sized implementation plan with TDD tasks for each vertical slice, incorporating risk mitigations and deferred decisions.

## Steps

### 5.1 Create Task Breakdown

For each vertical slice (from Phase 3), create **bite-sized tasks**:

- Each task should take 2-5 minutes to implement
- Tasks follow the TDD cycle: write failing test → implement → verify pass → refactor
- Each task includes:
  - Exact file path(s) to create/modify
  - What the test should verify
  - The minimal implementation to pass the test
  - The exact command to run tests
  - Expected output

Read `${CLAUDE_PLUGIN_ROOT}/references/tdd-ai-first.md` for the testing methodology.
Read `${CLAUDE_PLUGIN_ROOT}/references/layer-scaffold.md` for the canonical file paths (ports, adapters, types, test locations) used when writing task file references.

### 5.2 Incorporate Risk Mitigations

For each vertical slice, integrate the risk mitigations from Phase 4:

- Map each mitigation to a specific task
- Ensure edge case tests are included as separate tasks
- Mark which tasks are "risk mitigation" tasks vs "feature" tasks

### 5.3 Order Tasks Within Each Slice

Within each vertical slice, order tasks:

1. **Interface / adapter first** (for deferred architectural decisions — see `layer-scaffold.md` for port + adapter file paths)
2. **Walking skeleton components** (if this is the first slice)
3. **Core business logic** (with tests)
4. **Edge case handling** (with tests)
5. **Error handling** (with tests)
6. **Integration tests** (end-to-end for the slice)

### 5.4 Convert Pre-Mortem Risks to Tasks (AR-4)

After the Phase 4 pre-mortem, convert each identified risk into a tracked implementation task:

1. Read `.dev-flow/plans/premortem.md`
2. For each risk, determine if it warrants an implementation task:
   - **Has mitigation that can be tested?** → create a task with the mitigation as the implementation
   - **Risk is acceptable without action?** → add "accepted" note to the risk
   - **No clear mitigation?** → flag for discussion before proceeding
3. For each task created from a risk, tag it with `risk-mitigation` type
4. Verify every pre-mortem risk has either a mapped task or an accepted note

**Every pre-mortem risk MUST have a corresponding implementation task or an explicit "accepted" note.**
If a risk has neither, the Phase 5 gate fails.

### 5.5 Mark Deferred Decisions

For each task that involves a deferred architectural decision:
- Tag it with `[DEFERRED: {decision name}]`
- Include the adapter interface that must be used
- Note what the "simple" implementation looks like now
- Note what the "production" implementation will be swapped in later

### 5.5 Document the Plan

Write the implementation plan to `.dev-flow/plans/implementation.md`:

```markdown
# Implementation Plan — {feature name}

## Overview
{brief summary of what will be built}

## Vertical Slices
{ordered list of slices with brief scope}

## Tasks

### Slice 0: Walking Skeleton (AR-3)

**Task 0.1: DI Composition Root**
- **File**: `app/diComposition.ts`
- **Type**: implementation
- **TDD cycle**: RED → GREEN → REFACTOR
- **Test**: {what to test — e.g., "adapter resolves from container"}
- **Implementation**: Create DI container, wire at least one fake adapter
- **Verify**: `{command}` → `{expected output}`

**Task 0.2: End-to-End Flow**
- **File**: `server/api/{endpoint}.ts`, `layers/{domain}/domain/{entity}.ts`
- **Type**: implementation
- **TDD cycle**: RED → GREEN → REFACTOR
- **Test**: {e2e test — one flow, read or create}
- **Implementation**: One server route + one domain function + one test
- **Verify**: `{command}` → `{expected output}`

**Acceptance criteria for Slice 0:**
- [ ] App starts without errors
- [ ] `bun test` runs without errors
- [ ] One E2E flow works (read or create)
- [ ] At least one fake adapter wired

### Slice 1: {name}

| # | Task | Status | Wired | Type | Tags |
|---|------|--------|-------|------|------|
| 1.1 | {description} | pending | | test | |
| 1.2 | {description} | pending | | implementation | |

#### Task 1.1: {description}
- **File**: `{path}` — use canonical paths from `layer-scaffold.md` (e.g. `layers/{domain}/ports/`, `layers/{domain}/adapters/FakeXyzAdapter.ts`)
- **Type**: test | implementation | refactor | risk-mitigation
- **TDD cycle**: RED → GREEN → REFACTOR
- **Test**: {what to test}
- **Implementation**: {minimal code to pass}
- **Verify**: `{command}` → `{expected output}`
- **Tags**: [DEFERRED: {name}] (if applicable)

#### Task 1.2: {description}
...

### Slice 2: {name}
...

## Pre-Mortem Risk Mitigations (AR-4)

For each risk from `.dev-flow/plans/premortem.md`:

### [RISK] {risk name}
- **Source:** Pre-mortem Risk #{N}
- **Risk:** {one-line description}
- **Mitigation:** {what we'll do}
- **Acceptance criteria:** {test that proves mitigation works}
- **Mapped to task(s):** Task {X.Y}, Task {X.Z}

Every pre-mortem risk MUST have a corresponding implementation task or an explicit "accepted" note.
Risks without tasks = Phase 5 gate fail.
```

### 5.6 Plan Review

Review the plan for:

- **Completeness**: Does every vertical slice have tasks? Does every risk mitigation have a task?
- **Order**: Are dependencies respected? Is the walking skeleton first?
- **TDD compliance**: Does every implementation task have a preceding test task?
- **Clarity**: Could someone with no context execute each task?
- **Deferred decisions**: Are all adapter interfaces defined before they're used?

### 5.7 Update State and Journal

- Update `state.json`:
  - `artifacts.planDoc`: `.dev-flow/plans/implementation.md`
- Record planning decisions in the decision journal
- Record any scope adjustments made during planning

## Quality Gate

Before checkpoint, verify:

- [ ] Every vertical slice has a complete set of tasks
- [ ] Slice 0 (Walking Skeleton) is the first slice with acceptance criteria (AR-3)
- [ ] Every task follows the TDD cycle (test → implement → verify)
- [ ] Every task specifies exact file paths and commands
- [ ] Plan task table includes `Status` and `Wired` columns (AR-3/HI-3)
- [ ] All risk mitigations from Phase 4 are mapped to tasks (AR-4)
- [ ] Every pre-mortem risk has either a corresponding task or an accepted note (AR-4)
- [ ] All deferred decisions are tagged and have adapter interfaces
- [ ] Tasks are ordered correctly (dependencies respected, walking skeleton first)
- [ ] The plan is self-contained (implementer needs no extra context)
- [ ] State and decision journal are updated

### Documentation Review (ST-3 — Soft Gate)

This is a **soft gate** — the orchestrator asks, the user can proceed, but the prompt makes review obvious.

After Phase 5 completes, present the review prompt:

```
Implementation plan ready. Review before Phase 6:
- Plan: .dev-flow/plans/implementation.md
- Pre-mortem risks: .dev-flow/plans/premortem.md
- Architecture: .dev-flow/architecture/

Have you reviewed the plan? [Yes, proceed] [Not yet]
```

This is implemented as an explicit checklist item in the Phase 5 quality gate above.

### Engram Save

Before presenting the checkpoint:

1. Call `mem_save` with:
   - key: `{engramProjectKey}-phase5`
   - content: phase summary — key findings, decisions made, artifacts produced
2. Update `state.json` with completed phase and artifact paths

### Documentation Update Check

Ask: "Does anything need updating in project docs (C4 diagrams, decision journal, architecture docs, README)?"
If yes — update before presenting checkpoint.

## Checkpoint

Present to the user:

1. **Plan summary**: Number of slices, total tasks, estimated complexity
2. **Walking skeleton scope** (first slice tasks)
3. **Deferred decisions** and their locations in the plan
4. **Risk mitigations** integrated into tasks
5. **Any concerns** about the plan
6. Options: [Approve Plan & Start Implementation] [Pause] [End]
