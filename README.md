# Dev Flow

> [!TIP]
> Dev Flow is a rigorous multi-session development workflow for Claude Code. It structures work across 8 sequential phases with built-in quality gates, TDD discipline, and systematic verification.

Dev Flow keeps you in control across multiple sessions — it remembers where you left off, forces you to verify before you claim done, and separates the thinking (design) from the doing (implementation).

## The 8 Phases

| # | Phase | Purpose |
|---|-------|---------|
| 1 | Discovery & Brainstorming | Understand requirements, explore approaches, select solution |
| 2 | Codebase Exploration | Understand existing architecture, patterns, and conventions |
| 3 | Design & Architecture | Create C4 docs, folder structure, walking skeleton |
| 4 | Pre-Mortem | Identify failure modes and risks before implementation |
| 5 | Planning | Break work into bite-sized TDD tasks |
| 5b | Pre-Implementation Gate | HARD-GATE verification before coding |
| 6 | Implementation | Execute plan with sequential subagents, TDD, quality review |
| 7 | Gap Analysis | Identify and fill testing/documentation gaps |
| 8 | Completion Report | Final verification and integration options |

*(9 entries above — Phase 5b is a HARD-GATE sub-phase between Planning and Implementation)*

## Quick Start

```bash
# Install from GitHub
/plugin marketplace add https://raw.githubusercontent.com/thanksmors/dev-flow/main/.claude-plugin/marketplace.json
/plugin install dev-flow

# Start a new workflow
/dev-flow

# Resume from checkpoint
/dev-flow continue
```

## Core Principles

1. **Iron Law** — No completion claims without fresh verification evidence
2. **Fake Adapters First** — External dependencies get fakes before real implementation
3. **Agents Are First-Class** — Same APIs for agents and humans
4. **Swappability Is the Goal** — Design boundaries for replacement
5. **TDD Discipline** — Red before green, always
6. **Strict Phase Gates** — No skipping, no shortcuts

## Frontend Design Commands

Build interfaces that don't look AI-generated. These commands are available throughout the workflow:

| Command | Purpose |
|---------|---------|
| `/frontend-audit` | Scan for AI slop patterns |
| `/frontend-critique` | Deep design review across 10 dimensions |
| `/frontend-normalize` | Realign spacing, typography, color to design tokens |
| `/frontend-polish` | Final quality pass — micro-details, interaction states |
| `/frontend-distill` | Simplify UI and copy |
| `/frontend-animate` | Add purposeful motion with exponential easing |

See `skills/frontend-design/` for the full design reference (powered by [Impeccable](https://github.com/pbakaus/impeccable), Apache 2.0).

## Key Features

- **State persistence** — Resumes exactly where you left off
- **Preference system** — Tech stack, testing, and style defaults
- **HARD-GATE enforcement** — Phase 5b, 7, and 8 block progress until verified
- **YOLO mode** — Auto-select decisions for faster execution
- **Decision journal** — All significant decisions recorded with rationale
- **ADR support** — Formal architecture decision records

## Configuration

Dev Flow uses a preference system at `.dev-flow/preferences/` in your project:

- `user-profile.md` — Developer type, explanation depth, YOLO default
- `tech-stack.md` — Runtime, backend, frontend preferences
- `testing.md` — Test approach and coverage standards
- `programming-style.md` — Code conventions and patterns
- `setup-steps.md` — Project scaffolding defaults

See `PRINCIPLES.md` for the full methodology.

## Extending

- `PRINCIPLES.md` — The six non-negotiable principles
- `EXAMPLES.md` — Canonical patterns to replicate
- `references/tdd-ai-first.md` — TDD methodology
- `references/complexity-ladder.md` — Scope classification
- `skills/frontend-design/` — Frontend design guidance
