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
