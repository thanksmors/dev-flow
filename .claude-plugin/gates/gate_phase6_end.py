#!/usr/bin/env python3
"""Gate Phase 6 End: Deferred-decision gate — all open items must be resolved."""

import sys
import pathlib

PROJECT_ROOT = pathlib.Path.cwd()
TRACKER_PATH = PROJECT_ROOT / ".dev-flow" / "architecture" / "deferred-decisions.md"

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

def check_open_decisions() -> tuple[bool, list[dict[str, str]]]:
    """Return (pass, open_items). Pass=False if any item is fake or pending."""
    entries = parse_tracker(TRACKER_PATH)
    open_items = [
        e for e in entries
        if e.get("Status", "").lower() in ("fake", "pending")
    ]
    if open_items:
        return False, open_items
    return True, []

def main() -> int:
    print("=== Gate Phase 6 End: Deferred-Decision Gate ===\n")
    print(f"Tracker: {TRACKER_PATH}\n")

    passed, open_items = check_open_decisions()

    if passed:
        print("✅ No open deferred decisions.\n")
        print("Gate Phase 6 End: PASS")
        return 0

    print(f"❌ {len(open_items)} open deferred decision(s):\n")
    for item in open_items:
        name = item.get("name", "Unknown")
        status = item.get("Status", "?")
        deferred_to = item.get("Deferred to", "?")
        trigger = item.get("Trigger Criteria", "?")
        print(f"  {name}")
        print(f"    Status: {status}")
        print(f"    Deferred to: {deferred_to}")
        print(f"    Trigger: {trigger}")
        print()
    print("Handle all open items before proceeding to Phase 7.\n")
    print("Gate Phase 6 End: FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
