# Layer Scaffold

Canonical structure and file templates for Nuxt Layers architecture.
**This is the single source of truth for folder structure.** All other docs (CQRS, FSD) reference this.

---

## Directory Structure

```
layers/{domain}/
  ports/                # Port interfaces — layer's public contract (at boundary)
  types/               # Domain types — Order, LineItem, UserId (not API wrappers)
  composables/          # Feature composables — use cases, business logic, API calls
    api/               # API client code — HTTP calls, request/response types (client-side)
  adapters/            # Adapter implementations — real integrations (API, DB, external)
  components/          # Entity Vue components — domain objects rendered as UI
  widgets/             # Composite UI components — assembled from entities/features
  pages/               # Route-bound views — thin, delegate to composables
  middleware/          # Domain auth and permission checks (who can access this domain's resources)
  server/
    api/
      {resource}/
        index.get.ts  # GET handler (thin — delegates to composable)
        index.post.ts # POST handler (thin — validates, delegates)
  stores/              # Pinia — cross-layer shared state only
  tests/
    unit/
    properties/
    regression/
    components/
    integration/
  index.ts            # PUBLIC API — re-exports only what this layer exposes
  nuxt.config.ts       # Layer config — minimal (see Rules below)

layers/base/          # Shared layer — UI primitives, utilities, types
  components/         # Base UI components (BaseButton, BaseModal, etc.)
  utils/              # Pure utility functions
  types/              # Shared TypeScript types and interfaces

app/                   # Application entry point and composition root
  diComposition.ts    # All port → adapter bindings (single source of truth)
  plugins/            # Nuxt plugins
  middleware/         # Global middleware ONLY (rate limit, global headers)
                        # Domain permissions → layers/{domain}/middleware/
```

Project-root directories:
```
tests/
  e2e/
  fixtures/
    fakes/
  architecture/
```

---

## Design Decision: Domain-Isolated Server Routes

### The Choice

Server routes (HTTP handlers) live **inside each domain layer**, not at the project root:

```
layers/orders/server/api/orders/index.get.ts   ← domain-isolated
layers/auth/server/api/sessions/index.post.ts  ← domain-isolated
```

Not at the Nuxt standard location:
```
server/api/orders/index.get.ts     ← NOT this (Nuxt standard)
server/api/sessions/index.post.ts ← NOT this
```

### Justification

This is **domain-isolated architecture** (modular monolith). Every file related to a domain lives inside that domain's layer. The entire `orders` folder could be extracted and placed in a separate project and still be coherent internally.

Benefits:
- **Self-contained domains** — nothing related to orders is scattered across the project
- **Clear ownership** — when you need to change something about orders, you open one folder
- **Independent deployability** — in the future, domains could be split into separate services with minimal file movement
- **Bounded context enforcement** — cross-domain coupling becomes physically obvious

### Tradeoffs

- **Nuxt framework deviation** — Nuxt/Nitro's standard location is `server/api/` at the project root. This deviates from that. Compatibility with future Nuxt features that assume root `server/` is not guaranteed.
- **Community friction** — most Stack Overflow answers and tutorials assume root `server/api/`. Adjust answers for this structure.
- **Nitro discovery** — Nitro (Nuxt's server engine) scans for routes. This structure works with Nitro's `scanDirs` configuration, but verify after major Nuxt upgrades.

### What Makes This Work

In `nuxt.config.ts`, configure Nitro to discover server routes inside layers:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    scanDirs: [
      'layers/*/server',  // scan all layer server directories
    ]
  }
})
```

Without this, Nitro only looks at the default `server/` directory. With it, Nitro finds routes in all domain layers.

### Rule: One Route Per Domain

If a route spans two domains (e.g., an endpoint that creates an order and updates inventory), it belongs to **one domain** — the one that owns the primary resource. The other domain is called through its adapter, not by sharing a route.

---

## Public API Convention (`index.ts`)

**Every layer MUST have an `index.ts` that re-exports its public surface.** Everything not exported from `index.ts` is internal. This enforces the layer boundary.

### `layers/{domain}/index.ts` — Required Public API

```typescript
// layers/orders/index.ts
// PUBLIC API of the orders layer.
// Everything not exported here is INTERNAL — do not import from other layers.

// Public composables (the features this layer exposes)
export { useCheckout } from './composables/useCheckout'
export { useOrderList } from './composables/useOrderList'
export { useOrderDetail } from './composables/useOrderDetail'

// Public port interfaces (so other layers can implement consumers)
export type { OrderPort } from './ports/OrderPort'
export type { PlaceOrderCommand, OrderResult, LineItem } from './ports/OrderPort'

// Public entity types (domain shapes other layers may reference)
export type { OrderEntity } from './types/OrderEntity'

// NOT exported (internal):
//   - ./composables/useInternalHelper.ts
//   - ./adapters/FakeOrderAdapter.ts
//   - ./adapters/InstforgeOrderAdapter.ts
//   - ./types/InternalOrderHelper.ts  (only used inside this layer)
```

### `layers/base/index.ts` — Required for Shared

```typescript
// layers/base/index.ts
export { BaseButton, BaseModal, BaseCard } from './components/BaseButton.vue'
export { BaseModal.vue } from './components/BaseModal.vue'
export { formatDate, formatCurrency } from './utils/format'
export type { UserId, OrderId } from './types'
```

### What This Prevents

```typescript
// WRONG — importing internal file from another layer
import { useInternalHelper } from 'layers/orders/composables/useInternalHelper'

// RIGHT — import only through the public index
import { useCheckout } from 'layers/orders'  // resolves to layers/orders/index.ts
```

Nuxt auto-imports bypass this at the framework level, but **TypeScript imports and architecture tests** (Type 8) can enforce it. Add an architecture test:

```typescript
// tests/architecture/layer-boundaries.spec.ts
test('layers/{domain}/index.ts is the only valid import path from other layers', () => {
  // Verify no cross-layer imports of internal files
})
```

---

## Cross-Entity Imports (`@x/` Alias)

When a widget or page needs data from another domain, use the `@x/` alias. Set it up in `nuxt.config.ts`:

### `nuxt.config.ts` — Alias Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  alias: {
    // Cross-entity imports — each domain exposes only its public index
    '@x/users': 'layers/users/index.ts',
    '@x/orders': 'layers/orders/index.ts',
    '@x/auth': 'layers/auth/index.ts',
    '@x/base': 'layers/base/index.ts',
  }
})
```

### Usage in Widgets and Pages

```typescript
// layers/orders/widgets/OrderWidget.vue
// ✅ Correct — imports from the other layer's public index
import { useUser } from '@x/users'
import { UserCard } from '@x/users/components'

// ❌ Wrong — skips the index, imports internal file
import { useInternalHelper } from '@x/users/composables/useInternalHelper'
```

### Rule: Always Import From `index.ts`, Not Deep Paths

The alias points to `index.ts`. This means:
- `from '@x/users'` → gets `users/index.ts` → only public exports
- `from '@x/users/composables/useAuth'` → bypasses the public boundary → **architectural violation**

If you need something from another layer that isn't in its `index.ts`, **propose adding it to the index** rather than importing the deep path.

### Why This Matters

Without `@x/` aliases, developers import from deep paths:
```typescript
// This path leaks internals — if useUser internals change, this breaks
import { useInternalHelper } from 'layers/users/composables/useInternalHelper'
```

With aliases pointing to `index.ts`, the only stable import is through the public API:
```typescript
// This path is stable — index.ts is the contract
import { useUser } from '@x/users'
```

---

## Cross-Domain Shared Data

When two domains need to share read data (e.g., `OrderWidget` needs `customerName` from `Customer`), use one of these patterns:

### Pattern A: Domain Port with Read Model (Preferred for Thin Reads)

Define a query port in the consuming layer:

```typescript
// layers/orders/ports/CustomerQueryPort.ts
export interface CustomerSummary {
  customerId: string
  name: string
  email: string
}

export interface CustomerQueryPort {
  getCustomer(id: string): Promise<CustomerSummary | null>
}
```

The order domain doesn't own the customer — it just asks for a summary through a port. The customer domain implements the adapter.

### Pattern B: Pre-Enriched Read Model (When Join is Owned by One Domain)

The domain that needs the data most owns the read model and enriches it:

```typescript
// layers/orders/composables/useOrderWithCustomer.ts
// Returns an order with customer name pre-joined — no cross-domain port needed
export function useOrderWithCustomer(orderId: string) {
  const order = useOrderDetail(orderId)
  const customer = useCustomer(order.value?.customerId)

  return {
    order: computed(() => ({
      ...order.value,
      customerName: customer.value?.name
    }))
  }
}
```

Use Pattern B when the enriched model is owned by one domain. Use Pattern A when you need flexible composition across domains.

---

## Ports & Adapters — Complete Example

Every external dependency has a **port** (at layer boundary) and an **adapter** (in `adapters/`). The adapter is injected via composition root.

### Wiring Map

```
layers/orders/pages/checkout.vue
  └── useCheckout.ts                    (composable — feature)
        └── OrderPort                   (ports/OrderPort.ts — at layer boundary)
              └── InstforgeOrderAdapter  (adapters/InstforgeOrderAdapter.ts)
                    └── instforge       (external service)
```

### Step 1 — Define the Port (At Layer Boundary)

```typescript
// layers/orders/ports/OrderPort.ts
// Port interface — the layer's public contract with the outside world.
// Lives at layer boundary (ports/), not inside composables/.

export interface LineItem {
  sku: string
  quantity: number
  unitPrice: number
}

export interface PlaceOrderCommand {
  customerId: string
  lineItems: LineItem[]
  shippingAddressId: string
}

export interface OrderResult {
  orderId: string
  status: 'pending' | 'confirmed' | 'failed'
  placedAt: string
}

export interface OrderPort {
  placeOrder(command: PlaceOrderCommand): Promise<OrderResult>
  getOrder(orderId: string): Promise<OrderResult | null>
  listOrders(customerId: string): Promise<OrderResult[]>
}
```

### Step 2 — Create the Fake Adapter

```typescript
// layers/orders/adapters/FakeOrderAdapter.ts
// Fake adapter — deterministic, no network, no credentials.
// Lives permanently in adapters/ AND is imported as a test fixture.
// See testing-pyramid.md: fake adapters are integration test fixtures.

export class FakeOrderAdapter implements OrderPort {
  private orders = new Map<string, OrderResult>()

  async placeOrder(command: PlaceOrderCommand): Promise<OrderResult> {
    const orderId = `order_${Date.now()}`
    const result: OrderResult = {
      orderId,
      status: 'confirmed',
      placedAt: new Date().toISOString()
    }
    this.orders.set(orderId, result)
    return result
  }

  async getOrder(orderId: string): Promise<OrderResult | null> {
    return this.orders.get(orderId) ?? null
  }

  async listOrders(customerId: string): Promise<OrderResult[]> {
    return Array.from(this.orders.values())
  }
}
```

### Step 3 — Create the Real Adapter

```typescript
// layers/orders/adapters/InstforgeOrderAdapter.ts
// Real adapter — implements the same port interface.
// Fake adapter must walk before this is touched. See dev-flow/phases/06-implementation.md.

import type { OrderPort, PlaceOrderCommand, OrderResult } from '../ports/OrderPort'
import { instforge } from '~/lib/instforge'

export class InstforgeOrderAdapter implements OrderPort {
  async placeOrder(command: PlaceOrderCommand): Promise<OrderResult> {
    const response = await instforge.agents.call({
      agent: 'order-service',
      action: 'placeOrder',
      params: command
    })
    return response as OrderResult
  }

  async getOrder(orderId: string): Promise<OrderResult | null> {
    const response = await instforge.db.query({
      table: 'orders',
      where: { id: orderId }
    })
    return response.rows[0] as OrderResult ?? null
  }

  async listOrders(customerId: string): Promise<OrderResult[]> {
    const response = await instforge.db.query({
      table: 'orders',
      where: { customerId }
    })
    return response.rows as OrderResult[]
  }
}
```

### Step 4 — Register in Composition Root

```typescript
// app/diComposition.ts
// Single place where all port → adapter bindings are defined.
// Swap binding here to swap fake ↔ real. One line per adapter.

import { FakeOrderAdapter } from 'layers/orders/adapters/FakeOrderAdapter'
import { InstforgeOrderAdapter } from 'layers/orders/adapters/InstforgeOrderAdapter'
import type { OrderPort } from 'layers/orders/ports/OrderPort'

// Singleton instances — one per adapter type
export const orderAdapter: OrderPort = new FakeOrderAdapter()
// export const orderAdapter: OrderPort = new InstforgeOrderAdapter()  // swap for production
```

### Step 5 — Use in Composable

```typescript
// layers/orders/composables/useCheckout.ts
import type { OrderPort, PlaceOrderCommand } from '../ports/OrderPort'
import { orderAdapter } from '~/app/diComposition'

export function useCheckout() {
  async function placeOrder(command: PlaceOrderCommand) {
    return orderAdapter.placeOrder(command)
  }

  return { placeOrder }
}
```

### Step 6 — Export from Public Index

```typescript
// layers/orders/index.ts
export { useCheckout } from './composables/useCheckout'
export type { OrderPort, PlaceOrderCommand, OrderResult, LineItem } from './ports/OrderPort'
```

---

## File Templates

### nuxt.config.ts (layer)
```ts
// layers/{domain}/nuxt.config.ts
// Minimal — modules belong in root nuxt.config.ts only
export default defineNuxtConfig({})
```

### Public index
```typescript
// layers/{domain}/index.ts
// PUBLIC API — re-export everything other layers may use
export { use{Domain} } from './composables/use{Domain}'
export type { {Domain}Port } from './ports/{Domain}Port'
// NOT exported: internal composables, adapters, private helpers
```

### Port interface
```typescript
// layers/{domain}/ports/{Name}Port.ts
export interface {Name}Port {
  // Define methods with input/output types — no implementation here
}
```

### Feature composable
```typescript
// layers/{domain}/composables/use{Domain}.ts
export function use{Domain}() {
  // All Insforge calls live here — pages and components never call Insforge directly
  return { /* ... */ }
}
```

### Server route — GET
```ts
// layers/{domain}/server/api/{resource}/index.get.ts
export default defineEventHandler(async (event) => {
  try {
    const data = await // delegate to composable
    return { data, error: null }
  } catch (err) {
    return { data: null, error: (err as Error).message }
  }
})
```

### Entity component
```vue
<!-- layers/{domain}/components/{EntityName}.vue -->
<!-- Receives data via props, emits events. No data fetching. -->
<script setup lang="ts">
interface Props { entity: { name: string } }
const props = defineProps<Props>()
const emit = defineEmits<{ select: [id: string] }>()
</script>
<template>
  <div>{{ props.entity.name }}</div>
</template>
```

### Widget component
```vue
<!-- layers/{domain}/widgets/{WidgetName}.vue -->
<!-- Composes entities and features. Owns layout only. -->
<script setup lang="ts">
import { EntityCard } from '@x/other-domain/components'  // via @x alias
import { useFeatureA } from '@x/other-domain'           // via @x alias
</script>
<template>
  <!-- layout -->
</template>
```

### Pinia store (cross-layer only)
```ts
// layers/core/stores/{domain}.ts
export const use{Domain}Store = defineStore('{domain}', () => {
  const item = ref(null)
  return { item, set: (v) => { item.value = v }, clear: () => { item.value = null } }
})
```

---

## Naming Conventions

| Type | Convention | Location |
|------|-----------|----------|
| Public index | `index.ts` | `layers/{domain}/index.ts` |
| Composables | `use{Noun}.ts` | `layers/{domain}/composables/` |
| Port interfaces | `{Name}Port.ts` | `layers/{domain}/ports/` |
| Fake adapters | `Fake{Name}Adapter.ts` | `layers/{domain}/adapters/` |
| Real adapters | `{Provider}{Name}Adapter.ts` | `layers/{domain}/adapters/` |
| Entity components | `PascalCase.vue` | `layers/{domain}/components/` |
| Widget components | `PascalCase.vue` | `layers/{domain}/widgets/` |
| Pages | `kebab-case.vue` | `layers/{domain}/pages/` |
| Stores | `use{Noun}Store.ts` | `layers/core/stores/` |
| Server routes | `{resource}/index.{method}.ts` | `layers/{domain}/server/api/` |

---

## Rules

### Layer Boundaries
- **Every layer has an `index.ts`** — exports only the public surface. Everything else is internal.
- **Import only through `@x/` aliases** — `import from '@x/users'`, never `import from 'layers/users/composables/useUser'`
- **Ports live at layer boundary** — `layers/{domain}/ports/`, not `layers/{domain}/composables/ports/`

### Domain Types (`types/`)

Domain types are TypeScript types and interfaces that **belong to the domain** — things that would make sense if you moved the entire layer to a different project.

**What goes in `types/`:**
```
layers/orders/types/
  Order.ts         ← Order entity (id, status, lineItems, etc.)
  LineItem.ts      ← value object
  OrderId.ts      ← branded ID type
```

**What does NOT go in `types/`:**
- Generic utility types (→ `layers/base/utils/`)
- API request/response wrappers (→ `layers/{domain}/composables/api/`)
- JSON serialization types (→ `layers/{domain}/composables/api/`)

**Rule: If the type would be meaningless outside this domain, it belongs in `types/`**

Port interface types (`PlaceOrderCommand`, `OrderResult`) live in `ports/OrderPort.ts` alongside the interface they belong to — they are part of the port's public contract.

Entity types (`Order`, `LineItem`) belong in `types/` because they are domain shapes, not port contracts.

### Ports & Adapters
- **Every external dependency has a port** — define interface before adapter
- **Fake walks before real** — see `why/WALKING_SKELETON.md`
- **Adapters are injected, never imported directly** — composables receive via DI
- **Fake adapters are permanent** — test fixtures, not temporary code

### Composables
- Own all Insforge calls — pages and components never call Insforge directly
- May import from `ports/` — ports are a peer, not a child
- May NOT import from `adapters/` — adapters are lower-level infrastructure
- Never import from other domains' `composables/` directly — use `@x/`

### Components
- Entity components (`components/`) — UI representations of domain objects. No data fetching.
- Widget components (`widgets/`) — compose entities and features. Own layout only.
- Pages never import adapters — use composables exclusively.

### Stores
- Only for state that survives navigation or is shared across 2+ layers
- Single-layer state stays in the composable

### Middleware

Domain middleware lives inside each domain layer, not in a central location.

**Why:** Each domain owns its access rules. "Can this user access this order?" is orders domain logic, not global logic.

```
layers/orders/middleware/
  requireOrderOwnership.ts   ← only orders domain knows who owns orders
layers/auth/middleware/
  requireSession.ts         ← only auth domain knows what a valid session is
```

**What goes in domain middleware:**
- Permission checks specific to this domain (e.g., "can this user modify this order")
- Domain-specific session validation
- Resource ownership checks

**What does NOT go in domain middleware:**
- Global rate limiting (→ `app/middleware/`)
- Global auth (→ `layers/auth/middleware/`)
- CORS, headers (→ Nuxt config)

**Rule:** If the check only makes sense in one domain, it belongs in that domain's middleware.

### Testing
See `references/testing-pyramid.md`. Quick guide:

| Test Type | Location |
|-----------|----------|
| Unit (Type 1) | `layers/{domain}/tests/unit/` |
| Integration (Type 2) | `tests/integration/` (with fake adapters) |
| Component (Type 3) | `layers/{domain}/tests/components/` |
| E2E (Type 4) | `tests/e2e/` |
| Invariant (Type 5) | co-located with aggregate |
| Property (Type 6) | `layers/{domain}/tests/properties/` |
| Regression (Type 7) | `tests/regression/` |
| Architecture (Type 8) | `tests/architecture/` |

---

## FSD Layer Mapping

Layer-scaffold implements [Feature-Sliced Design](https://feature-sliced.design/) for Nuxt Layers:

| FSD Layer | Nuxt Layers Location | Notes |
|-----------|---------------------|-------|
| `app` | `app/` | Entry point, DI composition, plugins |
| `pages` | `layers/{domain}/pages/` | Route views |
| `widgets` | `layers/{domain}/widgets/` | Composite UI |
| `features` | `layers/{domain}/composables/` | Use cases |
| `entities` | `layers/{domain}/components/` | Domain objects |
| `shared` | `layers/base/` | Primitives, utils, types |

**Import rule:** FSD layers import downward only. Features may import entities. Entities may NOT import features. See `references/feature-sliced-design.md`.

---

## CQRS Compatibility

CQRS is a backend domain pattern that coexists with this structure.

| CQRS Concept | Location |
|--------------|---------|
| Command handler | `layers/{domain}/composables/` |
| Query handler | `layers/{domain}/composables/` |
| Event subscriber | `layers/{domain}/server/events/` |
| Repository interface | `layers/{domain}/ports/` |
| Repository implementation | `layers/{domain}/adapters/` |
| Event bus | `layers/{domain}/adapters/` |

For Tier 3 event-driven workflows, see `references/cqrs-patterns.md`.
