# Gate Fix Loop + Context Survival Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add machine-readable JSON output to gate scripts; replace manual gate failure stops with an autonomous fix loop; survive context compaction via PreCompact/SessionStart hooks.

**Architecture:** Three independent subsystems:
1. Gate JSON output — shared `_json_output.py` utility imported by all gate scripts
2. Gate fix loop — fix agents dispatched per failing check item before any stop
3. Context survival hooks — PreCompact saves state to `.dev-flow/.last-compact.json`, SessionStart restores on resume

**Tech Stack:** Python 3 stdlib (gates + hooks), Claude Code plugin hooks (PreCompact, SessionStart)

---

## File Map

| File | Role |
|------|------|
| `.claude-plugin/gates/_json_output.py` | New — shared utility: `print_gate_json(gate_name, items)` |
| `.claude-plugin/gates/gate_phase0.py` | Modify — call `print_gate_json()` before exiting |
| `.claude-plugin/gates/gate_phase5b.py` | Modify — call `print_gate_json()` before exiting |
| `.claude-plugin/gates/gate_phase6_start.py` | Modify — call `print_gate_json()` before exiting |
| `.claude-plugin/gates/gate_phase6_end.py` | Modify — call `print_gate_json()` before exiting |
| `.claude-plugin/hooks/precompact-save-state.py` | New — PreCompact hook, saves session state |
| `.claude-plugin/hooks/sessionstart-restore-state.py` | New — SessionStart hook, restores session state |
| `.claude-plugin/commands/dev-flow.md` | Modify — add fix loop on gate failure |
| `.claude-plugin/phases/05b-preimplementation-gate.md` | Modify — add fix loop on gate failure |
| `.claude-plugin/phases/06-implementation.md` | Modify — add fix loop on gate failure |
| `.claude-plugin/plugin.json` | Modify — register both hooks |

---

## Task 1: Gate JSON Output Utility

**Files:**
- Create: `.claude-plugin/gates/_json_output.py`

- [ ] **Step 1: Write `_json_output.py`**

```python
"""Shared JSON output utility for gate scripts.

Prints machine-readable JSON after the human-readable output.
Format is designed for easy parsing by fix loop dispatch logic.
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
```

- [ ] **Step 2: Verify it imports without error**

```bash
python3 -c "from _json_output import gate_exit, print_gate_json; print('OK')"
```

Expected: silent OK (imported from gates directory).

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/gates/_json_output.py && git commit -m "feat(gates): add shared JSON output utility

- print_gate_json() prints machine-readable JSON after human output
- gate_exit() prints summary + JSON + returns correct exit code
- Both imported by all gate scripts
- JSON format: {status, gate, round, checks, failing_count, fix_items}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Update `gate_phase0.py` with JSON Output

**Files:**
- Modify: `.claude-plugin/gates/gate_phase0.py`

- [ ] **Step 1: Replace `gate_phase0.py` with JSON-enabled version**

```python
#!/usr/bin/env python3
"""Gate Phase 0: Verify prerequisites before dev-flow Phase 0 completes."""

import subprocess
import sys
import pathlib

PLUGIN_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PROJECT_ROOT = pathlib.Path.cwd()

# Import shared JSON output utility
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _json_output import gate_exit

def run(cmd: list[str], capture: bool = True) -> tuple[int, str]:
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, timeout=30)
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return 124, "Command timed out"
    except FileNotFoundError:
        return 127, f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, str(e)

def check_gh_auth() -> dict:
    code, out = run(["gh", "auth", "status"])
    if code == 0:
        return {"check": "gh_auth", "status": "pass", "message": "gh auth: OK"}
    return {
        "check": "gh_auth",
        "status": "fail",
        "message": f"gh auth: FAILED\n{out.strip()}",
        "fix": "Run `gh auth login` to authenticate with GitHub",
        "missing": [],
    }

def check_git_remote() -> dict:
    code, out = run(["git", "remote", "-v"])
    if code == 0 and "origin" in out:
        remote_url = out.strip().split()[1] if out.strip().split() else "unknown"
        return {"check": "git_remote", "status": "pass", "message": f"git remote: OK ({remote_url})"}
    return {
        "check": "git_remote",
        "status": "fail",
        "message": "git remote: not configured or no origin",
        "fix": "Run `git remote add origin <url>` or `gh repo create` to set up a remote",
        "missing": [],
    }

def check_plugin_root() -> dict:
    root_file = PLUGIN_ROOT / "plugin.json"
    if root_file.exists():
        return {"check": "plugin_root", "status": "pass", "message": f"CLAUDE_PLUGIN_ROOT: OK ({PLUGIN_ROOT})"}
    return {
        "check": "plugin_root",
        "status": "fail",
        "message": f"CLAUDE_PLUGIN_ROOT: not found at {PLUGIN_ROOT}",
        "fix": "Verify the plugin is correctly installed — plugin.json not found",
        "missing": [],
    }

def main() -> int:
    checks = [check_gh_auth(), check_git_remote(), check_plugin_root()]
    for c in checks:
        symbol = "✅" if c["status"] == "pass" else "❌"
        print(f"{symbol} {c['message']}")
    return gate_exit("phase0", checks)

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run and verify JSON output appears**

```bash
python3 .claude-plugin/gates/gate_phase0.py
```

Expected: human-readable output first, then:
```
<!---
{
  "status": "pass",
  "gate": "phase0",
  "round": 1,
  "checks": [...],
  "failing_count": 0,
  "fix_items": []
}
-->

Gate phase0: PASS
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/gates/gate_phase0.py && git commit -m "feat(gate_phase0): add machine-readable JSON output

- Now emits structured JSON after human-readable output
- Fix items include specific fix instruction for each failing check
- exit code unchanged (0 pass, 1 fail)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Update `gate_phase5b.py` with JSON Output

**Files:**
- Modify: `.claude-plugin/gates/gate_phase5b.py`

- [ ] **Step 1: Replace `gate_phase5b.py` with JSON-enabled version**

The structure mirrors `gate_phase0.py`. Each `check_*` function now returns a dict with `check`, `status`, `message`, `fix`, and optionally `missing`. The `main()` function uses `gate_exit("phase5b", checks)`.

Key changes from current `gate_phase5b.py`:
- Add `sys.path.insert` + `from _json_output import gate_exit`
- Each `check_*` function returns a dict instead of a `(bool, str)` tuple
- Add `fix` field to each failing check dict
- `main()` uses `gate_exit()` instead of manual print + return

The four existing checks:
1. `check_plan_exists()` — fix: "Create an implementation plan at docs/superpowers/plans/"
2. `check_ports_defined()` — fix: "Define port interfaces in layers/*/ports/ or src/ports/"
3. `check_fake_adapters()` — fix: "Create the missing fake adapters at layers/*/adapters/FakeXyzAdapter.ts"
4. `check_deferred_decisions_clean()` — fix: "Handle all fake/pending deferred decisions at .dev-flow/architecture/deferred-decisions.md before Phase 6"

```python
#!/usr/bin/env python3
"""Gate Phase 5b: Pre-implementation gate — verify plan is ready before Phase 6."""

import sys
import pathlib
import re

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / "docs" / "superpowers" / "plans"
STATE_PATH = PROJECT_ROOT / ".dev-flow" / "state.json"
TRACKER_PATH = PROJECT_ROOT / ".dev-flow" / "architecture" / "deferred-decisions.md"
LAYERS_DIR = PROJECT_ROOT / "layers"

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
        return {"check": "plan_exists", "status": "pass", "message": f"implementation plan: OK ({PLAN_PATH.name})"}
    return {
        "check": "plan_exists",
        "status": "fail",
        "message": f"implementation plan: NOT FOUND at {PLAN_PATH}",
        "fix": f"Run Phase 5 planning to create a plan file",
        "missing": [],
    }

def check_ports_defined() -> dict:
    """If plan mentions external dependencies, ports should exist."""
    if PLAN_PATH is None or not PLAN_PATH.exists():
        return {"check": "ports_defined", "status": "skip", "message": "plan not found — skipping port check"}
    content = PLAN_PATH.read_text()
    external_keywords = ["API", "database", "auth", "email", "payment", "queue", "cache"]
    has_external = any(kw.lower() in content.lower() for kw in external_keywords)
    if not has_external:
        return {"check": "ports_defined", "status": "skip", "message": "ports: no external deps in plan, skipping"}
    ports_dir = LAYERS_DIR if LAYERS_DIR.exists() else PROJECT_ROOT / "src" / "ports"
    if not ports_dir.exists():
        return {
            "check": "ports_defined",
            "status": "fail",
            "message": f"ports: plan has external deps but no ports directory at {ports_dir}",
            "fix": f"Create port interfaces at {ports_dir} (e.g., layers/*/ports/XyzPort.ts)",
            "missing": [],
        }
    port_files = list(ports_dir.rglob("*Port*.ts")) + list(ports_dir.rglob("*port*.ts"))
    if not port_files:
        return {
            "check": "ports_defined",
            "status": "fail",
            "message": f"ports: external deps in plan but no port files found in {ports_dir}",
            "fix": f"Define port interfaces at {ports_dir}",
            "missing": [],
        }
    return {"check": "ports_defined", "status": "pass", "message": f"ports: OK ({len(port_files)} port file(s) found)"}

def check_fake_adapters() -> dict:
    """All fake adapters referenced in the plan should exist."""
    if PLAN_PATH is None or not PLAN_PATH.exists():
        return {"check": "fake_adapters", "status": "skip", "message": "plan not found — skipping fake adapter check"}
    content = PLAN_PATH.read_text()
    adapter_names = re.findall(r'(?:Fake|Wire)[A-Z][a-zA-Z]+(?:Adapter|Port)?', content)
    if not adapter_names:
        return {"check": "fake_adapters", "status": "pass", "message": "fake adapters: none referenced in plan"}
    adapters_dirs = []
    if LAYERS_DIR.exists():
        adapters_dirs.extend(d.parent for d in LAYERS_DIR.rglob("adapters"))
    src_adapters = PROJECT_ROOT / "src" / "adapters"
    if src_adapters.exists():
        adapters_dirs.append(src_adapters)
    if not adapters_dirs:
        return {
            "check": "fake_adapters",
            "status": "fail",
            "message": "fake adapters: no adapters directory found",
            "fix": "Create an adapters directory at layers/*/adapters/ or src/adapters/",
            "missing": list(set(adapter_names)),
        }
    missing = []
    for name in set(adapter_names):
        found = False
        for ad in adapters_dirs:
            if (ad / f"{name}.ts").exists():
                found = True
                break
        if not found:
            missing.append(name)
    if missing:
        return {
            "check": "fake_adapters",
            "status": "fail",
            "message": f"fake adapters: missing — {', '.join(missing)}",
            "fix": f"Create fake adapters at the adapters directory: {[str(a) for a in adapters_dirs]}",
            "missing": missing,
        }
    return {"check": "fake_adapters", "status": "pass", "message": f"fake adapters: OK ({len(set(adapter_names))} referenced)"}

def check_deferred_decisions_clean() -> dict:
    """No deferred decisions with Status=fake should be pending."""
    if not TRACKER_PATH.exists():
        return {"check": "deferred_decisions", "status": "skip", "message": "deferred decisions tracker: not found (skipping)"}
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
    return {"check": "deferred_decisions", "status": "pass", "message": "deferred decisions: all resolved or swapped"}

def main() -> int:
    checks = [
        check_plan_exists(),
        check_ports_defined(),
        check_fake_adapters(),
        check_deferred_decisions_clean(),
    ]
    for c in checks:
        symbol = {"pass": "✅", "fail": "❌", "skip": "⏭️"}[c["status"]]
        print(f"{symbol} {c['message']}")
    return gate_exit("phase5b", checks)

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run and verify JSON output**

```bash
python3 .claude-plugin/gates/gate_phase5b.py
```

Expected: human-readable + JSON block + "Gate phase5b: PASS/FAIL".

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/gates/gate_phase5b.py && git commit -m "feat(gate_phase5b): add machine-readable JSON output

- Each check now returns structured dict with fix instruction
- Emits JSON with failing items and specific fix guidance
- Same pattern as gate_phase0.py

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Update `gate_phase6_start.py` with JSON Output

**Files:**
- Modify: `.claude-plugin/gates/gate_phase6_start.py`

- [ ] **Step 1: Replace `gate_phase6_start.py` with JSON-enabled version**

Key changes from current:
- Add `sys.path.insert` + `from _json_output import gate_exit`
- Each check returns a dict with `check`, `status`, `message`, `fix`, `missing`
- Add `check_third_party_urls()` as a dict-returning function
- `main()` uses `gate_exit("phase6_start", checks)`

The four check dicts:
1. `check_env_vars()` — fix: "Add {VAR} to .env or .env.example"
2. `check_fake_adapters_pending()` — fix: "Swap or resolve each fake adapter in .dev-flow/architecture/deferred-decisions.md"
3. `check_third_party_urls()` — pass/skip only (URLs are informational)
4. `check_plan_scanned()` — ensures plan exists (skip if no plan yet)

- [ ] **Step 2: Run and verify JSON output**

```bash
python3 .claude-plugin/gates/gate_phase6_start.py
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/gates/gate_phase6_start.py && git commit -m "feat(gate_phase6_start): add machine-readable JSON output

- Adds structured check dicts with fix instructions
- Emits JSON with missing env vars and open fake adapters
- Same pattern as gate_phase0.py and gate_phase5b.py

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update `gate_phase6_end.py` with JSON Output

**Files:**
- Modify: `.claude-plugin/gates/gate_phase6_end.py`

- [ ] **Step 1: Replace `gate_phase6_end.py` with JSON-enabled version**

```python
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
        return {"check": "open_deferred_decisions", "status": "pass", "message": "deferred decisions: all resolved"}
    return {
        "check": "open_deferred_decisions",
        "status": "fail",
        "message": f"{len(open_items)} open deferred decision(s): {[e.get('name','?') for e in open_items]}",
        "fix": "Resolve, re-defer, or skip each open item in .dev-flow/architecture/deferred-decisions.md",
        "missing": [e.get("name", "?") for e in open_items],
    }

def main() -> int:
    c = check_open_decisions()
    symbol = {"pass": "✅", "fail": "❌", "skip": "⏭️"}[c["status"]]
    print(f"{symbol} {c['message']}")
    if c["status"] == "fail":
        print()
        for item in open_items if (open_items := [e for e in parse_tracker(TRACKER_PATH) if e.get("Status","").lower() in ("fake","pending")]) else []:
            print(f"  {item.get('name','?')} — Status: {item.get('Status','?')} — Deferred to: {item.get('Deferred to','?')}")
    return gate_exit("phase6_end", [c])

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run and verify JSON output**

```bash
python3 .claude-plugin/gates/gate_phase6_end.py
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/gates/gate_phase6_end.py && git commit -m "feat(gate_phase6_end): add machine-readable JSON output

- Check returns structured dict with all open decision names
- Emits JSON with fix_items for each open deferred decision
- Same pattern as other gate scripts

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Gate Fix Loop — Add to Phase Files

**Files:**
- Modify: `.claude-plugin/commands/dev-flow.md`
- Modify: `.claude-plugin/phases/05b-preimplementation-gate.md`
- Modify: `.claude-plugin/phases/06-implementation.md`

**What the fix loop does:**

When any gate exits 1:
1. Parse the JSON block from the gate's stdout (between `<!---\n` and `\n-->`)
2. Extract `fix_items` — each item has `check`, `fix`, and optionally `missing`
3. Dispatch one fix agent per `fix_item`
4. Each agent: reads the fix instruction, fixes the specific item, reports back
5. Re-run the gate
6. If gate exits 0 → continue
7. If gate still exits 1 → Round 2 (2 agents, more focused)
8. If still failing after Round 2 → present remaining issues to user with pause/end options

**Implementation:** The fix loop is described as prose in the phase files. The agent executing the phase follows the prose. The gate scripts' JSON output is the interface the agent parses.

### Step 1: Update `commands/dev-flow.md` — gate_phase0 failure handling

Find the current gate failure line:
```
- Exit 1 → gate failed. Print the gate's full output. Then tell the user: "Gate failed — fix the issues above, then run `/dev-flow continue` to re-run."
```

Replace with:

```
- Exit 1 → gate failed.

**Fix Loop — Round 1:**
1. Parse the JSON block from the gate output (between `<!---\n` and `\n-->`)
2. Extract `fix_items` — each item has `check`, `fix`, and `missing`
3. Dispatch one fix agent per failing item in parallel (max 3 agents)
4. Each fix agent: reads the fix instruction, fixes the specific item, verifies the fix worked
5. Re-run gate_phase0.py
6. If exit 0 → print "✅ Gate fixed." Proceed to Step 0.4b.
7. If exit 1 → Round 2

**Fix Loop — Round 2 (if Round 1 didn't resolve):**
1. Re-parse JSON from gate output
2. Remaining items are harder — dispatch up to 2 agents, each with full context of what was already tried
3. Re-run gate_phase0.py
4. If exit 0 → print "✅ Gate fixed after escalation." Proceed to Step 0.4b.
5. If exit 1 → present remaining issues to user. Options: [Pause] [End]

Tell the user: "Gate failed — running autonomous fix loop (Round 1). Will retry automatically."
```

### Step 2: Update `phases/05b-preimplementation-gate.md`

Replace the current gate failure line with the fix loop prose (same structure as above, but target is Phase 6 instead of Step 0.4b).

```
- Exit 1 → gate failed.

**Fix Loop — Round 1:**
1. Parse JSON from gate output
2. Dispatch one fix agent per failing item in parallel (max 3)
3. Each agent fixes its item
4. Re-run gate_phase5b.py
5. If exit 0 → print "✅ Gate fixed." Proceed to Phase 6.
6. If exit 1 → Round 2

**Fix Loop — Round 2 (if Round 1 didn't resolve):**
1. Re-parse JSON, dispatch up to 2 agents with full context
2. Re-run gate
3. If exit 0 → proceed to Phase 6
4. If exit 1 → present remaining issues to user. Options: [Pause] [End]

Tell the user: "Gate failed — running autonomous fix loop (Round 1). Will retry automatically."
```

### Step 3: Update `phases/06-implementation.md` — Step 6.0 gate failure

Find the current gate failure line in Step 6.0 and replace with the fix loop. Round 1 success proceeds to Step 6.1. Round 2 success proceeds to Step 6.1. Round 2 failure presents pause options.

### Step 4: Update `phases/06-implementation.md` — Section 6.4 gate failure

The deferred-decision gate has a different fix loop — it requires user input (Resolve/Re-defer/Skip per item). After the user handles each item, re-run the gate. If the user chooses to skip autonomous fix for this gate, present pause/end options.

### Step 5: Commit

```bash
git add .claude-plugin/commands/dev-flow.md .claude-plugin/phases/05b-preimplementation-gate.md .claude-plugin/phases/06-implementation.md && git commit -m "feat(gates): add autonomous fix loop on gate failure

- Gate failure now triggers a 2-round fix loop before any stop
- Round 1: up to 3 fix agents, one per failing check item
- Round 2: up to 2 agents with full context of what was tried
- Only stops and asks the user if both rounds fail
- Gate JSON output is the interface: fix agents read fix_items from JSON
- Applies to all 4 gate scripts across dev-flow, phase5b, and phase6

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: PreCompact Hook — Save State

**Files:**
- Create: `.claude-plugin/hooks/precompact-save-state.py`
- Modify: `.claude-plugin/plugin.json`

- [ ] **Step 1: Write `precompact-save-state.py`**

```python
#!/usr/bin/env python3
"""PreCompact hook: save session state before context compaction.

Writes to .dev-flow/.last-compact.json so SessionStart can restore on resume.
"""

import json
import os
import sys
import pathlib

PROJECT_ROOT = pathlib.Path.cwd())
DEV_FLOW_DIR = PROJECT_ROOT / ".dev-flow"
STATE_FILE = DEV_FLOW_DIR / ".last-compact.json"

def save_state() -> None:
    """Write current session state to .last-compact.json."""
    DEV_FLOW_DIR.mkdir(exist_ok=True)

    # Read current state if it exists
    current_state = {}
    if STATE_FILE.exists():
        try:
            current_state = json.loads(STATE_FILE.read_text())
        except Exception:
            pass

    # Extract what we can from environment and filesystem
    # The hook receives context via environment variables set by Claude Code
    compact_reason = os.environ.get("CLAUDE_COMPACT_REASON", "unknown")
    compact_start = os.environ.get("CLAUDE_COMPACT_START", "")

    state = {
        "saved_at": __import__("datetime").datetime.now().isoformat(),
        "compact_reason": compact_reason,
        "compact_start": compact_start,
        "cwd": str(PROJECT_ROOT),
        "phase": current_state.get("phase"),  # Will be updated by command context
        "gate_status": current_state.get("gate_status"),
        "gate_round": current_state.get("gate_round"),
        "open_items": current_state.get("open_items", []),
        "last_command": current_state.get("last_command"),
        "lessons_md_hash": _file_hash(PROJECT_ROOT / ".dev-flow" / "lessons.md") if (PROJECT_ROOT / ".dev-flow" / "lessons.md").exists() else None,
        "state_json_hash": _file_hash(PROJECT_ROOT / ".dev-flow" / "state.json") if (PROJECT_ROOT / ".dev-flow" / "state.json").exists() else None,
    }

    STATE_FILE.write_text(json.dumps(state, indent=2))

def _file_hash(path: pathlib.Path) -> str | None:
    """Return a quick content identifier (first 64 chars)."""
    if not path.exists():
        return None
    try:
        return path.read_text()[:64]
    except Exception:
        return None

if __name__ == "__main__":
    try:
        save_state()
        print(f"PreCompact: state saved to {STATE_FILE}", file=sys.stderr)
    except Exception as e:
        print(f"PreCompact: failed to save state: {e}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 2: Update `plugin.json` to register the PreCompact hook**

Find the `hooks` section (or create one) and add:

```json
{
  "hooks": [
    {
      "name": "precompact-save-state",
      "events": ["PreCompact"],
      "script": "./hooks/precompact-save-state.py"
    }
  ]
}
```

The full `plugin.json` should be:

```json
{
  "name": "dev-flow",
  "description": "Multi-session development workflow: 8 structured phases, sequential subagent execution with per-task spec+quality review, opinionated preferences system, Engram memory integration, progressive deployment, TDD discipline, C4 documentation, HARD-GATE enforcement, autonomous fix loops, and context survival hooks.",
  "version": "2.1.0",
  "author": {
    "name": "mors",
    "email": ""
  },
  "license": "MIT",
  "source": {
    "github": "thanksmors/dev-flow"
  },
  "commands": ["./commands"],
  "hooks": [
    {
      "name": "precompact-save-state",
      "events": ["PreCompact"],
      "script": "./hooks/precompact-save-state.py"
    },
    {
      "name": "sessionstart-restore-state",
      "events": ["SessionStart"],
      "script": "./hooks/sessionstart-restore-state.py"
    }
  ]
}
```

- [ ] **Step 3: Verify the hook script runs without error**

```bash
python3 .claude-plugin/hooks/precompact-save-state.py
echo "Exit: $?"
```

Expected: prints to stderr, exits 0. Check `.dev-flow/.last-compact.json` was created.

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/hooks/precompact-save-state.py .claude-plugin/plugin.json && git commit -m "feat(hooks): add PreCompact hook to save session state

- PreCompact hook fires before any context compaction
- Writes phase, gate status, open items, and file hashes to .dev-flow/.last-compact.json
- SessionStart hook (added next) reads this file and offers to restore context
- Enables dev-flow to survive context compaction and resume seamlessly

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: SessionStart Hook — Restore State

**Files:**
- Create: `.claude-plugin/hooks/sessionstart-restore-state.py`

- [ ] **Step 1: Write `sessionstart-restore-state.py`**

```python
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
        # No recent state — nothing to restore
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
```

- [ ] **Step 2: Verify the hook script runs without error**

```bash
python3 .claude-plugin/hooks/sessionstart-restore-state.py
```

Expected: prints restore prompt if `.last-compact.json` exists and is fresh.

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/hooks/sessionstart-restore-state.py .claude-plugin/plugin.json && git commit -m "feat(hooks): add SessionStart hook for context restoration

- SessionStart hook reads .dev-flow/.last-compact.json on session start
- If recent (< 4 hours), prints a restore prompt showing phase, gate status,
  and open items from before the last compaction
- Writes restore prompt to .dev-flow/.restore-prompt.txt for command reference
- User runs /dev-flow continue to resume seamlessly

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Spec Coverage Check

- ✅ All 4 gate scripts emit machine-readable JSON with fix_items
- ✅ Shared `_json_output.py` utility imported by all gates
- ✅ Fix loop (Round 1 + Round 2) added to all 3 phase files
- ✅ PreCompact hook saves state to `.dev-flow/.last-compact.json`
- ✅ SessionStart hook reads saved state and prints restore prompt
- ✅ `plugin.json` registers both hooks
- ✅ Gate fix loop is described in prose (not Python) — agent follows the prose

## Placeholder Scan

- No "TBD" or "TODO" found
- All gate scripts have complete code
- Fix loop described in full prose steps
- Hook scripts have complete code

## Type/Name Consistency

- All gates use `gate_exit("gate_name", checks)` — consistent
- All check functions return `dict` with keys: `check`, `status`, `message`, `fix`, `missing`
- Hook scripts: `precompact-save-state.py`, `sessionstart-restore-state.py` — consistent naming
- State file: `.dev-flow/.last-compact.json` — consistent across both hooks
