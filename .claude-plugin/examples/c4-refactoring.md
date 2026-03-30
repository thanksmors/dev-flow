# Worked Example: Refactoring Components

Updating workspace.dsl during a code refactor.

## Scenario

Refactoring: **Splitting a monolithic UserCommandHandler into separate RegisterUserCommandHandler and UpdateUserCommandHandler**.

## Before Refactoring

In workspace.dsl:

```structurizr
userCommandHandler = component "UserCommandHandler" "Handles all user commands" "CommandHandler" {
    tags "Item"
}

// Relationships
userCommandHandler -> user "creates / updates"
userCommandHandler -> userRepository "uses"
userCommandHandler -> userRegisteredEvent "publishes"
```

## Step 1: Remove Old Component

Delete the `userCommandHandler` component definition and all its relationships.

```structurizr
// DELETE:
userCommandHandler = component "UserCommandHandler" "Handles all user commands" "CommandHandler" {
    tags "Item"
}

// DELETE all relationships referencing userCommandHandler
```

## Step 2: Add New Components

In `group "Application"`:

```structurizr
registerUserCommandHandler = component "RegisterUserCommandHandler" "Handles user registration" "CommandHandler" {
    tags "Item"
}

updateUserCommandHandler = component "UpdateUserCommandHandler" "Handles user updates" "CommandHandler" {
    tags "Item"
}
```

## Step 3: Update Relationships

Add new relationships:

```structurizr
// RegisterUserCommandHandler flow
registerUserCommandHandler -> user "creates"
registerUserCommandHandler -> userRepository "uses for persistence"
registerUserCommandHandler -> userRegisteredEvent "publishes"

// UpdateUserCommandHandler flow
updateUserCommandHandler -> user "updates"
updateUserCommandHandler -> userRepository "uses for persistence"
updateUserCommandHandler -> emailChangedEvent "publishes"
```

## Common Refactoring Patterns

### Pattern 1: Split Handler
One handler with multiple responsibilities → separate handlers per command.
- Remove old component + relationships
- Add new components + specific relationships

### Pattern 2: Extract Domain Service
Handler contains complex business logic → extract a domain service.
- Add domain service component to Domain group
- Handler → domainService relationship
- domainService → entity relationship

### Pattern 3: Move Component Between Layers
Component in wrong layer (e.g., validator in Infrastructure instead of Domain).
- Move component definition to correct group
- No relationship changes needed

### Pattern 4: Introduce Interface (Hexagonal)
Direct repository dependency → port interface.
- Add repository interface to Domain group
- Handler → interface relationship
- Repository → interface relationship

## Verification Checklist

- [ ] Old component and relationships fully removed
- [ ] New components added to correct layer group
- [ ] All new relationships have standardized labels
- [ ] No orphaned relationships (references to deleted components)
- [ ] DSL validates (run `structurizr-cli validate workspace.dsl`)
- [ ] workspace.json saved after positioning
- [ ] Both files committed together
