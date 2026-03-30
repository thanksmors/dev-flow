# Why: HARD-GATE Markers

## What a HARD-GATE Is

A HARD-GATE is a barrier in the workflow that cannot be crossed until specific criteria are met. Unlike suggestions, recommendations, or best practices, a HARD-GATE is enforced. An autonomous agent reading a HARD-GATE either meets the criteria or stops and reports why it cannot.

The word "HARD" is not rhetorical. It means: do not pass this point. The gate is not a yellow light you can run. It is a locked door, and the key is meeting the criteria.

---

## What Happens Without Gates

Without hard gates, teams fall into a common trap: they defer quality work "for later" and keep moving forward because the code "basically works." Each compromise compounds. By the time the project is half-done, the foundation is rotten and nobody wants to say so because there's too much built on top of it.

Here is the pattern:
1. Phase 2 is rushed. Some Phase 1 artifacts are incomplete. "We'll fix it in Phase 3."
2. Phase 3 builds on incomplete Phase 2 artifacts. It takes twice as long as expected.
3. Phase 4 discovers that the foundation doesn't support what was promised.
4. The team is now halfway through the project with a broken foundation and no easy way out.

Without gates, quality debt accumulates interest. And unlike financial debt, technical debt at the end of a project is often invisible — it manifests as slow progress, constant bugs, and the creeping feeling that the system was never quite right.

The HARD-GATE exists to break this pattern. By requiring Phase N artifacts to be complete before Phase N+1 begins, you catch problems when they are small, cheap, and easy to fix.

---

## Why Phase Gates Specifically

Each phase in the workflow produces artifacts that the next phase depends on. Phase 1 produces the requirements and acceptance criteria. Phase 2 produces the architecture and port interfaces. Phase 3 produces the test suite. Phase 4 produces the implementation. Each phase's output is the next phase's input.

If Phase 2's port interfaces are wrong, every phase that follows will build on wrong interfaces. The cost to fix it grows exponentially:
- Phase 2 fix: rename a function and update three callers
- Phase 4 fix: rename a function, update three callers, rewrite two tests, re-review the acceptance criteria, and update the generated report

Phase gates ensure that each phase's artifacts are complete and correct before the next phase starts. This is the only way to keep the cost of changes low.

---

## The Three HARD-GATEs

### HARD-GATE 5b: Can We Implement?

Before any production code is written for a vertical slice, the agent must answer: do we have everything we need to implement this? This gate is checked after Phase 5 (Planning) and before Phase 6 (Implementation) begins.

At this gate, the agent verifies:
- All port interfaces for this slice are defined and reviewed
- A fake adapter exists and is wired into every port
- The test-first implementation plan is written
- There are no unknown unknowns — no "we'll figure it out during implementation" items remaining

If any of these are missing, the agent cannot proceed. It must complete the missing items or escalate.

Why this gate matters: implementing without a plan is guessing. Implementing without defined ports is building on quicksand. This gate ensures the agent knows exactly what it is building and has a clear path to building it.

### HARD-GATE 7: Did We Build It Right?

After implementation and before declaring a slice complete, the agent must prove the implementation is correct. This gate is checked during Phase 7 (verification).

At this gate, the agent verifies:
- All tests pass (unit, integration, and any UI-level tests)
- The fake adapter was used as the test fixture throughout
- No test was written after the code it tests — all tests are red-first
- The implementation matches the acceptance criteria from Phase 2
- No code was added beyond what the tests required

If tests are missing, if they were written after the code, or if the implementation diverges from the spec, the agent cannot pass this gate. It must write the missing tests, rewrite the incorrect tests, or fix the implementation.

Why this gate matters: red-first testing is the only way to know your code does what you intended. Tests written after the code verify what the code does, not what you wanted it to do. This gate enforces the discipline that makes the test suite a reliable safety net.

### HARD-GATE 8: Is the Report Complete?

Before a vertical slice is considered done, a completion report must be generated and verified. This gate is checked at the end of Phase 8 (reporting).

At this gate, the agent verifies:
- All required sections are present in the report
- Every artifact listed in the report exists in the codebase
- The report accurately reflects what was built, tested, and verified
- Any deferred decisions are documented with their swap criteria and triggers

If the report is incomplete or inaccurate, the slice is not done. The report is not paperwork — it is the permanent record of what was built, why decisions were made, and what was deferred. Future developers (including future-you) will rely on this report to understand the system.

---

## What "Blocking" Means in Autonomous Mode

In an autonomous agent context, "blocking" does not mean "the agent should stop and ask a human for permission." It means the agent cannot proceed to the next step until it meets the criteria.

When an agent encounters a HARD-GATE it cannot pass:
1. It identifies which criteria are not met
2. It attempts to meet them (write the missing tests, fix the broken code, fill in the missing documentation)
3. If it cannot meet them autonomously, it stops and reports exactly what is missing and why
4. It does not guess, approximate, or "move on with a TODO"

This is different from a human checkpoint, where a person might say "good enough, we'll fix it later." The agent does not have the judgment to know when "later" is actually coming. HARD-GATEs enforce the discipline consistently, every time, without relying on human memory or goodwill.

---

## Why This Is Better Than Human Checkpoints

Human checkpoints sound good in theory. A senior engineer reviews the work before moving to the next phase. But in practice:
- Humans get busy, rush reviews, or trust that "the team knows what they're doing"
- Checkpoints become rubber stamps rather than real gates
- The review happens at a point where significant work is already done, making rejection expensive and uncomfortable
- In autonomous workflows, there may be no human in the loop during execution

HARD-GATEs are programmatic and consistent. They run every time, on every slice, for every agent. They do not get tired, rushed, or politically compromised.

The tradeoff is that HARD-GATEs require well-defined criteria. You cannot gate on "is this good?" — you gate on "does this test pass?" and "does this artifact exist?" The discipline of making gates concrete is what makes them enforceable.

---

## Summary

HARD-GATEs exist to make quality non-negotiable. Without them, debt accumulates quietly until it becomes impossible to recover. With them, problems are caught early, when they are small and fixable. The three gates — can we implement, did we build it right, is the report complete — cover the full lifecycle of a vertical slice and ensure each phase's artifacts are complete before the next phase begins.
