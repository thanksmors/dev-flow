# Lint Gate Implementation Plan

## Goal

Add `bun lint` (oxlint) as a hard-gate quality check in dev-flow, with fixer-agent auto-fix support.

## Architecture

- **Phase 5b gate**: check `oxlintrc.json` exists (project has linting configured)
- **Lint fixer type**: runs `bun lint --fix`, verifies exit 0, reports remaining violations
- **Hard gate**: fixer attempts fix in 2-round loop, if both rounds fail → user decides (Resolve/Skip/Pause)

## Files

### Modify: `.claude-plugin/gates/gate_phase5b.py`
Add `lint_config` check:
- Check for `oxlintrc.json` or `.oxlintrc` in project root
- If missing → fail with fix: "create minimal oxlintrc.json"

### Modify: `.claude-plugin/agents/fixer-agent.md`
Add `lint_clean` fix type:
- Fix: run `bun lint --fix`
- Verification: `bun lint` exits 0
- BLOCKED if: `bun` not installed, or not a bun project

### Modify: `.claude-plugin/phases/05b-preimplementation-gate.md`
Add lint to the fix loop dispatch — `lint_clean` gets dispatched same as `env_vars`, `fake_adapters`, etc.

### Modify: `CHANGELOG.md`
Document lint gate addition in unreleased section.
