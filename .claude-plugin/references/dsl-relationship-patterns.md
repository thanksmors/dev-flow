# DSL Relationship Patterns

Standardized relationship labels for Structurizr workspace.dsl. Use consistent verbs — they make diagrams scannable and communicate intent.

## Label Conventions

- Use present tense: "creates", "publishes", "uses"
- Be specific: "validates user input" not "validates"
- Show direction: "dispatches RegisterUserCommand" not just "dispatches"
- Include protocol/technology on external dependencies: "HTTPS/JSON", "JDBC", "Avro"

## Common Relationship Labels

| From | To | Label | Example |
|---|---|---|---|
| Processor/Controller | Command Handler | "dispatches XCommand" | `processor -> handler "dispatches RegisterUserCommand"` |
| Command Handler | Entity | "creates" / "updates" / "deletes" | `handler -> user "creates"` |
| Command Handler | Repository Interface | "depends on" | `handler -> repoInterface "depends on"` |
| Command Handler | Event | "publishes" | `handler -> event "publishes"` |
| Repository | Entity | "stores / retrieves" | `repo -> user "stores / retrieves"` |
| Repository | Database | "accesses data" | `repo -> database "accesses data"` |
| Repository | Repository Interface | "implements" | `repo -> repoInterface "implements"` |
| Event | Event Subscriber | "triggers" | `event -> subscriber "triggers"` |
| Event Subscriber | External Service | "sends via" | `subscriber -> broker "sends via"` |
| Event Subscriber | Mailer | "sends email via" | `subscriber -> mailer "sends email via"` |
| Entity | Value Object | "has" | `user -> email "has"` |
| Entity | Domain Event | "creates" | `order -> event "creates on confirmation"` |
| Query Handler | Read Model | "queries" | `handler -> readModel "queries"` |
| API Controller | Service | "calls" | `controller -> service "calls"` |
| Service | Repository | "uses for persistence" | `service -> repo "uses for persistence"` |

## External Dependencies

External dependencies go **outside all groups** at container level. Label them generically:

| Element | Type | Label |
|---|---|---|
| PostgreSQL, MariaDB | Database | "accesses data", "persists to" |
| Redis | Cache | "caches via" |
| Kafka, SQS | Message Broker | "publishes to", "consumes from" |
| Stripe API | External API | "integrates with", "charges via" |
| SMTP | Mail | "sends email via" |

## Relationship Types

### Uses
Default relationship. Component A uses component B's public interface.
```
componentA -> componentB "uses"
```

### Creates
Component A creates an instance of component B (entity, value object, event).
```
handler -> user "creates"
handler -> event "publishes"
```

### Dispatches
Processor/controller dispatches a command or query to a handler.
```
processor -> commandHandler "dispatches RegisterUserCommand"
```

### Implements
Infrastructure component implements a domain port interface.
```
doctrineRepo -> userRepoInterface "implements"
```

### Triggers
Domain event triggers an event subscriber.
```
userRegisteredEvent -> emailSubscriber "triggers"
```

### Persists To / Retrieves From
Repository writes to or reads from a database.
```
userRepository -> database "accesses data"
```

## Anti-Patterns

### Vague Labels
```
BAD:  handler -> user "uses"
GOOD: handler -> user "validates and creates"
```

### Bidirectional Relationships
```
BAD:  handler <-> repository "uses"
GOOD: handler -> repository "uses for persistence"
      repository -> entity "manages"
```

### Missing External Dependencies
```
BAD:  Repository is shown but database is not
GOOD: repository -> database "accesses data"
```

### Circular Relationships
```
BAD:  A -> B "calls"; B -> A "returns result"
GOOD: A -> B "dispatches XCommand"
      B -> C "uses"
      C -> D "persists"
```

## See Also

- `why/c4-common-mistakes.md` — relationship mistakes to avoid
- `why/c4-event-driven.md` — event-driven relationship patterns
- `references/component-identification.md` — which components to include
