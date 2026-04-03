# Multi-Preference-Sets Design

**Date:** 2026-04-02
**Status:** Approved

## Overview

Allow multiple named preference sets to be stored in the plugin, with user selection at Phase 0 via AskUserQuestion. On selection, the chosen set is copied into `.dev-flow/preferences/` in the project.

---

## Folder Structure

### Plugin Side

```
.claude-plugin/preferences/
  sets/
    default/           ← the default set
      tech-stack.md
      programming-style.md
      testing.md
      libraries-and-mcps.md
      setup-steps.md
      user-profile.md
    minimal/           ← example additional set
      ...same 6 files...
    full-stack/        ← another additional set
      ...same 6 files...
  defaults/            ← symlink → sets/default/  (backward compat path)
```

**Constraint:** Each set folder must contain exactly the same 6 filenames. No extra files.

### Project Side

```
.dev-flow/
  preferences/         ← the active set (copied from a named set on selection)
  available-sets.json ← generated: list of discovered sets with sources
  active-set.txt      ← generated: name of the active set (e.g. "default")
```

---

## Phase 0 Changes

### Step 0.0 — Discover Available Sets

Before the current Step 0.1, scan for available sets:

1. Scan `${CLAUDE_PLUGIN_ROOT}/preferences/sets/` — each subfolder is a named set
2. Check if `.dev-flow/preferences/` exists and contains at least one `.md` file → note it as "(project override)"
3. Generate `available-sets.json` at `.dev-flow/available-sets.json`:
   ```json
   {
     "sets": [
       { "name": "default", "source": "plugin", "path": "...", "hasOverride": false },
       { "name": "minimal", "source": "plugin", "path": "...", "hasOverride": false },
       { "name": "full-stack", "source": "plugin", "path": "...", "hasOverride": false }
     ]
   }
   ```

### Step 0.1 — AskUserQuestion: Select Set

Present options as a list. Format each as `"Set name — description"` where description is a one-line summary extracted from `tech-stack.md` + `user-profile.md`.

If project has `.dev-flow/preferences/` with an active set already:
- Show it first, marked with "(current)"
- Also show it as an option to re-select

Options format:
```
> "Choose a preference set:"
  1. default — Bun + Nuxt layers + Nuxt UI, developer profile, YOLO off (current)
  2. minimal — Bun + Nuxt, developer profile, YOLO off
  3. full-stack — Bun + Nuxt + Fastify + Nuxt UI, developer profile, YOLO off
  4. Reset to plugin defaults (no saved preferences)
```

### Step 0.2 — Load Selected Set

- If user picks a named set → copy those 6 files into `.dev-flow/preferences/`, overwriting existing files
- Write the set name to `.dev-flow/active-set.txt`
- Update `available-sets.json` with `hasOverride: true` for the selected set
- Proceed to existing Step 0.2 (show preference summary)

**Backward compat:** If `sets/` doesn't exist yet (plugin hasn't been migrated), fall back to loading from `preferences/defaults/` (the old path). This allows incremental migration.

---

## Migration: `defaults/` → `sets/default/`

- Create `preferences/sets/default/` with the current contents of `preferences/defaults/`
- Keep `preferences/defaults/` as a symlink to `sets/default/` for any hardcoded references
- Phase 0 discovery should check `sets/` first, then fall back to `defaults/`

---

## New Files to Create

| File | Purpose |
|------|---------|
| `.claude-plugin/preferences/sets/default/` | Copy of current defaults |
| `.claude-plugin/preferences/sets/minimal/` | New minimal set (TBD) |
| `.claude-plugin/preferences/sets/full-stack/` | New full-stack set (TBD) |
| `.claude-plugin/preferences/defaults` | Symlink → `sets/default/` |
| `.dev-flow/available-sets.json` | Generated discovery manifest |
| `.dev-flow/active-set.txt` | Written on set selection |

## Modified Files

| File | Change |
|------|--------|
| `commands/devloop.md` | Phase 0 steps updated (0.0, 0.1, 0.2 as above) |

---

## Open Questions

- **Set creation:** No UI/command for users to create new named sets yet — that comes in a later iteration. For now, sets are added by editing plugin files directly.
- **Per-set descriptions:** How does Phase 0 extract a one-line description? Suggest storing a `description.txt` or `summary` field in each set folder. Recommend: read `tech-stack.md` first line + `user-profile.md` profile type.
