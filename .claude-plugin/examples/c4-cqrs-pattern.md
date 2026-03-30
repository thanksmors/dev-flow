# Worked Example: CQRS Pattern

Adding a new user registration feature using the CQRS pattern.

## Scenario

Implementing: **Register User** — a command handler that creates a user entity, publishes a domain event, and triggers an email confirmation subscriber.

## Components to Add

| Layer | Component | Type | Why |
|---|---|---|---|
| Application | RegisterUserCommandHandler | CommandHandler | Entry point for registration command |
| Domain | User | Entity | The aggregate being created |
| Domain | UserRegisteredEvent | DomainEvent | Published after successful registration |
| Domain | UserRepositoryInterface | Interface | Hexagonal port for persistence |
| Infrastructure | UserRepository | Repository | Implements the port with MariaDB |
| Infrastructure | SendConfirmationEmailSubscriber | EventSubscriber | Reacts to UserRegisteredEvent |
| External | Database | MariaDB | User data persistence |
| External | Message Broker | AWS SQS | Email queue |

## Step 1: Add Application Components

Add to the `group "Application"` block in workspace.dsl:

```structurizr
registerUserCommandHandler = component "RegisterUserCommandHandler" "Handles user registration commands" "CommandHandler" {
    tags "Item"
}
```

Note: The `RegisterUserCommand` itself is NOT added — commands are data structures (DTOs), not components.

## Step 2: Add Domain Components

Add to the `group "Domain"` block:

```structurizr
user = component "User" "User aggregate root" "Entity" {
    tags "Item"
}

userRegisteredEvent = component "UserRegisteredEvent" "Published when a user registers" "DomainEvent" {
    tags "Item"
}

userRepositoryInterface = component "UserRepositoryInterface" "Contract for user persistence" "Interface" {
    tags "Item"
}
```

## Step 3: Add Infrastructure Components

Add to the `group "Infrastructure"` block:

```structurizr
userRepository = component "UserRepository" "MariaDB implementation of user persistence" "Repository" {
    tags "Item"
}

sendConfirmationEmailSubscriber = component "SendConfirmationEmailSubscriber" "Sends confirmation email on registration" "EventSubscriber" {
    tags "Item"
}
```

## Step 4: Add External Dependencies

Add OUTSIDE all groups at container level:

```structurizr
database = component "Database" "MariaDB instance" "MariaDB" {
    tags "Database"
}

messageBroker = component "Message Broker" "AWS SQS for async messaging" "AWS SQS" {
    tags "Database"
}
```

## Step 5: Add Relationships

Add these relationships after all component definitions:

```structurizr
// Command flow
registerUserCommandHandler -> user "creates"
registerUserCommandHandler -> userRepositoryInterface "depends on"
registerUserCommandHandler -> userRegisteredEvent "publishes"

// Domain model
user -> userRegisteredEvent "creates on registration"

// Infrastructure implementation
userRepository -> userRepositoryInterface "implements"
userRepository -> user "stores / retrieves"
userRepository -> database "accesses data"

// Event flow
userRegisteredEvent -> sendConfirmationEmailSubscriber "triggers"
sendConfirmationEmailSubscriber -> messageBroker "sends via"
```

## Verification Checklist

- [ ] All 8 components defined (handler, entity, event, interface, repo, subscriber, db, broker)
- [ ] External dependencies outside groups
- [ ] Each relationship label uses standardized verbs from `references/dsl-relationship-patterns.md`
- [ ] Component types specified (CommandHandler, Entity, DomainEvent, Interface, Repository, EventSubscriber)
- [ ] workspace.json saved after positioning
- [ ] Both workspace.dsl and workspace.json committed

## What to Exclude

- `RegisterUserCommand` — it's a DTO, not a component
- `UserId`, `UserEmail`, `UserPassword` — value objects without complex logic
- `UuidFactory` — simple factory, not architecturally significant
