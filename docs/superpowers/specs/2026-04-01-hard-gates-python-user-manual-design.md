# Design: Hard Gates as Python, Preference Loading Fix, User Manual Artifact

Date: 2026-04-01
Status: Draft

## Context

Three related workflow improvements identified during brainstorming:

1. **Hard gates are prose-enforced** — current HARD-GATEs live in markdown phase files. The agent reads them and self-enforces. This works but is non-deterministic — compliance depends on the agent reading precisely. Gates that check concrete conditions (does this file exist?, does this test pass?, is this env var set?) can be codified as Python scripts with deterministic pass/fail output.

2. **Preference loading warned about missing files** — a previous session showed a warning that preference files or defaults were not found. The `${CLAUDE_PLUGIN_ROOT}` env var may not always resolve correctly in all invocation contexts. The loading logic needs to be path-resilient with better diagnostics.

3. **No user-facing verification artifact** — the design spec is developer-facing (architecture, ports, components). There is no user-facing document that describes what the app should do from a user's perspective. A user manual written before implementation serves as a cross-referenceable verification artifact during Phase 6.

---

## Decision 1: Hard Gates as Python Validators

### Problem

Current HARD-GATEs are markdown prose blocks like:

```
<HARD-GATE — Fake Adapters First>
Before any task involving an external dependency begins:
✅ A fake adapter interface MUST be defined first...
```

The agent reads this and self-enforces. It works when the agent is diligent but relies on interpretation. Gates with binary conditions (file exists / doesn't exist, test passes / fails, env var set / not set) should not depend on interpretation.

### Solution

Codify the most concrete gates as Python scripts. Each gate is a standalone CLI tool that:
- Reads relevant artifacts (state.json, plan files, .env, deferred-decisions tracker)
- Checks deterministic conditions
- Exits `0` for pass, `1` for fail
- Prints a human-readable report of what was checked and the result

The agent invokes the gate script as a subprocess before entering the gated phase. If it exits `1`, the workflow pauses and prints the gate's output.

### Gate Scripts to Implement

#### Gate 1: `gate_phase0.py` — Prerequisites Check

**When:** Before Phase 0 completes (git auth, gh auth).

**Checks:**
- `gh auth status` passes (run as subprocess, capture exit code)
- `git remote -v` returns a remote URL
- `${CLAUDE_PLUGIN_ROOT}` resolves to a readable directory

**Exit codes:** `0` = pass, `1` = fail

#### Gate 2: `gate_phase5b.py` — Pre-Implementation Gate

**When:** Before Phase 6 begins (Phase 5b / pre-implementation gate).

**Checks (all must pass):**
- `docs/superpowers/plans/implementation.md` exists
- All port interfaces defined in `layers/*/ports/` (at least one port file exists if the plan has external dependencies)
- All fake adapters referenced in the plan exist at `layers/*/adapters/Fake*.ts`
- No `fake` adapters in the deferred-decisions tracker are marked `pending` (they should be `fake` or `swapped`)

**Exit codes:** `0` = pass, `1` = fail

#### Gate 3: `gate_phase6_start.py` — Pre-Flight Check

**When:** Step 6.0, before any Phase 6 task dispatches.

**Checks:**
- Read `docs/superpowers/plans/implementation.md`
- Grep for `process.env` references in all task descriptions
- Check each referenced env var against `.env` and `.env.example`
- Check deferred-decisions tracker for `Status = fake` — any fake adapters that are still wired need swap before Phase 6
- Check for any third-party service URLs referenced but not configured

**Output on fail:**
```
⚠️ Pre-flight failed — missing dependencies:

Env vars referenced but not configured:
  STRIPE_SECRET_KEY  — used in PaymentAdapter (task N)
  DATABASE_URL       — used in UserRepository (task N)

Third-party services not yet configured:
  SendGrid — EmailAdapter fake still wired (swap before Phase 6 begins)

Run `/dev-flow continue` once ready.
```

**Exit codes:** `0` = pass, `1` = fail

#### Gate 4: `gate_phase6_end.py` — Deferred-Decision Gate

**When:** Section 6.4, after all Phase 6 tasks complete, before Phase 7 checkpoint.

**Checks:**
- Read `.dev-flow/architecture/deferred-decisions.md`
- If any items have `Status = fake` or `Status = pending` → exit 1
- Report each open item so the user can resolve one-by-one

**Output on fail:**
```
⚠️ Deferred-decision gate failed — {N} open items:

1. EmailAdapter — Status: fake — Deferred to: Phase 6
2. PaymentGateway — Status: pending — Deferred to: Phase 7

Handle all open items before proceeding to Phase 7.
```

**Exit codes:** `0` = all items resolved, `1` = open items remain

### Implementation Notes

- All gate scripts live at `.claude-plugin/gates/`
- Each script is a single `.py` file with no external dependencies beyond the stdlib
- Scripts receive artifacts as arguments or read from well-known paths relative to the project root
- Output is plain text suitable for display in a terminal or Claude Code message
- The agent treats the gate as a blocking subprocess — if it exits 1, the workflow pauses

### Not All Gates Are Codable

Some gates require judgment:
- "Is the implementation spec-compliant?" → requires a human or LLM reviewer to compare spec vs. code
- "Are there unknown unknowns?" → inherently qualitative
- "Is the design intent honored?" → requires architectural judgment

Only gates with binary pass/fail conditions are codified. The remaining gates stay as prose HARD-GATE blocks that the agent enforces.

---

## Decision 2: Preference Loading Path Resilience

### Problem

`dev-flow.md` Step 0.1 loads project preferences from `.dev-flow/preferences/` or falls back to `${CLAUDE_PLUGIN_ROOT}/preferences/defaults/`. If `${CLAUDE_PLUGIN_ROOT}` is not set or resolves incorrectly, the fallback silently fails and the agent proceeds without preferences.

### Solution

Three changes to the preference loading logic in `dev-flow.md`:

#### Change 1: Resolve plugin root explicitly

At command load time, resolve the plugin root using a known file as an anchor:

```python
import os, pathlib

# Find plugin root by locating a known file
PLUGIN_ROOT = pathlib.Path(__file__).parent.resolve()
# Or if called as a subprocess, use the caller's location
```

Since this is inside a Claude Code command (markdown with frontmatter, not Python), the equivalent is handled by the agent reading the command — but the principle is: resolve `${CLAUDE_PLUGIN_ROOT}` once at load time, not per-step.

#### Change 2: Verify all expected files exist after loading

After loading defaults, assert all 6 files are present:

```
preferences/defaults/tech-stack.md
preferences/defaults/programming-style.md
preferences/defaults/testing.md
preferences/defaults/libraries-and-mcps.md
preferences/defaults/setup-steps.md
preferences/defaults/user-profile.md
```

If any are missing after loading, print:
```
Preference loading warning: expected 6 default files but found {N} at {path}.
Missing: {list of filenames}.
```

Do not silently continue — warn so the issue is self-explanatory.

#### Change 3: Diagnose before defaulting

If neither project preferences nor defaults are found, do not silently use in-memory defaults. Print the diagnostic:

```
No preferences found at:
  Project: {project}/.dev-flow/preferences/
  Plugin:  {plugin_root}/preferences/defaults/

Check that the plugin is correctly installed. Proceeding with built-in defaults.
```

### Implementation Location

`dev-flow.md` Step 0.1 — update the preference loading logic with the three changes above.

---

## Decision 3: User Manual as Pre-Implementation Artifact

### Problem

The design spec (`docs/superpowers/specs/YYYY-MM-DD-<project>-design.md`) is developer-facing — it describes architecture, components, ports, and interfaces. It does not describe what the user actually does with the app. There is no user-facing artifact that can be used to verify implementation against real user expectations.

### Solution

A **user manual** is written alongside the design spec, in Phase 2 or early Phase 3, once the UI/UX is understood from discovery. It is written in plain English from the user's perspective — no code, no architecture, no component names.

### Location and Naming

```
docs/superpowers/specs/
├── YYYY-MM-DD-<project>-design.md       # Developer-facing spec
└── YYYY-MM-DD-<project>-user-manual.md  # User-facing manual
```

Both files share the same date and project name. They are cross-referenced but serve distinct purposes.

### Content Structure (User Manual)

```markdown
# {Project Name} — User Manual

## Overview
One paragraph: what the app does, who uses it, the core value.

## First-Time Setup
Step-by-step: what the user does the first time they open the app.

## Core User Flows

### Flow 1: {Descriptive Name}
1. User navigates to...
2. User enters...
3. User clicks...
4. App responds with...

### Flow 2: {Name}
...

## Input Reference
All user inputs: what each field means, format expected, validation rules.

## Output Reference
What the user sees after each action: success case, error case, empty state.

## Error States
What goes wrong and what the user sees. How to recover.

## FAQ / Edge Cases
Common questions or surprising behaviors.
```

### Cross-Reference Mechanism

In the design spec, acceptance criteria reference the user manual:

```markdown
## Acceptance Criteria

- [ ] **AC-1**: User can create a project → see User Manual Section 2.1
- [ ] **AC-2**: User receives email confirmation → see User Manual Section 3.2
```

During Phase 6 implementation, each acceptance criterion can be traced back to a user flow. During verification, the implemented behavior is checked against the manual's description.

### When It Is Written

Phase 2 (Exploration) or early Phase 3 (Design) — once the UI/UX is understood well enough to describe user flows. It does not require implementation details.

It is updated if the UX changes during implementation (documented as an ADR decision).

### Verification Use

During Phase 6.6 (Design Compliance Review) and Phase 7 (Gap Analysis), the user manual is part of the verification checklist:

```
- [ ] Each acceptance criterion maps to a user manual flow
- [ ] Each user manual flow has a corresponding implemented feature
- [ ] No user manual flow is unimplemented
- [ ] No implemented feature is missing from the user manual
```

---

## Summary of Changes

| # | Component | Change | File |
|---|-----------|--------|------|
| 1 | Gate scripts | Add `gate_phase0.py`, `gate_phase5b.py`, `gate_phase6_start.py`, `gate_phase6_end.py` | `.claude-plugin/gates/` |
| 2 | Phase 6 implementation | Replace prose Step 6.0 with subprocess call to `gate_phase6_start.py` | `phases/06-implementation.md` |
| 3 | Phase 6 deferred-decision | Replace prose Section 6.4 with subprocess call to `gate_phase6_end.py` | `phases/06-implementation.md` |
| 4 | Preference loading | Add path resilience + diagnostics to Step 0.1 | `commands/dev-flow.md` |
| 5 | Phase 3 design | Add user manual artifact to Phase 3 output checklist | `phases/03-design.md` |
| 6 | Design spec template | Add acceptance criteria cross-reference to user manual | `templates/completion-report.md` |

---

## Out of Scope

- Any gate requiring judgment (spec compliance, design intent) — stays as prose HARD-GATE
- Automated test execution — handled by existing `verification-before-completion` skill
- CI integration for gates — can be added later as a follow-up
