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
  backend: {e.g., none, tauri, insforge, fastify, nuxt-server-routes}
  frontend: {e.g., nuxt, react}
  ui: {e.g., none, @nuxt/ui, shadcn/ui}
profile:
  type: {non-technical, developer, experienced-developer}
  yolo_default: {on, off}
---
```

The frontmatter is parsed by Phase 0 to extract the one-line description shown in AskUserQuestion options.
