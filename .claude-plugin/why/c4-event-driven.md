# Event-Driven C4 Patterns

## Core Principle

**Show individual topics/queues as separate containers.** Never show a single "Kafka" or "RabbitMQ" box with all services connecting to it. This hides actual data flow.

## Pattern 1: Individual Topics as Containers

### Wrong — Single Message Bus

```mermaid
C4Container
  title WRONG: Single Message Bus

  Container(orderSvc, "Order Service", "Java")
  Container(inventorySvc, "Inventory Service", "Java")
  Container(kafka, "Kafka", "Event Streaming")

  Rel(orderSvc, kafka, "Publishes/Subscribes")
  Rel(inventorySvc, kafka, "Publishes/Subscribes")
```

### Correct — Individual Topics

```mermaid
C4Container
  title Correct: Individual Topics

  Container(orderSvc, "Order Service", "Java")
  Container(inventorySvc, "Inventory Service", "Java")

  ContainerQueue(orderCreated, "order.created", "Kafka", "New order events")
  ContainerQueue(stockReserved, "inventory.reserved", "Kafka", "Stock events")

  Rel(orderSvc, orderCreated, "Publishes")
  Rel(inventorySvc, orderCreated, "Consumes")
  Rel(inventorySvc, stockReserved, "Publishes")
  Rel(orderSvc, stockReserved, "Consumes")
```

## Pattern 2: CQRS Container View

Show command side and query side as separate container regions:

```mermaid
C4Container
  title CQRS Architecture

  Person(user, "User")

  Container_Boundary(cqrs, "CQRS Service") {
    Container(commandApi, "Command API", "Java", "Write operations")
    Container(queryApi, "Query API", "Node.js", "Read operations")
    ContainerDb(writeDb, "Write DB", "PostgreSQL", "Source of truth")
    ContainerDb(readDb, "Read DB", "Elasticsearch", "Query-optimized")
    ContainerQueue(events, "Domain Events", "Kafka", "State changes")
    Container(projector, "Projector", "Java", "Updates read model")
  }

  Rel(user, commandApi, "Commands", "HTTPS")
  Rel(user, queryApi, "Queries", "HTTPS")
  Rel(commandApi, writeDb, "Writes", "JDBC")
  Rel(commandApi, events, "Publishes", "Avro")
  Rel(projector, events, "Consumes", "Avro")
  Rel(projector, readDb, "Updates", "Native Client")
  Rel(queryApi, readDb, "Queries", "Elasticsearch client")
```

## Pattern 3: Saga Choreography vs Orchestration

### Choreography (events only)

Events trigger subscribers, no central orchestrator:

```mermaid
C4Container
  title Saga Choreography

  Container(orderSvc, "Order Service", "Java")
  Container(inventorySvc, "Inventory Service", "Go")
  Container(paymentSvc, "Payment Service", "Node.js")

  ContainerQueue(orderCreated, "order.created", "Kafka")
  ContainerQueue(paymentComplete, "payment.completed", "Kafka")

  Rel(orderSvc, orderCreated, "Publishes")
  Rel(inventorySvc, orderCreated, "Consumes + reserves")
  Rel(inventorySvc, paymentComplete, "Publishes on success")
  Rel(paymentSvc, paymentComplete, "Consumes + charges")
  Rel(paymentSvc, orderCreated, "Consumes on failure")
```

### Orchestration (central saga)

One component coordinates the entire saga:

```mermaid
C4Component
  title Saga Orchestrator

  Container_Boundary(order, "Order Service") {
    Component(saga, "OrderSagaOrchestrator", "Spring", "Coordinates order pipeline")
    Component(paymentStep, "PaymentStep", "Spring", "Payment sub-step")
    Component(inventoryStep, "InventoryStep", "Spring", "Inventory sub-step")
  }

  ContainerQueue(events, "Events", "Kafka")

  Rel(saga, paymentStep, "1. Execute payment")
  Rel(saga, inventoryStep, "2. Reserve inventory")
  Rel(saga, events, "3. Publish result")
```

## ADR Integration

For each event-driven pattern, note in the component description which ADR covers the decision.

ADR references go on infrastructure components (queues, databases, external services) and key architectural decisions. Format: `ADR-NNN: Short title`.

### Before/After Example

**Before (no ADR reference):**
```
Component(orderCreated, "order.created", "Kafka", "Order events")
```

**After (with ADR reference):**
```
Component(orderCreated, "order.created", "Kafka", "ADR-003: Event sourcing pattern")
```

### Full Example

```mermaid
C4Container
  title System Architecture

  Container(orderSvc, "Order Service", "Java", "Order processing")
  ContainerQueue(orderCreated, "order.created", "Kafka", "ADR-003: Event sourcing pattern")
  ContainerQueue(paymentComplete, "payment.completed", "Kafka", "ADR-003: Event sourcing pattern")

  Rel(orderSvc, orderCreated, "Publishes", "Avro")
```
