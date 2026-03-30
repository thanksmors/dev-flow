# Architecture Decision Record — Template

Copy this file to `docs/decisions/000N-{short-name}.md` and fill in all fields.
Replace `N` with the next available number (zero-padded to 4 digits: 0001, 0002, ...).
Replace `{short-name}` with a brief kebab-case description of the decision.

---

# {NNNN}. {Decision Title}

Date: {YYYY-MM-DD}
Status: Accepted | Superseded | Deprecated
Review by: Phase 7 agent / Human at Phase 7 checkpoint
Superseded by: (link to ADR if status is Superseded)
Review notes: Is this still the right decision? Any new alternatives?

## Context

What situation prompted this decision? What forces were at play? What was the
problem that needed to be solved? Include constraints that shaped the options.

## Decision

What was decided. Be direct: "We will use X" rather than "We considered X."

## Consequences

What becomes easier or harder as a result of this decision.
What was consciously accepted as a trade-off.
If this supersedes an earlier decision, note: "Supersedes [ADR-NNN](000N-old.md)."

---

## Status values

| Status | Meaning |
|--------|---------|
| Accepted | Decision is in effect and current |
| Superseded | Replaced by a later ADR — update this record and link to the replacement |
| Deprecated | No longer relevant but kept for historical record |

**Superseded by:** When Status is `Superseded`, add a link to the replacing ADR, e.g.:
`Superseded by: [ADR-NNN](000N-new-decision.md)`

## When to write an ADR

Write one whenever you make a significant architectural decision — one where you
consciously chose between alternatives and accepted trade-offs:

| Phase | Trigger | Filename example |
|-------|---------|-----------------|
| 1 (Discovery) | Approach selected from brainstorm | `0001-approach-selection.md` |
| 3 (Design) | Technology/framework chosen | `0002-database-choice.md` |
| 3 (Design) | Deferred architectural decision | `0003-deferred-{name}.md` |
| 4 (Pre-Mortem) | Risk changes the design | `0004-risk-mitigation-{name}.md` |
| 6 (Implementation) | Design pivots mid-build | `0005-pivot-{name}.md` |
| 7 (Gap Analysis) | Gap fix requires architectural change | `0006-gap-fix-{name}.md` |

**Do NOT write an ADR for:**
- Implementation details with no real alternatives
- Bug fixes
- Minor refactors
- Configuration choices with no long-term architectural consequences

**One decision = one file.** Never append a new decision to an existing ADR.
