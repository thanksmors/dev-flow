#!/usr/bin/env python3
"""SessionStart hook: check for saved state and offer to restore context.

Reads .dev-flow/.last-compact.json. If it exists and is recent (< 4 hours),
prints a restore prompt to stdout that the agent sees and can act on.
"""

import json
import sys
import pathlib
from datetime import datetime, timedelta

PROJECT_ROOT = pathlib.Path.cwd()
STATE_FILE = PROJECT_ROOT / ".dev-flow" / ".last-compact.json"
MAX_AGE_HOURS = 4

def get_saved_state() -> dict | None:
    """Load saved state if it exists and is recent."""
    if not STATE_FILE.exists():
        return None
    try:
        state = json.loads(STATE_FILE.read_text())
    except Exception:
        return None
    saved_at = datetime.fromisoformat(state["saved_at"])
    if datetime.now() - saved_at > timedelta(hours=MAX_AGE_HOURS):
        return None
    return state

def format_restore_prompt(state: dict) -> str:
    """Format the restore prompt shown to the user."""
    lines = [
        "## Context Restored from Previous Session\n",
        f"Saved: {state['saved_at']}",
    ]
    if state.get("phase"):
        lines.append(f"Phase: {state['phase']}")
    if state.get("gate_status"):
        lines.append(f"Gate status: {state['gate_status']} (round {state.get('gate_round', '?')})")
    if state.get("last_command"):
        lines.append(f"Last command: {state['last_command']}")
    open_items = state.get("open_items", [])
    if open_items:
        lines.append(f"Open items: {', '.join(open_items)}")
    lines.append("")
    lines.append("Run `/dev-flow continue` to resume from where you left off.")
    return "\n".join(lines)

def main() -> None:
    state = get_saved_state()
    if state is None:
        print("SessionStart: no recent saved state found.", file=sys.stderr)
        return

    prompt = format_restore_prompt(state)
    # Print to stdout so Claude Code captures it as a message
    print(prompt)

    # Also write to a well-known path the command can read on resume
    restore_file = PROJECT_ROOT / ".dev-flow" / ".restore-prompt.txt"
    restore_file.write_text(prompt)

if __name__ == "__main__":
    main()
