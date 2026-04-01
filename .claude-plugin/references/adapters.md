# Ports & Adapters — dev-flow Reference

## Pattern Overview

Every external dependency (API, database, auth, queue, observability) gets:
1. A **port interface** — the contract
2. A **fake adapter** — permanent test fixture
3. A **real adapter** — the production implementation
4. One **DI binding** in `app/diComposition.ts`

## Directory Convention

```
layers/{domain}/
├── ports/
│   └── XyzPort.ts          # Interface (the contract)
└── adapters/
    ├── FakeXyzAdapter.ts   # Permanent fake (never delete)
    └── XyzAdapter.ts       # Real implementation (deferred)
```

## Fake Adapter Rules

- **Fake adapters are PERMANENT.** Do not delete when real adapters are added.
- Fake adapters must walk end-to-end: they return realistic data that passes real validation.
- A fake adapter that throws "fake data" is not a walking fake. Build it properly.
- Fake adapters are used by tests and by the walking skeleton before real adapters exist.

## Discovery Step (Phase 3)

Before Phase 6, scan for all ports and their fakes:
- Ports without fakes: note as "fake needed before external dep"
- Fakes without ports: note as "orphan fake, create port"

## DI Binding Pattern

In `app/diComposition.ts`:
```typescript
// Swap by changing this line:
container.bind(TodoRepository).to(InMemoryTodoRepository)  // fake
// to:
container.bind(TodoRepository).to(InsforgeTodoRepository)  // real
```

## When to Build a Fake

Build a fake BEFORE touching any real adapter. The sequence is:
1. Define port interface
2. Build and verify fake adapter end-to-end
3. Only then build real adapter
