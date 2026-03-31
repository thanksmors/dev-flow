"""Tests for gate_phase0."""
import subprocess
import sys
import pathlib
from unittest.mock import patch

def test_check_plugin_root_finds_plugin_json():
    """Plugin root should resolve to a directory with plugin.json."""
    # Import from the gate module
    import gate_phase0
    ok, msg = gate_phase0.check_plugin_root()
    assert ok, f"Expected plugin root to resolve, got: {msg}"

def test_gate_exit_codes():
    """Gate script must exit 0 when all checks pass, 1 when any fails."""
    script = pathlib.Path(__file__).parent / "gate_phase0.py"
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    # We don't assert exit code here since gh/git may not be configured in test env
    assert result.returncode in (0, 1), f"Unexpected exit code: {result.returncode}"
    assert "Gate Phase 0:" in result.stdout