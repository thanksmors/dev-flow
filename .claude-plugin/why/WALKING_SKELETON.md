# Why: Walking Skeleton

## What a Walking Skeleton Is

A walking skeleton is the thinnest possible end-to-end slice of your system. It is not a prototype, not a proof-of-concept, and not throwaway code. It is a minimal version of your real system that:

- Connects every architectural layer (UI → port → adapter → external service)
- Returns real, typed data through every layer
- Uses production-quality structure and patterns
- Stays in the codebase permanently as your first passing slice

Think of it as the frame of a house. Before you add walls, insulation, or paint, you want to know the frame can hold weight. The skeleton proves the structure works before you invest in finishing materials.

---

## Why Fake Adapters First

The first thing you wire into the skeleton is fake adapters. Not because we expect the code to stay fake, but because fake adapters give you something invaluable at this stage: **total control over time and environment**.

With fake adapters:
- No credentials needed. No API keys, no tokens, no secrets.
- No network required. You can work on a plane, in a basement, or in a data center with no internet.
- No rate limits. You can run a thousand tests in a second.
- No external dependency outages. The external service can be down, rebranded, or not built yet, and you keep working.
- Deterministic behavior. Fake adapters return exactly what you program them to return, every time.

Starting with real adapters is like learning to drive by taking the car on the highway before you've touched a steering wheel. You don't know if your code works, if your interfaces are right, or if your data shapes are correct — because you're also fighting against infrastructure you don't control yet.

---

## Why Real Adapters Before Fakes Walk Is a Blocker

Here is the trap teams fall into: they decide "we'll use Postgres, so let's set up Postgres first." Then they spend two days getting Postgres running, another day configuring it, another day writing migrations, and only then do they discover that the port interface they designed doesn't map cleanly to Postgres's query model.

Now they have two problems at once: a broken interface design AND an infrastructure problem. Debugging becomes a maze of "is it the adapter, the database, the network, or my interface?"

The walking skeleton exists to separate these concerns. By the time you touch a real adapter:
- Your port interface is already validated by the fake adapter
- Your data shapes are already correct (the fake adapter returned them, the UI consumed them)
- Your integration is already proven — it just used fake data

Swapping in a real adapter is then a low-risk operation. You are replacing something known-working with something new, one adapter at a time.

---

## What "Walking" Actually Means

A skeleton walks when every layer in every vertical slice returns realistic data end-to-end. Here is what that looks like:

| Check | What It Proves |
|---|---|
| UI calls a port composable | Components don't import adapters directly |
| Port delegates to a fake adapter | Port follows the adapter pattern correctly |
| Fake adapter returns typed data | Data shapes are correct for this domain |
| Component renders the returned data | The full loop from request to display works |
| Auth port returns a fake user | Auth boundary is real, not just claimed |
| Auth-gated page respects the port response | Auth is enforced, not bypassed |

All boxes checked means the structure is sound. You have proven that data can flow from a fake source through every layer to the screen. The path exists. Now you just replace the scenery.

---

## The Swap Sequence

Once the skeleton walks, real adapters are introduced one at a time, one slice at a time. The entire change is changing one import line in one port file.

For example, to swap the task adapter:

```typescript
// In layers/tasks/ports/TaskPort.ts
// BEFORE (fake)
import { fakeTaskAdapter } from '~/layers/tasks/adapters/FakeTaskAdapter'

// AFTER (real)
import { instforgeTaskAdapter } from '~/layers/tasks/adapters/InstforgeTaskAdapter'
```

That is the entire diff. One line. The port interface doesn't change. The component doesn't change. The data shapes don't change. You are proving the real adapter satisfies the same contract the fake adapter already satisfied.

The sequence is:
1. Task domain — swap fake → real for the primary workflow
2. Agent domain — swap fake → real for orchestration
3. Auth domain — swap fake → real for identity
4. Observability — swap fake → real for logging and metrics

One PR per swap. Each PR is small, reviewable in minutes, and revertable with one line change.

---

## Why the Fake Adapter Never Gets Deleted

You might wonder: once the real adapter is working, why keep the fake one around?

Because the fake adapter is now a test fixture. It is the fastest, most reliable test double you have. Your unit tests can import the fake adapter directly. Your integration tests can use it to simulate success and failure conditions without touching the network. Your UI tests can render components with predictable, deterministic data.

Deleting the fake adapter means every test that depended on it now needs mocking setup, network mocking, or worse — becomes an integration test that hits a real service.

The fake adapter earned its place. It walked before it ran. It stays as the foundation of your test suite.

---

## Summary

The walking skeleton is not a shortcut. It is a specific technique with a specific purpose: prove the architecture works before you invest in infrastructure. Fake adapters make that fast and safe. The swap sequence makes it low-risk. And the fake adapter's permanent home in the test suite pays dividends forever.
