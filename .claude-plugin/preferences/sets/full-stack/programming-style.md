# Programming Style

## Core Philosophy
KISS first. If it's simple enough to not need abstraction, don't abstract it.
Rule of three: only extract a helper when the same logic appears 3+ times.

## Progressive Building Techniques
Apply these in order — they are not optional:

### Walking Skeleton
Build the thinnest possible end-to-end path first. One request flows from
the UI through a Nuxt layer → server route → Insforge → back to UI.
Nothing fancy. Just prove the skeleton works before adding flesh.
Reference: ${CLAUDE_PLUGIN_ROOT}/references/walking-skeleton.md

### Elephant Carpaccio
Slice features into the thinnest possible vertical slices. Each slice:
- Is deployable on its own
- Delivers real (if minimal) value
- Has its own tests
Reference: ${CLAUDE_PLUGIN_ROOT}/references/elephant-carpaccio.md

### Tracer Bullet
For unknown territory, fire a tracer bullet — the simplest possible
implementation of an uncertain path — before committing to it.

# ${CLAUDE_PLUGIN_ROOT} resolves to the devloop plugin directory.
# If reading this file from a project's .dev-flow/preferences/ copy,
# find these references in the plugin's own references/ folder.

## Architecture Principles

### Clean Architecture
- Business logic lives in composables/services inside each layer
- UI components know nothing about data fetching mechanics
- Server routes are thin — they delegate to services

### Hexagonal Architecture (Ports & Adapters — simplified)
Apply the principle without the boilerplate:
- Depend on abstractions, not concretions
- Insforge MCP IS the adapter layer — do not wrap it with custom interfaces
- Nuxt built-ins (useFetch, useAsyncData) ARE the port interfaces — use them directly
- Only introduce a custom abstraction when you have 3+ callers with shared behavior

### Evolutionary Architecture
- Defer architectural decisions until the last responsible moment
- Start simple (one Nuxt layer) and split when boundaries become clear
- Never prematurely extract a new layer for hypothetical future use

### Dependency Inversion
- Higher-level layers (UI, pages) depend on composables, not on Insforge directly
- Composables depend on Insforge via its MCP — no custom adapters needed
- If swapping Insforge became necessary, the change surface is composables only

### Layer Scaffold
When creating a new layer, follow the canonical structure and file templates in:
${CLAUDE_PLUGIN_ROOT}/references/layer-scaffold.md

### Auth Pattern (Insforge)
- `useCurrentUser()` composable in `layers/core` wraps Insforge auth — never call Insforge auth MCP directly from a page
- Protected routes use a Nuxt middleware in `layers/core/middleware/auth.ts`
- User/session state lives in a Pinia store (`layers/core/stores/auth.ts`) — it IS cross-layer shared state
- All other layers import `useCurrentUser()` from core, never from Insforge directly

### Error Handling
- Server routes: return typed `{ data, error }` objects — never throw unhandled exceptions
- `useAsyncData` / `useFetch`: always destructure `{ data, error, pending }` and handle all three states in the UI
- Components: use `<NuxtErrorBoundary>` at page level for fatal errors; use toast notifications for inline/recoverable errors
- Never swallow errors silently — at minimum log them

## What NOT to Do
- Do not create utility files "for future use"
- Do not add configuration flags for behaviour that only has one current variant
- Do not add error handling for errors that cannot happen
- Do not mock Insforge unless testing logic that is genuinely independent of it
