# Guardrails Design — Preventing UI Implementation Failures

Date: 2026-04-03
Status: Accepted

## Context

In a previous Nuxt + @nuxt/ui project, four systemic failures occurred:

1. Pages scaffolded in wrong directory — Nuxt only auto-discovers pages from `app/pages/`, but pages were placed in `layers/links/pages/`, resulting in silent blank pages
2. No visual verification — server routes tested with curl but browser never opened to confirm UI rendered
3. `@nuxt/ui` installed but zero `U*` components used — all form elements were raw HTML/Tailwind
4. UI layer had zero tests — 34 tests covered the adapter/service layer, 0 for the UI

The devloop workflow has no enforcement for (1), (2), or (3). These failures are preventable with targeted guardrails.

## Decision

Add four guardrails across two layers:

| # | Guardrail | Layer | When it fires |
|---|-----------|-------|---------------|
| G1 | Visual Verification | Workflow | After first walking skeleton pages exist (Phase 6) |
| G2 | Page Directory Check | Preferences (nuxt-insforge) | After each page-creating task (Phase 6) |
| G3 | U* Component Usage Check | Preferences (nuxt-insforge) | After each page-creating task (Phase 6) |
| G4 | UI Test Coverage | Workflow | End of Phase 6 (Phase 6.7 quality gate) |

## Design Principles

- **Workflow gates** are stack-agnostic Python scripts or Phase 6 steps that apply to all projects
- **Preferences** are stack-specific rules that only fire for the nuxt-insforge preference set
- Guardrails should **fail fast** — catch problems at write-time or immediately after a task, not hours later
- Do NOT modify other preference sets — changes are scoped to nuxt-insforge only

---

## Guardrail G1 — Visual Verification (Workflow)

### What

After the first page-creating task in Phase 6 completes, run a Playwright headless check that:
1. Navigates to `http://localhost:3000`
2. Waits for network idle
3. Asserts no console errors (Error level)
4. Asserts at least one key element is present (nav, form, or main content)
5. Exits 0 on success, 1 on failure

### Where it lives

Phase 6 implementation phase — new step after the first page-creating task completes, before the spec reviewer is dispatched.

### Why

The walking skeleton reference in the workflow correctly says "start full stack and verify data flows end-to-end." No step actually enforced this. G1 closes that gap by making browser verification a hard step, not an optional one.

### Integration

- If check fails: dispatch fixer agent with the task, re-run verification until pass
- Does NOT take a screenshot — automated pass/fail only
- Requires dev server running — implementer is responsible for starting `bun dev` before the check

---

## Guardrail G2 — Page Directory Check (Preferences, nuxt-insforge)

### What

After each task that creates or modifies `.vue` files in a `pages/` directory, the agent verifies:
- All page files are under `layers/{domain}/pages/`
- No pages exist outside this path

If a page is found at an incorrect path (e.g., `layers/links/pages/` instead of `app/pages/` or the correct layer path):
1. Fail the task
2. Report: "Page found at wrong path: `{path}`. Pages must live in `layers/{domain}/pages/` for their domain."
3. Dispatch fixer to move the page to the correct location

### Where it lives

- Phase 6 implementation — agent step after each task that touches `pages/` directories
- NOT a Python gate script — enforced by the agent reading the task diff
- Enforced for nuxt-insforge set only

### Trigger condition

Task touches files matching `**/pages/**/*.vue` or `**/pages/*.vue`.

### Nuxt-specific context

Nuxt auto-discovers pages from `app/pages/`. When using the layers architecture, each domain layer has its own `pages/` directory at `layers/{domain}/pages/`. Pages placed outside these paths are silently ignored — no error, just blank screen.

---

## Guardrail G3 — U* Component Usage Check (Preferences, nuxt-insforge)

### What

Two-part enforcement:

**Part A — ESLint rule**

Custom ESLint rule `no-raw-form-elements` in `.claude-plugin/rules/`:
- Fires when `@nuxt/ui` is in `package.json`
- Flags raw HTML form elements in `.vue` files: `<input>`, `<button>`, `<form>`, `<select>`, `<textarea>`
- Reports: "Raw `{element}` found. Use `<U{Element}>` from @nuxt/ui instead."
- Does NOT flag elements inside `<template #fallback>` or `<client-only>`

**Part B — Agent step**

After each page-creating task in Phase 6:
1. Run ESLint on changed `.vue` files
2. If `no-raw-form-elements` fires: fail task with the ESLint output
3. Fixer replaces raw elements with appropriate `U*` components
4. Re-run ESLint until clean

### Where it lives

- ESLint rule: `.claude-plugin/rules/no-raw-form-elements.js`
- Agent step: Phase 6 implementation, after each page-creating task
- Enforced for nuxt-insforge set only

### Trigger condition

- ESLint rule always active when `@nuxt/ui` is in `package.json` (no per-task trigger needed)
- Agent step triggers after any task that creates/modifies `.vue` files

### Example failure

```
no-raw-form-elements: Raw <input> found at layers/links/pages/index.vue:3.
Use <UInput> from @nuxt/ui instead. See: https://ui.nuxt.dev/components/input
```

---

## Guardrail G4 — UI Test Coverage (Workflow)

### What

Already exists as a Phase 6.7 quality gate checklist item. This spec makes it explicit:

After each task involving UI changes, verify:
- Playwright component tests or page tests exist for the rendered page
- Or: unit tests for composables that drive the UI

This is a quality gate at the end of Phase 6, not a per-task blocker.

### Where it lives

Phase 6.7 quality gate checklist (already exists, this spec clarifies scope).

---

## Implementation Files

| File | Change |
|------|--------|
| `.claude-plugin/rules/no-raw-form-elements.js` | New — custom ESLint rule |
| `.claude-plugin/phases/06-implementation.md` | Add G1 visual verification step after first page task; add G2/G3 as per-task agent steps |
| `.claude-plugin/preferences/sets/nuxt-insforge/tech-stack.md` | Document G2 and G3 as required rules for nuxt-insforge |

---

## Alternatives Considered

### G1 alternatives

- **Screenshot + human review**: Rejected — requires human in the loop, slows down the workflow, not automatable in CI
- **curl + grep for HTML**: Rejected — server can return 200 with empty body and pass the check

### G2 alternatives

- **Python gate script**: Rejected — page directory rules are Nuxt-specific (different frameworks have different conventions), so they belong in preferences, not workflow gates
- **Agent reminding**: Rejected — reminders are ignored; must be a hard fail

### G3 alternatives

- **Runtime smoke test**: Rejected — Playwright test would catch missing components only after they're rendered, not at write-time
- **Manual documentation**: Rejected — documented rules are ignored; must be enforced
