# Anti-Pattern Catalog

## What Are Anti-Patterns?

Anti-patterns are common solutions to recurring problems that appear correct on the surface but ultimately prove counterproductive. Unlike simple mistakes, anti-patterns are seductive because they feel right — they follow intuitive reasoning, use familiar patterns, and often emerge gradually from good intentions.

For autonomous agents working in autonomous-workflow contexts, anti-patterns present a particular hazard: the agent may recognize a pattern, apply it with confidence, and produce code that compiles, passes basic checks, and appears to solve the problem — while subtly degrading system quality in ways that compound over time.

## Why Anti-Patterns Matter for Autonomous Agents

1. **Agents lack institutional memory** — they cannot recall that "we tried this approach in Q3 and it caused X problem"
2. **Agents optimize for immediate completion** — anti-patterns often provide short-term velocity at long-term cost
3. **Agents may not have full context** — architectural constraints, domain invariants, and team conventions may not be visible in the task spec
4. **Agents can normalize bad patterns** — repeated use of an anti-pattern can make it feel like "the way we do things"

## Entry Format

Each anti-pattern entry uses this structure:

| Field | Purpose |
|-------|---------|
| **What it is** | Concrete description of the pattern |
| **Why it looks right** | The plausible reasoning that makes this anti-pattern attractive |
| **The actual problem** | What goes wrong when this pattern is applied |
| **Likelihood in autonomous context** | How frequently this appears (High / Medium / Low) |
| **How to detect it** | Observable symptoms and detection strategies |
| **The fix** | One-sentence correction |

## Category Mapping

| Category | File | Focus |
|----------|------|-------|
| Domain Modeling | `domain.md` | Entity design, aggregates, type relationships |
| Architecture | `architecture.md` | Module structure, dependencies, abstractions |
| Testing | `testing.md` | Test quality, mocking practices, test isolation |
| Autonomous Workflow | `autonomous-workflow.md` | Agent-specific failure modes in dev-flow execution |

## Usage Guide

### Before a Phase
Review the relevant category file to internalize what to avoid. For example, before starting **Phase 2 (Spec)**, review `domain.md` to ensure entity design decisions won't create problems later.

### During a Phase
If something feels wrong but you can't articulate why, check the relevant anti-pattern. The "Why it looks right" / "The actual problem" framing often clarifies intuition.

### After Quality Review
When a quality gate fails, cross-reference the failure type against anti-patterns. A test ordering issue points to `testing.md`; a circular dependency error points to `architecture.md`.

### In Phase 4 (Implementation)
Before committing code, do a quick anti-pattern scan:
- Does your entity have behavior, or is it just interfaces?
- Are your modules loosely coupled enough to test in isolation?
- Do your tests assert meaningful outcomes, or just "pass"?

## Active Rejection Checklist

Use this checklist during quality gates and self-critique passes. Each item is a hard rejection — if code matches, it does not pass.

### Testing Rejections

| # | Anti-Pattern | Rejection | Why |
|---|-------------|-----------|-----|
| 1 | vitest | Use `bun test` | Dual-runner complexity — Bun's test runner handles all test types |
| 2 | MSW for domain-level mocking | Use fake adapters | Fake adapters are permanent fixtures; MSW only for external HTTP APIs with no port |
| 3 | @vue/test-utils | Use E2E (Playwright) | Incompatible with Bun runtime (WeakMap internals) |
| 4 | Tests without assertions | Every test must have assertions that can fail | No-assertion tests create an illusion of safety |

### Architecture Rejections

| # | Anti-Pattern | Rejection | Why |
|---|-------------|-----------|-----|
| 5 | Business logic in pages/components | Move to composables/domain layer | Pages are for orchestration, not logic |
| 6 | Direct deep-path imports | Use `@x/` aliases through `index.ts` | Deep paths couple to internal structure |
| 7 | Direct adapter imports from UI | Use composables | Pages never import adapters — DI composition root handles wiring |
| 8 | Raw external calls outside adapters | All external deps through adapter layer | Violates ports & adapters boundary |
| 9 | Cross-domain imports without `@x/` | Use alias, never deep paths | Cross-domain access through public API only |

### How to Use This Checklist

- **During self-critique (Phase 6, step 6):** Run through each item against the changed files
- **During quality gates:** If any row matches → block progression, send back for fix
- **During code review:** Flag violations as critical issues

## Quick Reference

| Anti-Pattern | Severity | Detection |
|--------------|----------|-----------|
| Anemic Domain Model | High | Entity files are only TypeScript interfaces |
| God Aggregate | High | Entity > 200 lines; references 10+ domain types |
| Deep Hierarchy | Medium | 5+ levels of nested types |
| Circular Dependencies | High | `tsc --noEmit` shows circular errors |
| Tight Coupling | High | Refactoring one file requires immediate refactoring of another |
| Premature Abstraction | Low | Interface has one implementing class |
| Architecture Tourists | Medium | C4/ADR never referenced; workspace.dsl stale |
| Test-Only Pass | High | Tests assert nothing meaningful |
| Over-Mocking | Medium-High | More mock setup than test logic |
| Phantom Completion | Medium-High | Task marked DONE but no git commit |
| YOLO Without Flagging | High | YOLO active but yoloFlaggedDecisions empty |

---

For detailed entries, see individual category files.
