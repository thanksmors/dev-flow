# Extras Phase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new Extras phase between Phase 6 and Phase 7, containing the AI-suggests → user-selects → implement → verify workflow.

**Architecture:** Extras is a new markdown phase file that orchestrator calls by name. It reads project context, generates 6 suggestions, presents them to the user, implements selections with Phase 6 discipline, and re-verifies before passing to Phase 7 gap analysis.

**Tech Stack:** dev-flow phase files (markdown), no code, no tests required for the phase itself.

---

## File Map

| File | Change |
|------|--------|
| `dev-flow/.claude-plugin/phases/06-extras.md` | Create — new Extras phase |
| `dev-flow/.claude-plugin/phases/06-implementation.md` | Modify — add Extras reference in Phase 6 checkpoint |
| `.dev-flow/extras-backlog.md` | Create — backlog template (used by Extras phase) |

---

### Task 1: Create Extras phase file

**Files:**
- Create: `dev-flow/.claude-plugin/phases/06-extras.md`

- [ ] **Step 1: Write the Extras phase file**

Create `dev-flow/.claude-plugin/phases/06-extras.md` with the following content:

```markdown
---
name: extras
description: AI proposes 6 improvements, user selects, implemented with Phase 6 discipline, verified before Phase 7
---

# Phase: Extras

**Objective**: After Phase 6 is verified, generate suggestions for improvements across
Features, Quality-of-life, and Technical categories. Let the user select which ones
to pursue. Implement selected improvements with full TDD and verification. Prove the
tech stack is extensible.

**Required skill:** @dev-flow:verification-before-completion

## Extras 1: Generate Suggestions

Read the full project context:
- Current codebase (key files, recent changes)
- Phase 6 artifacts (`docs/superpowers/plans/`, `docs/superpowers/specs/`)
- Existing docs (README, architecture, C4 diagrams)
- `.dev-flow/extras-backlog.md` (if exists — to avoid duplicating suggestions already proposed)

Generate **exactly 6** suggested improvements, exactly 2 from each category:
- **Features** — new capabilities the project could have
- **Quality-of-life** — DX improvements (tooling, docs, scripts)
- **Technical** — performance, refactoring, robustness

For each suggestion, output in this exact format:

```
{n}. {Name}
   Category: {Feature | QoL | Technical}
   Description: {2-3 sentence description of what this adds}
   Effort: {Low | Medium | High}
   Complexity: {Low | Medium | High}
```

Rules:
- Suggestions must be specific to this project — not generic boilerplate
- Do NOT suggest something already implemented or in the current plan
- Check `.dev-flow/extras-backlog.md` first — do not repeat items from the backlog
- Aim for variety — don't suggest 3 refactorings when there are already 2 in the list

## Extras 2: Present to User

Present all 6 suggestions in this format:

```
## Suggested Improvements

1. {Name} — {Feature} — {Effort} effort, {Complexity} complexity
   {Description}

2. {Name} — {QoL} — {Effort} effort, {Complexity} complexity
   {Description}

... (6 items total)

Select improvements to implement. Enter numbers separated by commas (e.g. 1, 3, 5),
or leave blank to skip Extras and proceed to Phase 7.
```

Wait for user input. Empty input (blank line) = skip Extras, proceed to Phase 7.

## Extras 3: Implement Selected Improvements

For each selected improvement:

1. **Write a minimal spec** — save to `docs/superpowers/specs/YYYY-MM-DD-extras-{slug}.md`
   - One sentence on what this adds
   - 2-3 sentences on why it matters
   - Basic approach (no more than 3-4 sentences)
   - Acceptance criteria (2-3 bullet points)

2. **Implement with TDD** — follow the same per-task loop from Phase 6:
   - Write a failing test first
   - Implement the minimal code
   - Verify test passes
   - Commit

3. **Verify** — run the test command, confirm output passes

Repeat for each selected improvement. If multiple improvements are selected,
implement them one at a time (same as Phase 6 sequential subagents).

## Extras 4: Update Backlog

After user selection (even if user selected none), append all unselected suggestions
to `.dev-flow/extras-backlog.md`.

If `.dev-flow/extras-backlog.md` does not exist, create it:

```markdown
# Extras Backlog

Unselected suggestions from Extras phase, accumulated across projects.
Do not re-propose items already in this backlog.

<!-- -- >
```

Then append:

```markdown
## {YYYY-MM-DD} — {project name}

- [1] **{Name}** — {category} — {effort} effort, {complexity} complexity
  {Description}
- [2] **{Name}** — {category} — {effort} effort, {complexity} complexity
  {Description}

```

(Include all 6 items, not just the unselected ones — the backlog tracks what was offered.)

## Extras 5: Phase 6 Verification

After all selected improvements are implemented, re-run Phase 6 verification:

1. **Run full test suite** — must pass (no skipped tests, no warnings)
2. **Verify docs updated** — all changed files reflected in docs
3. **Verify workspace.dsl** — updated if any architecture changes

Do NOT proceed to Phase 7 until all three pass.

Present output to user with:
```
## Extras Complete

Implemented: {N} improvements
Tests: {pass/fail}
Docs: {updated/not updated}
DSL: {updated/not updated}
```

## Extras Gate

No independent gate. Phase passes when Extras 5 verification passes.
If no improvements were selected, this step is skipped.

## Transition to Phase 7

After Extras completes (or is skipped), proceed directly to Phase 7 gap analysis.
Phase 7 audits the full system — including any improvements implemented in Extras.
```

- [ ] **Step 2: Commit**

```bash
git add dev-flow/.claude-plugin/phases/06-extras.md
git commit -m "feat(dev-flow): add Extras phase

Phase 6-extras: AI proposes 6 improvements, user selects,
implemented with TDD, verified before Phase 7 gap analysis.
Unselected items saved to extras-backlog.md.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: Add Extras reference to Phase 6 checkpoint

**Files:**
- Modify: `dev-flow/.claude-plugin/phases/06-implementation.md`

- [ ] **Step 1: Add Extras to Phase 6 checkpoint options**

Read the Phase 6 `## Phase 6 Checkpoint` section. Find the options list (the three options: Continue, Pause, End).

Add a note after the options:
```
**After Extras completes, proceed to Phase 7 (gap analysis).**
```

Or insert as a fourth option:
```
- [Continue to Extras] — Phase 7: Gap Analysis will run after Extras
```

- [ ] **Step 2: Commit**

```bash
git add dev-flow/.claude-plugin/phases/06-implementation.md
git commit -m "feat(dev-flow): reference Extras phase in Phase 6 checkpoint

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: Create extras-backlog.md template

**Files:**
- Create: `.dev-flow/extras-backlog.md`

- [ ] **Step 1: Create the backlog file**

Create `.dev-flow/extras-backlog.md`:

```markdown
# Extras Backlog

Unselected suggestions from Extras phase, accumulated across projects.
Do not re-propose items already in this backlog.

<!-- -- >
```

- [ ] **Step 2: Commit**

```bash
git add .dev-flow/extras-backlog.md
git commit -m "feat(dev-flow): add extras-backlog.md template

Backlog for unselected improvement suggestions from Extras phase.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Self-Review Checklist

1. **Spec coverage:**
   - [x] Extras 1: Generate 6 suggestions (2 per category) → Task 1, step 1
   - [x] Extras 2: Present to user with format → Task 1, step 1
   - [x] Extras 3: Implement selected with TDD → Task 1, step 1
   - [x] Extras 4: Update backlog → Task 1, step 1
   - [x] Extras 5: Phase 6 verification → Task 1, step 1
   - [x] Backlog file creation → Task 3
   - [x] Phase 6 checkpoint reference → Task 2

2. **Placeholder scan:** No TBD/TODO. All steps have actual content.

3. **Type consistency:** All file paths are exact. No type/signature drift.

4. **No missing tasks:** All spec requirements mapped to tasks.

---

## Execution Options

**Plan complete and saved to `docs/superpowers/plans/2026-04-01-extras-phase.md`.**

Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
