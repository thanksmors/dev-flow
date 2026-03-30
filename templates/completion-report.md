# Completion Report — {feature name}

## Summary

- **Status**: {completed | partial | ended-early}
- **Started**: {date}
- **Completed**: {date}
- **Total sessions**: {N}
- **Phases completed**: {list of phase numbers and names}

## What Was Built

{1-2 paragraph description of the feature as implemented}

## Vertical Slices Delivered

| # | Slice Name | Status | Tests | Notes |
|---|-----------|--------|-------|-------|
| 1 | {name} | {done|partial|skipped} | {N} | {notes} |

## Architecture

### C4 Diagrams
- System Context: `.dev-flow/architecture/c4/context.puml`
- Container: `.dev-flow/architecture/c4/container.puml`
- Components: {list component diagram files}

### Sequence & Flow Diagrams
- {list mermaid diagram files}

### Folder Structure
- Documented in: `.dev-flow/architecture/folder-structure.md`

## Testing

- **Total tests**: {N}
- **Test types**: unit ({N}), integration ({N}), property-based ({N}), invariant ({N}), regression ({N})
- **Coverage**: {percentage if available, otherwise "not measured"}
- **Test command**: `{command to run tests}`

## Decisions Made

See full journal: `.dev-flow/decisions/journal.md`

| # | Decision | Phase | Key Rationale |
|---|---------|-------|--------------|
| 1 | {name} | {N} | {rationale} |

## Deferred Decisions

| Decision | Current Choice | Production Choice | Swapped? |
|----------|---------------|-------------------|----------|
| {name} | {simple} | {production} | {yes/no} |

## Risks

### Mitigated
| Risk | Mitigation | Verified By Test? |
|------|-----------|-------------------|
| {risk} | {mitigation} | {yes/no} |

### Accepted
| Risk | Rationale for Acceptance |
|------|------------------------|
| {risk} | {rationale} |

## Known Gaps

| Gap | Category | Severity | Status |
|-----|----------|----------|--------|
| {gap} | {testing|docs|error handling|etc} | {critical|important|minor} | {open|deferred} |

## Files Created/Modified

### Created
- {list new files}

### Modified
- {list modified files}

## How to Run

```bash
# Install dependencies
{install command}

# Run development server
{dev command}

# Run tests
{test command}

# Run production build
{build command}
```

## Next Steps

- [ ] {any remaining work}
- [ ] {deployment steps}
- [ ] {monitoring setup}
