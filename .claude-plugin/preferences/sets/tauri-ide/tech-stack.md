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
tailwindcss + shadcn/ui
# Tailwind CSS 4.x for utility-first styling.
# shadcn/ui for component primitives (sidebar, tabs, dialog, command palette, tree view, resizable panels).
# CodeMirror 6 for code editing (used by the code-editor plugin).
# xterm.js for terminal emulation (used by the terminal plugin).

## Architecture Pattern
plugin-driven shell
# Core app shell (sidebar, tabs, status bar) is separate from features.
# Each feature (code editor, terminal) is a plugin.
# Plugin contract: FrontendPlugin interface in src/plugin-api/.
# One-way dependency rule: core → plugin-api ← plugins.

## State Management
React Context + useReducer (ephemeral UI state: open tabs, active file, sidebar state)
Tauri Store (persistent state: recent workspaces, preferences, sidebar width)
CodeMirror 6 (editor state: document content, cursor, undo history — owned by CM6, not React state)
xterm.js (terminal buffer — owned by xterm.js, not React state)

## TypeScript
strict: true always

## Layer Boundary Rule
# src/core/ never imports from src/plugins/.
# src/plugin-api/ is the only bridge between core and plugins.
# src-tauri/src/core/ never imports from src-tauri/src/plugins/.
# Each plugin is isolated and deletable without breaking core.
