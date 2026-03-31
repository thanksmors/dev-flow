#!/usr/bin/env python3
"""Gate Phase 0: Verify prerequisites before dev-flow Phase 0 completes."""

import subprocess
import sys
import os
import pathlib

PLUGIN_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PROJECT_ROOT = pathlib.Path.cwd()

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

def check_gh_auth() -> tuple[bool, str]:
    code, out = run(["gh", "auth", "status"])
    if code == 0:
        return True, "gh auth: OK"
    return False, f"gh auth: FAILED\n{out.strip()}"

def check_git_remote() -> tuple[bool, str]:
    code, out = run(["git", "remote", "-v"])
    if code == 0 and "origin" in out:
        return True, f"git remote: OK ({out.strip().split()[1]})"
    return False, f"git remote: not configured or not origin"

def check_plugin_root() -> tuple[bool, str]:
    root_file = PLUGIN_ROOT / "plugin.json"
    if root_file.exists():
        return True, f"CLAUDE_PLUGIN_ROOT: OK ({PLUGIN_ROOT})"
    return False, f"CLAUDE_PLUGIN_ROOT: not found at {PLUGIN_ROOT}"

def main() -> int:
    checks = [check_gh_auth(), check_git_remote(), check_plugin_root()]
    all_pass = True
    for ok, msg in checks:
        symbol = "✅" if ok else "❌"
        print(msg)
        if not ok:
            all_pass = False
    if all_pass:
        print("\nGate Phase 0: PASS")
        return 0
    print("\nGate Phase 0: FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())