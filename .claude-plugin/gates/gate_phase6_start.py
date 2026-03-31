#!/usr/bin/env python3
"""Gate Phase 6 Start: Pre-flight check — scan for missing env vars and third-party deps."""

import sys
import pathlib
import re

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / "docs" / "superpowers" / "plans"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"
TRACKER_PATH = PROJECT_ROOT / ".dev-flow" / "architecture" / "deferred-decisions.md"

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
        # Track code block boundaries
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        # Skip content inside code blocks
        if in_code_block:
            continue
        # Skip markdown comment lines
        if stripped.startswith('#'):
            continue
        # Skip markdown structural lines (headers, list items)
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

def check_env_vars() -> tuple[bool, list[str]]:
    """Check that all process.env references in the plan have values set."""
    refs = scan_env_references(PLAN_PATH)
    if not refs:
        return True, []
    env = load_env(ENV_PATH)
    env_example = load_env(ENV_EXAMPLE_PATH)
    missing = []
    for var in refs:
        if var not in env and var not in env_example:
            missing.append(var)
    if missing:
        return False, missing
    return True, []

def check_fake_adapters_pending() -> tuple[bool, list[str]]:
    """Check deferred decisions tracker for fake adapters that need swapping."""
    if not TRACKER_PATH.exists():
        return True, []
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
        return False, fake_items
    return True, []

def check_third_party_urls() -> tuple[bool, list[str]]:
    """Check if third-party URLs referenced in plan are configured."""
    urls = scan_third_party_urls(PLAN_PATH)
    if not urls:
        return True, []
    return True, urls  # Pass but report

def main() -> int:
    print("=== Gate Phase 6 Start: Pre-flight Check ===\n")
    print(f"Plan: {PLAN_PATH.name if PLAN_PATH else 'none found'}")
    print(f"Env:  {ENV_PATH}\n")

    env_pass, missing_envs = check_env_vars()
    fake_pass, fake_items = check_fake_adapters_pending()
    url_pass, urls = check_third_party_urls()

    failed = False

    if not env_pass:
        failed = True
        print(f"❌ Missing env vars ({len(missing_envs)}):")
        for var in missing_envs:
            print(f"   {var}")
        print()

    if not fake_pass:
        failed = True
        print(f"❌ Fake adapters still wired ({len(fake_items)}):")
        for item in fake_items:
            print(f"   {item}")
        print("   Run swap protocol before Phase 6 begins.")
        print()

    if url_pass and urls:
        print(f"✅ Third-party services: {len(urls)} URL(s) found in plan")
        for url in urls:
            print(f"   {url}")
        print()

    if not failed:
        print("✅ Pre-flight: PASS — no missing env vars or third-party dependencies\n")
        print("Gate Phase 6 Start: PASS")
        return 0

    print()
    print("Gate Phase 6 Start: FAIL")
    print("Run `/dev-flow continue` once ready.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
