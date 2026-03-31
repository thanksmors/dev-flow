# Phase 6 Gate, Pre-Flight Check, and Structurizr Cleanup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix four workflow issues in the dev-flow plugin: (1) add a pre-flight env-var check before Phase 6 starts, (2) make deferred-decision handling a hard gate at Phase 6 end, (3) simplify Structurizr setup to Docker-only with DSL error docs, (4) create the deferred-decisions tracker at Phase 3 instead of Phase 6.5.

**Architecture:** Documentation-only changes to plugin markdown files. No code, no tests needed. Changes are concentrated in four plugin files: `phases/06-implementation.md` (pre-flight + deferred gate), `references/c4-documentation.md` (Docker simplification + DSL errors), `commands/dev-flow.md` (remove orphan folder reference), and `phases/03-design.md` (tracker creation timing).

**Tech Stack:** This plugin — all edits are markdown file changes.

---

## Before You Start

Read these files in full before touching anything:
- `.claude-plugin/phases/06-implementation.md` — the file you'll modify most
- `.claude-plugin/references/c4-documentation.md` — the file being simplified
- `.claude-plugin/commands/dev-flow.md` — the file losing the orphan folder reference
- `.claude-plugin/phases/03-design.md` — the file getting tracker creation earlier
- `docs/superpowers/specs/2026-03-31-deferred-decisions-phase6-gate-design.md` — the design this plan implements

---

## Task 1: Add Phase 6 Pre-Flight Gate (Step 6.0)

**Files:**
- Modify: `.claude-plugin/phases/06-implementation.md`

Add a new **Step 6.0** before the existing Step 6.1 in `phases/06-implementation.md`. Insert it after the HARD-GATE section block at the top and before "## 6.1 Execution Mode".

The new Step 6.0 replaces the current opening of Section 6.1 (the `## 6.1 Execution Mode` heading becomes `## 6.2 Sequential Subagents`, and all subsequent section numbers shift by +1: 6.2→6.3, 6.3→6.4, ..., 6.8→6.9).

### Step 6.0 Pre-Flight Check

Add this as a new section:

```markdown
## 6.0 Pre-Flight Check (HARD-GATE)

**Before any task runs, scan the full implementation plan for missing dependencies.**

### 6.0.1 Env Var and Third-Party Dependency Scan

Read `docs/superpowers/plans/implementation.md` (or the active plan path in state.json).
Scan all tasks for:
- `process.env.*` references → check if the env var is set in `.env` or `.env.example`
- Third-party service URLs (API endpoints, database connection strings, OAuth provider configs)
- Adapter references: any adapter in the deferred-decisions tracker with Status = `fake`

### 6.0.2 If Anything Is Missing

1. **Pause the workflow** — do NOT dispatch any implementer subagents.
2. **Present the missing dependency list:**

```
⚠️ Pre-flight failed — missing dependencies:

Env vars referenced but not configured:
  STRIPE_SECRET_KEY  — used in PaymentAdapter (task N)
  DATABASE_URL       — used in UserRepository (task N)

Third-party services not yet configured:
  SendGrid — EmailAdapter fake still wired (swap before Phase 6 begins)

Resolve these before continuing. Run `/dev-flow continue` once ready.
```

3. **Resume** runs the pre-flight check again from the top.

### 6.0.3 If All Clear

Show: "✅ Pre-flight passed — no missing env vars or third-party dependencies detected."
Proceed directly to Step 6.1 (Execution Mode).

### Implementation Note

This is a **HARD-GATE** — the workflow does not proceed to Step 6.1 until pre-flight passes. No warning, no override. The scan logic is: read the plan, grep for `process.env`, check `.env` for existence. If unsure whether an env var is configured, treat it as missing.
```

### Renumber Subsequent Sections

After adding Step 6.0, renumber all existing sections in `phases/06-implementation.md`:
- `## 6.1 Execution Mode` → `## 6.1 Execution Mode` (unchanged — Step 6.0 comes before it)
- Wait — Step 6.0 is NEW, so existing 6.1 stays 6.1. Only the sections that were 6.2+ shift.
- Old 6.2 "Sequential Subagents" → stays as a sub-section of 6.1
- `## 6.2 C4 Workspace Sync` → `## 6.3 C4 Workspace Sync`
- `## 6.3 Deferred Decision Swaps` → `## 6.4 Deferred Decision Swaps`
- `## 6.4 E2E Verification` → `## 6.5 E2E Verification`
- `## 6.5 Design Compliance Review` → `## 6.6 Design Compliance Review`
- `## 6.6 Quality Gate` → `## 6.7 Quality Gate`
- `## 6.7 Engram Save` → `## 6.8 Engram Save`
- `## 6.8 Phase 6 Adjustment Gate` → `## 6.9 Phase 6 Adjustment Gate`

Also update any **cross-references** within the file (e.g., "see Section 6.5" → "see Section 6.4", etc.).

- [ ] **Step 1: Add Step 6.0 Pre-Flight Check section** — insert new section before Step 6.1 in `phases/06-implementation.md`

- [ ] **Step 2: Renumber sections 6.2–6.9** — update all section headings and internal cross-references in `phases/06-implementation.md`

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/phases/06-implementation.md
git commit -m "feat(dev-flow): add Step 6.0 pre-flight env-var and dependency check"
```

---

## Task 2: Convert Deferred-Decision Swaps from Soft Note to Hard Gate

**Files:**
- Modify: `.claude-plugin/phases/06-implementation.md`

Two sub-changes within `phases/06-implementation.md`:

### 2A: Rewrite Section 6.4 (formerly 6.3) Deferred Decision Swaps

Replace the current Section 6.3 text with this — the key change is that this section now runs as a **hard gate on the Phase 7 checkpoint**, one-by-one, with explicit dispositions for every open item.

**The current text** (to be replaced) starts at `## 6.3 Deferred Decision Swaps` and runs through the swap protocol. The new text:

```markdown
## 6.4 Deferred-Decision Gate (HARD-GATE)

**After all Phase 6 tasks complete, before the Phase 7 checkpoint — this section MUST run.**

### 6.4.1 Read the Tracker

Read `.dev-flow/architecture/deferred-decisions.md`.
Count open items: any row where Status = `fake` or `pending`.

### 6.4.2 If No Open Deferred Decisions

Show: "No open deferred decisions. Proceeding to Phase 7 checkpoint."
Continue to the Phase 7 checkpoint immediately.

### 6.4.3 If Open Deferred Decisions Exist

**Present each one, one at a time.** For each, show:

```
Deferred Decision: {AdapterName}
Current status: {fake|pending}
Deferred to: {what it's deferred to}
Original trigger: {trigger criteria from tracker}

Options:
  [1] Resolve — swap fake→real adapter now
  [2] Re-defer — keep open, update trigger criteria with new reason
  [3] Skip — mark as closed with documented reason
```

**Option 1 — Resolve:**
Run the Swap Protocol from Step 6.4.5.

**Option 2 — Re-defer:**
- Ask the user to provide the new trigger criteria in plain text
- Update the `Trigger Criteria` column in the tracker
- Mark Status as `pending` (if it was `fake`)
- Move to next item.

**Option 3 — Skip:**
- Require the user to type a brief reason (one sentence minimum)
- Update the tracker's `Trigger Criteria` column with: "SKIPPED — {reason}"
- Mark Status as `skipped`
- Move to next item.

### 6.4.4 Hard Gate Enforcement

**This is a HARD-GATE on the Phase 7 checkpoint.** The standard checkpoint options (Continue / Pause / End) are NOT shown until ALL open deferred decisions have a final disposition (resolved, re-deferred, or skipped with reason).

After the last item is handled:
```
All {N} deferred decisions handled.
Proceeding to Phase 7 checkpoint.
```

### 6.4.5 Swap Protocol (unchanged from current 6.3)

The swap protocol stays the same as in the current Section 6.3:

1. Mark the fake as `@deprecated use XyzAdapter`
2. Create the real adapter implementing the same port interface
3. Swap the DI binding (one line in composition root)
4. Run full test suite — all must pass
5. Update the deferred-decisions tracker: set **Status** to `swapped`, **Swapped On** to today's date
```

### 2B: Update the Phase 6 Checkpoint Section

Find the Phase 6 checkpoint (the text that starts with `## Quality Gate` or the checkpoint section near the end of Phase 6). The current Phase 6 checkpoint presents options `[Continue to Gap Analysis] [Pause] [End]`.

After this task's changes, the checkpoint flow is:
1. Run Section 6.4 Deferred-Decision Gate FIRST
2. Then show the Phase 7 checkpoint options

Update the checkpoint description text to reflect this:

```markdown
## Phase 6 Checkpoint

Before presenting options:

1. ✅ Run Section 6.4 Deferred-Decision Gate — ALL open items must be resolved, re-deferred, or skipped before proceeding
2. ✅ Present Phase 7 checkpoint options:

Options: [Continue to Gap Analysis] [Pause] [End]
```

Also update the **Phase 6 Quality Gate** checklist item that references deferred decisions. Find and update the line that currently says something like "Deferred decision swaps: which were done, which were kept" in the checkpoint summary. Change it to:

```
- [ ] ALL deferred decisions have a final disposition (resolved / re-deferred / skipped with reason)
```

### 2C: Phase 6 Quality Gate Checklist

Update the Quality Gate section (now Section 6.7 after renumbering) to add:

```
- [ ] All deferred decisions reviewed at Section 6.4 gate (hard gate passed)
```

And update any references to "Section 6.3" or "Section 6.5" to match the new numbering (6.4 for Deferred-Decision Gate, 6.5 for E2E, 6.6 for Design Compliance, 6.7 for Quality Gate, 6.8 for Engram Save, 6.9 for Phase 6 Adjustment Gate).

- [ ] **Step 4: Rewrite Section 6.4 Deferred-Decision Gate** — replace current soft Section 6.3 with hard-gate version in `phases/06-implementation.md`

- [ ] **Step 5: Update Phase 6 checkpoint** — reflect that deferred-decision gate runs before checkpoint options in `phases/06-implementation.md`

- [ ] **Step 6: Update Quality Gate checklist** — add hard-gate passed item in `phases/06-implementation.md`

- [ ] **Step 7: Commit**

```bash
git add .claude-plugin/phases/06-implementation.md
git commit -m "feat(dev-flow): make deferred-decision review a hard gate on Phase 7"
```

---

## Task 3: Structurizr Cleanup — Docker-Only and DSL Error Docs

**Files:**
- Modify: `.claude-plugin/references/c4-documentation.md`
- Modify: `.claude-plugin/commands/dev-flow.md`

### 3A: Simplify c4-documentation.md — Docker-Only

In `.claude-plugin/references/c4-documentation.md`, find the section **"Starting Structurizr Lite"**. Replace the current content (which has docker-compose + fallback) with this:

```markdown
## Starting Structurizr Lite

Run this one command:

```bash
docker run -it --rm -p 8080:8080 -v $(pwd)/docs:/usr/local/structurizr structurizr/lite
```

Open http://localhost:8080 in your browser.

Structurizr Lite watches `workspace.dsl` for changes and auto-refreshes the browser. Keep it running split-screen with your editor for the fastest feedback loop.

> **Note:** `workspace.json` is auto-generated by Structurizr Lite when it first reads `workspace.dsl`. After the first run, commit `workspace.json` to version control.
```

**Remove entirely:**
- The `docker-compose.yml` example
- The "Default: docker compose (wired to dev server)" section
- The "Start everything together: `docker compose up`" instruction
- The "Fallback: standalone Docker" section and its heading
- The "Auto-refresh" section (its content is merged into the simplified version above)

### 3B: Add Common DSL Errors Section to c4-documentation.md

After the existing content (before any "See Also" section), add:

```markdown
## Troubleshooting

### Common DSL Parse Errors

Structurizr DSL errors show the file, line number, unexpected token, and expected tokens. Here are the most common errors and how to fix them.

**Error: "Unexpected tokens (expected: include, exclude, autolayout, default, animation, title, description, properties)"**

Cause: A directive keyword used outside its valid context. The `replace` keyword, for example, is not valid at the workspace level.

Fix: Remove the invalid directive. Check the DSL reference for where a keyword is valid.

Example bad:
```
replace user [position:left]   # 'replace' is not valid at workspace level
```

Example good: Remove the line or move it inside the correct block.

---

**Error: "Unexpected tokens (expected: !docs, !decisions, group, container, description, tags, url, properties, perspectives, ->)"**

Cause: Incorrect syntax inside a `component` definition. The assignment operator (`=`) is not valid when defining inline components.

Example bad:
```
diComposition = component "DI Composition" "Single binding: LinkPort → adapter" "TypeScript" ""
```

Example good — no assignment operator for inline components:
```
component "DI Composition" "Single binding: LinkPort → adapter" "TypeScript"
```

Note: The fourth parameter (technology) is optional. An empty string `""` for technology is also unusual — omit it if there is no specific technology to note.
```

### 3C: Remove Orphan Folder Reference from dev-flow.md

In `.claude-plugin/commands/dev-flow.md`, find the **Artifacts Directory Structure** section. It contains:

```
.dev-flow/
├── architecture/           # Phase 3 outputs
│   ├── c4/                 # C4 diagrams (Structurizr DSL)   ← REMOVE THIS LINE
│   ├── sequences/          # Mermaid sequence diagrams
│   └── folder-structure.md # Project folder layout
```

Remove the `│   ├── c4/` line (and the comment `# C4 diagrams (Structurizr DSL)`). The C4 files live in `docs/` per the C4 docs, not in `.dev-flow/`.

Keep `sequences/` and `folder-structure.md` under `.dev-flow/architecture/` — those are correct.

- [ ] **Step 8: Simplify c4-documentation.md** — remove docker-compose, keep Docker one-liner only in `.claude-plugin/references/c4-documentation.md`

- [ ] **Step 9: Add Common DSL Errors section** — add troubleshooting section to `.claude-plugin/references/c4-documentation.md`

- [ ] **Step 10: Remove orphan c4/ folder reference** — update artifacts directory in `.claude-plugin/commands/dev-flow.md`

- [ ] **Step 11: Commit**

```bash
git add .claude-plugin/references/c4-documentation.md .claude-plugin/commands/dev-flow.md
git commit -m "feat(dev-flow): simplify Structurizr to Docker-only, add DSL error docs, remove orphan folder"
```

---

## Task 4: Create Deferred-Decisions Tracker at Phase 3

**Files:**
- Modify: `.claude-plugin/phases/03-design.md`
- Modify: `.claude-plugin/phases/06-implementation.md` (one line update)

### 4A: Update Phase 3 Step 3.7

Find the current **Step 3.7 "Deferred Architectural Decisions"** in `phases/03-design.md`. Currently it says to create `.dev-flow/architecture/deferred-decisions.md` with a markdown template.

**The change:** After creating the tracker file, ALSO add every deferred decision from the Phase 3 design to the tracker immediately — don't wait for Phase 6.5.

Update Step 3.7 text to include this additional action:

In the `### 3.7 Deferred Architectural Decisions` section, after the block that creates the tracker, add:

```markdown
**IMPORTANT — populate the tracker immediately:** Every deferred decision identified in this phase (fake adapter, deferred DB choice, deferred auth provider, etc.) must be added to the tracker right now — not at Phase 6.5. The tracker is a living document from Phase 3 forward.

For each deferred decision in this phase:
1. Add a row to the tracker table
2. Set initial Status: `fake` or `pending`
3. Set the trigger criteria from what was documented above
```

Also update the **Phase 3 Quality Gate** checklist item for deferred decisions. Find the line about deferred decisions in the quality gate and ensure it says: "Deferred decisions are documented with adapter interfaces AND added to `.dev-flow/architecture/deferred-decisions.md` tracker."

### 4B: Update Phase 6 Section 6.4 (Deferred-Decision Gate) Intro

In the new Section 6.4 (Deferred-Decision Gate), update the `### 6.4.1 Read the Tracker` step text to reflect that the tracker was created at Phase 3:

```markdown
### 6.4.1 Read the Tracker

The tracker at `.dev-flow/architecture/deferred-decisions.md` was created at Phase 3 when each decision was first deferred. Read it now to see all open items.
```

- [ ] **Step 12: Update Phase 3 Step 3.7** — add instruction to populate tracker immediately in `.claude-plugin/phases/03-design.md`

- [ ] **Step 13: Update Phase 3 Quality Gate** — clarify deferred decisions must be added to tracker at Phase 3

- [ ] **Step 14: Update Section 6.4.1 intro** — note tracker was created at Phase 3

- [ ] **Step 15: Commit**

```bash
git add .claude-plugin/phases/03-design.md .claude-plugin/phases/06-implementation.md
git commit -m "feat(dev-flow): create deferred-decisions tracker at Phase 3 instead of Phase 6.5"
```

---

## Spec Coverage Check

| Spec Decision | Plan Task |
|---|---|
| D1: Phase 6 Pre-Flight Gate | Task 1 — Step 6.0 |
| D2: Phase 6 End Deferred-Decision Gate | Task 2 — Sections 6.4, checkpoint, quality gate |
| D3: Structurizr Docker-only | Task 3 — 3A |
| D4: Remove orphan .dev-flow/architecture/c4 | Task 3 — 3C |
| D5: DSL error docs | Task 3 — 3B |
| D8: Tracker at Phase 3 | Task 4 |

All 6 spec items are covered. No gaps.

## Placeholder Scan

- No "TBD", "TODO", or placeholder content in any step
- All file paths are exact
- All section names match existing headings being modified
- Cross-references updated to match new numbering

## Implementation Order

Tasks 1 and 2 both modify `phases/06-implementation.md`. Do them in order (1 then 2) — Task 2 references the new numbering from Task 1.

Tasks 3 and 4 are independent of each other and of Tasks 1-2. They can be done in any order after Task 1+2 are committed.
