# Why: Vertical Slices

## Definition: A Vertical Slice

A vertical slice is a thin cut through all layers of the architecture for a single feature. It includes:
- The UI component or page that triggers the feature
- The business logic that processes the request
- The data layer that stores or retrieves the result
- The full end-to-end path from user action to system response

A vertical slice is the opposite of a horizontal layer. Horizontal layers build all of one type of thing before moving to the next (all UI, then all business logic, then all data). Vertical slices build one feature end-to-end before moving to the next.

---

## Why Horizontal Layers Create Longest Feedback Cycles

When you build horizontally, you defer integration until late in the project. You might spend two weeks building all the UI components, then two weeks building all the business logic, then two weeks wiring everything together. When the integration fails, you have no idea whether the problem is in the UI layer, the business logic, or the data layer — because nothing was ever connected before.

The feedback cycle for a horizontal approach is the entire length of the project. You find out if the architecture works when you try to connect the last layer. By then, fixing a broken interface or a wrong assumption is expensive, because a lot of code depends on it.

Worse, horizontal layers create social dynamics that make it hard to fix problems. Someone "owns" the UI layer, someone else owns the business logic. When the integration fails, ownership disputes begin. "The UI sent the right data, it's the business logic's fault." Everyone has plausible deniability because nothing was ever proven to work end-to-end.

---

## Why Vertical Slices Surface Integration Problems Immediately

When you build vertically, each slice is independently verifiable. You build the thinnest possible version of the feature — from UI to data — and you verify it works before moving on.

If there is a problem with the interface between layers, you find out immediately, while the code is fresh in your mind, while the cost to fix it is low. The slice either works or it doesn't. There is no ambiguity.

This also changes the social dynamics of development. When a slice is end-to-end, it either works or it doesn't, and everyone can see which slice is failing. The accountability is clear. There is no "my part works, the integration is someone else's problem" because the slice includes the integration.

---

## Elephant Carpaccio: Slice Thin, Not Wide

The elephant carpaccio technique is a practice from agile estimation and delivery. The metaphor: you cannot eat an elephant in one bite, but you can eat it one thin slice at a time.

When applied to vertical slices, it means: slice features on acceptance criteria, not on functional areas. Each slice should represent one discrete unit of value that delivers something measurable.

Bad slice: "Build the user authentication system" (too wide, takes months, no feedback until the end)

Good slices:
1. "Show a login form that accepts email and password" (UI only, fake response)
2. "Wire the form to a fake auth adapter that returns a user" (full stack, fake)
3. "Swap fake auth for a real auth adapter" (real integration)
4. "Show an error when credentials are invalid" (error path)
5. "Remember the session across page refreshes" (session management)

Each of these slices is independently verifiable, independently commit-able, and delivers measurable value. You can show the first slice to a stakeholder after a day, not after three months.

---

## Why This Matters for Autonomous Agents

Autonomous agents benefit disproportionately from vertical slices for several reasons:

**Each slice is independently verifiable.** The agent does not need a human to tell it whether the slice works. It runs the tests. The tests pass or they don't. The slice is done or it isn't.

**Each slice is independently commit-able.** A vertical slice is small enough to review in one PR. The reviewer can understand the full context — what changed, why, and how to verify it — in a single sitting. No sprawling PRs that require understanding three months of parallel work.

**Each slice reduces risk.** If a slice goes wrong, you have not invested months of work on a broken foundation. You revert one small PR. The cost of recovery is low.

**Slices create natural checkpoints.** At the end of each slice, the agent can stop and report. The human can review direction, correct course, or escalate. The agent is not running for weeks on a direction that was wrong from day one.

**Architectural drift is visible early.** If a slice's implementation starts to diverge from the port/adapter architecture, you find out on slice 3, not slice 30. The cost to correct is tiny compared to refactoring a sprawling, untested codebase.

---

## Summary

Vertical slices are not just a development technique. They are a risk management strategy. By keeping slices thin, end-to-end, and independently verifiable, you shorten feedback cycles, surface problems early, and give autonomous agents clear, objective markers of progress. The alternative — horizontal layers with late integration — is the most reliable way to build a system that fails quietly until it is too expensive to fix.
