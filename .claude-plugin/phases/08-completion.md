---
name: completion
description: Generate a comprehensive completion report and present integration options
---

# Phase 8: Completion Report

**Objective**: Generate a comprehensive completion report, finalize all documentation, and present the user with integration options.

<HARD-GATE>
You cannot enter Phase 8 (Completion Report) until:
✅ Phase 7 gap analysis is complete
✅ All Critical and Important gaps are fixed
✅ Minor gaps are documented with deferral reason
✅ All tests pass (fresh verification evidence required)
✅ Completion report draft exists at .dev-flow/reports/completion.md
</HARD-GATE>

When the HARD-GATE passes: log gate pass in state.json under `gatePasses.prePhase8`, then proceed.

### 8.1 Generate Completion Report

Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/completion-report.md` and use it to write the completion report to `.dev-flow/reports/completion.md`. Fill in every section with actual values from the workflow.

### 8.2 Draft README

Read `.dev-flow/design/readme-outline.md` and the example READMEs:
- https://raw.githubusercontent.com/Azure-Samples/serverless-chat-langchainjs/refs/heads/main/README.md
- https://raw.githubusercontent.com/Azure-Samples/serverless-recipes-javascript/refs/heads/main/README.md
- https://raw.githubusercontent.com/sinedied/run-on-output/refs/heads/main/README.md
- https://raw.githubusercontent.com/sinedied/smoke/refs/heads/main/README.md

Draft the README following the outline. Use:
- GFM (GitHub Flavored Markdown) throughout
- GitHub admonition syntax for notes and warnings
- No LICENSE / CONTRIBUTING / CHANGELOG sections (separate files)
- A logo or icon if one exists for the project

Save to `README.md` in the project root. Present to user before integration options.

### 8.3 Finalize Structurizr Workspace

Ensure `docs/workspace.dsl` reflects the **actual final implementation**:

1. Compare each container and component in the model against the actual code
2. Update model elements for anything added, renamed, or removed during implementation
3. Verify every view renders without errors (Structurizr Lite shows parse errors in the browser)
4. Confirm `workspace.json` is current (Structurizr Lite regenerates it on each save of `workspace.dsl`)
5. Commit `workspace.json` — it should be in sync with `workspace.dsl`

Then audit `docs/architecture/`:

6. Read each section — does it accurately describe what was actually built?
7. Update any section where reality diverged from the Phase 3 draft
8. Confirm all diagram embeds still reference valid view keys (e.g. `embed:SystemContext`, `embed:Containers`)

### 8.3 Finalize Architecture Decision Records

Review `docs/decisions/` to ensure it is complete and all Status fields are current:

1. Verify an ADR exists for every significant decision across all phases:
   - Phase 1: approach selection (`0001-approach-selection.md`)
   - Phase 3: technology choices, deferred decisions
   - Phase 4: risk-driven design changes (if any)
   - Phase 6: implementation pivots
   - Phase 7: gap-fix architectural changes (if any)
2. If any decision is missing, write its ADR now (back-date the Date field if needed)
3. **Verify Status is current for every ADR:**
   - Read each ADR's `Status:` field
   - Confirm `Accepted` ADRs are still valid — update any that should now be `Superseded` or `Deprecated`
   - If a deferred decision was resolved, update the original ADR: set `Status: Superseded`, set `Superseded by: [ADR-N](000N-resolved-name.md)`, add a `Review notes:` entry
   - Confirm no decision is missing an ADR

### 8.4 Update State

Final state update:
- `status`: `"ended"`
- `metadata.completedAt`: current timestamp
- `artifacts.completionReport`: `.dev-flow/reports/completion.md`

### 8.5 Present Integration Options

Use AskUserQuestion to present exactly these options:

**Option 1: Merge to base branch**
- Merge the feature branch back to the base branch locally
- Run full test suite one final time
- Clean up worktree if applicable

**Option 2: Create a Pull Request**
- Push the branch to remote
- Create a PR with the completion report as the description
- Link any related issues

**Option 3: Keep the branch**
- Leave everything as-is for later work
- Branch and worktree remain intact

**Option 4: Discard this work**
- Requires the user to type "discard" to confirm
- Removes the worktree and branch
- Archives the `.dev-flow/` artifacts

### 8.6 Cleanup (if applicable)

For options 1, 2, or 4:
- If using a worktree, ask about cleanup
- Offer to archive `.dev-flow/` artifacts before cleanup
- Remove any temporary files

For option 3:
- Ensure state is saved
- Remind user how to resume: `/devloop continue`

## Quality Gate

Before presenting the integration options, run **mandatory final verification**:

1. Run the full test suite — show full output
2. If any failures → do NOT present integration options → fix failures first
3. Only when all tests pass with evidence shown → present integration options

Before presenting the integration options, verify:

- [ ] Completion report is comprehensive and accurate
- [ ] README is complete and passes AI Slop Test
- [ ] `docs/workspace.dsl` model matches the actual implementation
- [ ] All `docs/architecture/` sections are accurate and complete
- [ ] `docs/decisions/` contains ADRs for all significant decisions across all phases
- [ ] `workspace.json` is current and committed
- [ ] All tests pass (final verification)
- [ ] `state.json` is finalized
- [ ] The user has clear next steps

### Final Engram Save

1. Call `mem_save` with:
   - key: `{engramProjectKey}-complete`
   - content: completion summary — what was built, final test count, key decisions, lessons learned, any follow-up work identified
2. This enables future sessions on this project to immediately load the full context

## Final Output

After the user selects an integration option, execute it and confirm:

"devloop complete for **{feature name}**.

- Phases completed: {N}/8
- Total tests: {N}
- Sessions: {N}
- Report: `.dev-flow/reports/completion.md`
- README: `README.md` in project root

{Integration action taken}"
