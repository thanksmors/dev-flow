# Multi-Preference-Sets v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename preference sets so `default` is the true starting point, create tauri-ide set, add YAML-frontmatter README to every set, create a YAML registry in root sets/README.md, and update Phase 0 to parse YAML instead of scanning directories.

**Architecture:** Rename existing directories via git mv to preserve history. Create new tauri-ide set by mapping the Tauri IDE design doc to the 7 required preference files. Add YAML frontmatter to each set README per the v2 spec. Phase 0 reads `${CLAUDE_PLUGIN_ROOT}/preferences/sets/README.md` YAML frontmatter to discover sets — no directory scanning needed.

**Tech Stack:** YAML frontmatter (Python `yaml` stdlib), bash git mv, Python file I/O.

---

## File Structure (End State)

```
.claude-plugin/preferences/sets/
├── README.md                          # Root registry with YAML frontmatter
├── default/                           # (was minimal) — Bun + Nuxt, no backend
│   ├── README.md                      # YAML frontmatter: name, description, stack, profile
│   ├── tech-stack.md
│   ├── programming-style.md
│   ├── testing.md
│   ├── libraries-and-mcps.md
│   ├── setup-steps.md
│   └── user-profile.md
├── nuxt-insforge/                     # (was default) — Bun + Nuxt + Insforge + Nuxt UI
│   ├── README.md                      # YAML frontmatter
│   ├── tech-stack.md
│   ├── programming-style.md
│   ├── testing.md
│   ├── libraries-and-mcps.md
│   ├── setup-steps.md
│   └── user-profile.md
├── full-stack/                        # Bun + Nuxt + Fastify
│   ├── README.md                      # YAML frontmatter (was missing)
│   ├── tech-stack.md
│   ├── programming-style.md
│   ├── testing.md
│   ├── libraries-and-mcps.md
│   ├── setup-steps.md
│   └── user-profile.md
└── tauri-ide/                         # NEW — Tauri 2.0 + React + Rust + CodeMirror 6
    ├── README.md                      # YAML frontmatter
    ├── tech-stack.md
    ├── programming-style.md
    ├── testing.md
    ├── libraries-and-mcps.md
    ├── setup-steps.md
    └── user-profile.md
```

---

## Before All Tasks

Run these commands once to verify current state:

```bash
cd /home/mors/Projects/dtt-ultrainstinct/devloop
ls .claude-plugin/preferences/sets/
# Expected output: default  full-stack  minimal
```

---

## Task 1: Rename Sets (minimal → default, default → nuxt-insforge)

**Files:**
- Modify: `.claude-plugin/preferences/sets/` (directory rename via git mv)

- [ ] **Step 1: Rename `minimal/` → `default/` via git mv**

```bash
git mv .claude-plugin/preferences/sets/minimal .claude-plugin/preferences/sets/default
```

- [ ] **Step 2: Verify the rename**

```bash
ls .claude-plugin/preferences/sets/
# Expected: default  full-stack
```

- [ ] **Step 3: Commit rename**

```bash
git commit -m "rename(minimal→default): rename minimal set to default as starting point"
```

---

## Task 2: Rename `default/` (original) → `nuxt-insforge/`

**Files:**
- Modify: `.claude-plugin/preferences/sets/` (directory rename via git mv)

- [ ] **Step 1: Rename the original default set (still named `default` in git working tree) → `nuxt-insforge/`**

The original `default/` was already committed in a prior session as `default/`. It still exists on disk as `default/` alongside the newly renamed `default/` (from minimal). Rename the original one.

```bash
git mv .claude-plugin/preferences/sets/default .claude-plugin/preferences/sets/nuxt-insforge
# Note: this moves the ORIGINAL default (Insforge stack), not the newly renamed default
```

Wait — verify which `default` we're moving. Run:

```bash
cat .claude-plugin/preferences/sets/default/tech-stack.md | head -5
# If output contains "none" for backend → this is the new default (from minimal) → DO NOT rename
# If output contains "insforge" for backend → this is the original → safe to rename to nuxt-insforge
```

If the wrong `default` is targeted, use `git status` to identify both directories and rename the correct one by its git object ID.

Correct approach:
```bash
# Identify the original default commit
git log --oneline -3 -- .claude-plugin/preferences/sets/default/

# The original default (Insforge) was committed as "feat(preferences): migrate defaults to sets/default/"
# Rename it via git mv
git mv .claude-plugin/preferences/sets/default .claude-plugin/preferences/sets/nuxt-insforge
```

- [ ] **Step 2: Verify bothrenames**

```bash
ls .claude-plugin/preferences/sets/
# Expected: default  nuxt-insforge  full-stack
```

- [ ] **Step 3: Commit**

```bash
git commit -m "rename(default→nuxt-insforge): rename original default set to nuxt-insforge"
```

---

## Task 3: Add README.md with YAML frontmatter to full-stack set

**Files:**
- Create: `.claude-plugin/preferences/sets/full-stack/README.md`

Read the existing `full-stack/tech-stack.md` and `full-stack/user-profile.md` to extract values for frontmatter before writing.

- [ ] **Step 1: Read tech-stack.md and user-profile.md for frontmatter values**

```bash
grep -A1 "^## Package Manager" .claude-plugin/preferences/sets/full-stack/tech-stack.md
grep -A1 "^## Backend" .claude-plugin/preferences/sets/full-stack/tech-stack.md
grep -A1 "^## Frontend" .claude-plugin/preferences/sets/full-stack/tech-stack.md
grep -A1 "^## UI Components" .claude-plugin/preferences/sets/full-stack/tech-stack.md
grep "^type:" .claude-plugin/preferences/sets/full-stack/user-profile.md
grep "^default:" .claude-plugin/preferences/sets/full-stack/user-profile.md
```

Expected values:
- `package_manager`: `bun`
- `backend`: `fastify`
- `frontend`: `nuxt`
- `ui`: `@nuxt/ui` (read from tech-stack.md UI Components section)
- `profile.type`: `developer` (read from user-profile.md)
- `profile.yolo_default`: `off` (read from user-profile.md)

- [ ] **Step 2: Write full-stack/README.md**

```markdown
---
name: full-stack
description: Bun + Nuxt + Fastify — for CPU-intensive backend work
stack:
  package_manager: bun
  backend: fastify
  frontend: nuxt
  ui: "@nuxt/ui"
profile:
  type: developer
  yolo_default: off
---

# full-stack Preference Set

Bun + Nuxt + Fastify — for CPU-intensive backend work.

## Stack Summary

- **Package Manager:** bun
- **Backend:** Fastify
- **Frontend:** Nuxt
- **UI:** @nuxt/ui
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/preferences/sets/full-stack/README.md
git commit -m "feat(preferences): add README with YAML frontmatter to full-stack set"
```

---

## Task 4: Add README.md with YAML frontmatter to nuxt-insforge set

**Files:**
- Create: `.claude-plugin/preferences/sets/nuxt-insforge/README.md`

- [ ] **Step 1: Read tech-stack.md and user-profile.md for frontmatter values**

```bash
grep -A1 "^## Package Manager" .claude-plugin/preferences/sets/nuxt-insforge/tech-stack.md
grep -A1 "^## Backend" .claude-plugin/preferences/sets/nuxt-insforge/tech-stack.md
grep -A1 "^## Frontend" .claude-plugin/preferences/sets/nuxt-insforge/tech-stack.md
grep -A1 "^## UI Components" .claude-plugin/preferences/sets/nuxt-insforge/tech-stack.md
grep "^type:" .claude-plugin/preferences/sets/nuxt-insforge/user-profile.md
grep "^default:" .claude-plugin/preferences/sets/nuxt-insforge/user-profile.md
```

Expected values:
- `package_manager`: `bun`
- `backend`: `insforge`
- `frontend`: `nuxt`
- `ui`: `@nuxt/ui`
- `profile.type`: `developer`
- `profile.yolo_default`: `off`

- [ ] **Step 2: Write nuxt-insforge/README.md**

```markdown
---
name: nuxt-insforge
description: Bun + Nuxt + Insforge + Nuxt UI — full vertical slices + ports-and-adapters
stack:
  package_manager: bun
  backend: insforge
  frontend: nuxt
  ui: "@nuxt/ui"
profile:
  type: developer
  yolo_default: off
---

# nuxt-insforge Preference Set

Bun + Nuxt + Insforge + Nuxt UI — full vertical slices + ports-and-adapters.

## Stack Summary

- **Package Manager:** bun
- **Backend:** Insforge
- **Frontend:** Nuxt
- **UI:** @nuxt/ui
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/preferences/sets/nuxt-insforge/README.md
git commit -m "feat(preferences): add README with YAML frontmatter to nuxt-insforge set"
```

---

## Task 5: Add README.md with YAML frontmatter to default set

**Files:**
- Create: `.claude-plugin/preferences/sets/default/README.md`

- [ ] **Step 1: Read tech-stack.md and user-profile.md for frontmatter values**

```bash
grep -A1 "^## Package Manager" .claude-plugin/preferences/sets/default/tech-stack.md
grep -A1 "^## Backend" .claude-plugin/preferences/sets/default/tech-stack.md
grep -A1 "^## Frontend" .claude-plugin/preferences/sets/default/tech-stack.md
grep -A1 "^## UI Components" .claude-plugin/preferences/sets/default/tech-stack.md
grep "^type:" .claude-plugin/preferences/sets/default/user-profile.md
grep "^default:" .claude-plugin/preferences/sets/default/user-profile.md
```

Expected values:
- `package_manager`: `bun`
- `backend`: `none`
- `frontend`: `nuxt`
- `ui`: `none`
- `profile.type`: `developer`
- `profile.yolo_default`: `off`

- [ ] **Step 2: Write default/README.md**

```markdown
---
name: default
description: Bun + Nuxt — single-app frontend, no backend yet
stack:
  package_manager: bun
  backend: none
  frontend: nuxt
  ui: none
profile:
  type: developer
  yolo_default: off
---

# default Preference Set

Bun + Nuxt — single-app frontend, no backend yet.

## Stack Summary

- **Package Manager:** bun
- **Backend:** none
- **Frontend:** Nuxt
- **UI:** none
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/preferences/sets/default/README.md
git commit -m "feat(preferences): add README with YAML frontmatter to default set"
```

---

## Task 6: Create tauri-ide preference set

**Files:**
- Create: `.claude-plugin/preferences/sets/tauri-ide/README.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/tech-stack.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/programming-style.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/testing.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/libraries-and-mcps.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/setup-steps.md`
- Create: `.claude-plugin/preferences/sets/tauri-ide/user-profile.md`

Read `.temp/TAURI_IDE_DESIGN.md` to map design sections to the 7 required preference files.

- [ ] **Step 1: Create tauri-ide/ directory**

```bash
mkdir -p .claude-plugin/preferences/sets/tauri-ide
```

- [ ] **Step 2: Write tauri-ide/README.md**

```markdown
---
name: tauri-ide
description: Tauri 2.0 + React + Rust + CodeMirror 6 — desktop IDE with plugin system
stack:
  package_manager: pnpm
  backend: none
  frontend: react
  ui: none
profile:
  type: developer
  yolo_default: off
---

# tauri-ide Preference Set

Tauri 2.0 + React + Rust + CodeMirror 6 — desktop IDE with plugin system.

## Stack Summary

- **Package Manager:** pnpm
- **Backend:** Rust (Tauri 2)
- **Frontend:** React 19
- **UI:** shadcn/ui + Tailwind CSS 4
```

- [ ] **Step 3: Write tauri-ide/tech-stack.md**

```markdown
# Tech Stack

## Package Manager
pnpm

## Backend
none
# Rust via Tauri 2. No separate backend server. Tauri handles file system, PTY, and OS access.

## Frontend
react@^19.0.0
# SPA via Vite 8. No SSR framework — Tauri needs a plain SPA, not SSR.

## UI Components
none
# No UI component library. Use native HTML elements or add shadcn/ui later.

## Architecture Pattern
plugin-driven shell
# Core app shell (sidebar, tabs, status bar) is separate from features.
# Each feature (code editor, terminal) is a plugin.
# Plugin contract: FrontendPlugin interface in src/plugin-api/.
# One-way dependency rule: core → plugin-api ← plugins.

## State Management
React Context + useReducer (ephemeral UI state)
Tauri Store (persistent state: recent workspaces, preferences)
# ~5 pieces of global state. Context + useReducer handles this.
# No Zustand, Redux, or Jotai needed.

## TypeScript
strict: true always

## Layer Boundary Rule
# src/core/ never imports from src/plugins/.
# src/plugin-api/ is the only bridge between core and plugins.
# src-tauri/src/core/ never imports from src-tauri/src/plugins/.
# Each plugin is isolated and deletable without breaking core.
```

- [ ] **Step 4: Write tauri-ide/programming-style.md**

```markdown
# Programming Style

## Core Philosophy
Plugin-first architecture. The app shell is dumb — it reads contributions from the plugin registry and renders them. Core never imports plugin code directly.

## Architecture Principles
One-way dependency rule: core → plugin-api ← plugins. Neither core nor plugins reach across the boundary.

Lean components: Tab components (CodeEditorTab, TerminalTab) are thin wrappers. They mount the third-party library into a div ref, wire up IPC, and that's it. Business logic lives in hooks.

No god contexts: separate WorkspaceContext, TabContext, PluginContext — not one catch-all context.

## Auth Pattern
N/A — desktop IDE with no auth requirements.

## Error Handling
Rust: use `Result<T, Box<dyn std::error::Error>>` for all async commands. Never `unwrap()` on user-facing paths.
Frontend: let CodeMirror and xterm.js own their internal state. Only catch errors at the plugin API boundary.
```

- [ ] **Step 5: Write tauri-ide/testing.md**

```markdown
# Testing Strategy

## Test Types

### Rust Unit Tests (cargo test)
Test core services in isolation. Mock the file system and PTY where needed.
Location: src-tauri/tests/*.rs

### Frontend Unit Tests (Vitest)
Test the plugin registry, file association resolution, and context reducers.
Location: src/**/*.test.ts
Location: src/plugin-api/__tests__/registry.test.ts

### Component Tests (Vitest + React Testing Library)
Test shell components and plugin API hooks.
Mock Tauri invoke with `vi.mock('@tauri-apps/api/core')`.

### E2E Tests (WebdriverIO)
Smoke tests on compiled app: launch, open folder, edit file, terminal, command palette.
Location: e2e/specs/*.spec.ts

## Coverage Thresholds
- Rust core services: 80% line coverage via cargo test
- Plugin registry logic: 90% line coverage
- Shell components: integration test coverage (no specific %)
- E2E: 5 critical paths minimum
```

- [ ] **Step 6: Write tauri-ide/libraries-and-mcps.md**

```markdown
# Libraries and MCPs

## Production Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| react | ^19.0.0 | UI framework |
| react-dom | ^19.0.0 | React DOM renderer |
| @tauri-apps/api | latest | Tauri IPC commands and events |
| @tauri-apps/plugin-store | latest | Persistent settings |
| codemirror | latest | Code editor (CM6) |
| @codemirror/lang-javascript | latest | JS/TS syntax |
| @codemirror/lang-rust | latest | Rust syntax |
| @codemirror/lang-html | latest | HTML syntax |
| @codemirror/lang-css | latest | CSS syntax |
| @codemirror/lang-json | latest | JSON syntax |
| @codemirror/lang-markdown | latest | Markdown syntax |
| @xterm/xterm | latest | Terminal emulator UI |
| @xterm/addon-fit | latest | xterm.js terminal fitting |
| @xterm/addon-webgl | latest | xterm.js WebGL renderer |
| tailwindcss | ^4.0.0 | Utility-first CSS |
| clsx | latest | ClassName utility |
| tailwind-merge | latest | Tailwind class merging |

## Dev Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| @tauri-apps/cli | latest | Tauri CLI, `pnpm tauri dev/build` |
| vite | ^8.0.0 | Dev server, bundler |
| @vitejs/plugin-react | latest | React plugin for Vite |
| typescript | ^5.0.0 | Type safety |
| @types/react | ^19.0.0 | React type definitions |
| @types/react-dom | ^19.0.0 | React DOM type definitions |
| vitest | latest | Frontend unit tests |
| @testing-library/react | latest | Component tests |
| @testing-library/jest-dom | latest | DOM assertion matchers |
| webdriverio | latest | E2E test framework |
| @wdio/cli | latest | WebdriverIO CLI |

## MCPs
No MCPs required for tauri-ide set.
```

- [ ] **Step 7: Write tauri-ide/setup-steps.md**

```markdown
# Project Scaffolding

## Step 1: Scaffold Tauri + React app

```bash
pnpm create tauri-app tauri-ide --template react-ts --manager pnpm
cd tauri-ide
```

## Step 2: Upgrade to Vite 8 (Rolldown-powered)

```bash
pnpm add -D vite@^8.0.0 @vitejs/plugin-react@latest
```

Update `vite.config.ts`:
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindCSS()],
});
```

## Step 3: Install frontend dependencies

```bash
pnpm add react react-dom
pnpm add @tauri-apps/api @tauri-apps/plugin-store
pnpm add codemirror @codemirror/lang-javascript @codemirror/lang-rust @codemirror/lang-html @codemirror/lang-css @codemirror/lang-json @codemirror/lang-markdown
pnpm add @xterm/xterm @xterm/addon-fit @xterm/addon-webgl
pnpm add clsx tailwind-merge
pnpm add -D @types/react @types/react-dom typescript vitest @testing-library/react @testing-library/jest-dom
```

## Step 4: Install shadcn/ui

```bash
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button tabs dialog scroll-area separator tooltip resizable command
```

## Step 5: Create plugin API structure

```bash
mkdir -p src/plugin-api src/core/context src/core/shell src/core/hooks src/plugins/code-editor src/plugins/terminal
```

Create `src/plugin-api/types.ts` — define `FrontendPlugin`, `PluginContributions`, `TabContribution`, `PluginAPI` interfaces.

Create `src/plugin-api/registry.ts` — implement `registerPlugin()`, `getPlugins()`, `getTabComponentForFile()`.

Create `src/plugin-api/hooks.ts` — implement `usePluginAPI()` hook.

## Step 6: Scaffold app shell

Create `src/core/shell/Sidebar.tsx`, `FileTree.tsx`, `TabBar.tsx`, `TabContent.tsx`, `StatusBar.tsx`, `CommandPalette.tsx`.

Create `src/core/context/WorkspaceContext.tsx`, `TabContext.tsx`, `PluginContext.tsx`.

Wire PluginContext into shell components — shell reads from registry, never imports plugin code.

## Step 7: Scaffold code-editor plugin

Create `src/plugins/code-editor/index.ts` — implement `FrontendPlugin`, register `.ts`, `.tsx`, `.rs`, `.md`, etc. file associations.

Create `src/plugins/code-editor/CodeEditorTab.tsx` — CM6 wrapper, mount via EditorView in useEffect.

## Step 8: Scaffold Rust backend services

```bash
mkdir -p src-tauri/src/core src-tauri/src/plugin_host src-tauri/src/plugins/terminal src-tauri/tests
```

Create `src-tauri/src/core/fs.rs` — read_file, write_file, list_dir, watch_file commands.

Create `src-tauri/src/core/workspace.rs` — open_folder, recent_workspaces state.

Create `src-tauri/src/core/pty.rs` — spawn_shell via portable-pty, stream output via events.

Create `src-tauri/src/plugin_host/trait_def.rs` — `BackendPlugin` trait.

Create `src-tauri/src/plugin_host/registry.rs` — `PluginRegistry::activate_all()`.

## Step 9: Verify the shell walks

Run `pnpm tauri dev` — confirm window opens, sidebar shows, no console errors.
```

- [ ] **Step 8: Write tauri-ide/user-profile.md**

```markdown
# User Profile

## Profile Type
developer

## YOLO Mode
default: off

## Communication Style
 terse — short, direct answers
 explanation_depth: medium — show reasoning for architectural decisions only
```

- [ ] **Step 9: Commit**

```bash
git add .claude-plugin/preferences/sets/tauri-ide/
git commit -m "feat(preferences): add tauri-ide preference set from TAURI_IDE_DESIGN.md"
```

---

## Task 7: Create root sets/README.md with YAML registry

**Files:**
- Create: `.claude-plugin/preferences/sets/README.md`

- [ ] **Step 1: Write root sets/README.md**

```markdown
---
sets:
  - name: default
    description: Bun + Nuxt — single-app frontend, no backend yet
    path: default
  - name: nuxt-insforge
    description: Bun + Nuxt + Insforge + Nuxt UI — full vertical slices + ports-and-adapters
    path: nuxt-insforge
  - name: full-stack
    description: Bun + Nuxt + Fastify — for CPU-intensive backend work
    path: full-stack
  - name: tauri-ide
    description: Tauri 2.0 + React + Rust + CodeMirror 6 — desktop IDE with plugin system
    path: tauri-ide
---

# Preference Sets

A preference set defines the tech stack, patterns, and conventions for a project.
Each set lives in its own folder under `sets/`.

## Registry

The YAML frontmatter above (`sets:`) is the machine-readable registry.
Phase 0 parses this to build the AskUserQuestion options.

## Creating a New Set

1. Create a folder under `sets/`
2. Add all 7 required files (see below)
3. Add a `README.md` with YAML frontmatter to the set folder
4. Add the set to the root `README.md` YAML frontmatter

## Required Files

Each set must contain exactly these files:

| File | Purpose | Key Sections |
|------|---------|--------------|
| `tech-stack.md` | Runtime, backend, frontend, UI | Package Manager, Backend, Frontend, UI Components, Architecture Pattern, State Management, TypeScript, Layer Boundary Rule |
| `programming-style.md` | Architecture principles | Core Philosophy, Architecture Principles, Auth Pattern, Error Handling |
| `testing.md` | Test strategy | Test Types, Coverage Thresholds |
| `libraries-and-mcps.md` | Approved dependencies | Production Deps, Dev Deps, MCPs |
| `setup-steps.md` | Project scaffolding | Step-by-step initialization |
| `user-profile.md` | Communication defaults | Profile Type, YOLO Mode, Communication Style |
| `README.md` | Set documentation | YAML frontmatter (name, description, stack, profile) |

## Per-Set README Frontmatter

Each set's `README.md` must start with YAML frontmatter:

```yaml
---
name: {set-name}
description: {one-line description}
stack:
  package_manager: {e.g., bun, pnpm}
  backend: {e.g., none, insforge, fastify, nuxt-server-routes}
  frontend: {e.g., nuxt, react}
  ui: {e.g., none, @nuxt/ui}
profile:
  type: {non-technical, developer, experienced-developer}
  yolo_default: {on, off}
---
```

The frontmatter is parsed by Phase 0 to extract the one-line description shown in AskUserQuestion options.
```

- [ ] **Step 2: Commit**

```bash
git add .claude-plugin/preferences/sets/README.md
git commit -m "feat(preferences): add root sets/README.md with YAML registry"
```

---

## Task 8: Update Phase 0 in dev-flow.md to parse YAML instead of directory scanning

**Files:**
- Modify: `.claude-plugin/commands/devloop.md` — Step 0.0 and Step 0.1 sections

The current Phase 0 uses directory scanning. Replace it with YAML parsing from the root `sets/README.md` YAML frontmatter.

- [ ] **Step 1: Read current Step 0.0 and Step 0.1 in dev-flow.md**

Find the section that reads:
```
### Step 0.0 — Discover Available Sets
...
Scan `${CLAUDE_PLUGIN_ROOT}/preferences/sets/` — each subfolder is a named set
```

- [ ] **Step 2: Replace Step 0.0 with YAML-based discovery**

Replace the current Step 0.0 content with:

```
### Step 0.0 — Discover Available Sets

Before Step 0.1, read the YAML registry to discover available preference sets.

1. Read `${CLAUDE_PLUGIN_ROOT}/preferences/sets/README.md`
2. Parse the YAML frontmatter (between `---` markers) to extract `sets[]` — each entry has `name`, `description`, `path`
3. If YAML parsing fails or `sets/` does not exist → fall back to scanning `${CLAUDE_PLUGIN_ROOT}/preferences/sets/` directories (backward compat)
4. Check if `.dev-flow/preferences/` has an active set (read `.dev-flow/active-set.txt` if it exists)
5. Write `.dev-flow/available-sets.json`:

```json
{
  "sets": [
    { "name": "default",       "source": "plugin", "path": ".../sets/default",       "description": "Bun + Nuxt — single-app frontend, no backend yet",       "hasOverride": false },
    { "name": "nuxt-insforge", "source": "plugin", "path": ".../sets/nuxt-insforge", "description": "Bun + Nuxt + Insforge + Nuxt UI — full vertical slices", "hasOverride": false },
    { "name": "full-stack",    "source": "plugin", "path": ".../sets/full-stack",    "description": "Bun + Nuxt + Fastify — for CPU-intensive backend work",  "hasOverride": false },
    { "name": "tauri-ide",     "source": "plugin", "path": ".../sets/tauri-ide",     "description": "Tauri 2.0 + React + Rust + CodeMirror 6 — desktop IDE",  "hasOverride": false }
  ],
  "activeSet": null
}
```

Set `activeSet` to the value from `active-set.txt` if it exists.
```

- [ ] **Step 3: Replace Step 0.1 description-sourcing logic**

Replace the current Step 0.1 description logic:
> "For each set, extract a one-line description: read the first non-empty line of `tech-stack.md`..."

Replace with:
> "For each set, the description comes from the `description` field in `available-sets.json` (extracted from the YAML registry). No need to read any set files."

Keep the rest of the AskUserQuestion structure identical.

- [ ] **Step 4: Verify the updated Step 0.0 and Step 0.1 sections**

Read the updated file and confirm:
- Step 0.0 mentions YAML parsing from `sets/README.md`
- Step 0.1 references `available-sets.json` `description` field
- Step 0.2 (Load Selected Set) is unchanged

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/commands/devloop.md
git commit -m "feat(phase0): parse YAML registry in sets/README.md instead of scanning directories"
```

---

## Self-Review Checklist

**1. Spec coverage:**
- [x] Rename `minimal/` → `default/` → Task 1
- [x] Rename `default/` → `nuxt-insforge/` → Task 2
- [x] Add README frontmatter to `full-stack/` → Task 3
- [x] Add README frontmatter to `nuxt-insforge/` → Task 4
- [x] Add README frontmatter to `default/` → Task 5
- [x] Create `tauri-ide/` set with all 7 files → Task 6
- [x] Create root `sets/README.md` with YAML registry → Task 7
- [x] Update Phase 0 to parse YAML → Task 8

**2. Placeholder scan:**
- No "TBD", "TODO", or incomplete steps found
- All file paths are exact
- All YAML frontmatter values are concrete (no placeholders)

**3. Type consistency:**
- All YAML `name` fields match directory names exactly
- `backend: none` for default set (not "None" or empty)
- `package_manager: pnpm` for tauri-ide, `bun` for all Nuxt-based sets
- YAML boolean: `yolo_default: off` (not `false`)
