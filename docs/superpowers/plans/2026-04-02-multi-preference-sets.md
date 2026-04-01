# Multi-Preference-Sets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow multiple named preference sets in the plugin, selected at Phase 0 via AskUserQuestion. On selection, the chosen set is copied into `.dev-flow/preferences/` in the project.

**Architecture:**
- `preferences/sets/{name}/` — named sets live in the plugin, each containing exactly 6 preference files
- `preferences/defaults/` — symlink to `preferences/sets/default/` for backward compat
- `.dev-flow/available-sets.json` — generated discovery manifest written at Phase 0 start
- `.dev-flow/active-set.txt` — written when a set is selected and copied
- Phase 0 updated to discover sets, AskUserQuestion to select, then copy into `.dev-flow/preferences/`

**Tech Stack:** Plugin markdown files, shell (ln -s), Claude Code command/hook infrastructure

---

## File Map

**Create:**
- `.claude-plugin/preferences/sets/default/` — migrated from `preferences/defaults/`
- `.claude-plugin/preferences/sets/minimal/` — stripped-down stub
- `.claude-plugin/preferences/sets/full-stack/` — fuller stub
- `.dev-flow/available-sets.json` — generated at Phase 0
- `.dev-flow/active-set.txt` — written on set selection

**Modify:**
- `.claude-plugin/commands/dev-flow.md` — Phase 0 steps updated (add 0.0, 0.1, 0.2, keep 0.3+)

**Delete:**
- `.claude-plugin/preferences/defaults/` — replaced by symlink (not deleted — replaced by symlink)

---

## Task 1: Create `sets/default/` directory and copy current defaults

**Files:**
- Create: `.claude-plugin/preferences/sets/default/`
- Read source: `.claude-plugin/preferences/defaults/` (git history if not on disk)

- [ ] **Step 1: Read all 6 default preference files from git history**

Run:
```bash
git show HEAD~3:.claude-plugin/preferences/defaults/tech-stack.md
git show HEAD~3:.claude-plugin/preferences/defaults/programming-style.md
git show HEAD~3:.claude-plugin/preferences/defaults/testing.md
git show HEAD~3:.claude-plugin/preferences/defaults/libraries-and-mcps.md
git show HEAD~3:.claude-plugin/preferences/defaults/setup-steps.md
git show HEAD~3:.claude-plugin/preferences/defaults/user-profile.md
```

- [ ] **Step 2: Create `sets/default/` directory**

Run:
```bash
mkdir -p .claude-plugin/preferences/sets/default
```

- [ ] **Step 3: Write each file into `sets/default/`**

Write the 6 files with their full content from the git history reads above. Filenames:
- `tech-stack.md`
- `programming-style.md`
- `testing.md`
- `libraries-and-mcps.md`
- `setup-steps.md`
- `user-profile.md`

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/preferences/sets/default/
git commit -m "feat(preferences): migrate defaults to sets/default/"
```

---

## Task 2: Create `sets/minimal/` stub

**Files:**
- Create: `.claude-plugin/preferences/sets/minimal/` (6 files)
- Differences from default:
  - `tech-stack.md`: Remove `@nuxt/ui`, remove Insforge (backend: "none"), add note "minimal = no backend, no UI library"
  - `user-profile.md`: Same profile
  - Other files: Same as default (minimal doesn't remove testing philosophy, etc.)

- [ ] **Step 1: Create directory and write stripped-down `tech-stack.md`**

```markdown
# Tech Stack

## Package Manager
bun

## Backend
none
# Minimal project — no backend yet. Add Fastify or similar when needed.

## Frontend
nuxt@^4.0.0
# No layer architecture for minimal — single-app Nuxt until boundaries emerge.

## UI Components
none
# No UI component library. Use native HTML elements or add @nuxt/ui later.

## Architecture Pattern
single-app → vertical-slices-on-demand
# Start simple. Add layers/ports-adapters only when you have 3+ related domains.

## State Management
nuxt built-ins (useAsyncData/useFetch)
# Only add Pinia when you have genuine cross-page shared state.

## TypeScript
strict: true always

## Layer Boundary Rule
# For minimal: all code lives in `server/` and `pages/` until there is a reason to split.
# Create a layer only when 3+ pages/features share the same domain concept.
```

- [ ] **Step 2: Write `user-profile.md` for minimal**

```markdown
# User Profile

## Profile Type
type: developer

## YOLO Mode
default: off

## Communication Style
explanation-depth: standard
jargon: some
```

- [ ] **Step 3: Copy remaining 4 files from `sets/default/`**

Run:
```bash
cp .claude-plugin/preferences/sets/default/programming-style.md .claude-plugin/preferences/sets/minimal/
cp .claude-plugin/preferences/sets/default/testing.md .claude-plugin/preferences/sets/minimal/
cp .claude-plugin/preferences/sets/default/libraries-and-mcps.md .claude-plugin/preferences/sets/minimal/
cp .claude-plugin/preferences/sets/default/setup-steps.md .claude-plugin/preferences/sets/minimal/
```

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/preferences/sets/minimal/
git commit -m "feat(preferences): add minimal preference set"
```

---

## Task 3: Create `sets/full-stack/` stub

**Files:**
- Create: `.claude-plugin/preferences/sets/full-stack/` (6 files)
- Differences from default:
  - `tech-stack.md`: Add Fastify backend alongside Nuxt
  - `libraries-and-mcps.md`: Add Fastify-related packages
  - Other files: Same as default

- [ ] **Step 1: Create directory and write expanded `tech-stack.md`**

```markdown
# Tech Stack

## Package Manager
bun

## Backend
nuxt (server routes) + fastify
# Fastify for CPU-intensive or complex API work that doesn't fit Nuxt server routes.
# Use Nuxt server routes for simple CRUD. Graduate to Fastify when needed.

## Frontend
nuxt@^4.0.0

## UI Components
@nuxt/ui

## Architecture Pattern
vertical-slices + ports-and-adapters
# Nuxt layers for frontend domains. Fastify plugins for backend domains.
# Each domain is self-contained with its own tests.

## State Management
pinia (via @pinia/nuxt) + nuxt built-ins
# Pinia: cross-layer shared state (auth, user, cart, global prefs)
# useAsyncData/useFetch: server-fetched data local to a page

## TypeScript
strict: true always

## Agent-First Design
agentTriggered: true

## Layer Boundary Rule
# Same as default: layers/{domain}/ports/ + adapters/ per domain.
# Fastify domains live in server/plugins/ with co-located tests.
```

- [ ] **Step 2: Write updated `libraries-and-mcps.md`**

```markdown
# Libraries & MCPs

## Architecture
Same ports-and-adapters pattern as default.

## Required MCPs
- **insforge**: Backend as a service

## Production Dependencies

| Package | Purpose |
|---------|---------|
| @nuxt/ui | Component library |
| @pinia/nuxt | Cross-layer shared state |
| nuxt | Framework |
| fastify | CPU-intensive API work |

## Development Dependencies

| Package | Purpose |
|---------|---------|
| playwright | E2E testing |
| fast-check | Property-based testing |
| zod | Runtime validation |

## Adapter Dependencies
Same pattern as default — fake adapters always present before real adapters.
For Fastify: fake adapter in `server/plugins/{domain}/fakes/`.
```

- [ ] **Step 3: Copy remaining 4 files from `sets/default/`**

Run:
```bash
cp .claude-plugin/preferences/sets/default/programming-style.md .claude-plugin/preferences/sets/full-stack/
cp .claude-plugin/preferences/sets/default/testing.md .claude-plugin/preferences/sets/full-stack/
cp .claude-plugin/preferences/sets/default/setup-steps.md .claude-plugin/preferences/sets/full-stack/
cp .claude-plugin/preferences/sets/default/user-profile.md .claude-plugin/preferences/sets/full-stack/
```

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/preferences/sets/full-stack/
git commit -m "feat(preferences): add full-stack preference set"
```

---

## Task 4: Replace `preferences/defaults/` with a symlink to `sets/default/`

**Files:**
- Modify: `.claude-plugin/preferences/defaults/` (replace with symlink)

- [ ] **Step 1: Remove `defaults/` directory and create symlink**

Run:
```bash
rm -rf .claude-plugin/preferences/defaults/
ln -s sets/default .claude-plugin/preferences/defaults
```

Verify:
```bash
ls -la .claude-plugin/preferences/defaults
# Expected: defaults -> sets/default (symlink)

cat .claude-plugin/preferences/defaults/tech-stack.md
# Should show the same content as sets/default/tech-stack.md
```

- [ ] **Step 2: Commit**

```bash
git add .claude-plugin/preferences/defaults
git commit -m "feat(preferences): convert defaults/ to symlink pointing to sets/default/"
```

---

## Task 5: Update Phase 0 in `dev-flow.md`

**Files:**
- Modify: `.claude-plugin/commands/dev-flow.md` — insert new steps 0.0, 0.1, 0.2 before existing Step 0.1, renumber existing steps

- [ ] **Step 1: Read the current Phase 0 section in dev-flow.md**

Read from line 1 to approximately line 120 (the Phase 0 section).

- [ ] **Step 2: Replace the Phase 0 content**

Find the "## Phase 0 — Preference Bootstrap" section (starts around line 50-70). Replace everything from that header through the existing Step 0.1 with the new steps below.

**New Phase 0 content to insert:**

```markdown
## Phase 0 — Preference Bootstrap

Run this before checking state.json on every `/dev-flow` start (including `continue`). Not triggered by the `end` argument — Phase 8 runs immediately for `end`.

Also read `PRINCIPLES.md` at `${CLAUDE_PLUGIN_ROOT}/PRINCIPLES.md` — the six non-negotiables are active for the entire session.

### Step 0.0 — Discover Available Sets

Before Step 0.1, scan for available preference sets.

1. Resolve plugin root: `${CLAUDE_PLUGIN_ROOT}` — if not set, look for `${CLAUDE_PLUGIN_ROOT}/plugin.json` marker
2. Scan `${CLAUDE_PLUGIN_ROOT}/preferences/sets/` — each subfolder is a named set
3. If `sets/` does not exist → fall back to `${CLAUDE_PLUGIN_ROOT}/preferences/defaults/` (the legacy path) and treat it as the only set named "default"
4. Check if `.dev-flow/preferences/` exists in the project root and contains at least one `.md` file → note the current active set (read `.dev-flow/active-set.txt` if it exists)
5. Write `.dev-flow/available-sets.json`:

```json
{
  "sets": [
    { "name": "default",   "source": "plugin", "path": ".../sets/default",   "hasOverride": false },
    { "name": "minimal",   "source": "plugin", "path": ".../sets/minimal",   "hasOverride": false },
    { "name": "full-stack", "source": "plugin", "path": ".../sets/full-stack","hasOverride": false }
  ],
  "activeSet": null
}
```

Set `activeSet` to the value from `active-set.txt` if it exists.

### Step 0.1 — AskUserQuestion: Select Set

Build the options list from `available-sets.json`. For each set, extract a one-line description:
- Read the first non-empty line of `tech-stack.md` under the `## Package Manager` section (e.g., "bun")
- Read the first non-empty line of `## Backend` (e.g., "insforge" or "none")
- Read the `type:` value from `user-profile.md`
- Format: `"{name} — {bun} + {backend}, {profile} profile, YOLO {yolo-default}"`

If a set is the current active set (from `active-set.txt`), append " (current)".

**AskUserQuestion options:**
- [ ] Use saved preferences (only shown if `active-set.txt` exists and user picks the same set)
- [ ] **Set name 1** — description (current)
- [ ] **Set name 2** — description
- [ ] **Set name 3** — description
- [ ] Reset to plugin defaults (no saved preferences)

Ask:
> "Choose a preference set:"
{mutliselect: false, options: [...the list above...]}

### Step 0.2 — Load Selected Set

**If user picks "Use saved preferences":**
→ Load files from `.dev-flow/preferences/` in memory, skip to Step 0.3

**If user picks "Reset to plugin defaults (no saved preferences)":**
→ Remove `.dev-flow/preferences/` directory and `.dev-flow/active-set.txt`
→ Load files from `${CLAUDE_PLUGIN_ROOT}/preferences/defaults/` in memory
→ Do NOT write to disk for this session

**If user picks a named set:**
1. Resolve the set path: `${CLAUDE_PLUGIN_ROOT}/preferences/sets/{name}/`
2. Copy the 6 `.md` files from the set folder into `.dev-flow/preferences/`, overwriting existing files
3. Write the set name to `.dev-flow/active-set.txt`
4. Update `available-sets.json`: set `activeSet` to the chosen name, set `hasOverride: true` for that set
5. Load the files in memory and proceed to Step 0.3

After copying, count the files in `.dev-flow/preferences/`. If not exactly 6, print a warning:
> "Preference set copy warning: expected 6 files but found {N}. Check that the set at `{path}` is complete."

### Step 0.3 — Show Preference Summary

(Existing Step 0.2 — renumber from 0.2 to 0.3)
Extract from the loaded files:
- Stack: read `## Package Manager`, `## Backend`, `## Frontend` from tech-stack.md, join with " + "
- Profile: read the value after `type:` in `## Profile Type` from user-profile.md
- YOLO default: read the value after `default:` in `## YOLO Mode` from user-profile.md
- Output: > "Using {set-name} — stack: {stack}, profile: {type}, YOLO: {yolo-default}"

### Step 0.4 — Customize Preferences

(Existing Step 0.3 — renumber from 0.3 to 0.4)
Walk through each preference file one at a time, offer to customize.
```

**Then renumber the remaining steps (0.4 → 0.5, etc.) and the references to Step 0.2 and 0.3 throughout the rest of the document.**

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/commands/dev-flow.md
git commit -m "feat(phase0): add multi-set discovery and AskUserQuestion selection"
```

---

## Verification

After all tasks complete, verify:

1. `ls .claude-plugin/preferences/sets/` shows `default/`, `minimal/`, `full-stack/`
2. `ls .claude-plugin/preferences/defaults/` is a symlink to `sets/default/`
3. Each set folder has exactly 6 `.md` files
4. `.dev-flow/available-sets.json` is generated when Phase 0 runs
5. Selecting a set copies its 6 files into `.dev-flow/preferences/`
6. `.dev-flow/active-set.txt` is written with the set name

---

## Open Questions (resolved in this plan)

- **Set descriptions:** Extracted at runtime from `tech-stack.md` (bun + backend) + `user-profile.md` (type, YOLO). No extra metadata file needed.
- **Backward compat:** `sets/` checked first; if absent, falls back to `preferences/defaults/` (the old path). Allows incremental migration.
- **minimal vs full-stack defaults:** Both derived from the current defaults with specific modifications documented in Tasks 2 and 3.
