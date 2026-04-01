#!/usr/bin/env python3
"""Gate Phase 5b: Pre-implementation gate — verify plan is ready before Phase 6."""

import sys
import pathlib

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / "docs" / "superpowers" / "plans"
STATE_PATH = PROJECT_ROOT / ".dev-flow" / "state.json"
TRACKER_PATH = PROJECT_ROOT / ".dev-flow" / "architecture" / "deferred-decisions.md"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _json_output import gate_exit

def find_latest_plan() -> pathlib.Path | None:
    """Find the most recently modified .md plan file, excluding premortem plans."""
    if not PLANS_DIR.exists():
        return None
    plan_files = [
        f for f in PLANS_DIR.glob("*.md")
        if "premortem" not in f.stem.lower()
    ]
    if not plan_files:
        return None
    return max(plan_files, key=lambda f: f.stat().st_mtime)

PLAN_PATH = find_latest_plan()

def check_plan_exists() -> dict:
    if PLAN_PATH is None:
        return {
            "check": "plan_exists",
            "status": "fail",
            "message": f"implementation plan: NOT FOUND — no .md plan file in {PLANS_DIR}",
            "fix": f"Run Phase 5 planning to create a plan file in {PLANS_DIR}",
            "missing": [],
        }
    if PLAN_PATH.exists():
        return {"check": "plan_exists", "status": "pass", "message": f"implementation plan: OK ({PLAN_PATH.name})", "fix": "", "missing": []}
    return {
        "check": "plan_exists",
        "status": "fail",
        "message": f"implementation plan: NOT FOUND at {PLAN_PATH}",
        "fix": "Run Phase 5 planning to create a plan file",
        "missing": [],
    }

def check_deferred_decisions_clean() -> dict:
    """No deferred decisions with Status=fake should be pending."""
    if not TRACKER_PATH.exists():
        return {"check": "deferred_decisions", "status": "skip", "message": "deferred decisions tracker: not found (skipping)", "fix": "", "missing": []}
    content = TRACKER_PATH.read_text()
    fake_lines = [l for l in content.split('\n') if 'Status:' in l and ('fake' in l.lower() or 'pending' in l.lower())]
    if fake_lines:
        return {
            "check": "deferred_decisions",
            "status": "fail",
            "message": f"deferred decisions: {len(fake_lines)} item(s) still open (fake/pending)",
            "fix": "Handle all fake/pending deferred decisions in .dev-flow/architecture/deferred-decisions.md",
            "missing": [f"open deferred decision #{i+1}" for i in range(len(fake_lines))],
        }
    return {"check": "deferred_decisions", "status": "pass", "message": "deferred decisions: all resolved or swapped", "fix": "", "missing": []}

def main() -> int:
    checks = [
        check_plan_exists(),
        check_deferred_decisions_clean(),
    ]
    for c in checks:
        symbol = {"pass": "✅", "fail": "❌", "skip": "⏭️"}[c["status"]]
        print(f"{symbol} {c['message']}")
    return gate_exit("phase5b", checks)

if __name__ == "__main__":
    sys.exit(main())
