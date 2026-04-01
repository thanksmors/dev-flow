# Tech Stack

## Package Manager
bun

## Backend
nuxt (server routes) + fastify
# Fastify for CPU-intensive or complex API work that doesn't fit Nuxt server routes.
# Use Nuxt server routes for simple CRUD. Graduate to Fastify when needed.

## Frontend
nuxt@^4.0.0

## UI Components
@nuxt/ui

## Architecture Pattern
vertical-slices + ports-and-adapters
# Nuxt layers for frontend domains. Fastify plugins for backend domains.
# Each domain is self-contained with its own tests.

## State Management
pinia (via @pinia/nuxt) + nuxt built-ins
# Pinia: cross-layer shared state (auth, user, cart, global prefs)
# useAsyncData/useFetch: server-fetched data local to a page

## TypeScript
strict: true always

## Agent-First Design
agentTriggered: true

## Layer Boundary Rule
# Same as default: layers/{domain}/ports/ + adapters/ per domain.
# Fastify domains live in server/plugins/ with co-located tests.
