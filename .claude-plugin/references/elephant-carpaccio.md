# Elephant Carpaccio: Thin Vertical Slices

## Concept

"Elephant Carpaccio" is a technique for slicing large features into the thinnest possible vertical slices — each delivering end-to-end value. Like slicing an elephant so thin it becomes carpaccio.

The key insight: **slice vertically** (through all layers) rather than **horizontally** (one layer at a time).

## Horizontal vs Vertical Slicing

### Wrong: Horizontal Slices
```
Slice 1: Database layer (all tables)
Slice 2: API layer (all endpoints)
Slice 3: Frontend (all UI components)
```
Problem: No slice delivers value until ALL slices are done. High risk, late feedback.

### Right: Vertical Slices
```
Slice 1: One feature, end-to-end (DB + API + UI for creating an item)
Slice 2: Another feature, end-to-end (DB + API + UI for listing items)
Slice 3: Another feature, end-to-end (DB + API + UI for deleting items)
```
Benefit: Each slice delivers real value. Early feedback, low risk, incremental progress.

## How to Slice

### Step 1: Identify the End-to-End Path

For each feature, trace the path from user action to database and back:

```
User clicks → Frontend component → API call → Business logic → Database query → Response → UI update
```

### Step 2: Find the Thinnest Useful Slice

Ask: "What's the SMALLEST version of this feature that still delivers value?"

- Start with the simplest case (happy path only)
- Hardcode values where possible (no configuration yet)
- Use the simplest technology (in-memory store before database)
- Skip edge cases and error handling (add in later slices)

### Step 3: Order Slices

Order from smallest/simplest to largest/most complex:

1. **Walking skeleton** — thinnest possible end-to-end path
2. **Core feature** — the main value proposition
3. **Variations** — alternative cases and options
4. **Edge cases** — boundary conditions and error paths
5. **Polish** — UX improvements, performance, monitoring

### Step 4: Make Each Slice Independent

Each slice should:
- Be deployable on its own
- Work without depending on future slices
- Have its own tests
- Deliver measurable value

## Example: Chat Application

### Slice 1: Send a message (hardcoded user)
- Single user sends a message
- Message stored in memory (no database)
- No authentication
- No conversation list
- Tests: message created, message stored

### Slice 2: List messages (add database)
- Messages persist to SQLite
- Messages display in chronological order
- Still single user, no auth
- Tests: messages persist, messages ordered

### Slice 3: Multiple conversations
- User can create conversations
- Messages belong to conversations
- Conversation list in sidebar
- Tests: conversation CRUD, message scoping

### Slice 4: User authentication
- Users can sign up / log in
- Messages belong to authenticated users
- Session management
- Tests: auth flow, message ownership

### Slice 5: Error handling & edge cases
- Empty message validation
- Max message length
- Network error recovery
- Concurrent message handling
- Tests: all error paths

## Integration with TDD

Each slice follows strict TDD:
1. Write tests for the slice's behavior
2. Implement the slice
3. Verify all tests pass (including previous slices)
4. Refactor if needed

## Integration with Deferred Decisions

When slicing, explicitly identify which architectural decisions to defer:

| Slice | Current Implementation | Deferred To |
|-------|----------------------|-------------|
| 1-2 | In-memory storage | Slice 2 (SQLite) |
| 2-4 | SQLite | Final swap (Postgres) |
| 1-3 | No auth | Slice 4 |
| 1-5 | Hardcoded config | Post-completion (env vars) |
