# Structurizr Workspace Template

Copy this template as the starting point for a new project's `docs/workspace.dsl`.

## Quick Copy

```structurizr
workspace {

    !identifiers hierarchical

    model {
        properties {
            "structurizr.groupSeparator" "/"
        }

        softwareSystem = softwareSystem "{SystemName}" {
            {containerName} = container "{ContainerName}" {

                group "Application" {
                    {processor} = component "{ProcessorName}" "Processes HTTP requests for {feature}" "RequestProcessor" {
                        tags "Item"
                    }
                    {commandHandler} = component "{CommandHandlerName}" "Handles {CommandName}" "CommandHandler" {
                        tags "Item"
                    }
                }

                group "Domain" {
                    {entity} = component "{EntityName}" "{EntityDescription}" "Entity" {
                        tags "Item"
                    }
                    {domainEvent} = component "{EventName}" "Published when {condition}" "DomainEvent" {
                        tags "Item"
                    }
                    {repoInterface} = component "{RepoInterfaceName}" "Contract for {EntityName} persistence" "Interface" {
                        tags "Item"
                    }
                }

                group "Infrastructure" {
                    {repository} = component "{RepositoryName}" "{Technology} implementation of {EntityName} persistence" "Repository" {
                        tags "Item"
                    }
                    {eventBus} = component "{EventBusName}" "Handles event publishing" "EventBus" {
                        tags "Item"
                    }
                }

                // External dependencies — OUTSIDE all groups
                database = component "Database" "Stores application data" "{DBTechnology}" {
                    tags "Database"
                }
                {cacheOrBroker} = component "{CacheOrBrokerName}" "{Description}" "{Technology}" {
                    tags "Database"
                }

                // Relationships — add as features are implemented
                {processor} -> {commandHandler} "dispatches {CommandName}"
                {commandHandler} -> {entity} "creates"
                {commandHandler} -> {repoInterface} "depends on"
                {commandHandler} -> {domainEvent} "publishes"
                {repository} -> {repoInterface} "implements"
                {repository} -> {entity} "stores / retrieves"
                {repository} -> database "accesses data"
                {domainEvent} -> {eventSubscriber} "triggers"
            }
        }
    }

    views {
        systemContext softwareSystem "SystemContext" {
            include *
            autoLayout
        }

        container softwareSystem "Containers" {
            include *
            autoLayout
        }

        component {containerName} "{ContainerName}-Components" {
            include *
        }

        styles {
            element "Item" {
                color white
                background #34abeb
            }
            element "Database" {
                color white
                shape cylinder
                background #34abeb
            }
        }
    }
}
```

## Key Elements

### !identifiers hierarchical
Enables dot-notation for component paths: `softwareSystem.containerName.processor`

### structurizr.groupSeparator = "/"
Allows group names like "Application/Domain" to render cleanly in views.

### External Dependencies Outside Groups
Database, cache, and message broker are **outside all group blocks**. They are not part of your application code — they are external systems your code connects to.

### Tags
The `tags "Item"` marker applies the standard component style (blue background, white text). `tags "Database"` applies the cylinder shape.

### Component Type Parameter
Every component should have a type: `RequestProcessor`, `CommandHandler`, `EventSubscriber`, `Entity`, `Repository`, `EventBus`, etc.

## Adding Components

1. Choose the correct group (Application / Domain / Infrastructure)
2. Add the component definition with: variable name, display name, description, type, tags
3. Add relationships after all component definitions
4. Run `docker compose up` (or standalone Structurizr Lite) and verify at http://localhost:8080
5. Position components manually, then click "Save workspace" to update workspace.json
6. Commit both workspace.dsl and workspace.json

## Common Patterns

See the worked examples for specific patterns:
- `examples/c4-cqrs-pattern.md` — CQRS command/query handlers + events + subscribers
- `examples/c4-api-endpoint.md` — REST endpoint with processor + transformer
- `examples/c4-refactoring.md` — updating workspace.dsl during code refactoring
