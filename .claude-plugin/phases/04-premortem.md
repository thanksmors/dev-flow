---
name: premortem
description: Identify potential bugs, edge cases, failure modes, and risks before implementation begins
---

# Phase 4: Pre-Mortem

**Objective**: Identify potential bugs, edge cases, failure modes, and risks BEFORE implementation begins. Then iterate through a plan-fix-verify loop until all issues are addressed.

## Steps

### 4.1 Conduct Pre-Mortem Analysis

Imagine the feature has been implemented and **failed in production**. Ask: "What went wrong?" When identifying failure modes, use named patterns from `why/NAMED_PATTERNS.md` — for example, write 'Saga compensation failure' not just 'distributed transaction failure.' Named patterns make risks concrete and testable.

Systematically analyze these categories:

**Bugs & Logic Errors**
- Off-by-one errors, null/undefined handling, race conditions
- Boundary conditions (empty input, max values, negative numbers)
- State machine transitions (invalid states, missing transitions)
- Concurrent access issues (if applicable)

**Edge Cases**
- What happens at the boundaries of each vertical slice?
- Empty collections, missing data, malformed input
- Unicode / internationalization issues
- Time zone and date handling
- Large datasets / pagination

**Failure Modes**
- Network failures, timeouts, connection drops
- Database failures, constraint violations, deadlocks
- External service unavailability, rate limiting
- File system errors (permissions, disk space)
- Authentication / authorization failures

**Integration Risks**
- API contract changes between components
- Schema migration conflicts
- Dependency version conflicts
- Breaking changes in libraries

**Security Concerns**
- Input validation gaps
- Authentication bypass scenarios
- Data exposure / leakage
- Injection vulnerabilities (SQL, XSS, command)

**Performance Risks**
- N+1 query patterns
- Memory leaks
- Unbounded growth (logs, caches, queues)
- Missing indexes for common queries

### 4.2 Document Findings

Write to `.dev-flow/plans/premortem.md`:

```markdown
# Pre-Mortem Analysis — {feature name}

## Bugs & Logic Errors
| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|

## Edge Cases
| # | Edge Case | Affected Slice | Mitigation |
|---|-----------|---------------|------------|

## Failure Modes
| # | Failure Mode | Recovery Strategy | Test Plan |
|---|-------------|-------------------|-----------|

## Integration Risks
| # | Risk | Named Pattern | Component | Mitigation |
|---|------|-------------|-----------|------------|

## Security Concerns
| # | Concern | Severity | Mitigation |
|---|---------|----------|------------|

## Performance Risks
| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
```

### 4.3 Plan-Fix-Verify Loop

This is a **loop** — iterate until all identified risks have mitigations:

**Iteration:**

1. **Review** the pre-mortem document
2. **Identify** any risks without adequate mitigations
3. For each unmitigated risk:
   - Design a specific mitigation strategy
   - Identify which implementation slice should address it
   - Define a test that verifies the mitigation works
4. **Update** the pre-mortem document with new mitigations
5. **Verify** the mitigation is testable and assigned to a slice
6. **Check**: Are ALL risks now mitigated?
   - Yes → exit loop
   - No → repeat from step 1

Max 5 iterations. If risks remain after 5 iterations, flag them to the user at checkpoint.

### 4.4 Create Risk Mitigation Plan

Extract mitigations into `.dev-flow/plans/risk-mitigations.md` organized by vertical slice:

```markdown
# Risk Mitigations by Slice

## Slice 1: {name}
- Risk: {risk} → Mitigation: {strategy} → Test: {test description}

## Slice 2: {name}
- Risk: {risk} → Mitigation: {strategy} → Test: {test description}
```

This document feeds directly into Phase 5 (Planning).

### 4.5 Update State and Journal

- Update `state.json` with artifact paths
- Record risk-related decisions in the decision journal
- Record any risks that were accepted (not mitigated) with explicit acceptance rationale

## Quality Gate

Before checkpoint, verify:

- [ ] All 6 risk categories have been analyzed
- [ ] Each risk has a likelihood and impact assessment
- [ ] Each risk has a mitigation strategy
- [ ] Mitigations are assigned to specific vertical slices
- [ ] Each mitigation has a testable verification criterion
- [ ] The plan-fix-verify loop has been executed (at least once)
- [ ] Accepted risks (if any) are explicitly documented with rationale
- [ ] State and decision journal are updated

### Engram Save

Before presenting the checkpoint:

1. Call `mem_save` with:
   - key: `{engramProjectKey}-phase4`
   - content: phase summary — key findings, decisions made, artifacts produced
2. Update `state.json` with completed phase and artifact paths

### Documentation Update Check

Ask: "Does anything need updating in project docs (C4 diagrams, decision journal, architecture docs, README)?"
If yes — update before presenting checkpoint.

## Checkpoint

Present to the user:

1. **Risk summary**: Total risks identified, mitigated, and accepted
2. **Top 3 highest-impact risks** and their mitigations
3. **Any accepted risks** that were not mitigated (with rationale)
4. **Plan-fix-verify loop iterations** completed
5. Options: [Continue to Planning] [Pause] [End]
