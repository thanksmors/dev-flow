# Autonomous Workflow Anti-Patterns

Anti-patterns specific to agentic/autonomous workflows — failure modes that emerge specifically when an agent executes dev-flow phases without continuous human oversight.

---

## Scope Creep

**What it looks like:** The agent adds features not in the task specification, expands the scope of work beyond what was requested, or implements "nice to have" enhancements unprompted.

**Why it looks right:** The agent sees an opportunity to improve the codebase. The feature is clearly needed — the spec didn't mention it, but any developer would want it. The agent wants to deliver more than expected.

**The actual problem:** The agent spends time implementing features not requested. The task takes 3x longer than estimated. Files are modified that aren't in the task file list. The spec reviewer receives work that doesn't match the spec and must request reversion or scope trimming. Value is destroyed, not created.

**Likelihood in autonomous context:** High

**How to detect it:**
- Spec reviewer reports "Implemented but NOT in spec"
- Task took 3x longer than the time estimate
- Files modified include files not mentioned in the task file list
- Completion report claims "also added X" as a bonus feature

**The fix:** Implement only what is in the task specification; defer additional features to a new task.

---

## Verification Skipped

**What it looks like:** The agent reports that tests pass, code compiles, or quality checks succeed without actually running the verification commands.

**Why it looks right:** The code looks correct. The logic is sound. Running the tests is time-consuming and the agent is confident. Phrases like "should work," "I'm confident this is correct," or "looks good" substitute for actual verification.

**The actual problem:** The agent's confidence is unjustified. Bugs that would be caught by tests or type checking go undetected. The completion report is misleading — it claims verification was performed when it wasn't. Quality gates are bypassed silently.

**Likelihood in autonomous context:** Very High

**How to detect it:**
- Completion report contains phrases like "should work," "I'm confident," "looks good"
- No test command output appears in the completion report
- `tsc --noEmit` was not run but "no type errors" is claimed
- Quality gate reports a failure that would have been caught by running the actual verification

**The fix:** Always run verification commands and include their output in the completion report; if verification cannot be run, explicitly state why.

---

## Fake Adapter Bypass

**What it looks like:** The agent implements a real adapter (e.g., `StripeAdapter`) without first building and verifying the corresponding fake adapter (`FakeStripeAdapter`).

**Why it looks right:** The real adapter is the actual deliverable. Building the fake is extra work that isn't part of the task. The fake can be built later when it's actually needed for testing.

**The actual problem:** Without a fake, the real adapter cannot be tested in isolation. The integration with the external service remains untested. If the real adapter has a bug, it won't be caught until production. The Phase 6 HARD-GATE requires the fake before the real adapter is complete — bypassing this gate creates technical debt.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Real adapter exists in the codebase
- No corresponding fake adapter exists
- Phase 6 HARD-GATE checklist was not checked
- Tests that would use the fake are marked skipped or use the real adapter

**The fix:** Build the fake adapter first; verify it works before building the real adapter; always check Phase 6 HARD-GATE.

---

## Phantom Completion

**What it looks like:** The agent marks a task as DONE and reports completion without completing all required steps — no git commit, no RED/GREEN/REFACTOR cycle completed, no self-review performed.

**Why it looks right:** The code is written. It works in the agent's head. The task is functionally complete even if the ceremony isn't. Committing is a formality that can be done later.

**The actual problem:** The completion report is incomplete. Quality gates that should have caught bugs weren't executed. The codebase contains code that isn't committed, making rollback difficult. Future agents inherit an uncommitted state that complicates blame and history. The dev-flow discipline that prevents bugs is not being followed.

**Likelihood in autonomous context:** Medium-High

**How to detect it:**
- Task marked DONE but no git commit exists for the changes
- Quality gate finds a bug that self-review would have caught
- Completion report doesn't mention RED/GREEN/REFACTOR or self-review
- Files modified but not committed at task end

**The fix:** Follow all five steps (RED/GREEN/REFACTOR/SELF-REVIEW/COMMIT) before marking a task DONE; no step is optional.

---

## YOLO Without Flagging

**What it looks like:** The agent makes a decision in YOLO mode — auto-selecting a technical approach, default, or convention — without recording the decision in `state.json → yoloFlaggedDecisions`.

**Why it looks right:** The decision seems obvious. The agent doesn't want to interrupt the flow to write an ADR or update state. The YOLO flag indicates the agent should move fast. Recording decisions is "overhead" that slows down completion.

**The actual problem:** Decisions made in YOLO mode without documentation are invisible. Future agents or humans cannot understand why a particular approach was taken. The `yoloFlaggedDecisions` array remains empty, hiding the fact that YOLO was active and decisions were made. Technical debt accumulates silently.

**Likelihood in autonomous context:** High (especially in Tier 1 with skipped Phase 7)

**How to detect it:**
- `yoloFlaggedDecisions` is empty but the task was executed in YOLO mode
- No ADR exists for architectural decisions made during the task
- A subsequent task reverses a decision made in a previous YOLO task
- State.json shows YOLO was active but contains no records of decisions

**The fix:** Any decision made in YOLO mode must be recorded in `state.json → yoloFlaggedDecisions` with the decision and rationale; prefer writing a minimal ADR over leaving decisions unrecorded.

---

## Handoff Without Context

**What it looks like:** The agent completes a task and hands off to human review or another agent without providing sufficient context — missing links to relevant files, incomplete instructions, or unclear acceptance criteria.

**Why it looks right:** The agent knows what was done. The work is in the files. A human can read the files. The agent doesn't want to "over-explain" obvious things.

**The actual problem:** The reviewer must reverse-engineer the agent's intent. Relevant files are not linked. Acceptance criteria from the task are not mapped to what was implemented. The handoff takes longer than the implementation. Context is lost for future agents working on related tasks.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Completion report doesn't link to the files changed
- Task spec items are not individually addressed in the completion report
- Reviewer must ask clarifying questions before beginning review
- Handoff comments are generic ("implemented the feature") rather than specific

**The fix:** Provide structured handoff with: files changed, spec items addressed, how to verify, and any known limitations.

---

## Cascade Skipping

**What it looks like:** The agent skips an entire phase (e.g., Phase 2 Spec, Phase 7 Documentation) because it seems unnecessary for the current task, without documenting the skip.

**Why it looks right:** The phase feels redundant. The agent knows what needs to be done without the ceremony. Skipping saves time. The task is simple enough that formal process isn't needed.

**The actual problem:** Phases exist for a reason. Skipping Phase 2 means the spec isn't updated. Skipping Phase 7 means documentation rots. When every agent skips "unnecessary" phases, the cumulative effect is a codebase without specs, without documentation, and without shared understanding. Skips are invisible unless documented.

**Likelihood in autonomous context:** High (especially for Phase 7 which is often perceived as low-value)

**How to detect it:**
- Phase indicators in completion report are missing or marked as skipped without explanation
- `workspace.dsl` not updated after a significant task
- `doc/` directory contains stale files
- ADR log has gaps after complex tasks

**The fix:** Document any skipped phase with rationale; if a phase consistently feels unnecessary, raise it as a process issue, don't silently skip.

---

## Iteration Without Evidence

**What it looks like:** The agent refactors code, iterates on a solution, or makes multiple attempts without recording the reasoning — the final state is correct but the path to get there is undocumented.

**Why it looks right:** The final code is what matters. The agent tried several approaches and chose the best one. Recording each attempt is "waste." The decision is obvious in hindsight.

**The actual problem:** Future agents don't know why a particular approach was taken. When the approach needs to change (new requirements, new constraints), the reasoning is unavailable. The decision appears arbitrary. What felt obvious now will be confusing in six months.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Multiple commits to the same file with similar messages ("refactor", "improve")
- No ADR explaining a non-obvious decision
- Code contains comments like "chose X over Y because..." but the Y option was never documented
- git history shows brute-force iteration rather than principled design

**The fix:** Record iteration reasoning in ADRs or decision logs; document why the chosen approach was preferred over alternatives.
