---
name: preimplementation-gate
description: HARD-GATE verification before entering Phase 6 implementation
---

# Phase 5b: Pre-Implementation Gate

Run: `python3 ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase5b.py`

- Exit 0 → pre-implementation checks passed. Proceed to Phase 6.
- Exit 1 → gate failed. Print the gate's full output. Then tell the user: "Gate failed — fix the issues above, then run `/dev-flow continue` to re-run."

This is a **HARD-GATE** — Phase 6 cannot begin until gate_phase5b.py exits 0.
