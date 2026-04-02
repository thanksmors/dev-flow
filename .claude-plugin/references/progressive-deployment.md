# Progressive Deployment Strategy

## Overview

Progressive deployment is the practice of building software incrementally, starting with the simplest working version and progressively adding complexity. This plugin combines several techniques to achieve this.

## Core Principles

1. **Start simple, add complexity later** — Don't over-engineer the initial implementation
2. **Every increment must work** — Each addition is tested and verified before moving on
3. **Defer decisions with adapters** — Use interfaces to postpone technology choices
4. **Thin slices, not thick layers** — Build end-to-end value, not complete layers

## Technique 1: Walking Skeleton

Start with the thinnest possible end-to-end path.

See: `walking-skeleton.md`

**Key rules:**
- Takes hours, not days
- Connects all major components
- Has at least one end-to-end test
- Proves the architecture works

## Technique 2: Elephant Carpaccio (Thin Vertical Slices)

Slice features into thin, end-to-end increments.

See: `elephant-carpaccio.md`

**Key rules:**
- Each slice delivers user-visible value
- Each slice is independently deployable
- Order from simplest to most complex
- Skip edge cases in early slices, add them later

## Technique 3: Deferred Architectural Decisions

Don't commit to technology choices prematurely. Start simple and swap later.

### How It Works

1. **Define an interface** for the capability you need
2. **Implement with the simplest option** (SQLite, in-memory, hardcoded)
3. **Build all features against the interface**, not the implementation
4. **Swap to production option** at the very end (before deployment)

### Adapter Pattern

```typescript
// Define the interface once
interface MessageRepository {
  save(message: Message): Promise<Message>;
  findById(id: string): Promise<Message | null>;
  list(conversationId: string): Promise<Message[]>;
}

// Implement with SQLite (simple)
class SqliteMessageRepository implements MessageRepository {
  // ...
}

// Later: swap to PostgreSQL (production)
class PostgresMessageRepository implements MessageRepository {
  // ...
}

// The rest of the code only knows about MessageRepository
```

### Common Deferred Decisions

| Capability | Simple Start | Production Swap | When to Swap |
|-----------|-------------|----------------|-------------|
| Database | SQLite | PostgreSQL | Before production deploy |
| Auth | Hardcoded user | JWT/OAuth | When multi-user needed |
| File storage | Local filesystem | S3/GCS | Before production deploy |
| Search | In-memory filter | Elasticsearch | When scale demands it |
| Queue | In-memory | Redis/RabbitMQ | When async needed |
| Config | Hardcoded | Environment/config file | Before any deploy |
| Logging | console.log | Structured logger | When monitoring needed |
| Caching | No cache | Redis | When performance demands it |

### Rules for Deferring

1. **MUST define the interface before implementing** — The interface IS the architecture
2. **MUST implement the simple option first** — Prove the feature works before optimizing
3. **MUST NOT couple feature code to the simple implementation** — Always code against the interface
4. **MUST swap at the right time** — Too early wastes effort, too late creates technical debt
5. **MUST test the swap** — Write tests that verify both implementations satisfy the interface

## Technique 4: Progressive Testing

Start with basic tests, progressively add sophisticated testing.

1. **Slice 1**: Basic happy path test
2. **Slice 2**: Add error case tests
3. **Slice 3**: Add edge case tests
4. **Slice 4**: Add invariant tests
5. **Slice 5**: Add property-based tests
6. **After all slices**: Regression test suite, coverage analysis

## Putting It All Together

The typical progression:

```
Walking Skeleton → Vertical Slice 1 → Vertical Slice 2 → ... → Swap Deferred Decisions → Gap Analysis → Deploy
     ↓                   ↓                    ↓                                              ↓
  Prove architecture   Core feature      Additional features                          Production-ready
  Simplest options     Basic tests       Progressive complexity                       All decisions resolved
```
