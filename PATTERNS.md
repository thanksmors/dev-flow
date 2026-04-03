# Observed Patterns

Patterns identified during devloop iterations that warrant watching.
Each entry: what to watch for, how many times seen, whether it's fixed.

## Active Patterns

| Pattern | First Seen | Occurrences | Status |
|---------|-----------|-------------|--------|
| Internal consistency: integration table vs. directory structure | 2026-04-01 | 1 | :blue_circle: Watch |

### :blue_circle: Internal Consistency: Integration Table vs. Directory Structure

**What to check:** In any `codebase-map.md`, verify the integration points table
matches the directory tree structure documented in the same file.

**How to check:** Cross-reference table entries against `## Directory Structure`
section. Contradictions = pattern active.

**Gate hint:** This should be caught by Phase 2 quality gate item:
`"Integration points table entries match the directory structures documented in
the same file"`

**Occurrences:**
- [x] 2026-04-01 — Phase 2 for [project] — integration table listed `src/api/`
  but directory tree showed `src/routes/` — contradiction caught late

---

## Resolved / Retired Patterns

_(moves here when no longer observed after 2 consecutive projects or explicitly fixed)_
