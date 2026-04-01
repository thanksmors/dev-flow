# Multi-Preference-Sets v2 Design

**Date:** 2026-04-02
**Status:** Approved

## Overview

Revamp the preference sets to use a YAML registry and rename sets so `default` is the true starting point (currently `minimal`).

---

## Set Naming

| Folder | Name | Description |
|--------|------|-------------|
| `default/` (was `minimal`) | `default` | Bun + Nuxt — single-app frontend, no backend |
| `nuxt-insforge/` (was `default`) | `nuxt-insforge` | Bun + Nuxt + Insforge + Nuxt UI |
| `full-stack/` | `full-stack` | Bun + Nuxt + Fastify |
| `tauri-ide/` (new) | `tauri-ide` | Tauri 2.0 + React + Rust + CodeMirror 6 |

---

## Root Registry: `preferences/sets/README.md`

Serves as both machine-readable registry (YAML frontmatter) and human-readable template guide.

```yaml
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

---

## Phase 0 Changes

### Step 0.0 — Discover Available Sets

Replace directory scanning with YAML parsing:

1. Read `${CLAUDE_PLUGIN_ROOT}/preferences/sets/README.md`
2. Parse YAML frontmatter to extract `sets[]` — each entry has `name`, `description`, `path`
3. If YAML parsing fails → fall back to scanning `sets/` directories (backward compat)
4. Check if `.dev-flow/preferences/` has an active set (read `.dev-flow/active-set.txt`)
5. Write `.dev-flow/available-sets.json`:

```json
{
  "sets": [
    { "name": "default",   "source": "plugin", "path": ".../sets/default",   "hasOverride": false },
    { "name": "nuxt-insforge", "source": "plugin", "path": ".../sets/nuxt-insforge", "hasOverride": false },
    { "name": "full-stack",   "source": "plugin", "path": ".../sets/full-stack",   "hasOverride": false },
    { "name": "tauri-ide",    "source": "plugin", "path": ".../sets/tauri-ide",    "hasOverride": false }
  ],
  "activeSet": null
}
```

### Step 0.1 — AskUserQuestion: Select Set

Build options from `available-sets.json`. For each set, description comes from YAML `description` field (no need to read files).

If active set exists → mark it "(current)".

### Step 0.2 — Load Selected Set

Unchanged from v1 design (copy files, write `active-set.txt`).

---

## Implementation Tasks

1. **Rename `minimal/` → `default/`**
2. **Rename `default/` → `nuxt-insforge/`**
3. **Update `full-stack/README.md`** with YAML frontmatter
4. **Update `nuxt-insforge/README.md`** with YAML frontmatter (after rename)
5. **Update `default/README.md`** with YAML frontmatter (after rename)
6. **Create `tauri-ide/` set** from `.temp/TAURI_IDE_DESIGN.md` — map design doc sections to the 7 required files:
   - `tech-stack.md` → pnpm, Vite 8, Tauri 2, Rust, React 19, TypeScript, Tailwind CSS 4, shadcn/ui, CodeMirror 6, xterm.js
   - `programming-style.md` → plugin contract, one-way dependency rule, lean components, IPC naming conventions
   - `testing.md` → cargo test (Rust), Vitest (frontend), WebdriverIO (E2E)
   - `libraries-and-mcps.md` → Tauri API packages, CodeMirror, xterm.js
   - `setup-steps.md` → pnpm create tauri-app, Vite 8 upgrade, plugin API scaffolding, shell layout
   - `user-profile.md` → developer, YOLO off
   - `README.md` → YAML frontmatter + summary
7. **Create root `preferences/sets/README.md`** with YAML registry
8. **Update Phase 0** to parse YAML instead of scanning directories
