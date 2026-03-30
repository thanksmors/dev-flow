# C4Dynamic Diagrams

## When to Use

C4Dynamic shows **numbered sequence steps** within a container or component boundary. Use for:

- Complex request flows (auth, checkout, registration)
- Error handling and circuit breaker flows
- Saga compensation sequences
- Event-driven choreography sequences

Do NOT use for: simple 2-3 step flows (use a labeled Rel instead). For simple flows, a labeled `Rel` on a C4Container or C4Component diagram suffices — no numbered steps needed.

Use a standard Mermaid sequenceDiagram for cross-container flows or when you don't need C4 element types. Use C4Dynamic when the flow stays within a container boundary and you want C4 context.

## Syntax

> **Note:** C4Dynamic requires the C4 plugin for Mermaid. In Structurizr DSL (which dev-flow uses for workspace.dsl), C4Dynamic is not used — use Structurizr's native component views instead. This reference applies when writing Mermaid C4 in markdown files.

### Diagram Declaration

```
C4Dynamic
  title {Diagram Title}
```

### Elements

```
Container(name, "Label", "Technology", "Description")
Component(name, "Label", "Technology", "Description")
ContainerDb(name, "Label", "Technology", "Description")
Container_Boundary(alias, "Label") { ... }
```

### Relationships

```
Rel(from, to, "N. Step description", "Technology")
UpdateRelStyle(from, to, $offsetX, $offsetY)
```

## Common Patterns

### Pattern 1: Authentication Flow

```mermaid
C4Dynamic
  title Dynamic Diagram - User Sign In

  Container(spa, "SPA", "React")
  Container_Boundary(api, "API Application") {
    Component(signIn, "Sign In Controller", "Express")
    Component(security, "Security Service", "JWT")
  }
  ContainerDb(db, "Database", "PostgreSQL")

  Rel(spa, signIn, "1. Submit credentials", "JSON/HTTPS")
  Rel(signIn, security, "2. Validate")
  Rel(security, db, "3. Query user", "SQL")
```

### Pattern 2: Saga Compensation

```mermaid
C4Dynamic
  title Dynamic Diagram - Order Saga Compensation

  Container(orderSvc, "Order Service", "Java")
  Container(inventorySvc, "Inventory Service", "Go")
  Container(paymentSvc, "Payment Service", "Node.js")

  Rel(orderSvc, inventorySvc, "1. Reserve inventory", "HTTP")
  Rel(inventorySvc, orderSvc, "2. Inventory reserved")
  Rel(orderSvc, paymentSvc, "3. Charge payment", "HTTP")
  Rel(paymentSvc, orderSvc, "4. Payment failed")
  Rel(orderSvc, inventorySvc, "5. Release inventory", "HTTP")
```

## Layout Tips

- Use `$offsetY="-30"` to fix overlapping labels
- Keep steps under 10 per diagram
- One entry point (leftmost), external deps (rightmost)
- Use `Container_Boundary` to scope the system under consideration

### Layout Fix Example

When labels overlap, use `UpdateRelStyle` to nudge the relationship line:

```mermaid
C4Dynamic
  title Before Offset Fix

  Container(spa, "SPA", "React")
  Container(signIn, "Sign In", "Express")
  Container(security, "Security", "JWT")

  Rel(spa, signIn, "1. POST /login")
  Rel(signIn, security, "2. Validate creds")
  Rel(security, spa, "3. Return token")
```

```mermaid
C4Dynamic
  title After Offset Fix

  Container(spa, "SPA", "React")
  Container(signIn, "Sign In", "Express")
  Container(security, "Security", "JWT")

  Rel(spa, signIn, "1. POST /login")
  Rel(signIn, security, "2. Validate creds")
  UpdateRelStyle(spa, signIn, $offsetY="-30")
  Rel(security, spa, "3. Return token")
  UpdateRelStyle(security, spa, $offsetY="30")
```

The `UpdateRelStyle` call adjusts the bend point of the relationship line:
```
UpdateRelStyle(spa, signIn, $offsetY="-30")
```
