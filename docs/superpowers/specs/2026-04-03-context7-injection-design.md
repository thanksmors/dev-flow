# Spec: Context7 Injection Rules

Date: 2026-04-03
Status: Draft

## Context

workspace.dsl (Structurizr DSL) syntax is frequently broken in practice. Additionally, unexpected errors during implementation require fresh, accurate library documentation. Both situations benefit from consulting Context7 — up-to-date, authoritative documentation — rather than relying on potentially stale training data.

## Decision

Add Context7 consultation as hard-coded inline instructions in the relevant phase files. No new hooks, no new mechanics — just visibility of the rule in the right places.

---

## 1. workspace.dsl — Always Consult Context7

**Where:** Phase 6 (Implementation) and Phase 7 (Gap Analysis)

**What to add (exact location):**

In **Phase 6** (`phases/06-implementation.md`), add to Section 6.3 C4 Workspace Sync:

> **ALWAYS consult Context7 before writing or modifying `docs/workspace.dsl`.**
> Use `mcp__plugin_context7_context7__resolve-library-id` with query `"structurizrdsl"` or `"structurizr python"`, then `mcp__plugin_context7_context7__query-docs` for the specific syntax needed (component, relationship, view, etc.).
> Common needs: adding a component, changing a relationship label, creating a view, using `contains()`, `uses()`, `internal()`.
> Do NOT write DSL from memory. Verify every DSL block against current Structurizr documentation.

In **Phase 7** (`phases/07-gap-analysis.md`), add to the Architecture Gaps section under Step 7.1:

> **ALWAYS consult Context7 when updating `docs/workspace.dsl`.**
> If the gap analysis reveals that workspace.dsl is out of sync with the code, update workspace.dsl using the same Context7 workflow as Phase 6 Section 6.3.

---

## 2. Debugging — Always Consult Context7 on Unexpected Errors

**Where:** Phase 6 (`phases/06-implementation.md`), Section 6.8 Debugging Escalation

**What to add (exact location):**

At the **top of the Debugging Escalation section** (before "Round 1 — 3 Hypothesis Agents"):

> **ALWAYS consult Context7 when an error is unexpected or unexplained.**
> Before running hypothesis agents or attempting any fix, use `mcp__plugin_context7_context7__query-docs` with the relevant library/framework and error keywords.
> Examples:
> - Nuxt error → query `"nuxt 3"` with the error message
> - Prisma error → query `"prisma"` with the error message
> - TypeScript error → query `"typescript"` with the error message
> - Bun/Node error → query `"bun"` or `"node.js"` with the error message
> If Context7 returns relevant documentation, incorporate the findings before dispatching hypothesis agents.

This does NOT replace the hypothesis agent rounds. Context7 is consulted first to establish facts, then hypothesis agents are dispatched with that context.

---

## 3. Skill References — Update skill names

The `@dev:verification-before-completion` skill reference appears in:
- `phases/06-extras.md`
- `phases/06-implementation.md`

After the rebrand, these become `@devloop:verification-before-completion`. The skill file itself is not renamed — only the invocation reference changes.

---

## What Does NOT Change

- No new skill files
- No new hooks
- No new directories
- No workspace.dsl files are modified by this spec — only the instruction to consult Context7 is added
- Python gate scripts do not need Context7 (they use the standard library only)

---

## Effort Estimate

- **Rebrand** (Item 1): ~1 hour mechanical text replacement across ~50 files. Mostly find-and-replace with some manual verification of frontmatter fields.
- **Context7 injections** (Item 2): ~15 minutes — add 2 short instruction blocks to phase files.
- **Testing**: None required — this is documentation/instruction change only.

**Combined estimate**: ~1.5 hours total. No risk of breaking anything — purely textual changes with no code logic modifications.
