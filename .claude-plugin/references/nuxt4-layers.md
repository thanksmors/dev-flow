# Nuxt 4 Layers — dev-flow Reference

## How Nuxt 4 Layers Work

Nuxt 4 layers are extended via `nuxt.config.ts` `extends` array. Each layer
contributes: auto-imports, layouts, pages, server routes, and composables.

## Critical Rules for dev-flow

### Server Routes — Where They Go

Server routes for a feature belong in `server/api/` at the **project root**.
They do NOT go in `layers/features/{feature}/server/api/`.

**Reason:** Nuxt layer aliases (e.g. `#app/diComposition`, `~/shared/schemas`)
resolve from the project root, not from within a layer directory. Files in
`layers/features/*/server/` are NOT auto-registered by Nuxt.

### Composables — Where They Go

Composables used by the feature belong in `composables/` or `shared/composables/`
at the project root. They are NOT auto-imported from `layers/features/*/app/`.
If a composable lives inside a layer, it must be explicitly imported.

### DI Composition

- The composition root is at `app/diComposition.ts` at the project root.
- Layer aliases (`#app/diComposition`) are configured in `nuxt.config.ts`.
- Adapters are wired in `app/diComposition.ts` using `bind()`.
- Port interfaces live at `layers/{domain}/ports/XyzPort.ts`.

### Folder Structure (Canonical)

```
project/
├── app/
│   └── diComposition.ts       # DI composition root
├── layers/
│   └── {domain}/
│       ├── ports/            # Port interfaces
│       ├── adapters/          # Fake + real adapters
│       ├── domain/            # Domain logic
│       └── app/               # Composables (explicit import only)
├── server/
│   └── api/                   # Server routes (at project root)
├── composables/               # Composable auto-imports
└── nuxt.config.ts             # Extends layers
```

### Walking Skeleton Pattern

1. Create the DI composition root at `app/diComposition.ts`
2. Wire an InMemory fake adapter first
3. Create server routes in `server/api/`
4. Verify end-to-end works before adding real adapters
5. Swap adapter in `app/diComposition.ts` when ready
