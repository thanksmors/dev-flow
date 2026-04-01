"""Shared JSON output utility for gate scripts.

Prints machine-readable JSON after the human-readable output.
Format is designed for easy parsing by fix loop dispatch logic.

Ensure gates are run with PYTHONIOENCODING=utf-8 on Windows to prevent
UnicodeEncodeError when printing ASCII check symbols.
"""

import json
import sys
from typing import Any


def print_gate_json(
    gate: str,
    checks: list[dict[str, Any]],
    *,
    round: int = 1,
) -> None:
    """Print machine-readable JSON gate result.

    Args:
        gate: Gate name, e.g. "phase0", "phase5b", "phase6_start", "phase6_end"
        checks: List of check result dicts, each with keys:
            - check: str — human-readable check name
            - status: "pass" | "fail" | "skip"
            - message: str — human-readable detail
            - fix: str — one-sentence fix instruction (only if status == "fail")
            - missing: list[str] — list of specific missing items (optional)
        round: Fix loop round number (1, 2, or 3)
    """
    failing = [c for c in checks if c["status"] == "fail"]

    payload = {
        "status": "pass" if not failing else "fail",
        "gate": gate,
        "round": round,
        "checks": checks,
        "failing_count": len(failing),
        "fix_items": [
            {
                "check": c["check"],
                "fix": c.get("fix", "fix manually"),
                "missing": c.get("missing", []),
            }
            for c in failing
        ],
    }
    print(f"\n<!---\n{json.dumps(payload, indent=2)}\n-->")


def gate_exit(gate: str, checks: list[dict[str, Any]], *, round: int = 1) -> int:
    """Print human summary, JSON, then exit with appropriate code.

    Call this as the last thing in main().
    """
    print_gate_json(gate, checks, round=round)
    failing = [c for c in checks if c["status"] == "fail"]
    if failing:
        print(f"\nGate {gate}: FAIL")
        return 1
    print(f"\nGate {gate}: PASS")
    return 0
