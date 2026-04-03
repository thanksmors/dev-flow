---
name: discovery
description: Understand what needs to be built, explore the problem space, and converge on an approach with the user
---

# Phase 1: Discovery & Brainstorming

**Objective**: Understand what needs to be built, explore the problem space, and converge on an approach with the user.

## Steps

### 1.0 Load Prior Context

Before anything else:

1. Run `mem_search` with the project name and "devloop" to check for prior session context
2. Run `mem_search` with the feature name or description if provided
3. If prior context found: summarize it for the user ("I found prior work on this: ...") and ask if it's relevant
4. Set `metadata.engramProjectKey` in state.json to `devloop-{featureName}` (slugified)

### 1.1 Understand the Request

- Read the user's original feature request / issue / description
- If the user invoked `/devloop` with a description, use that as the starting point
- If unclear, ask clarifying questions (one at a time, not a wall of questions):
  - What problem does this solve?
  - Who are the users?
  - What are the success criteria?
  - Are there constraints (tech stack, timeline, budget)?

### 1.2 Classify Complexity (Required — Do Not Skip)

This step determines which phases run and how thoroughly each is executed. Do not proceed to Step 1.3 until the complexity tier is set in `state.json`.

1. Read `references/complexity-ladder.md` to understand the three tiers and their criteria
2. Walk through the five decision tree questions:
   - **Q1**: Is this a single-file or small surface change?
   - **Q2**: Are requirements fully clear with no ambiguity?
   - **Q3**: Does it affect multiple components or require new dependencies?
   - **Q4**: Are there security, performance, or compliance needs?
   - **Q5**: Are there external integrations or API changes?
3. Apply the decision tree to determine the tier: Simple, Moderate, or Complex
4. Update `state.json` with the classification:
   - **For Tier 1 (Simple)**: Set `metadata.complexityTier` to `"simple"` and initialize `metadata.phasesSkipped` with all phases being skipped
   - **For Tier 2 (Moderate) or Tier 3 (Complex)**: Set `metadata.complexityTier` to `"moderate"` or `"complex"` and clear `metadata.phasesSkipped` to an empty array

**Tier 1 special note**: If the task is Tier 1, Phase 3 is replaced with a lightweight substitute. In your approach document, add a section listing the files changed and any interface considerations. This is not a full Phase 3 — it is a abbreviated note that satisfies the phase without running it.

**Tier 3 special requirement**: If the task is Tier 3, Phase 3 must include a component diagram showing all major components and their interactions. Flag this requirement in your approach document so it is not missed during Phase 3.

**Do not skip this step.** The complexity classification affects every subsequent phase. If you are unsure whether to classify as Tier 1, 2, or 3, lean toward the higher tier — it is easier to skip phases later than to discover you needed them.

### 1.3 Explore Project Context

- Check for existing documentation: `README.md`, `docs/`, `CLAUDE.md`, `AGENTS.md`
- Check recent git history: `git log --oneline -20`
- Check the current project structure
- Identify any existing design docs or plans in `.dev-flow/` or `docs/`
- Note the tech stack from `package.json`, `Cargo.toml`, `go.mod`, or equivalent

### 1.3.x — LESSONS.md Check
Scan for `.dev-flow/lessons.md`.
If it exists:
  - Read all entries
  - If any entry is relevant to the current feature, note it: "Prior lesson relevant to this feature: {title} — {one-line summary}"
If a gap is discovered during this session (not covered by the workflow):
  - Append to `.dev-flow/lessons.md` using the format:
```markdown
## {YYYY-MM-DD} — {one-line title}

**Gap:** What went wrong / what the workflow missed

**Fix:** What to do differently next time

**Files to update:**
- `dev-flow/phases/XX-xxx.md` — {specific change needed}

**Context:** {what was being attempted, what triggered the revert}
```

### 1.4 Brainstorm Approaches

Propose **2-3 distinct approaches** for solving the problem. For each approach, describe:

- **What it is** (2-3 sentences)
- **Pros** (why it might be good)
- **Cons** (trade-offs and risks)
- **Complexity estimate** (simple / moderate / complex)
- **Your recommendation** and why

Present approaches clearly so the user can compare them.

### 1.5 Capture the Decision

Once the user selects an approach:

1. Document it in `.dev-flow/design/approach.md`:
   - Selected approach name
   - Rationale for selection
   - Alternatives considered and why they were rejected
   - Key assumptions
   - Known constraints
2. Update `state.json`:
   - `artifacts.designDoc`: `.dev-flow/design/approach.md`
   - `metadata.featureName`: short name
   - `metadata.featureDescription`: one-line description
   - Add decision to `decisions` array

### 1.6 Decision Journal Entry

Record this decision in `.dev-flow/decisions/journal.md` using the template format:
```
## [YYYY-MM-DD] Approach Selection: {name}
- **Decision**: Selected {approach}
- **Rationale**: {why}
- **Alternatives**: {list rejected approaches and reasons}
- **Trade-offs**: {key trade-offs accepted}
```

## Quality Gate

Before presenting the checkpoint, verify:

- [ ] The approach is clearly documented with rationale
- [ ] At least 2 alternatives were considered
- [ ] Key assumptions are explicit
- [ ] The decision journal has been updated
- [ ] `state.json` reflects the current state

If any item is missing, complete it before checkpoint.

### Engram Save

Before presenting the checkpoint:

1. Call `mem_save` with:
   - key: `{engramProjectKey}-phase1`
   - content: phase summary including selected approach, key decisions, assumptions
2. Update `state.json` artifacts and decisions array

### Documentation Update Check

Ask: "Does anything need updating in project docs (README, existing architecture docs, CLAUDE.md)?"
If yes — update before presenting checkpoint.

## Checkpoint

Present to the user:

1. **Summary** of the selected approach
2. **Key assumptions** that could invalidate the approach
3. **Any concerns** or open questions
4. Options: [Continue to Codebase Exploration] [Pause] [End]
