# Dev Flow

> [!TIP]
> A rigorous multi-session development workflow for Claude Code. Structures work across 8 sequential phases with built-in quality gates, TDD discipline, systematic verification, and an opinionated preference system.

Dev Flow keeps you in control across multiple sessions — remembers where you left off, forces you to verify before claiming done, and separates the thinking (design) from the doing (implementation).

## The 8 Phases

| # | Phase | Purpose |
|---|-------|---------|
| 1 | Discovery | Understand requirements, explore approaches, converge on solution |
| 2 | Exploration | Understand existing architecture, patterns, and conventions |
| 3 | Design | Create C4 docs, folder structure, walking skeleton |
| 4 | Pre-Mortem | Identify failure modes and risks before implementation |
| 5 | Planning | Break work into bite-sized TDD tasks |
| 5b | Pre-Implementation Gate | HARD-GATE — plan must exist before coding starts |
| 6 | Implementation | Execute plan with sequential subagents, TDD, quality review |
| 6b | Extras | Post-completion polish and supplementary work |
| 7 | Gap Analysis | Identify and fill testing and documentation gaps |
| 8 | Completion | Final verification and integration options |

## Installation

```bash
/plugin install https://github.com/thanksmors/dev-flow
```

## Quick Start

```bash
# Start a new workflow
/dev-flow

# Resume from last checkpoint
/dev-flow continue
```

## Preference System

Dev Flow uses a **multi-set preference system** — you choose a named preference set at Phase 0, which configures tech stack, testing philosophy, architecture patterns, and communication style for the session.

### Preference Sets

| Set | Description |
|-----|-------------|
| `default` | Bun + Nuxt + Insforge + Nuxt UI — full vertical slices + ports-and-adapters |
| `minimal` | Bun + Nuxt (no backend, no UI library) — single-app until boundaries emerge |
| `full-stack` | Bun + Nuxt + Fastify + Nuxt UI — for CPU-intensive backend work |

Preference sets live in the plugin at `.claude-plugin/preferences/sets/`. Each set contains 6 files:

```
sets/{name}/
  tech-stack.md           # Runtime, backend, frontend, UI components, architecture
  programming-style.md    # Architecture principles, auth pattern, error handling
  testing.md             # Test types, tools, coverage thresholds
  libraries-and-mcps.md  # Approved dependencies and MCPs
  setup-steps.md         # One-time project scaffolding sequence
  user-profile.md        # Communication style, YOLO default
```

### How Phase 0 Works

1. **Discover** — scans `.claude-plugin/preferences/sets/` for available sets
2. **AskUserQuestion** — "Choose a preference set:" with one-line descriptions
3. **Load** — copies the chosen set's 6 files into `.dev-flow/preferences/` in the project

See `docs/superpowers/specs/2026-04-02-multi-preference-sets-design.md` for the full design.

## Core Principles

1. **Iron Law** — No completion claims without fresh verification evidence
2. **Fake Adapters First** — External dependencies get in-memory fakes before real adapters
3. **Agents Are First-Class** — Same interfaces for agents and humans
4. **Swappability Is the Goal** — Design boundaries for replacement
5. **TDD Discipline** — Red before green, always
6. **Strict Phase Gates** — No skipping, no shortcuts

## HARD-GATE System

Automated Python gate scripts run at key phase transitions. Gates are **tech-agnostic** — they check universal concerns only.

| Gate | When | Checks |
|------|------|--------|
| `gate_phase0.py` | Before Phase 1 | `gh` auth, git remote configured, plugin root valid |
| `gate_phase5b.py` | Before Phase 6 | Implementation plan exists, no open fake/pending deferred decisions |
| `gate_phase6_start.py` | Before each implementation task | Plan exists, all `process.env` vars configured, no pending fake adapters |
| `gate_phase6_end.py` | After Phase 6 | All deferred decisions resolved, swapped, or skipped |

**Fix loop:** If a gate fails, autonomous fixer agents attempt up to 2 rounds of fixes. Only escalates to user if both rounds fail.

## Implementation Workflow

Phase 6 dispatches **one subagent per task** with:
1. Fresh context (full task text + scene-setting)
2. TDD enforcement (red → green → refactor)
3. Spec compliance review (did you build what was specified?)
4. Code quality review (correctness, style, performance, security)
5. Per-task verification (test output logged, not assumed)

See `.claude-plugin/phases/06-implementation.md` for the full workflow.

## Frontend Design Commands

Available throughout the workflow to keep UI outputs from looking AI-generated:

| Command | Purpose |
|---------|---------|
| `/frontend-audit` | Scan for AI slop patterns |
| `/frontend-critique` | Deep design review across 10 dimensions |
| `/frontend-normalize` | Realign spacing, typography, color to design tokens |
| `/frontend-polish` | Final quality pass — micro-details, interaction states |
| `/frontend-distill` | Simplify UI and copy |
| `/frontend-animate` | Add purposeful motion with exponential easing |

## Key Features

- **Multi-set preference system** — choose your stack config at Phase 0
- **State persistence** — PreCompact saves session state; SessionStart restores after compaction
- **HARD-GATE enforcement** — gates block progress until verified
- **Autonomous fix loop** — gate failures trigger fixer agents before escalating
- **YOLO mode** — auto-select decisions for faster execution
- **Decision journal** — significant decisions recorded with rationale
- **ADR support** — formal architecture decision records in `docs/decisions/`

## Configuration

Project-level preferences at `.dev-flow/preferences/`:

- `user-profile.md` — Developer type, explanation depth, YOLO default
- `tech-stack.md` — Runtime, backend, frontend preferences
- `testing.md` — Test approach and coverage standards
- `programming-style.md` — Code conventions and patterns
- `setup-steps.md` — Project scaffolding defaults
- `libraries-and-mcps.md` — Approved dependencies and MCPs

These are copied from the chosen preference set at Phase 0. Modify them to override the set defaults for this project.

## Phase Files

| File | Purpose |
|------|---------|
| `.claude-plugin/phases/02-exploration.md` | Parallel code explorer agents |
| `.claude-plugin/phases/03-design.md` | C4 diagrams, architecture decisions |
| `.claude-plugin/phases/05b-preimplementation-gate.md` | Pre-implementation gate + fix loop |
| `.claude-plugin/phases/06-implementation.md` | Full implementation workflow |
| `.claude-plugin/phases/06-extras.md` | Post-completion supplementary work |
| `.claude-plugin/commands/dev-flow.md` | The main orchestrating command |
