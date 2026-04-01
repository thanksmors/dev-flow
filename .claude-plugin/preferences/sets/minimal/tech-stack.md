# Tech Stack

## Package Manager
bun

## Backend
none
# Minimal project — no backend yet. Add Fastify or similar when needed.

## Frontend
nuxt@^4.0.0
# No layer architecture for minimal — single-app Nuxt until boundaries emerge.

## UI Components
none
# No UI component library. Use native HTML elements or add @nuxt/ui later.

## Architecture Pattern
single-app → vertical-slices-on-demand
# Start simple. Add layers/ports-adapters only when you have 3+ related domains.

## State Management
nuxt built-ins (useAsyncData/useFetch)
# Only add Pinia when you have genuine cross-page shared state.

## TypeScript
strict: true always

## Layer Boundary Rule
# For minimal: all code lives in `server/` and `pages/` until there is a reason to split.
# Create a layer only when 3+ pages/features share the same domain concept.
