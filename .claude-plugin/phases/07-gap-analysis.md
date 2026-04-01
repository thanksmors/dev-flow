---
name: gap-analysis
description: Systematically identify gaps in tests, documentation, error handling, and edge cases
---

# Phase 7: Gap Analysis & Loop

**Objective**: Systematically identify gaps in tests, documentation, error handling, and edge cases. Loop back to implementation to fill gaps autonomously until all Critical and Important gaps are resolved.

<HARD-GATE>
You cannot enter Phase 7 (Gap Analysis) until:
✅ Phase 6 is complete (all tasks done, verification evidence in state.json)
✅ Full test suite has been run and passes (verification-before-completion evidence)
✅ All spec and quality reviews are approved
✅ state.json reflects all completed work
✅ **Both Phase 6 gates passed:**
  - gate_phase6_evidence.py exited 0
  - gate_phase6_end.py exited 0
</HARD-GATE>

When the HARD-GATE passes: log gate pass in state.json under `gatePasses.prePhase7`, then proceed.

## Steps

### 7.1 YOLO Decision Review (HI-2)

**Before gap analysis begins**, review any YOLO auto-selected decisions from Phase 6.

1. Read `.dev-flow/state.json` for `yoloFlaggedDecisions[]`
2. If array is non-empty, present each YOLO ADR:
   ```
   YOLO Decision — auto-selected during Phase 6:
   ADR-{NN}: {title}
   {one-line summary of what was decided}

   [Confirm this decision] [Revise it]
   ```
3. If user selects Revise → pause to let user modify the ADR
4. Gate re-checks after revision
5. Only proceed to gap analysis once all YOLO decisions are confirmed

If `yoloFlaggedDecisions[]` is empty: proceed immediately to 7.2.

### 7.2 Systematic Gap Analysis

Analyze the implementation across these dimensions:

**Test Coverage Gaps**
- Are there untested code paths?
- Are there untested error handling branches?
- Are invariant tests missing for critical business rules?
- Are property-based tests warranted but missing?
- Are integration tests covering the full flow?
- Run test coverage tool (if available) and identify uncovered lines

**Documentation Gaps**
- Does `docs/workspace.dsl` match the actual containers/components built?
- Are all `docs/architecture/` sections accurate (no stale descriptions)?
- Are all significant decisions captured as ADRs in `docs/decisions/`?
- Are API endpoints documented?
- Are adapter interfaces documented?
- Is the folder structure documentation accurate?
- Are there TODO/FIXME comments that should be addressed?

**Error Handling Gaps**
- Are all error paths tested?
- Are error messages user-friendly?
- Is there proper logging for debugging?
- Are failures recoverable where they should be?
- Are there silent failures that should surface errors?

**Edge Case Gaps**
- Review the pre-mortem document — are all edge cases covered?
- Test with empty inputs, null values, boundary values
- Test concurrent access (if applicable)
- Test with malformed data

**Architecture Gaps**
- Do the actual components match the C4 diagrams?
- Does the actual component structure in workspace.dsl match what was built? (new components added? relationships updated? obsolete components removed?)
- Are adapter interfaces clean enough for future swaps?
- Is there unnecessary coupling between components?
- Are there missing abstractions that would help maintenance?

**Security Gaps**
- Input validation on all external inputs
- Authentication/authorization on all protected endpoints
- No hardcoded secrets or credentials
- Proper error messages (no stack traces to users)

- [ ] README exists at project root and passes the AI Slop Test
  - Run `/frontend-audit` on the README — does it look like something a human wrote for this specific project?
  - Check: generic filler language, vague "a modern app", no actual description of what was built
  - If it fails → add to task list for Phase 8

### 7.2.x — LESSONS.md Write Trigger
If any gap is found during this session:
  - Append to `.dev-flow/lessons.md` with:
    - Context: what gap was found
    - Gap: what the workflow didn't cover
    - Resolution: what was done to fix it (or "pending" if deferred)
  - Never edit existing entries — only append new ones

### 7.3.x — AI Slop Test Check

For any UI work found in the gap analysis:
- Run `/frontend-audit` on the rendered output
- Does any component trigger the AI Slop Test?
- If yes → add to gap list with `/frontend-critique` recommendation

### 7.3 Document Findings

Write to `.dev-flow/reports/gap-analysis.md`:

```markdown
# Gap Analysis — {feature name}

## Summary
- Total gaps found: {N}
- Critical: {N}
- Important: {N}
- Minor: {N}

## Test Coverage Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|

## Documentation Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|

## Error Handling Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|

## Edge Case Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|

## Architecture Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|

## Security Gaps
| # | Gap | Location | Severity | Fix Effort |
|---|-----|----------|----------|-----------|
```

### 7.4 Autonomous Gap Fix Loop

This is an **autonomous loop** — iterate until all Critical and Important gaps are resolved. The user is not asked to approve fixes — the loop proceeds automatically and logs decisions.

**Iteration:**

1. **Prioritize** gaps: Critical > Important > Minor
2. **For Critical and Important gaps:**
   - Write failing test first (TDD)
   - Implement the fix
   - Run tests → show output → verify pass
   - Log the fix in gap-analysis.md with evidence
   - If workspace.dsl is out of sync with code: update workspace.dsl using `references/workspace-template.md` and the worked examples (`examples/c4-*.md`). Commit both workspace.dsl and workspace.json together.
3. **For Minor gaps:**
   - Document as "deferred" in gap-analysis.md with reason
   - Log as deferred
4. **After each gap fix:**
   - Mark gap as fixed in gap-analysis.md with verification evidence
   - Run full test suite → show full output
   - If failures → fix before proceeding
5. **After all Critical/Important gaps fixed:**
   - Log loop completion in state.json
   - Present summary to user (non-blocking): gaps found, fixed, deferred
   - Exit loop

After each gap-fix iteration:
  - If the fix revealed a workflow gap not previously documented → append to .dev-flow/lessons.md

Max 5 iterations. If gaps remain after 5 iterations, document and proceed with remaining gaps noted.

### Documentation Update Check

After each gap-fix cycle: "Do the fixes require any documentation updates?"

Max 5 iterations. If gaps remain after 5 iterations, document them and proceed.

### 7.4.5 ADR Currency Review

**Before the critical/important gap review, verify all ADRs in `docs/decisions/` are current.**

1. **Read all ADR files** in `docs/decisions/` (e.g. `0001-*.md`, `0002-*.md`, ...).
2. **Check each ADR's `Status:` field:**
   - Flag any ADR with `Status: Accepted` that has NOT been reviewed in the current session (no prior review evidence in state.json).
   - Flag any ADR with `Status: Accepted` that should be `Superseded` — e.g., a new ADR was written during this session that replaces it.
3. **Auto-update stale ADRs:**
   - If a new ADR supersedes an existing one, update the old ADR's header:
     - Set `Status: Superseded`
     - Set `Superseded by: [ADR-NNN](000N-new-decision.md)`
     - Add a `Review notes:` entry explaining why it was superseded.
4. **Log results** in the gap analysis report under a new "ADR Currency" section:
   ```markdown
   ## ADR Currency
   - ADRs reviewed: {N}
   - ADRs updated: {N} (list each)
   - Stale ADRs flagged: {N} (list each, if any require human review)
   ```
5. If any ADR requires human decision (e.g., is `Accepted` but no clear replacement exists), flag it for the checkpoint.

**This step runs once per gap-analysis session, before the gap-fix loop.**

### 7.5 Update Structurizr Artifacts

After each gap-fix cycle, update the following if anything changed:

**`docs/workspace.dsl`** — if architecture changed (new component, renamed container, removed element): update the model and views. Structurizr Lite auto-refreshes on save.

**`docs/architecture/`** — update the section that describes what changed:
- New component added → update `03-components.md`
- Flow changed → update `04-key-flows.md`
- Dev setup changed → update `05-development-guide.md`

**`docs/decisions/`** — write a new ADR for any gap-fix that was architectural in nature:

```markdown
# N. Gap Fix: {short name}

Date: YYYY-MM-DD
Status: Accepted

## Context

Gap identified in Phase 7 gap analysis: {describe the gap}

## Decision

{What was done to fix it}

## Consequences

{What changed as a result — what's easier or harder now}
```

**`state.json`** — update with final artifact paths.

## Quality Gate

Before checkpoint, verify:

- [ ] All 6 gap categories have been analyzed
- [ ] All Critical gaps are fixed
- [ ] All Important gaps are fixed (or explicitly deferred with user approval)
- [ ] The gap analysis document is up to date
- [ ] All tests still pass after fixes
- [ ] `docs/workspace.dsl` reflects the actual implementation (no C4 drift)
- [ ] All `docs/architecture/` sections are accurate
- [ ] All significant gap-fix decisions have ADRs in `docs/decisions/`
- [ ] Named patterns used correctly in gap analysis (reference `why/NAMED_PATTERNS.md`)
  - CQRS, saga, outbox, idempotent consumer terms used precisely, not generically
  - No "distributed transaction" when "saga compensation failure" is meant
- [ ] `state.json` is updated

### Engram Save

Before presenting the checkpoint:

1. Call `mem_save` with:
   - key: `{engramProjectKey}-phase7`
   - content: gap analysis summary — gaps found, gaps closed, remaining known issues

## Checkpoint

Present to the user:

1. **Gap analysis summary**: Total found, fixed, remaining
2. **Critical/Important gaps** — all should be fixed
3. **Minor gaps** — list remaining ones
4. **Iterations** completed
5. **Recommendation**: Whether to proceed to completion or do another gap analysis pass
6. Options: [Continue to Completion Report] [Pause] [End]
