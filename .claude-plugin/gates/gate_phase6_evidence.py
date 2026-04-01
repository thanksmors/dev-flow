#!/usr/bin/env python
"""Gate Phase 6 Evidence: Verify implementation evidence exists before Phase 7.

Checks mechanical evidence: test files, ADR files, workspace.dsl, Mermaid C4,
slice wiring status, test suite passes, no skipped tests.
PYTHONIOENCODING=utf-8 must be set when running this script on Windows.
"""

import sys
import pathlib
import re
import subprocess

PROJECT_ROOT = pathlib.Path.cwd()
PLANS_DIR = PROJECT_ROOT / ".dev-flow" / "plans"
DOCS_DIR = PROJECT_ROOT / "docs"
C4_DIR = PROJECT_ROOT / ".dev-flow" / "architecture" / "c4"
STATE_PATH = PROJECT_ROOT / ".dev-flow" / "state.json"
TEMPLATES_DIR = PROJECT_ROOT / ".claude-plugin" / "templates" if (PROJECT_ROOT / ".claude-plugin").exists() else PROJECT_ROOT / "templates"

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _json_output import gate_exit


def find_latest_plan() -> pathlib.Path | None:
    if not PLANS_DIR.exists():
        return None
    plan_files = [f for f in PLANS_DIR.glob("*.md") if "premortem" not in f.stem.lower()]
    if not plan_files:
        return None
    return max(plan_files, key=lambda f: f.stat().st_mtime)

PLAN_PATH = find_latest_plan()


def scan_test_files() -> dict:
    """At least one test file matching **/*.test.ts or **/*.spec.ts must exist."""
    test_patterns = list(PROJECT_ROOT.glob("**/*.test.ts")) + list(PROJECT_ROOT.glob("**/*.spec.ts"))
    test_files = [f for f in test_patterns if "node_modules" not in str(f)]
    if not test_files:
        return {
            "check": "test_files",
            "status": "fail",
            "message": "test files: no .test.ts or .spec.ts files found",
            "fix": "Run Phase 6 implementation — at least one test file must exist",
            "missing": [],
        }
    return {
        "check": "test_files",
        "status": "pass",
        "message": f"test files: OK ({len(test_files)} file(s) found)",
        "fix": "",
        "missing": [],
    }


def scan_e2e_tests() -> dict:
    """E2E test count must match what the plan promised."""
    if PLAN_PATH is None:
        return {"check": "e2e_test_count", "status": "skip", "message": "plan not found — skipping E2E count check", "fix": "", "missing": []}
    content = PLAN_PATH.read_text()
    # Find "N E2E tests" pattern in plan
    e2e_match = re.search(r'(\d+)\s+E2E\s+test', content, re.IGNORECASE)
    if not e2e_match:
        return {"check": "e2e_test_count", "status": "skip", "message": "E2E tests: count not specified in plan", "fix": "", "missing": []}
    planned_count = int(e2e_match.group(1))
    # Discover actual E2E test files
    e2e_patterns = list(PROJECT_ROOT.glob("**/*.e2e.ts"))
    if "tests" in str(PROJECT_ROOT):
        e2e_patterns += list((PROJECT_ROOT / "tests").glob("**/*.test.ts"))
    actual_files = [f for f in e2e_patterns if "node_modules" not in str(f)]
    actual_count = len(actual_files)
    if actual_count < planned_count:
        return {
            "check": "e2e_test_count",
            "status": "fail",
            "message": f"E2E tests: plan promised {planned_count}, found {actual_count}",
            "fix": f"Expected {planned_count} E2E test files, found {actual_count}. Check plan's test strategy section.",
            "missing": [f"{planned_count - actual_count} missing E2E test file(s)"],
        }
    return {
        "check": "e2e_test_count",
        "status": "pass",
        "message": f"E2E tests: {actual_count} found (plan promised {planned_count})",
        "fix": "",
        "missing": [],
    }


def scan_adr_files() -> dict:
    """At least one ADR file must exist in docs/decisions/."""
    if not DOCS_DIR.exists():
        return {"check": "adr_files", "status": "fail", "message": "docs/decisions/: docs/ directory not found", "fix": "Create docs/decisions/ directory and add ADR files", "missing": []}
    decisions_dir = DOCS_DIR / "decisions"
    if not decisions_dir.exists():
        return {"check": "adr_files", "status": "fail", "message": "docs/decisions/: directory not found", "fix": "Create docs/decisions/ and add ADR files", "missing": []}
    adr_files = list(decisions_dir.glob("*.md"))
    if not adr_files:
        return {
            "check": "adr_files",
            "status": "fail",
            "message": "docs/decisions/: no ADR files found",
            "fix": "Create at least one ADR file in docs/decisions/ (e.g., 0001-approach-selection.md)",
            "missing": ["no ADR files"],
        }
    return {
        "check": "adr_files",
        "status": "pass",
        "message": f"ADR files: OK ({len(adr_files)} file(s) in docs/decisions/)",
        "fix": "",
        "missing": [],
    }


def check_workspace_dsl() -> dict:
    """docs/workspace.dsl must exist and be non-empty."""
    dsl_path = DOCS_DIR / "workspace.dsl"
    if not dsl_path.exists():
        return {
            "check": "workspace_dsl",
            "status": "fail",
            "message": "docs/workspace.dsl: not found",
            "fix": "Run Phase 3 to create docs/workspace.dsl",
            "missing": [],
        }
    if dsl_path.stat().st_size == 0:
        return {
            "check": "workspace_dsl",
            "status": "fail",
            "message": "docs/workspace.dsl: file is empty",
            "fix": "Populate docs/workspace.dsl with C4 model and views",
            "missing": [],
        }
    return {
        "check": "workspace_dsl",
        "status": "pass",
        "message": "docs/workspace.dsl: OK",
        "fix": "",
        "missing": [],
    }


def check_c4_mmd() -> dict:
    """.dev-flow/architecture/c4/ must have at least one .mmd file."""
    if not C4_DIR.exists():
        return {
            "check": "c4_mmd",
            "status": "fail",
            "message": ".dev-flow/architecture/c4/: directory not found",
            "fix": "Run Phase 3 to generate Mermaid C4 diagrams in .dev-flow/architecture/c4/",
            "missing": [],
        }
    mmd_files = list(C4_DIR.glob("*.mmd"))
    if not mmd_files:
        return {
            "check": "c4_mmd",
            "status": "fail",
            "message": ".dev-flow/architecture/c4/: no .mmd files found",
            "fix": "Generate Mermaid C4 diagrams in .dev-flow/architecture/c4/ (ST-1)",
            "missing": [],
        }
    return {
        "check": "c4_mmd",
        "status": "pass",
        "message": f"Mermaid C4: OK ({len(mmd_files)} .mmd file(s))",
        "fix": "",
        "missing": [],
    }


def check_slice_wiring() -> dict:
    """All slices with Status=complete must have Wired=yes."""
    if PLAN_PATH is None:
        return {"check": "slice_tracking", "status": "skip", "message": "plan not found — skipping slice wiring check", "fix": "", "missing": []}
    content = PLAN_PATH.read_text()
    # Find task rows with Status=complete but no Wired=yes
    rows = re.findall(r'\|\s*(\d+(?:\.\d+)?)\s*\|[^|]*\|[^|]*\|\s*(complete)\s*\|[^|]*\|\s*(no)\s*\|', content, re.IGNORECASE)
    if rows:
        task_ids = [r[0] for r in rows]
        return {
            "check": "slice_tracking",
            "status": "fail",
            "message": f"slice tracking: task(s) {', '.join(task_ids)} marked complete but Wired=no",
            "fix": "Set Wired=yes for all complete tasks, or downgrade Status to scaffolded",
            "missing": task_ids,
        }
    return {
        "check": "slice_tracking",
        "status": "pass",
        "message": "slice tracking: all complete tasks have Wired=yes",
        "fix": "",
        "missing": [],
    }


def check_test_suite_passes() -> dict:
    """bun test must exit 0."""
    try:
        result = subprocess.run(["bun", "test"], capture_output=True, text=True, timeout=120, cwd=PROJECT_ROOT)
        if result.returncode == 0:
            return {"check": "test_suite_passes", "status": "pass", "message": "test suite: all tests pass", "fix": "", "missing": []}
        return {
            "check": "test_suite_passes",
            "status": "fail",
            "message": f"test suite: FAILED (exit {result.returncode})\n{result.stdout[-500:]}{result.stderr[-500:]}",
            "fix": "Run 'bun test' in project root to see failures, fix before Phase 7",
            "missing": [],
        }
    except FileNotFoundError:
        return {"check": "test_suite_passes", "status": "skip", "message": "test suite: bun not found — skipping", "fix": "", "missing": []}
    except subprocess.TimeoutExpired:
        return {"check": "test_suite_passes", "status": "fail", "message": "test suite: timed out after 120s", "fix": "Run 'bun test' manually to diagnose", "missing": []}


def check_no_skipped_tests() -> dict:
    """No test.skip = true should be present."""
    test_files = list(PROJECT_ROOT.glob("**/*.test.ts")) + list(PROJECT_ROOT.glob("**/*.spec.ts"))
    skipped = []
    for f in test_files:
        if "node_modules" in str(f):
            continue
        content = f.read_text()
        if re.search(r'test\.skip\s*=\s*true', content):
            skipped.append(str(f.relative_to(PROJECT_ROOT)))
    if skipped:
        return {
            "check": "no_skipped_tests",
            "status": "fail",
            "message": f"skipped tests: {len(skipped)} file(s) with test.skip=true",
            "fix": "Remove test.skip=true or convert to test() with pending assertion",
            "missing": skipped,
        }
    return {"check": "no_skipped_tests", "status": "pass", "message": "skipped tests: none found", "fix": "", "missing": []}


def main() -> int:
    print("=== Gate Phase 6 Evidence ===\n")
    checks = [
        scan_test_files(),
        scan_e2e_tests(),
        scan_adr_files(),
        check_workspace_dsl(),
        check_c4_mmd(),
        check_slice_wiring(),
        check_test_suite_passes(),
        check_no_skipped_tests(),
    ]
    for c in checks:
        symbol = {"pass": "[PASS]", "fail": "[FAIL]", "skip": "[SKIP]", "warn": "[WARN]"}[c["status"]]
        print(f"{symbol} {c['message']}")
    return gate_exit("phase6_evidence", checks)

if __name__ == "__main__":
    sys.exit(main())
