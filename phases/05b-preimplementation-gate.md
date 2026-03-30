---
name: preimplementation-gate
description: HARD-GATE verification before entering Phase 6 implementation
---

# Phase 5b: Pre-Implementation Gate

<HARD-GATE>
You CANNOT begin Phase 6 (Implementation) until ALL of the following are true:

✅ Phase 5 planning is complete (`.dev-flow/plans/implementation.md` exists and contains tasks)
✅ All previous phases are complete (phases 1–5 in completedPhases)
✅ User has approved the plan at the Phase 5 checkpoint
✅ Execution mode has been selected (Sequential Subagents)
✅ YOLO mode has been confirmed (if applicable)
</HARD-GATE>

If any gate item is false:
→ State which gate item is unmet
→ Do not proceed to Phase 6

If all gate items are true:
→ Log gate pass in state.json
→ Proceed to Phase 6
