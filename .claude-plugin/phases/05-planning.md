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

### 5.4 Mark Deferred Decisions

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

### Slice 1: {name}

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
- [ ] Every task follows the TDD cycle (test → implement → verify)
- [ ] Every task specifies exact file paths and commands
- [ ] All risk mitigations from Phase 4 are mapped to tasks
- [ ] All deferred decisions are tagged and have adapter interfaces
- [ ] Tasks are ordered correctly (dependencies respected)
- [ ] The plan is self-contained (implementer needs no extra context)
- [ ] State and decision journal are updated

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
