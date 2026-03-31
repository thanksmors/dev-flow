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

def check_plan_exists() -> tuple[bool, str]:
    if PLAN_PATH is None:
        return False, f"implementation plan: NOT FOUND — no .md plan file in {PLANS_DIR} (excluding premortem)"
    if PLAN_PATH.exists():
        return True, f"implementation plan: OK ({PLAN_PATH.name})"
    return False, f"implementation plan: NOT FOUND at {PLAN_PATH}"

def check_ports_defined() -> tuple[bool, str]:
    """If plan mentions external dependencies, ports should exist."""
    if not PLAN_PATH.exists():
        return True, "plan not found — skipping port check"
    content = PLAN_PATH.read_text()
    # Check for any external dependency keywords
    external_keywords = ["API", "database", "auth", "email", "payment", "queue", "cache"]
    has_external = any(kw.lower() in content.lower() for kw in external_keywords)
    if not has_external:
        return True, "ports: no external deps in plan, skipping"
    ports_dir = LAYERS_DIR if LAYERS_DIR.exists() else PROJECT_ROOT / "src" / "ports"
    if not ports_dir.exists():
        return False, f"ports: plan has external deps but no ports directory at {ports_dir}"
    port_files = list(ports_dir.rglob("*Port*.ts")) + list(ports_dir.rglob("*port*.ts"))
    if not port_files:
        return False, f"ports: external deps in plan but no port files found in {ports_dir}"
    return True, f"ports: OK ({len(port_files)} port file(s) found)"

def check_fake_adapters() -> tuple[bool, str]:
    """All fake adapters referenced in the plan should exist."""
    if not PLAN_PATH or not PLAN_PATH.exists():
        return True, "plan not found — skipping fake adapter check"
    content = PLAN_PATH.read_text()
    # Find adapter names in task descriptions (rough heuristic)
    adapter_names = re.findall(r'(?:Fake|Wire)[A-Z][a-zA-Z]+(?:Adapter|Port)?', content)
    if not adapter_names:
        return True, "fake adapters: none referenced in plan"
    # Look in layers/*/adapters/ first, then src/adapters/
    adapters_dirs = []
    if LAYERS_DIR.exists():
        adapters_dirs.extend(d.parent for d in LAYERS_DIR.rglob("adapters"))
    src_adapters = PROJECT_ROOT / "src" / "adapters"
    if src_adapters.exists():
        adapters_dirs.append(src_adapters)
    if not adapters_dirs:
        return False, f"fake adapters: no adapters directory found (tried layers/*/adapters/, src/adapters/)"
    missing = []
    found_dirs = []
    for name in set(adapter_names):
        found = False
        for ad in adapters_dirs:
            expected = ad / f"{name}.ts"
            if expected.exists():
                found = True
                break
        if not found:
            missing.append(name)
        else:
            found_dirs.extend([ad for ad in adapters_dirs if (ad / f"{name}.ts").exists()])
    if missing:
        return False, f"fake adapters: missing — {', '.join(missing)}"
    return True, f"fake adapters: OK ({len(set(adapter_names))} referenced)"

def check_deferred_decisions_clean() -> tuple[bool, str]:
    """No deferred decisions with Status=fake should be pending."""
    if not TRACKER_PATH.exists():
        return True, "deferred decisions tracker: not found (skipping)"
    content = TRACKER_PATH.read_text()
    # Check for Status = fake or Status = pending lines (rough heuristic)
    fake_lines = [l for l in content.split('\n') if 'Status:' in l and ('fake' in l.lower() or 'pending' in l.lower())]
    if fake_lines:
        return False, f"deferred decisions: {len(fake_lines)} item(s) still open (fake/pending)"
    return True, "deferred decisions: all resolved or swapped"

def main() -> int:
    checks = [
        check_plan_exists(),
        check_ports_defined(),
        check_fake_adapters(),
        check_deferred_decisions_clean(),
    ]
    all_pass = True
    for ok, msg in checks:
        symbol = "✅" if ok else "❌"
        print(f"{symbol} {msg}")
        if not ok:
            all_pass = False
    if all_pass:
        print("\nGate Phase 5b: PASS")
        return 0
    print("\nGate Phase 5b: FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
