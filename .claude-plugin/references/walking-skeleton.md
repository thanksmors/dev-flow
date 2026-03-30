# Walking Skeleton

## Concept

A walking skeleton is the **thinnest possible end-to-end implementation** of a system that still demonstrates the architecture works. It should:

- Compile and run
- Connect all major components (frontend → API → database)
- Demonstrate the basic data flow
- Be testable end-to-end
- Take hours, not days, to build

It's called a "skeleton" because it has the structure but none of the meat. It "walks" because it actually works end-to-end.

## Why Start with a Walking Skeleton?

1. **Validate architecture early**: Prove the tech stack works together before investing in features
2. **Establish patterns**: Set up the project structure, build tools, and conventions once
3. **Enable vertical slicing**: Once the skeleton exists, each feature slice plugs into it
4. **Reduce risk**: Catch integration problems immediately, not after weeks of development
5. **Provide a test baseline**: All future tests build on the skeleton's passing state

## What to Include

### MUST Include
- Project setup (package manager, build tools, dev scripts)
- Basic folder structure
- One end-to-end path through the system
- At least one test (even trivial) that proves the path works
- Database connection (even if using the simplest option)
- API server that starts and responds
- Frontend that renders something from the API

### MUST NOT Include
- Feature logic (beyond the trivial demo)
- Error handling (beyond what the framework provides)
- Authentication/authorization
- Configuration management
- Multiple routes/endpoints
- Styling/polish
- Performance optimizations

## How to Build It

### Step 1: Project Setup
- Initialize the project with the chosen tech stack
- Set up build tools and dev scripts
- Create the folder structure
- Verify the project builds and tests run (even with no tests yet)

### Step 2: Backend Skeleton
- Create the simplest possible API endpoint
- Connect to the simplest possible data store
- Write one test that hits the endpoint and gets a response
- Example: `GET /health` returns `{"status": "ok"}`

### Step 3: Frontend Skeleton
- Create the simplest possible page
- Make a call to the backend API
- Display the response
- Write one test that verifies the page loads

### Step 4: End-to-End Verification
- Start the full stack
- Verify data flows from frontend through API to database and back
- Run all tests — all must pass
- Commit: `feat: walking skeleton`

## Example: Chat Application Walking Skeleton

```
Backend:
  - POST /api/messages → saves message to SQLite → returns saved message
  - GET /api/messages → returns all messages from SQLite
  - One test: "POST /api/messages saves and returns a message"

Frontend:
  - Input field + send button
  - On submit: POST message, then GET messages, display them
  - One test: "app renders message list"

Database:
  - Single `messages` table with `id, content, created_at`
  - SQLite (simplest option — will swap to Postgres later)
```

This skeleton proves:
- Bun + Hono works as a backend
- React + Vite works as a frontend
- bun:sqlite works for storage
- Frontend can talk to backend
- Tests can run against the stack

Everything else (auth, conversations, council flow, etc.) builds on this foundation.

## Deferred Decisions in the Walking Skeleton

The walking skeleton is where you make your first deferred decisions:

| Decision | Skeleton Choice | Production Choice | Adapter |
|----------|----------------|-------------------|---------|
| Database | SQLite | PostgreSQL | Repository interface |
| Auth | None (hardcoded user) | JWT/OAuth | Auth middleware interface |
| Config | Hardcoded | Environment vars | Config loader interface |
| Transport | HTTP | (same) | Not deferred |
| Frontend state | Local state | State manager | Store interface |

Each adapter interface is defined in the skeleton but implemented with the simplest option. The interface stays stable while the implementation swaps later.
