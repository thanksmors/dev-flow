# dev-flow Plugin Enhancement — v2.0.1 to v2.1.0

Date: 2026-04-01
Status: Accepted

## Context

The dev-flow plugin v2.0.1 was tested during a todo app build. The 8-phase workflow completed successfully but revealed 25 targeted enhancements across 4 priority tiers. These range from silent HARD-GATE failures (Python gates crashed on Windows without error messages) to missing quality enforcement (spec reviews skipped, lessons not surfacing to agents). This design documents all 25 enhancements to produce v2.1.0.

The plugin lives at `dev-flow/.claude-plugin/`. Enhancement changes live inside this directory. The design doc lives at `dev-flow/docs/plugin-enhancement-design.md`.

## Canonical Artifact Paths

All phases, gates, and agents use these paths (CR-2 enforces alignment):

| Artifact | Path |
|---|---|
| Implementation plan | `.dev-flow/plans/implementation.md` |
| Pre-mortem | `.dev-flow/plans/premortem.md` |
| Design approach | `.dev-flow/design/approach.md` |
| Architecture diagrams | `.dev-flow/architecture/c4/` |
| Sequences | `.dev-flow/architecture/sequences/` |
| States | `.dev-flow/architecture/states/` |
| Gap analysis | `.dev-flow/reports/gap-analysis.md` |
| Completion report | `.dev-flow/reports/completion.md` |
| Decisions (ADR) | `docs/decisions/` |
| Structurizr workspace | `docs/workspace.dsl` |
| Plugin-level lessons | `dev-flow-plugin/lessons/` |

---

## Tier 1 — CRITICAL

Issues that silently blocked or corrupted the workflow during the todo app build.

### CR-1 — Python Gates Cross-Platform

**Problem:** `python3` resolves to a Windows Store shortcut stub on many Windows machines (not an actual Python installation). The full Python at `C:/Program Files/Python312/python` exists but is not on the PATH. Additionally, gate scripts print emoji (`✅ ❌ ⏭️`) which crashes on cp1252 Windows consoles with `UnicodeEncodeError`.

**Fix:**

1. Change `#!/usr/bin/env python3` → `#!/usr/bin/env python` in all gate scripts
2. Add `PYTHONIOENCODING=utf-8` to all gate invocation lines in phase files
3. Replace emoji symbols with ASCII equivalents:
   - `✅` → `[PASS]`
   - `❌` → `[FAIL]`
   - `⏭️` → `[SKIP]`

**Files affected:**
- `gates/gate_phase0.py`
- `gates/gate_phase5b.py`
- `gates/gate_phase6_start.py`
- `gates/gate_phase6_end.py`
- `gates/_json_output.py`
- `phases/05b-preimplementation-gate.md` (update invocation examples)
- `phases/06-implementation.md` (update invocation examples)

**Verification:** All gates run without `UnicodeEncodeError` on Windows cp1252 console.

---

### CR-2 — Artifact Path Mismatch

**Problem:** Phase 3 saves implementation artifacts to `.dev-flow/plans/`, `.dev-flow/design/`, and `.dev-flow/architecture/`. But gates, agents, and phase files reference `docs/superpowers/plans/` and `docs/superpowers/specs/`. The mismatch caused Phase 5b to always fail "plan not found" (silently, due to CR-1 crash).

**Fix:** Align all references across the plugin:

1. `gate_phase5b.py`: change `PLANS_DIR = PROJECT_ROOT / "docs/superpowers/plans"` → `PROJECT_ROOT / ".dev-flow/plans"`
2. `gate_phase6_start.py`: change `PLANS_DIR` path similarly
3. `phases/05b-preimplementation-gate.md`: update all path examples
4. `phases/06-implementation.md`: update plan path references
5. `agents/spec-reviewer.md`: update design spec path to `.dev-flow/design/`
6. `phases/03-design.md`: ensure it saves to `.dev-flow/` paths (already correct, verify)
7. Any other reference to `docs/superpowers/` → `.dev-flow/`

**Files affected:**
- `gates/gate_phase5b.py`
- `gates/gate_phase6_start.py`
- `phases/05b-preimplementation-gate.md`
- `phases/06-implementation.md`
- `agents/spec-reviewer.md`

---

### CR-3 — Phase 6 Evidence Gate Missing

**Problem:** Phase 6 has a 23-item quality gate checklist but no enforcement. Agents skipped reviews, files were never verified, and the workflow proceeded anyway. The existing `gate_phase6_end.py` only checks deferred decisions — it does not verify that implementation evidence exists.

**Fix — Two-Gate Approach:**

**Gate A — `gate_phase6_end.py` (existing):** Stays as-is. Checks deferred decisions are resolved. HARD-GATE on Phase 7 checkpoint.

**Gate B — `gate_phase6_evidence.py` (new):** Checks mechanical implementation evidence:

| Check | What it verifies |
|---|---|
| `test_files` | At least one test file exists matching `**/*.test.ts` or `**/*.spec.ts` |
| `e2e_test_count` | Actual E2E test count matches plan's promised count (HI-4) |
| `adr_files` | At least one ADR file exists in `docs/decisions/` |
| `workspace_dsl` | `docs/workspace.dsl` exists and is non-empty |
| `c4_mmd` | At least one Mermaid C4 file exists in `.dev-flow/architecture/c4/` |
| `slice_tracking` | All slices with `Status: complete` have `Wired: yes` (HI-3) |
| `test_suite_passes` | Fresh `bun test` run exits 0 |
| `no_skipped_tests` | No `test.skip = true` in test files |

Both gates must pass before Phase 7 checkpoint. Human-gated items (quality reviews passed, design intent honored) are tracked via self-attestation flags in `state.json` set by the orchestrator.

**Files affected:**
- `gates/gate_phase6_evidence.py` (new)
- `phases/06-implementation.md` (update to reference both gates)
- `phases/07-gap-analysis.md` (update HARD-GATE description to list both gates)

---

## Tier 2 — HIGH-PRIORITY

Quality enforcement improvements that prevent implementation drift.

### HI-1 — Spec & Quality Reviews Made Non-Optional

**Problem:** The per-task loop in Phase 6 lists spec review and quality review as steps, but nothing enforced them. Implementer agents skipped both entirely during the todo app build.

**Fix:** Convert steps 4 (spec compliance review) and 5 (quality review) in the per-task autonomous loop into HARD-GATE steps:

1. After implementer reports DONE, orchestrator dispatches spec-reviewer
2. If reviewer returns `NOT COMPLIANT` → implementer receives specific non-compliant items → fixes → re-verify → re-review
3. Loop until `COMPLIANT`
4. Then dispatch quality-reviewer
5. If reviewer returns `NEEDS WORK` on Critical issues → implementer fixes → re-verify → re-review
6. Loop until `APPROVED` (zero Critical)
7. Only then mark task complete and proceed

**Orchestrator enforces:** Neither review can be skipped, bypassed, or short-circuited. The loop continues until both pass.

**Files affected:**
- `phases/06-implementation.md`

---

### HI-2 — YOLO Decision Review in Phase 7

**Problem:** YOLO auto-selected decisions during Phase 6 are never revisited. The user never sees what was auto-selected or has a chance to confirm it.

**Fix:** At Phase 7 start (before gap analysis begins):

1. Orchestrator reads `state.json` for `yoloFlaggedDecisions[]`
2. If array is non-empty, presents each YOLO ADR:
   ```
   YOLO Decision — auto-selected during Phase 6:
   ADR-{NN}: {title}
   {one-line summary of what was decided}

   [Confirm this decision] [Revise it]
   ```
3. If user selects Revise → pauses to let user modify the ADR
4. Gate re-checks after revision
5. Only proceeds to gap analysis once all YOLO decisions are confirmed

**Files affected:**
- `phases/07-gap-analysis.md`
- `phases/06-implementation.md` (ensure ADR path is appended to `yoloFlaggedDecisions`)

---

### HI-3 — Slice Tracking Accuracy

**Problem:** "Slice 4 executed" was recorded in the plan, but the slice was scaffolded (files created) and never wired (integrated and verified end-to-end). False sense of completion.

**Fix:** Add two columns to the implementation plan task table:

| Column | Values | Meaning |
|---|---|---|
| `Status` | pending / scaffolded / complete | Whether the task has been done |
| `Wired` | yes / no | Whether the task's output is integrated and verified end-to-end |

- `scaffolded` = files exist, not yet integrated
- `complete` = integrated, tested, verified
- `Wired: yes` is required for `Status: complete`

`gate_phase6_evidence.py` (CR-3) checks that all slices with `Status: complete` have `Wired: yes`. If scaffolded ≠ wired, the gate fails with the specific slice name.

**Files affected:**
- `templates/implementation-plan.md` (add Wired column)
- `phases/06-implementation.md` (track wired status per task)
- `gates/gate_phase6_evidence.py` (add wired check)

---

### HI-4 — E2E Test Count Verification

**Problem:** No gate checks if the actual E2E test count matches what the implementation plan promised. Plans can claim N E2E tests but fewer exist.

**Fix:** `gate_phase6_evidence.py` (CR-3) reads the planned E2E test count from `.dev-flow/plans/implementation.md` (from the test strategy section), discovers actual E2E test files via glob, and compares. Fail if counts don't match with diff shown.

**Files affected:**
- `gates/gate_phase6_evidence.py`

---

## Tier 3 — ARCHITECTURE & DOCS

Framework-specific guidance and documentation improvements.

### AR-1 — Nuxt 4 Layers Guidance

**Problem:** No plugin-specific guidance for Nuxt 4 layers patterns. The todo app build created duplicate server routes in `layers/features/todo/server/` and `server/api/` — both never called because layer aliases don't resolve from project root.

**Fix:** New reference document at `references/nuxt4-layers.md`:

```markdown
# Nuxt 4 Layers — dev-flow Reference

## How Nuxt 4 Layers Work

Nuxt 4 layers are extended via `nuxt.config.ts` `extends` array. Each layer
contributes: auto-imports, layouts, pages, server routes, and composables.

## Critical Rules for dev-flow

### Server Routes — Where They Go
Server routes for a feature belong in `server/api/` at the PROJECT ROOT.
They do NOT go in `layers/features/{feature}/server/api/`.
Reason: Nuxt layer aliases (e.g. `#app/diComposition`, `~/shared/schemas`)
resolve from the project root, not from within a layer directory.
Files in `layers/features/*/server/` are NOT auto-registered.

### Composables — Where They Go
Composables used by the feature belong in `composables/` or `shared/composables/`
at the project root. They are NOT auto-imported from `layers/features/*/app/`.
If a composable lives inside a layer, it must be explicitly imported.

### DI Composition
- The composition root is at `app/diComposition.ts` at the project root.
- Layer aliases (`#app/diComposition`) are configured in `nuxt.config.ts`.
- Adapters are wired in `app/diComposition.ts` using `bind()`.
- Port interfaces live at `layers/{domain}/ports/XyzPort.ts`.

### Folder Structure (Canonical)
```
project/
├── app/
│   └── diComposition.ts       # DI composition root
├── layers/
│   └── {domain}/
│       ├── ports/             # Port interfaces
│       ├── adapters/          # Fake + real adapters
│       ├── domain/            # Domain logic
│       └── app/               # Composables (explicit import only)
├── server/
│   └── api/                   # Server routes (at project root)
├── composables/               # Composable auto-imports
└── nuxt.config.ts             # Extends layers
```

### Walking Skeleton Pattern
1. Create the DI composition root at `app/diComposition.ts`
2. Wire an InMemory fake adapter first
3. Create server routes in `server/api/`
4. Verify end-to-end works before adding real adapters
5. Swap adapter in `app/diComposition.ts` when ready
```

Phase 3 checklist adds: "Read `references/nuxt4-layers.md` before designing layer structure."

**Files affected:**
- `references/nuxt4-layers.md` (new)
- `phases/03-design.md` (add reference)

---

### AR-2 — Fake Adapter Path Pattern

**Problem:** No documented pattern for where to place fake adapters. The adapter discovery step was missing from Phase 3, leading to confusion during the todo app build.

**Fix:** New reference document at `references/adapters.md`:

```markdown
# Ports & Adapters — dev-flow Reference

## Pattern Overview

Every external dependency (API, database, auth, queue, observability) gets:
1. A port interface — the contract
2. A fake adapter — permanent test fixture
3. A real adapter — the production implementation
4. One DI binding in `app/diComposition.ts`

## Directory Convention

```
layers/{domain}/
├── ports/
│   └── XyzPort.ts          # Interface (the contract)
└── adapters/
    ├── FakeXyzAdapter.ts   # Permanent fake (never delete)
    └── XyzAdapter.ts       # Real implementation (deferred)
```

## Fake Adapter Rules

- Fake adapters are PERMANENT. Do not delete when real adapters are added.
- Fake adapters must walk end-to-end: they return realistic data that passes real validation.
- A fake adapter that throws "fake data" is not a walking fake. Build it properly.
- Fake adapters are used by tests and by the walking skeleton before real adapters exist.

## Discovery Step (Phase 3)

Before Phase 6, scan for all ports and their fakes:
- Ports without fakes: note as "fake needed before external dep"
- Fakes without ports: note as "orphan fake, create port"

## DI Binding Pattern

In `app/diComposition.ts`:
```typescript
// Swap by changing this line:
container.bind(TodoRepository).to(InMemoryTodoRepository)  // fake
// to:
container.bind(TodoRepository).to(InsforgeTodoRepository)  // real
```

## When to Build a Fake

Build a fake BEFORE touching any real adapter. The sequence is:
1. Define port interface
2. Build and verify fake adapter end-to-end
3. Only then build real adapter
```

Phase 3 checklist adds: "Run adapter discovery — list all ports, list all fakes, flag missing fakes before Phase 6."

**Files affected:**
- `references/adapters.md` (new)
- `phases/03-design.md` (add adapter discovery step)
- `phases/06-implementation.md` (reference in HARD-GATE section)

---

### AR-3 — Walking Skeleton Milestone

**Problem:** Walking skeleton was defined conceptually but not as the explicit first task in the implementation plan. The todo app build started implementation without a clear first milestone.

**Fix:** Implementation plan template (updated in `templates/implementation-plan.md`) always includes a "Skeleton Slice" as the first task:

```markdown
## Slice 0: Walking Skeleton

**Task 0.1: DI Composition Root**
- Create `app/diComposition.ts`
- Wire at least one fake adapter
- Verify app starts without errors

**Task 0.2: End-to-End Flow**
- One server route (e.g. GET /api/todos)
- One domain function
- One test that hits the full stack
- Tests run and pass

**Acceptance criteria:**
- [ ] App starts without errors
- [ ] `bun test` runs without errors
- [ ] One E2E flow works (read or create)
- [ ] At least one fake adapter wired
```

Phase 5 planning must produce this first slice. No other Phase 6 tasks start until all Slice 0 acceptance criteria pass.

**Files affected:**
- `templates/implementation-plan.md`
- `phases/05-planning.md`

---

### AR-4 — Premortem Risks → Tracked Tasks

**Problem:** Phase 4 pre-mortem identified risks but they were never turned into implementation tasks. Risks remained theoretical — some became real bugs.

**Fix:** Phase 5 planning step (after pre-mortem) converts each identified risk into a tracked implementation task:

```markdown
### [RISK] {risk name}
- **Source:** Pre-mortem Risk #{N}
- **Risk:** {one-line description}
- **Mitigation:** {what we'll do}
- **Acceptance criteria:** {test that proves mitigation works}
```

Every pre-mortem risk MUST have a corresponding implementation task or an explicit "accepted" note. Risks without tasks = Phase 5 gate fail.

**Files affected:**
- `phases/04-premortem.md` (add explicit step: "convert risks to tasks")
- `phases/05-planning.md`

---

### AR-5 — ADR Format Enforcement

**Problem:** ADR format varied across files (date formats, status values, missing fields). Automated parsing was fragile.

**Fix:** `gate_phase5b.py` (merged into the existing gate or as a sub-check) validates each ADR file:

| Check | Rule |
|---|---|
| Filename | Matches `NNNN-*.md` (4-digit prefix) |
| Required fields | `Date:`, `Status:`, `## Context`, `## Decision`, `## Consequences` |
| Status values | One of: Proposed / Accepted / Superseded / Deprecated / Rejected |
| Date format | `YYYY-MM-DD` |

Fail if any ADR has missing fields, invalid Status, or non-sequential numbering.

**Files affected:**
- `gates/gate_phase5b.py` (add ADR validation sub-check)
- `templates/decision-journal.md` (already correct, verify)

---

### ST-1 — Dual C4 Diagram Generation

**Problem:** The `.dev-flow/architecture/c4/` folder was empty after the todo app build. Users without Docker had no way to view C4 diagrams. Structurizr DSL generates frequent parse errors.

**Fix:** Phase 3 always generates BOTH formats simultaneously:

**Structurizr DSL** → `docs/workspace.dsl` (existing path)
- Docker users: `docker run -it --rm -p 8080:8080 -v $(pwd)/docs:/usr/local/structurizr structurizr/lite`
- View at `http://localhost:8080`

**Mermaid C4** → `.dev-flow/architecture/c4/` (new, always generated)
```
.dev-flow/architecture/c4/
├── context.mmd        # C4Context diagram
├── containers.mmd     # C4Container diagram
└── components-{name}.mmd  # C4Component per container
```

Both formats are committed in the same git commit. Mermaid diagrams render natively in GitHub, GitLab, VS Code, and any Markdown viewer — no Docker required.

Phase 3 quality gate adds these as **explicit checklist items** (not prose descriptions):
- [ ] `docs/workspace.dsl` exists with valid Structurizr DSL
- [ ] `.dev-flow/architecture/c4/*.mmd` files exist (Mermaid C4 — **NEW checklist item added by ST-1**)
- [ ] `references/c4-documentation.md` includes Mermaid C4 syntax reference

**Files affected:**
- `phases/03-design.md` (add dual generation step)
- `references/c4-documentation.md` (add Mermaid C4 syntax reference)

---

### ST-2 — Structurizr DSL Validation

**Problem:** Structurizr DSL has frequent parse errors, especially on Windows (path separators, quotes). Errors were discovered late — sometimes after Phase 6 was underway.

**Fix — Two-Part Validation:**

**Part 1 — Immediate (after Phase 3 DSL generation):**
The orchestrator performs a lightweight DSL validation check after generating `workspace.dsl`:

1. **Structural check**: Verify the file contains the required top-level blocks:
   - `workspace {` ... `}` wrapping everything
   - `model {` inside the workspace block
   - `views {` inside the workspace block
   - `!docs architecture/` inside the workspace block
   - `!adrs decisions/` inside the workspace block

2. **Brace balance check**: Count opening `{` and closing `}` — must balance

3. **Path check**: Warn if any Windows backslashes are found in the file

4. **Docker fallback**: If Docker is available, run `structurizr-cli validate workspace.dsl` (or start Structurizr Lite briefly to surface parse errors)

5. **On parse error**: Show error with line number and do NOT proceed to the Phase 3 checkpoint

Common DSL errors to surface with fix guidance:
- Unmatched braces: line where brace count goes negative
- Missing `model {` or `views {`: block not found
- `!docs` or `!adrs` outside `workspace { }`: directive placement error
- Backslash paths on Linux/macOS: replace `\` with `/`

No full DSL parser library is required — the above checks catch the common errors that caused failures in practice.

**Part 2 — Gate (Phase 5b / Phase 6 start):**
- `gate_phase5b.py` checks `docs/workspace.dsl` exists and is non-empty
- `gate_phase6_start.py` confirms DSL exists (fails fast if missing)
- Phase 6 will not start with a broken DSL

**Files affected:**
- `phases/03-design.md` (add validation step after DSL generation)
- `gates/gate_phase5b.py` (add DSL existence check)
- `gates/gate_phase6_start.py` (add DSL existence check)

---

### ST-3 — Pre-Implementation Review Gate (Soft Gate)

**Problem:** Design docs and implementation plans are created during Phases 3 and 5. The user only sees the output after Phase 6 is done — too late to catch issues.

**Fix — Soft gate notification after Phase 3 and Phase 5:**

After Phase 3 completes:
```
Design docs ready. Review before proceeding to Pre-Mortem:
- Architecture overview: .dev-flow/architecture/01-overview.md
- C4 diagrams (Mermaid): .dev-flow/architecture/c4/
- C4 diagrams (Structurizr): http://localhost:8080 (if Docker available)
- Sequence/flow diagrams: .dev-flow/architecture/sequences/
- Deferred decisions: .dev-flow/architecture/deferred-decisions.md

Have you reviewed them? [Yes, proceed] [Not yet]
```

After Phase 5 completes:
```
Implementation plan ready. Review before Phase 6:
- Plan: .dev-flow/plans/implementation.md
- Pre-mortem risks: .dev-flow/plans/premortem.md
- Architecture: .dev-flow/architecture/

Have you reviewed the plan? [Yes, proceed] [Not yet]
```

This is a **soft gate** — the orchestrator asks, the user can proceed, but the prompt makes review obvious. The goal is human review before irreversible implementation decisions are made.

**Implementation:** Add as an explicit checklist item in the Phase 3 and Phase 5 checkpoint sections. For example, in the Phase 3 checkpoint:
```
### Documentation Review (ST-3)
- [ ] User has been shown the design doc locations and prompted to review
- [ ] Structurizr URL shown if Docker available
- [ ] Mermaid C4 paths shown as fallback
```

**Files affected:**
- `phases/03-design.md` (add review gate as explicit checkpoint checklist item)
- `phases/05-planning.md` (add review gate as explicit checkpoint checklist item)

---

## Tier 4 — DECISION CONTEXT & LESSONS

Self-improving feedback system that makes the plugin learn from every project.

### DC-1 — Engram Integration (Heavy)

**Problem:** No cross-project context. Lessons from the todo app build don't help the next project unless manually copied.

**Fix — Three integration points:**

**Phase 0 (on every start — modify Step 0.2 in `commands/dev-flow.md`):**

The existing `mem_search` step in dev-flow.md Step 0.2 (Engram Context Load) is the integration point. Modify it to:

1. `mem_search "{engramProjectKey}"` for prior sessions on this project (existing step)
2. If found: present summary, ask "Continue from where we left off, or start fresh?" (existing step)
3. **New**: Scan `dev-flow-plugin/lessons/` directory (if it exists) for lesson files with tags matching the current project context:
   - Read `dev-flow-plugin/lessons/TOPICS.md` for the topic index
   - Match by `framework`, `phase`, and `stack` frontmatter
   - Surface top matching lessons as a brief list in the Phase 0 output
4. **New**: Read `.dev-flow/lessons.md` if it exists — surface recent entries as "context from this project"

The Phase 1 discovery file (`phases/01-discovery.md`) is NOT modified. All Engram and plugin-lessons integration happens within the existing Step 0.2 context in `commands/dev-flow.md`.

**Phase 6 (before first task):**
1. Read `.dev-flow/lessons.md` AND `dev-flow-plugin/lessons/`
2. Filter by relevance: current framework (`nuxt`), current phase (`implementation`), current stack (`insforge`, `nuxt-ui`)
3. Inject top 3-5 relevant lessons into implementer agent dispatch prompt:
   ```
   Relevant lessons from past projects:
   - {lesson title}: {one-line summary}
   - {lesson title}: {one-line summary}
   ```
4. Also inject into fixer agent dispatch during fix loops

**Phase 8 (on completion):**
1. `mem_save key: {enagramProjectKey}-complete` with structured summary
2. Orchestrator proposes pushing project lessons to plugin lessons library (DC-5)

**Files affected:**
- `commands/dev-flow.md` (Phase 0 Step 0.2 — Engram Context Load: modify existing `mem_search` block to also scan plugin lessons)
- `phases/06-implementation.md` (Phase 6 lesson injection, Step 6.9 Adjustment Gate)
- `phases/08-completion.md` (Phase 8: `mem_save` + lessons sync step)
- `phases/01-discovery.md` — NOT modified; all Engram/lessons integration lives in Phase 0

---

### DC-2 — lessons.md Format Validation

**Problem:** `.dev-flow/lessons.md` format was not enforced. Entries could be malformed or incomplete.

**Fix:** A gate or sub-check validates `.dev-flow/lessons.md`:

| Check | Rule |
|---|---|
| Header | Each entry starts with `## {date}` |
| Required fields | `**Error:**`, `**Root cause:**`, `**Fix:**` |
| Append-only | No existing entries edited (append-only file) |
| Non-empty | File is not empty |

**DC-2 is a two-tier check:**

1. **Existence (soft warn):** If `.dev-flow/lessons.md` does not exist at Phase 5b, warn but do not fail. The file may not yet contain entries if no gaps were encountered. Create a placeholder file if missing so DC-3 has a target to append to.

2. **Format (hard fail):** If the file exists but entries are malformed (missing `## {date}` header, missing `**Error:**`, missing `**Fix:**`), fail at the gate. Entries must follow the append format.

**Files affected:**
- `gates/gate_phase5b.py` (add lessons.md format check)
- `commands/dev-flow.md` (cross-cutting: format reminder on append)

---

### DC-3 — Lessons Appended During Failures

**Problem:** Lessons were only appended at phase end. Mid-phase failures, bugs, and workarounds were not captured.

**Fix — Cross-cutting orchestrator rule:**

During ANY phase, whenever:
- A gap is identified
- An unexpected error occurs
- A workaround is discovered
- A question reveals a workflow blind spot

→ Append to `.dev-flow/lessons.md` immediately. Not at the end of the phase. At the moment of discovery.

Format (same as DC-2):
```markdown
## {date} — {one-line title}

**Error:** {what went wrong}

**Root cause:** {what caused it}

**Fix:** {what was done, or "pending" if deferred}

**Phase:** {which phase this occurred in}
```

**Files affected:**
- `commands/dev-flow.md` (cross-cutting: append-on-gap rule)
- All phase files (add lessons trigger step)

---

### DC-4 — Lessons Injected Into Agent Prompts

**Problem:** Lessons existed in `.dev-flow/lessons.md` but implementer agents never read them. The same mistakes repeated across tasks.

**Fix:** Before Phase 6 (and before each implementer dispatch in Phase 6):

1. Orchestrator reads `.dev-flow/lessons.md`
2. Orchestrator reads `dev-flow-plugin/lessons/` directory
3. Filters lessons by:
   - Current phase = `implementation`
   - Current framework (e.g., `nuxt`)
   - Current stack (e.g., `nuxt-ui`, `insforge`)
   - Severity = `critical` (always included)
4. Injects into implementer agent system prompt:
   ```
   ## Relevant Past Lessons
   {lesson title}: {one-line summary of the lesson and the rule}
   {lesson title}: {one-line summary}
   ```
5. Also injects into fixer agent during fix loops (debug lessons are most relevant here)

**Files affected:**
- `phases/06-implementation.md`
- `agents/implementer.md` (update system prompt template)
- `agents/fixer-agent.md`

---

### DC-5 — Two-Tier Lessons Sync

**Problem:** Project lessons stay in the project forever. The plugin never learns from past projects automatically.

**Fix — Phase 8 completion step:**

After Phase 8 generates the completion report:

1. Orchestrator scans `.dev-flow/lessons.md`
2. Presents high-value lessons for promotion:
   ```
   Promising lessons detected:
   - {title}: {one-line summary} [Promote] [Skip]
   - {title}: {one-line summary} [Promote] [Skip]

   [Promote all] [Select] [Skip]
   ```
3. For each promoted lesson, creates a file in `dev-flow-plugin/lessons/{category}/{slug}.md`:
   ```markdown
   # {slug} — {title}

   **Framework/Phase:** {framework} / {phase}
   **Severity:** {critical | important | minor}
   **Date:** {original lesson date}
   **Source project:** {project name}

   ## Context
   {original error section}

   ## Lesson
   {original fix section distilled into an actionable rule}

   ## Rule
   {one-sentence actionable rule for future projects}
   ```
4. Updates `dev-flow-plugin/lessons/TOPICS.md` index:
   ```markdown
   ## {Category}
   - [{slug}]({category}/{slug}.md)
   ```
5. Tags: `framework`, `phase`, `severity`, `stack`

**Lesson category taxonomy:**
- `testing/` — test runner, E2E, isolation
- `architecture/` — component patterns, layer boundaries, ports & adapters
- `framework-{name}/` — framework-specific (e.g., `framework-nuxt/`)
- `workflow/` — process gaps, phase gaps, gate failures
- `security/`

**Files affected:**
- `phases/08-completion.md` (add lessons sync step)
- `dev-flow-plugin/lessons/TOPICS.md` (new)
- `dev-flow-plugin/lessons/` directory structure (new)

---

## Enhancement Count

Total: **20 named enhancements** across 4 tiers:
- Tier 1 CRITICAL: 3 (CR-1, CR-2, CR-3)
- Tier 2 HIGH-PRIORITY: 4 (HI-1, HI-2, HI-3, HI-4)
- Tier 3 ARCHITECTURE & DOCS: 8 (AR-1, AR-2, AR-3, AR-4, AR-5, ST-1, ST-2, ST-3)
- Tier 4 DECISION CONTEXT & LESSONS: 5 (DC-1, DC-2, DC-3, DC-4, DC-5)

The earlier "25" count included the cross-tier items as separate entries — they are not separate enhancements. They are the same CR/HI/AR/DC enhancements referenced in multiple places.

## Implementation Plan Structure

The enhancements are implemented in this dependency order:

### Phase 1 — Gate Infrastructure (foundational)
- CR-1: Python cross-platform fixes
- CR-2: Path alignment
- DC-2: lessons.md format validation (soft warn for existence, hard fail for malformed entries)

### Phase 2 — Phase 6 Quality Enforcement
- CR-3: `gate_phase6_evidence.py` (new gate)
- HI-1: Make reviews non-optional
- HI-3: Slice tracking (Wired column)
- HI-4: E2E test count check

### Phase 3 — Phase 7 Integration
- HI-2: YOLO decision review in Phase 7

### Phase 4 — Phase 3 & 5 Documentation Improvements
- AR-1: `references/nuxt4-layers.md`
- AR-2: `references/adapters.md`
- AR-3: Walking skeleton in plan template
- AR-4: Premortem risks as tasks (Phase 5 gate verifies)
- AR-5: ADR format enforcement (in gate_phase5b.py)
- ST-1: Dual C4 generation (PUML + Mermaid)
- ST-2: DSL validation (structural + brace + path checks)
- ST-3: Pre-implementation review gates (Phase 3 + Phase 5 checkpoints)

### Phase 5 — Lessons System
- DC-1: Engram integration (Phase 0 Step 0.2, Phase 6 lesson injection, Phase 8 mem_save)
- DC-3: Lessons appended during failures (cross-cutting rule in dev-flow.md)
- DC-4: Lessons injected into agent prompts (implementer + fixer agents)
- DC-5: Two-tier lessons sync (Phase 8 completion step, creates `dev-flow-plugin/lessons/` structure)

---

## What Does Not Change

- The 8-phase structure stays the same
- Agent types (implementer, spec-reviewer, quality-reviewer, fixer) stay the same
- State.json schema is backwards-compatible (new fields added, none removed)
- Preferences system unchanged
- `why/` and `examples/` directories unchanged
- Frontend commands (`frontend-animate`, `frontend-audit`, etc.) unchanged
- `dev-flow/docs/plugin-enhancement-design.md` is the design artifact for this enhancement cycle, not a plugin file

---

## Verification

Each enhancement is verified by:
- CR-1: All gates run without UnicodeEncodeError on Windows cp1252 console
- CR-2: `gate_phase5b.py` finds the plan at `.dev-flow/plans/implementation.md`
- CR-3: `gate_phase6_evidence.py` fails if ADR files are missing, test suite doesn't pass, or slices are scaffolded but not wired
- HI-1: Spec and quality reviews are dispatched for every task and loop until pass
- HI-2: Phase 7 presents YOLO decisions if any exist in state.json
- HI-3: Plan template has Wired column; gate fails if scaffolded ≠ wired
- HI-4: Gate fails if planned E2E count ≠ actual discovered count
- AR-1: `references/nuxt4-layers.md` exists and is referenced in Phase 3 checklist
- AR-2: `references/adapters.md` exists and adapter discovery step is in Phase 3
- AR-3: Implementation plan template always has Slice 0 (Walking Skeleton) as the first task
- AR-4: Phase 5 gate (or Phase 5 quality checklist) verifies every pre-mortem risk has a corresponding task or accepted note
- AR-5: Gate fails if any ADR has missing required fields
- ST-1: `.dev-flow/architecture/c4/*.mmd` files exist after Phase 3; Phase 3 quality gate explicitly checks for them
- ST-2: Phase 3 DSL validation uses the concrete structural + brace + path checks; parse errors are caught before checkpoint
- ST-3: Phase 3 and Phase 5 checkpoint sections include the soft review gate as an explicit checklist item; orchestrator presents the review prompt
- DC-1: Phase 0 Step 0.2 in dev-flow.md scans Engram and surfaces plugin lessons; Phase 8 mem_save is called
- DC-2: Gate warns (soft) if `.dev-flow/lessons.md` is missing; gate fails (hard) if file exists with malformed entries
- DC-3: Cross-cutting orchestrator rule is documented in commands/dev-flow.md; Phase 6.9 Adjustment Gate reads lessons.md as an explicit step
- DC-4: `agents/implementer.md` system prompt template is updated to include a `## Relevant Past Lessons` section; Phase 6 orchestrator populates it before dispatch
- DC-5: Phase 8 completion step proposes promoting lessons; `dev-flow-plugin/lessons/TOPICS.md` index is updated

---

## Consequences

**What becomes easier:**
- Running the plugin on Windows without silent gate failures
- Enforcing quality at every Phase 6 task boundary
- Reviewing design docs before committing to implementation
- Viewing C4 diagrams without Docker
- Learning from past projects via the lessons system
- Tracking which slices are truly wired vs. just scaffolded

**What becomes harder:**
- Skipping spec or quality reviews (now enforced)
- Starting Phase 6 without a valid workspace.dsl
- Proceeding past Phase 5 without reviewing docs

**Trade-offs accepted:**
- More gate checks = slightly longer workflow startup. Worth it for reliability.
- Dual C4 generation doubles diagram work in Phase 3. Worth it for accessibility.
- Lessons injection adds context to every agent dispatch. Worth it for preventing repeated mistakes.
