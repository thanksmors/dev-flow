# Libraries & MCPs

## Architecture
Same ports-and-adapters pattern as default.

## Required MCPs
- **insforge**: Backend as a service

## Production Dependencies

| Package | Purpose |
|---------|---------|
| @nuxt/ui | Component library |
| @pinia/nuxt | Cross-layer shared state |
| nuxt | Framework |
| fastify | CPU-intensive API work |

## Development Dependencies

| Package | Purpose |
|---------|---------|
| playwright | E2E testing |
| fast-check | Property-based testing |
| zod | Runtime validation |

## Adapter Dependencies
Same pattern as default — fake adapters always present before real adapters.
For Fastify: fake adapter in `server/plugins/{domain}/fakes/`.
