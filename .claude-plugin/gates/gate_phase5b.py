#!/usr/bin/env python
"""Gate Phase 5b: Pre-implementation gate — verify plan is ready before Phase 6."""

import sys
import pathlib
import re

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / ".dev-flow" / "plans"
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
        return {"check": "plan_exists", "status": "pass", "message": f"implementation plan: OK ({PLAN_PATH.name})", "fix": "", "missing": []}
    return {
        "check": "plan_exists",
        "status": "fail",
        "message": f"implementation plan: NOT FOUND at {PLAN_PATH}",
        "fix": "Run Phase 5 planning to create a plan file",
        "missing": [],
    }

def check_ports_defined() -> dict:
    """If plan mentions external dependencies, ports should exist."""
    if PLAN_PATH is None or not PLAN_PATH.exists():
        return {"check": "ports_defined", "status": "skip", "message": "plan not found — skipping port check", "fix": "", "missing": []}
    content = PLAN_PATH.read_text()
    external_keywords = ["API", "database", "auth", "email", "payment", "queue", "cache"]
    has_external = any(kw.lower() in content.lower() for kw in external_keywords)
    if not has_external:
        return {"check": "ports_defined", "status": "skip", "message": "ports: no external deps in plan, skipping", "fix": "", "missing": []}
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
    return {"check": "ports_defined", "status": "pass", "message": f"ports: OK ({len(port_files)} port file(s) found)", "fix": "", "missing": []}

def check_fake_adapters() -> dict:
    """All fake adapters referenced in the plan should exist."""
    if PLAN_PATH is None or not PLAN_PATH.exists():
        return {"check": "fake_adapters", "status": "skip", "message": "plan not found — skipping fake adapter check", "fix": "", "missing": []}
    content = PLAN_PATH.read_text()
    adapter_names = re.findall(r'(?:Fake|Wire)[A-Z][a-zA-Z]+(?:Adapter|Port)?', content)
    if not adapter_names:
        return {"check": "fake_adapters", "status": "pass", "message": "fake adapters: none referenced in plan", "fix": "", "missing": []}
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
            "fix": f"Create fake adapters at the adapters directory",
            "missing": missing,
        }
    return {"check": "fake_adapters", "status": "pass", "message": f"fake adapters: OK ({len(set(adapter_names))} referenced)", "fix": "", "missing": []}

def check_lint_config() -> dict:
    """oxlintrc.json or .oxlintrc should exist in project root."""
    possible_paths = [PROJECT_ROOT / "oxlintrc.json", PROJECT_ROOT / ".oxlintrc"]
    for p in possible_paths:
        if p.exists():
            return {"check": "lint_config", "status": "pass", "message": f"lint config: OK ({p.name})", "fix": "", "missing": []}
    return {
        "check": "lint_config",
        "status": "fail",
        "message": "lint config: oxlintrc.json or .oxlintrc not found in project root",
        "fix": "Create a minimal oxlintrc.json in the project root",
        "missing": [],
    }

def check_deferred_decisions_clean() -> dict:
    """No deferred decisions with Status=fake should be pending."""
    if not TRACKER_PATH.exists():
        return {"check": "deferred_decisions", "status": "skip", "message": "deferred decisions tracker: not found (skipping)", "fix": "", "missing": []}
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
    return {"check": "deferred_decisions", "status": "pass", "message": "deferred decisions: all resolved or swapped", "fix": "", "missing": []}

def main() -> int:
    checks = [
        check_plan_exists(),
        check_lint_config(),
        check_ports_defined(),
        check_fake_adapters(),
        check_deferred_decisions_clean(),
    ]
    for c in checks:
        symbol = {"pass": "[PASS]", "fail": "[FAIL]", "skip": "[SKIP]"}[c["status"]]
        print(f"{symbol} {c['message']}")
    return gate_exit("phase5b", checks)

if __name__ == "__main__":
    sys.exit(main())
