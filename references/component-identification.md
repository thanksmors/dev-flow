# Component Identification Guide

Use this guide to decide which components to include in a C4 model. Apply the scoring matrix below to any class, module, or architectural unit you're considering.

## Scoring Matrix

For each component, score it against these questions:

| Question | Weight | Yes | No |
|---|---|---|---|
| Does it participate in a use case or user journey? | High (+3) | +3 | 0 |
| Does it have business logic (not just data passing)? | High (+3) | +3 | 0 |
| Does it cross an architectural boundary (layer, service, domain)? | High (+3) | +3 | 0 |
| Is it an entry point (HTTP handler, CLI, message consumer)? | High (+3) | +3 | 0 |
| Is it a domain entity or aggregate root? | High (+3) | +3 | 0 |
| Does it implement a port (hexagonal architecture)? | Medium (+2) | +2 | 0 |
| Is it an infrastructure adapter (repository, external client)? | Medium (+2) | +2 | 0 |
| Does it handle or publish domain events? | Medium (+2) | +2 | 0 |
| Would a new developer need to know about it to understand the architecture? | Medium (+2) | +2 | 0 |
| Is it reused across multiple components? | Low (+1) | +1 | 0 |
| Does it have significant dependencies? | Low (+1) | +1 | 0 |
| Is it just data transfer (DTO, pure data)? | High (-3) | 0 | -3 |
| Is it a test class? | High (-3) | 0 | -3 |
| Is it framework boilerplate (no domain logic)? | Medium (-2) | 0 | -2 |
| Is it a private helper or utility? | Medium (-2) | 0 | -2 |

**Scoring:**
- **≥ 5 points**: Include — document as a component
- **2–4 points**: Consider including — use judgment
- **≤ 1 point**: Exclude — omit from the C4 model
- **Negative**: Definitely exclude

## Always Include

Regardless of score, always include:
- HTTP handlers / controllers / processors
- Command handlers (CQRS)
- Query handlers
- Event subscribers
- Domain entities and aggregates
- Repository interfaces and implementations
- Event buses
- External dependencies (databases, caches, message brokers)

## Always Exclude

Regardless of score, never include:
- DTOs and input/output objects
- Test classes
- Framework configuration
- Base classes without logic
- Private helper methods
- Value objects without validation (e.g., simple `FirstName` wrappers)
- Factories and mappers (unless architecturally significant)

## Layer Grouping

Components in Structurizr workspace.dsl are grouped by layer:

| Layer | Contains |
|---|---|
| `group "Application"` | Processors, controllers, command handlers, event subscribers |
| `group "Domain"` | Entities, aggregates, domain events, repository interfaces (ports) |
| `group "Infrastructure"` | Repository implementations, event bus implementations, external adapters |

External dependencies (database, cache, message broker) go **outside all groups** at container level.

## Quick Decision

If the scoring matrix is too detailed, ask:
1. Would removing this change the C4 diagram significantly? → Include
2. Would a new developer ask about this during onboarding? → Include
3. Is this just moving data without logic? → Exclude

## See Also

- `why/c4-common-mistakes.md` — common C4 errors including what NOT to document
- `references/cqrs-patterns.md` — CQRS-specific component patterns
