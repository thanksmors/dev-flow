#!/usr/bin/env python
"""Gate Phase 6 Start: Pre-flight check — scan for missing env vars and third-party deps."""

import sys
import pathlib
import re

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / ".dev-flow" / "plans"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"
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

def load_env(path: pathlib.Path) -> dict[str, str]:
    """Parse a .env file into a dict of key=value."""
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            key, _, value = line.partition('=')
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env

def scan_env_references(plan_path: pathlib.Path | None) -> list[str]:
    """Find process.env.* references in the plan file, skipping comments and code blocks."""
    if plan_path is None or not plan_path.exists():
        return []
    content = plan_path.read_text()
    refs = []
    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith('#'):
            continue
        if stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('|'):
            continue
        if 'process.env' in line:
            found = re.findall(r'process\.env\.([A-Z_][A-Z0-9_]*)', line)
            refs.extend(found)
    return list(set(refs))

def scan_third_party_urls(plan_path: pathlib.Path | None) -> list[str]:
    """Find third-party URLs referenced in the plan."""
    if plan_path is None or not plan_path.exists():
        return []
    content = plan_path.read_text()
    urls = re.findall(r'https?://[^\s<>"\')]+', content)
    external = [u for u in urls if not any(h in u for h in ['localhost', '127.0.0.1', '.local'])]
    return list(set(external))

def check_plan_exists() -> dict:
    if PLAN_PATH is None:
        return {
            "check": "plan_exists",
            "status": "fail",
            "message": f"implementation plan: NOT FOUND in {PLANS_DIR}",
            "fix": "Run Phase 5 planning to create an implementation plan",
            "missing": [],
        }
    if PLAN_PATH.exists():
        return {"check": "plan_exists", "status": "pass", "message": f"plan: OK ({PLAN_PATH.name})", "fix": "", "missing": []}
    return {
        "check": "plan_exists",
        "status": "fail",
        "message": f"implementation plan: NOT FOUND",
        "fix": "Run Phase 5 planning to create an implementation plan",
        "missing": [],
    }

def check_env_vars() -> dict:
    """Check that all process.env references in the plan have values set."""
    refs = scan_env_references(PLAN_PATH)
    if not refs:
        return {"check": "env_vars", "status": "pass", "message": "env vars: none referenced in plan", "fix": "", "missing": []}
    env = load_env(ENV_PATH)
    env_example = load_env(ENV_EXAMPLE_PATH)
    missing = []
    for var in refs:
        if var not in env and var not in env_example:
            missing.append(var)
    if missing:
        return {
            "check": "env_vars",
            "status": "fail",
            "message": f"missing env vars ({len(missing)}): {', '.join(missing)}",
            "fix": f"Add {missing[0]}{' and others' if len(missing) > 1 else ''} to .env or .env.example",
            "missing": missing,
        }
    return {"check": "env_vars", "status": "pass", "message": f"env vars: all {len(refs)} referenced vars configured", "fix": "", "missing": []}

def check_fake_adapters_pending() -> dict:
    """Check deferred decisions tracker for fake adapters that need swapping."""
    if not TRACKER_PATH.exists():
        return {"check": "fake_adapters_pending", "status": "pass", "message": "deferred decisions tracker: not found (skipping)", "fix": "", "missing": []}
    content = TRACKER_PATH.read_text()
    fake_items = []
    in_entry = False
    current_entry = []
    for line in content.splitlines():
        if line.startswith('## '):
            if 'fake' in ' '.join(current_entry).lower():
                name = line.removeprefix('## ').strip()
                fake_items.append(name)
            current_entry = []
            in_entry = True
        if in_entry:
            current_entry.append(line)
    if fake_items:
        return {
            "check": "fake_adapters_pending",
            "status": "fail",
            "message": f"fake adapters still wired ({len(fake_items)}): {', '.join(fake_items)}",
            "fix": "Swap or resolve each fake adapter in .dev-flow/architecture/deferred-decisions.md before Phase 6",
            "missing": fake_items,
        }
    return {"check": "fake_adapters_pending", "status": "pass", "message": "fake adapters: none pending", "fix": "", "missing": []}

def check_third_party_urls() -> dict:
    """Report third-party URLs found in plan (informational)."""
    urls = scan_third_party_urls(PLAN_PATH)
    if not urls:
        return {"check": "third_party_urls", "status": "pass", "message": "third-party URLs: none found in plan", "fix": "", "missing": []}
    return {"check": "third_party_urls", "status": "pass", "message": f"third-party URLs: {len(urls)} found in plan (informational)", "fix": "", "missing": urls}

def main() -> int:
    print("=== Gate Phase 6 Start: Pre-flight Check ===\n")
    print(f"Plan: {PLAN_PATH.name if PLAN_PATH else 'none found'}")
    print(f"Env:  {ENV_PATH}\n")
    checks = [
        check_plan_exists(),
        check_env_vars(),
        check_fake_adapters_pending(),
        check_third_party_urls(),
    ]
    for c in checks:
        symbol = {"pass": "[PASS]", "fail": "[FAIL]", "skip": "[SKIP]"}[c["status"]]
        print(f"{symbol} {c['message']}")
    return gate_exit("phase6_start", checks)

if __name__ == "__main__":
    sys.exit(main())
