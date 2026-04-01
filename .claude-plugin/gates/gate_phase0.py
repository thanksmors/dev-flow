#!/usr/bin/env python
"""Gate Phase 0: Verify prerequisites before dev-flow Phase 0 completes."""

import subprocess
import sys
import pathlib

PLUGIN_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PROJECT_ROOT = pathlib.Path.cwd()

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
        return {"check": "gh_auth", "status": "pass", "message": "gh auth: OK", "fix": "", "missing": []}
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
        return {"check": "git_remote", "status": "pass", "message": f"git remote: OK ({remote_url})", "fix": "", "missing": []}
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
        return {"check": "plugin_root", "status": "pass", "message": f"CLAUDE_PLUGIN_ROOT: OK ({PLUGIN_ROOT})", "fix": "", "missing": []}
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
        symbol = "[PASS]" if c["status"] == "pass" else "[FAIL]"
        print(f"{symbol} {c['message']}")
    return gate_exit("phase0", checks)

if __name__ == "__main__":
    sys.exit(main())
