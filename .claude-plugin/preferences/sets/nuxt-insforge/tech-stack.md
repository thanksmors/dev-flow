# Tech Stack

## Package Manager
bun

## Backend
insforge
# AI-first backend as a service: postgres, auth, storage, edge functions,
# realtime, vector search. Integrates via MCP.
# https://insforge.dev

## Frontend
nuxt@^4.0.0
# Architecture: layers — each layer is a vertical slice / mini-app
# Every folder in layers/ is a self-contained domain with its own
# pages, components, composables, stores, server routes, and tests.

## UI Components
@nuxt/ui

## Architecture Pattern
vertical-slices + ports-and-adapters
# Each Nuxt layer = one business domain, fully self-contained.
# Layers map to business domains, not technical concerns.

Each external dependency within a layer goes through:
  layers/{domain}/ports/{Domain}Port.ts  (the port — defines the interface)
  layers/{domain}/adapters/Fake{Domain}Adapter.ts  (always present, in-memory)
  adapters/{provider}/{provider}Adapter.ts (swapped in one at a time)

## State Management
pinia (via @pinia/nuxt)
# Required if using stores/ in layers. Nuxt 3 auto-imports Pinia stores.
# Add to dependencies: bun add @pinia/nuxt

### Decision Rules — when to use which state mechanism
# Server data (async, fetched from Insforge) → useAsyncData / useFetch
#   Do NOT put server-fetched data in Pinia unless caching across navigations
# Cross-layer shared state (auth, user profile, cart, global prefs) → Pinia store
# UI state local to a component or composable → composable-local ref/computed
# Rule: if only one component needs it, it's not Pinia state

## TypeScript
strict: true always
# zod: required for all user input validation and server route request body parsing
# Layer boundary types: define explicit interfaces for what each layer exports
# Never use `any` — use `unknown` and narrow it

## Agent-First Design
agentTriggered: true
# Every type that represents a workflow/task/event includes an agentTriggered: boolean field
# Ports work identically for human-initiated and agent-initiated calls
# No special backdoors for agents — same ports as the UI

## Layer Boundary Rule
# A Nuxt layer = one bounded domain. A slice = one feature increment within a domain.
#
# When adding a feature:
#   1. Identify which domain it belongs to (what entities does it operate on?)
#   2. If that domain has an existing layer → add the slice there
#   3. If no existing layer matches → create a new one for that domain
#
# Create a new layer ONLY when:
#   - The feature operates on entirely different entities with no shared state
#   - It would naturally have zero imports from any existing layer
#   - The domain name is clearly distinct
#
# Shared infrastructure (uploads, notifications, audit logs) stays inside the first
# domain that needs it. Graduate to its own layer only when 3+ domains depend on it.
#
# Default: add to an existing layer. Split only when it hurts to keep them together.
#
# Cross-layer composable sharing:
# If two layers need the same composable, duplicate it.
# Move to core/ only when a third layer needs it. Duplication is intentional here.

# App Shell & Layouts

## `app.vue` — minimal
Keep it minimal. All logic lives in composables and layers.

```vue
<!-- app.vue -->
<template>
  <NuxtErrorBoundary>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </NuxtErrorBoundary>
</template>
```

## Layouts directory

```
app/
  layouts/
    default.vue   ← app shell: nav, sidebar, footer, main content slot
    auth.vue      ← centered card, no nav (login, register, password reset)
    blank.vue     ← minimal — no nav, no sidebar (public landing, popups)
```

Layouts live in `app/layouts/` (top-level, app-wide). They are **cross-domain** — shared shells used by pages across multiple domains. Do NOT put layouts inside individual domain layers.

Each layout is a standard Nuxt layout wrapping `<slot />` with `<NuxtPage />` content.

## Layouts vs Domain Pages

| Concern | Location |
|---------|----------|
| Shell (nav, sidebar, footer) | `app/layouts/default.vue` |
| Auth shell (centered card) | `app/layouts/auth.vue` |
| Public/minimal shell | `app/layouts/blank.vue` |
| Route pages | `layers/{domain}/pages/` |
| Domain components | `layers/{domain}/components/` |
| Business logic | `layers/{domain}/composables/` |

## Using layouts

Set layout per-page with `definePageMeta`:

```vue
<!-- layers/auth/pages/login.vue -->
<script setup>
definePageMeta({ layout: 'auth' })
</script>

<!-- layers/orders/pages/index.vue -->
<script setup>
definePageMeta({ layout: 'default' })
</script>
```

## Nested pages

Nested routes work identically to standard Nuxt — no special config. A parent page's layout automatically wraps child pages.

```
layers/orders/pages/
  index.vue           ← /orders — parent layout wraps this
  [id].vue            ← /orders/:id — same parent layout
```

The parent `index.vue` uses `<NuxtPage />` to render child routes within its own layout slot.

## Global middleware

Global middleware (rate limiting, security headers) lives in `app/middleware/`. Domain-specific auth/permission middleware lives in `layers/{domain}/middleware/`.

# Port & Adapter boundaries (within each layer):
layers/{domain}/
  layers/{domain}/ports/   ← port interfaces (never touch external world directly)
  adapters/            ← adapters (fake/ and real/ subdirs)
    fake/              ← in-memory, always present, never deleted
    {provider}/        ← real adapters, swapped in one at a time
  types/               ← domain types, imported by ports and adapters

## Guardrails Enforced (nuxt-insforge)

These rules are enforced during Phase 6 for the nuxt-insforge preference set.

### Page Directory Rule (G2)

Pages must live in `layers/{domain}/pages/` for their domain.

Nuxt auto-discovers pages from `layers/{domain}/pages/` directories. Pages placed outside these paths are silently ignored — no error, just a blank screen. The agent verifies this after every page-creating task.

**Wrong:** `layers/links/pages/index.vue`
**Correct:** `layers/links/pages/index.vue` (if the layer is named `links`)

### U* Component Usage Rule (G3)

When `@nuxt/ui` is installed, all form elements must use `U*` components.

Raw HTML form elements (`<input>`, `<button>`, `<form>`, `<select>`, `<textarea>`) are forbidden in `.vue` files. Use the Nuxt UI equivalents: `<UInput>`, `<UButton>`, `<UForm>`, `<USelect>`, `<UTextarea>`.

ESLint rule: `.claude-plugin/rules/no-raw-form-elements.js`

The rule is active when `@nuxt/ui` is in `package.json`. It does not flag elements inside `<client-only>` or `<template #fallback>`.
