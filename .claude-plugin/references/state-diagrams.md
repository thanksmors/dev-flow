# State Diagrams — Mermaid

## When to Use

Use a **Mermaid stateDiagram** when a component or domain entity has meaningful state with transitions that are complex enough to benefit from visual representation.

**Good candidates:**
- Entities with distinct states: `Order.pending → Order.processing → Order.shipped → Order.delivered`
- Services with internal state machines: `AuthService.idle → AuthService.validating → AuthService.authenticated → AuthService.error`
- Workflows with stages and transitions: `Onboarding.start → Onboarding.profile → Onboarding.verify → Onboarding.complete`

**Not needed:**
- Simple boolean flags (e.g., `isActive: true/false`)
- CRUD entities where state is just database persistence
- Components with no meaningful internal state

## Syntax

```mermaid
stateDiagram-v2
    [*] --> StateA
    StateA --> StateB : event / action
    StateB --> [*]
```

### Key Elements

```mermaid
stateDiagram-v2
    [*] --> Idle                    # initial state

    Idle --> Processing : submit     # transition with trigger
    Processing --> Success : complete / writeDB
    Processing --> Error : fail / rollback
    Error --> Idle : retry

    Success --> [*]                # final state
```

### Guards (Conditional Transitions)

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Confirmed : validate() / isValid
    Pending --> Rejected : validate() / !isValid
    Rejected --> [*]
    Confirmed --> [*]
```

### Fork and Join

```mermaid
stateDiagram-v2
    [*] --> Processing
    Processing --> Split : done

    state Split {
        [*] --> A
        [*] --> B
        A --> [*]
        B --> [*]
    }

    Split --> Complete : both done
    Complete --> [*]
```

### Notes

```mermaid
stateDiagram-v2
    [*] --> Authenticated
    Authenticated --> [*] : logout

    note right of Authenticated
        Session expires after
        30 minutes of inactivity
    end note
```

## Common Patterns

### Pattern 1: Entity Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Active : enable
    Active --> Suspended : suspend
    Suspended --> Active : reactivate
    Suspended --> Deleted : delete
    Active --> Deleted : delete
    Created --> Deleted : delete
    Deleted --> [*]
```

### Pattern 2: Service State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Initializing : init()
    Initializing --> Ready : setupComplete
    Initializing --> Failed : setupError

    Failed --> Initializing : retry()
    Ready --> Processing : handle()
    Processing --> Ready : complete()
    Ready --> ShuttingDown : shutdown()
    ShuttingDown --> [*]
```

### Pattern 3: Async Workflow

```mermaid
stateDiagram-v2
    [*] --> Queued
    Queued --> Processing : worker picks up
    Processing --> Success : task completes
    Processing --> Retrying : transient failure / retryCount < 3
    Retrying --> Processing : retry
    Processing --> DeadLetter : max retries exceeded
    Success --> [*]
    DeadLetter --> [*]
```

## Placement

State diagrams go in `.dev-flow/architecture/states/` with one file per domain/component:

```
.dev-flow/architecture/
├── states/
│   ├── order-entity.states.md
│   ├── auth-service.states.md
│   └── task-workflow.states.md
└── sequences/
    ├── checkout-flow.md
    └── auth-flow.md
```

Reference them from `docs/architecture/04-key-flows.md` or the relevant domain section.

## Verification

When implementing, compare the actual state transitions in code against the diagram:
- Every `[*] --> State` must have a corresponding initialization path
- Every transition `A --> B` must be implementable (guards must be testable)
- Final states `State --> [*]` must be reachable

If a transition in the diagram cannot be implemented, the diagram is wrong — fix the diagram first.
