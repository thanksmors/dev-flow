# Changelog

All notable changes to dev-flow are documented here.

## [2.1.0] — 2026-04-01

### Added

- **Python gate scripts** — Deterministic HARD-GATE enforcement via standalone scripts in `gates/`:
  - `gate_phase0.py` — gh auth, git remote, plugin root (runs at Phase 0)
  - `gate_phase5b.py` — plan exists, lint config, ports defined, fake adapters exist (runs at Phase 5b)
  - `gate_phase6_start.py` — env vars, third-party deps, fake adapter swaps (runs at Step 6.0)
  - `gate_phase6_end.py` — all deferred decisions resolved (runs at Section 6.4)

- **Machine-readable JSON output** — All gate scripts emit structured JSON between `<!---\n` and `\n-->` with `status`, `gate`, `round`, `checks`, `failing_count`, and `fix_items` for autonomous parsing

- **Lint gate (oxlint)** — `gate_phase5b.py` checks for `oxlintrc.json` or `.oxlintrc` in project root; fixer-agent handles `lint_clean` fix type by running `bun lint --fix` then verifying `bun lint .` exits 0

- **Autonomous fix loop** — Gate failures trigger a 2-round fix loop before any stop:
  - Round 1: up to 3 fixer agents in parallel, one per failing check item
  - Round 2: up to 2 fixer agents with full context of what was tried
  - Only stops and asks the user if both rounds fail

- **fixer-agent.md** — Specialized agent for the fix loop. Handles all fix types: env vars, ports, fake adapters, lint_clean, deferred decisions, gh auth, git remote, plugin root. Round-aware, verifies before reporting done.

- **Context survival hooks** — Plugin hooks survive Claude Code context compaction:
  - `PreCompact` hook saves session state to `.dev-flow/.last-compact.json`
  - `SessionStart` hook reads saved state and prints a restore prompt
  - State includes phase, gate status, open items, and file hashes

### Changed

- Gate scripts find the latest plan by modification time — no hardcoded `implementation.md` filename
- `scan_env_references()` skips content inside triple-backtick code blocks and markdown comment lines to avoid false positives
- `check_fake_adapters()` searches `layers/*/adapters/` and `src/adapters/` with proper path fallback
- README updated with new features: Python gate scripts, autonomous fix loop, context survival hooks

### Fixed

- `gate_phase6_start.py` no longer falsely reports `VARIABLE_NAME` from example code in plan files

## [2.0.0] — 2026-03-30

- Initial public release
