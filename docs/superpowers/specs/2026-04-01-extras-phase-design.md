# Extras Phase — Design

## Context

Phase 6 implementation is complete and verified. Phase 7 gap analysis audits the existing system for coverage. Neither phase is designed to surface *new* ideas or quality-of-life improvements that weren't part of the original plan.

The Extras phase exists to prove the tech stack is extensible — by generating suggestions for improvements, letting the user pick which ones to pursue, and implementing them within the same workflow before the final system audit.

## Trigger

Runs after Phase 6 implementation is verified (Phase 6 Quality Gate passed).

## Flow

```
Phase 6 (done) → Extras → AI proposes 6 suggestions → User selects → Implement → Phase 7 audit → Phase 8
```

## Phase Steps

### Extras 1: Generate Suggestions

The orchestrator reads the full project context (current codebase, Phase 6 artifacts, existing docs) and generates **6 suggested improvements** across three categories:

- **Features** — new capabilities
- **Quality-of-life** — DX improvements (tooling, docs, scripts)
- **Technical** — performance, refactoring, robustness

Each suggestion includes:
```
{index}. {Name}
   Category: {Feature | QoL | Technical}
   Description: {2-3 sentence description of what this adds}
   Effort: {Low | Medium | High}
   Complexity: {Low | Medium | High}
```

The orchestrator may invent suggestions from scratch. Suggestions should be specific to the project — not generic.

### Extras 2: Present to User

Present all 6 suggestions. Ask:

> **Select improvements to implement.** Enter numbers separated by commas (e.g. 1, 3, 5), or leave blank to skip.

No minimum. No maximum. Empty input = skip Extras entirely and proceed to Phase 7.

### Extras 3: Implement Selected

For each selected suggestion:
1. Write the minimal spec for this improvement
2. Implement it (using the same TDD approach as Phase 6)
3. Verify it works

### Extras 4: Update Backlog

After user selection, append unselected suggestions to `.dev-flow/extras-backlog.md`:

```markdown
## YYYY-MM-DD — {project name}

- [{number}] {Name} — {category} — {effort} effort, {complexity} complexity
  {Description}
```

If `extras-backlog.md` does not exist, create it.

### Extras 5: Phase 6 Verification

After all selected improvements are implemented, re-run Phase 6 verification:
- Run full test suite — must pass
- Verify docs are updated for all changes
- Verify workspace.dsl is updated if architecture changed

Do NOT proceed until Phase 6 verification passes.

## Gate

No independent gate. The Extras phase passes when Phase 6 verification passes (after improvements are implemented).

## Phase 7 After Extras

Phase 7 runs normally after Extras completes. The gap analysis should cover both the original implementation AND the new improvements from Extras.

## Files

| File | Role |
|------|------|
| `.dev-flow/extras-backlog.md` | Backlog of unselected improvements, accumulated across projects |
| `docs/superpowers/specs/YYYY-MM-DD-extras-{n}.md` | One spec per selected improvement |

## Retirement / Evolution

If Extras consistently produces no selections across multiple projects, consider making it opt-in (skippable) rather than required. Track selection rate in PATTERNS.md.
