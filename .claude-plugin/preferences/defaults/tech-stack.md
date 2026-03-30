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

# Port & Adapter boundaries (within each layer):
layers/{domain}/
  layers/{domain}/ports/   ← port interfaces (never touch external world directly)
  adapters/            ← adapters (fake/ and real/ subdirs)
    fake/              ← in-memory, always present, never deleted
    {provider}/        ← real adapters, swapped in one at a time
  types/               ← domain types, imported by ports and adapters
