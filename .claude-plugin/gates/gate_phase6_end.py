#!/usr/bin/env python3
"""Gate Phase 6 End: Deferred-decision gate — all open items must be resolved."""

import sys
import pathlib

PROJECT_ROOT = pathlib.Path.cwd()
TRACKER_PATH = PROJECT_ROOT / ".dev-flow" / "architecture" / "deferred-decisions.md"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _json_output import gate_exit

def parse_tracker(path: pathlib.Path) -> list[dict[str, str]]:
    """Parse the deferred-decisions tracker markdown into structured entries."""
    if not path.exists():
        return []
    content = path.read_text()
    entries = []
    current = {}
    current_name = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith('## '):
            if current_name and current:
                entries.append(current)
            current_name = stripped.removeprefix('## ').strip()
            current = {"name": current_name}
        elif ':' in stripped and current_name:
            key, _, val = stripped.partition(':')
            current[key.strip()] = val.strip()
    if current_name and current:
        entries.append(current)
    return entries

def check_open_decisions() -> dict:
    """Return check dict. Fail if any item is fake or pending."""
    if not TRACKER_PATH.exists():
        return {
            "check": "open_deferred_decisions",
            "status": "fail",
            "message": f"deferred decisions tracker: NOT FOUND at {TRACKER_PATH}",
            "fix": "Create .dev-flow/architecture/deferred-decisions.md with the tracker template",
            "missing": [],
        }
    entries = parse_tracker(TRACKER_PATH)
    open_items = [
        e for e in entries
        if e.get("Status", "").lower() in ("fake", "pending")
    ]
    if not open_items:
        return {"check": "open_deferred_decisions", "status": "pass", "message": "deferred decisions: all resolved", "fix": "", "missing": []}
    names = [e.get("name", "?") for e in open_items]
    return {
        "check": "open_deferred_decisions",
        "status": "fail",
        "message": f"{len(open_items)} open deferred decision(s): {', '.join(names)}",
        "fix": "Resolve, re-defer, or skip each open item in .dev-flow/architecture/deferred-decisions.md",
        "missing": names,
    }

def main() -> int:
    print("=== Gate Phase 6 End: Deferred-Decision Gate ===\n")
    print(f"Tracker: {TRACKER_PATH}\n")
    c = check_open_decisions()
    symbol = {"pass": "✅", "fail": "❌", "skip": "⏭️"}[c["status"]]
    print(f"{symbol} {c['message']}")
    if c["status"] == "fail":
        # Print detail for each open item
        entries = parse_tracker(TRACKER_PATH)
        open_items = [e for e in entries if e.get("Status","").lower() in ("fake","pending")]
        for item in open_items:
            print(f"  {item.get('name','?')} — Status: {item.get('Status','?')} — Deferred to: {item.get('Deferred to','?')}")
    print()
    return gate_exit("phase6_end", [c])

if __name__ == "__main__":
    sys.exit(main())
