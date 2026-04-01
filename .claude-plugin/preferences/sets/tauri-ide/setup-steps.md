# Project Scaffolding

## Step 1: Scaffold Tauri + React app

pnpm create tauri-app tauri-ide --template react-ts --manager pnpm
cd tauri-ide

## Step 2: Upgrade to Vite 8 (Rolldown-powered)

pnpm add -D vite@^8.0.0 @vitejs/plugin-react@latest

Update vite.config.ts:
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindCSS from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindCSS()],
});
```

## Step 3: Install frontend dependencies

pnpm add react react-dom
pnpm add @tauri-apps/api @tauri-apps/plugin-store
pnpm add codemirror @codemirror/lang-javascript @codemirror/lang-rust @codemirror/lang-html @codemirror/lang-css @codemirror/lang-json @codemirror/lang-markdown
pnpm add @xterm/xterm @xterm/addon-fit @xterm/addon-webgl
pnpm add clsx tailwind-merge
pnpm add -D @types/react @types/react-dom typescript vitest @testing-library/react @testing-library/jest-dom

## Step 4: Install shadcn/ui

pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button tabs dialog scroll-area separator tooltip resizable command

## Step 5: Create plugin API structure

mkdir -p src/plugin-api src/core/context src/core/shell src/core/hooks src/plugins/code-editor src/plugins/terminal

Create src/plugin-api/types.ts — define FrontendPlugin, PluginContributions, TabContribution, PluginAPI interfaces.

Create src/plugin-api/registry.ts — implement registerPlugin(), getPlugins(), getTabComponentForFile().

Create src/plugin-api/hooks.ts — implement usePluginAPI() hook.

## Step 6: Scaffold app shell

Create src/core/shell/Sidebar.tsx, FileTree.tsx, TabBar.tsx, TabContent.tsx, StatusBar.tsx, CommandPalette.tsx.

Create src/core/context/WorkspaceContext.tsx, TabContext.tsx, PluginContext.tsx.

Wire PluginContext into shell components — shell reads from registry, never imports plugin code.

## Step 7: Scaffold code-editor plugin

Create src/plugins/code-editor/index.ts — implement FrontendPlugin, register .ts, .tsx, .rs, .md, etc. file associations.

Create src/plugins/code-editor/CodeEditorTab.tsx — CM6 wrapper, mount via EditorView in useEffect.

## Step 8: Scaffold Rust backend services

mkdir -p src-tauri/src/core src-tauri/src/plugin_host src-tauri/src/plugins/terminal src-tauri/tests

Create src-tauri/src/core/fs.rs — read_file, write_file, list_dir, watch_file commands.

Create src-tauri/src/core/workspace.rs — open_folder, recent_workspaces state.

Create src-tauri/src/core/pty.rs — spawn_shell via portable-pty, stream output via events.

Create src-tauri/src/plugin_host/trait_def.rs — BackendPlugin trait.

Create src-tauri/src/plugin_host/registry.rs — PluginRegistry::activate_all().

## Step 9: Verify the shell walks

Run pnpm tauri dev — confirm window opens, sidebar shows, no console errors.
