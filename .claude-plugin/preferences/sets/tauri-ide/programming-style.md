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
Rust: use Result<T, Box<dyn std::error::Error>> for all async commands. Never unwrap() on user-facing paths.
Frontend: let CodeMirror and xterm.js own their internal state. Only catch errors at the plugin API boundary.
