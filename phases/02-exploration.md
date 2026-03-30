---
name: exploration
description: Deeply understand the existing codebase — architecture, patterns, conventions, and integration points
---

# Phase 2: Codebase Exploration

**Objective**: Deeply understand the existing codebase — architecture, patterns, conventions, and integration points — before designing the solution.

## Steps

### 2.1 Launch Parallel Explorer Agents

Dispatch **2-3 code-explorer agents** in parallel, each with a different focus:

**Agent 1: Architecture & Patterns**
- Trace the overall architecture layers
- Identify key patterns (repository pattern, service layer, etc.)
- Map dependency injection / composition patterns
- Find shared utilities and abstractions
- Identify the data flow from entry points to storage

**Agent 2: Conventions & Standards**
- Identify naming conventions (files, functions, variables)
- Find test patterns (where tests live, testing frameworks used)
- Document error handling patterns
- Find logging/monitoring patterns
- Identify code organization principles

**Agent 3: Integration Points**
- Map API routes / endpoints
- Identify database schema and ORM patterns
- Find external service integrations
- Document configuration management
- Identify authentication/authorization patterns

Each agent should produce a structured summary of findings.

### 2.2 Synthesize Findings

After all agents complete:

1. Read each agent's output
2. Merge findings into a coherent codebase map
3. Identify the most relevant integration points for the feature being built
4. Note any patterns the implementation MUST follow
5. Note any anti-patterns to avoid

### 2.3 Document Exploration Results

Write findings to `.dev-flow/design/codebase-map.md`:

```markdown
# Codebase Map — {feature name}

## Architecture Overview
{high-level architecture description}

## Key Patterns
{patterns discovered, with examples}

## Conventions
{naming, testing, error handling conventions}

## Integration Points
{where the new feature will connect}

## Must-Follow Patterns
{patterns the implementation must adhere to}

## Anti-Patterns to Avoid
{patterns found that should not be replicated}

## Open Questions
{anything still unclear after exploration}
```

### 2.3a Extract Domain Glossary

Create or update `docs/domain-glossary.md` with the domain vocabulary discovered during exploration:

```markdown
# Domain Glossary

| Concept | Canonical Name | Avoid | Context |
|---------|---------------|-------|---------|
| {what the concept is} | {one canonical name} | {synonyms to avoid} | {where it's used} |
```

Rules:
- Every domain concept gets exactly one canonical name
- "Avoid" column lists synonyms that have appeared or could appear
- "Context" column notes which domain/layer uses this term
- If the glossary already exists, update it — do not recreate

This glossary is the source of truth for naming. Implementation phases reference it to prevent terminology drift.

### 2.4 Update State

- `state.json`: Record artifact path in appropriate field
- `decisions`: Record any decisions made during exploration

### 2.5 Decision Journal Entry

Record any significant findings that affect the approach:
```
## [YYYY-MM-DD] Codebase Exploration Findings
- **Key discovery**: {finding}
- **Impact on approach**: {how it changes the plan}
- **Pattern to follow**: {pattern}
- **Anti-pattern to avoid**: {anti-pattern}
```

## Quality Gate

Before checkpoint, verify:

- [ ] At least 2 explorer agents were dispatched with distinct focuses
- [ ] Architecture patterns are documented with file references
- [ ] Integration points for the new feature are identified
- [ ] Conventions are documented (naming, testing, error handling)
- [ ] Open questions are listed (if any)
- [ ] State and decision journal are updated
- [ ] Domain glossary created/updated at `docs/domain-glossary.md`

### Engram Save

Before presenting the checkpoint:

1. Call `mem_save` with:
   - key: `{engramProjectKey}-phase2`
   - content: phase summary — key findings, decisions made, artifacts produced
2. Update `state.json` with completed phase and artifact paths

### Documentation Update Check

Ask: "Does anything need updating in project docs (C4 diagrams, decision journal, architecture docs, README)?"
If yes — update before presenting checkpoint.

## Checkpoint

Present to the user:

1. **Architecture summary** (3-5 sentences)
2. **Key patterns** the implementation must follow
3. **Integration points** where the feature connects
4. **Open questions** that need resolution before design
5. Options: [Continue to Design & Architecture] [Pause] [End]
