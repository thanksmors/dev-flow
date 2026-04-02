#!/usr/bin/env python3
"""PreCompact hook: save session state before context compaction.

Writes to .dev-flow/.last-compact.json so SessionStart can restore on resume.
"""

import json
import os
import sys
import pathlib
from datetime import datetime

PROJECT_ROOT = pathlib.Path.cwd()
DEV_FLOW_DIR = PROJECT_ROOT / ".dev-flow"
STATE_FILE = DEV_FLOW_DIR / ".last-compact.json"

def _file_hash(path: pathlib.Path) -> str | None:
    """Return first 64 chars of file content as identifier."""
    if not path.exists():
        return None
    try:
        return path.read_text()[:64]
    except Exception:
        return None

def save_state() -> None:
    """Write current session state to .last-compact.json."""
    DEV_FLOW_DIR.mkdir(exist_ok=True)

    compact_reason = os.environ.get("CLAUDE_COMPACT_REASON", "unknown")
    compact_start = os.environ.get("CLAUDE_COMPACT_START", "")

    # Read current state if exists
    current_state = {}
    if STATE_FILE.exists():
        try:
            current_state = json.loads(STATE_FILE.read_text())
        except Exception:
            pass

    state = {
        "saved_at": datetime.now().isoformat(),
        "compact_reason": compact_reason,
        "compact_start": compact_start,
        "cwd": str(PROJECT_ROOT),
        "phase": current_state.get("phase"),
        "gate_status": current_state.get("gate_status"),
        "gate_round": current_state.get("gate_round"),
        "open_items": current_state.get("open_items", []),
        "last_command": current_state.get("last_command"),
        "lessons_md_hash": _file_hash(PROJECT_ROOT / ".dev-flow" / "lessons.md"),
        "state_json_hash": _file_hash(PROJECT_ROOT / ".dev-flow" / "state.json"),
    }

    STATE_FILE.write_text(json.dumps(state, indent=2))

if __name__ == "__main__":
    try:
        save_state()
        print(f"PreCompact: state saved to {STATE_FILE}", file=sys.stderr)
    except Exception as e:
        print(f"PreCompact: failed to save state: {e}", file=sys.stderr)
        sys.exit(1)
