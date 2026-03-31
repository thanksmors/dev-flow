---
name: preimplementation-gate
description: HARD-GATE verification before entering Phase 6 implementation
---

# Phase 5b: Pre-Implementation Gate

Run: `python3 ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase5b.py`

- Exit 0 → pre-implementation checks passed. Proceed to Phase 6.
- Exit 1 → gate failed.

**Fix Loop — Round 1:**
1. Parse the JSON block from the gate output (between `<!---\n` and `\n-->`)
2. Extract `fix_items` — each item has `check`, `fix`, and optionally `missing`
3. Dispatch one fix agent per failing item in parallel (max 3 agents)
4. Each fix agent: reads the fix instruction, fixes the specific item, verifies the fix worked
5. Re-run gate_phase5b.py
6. If exit 0 → print "✅ Gate fixed." Proceed to Phase 6.
7. If exit 1 → Round 2

**Fix Loop — Round 2 (if Round 1 didn't resolve):**
1. Re-parse JSON from gate output
2. Remaining items are harder — dispatch up to 2 agents, each with full context of what was already tried
3. Re-run gate_phase5b.py
4. If exit 0 → print "✅ Gate fixed after escalation." Proceed to Phase 6.
5. If exit 1 → present remaining issues to user. Options: [Pause] [End]

Tell the user: "Gate failed — running autonomous fix loop (Round 1). Will retry automatically."

This is a **HARD-GATE** — Phase 6 cannot begin until gate_phase5b.py exits 0.
