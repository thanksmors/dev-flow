# Tauri IDE — Design Document

> **Purpose**: This is the authoritative design document for a lightweight, plugin-driven terminal IDE built with Tauri 2.0. It is intended to be consumed by an AI coding agent (Claude Code CLI) as the single source of truth for all implementation decisions.

---

## 1. Product vision

A minimal, fast desktop IDE with three core capabilities:

1. **Code editing** — syntax-highlighted editing for all file types via CodeMirror 6
2. **Terminal** — integrated shell via xterm.js connected to a real PTY
3. **Workspace management** — open folders, switch between workspaces, file tree navigation

The app is designed to be extended via a plugin system. Features like markdown WYSIWYG editing (Milkdown/Crepe), Git integration, LSP support, and AI copilot are all future plugins — not part of v1 core.

---

## 2. V1 tech stack (approved)

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Package manager | pnpm | latest | Dependency management, script running |
| Dev server / bundler | Vite | 8.x (Rolldown-powered) | Dev server, HMR, production builds |
| Desktop shell | Tauri | 2.x | Native window, IPC, file system, OS access |
| Backend language | Rust | stable | Tauri backend, PTY management, file ops |
| Frontend framework | React | 19.x | UI components |
| Language | TypeScript | 5.x | Type safety, plugin contracts |
| Styling | Tailwind CSS | 4.x | Utility-first CSS |
| Component library | shadcn/ui | latest | Sidebar, tabs, command palette, dialogs, tree view |
| Code editor | CodeMirror 6 | latest | All file type editing (including markdown as plain text) |
| Terminal emulator | xterm.js | latest (@xterm/xterm) | Terminal UI in the browser |
| UI state | React Context + useReducer | built-in | Ephemeral UI state (open tabs, active file, sidebar) |
| Persistent state | @tauri-apps/plugin-store | latest | Workspace preferences, recent folders, settings |
| Unit tests (Rust) | cargo test | built-in | Backend service and plugin host tests |
| Unit tests (Frontend) | Vitest | latest (shares Vite config) | Component tests, plugin registry logic |
| E2E tests | WebdriverIO | latest | Smoke tests on compiled app |

### What we are NOT using and why

| Technology | Reason for exclusion |
|---|---|
| Bun | Redundant with Vite 8. Bun's speed advantage is marginal now that Vite uses Rolldown (Rust). Adds confusion about which tool does what. |
| Zustand / Redux / Jotai | Overkill. The app has ~5 pieces of global state. React Context + useReducer handles this. Tauri Store handles persistence. |
| Electron | Bundles Chromium + Node.js (~150MB). Tauri uses native webview (~15MB). |
| Monaco Editor | ~2-3MB, opinionated, hard to theme consistently with shadcn. CodeMirror 6 is lighter and more modular. |
| Milkdown / Crepe | Deferred to a future plugin. CM6 handles .md files as plain text for v1. |
| Next.js / Nuxt / SvelteKit | SSR frameworks. Tauri needs an SPA, not SSR. Plain Vite + React is correct. |
| Webpack | Vite is faster, simpler config, native ESM. |
| styled-components / CSS modules | Tailwind is sufficient and consistent with shadcn/ui. |

---

## 3. Project structure

```
tauri-ide/
├── package.json
├── pnpm-lock.yaml
├── vite.config.ts
├── vitest.config.ts              # Extends vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── index.html                    # Vite entry point
│
├── src-tauri/                    # ── RUST BACKEND ──
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── capabilities/
│   │   └── default.json          # Tauri 2 permission declarations
│   │
│   ├── src/
│   │   ├── main.rs               # Entry: builds Tauri app, registers plugins
│   │   ├── lib.rs                # Tauri::Builder configuration
│   │   │
│   │   ├── core/                 # Core services — NO plugin imports
│   │   │   ├── mod.rs
│   │   │   ├── fs.rs             # Read, write, watch files, list directory
│   │   │   ├── pty.rs            # Spawn shell, stream stdin/stdout via events
│   │   │   ├── workspace.rs      # Open folder, recent workspaces, active workspace
│   │   │   └── events.rs         # Typed event bus (emit to frontend, listen from frontend)
│   │   │
│   │   ├── plugin_host/          # Plugin infrastructure
│   │   │   ├── mod.rs
│   │   │   ├── trait_def.rs      # pub trait BackendPlugin — the contract
│   │   │   └── registry.rs       # Collects plugins, calls activate(), registers commands
│   │   │
│   │   └── plugins/              # Each plugin is an isolated module
│   │       ├── mod.rs            # Conditionally re-exports enabled plugins
│   │       └── terminal/         # v1: only built-in plugin
│   │           ├── mod.rs        # Implements BackendPlugin
│   │           └── commands.rs   # #[tauri::command] fns for PTY operations
│   │
│   └── tests/
│       ├── fs_test.rs
│       ├── pty_test.rs
│       └── workspace_test.rs
│
├── src/                          # ── REACT FRONTEND ──
│   ├── main.tsx                  # ReactDOM.createRoot, mounts <App />
│   ├── App.tsx                   # Shell layout: sidebar + tab area + status bar
│   │
│   ├── core/                     # Core app shell — NO plugin imports
│   │   ├── shell/
│   │   │   ├── Sidebar.tsx       # File tree + workspace switcher
│   │   │   ├── FileTree.tsx      # Recursive tree, reads from workspace store
│   │   │   ├── TabBar.tsx        # Tab strip, delegates content to plugin registry
│   │   │   ├── TabContent.tsx    # Renders the active tab's component
│   │   │   ├── StatusBar.tsx     # Bottom bar, reads from plugin contributions
│   │   │   └── CommandPalette.tsx # Cmd+K palette, reads commands from plugin registry
│   │   │
│   │   ├── context/
│   │   │   ├── WorkspaceContext.tsx   # Open folder path, file tree, active file
│   │   │   ├── TabContext.tsx         # Open tabs, active tab, tab ordering
│   │   │   └── PluginContext.tsx      # Registered plugins and their contributions
│   │   │
│   │   └── hooks/
│   │       ├── useFileSystem.ts      # Wraps Tauri invoke for fs operations
│   │       ├── useTauriEvents.ts     # Subscribe to backend events (file changes, PTY output)
│   │       ├── useTauriStore.ts      # Read/write persistent settings
│   │       └── useWorkspace.ts       # Combines fs + events for workspace operations
│   │
│   ├── plugin-api/               # ★ THE CONTRACT — plugins import ONLY from here ★
│   │   ├── index.ts              # Barrel export of all public API
│   │   ├── types.ts              # FrontendPlugin interface, contribution types
│   │   ├── registry.ts           # registerPlugin(), getPlugins(), getTabForFile()
│   │   ├── hooks.ts              # usePluginAPI() — sandboxed access to core capabilities
│   │   └── contribution-points.ts # What plugins can contribute: TAB, SIDEBAR_PANEL, STATUS_ITEM, COMMAND
│   │
│   ├── plugins/                  # Each plugin is a self-contained folder
│   │   ├── index.ts              # Auto-discovers and registers all plugins
│   │   │
│   │   ├── code-editor/          # v1 built-in
│   │   │   ├── index.ts          # Implements FrontendPlugin, registers tab + file associations
│   │   │   ├── manifest.json     # { id, name, version, contributions }
│   │   │   ├── CodeEditorTab.tsx # CodeMirror 6 wrapper component
│   │   │   └── extensions/       # CM6 language modes, keybindings, themes
│   │   │       ├── languages.ts  # Language detection + lazy loading
│   │   │       └── keymaps.ts    # Custom keybindings
│   │   │
│   │   └── terminal/             # v1 built-in
│   │       ├── index.ts          # Implements FrontendPlugin, registers tab + panel
│   │       ├── manifest.json
│   │       ├── TerminalTab.tsx   # xterm.js wrapper, connects to PTY via Tauri events
│   │       └── theme.ts          # Terminal color scheme matching app theme
│   │
│   ├── lib/
│   │   ├── utils.ts              # General utilities
│   │   └── cn.ts                 # shadcn className merge helper (clsx + tailwind-merge)
│   │
│   └── components/               # shadcn/ui primitives (generated via CLI)
│       └── ui/
│           ├── button.tsx
│           ├── tabs.tsx
│           ├── command.tsx        # For command palette
│           ├── dialog.tsx
│           ├── scroll-area.tsx
│           ├── separator.tsx
│           ├── tooltip.tsx
│           └── resizable.tsx      # For sidebar/panel resizing
│
├── public/                       # Static assets
└── e2e/                          # WebdriverIO E2E tests
    ├── wdio.conf.ts
    └── specs/
        ├── open-folder.spec.ts
        ├── file-editing.spec.ts
        └── terminal.spec.ts
```

### Critical structural rules

1. **`src/core/` never imports from `src/plugins/`**. The dependency arrow is one-way: plugins → plugin-api → (used by) core.
2. **`src/plugins/*/` only imports from `src/plugin-api/`** and its own internal files. Never from `src/core/` directly.
3. **`src/plugin-api/`** is the bridge. It exposes hooks and types that give plugins controlled access to core capabilities without direct coupling.
4. **Each plugin folder is deletable**. Removing `src/plugins/terminal/` should cause zero TypeScript errors in core — just one less registered plugin.
5. **`src-tauri/src/core/` never imports from `src-tauri/src/plugins/`**. Same one-way rule on the Rust side.

---

## 4. Plugin architecture — detailed design

### 4.1 Frontend plugin contract

```typescript
// src/plugin-api/types.ts

import { ComponentType } from 'react';

/**
 * Every frontend plugin must implement this interface.
 * Core never imports plugin code directly — it reads contributions
 * from the registry and renders them dynamically.
 */
export interface FrontendPlugin {
  /** Unique identifier, e.g. "code-editor", "terminal", "git" */
  id: string;
  /** Human-readable name */
  name: string;
  /** Semver version string */
  version: string;

  /** What this plugin adds to the app */
  contributions: PluginContributions;

  /** Called once when the plugin is loaded. Use api to register commands, listen to events. */
  activate(api: PluginAPI): void | Promise<void>;

  /** Called when the plugin is unloaded. Clean up subscriptions, intervals, etc. */
  deactivate?(): void;
}

export interface PluginContributions {
  /** Tab types this plugin can render */
  tabs?: TabContribution[];
  /** Sidebar panels (below the file tree) */
  sidebarPanels?: SidebarPanelContribution[];
  /** Status bar items */
  statusBarItems?: StatusBarItemContribution[];
  /** Commands available in the command palette */
  commands?: CommandContribution[];
  /** File extensions this plugin handles (routes to a specific tab type) */
  fileAssociations?: FileAssociation[];
}

export interface TabContribution {
  /** Unique tab type ID, e.g. "code-editor", "terminal" */
  type: string;
  /** Display name for the tab type */
  displayName: string;
  /** Icon component for the tab header */
  icon?: ComponentType<{ className?: string }>;
  /** The React component that renders the tab content */
  component: ComponentType<TabProps>;
}

export interface TabProps {
  /** Absolute file path (null for non-file tabs like terminal) */
  filePath: string | null;
  /** Whether this tab is currently active/visible */
  isActive: boolean;
}

export interface FileAssociation {
  /** File extensions, e.g. [".ts", ".tsx", ".js"] */
  extensions: string[];
  /** Which tab type handles these files */
  tabType: string;
  /** Priority (higher wins when multiple plugins claim the same extension) */
  priority?: number;
}

export interface SidebarPanelContribution {
  id: string;
  title: string;
  icon?: ComponentType<{ className?: string }>;
  component: ComponentType;
  /** Position in sidebar. Lower numbers appear higher. */
  order?: number;
}

export interface StatusBarItemContribution {
  id: string;
  component: ComponentType;
  /** "left" or "right" alignment in the status bar */
  alignment: 'left' | 'right';
  order?: number;
}

export interface CommandContribution {
  id: string;
  /** Display name in command palette */
  title: string;
  /** Keyboard shortcut, e.g. "Ctrl+Shift+P" */
  keybinding?: string;
  /** The function to execute */
  execute: () => void | Promise<void>;
}
```

### 4.2 Plugin API (sandboxed access to core)

```typescript
// src/plugin-api/hooks.ts

/**
 * Plugins call usePluginAPI() to get controlled access to core capabilities.
 * This is the ONLY way plugins interact with the app.
 * Core internals (context values, store shape) are never exposed.
 */
export interface PluginAPI {
  fs: {
    readFile(path: string): Promise<string>;
    writeFile(path: string, content: string): Promise<void>;
    watchFile(path: string, callback: (event: FileChangeEvent) => void): () => void;
    listDir(path: string): Promise<DirEntry[]>;
  };

  workspace: {
    getWorkspacePath(): string | null;
    getOpenFiles(): string[];
    getActiveFile(): string | null;
    openFile(path: string): void;
  };

  commands: {
    register(id: string, handler: () => void | Promise<void>): void;
    execute(id: string): Promise<void>;
  };

  events: {
    on(event: string, handler: (payload: unknown) => void): () => void;
    emit(event: string, payload: unknown): void;
  };

  ui: {
    showNotification(message: string, type?: 'info' | 'warning' | 'error'): void;
    showQuickPick(items: string[]): Promise<string | null>;
  };
}
```

### 4.3 Plugin registration flow

```typescript
// src/plugins/index.ts
// This is the ONLY file that imports from plugin folders.
// It auto-registers all plugins at startup.

import { registerPlugin } from '../plugin-api/registry';
import { codeEditorPlugin } from './code-editor';
import { terminalPlugin } from './terminal';

export function loadPlugins() {
  // Built-in plugins
  registerPlugin(codeEditorPlugin);
  registerPlugin(terminalPlugin);

  // Future: dynamic loading from a plugins directory
  // const externalPlugins = await discoverPlugins('~/.tauri-ide/plugins/');
  // externalPlugins.forEach(registerPlugin);
}
```

```typescript
// src/plugin-api/registry.ts

const plugins: Map<string, FrontendPlugin> = new Map();

export function registerPlugin(plugin: FrontendPlugin): void {
  if (plugins.has(plugin.id)) {
    console.warn(`Plugin "${plugin.id}" is already registered. Skipping.`);
    return;
  }
  plugins.set(plugin.id, plugin);
}

export function getPlugins(): FrontendPlugin[] {
  return Array.from(plugins.values());
}

export function getTabComponentForFile(filePath: string): TabContribution | null {
  const ext = '.' + filePath.split('.').pop();
  let bestMatch: { contribution: TabContribution; priority: number } | null = null;

  for (const plugin of plugins.values()) {
    for (const assoc of plugin.contributions.fileAssociations ?? []) {
      if (assoc.extensions.includes(ext)) {
        const priority = assoc.priority ?? 0;
        if (!bestMatch || priority > bestMatch.priority) {
          const tab = plugin.contributions.tabs?.find(t => t.type === assoc.tabType);
          if (tab) bestMatch = { contribution: tab, priority };
        }
      }
    }
  }

  return bestMatch?.contribution ?? null;
}

export function getAllCommands(): CommandContribution[] {
  return getPlugins().flatMap(p => p.contributions.commands ?? []);
}

export function getAllStatusBarItems(): StatusBarItemContribution[] {
  return getPlugins()
    .flatMap(p => p.contributions.statusBarItems ?? [])
    .sort((a, b) => (a.order ?? 50) - (b.order ?? 50));
}

export function getAllSidebarPanels(): SidebarPanelContribution[] {
  return getPlugins()
    .flatMap(p => p.contributions.sidebarPanels ?? [])
    .sort((a, b) => (a.order ?? 50) - (b.order ?? 50));
}
```

### 4.4 Rust backend plugin contract

```rust
// src-tauri/src/plugin_host/trait_def.rs

use tauri::AppHandle;

/// Every Rust-side plugin implements this trait.
/// Core services never import plugin modules directly.
/// The registry collects plugins and wires them into the Tauri builder.
pub trait BackendPlugin: Send + Sync {
    /// Unique identifier matching the frontend plugin id
    fn id(&self) -> &str;

    /// Human-readable name
    fn name(&self) -> &str;

    /// Called once at app startup. Use app_handle to register
    /// event listeners, access the file system, spawn processes, etc.
    fn activate(&self, app_handle: &AppHandle) -> Result<(), Box<dyn std::error::Error>>;

    /// Called at app shutdown
    fn deactivate(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}
```

```rust
// src-tauri/src/plugin_host/registry.rs

use super::trait_def::BackendPlugin;
use tauri::AppHandle;

pub struct PluginRegistry {
    plugins: Vec<Box<dyn BackendPlugin>>,
}

impl PluginRegistry {
    pub fn new() -> Self {
        Self { plugins: Vec::new() }
    }

    pub fn register(&mut self, plugin: Box<dyn BackendPlugin>) {
        self.plugins.push(plugin);
    }

    pub fn activate_all(&self, app_handle: &AppHandle) {
        for plugin in &self.plugins {
            if let Err(e) = plugin.activate(app_handle) {
                eprintln!("Failed to activate plugin '{}': {}", plugin.id(), e);
            }
        }
    }
}
```

### 4.5 Example: how a plugin is implemented

```typescript
// src/plugins/code-editor/index.ts

import type { FrontendPlugin } from '../../plugin-api/types';
import { CodeEditorTab } from './CodeEditorTab';

export const codeEditorPlugin: FrontendPlugin = {
  id: 'code-editor',
  name: 'Code Editor',
  version: '1.0.0',

  contributions: {
    tabs: [
      {
        type: 'code-editor',
        displayName: 'Code Editor',
        component: CodeEditorTab,
      },
    ],
    fileAssociations: [
      {
        extensions: [
          '.ts', '.tsx', '.js', '.jsx', '.json',
          '.rs', '.toml', '.md', '.css', '.html',
          '.py', '.go', '.yaml', '.yml', '.sh',
        ],
        tabType: 'code-editor',
        priority: 0, // Low priority — other plugins can override specific extensions
      },
    ],
    commands: [
      {
        id: 'editor.formatDocument',
        title: 'Format Document',
        keybinding: 'Ctrl+Shift+F',
        execute: () => {
          // Dispatched via plugin API events
        },
      },
    ],
  },

  activate(api) {
    // Listen for file open events
    api.events.on('file:open', (payload) => {
      const { path } = payload as { path: string };
      api.workspace.openFile(path);
    });
  },
};
```

### 4.6 How core renders plugin contributions (zero coupling)

```tsx
// src/core/shell/TabContent.tsx
// Core renders whatever component the plugin registry returns.
// It never imports CodeEditorTab or TerminalTab directly.

import { getTabComponentForFile } from '../../plugin-api/registry';

export function TabContent({ tab }: { tab: OpenTab }) {
  if (tab.filePath) {
    const contribution = getTabComponentForFile(tab.filePath);
    if (!contribution) return <div>No editor available for this file type</div>;
    const Component = contribution.component;
    return <Component filePath={tab.filePath} isActive={tab.isActive} />;
  }

  // Non-file tabs (e.g. terminal) are looked up by tab type
  const contribution = getTabByType(tab.type);
  if (!contribution) return null;
  const Component = contribution.component;
  return <Component filePath={null} isActive={tab.isActive} />;
}
```

---

## 5. IPC design — Rust ↔ React communication

### 5.1 Commands (frontend → backend, request/response)

```rust
// Rust: define a command
#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}

// Register in lib.rs
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![read_file])
```

```typescript
// Frontend: call the command
import { invoke } from '@tauri-apps/api/core';

const content = await invoke<string>('read_file', { path: '/some/file.ts' });
```

### 5.2 Events (backend → frontend, streaming/push)

Used for PTY output, file system watcher notifications, and long-running operations.

```rust
// Rust: emit an event
app_handle.emit("pty:output", payload)?;
```

```typescript
// Frontend: listen to the event
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<string>('pty:output', (event) => {
  terminal.write(event.payload);
});
```

### 5.3 Naming conventions

All IPC commands and events follow a namespaced pattern:

| Pattern | Examples |
|---|---|
| Commands: `{domain}_{action}` | `fs_read_file`, `fs_write_file`, `fs_list_dir`, `pty_spawn`, `pty_write`, `workspace_open_folder` |
| Events: `{domain}:{action}` | `pty:output`, `pty:exit`, `fs:changed`, `workspace:switched` |

---

## 6. State management

### 6.1 Ephemeral UI state — React Context

Three focused contexts, each with its own reducer:

**WorkspaceContext**: Current workspace path, file tree data, active file.
**TabContext**: Open tabs array, active tab ID, tab order.
**PluginContext**: Registered plugins, resolved contributions.

Each context has a small, predictable shape. If any context grows beyond ~10 fields, that is a signal to split it or push state into a plugin.

### 6.2 Persistent state — Tauri Store

```typescript
import { Store } from '@tauri-apps/plugin-store';

const store = await Store.load('settings.json');

// Write
await store.set('recentWorkspaces', ['/path/one', '/path/two']);
await store.save();

// Read
const recent = await store.get<string[]>('recentWorkspaces');
```

Persisted data includes: recent workspaces, sidebar width, last open files per workspace, terminal shell preference, editor font size.

### 6.3 What goes where

| Data | Location | Why |
|---|---|---|
| Open tabs, active tab | TabContext | Ephemeral, changes constantly |
| File tree contents | WorkspaceContext | Rebuilt on folder open, not persisted |
| Sidebar collapsed/width | Tauri Store | User preference, survives restart |
| Recent workspaces | Tauri Store | Survives restart |
| Registered plugins | PluginContext | Built at startup from loaded plugins |
| Terminal scroll buffer | xterm.js internal | Managed by xterm, not our state |
| Editor content | CodeMirror internal | CM6 manages its own document state |

---

## 7. Key integration details

### 7.1 CodeMirror 6

```tsx
// src/plugins/code-editor/CodeEditorTab.tsx

import { EditorView, basicSetup } from 'codemirror';
import { useEffect, useRef } from 'react';
import { usePluginAPI } from '../../plugin-api/hooks';

export function CodeEditorTab({ filePath, isActive }: TabProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView | null>(null);
  const api = usePluginAPI();

  useEffect(() => {
    if (!containerRef.current || !filePath) return;

    api.fs.readFile(filePath).then((content) => {
      const view = new EditorView({
        doc: content,
        extensions: [
          basicSetup,
          // Language detection based on file extension
          // Theme matching the app
          // Save on Ctrl+S via keybinding
        ],
        parent: containerRef.current!,
      });
      viewRef.current = view;
    });

    return () => {
      viewRef.current?.destroy();
    };
  }, [filePath]);

  return <div ref={containerRef} className="h-full w-full" />;
}
```

Important CM6 decisions:
- Use `basicSetup` as a starting point, then customize by adding/removing extensions.
- Language modes are lazy-loaded — only import the language grammar when a file of that type is opened.
- CM6 manages its own undo history and document state. Do not mirror document content in React state.
- Save operations go through the plugin API: `api.fs.writeFile(filePath, view.state.doc.toString())`.

### 7.2 xterm.js + PTY

The terminal has two halves — xterm.js in the frontend renders the terminal UI, and a Rust PTY manager on the backend spawns and manages the actual shell process.

```
[xterm.js]  ──user keystrokes──→  [Tauri IPC]  ──→  [Rust PTY stdin]
[xterm.js]  ←──pty:output event──  [Tauri IPC]  ←──  [Rust PTY stdout]
```

On the Rust side, use the `portable-pty` crate to spawn a shell:

```rust
// src-tauri/src/core/pty.rs (simplified)

use portable_pty::{CommandBuilder, PtySize, native_pty_system};

pub fn spawn_shell() -> Result<(Box<dyn MasterPty>, Box<dyn Child>), Error> {
    let pty_system = native_pty_system();
    let pair = pty_system.openpty(PtySize {
        rows: 24,
        cols: 80,
        pixel_width: 0,
        pixel_height: 0,
    })?;

    let cmd = CommandBuilder::new_default_prog();
    let child = pair.slave.spawn_command(cmd)?;

    Ok((pair.master, child))
}
```

Critical rules:
- Each terminal tab gets its own PTY process.
- PTY output is streamed to the frontend via Tauri events, not IPC commands (events are non-blocking push).
- Terminal resize events (when the panel resizes) must call `pty.resize()` on the Rust side AND `terminal.resize()` on xterm.js.
- On tab close, kill the PTY child process.

### 7.3 File tree

The sidebar file tree is populated by a Rust command that reads the directory structure:

```rust
#[tauri::command]
async fn list_dir(path: String) -> Result<Vec<DirEntry>, String> {
    // Returns { name, path, is_dir, is_file } entries
    // Sorted: directories first, then files, both alphabetical
}
```

The tree is lazily expanded — only the children of expanded directories are loaded. Use Tauri's file system watcher to listen for changes and update the tree.

---

## 8. Patterns to follow

### 8.1 One-way dependency rule

```
src/core/  ←───reads from───  src/plugin-api/  ←───imports───  src/plugins/
    │                              │
    │  NEVER imports from          │  NEVER imports from
    │  src/plugins/                │  src/core/
    ▼                              ▼
```

Core reads contribution data from the plugin registry (via plugin-api). Plugins register themselves with the registry (via plugin-api). Neither side reaches into the other.

### 8.2 Plugin manifest pattern

Every plugin folder contains a `manifest.json`:

```json
{
  "id": "code-editor",
  "name": "Code Editor",
  "version": "1.0.0",
  "description": "CodeMirror 6 based code editor",
  "contributions": {
    "tabs": ["code-editor"],
    "fileAssociations": {
      ".ts": "code-editor",
      ".js": "code-editor"
    }
  }
}
```

This is declarative metadata. The `index.ts` reads it and constructs the `FrontendPlugin` object. This separation means you can statically analyze plugin capabilities without loading their code.

### 8.3 Command naming

All commands follow `{pluginId}.{action}` naming:

```
editor.formatDocument
editor.goToLine
terminal.new
terminal.split
workspace.openFolder
workspace.switchWorkspace
```

### 8.4 Lean components

Tab components (CodeEditorTab, TerminalTab) are thin wrappers. They mount the third-party library into a div ref, wire up IPC, and that's it. Business logic lives in hooks or the plugin's own utilities — not in JSX.

---

## 9. Anti-patterns to avoid

### 9.1 Do NOT import plugin code in core

```typescript
// ❌ WRONG — core is now coupled to the terminal plugin
import { TerminalTab } from '../plugins/terminal/TerminalTab';

// ✅ RIGHT — core reads from the registry
const tabContribution = getTabByType('terminal');
const Component = tabContribution.component;
```

### 9.2 Do NOT mirror editor state in React

```typescript
// ❌ WRONG — fighting CM6's own state management
const [content, setContent] = useState('');
// ...syncing content back and forth with CM6

// ✅ RIGHT — let CM6 own its document, read it only when saving
const content = viewRef.current.state.doc.toString();
await api.fs.writeFile(filePath, content);
```

Same applies to xterm.js — do not mirror the terminal buffer in React state.

### 9.3 Do NOT use IPC for high-frequency data

```typescript
// ❌ WRONG — invoking a command for every PTY byte
const output = await invoke('pty_read'); // polling

// ✅ RIGHT — use events for streaming data
listen('pty:output', (event) => terminal.write(event.payload));
```

### 9.4 Do NOT create god contexts

```typescript
// ❌ WRONG — one context for everything
const AppContext = createContext({
  workspace: ...,
  tabs: ...,
  plugins: ...,
  theme: ...,
  settings: ...,
  terminal: ...,
});

// ✅ RIGHT — separate contexts by concern
// WorkspaceContext, TabContext, PluginContext
// Each has its own provider and reducer
```

### 9.5 Do NOT use Tauri Store for ephemeral state

```typescript
// ❌ WRONG — persisting the active tab (it's ephemeral UI state)
await store.set('activeTab', tabId);

// ✅ RIGHT — active tab lives in TabContext
dispatch({ type: 'SET_ACTIVE_TAB', tabId });
```

### 9.6 Do NOT block the Rust main thread

```rust
// ❌ WRONG — blocking read in a Tauri command
#[tauri::command]
fn read_file(path: String) -> String {
    std::fs::read_to_string(&path).unwrap()
}

// ✅ RIGHT — async command
#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    tokio::fs::read_to_string(&path).await.map_err(|e| e.to_string())
}
```

### 9.7 Do NOT hardcode file type routing

```typescript
// ❌ WRONG — switch statement in core that knows about file types
switch (ext) {
  case '.md': return <MarkdownTab />;
  case '.ts': return <CodeEditorTab />;
}

// ✅ RIGHT — ask the registry
const contribution = getTabComponentForFile(filePath);
const Component = contribution.component;
return <Component {...props} />;
```

---

## 10. Testing strategy

### 10.1 Rust unit tests

Test core services in isolation. Mock the file system and PTY where needed.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_workspace_tracks_recent() {
        let mut ws = WorkspaceState::new();
        ws.open("/path/one");
        ws.open("/path/two");
        assert_eq!(ws.recent(), vec!["/path/two", "/path/one"]);
    }

    #[test]
    fn test_plugin_registry_rejects_duplicates() {
        let mut registry = PluginRegistry::new();
        registry.register(Box::new(FakePlugin::new("test")));
        registry.register(Box::new(FakePlugin::new("test"))); // should warn, not panic
        assert_eq!(registry.count(), 1);
    }
}
```

### 10.2 Frontend unit tests (Vitest)

Test the plugin registry, file association resolution, and context reducers.

```typescript
// src/plugin-api/__tests__/registry.test.ts
import { describe, it, expect } from 'vitest';
import { registerPlugin, getTabComponentForFile } from '../registry';

describe('plugin registry', () => {
  it('resolves file associations by priority', () => {
    registerPlugin(codeEditorPlugin);  // .md at priority 0
    registerPlugin(markdownPlugin);     // .md at priority 10

    const tab = getTabComponentForFile('readme.md');
    expect(tab?.type).toBe('markdown'); // higher priority wins
  });
});
```

### 10.3 Component tests (Vitest + React Testing Library)

```typescript
// Mock Tauri's invoke
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}));
```

### 10.4 E2E smoke tests (WebdriverIO)

Keep to 5-10 critical paths:

1. App launches, window appears
2. Open folder → file tree populates
3. Click file → editor tab opens with content
4. Edit file → save → re-open → changes persisted
5. Open terminal → type command → see output
6. Switch workspace → file tree updates
7. Command palette opens and lists commands

---

## 11. Build and run commands

```bash
# Install dependencies
pnpm install

# Development (runs Vite dev server + Tauri in parallel)
pnpm tauri dev

# Run frontend tests
pnpm vitest

# Run Rust tests
cd src-tauri && cargo test

# Build production app
pnpm tauri build

# Add a shadcn/ui component
pnpm dlx shadcn@latest add button
```

---

## 12. Future plugin roadmap (not v1)

These are designed as plugins that slot into the existing architecture with zero core changes:

| Plugin | Type | What it contributes |
|---|---|---|
| Milkdown/Crepe | Frontend | Tab for `.md` files (WYSIWYG), overrides code-editor's .md association at higher priority |
| Git | Frontend + Backend | Sidebar panel (changed files), status bar item (branch name), commands (commit, push, pull) |
| LSP client | Backend | Diagnostics, completions, go-to-definition. Communicates with CM6 via events. |
| AI copilot | Frontend + Backend | Inline completions in CM6, chat sidebar panel |
| Theme | Frontend | Custom CM6 theme + xterm.js colors + Tailwind CSS variables |
| File search | Frontend + Backend | Cmd+P file finder, Cmd+Shift+F text search across workspace |
| Snippets | Frontend | Custom snippet expansion in CM6 |

Each one follows the same pattern: create a folder in `src/plugins/`, implement `FrontendPlugin`, optionally implement `BackendPlugin` in Rust, register at startup.

---

## 13. Key dependencies with install commands

```bash
# Frontend
pnpm add react react-dom
pnpm add -D @types/react @types/react-dom typescript
pnpm add -D vite @vitejs/plugin-react
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D tailwindcss @tailwindcss/vite
pnpm add codemirror @codemirror/lang-javascript @codemirror/lang-python @codemirror/lang-rust @codemirror/lang-html @codemirror/lang-css @codemirror/lang-json @codemirror/lang-markdown
pnpm add @xterm/xterm @xterm/addon-fit @xterm/addon-webgl
pnpm add @tauri-apps/api @tauri-apps/plugin-store

# Tauri CLI
pnpm add -D @tauri-apps/cli

# Rust (in Cargo.toml)
# tauri = { version = "2", features = ["devtools"] }
# tauri-plugin-store = "2"
# portable-pty = "0.8"
# serde = { version = "1", features = ["derive"] }
# serde_json = "1"
# tokio = { version = "1", features = ["full"] }
# notify = "7"  # file system watcher
```

---

## 14. Scaffolding order

When implementing, build in this order:

1. **Scaffold Tauri + Vite + React** — `pnpm create tauri-app` with React template, then upgrade to Vite 8
2. **Plugin API types and registry** — `src/plugin-api/` with types, registry, contribution points
3. **App shell** — Sidebar, TabBar, TabContent, StatusBar reading from PluginContext
4. **Code editor plugin** — CM6 wrapper, file association for all types, basic save
5. **Rust core services** — `fs.rs` (read/write/list/watch), `workspace.rs` (open folder, recent)
6. **File tree** — Sidebar file tree connected to Rust fs commands
7. **Terminal plugin** — xterm.js wrapper + Rust PTY via `portable-pty`
8. **Persistent state** — Tauri Store for recent workspaces, sidebar width, preferences
9. **Command palette** — reads commands from plugin registry
10. **Testing** — unit tests for registry + Rust core, component tests, 5 E2E smoke tests
