# Libraries & MCPs

## Architecture

This stack uses **Ports & Adapters** (Hexagonal Architecture):

```
UI (components/pages)
  → Port (layers/{domain}/ports/)
  → Adapter (layers/{domain}/adapters/)
  → External world (Instforge, Anthropic API, etc.)
```

Every external dependency has:
- A **port** — a TypeScript interface in `layers/{domain}/ports/` (e.g., `TaskPort.ts`)
- A **fake adapter** — in-memory, always present (`layers/{domain}/adapters/FakeTaskAdapter.ts`)
- A **real adapter** — swapped in when needed (`layers/{domain}/adapters/InstforgeTaskAdapter.ts`)

Reference: PRINCIPLES.md (non-negotiable)

## Required MCPs

- **insforge**: Backend as a service — accessed only through ports and adapters, never directly

## Production Dependencies

| Package | Purpose |
|---------|---------|
| @nuxt/ui | Component library |
| @pinia/nuxt | Cross-layer shared state (auth, user profile) |
| nuxt | Framework |

## Adapter Dependencies (swappable)

| Adapter | Concern | Fake adapter | Real adapter |
|---------|---------|-------------|--------------|
| `layers/{domain}/adapters/` | All external deps during skeleton | `FakeXxxAdapter.ts` (permanent) | `InstforgeXxxAdapter.ts` (deferred) |

## Development Dependencies

| Package | Purpose |
|---------|---------|
| playwright | E2E testing |
| fast-check | Property-based testing |
| zod | Runtime validation (user input, server route bodies) |

**Note:** All non-E2E tests run on `bun test` — no vitest needed. Bun's built-in test runner handles unit, integration, invariant, property-based, regression, and architecture tests.

**Note:** Fake adapters serve as integration test fixtures — they stay permanently and are NOT replaced by MSW or other network-level mocks.

## Adding New Dependencies

Before adding ANY dependency:
1. Does it need a port? (almost always yes)
2. Does it need a fake adapter first? (yes, unless it's pure UI)
3. Research the library — does it fit the adapter pattern?
4. Explain to the user why it's the best choice
5. Get explicit permission before installing
