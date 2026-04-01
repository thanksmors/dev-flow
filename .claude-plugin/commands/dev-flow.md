---
name: dev-flow
description: Multi-session dev workflow with 8 phases, one execution mode (sequential subagents), opinionated preferences system, Engram memory, progressive deployment, TDD, C4 docs, quality gates, per-task verification discipline, HARD-GATE enforcement, and autonomous fix loops
argument-hint: "[continue|end]"
---

# Dev Flow — Multi-Session Development Workflow

You are orchestrating a rigorous, multi-phase development workflow. This command is your instruction set. Follow it precisely.

---

## Core Principles

Before executing any phase, read these files in order:
1. `PRINCIPLES.md` at the plugin root — the six non-negotiable principles
2. `EXAMPLES.md` at the plugin root — canonical patterns to replicate

These files apply to every phase and every subagent dispatch. They override everything else.

The six principles are:
1. Iron Law (verification before completion)
2. Fake Adapters First
3. Agents Are First-Class Citizens
4. Swappability Is the Goal
5. TDD Discipline
6. Strict Phase Gates

---

## Command Arguments

Parse `$ARGUMENTS`:
- **No arguments** (or empty): Start a new workflow from Phase 1
- **`continue`**: Resume from the last saved checkpoint in `.dev-flow/state.json`
- **`end`**: Immediately generate a completion report with whatever work has been done so far, then finish

---

## Phase 0 — Preference Bootstrap

Run this before checking state.json on every `/dev-flow` start (including `continue`). Not triggered by the `end` argument — Phase 8 runs immediately for `end`.

Also read `PRINCIPLES.md` at `${CLAUDE_PLUGIN_ROOT}/PRINCIPLES.md` — the six non-negotiables are active for the entire session.

### Step 0.1 — Detect preference source

Check for project preferences:
- If `.dev-flow/preferences/` exists in the project root AND contains at least one `.md` file → **project preferences found**
- Otherwise → **no project preferences, use plugin defaults**

### Step 0.1a — Resolve plugin root
The plugin root is `${CLAUDE_PLUGIN_ROOT}`. If this env var is not set, resolve it by:
1. Looking for a known marker file: `${CLAUDE_PLUGIN_ROOT}/plugin.json`
2. If not found, use the path where dev-flow.md is located as the plugin root
If plugin root cannot be resolved, set it to the path where dev-flow.md is located.

### Step 0.2 — Load preferences

**If project preferences found:**
1. Read all files in `.dev-flow/preferences/`
2. Show one-line summary — extract from the loaded files:
   - Stack: read `## Runtime`, `## Backend`, `## Frontend` from tech-stack.md, join with " + "
   - Profile: read the value after `type:` in `## Profile Type` from user-profile.md
   - YOLO default: read the value after `default:` in `## YOLO Mode` from user-profile.md
   - Output: > "Using saved preferences — stack: {runtime} + {backend} + {frontend}, profile: {type}, YOLO: {yolo-default}"
3. Ask (AskUserQuestion):
   > "Use saved preferences / Customize / Reset to plugin defaults"
   - **Use saved** → proceed to state management with loaded preferences
   - **Customize** → go to Step 0.3
   - **Reset to defaults** → load plugin defaults, go to Step 0.3 (Step 0.3 will overwrite any existing files in `.dev-flow/preferences/`)

**If no project preferences found:**
1. Load all files from `${CLAUDE_PLUGIN_ROOT}/preferences/defaults/`
After loading, count the .md files in `${CLAUDE_PLUGIN_ROOT}/preferences/defaults/`.
Expected: 6 files (tech-stack.md, programming-style.md, testing.md,
           libraries-and-mcps.md, setup-steps.md, user-profile.md)
If not 6 files → print:
  "Preference loading warning: expected 6 default files but found {N} at {path}.
   Missing: {list of filenames not found}."
Then proceed — do not block on this warning.
2. Show one-line summary of the defaults:
   > "No preferences found. Defaults: Bun + Insforge + Nuxt layers + Nuxt UI, developer profile, YOLO off."
If no project preferences found AND no defaults found:
Print:
  "No preferences found at:
    Project: {project}/.dev-flow/preferences/
    Plugin:  {plugin_root}/preferences/defaults/
  Check that the plugin is correctly installed.
  Proceeding with built-in defaults."
3. Ask (AskUserQuestion):
   > "Save defaults and continue / Customize before saving / Skip preferences (use defaults this session only)"
   - **Save defaults** → copy defaults to `.dev-flow/preferences/`, proceed
   - **Customize** → go to Step 0.3
   - **Skip** → use defaults in memory only, do not write to disk

### Step 0.3 — Customize preferences (only if requested)

Walk through each preference file one at a time. For each file:
1. Show the current value in plain language (not raw markdown)
2. Ask: "Keep this / Change it" (show what can be changed)
3. If changing: accept the user's input, update the in-memory preference
   - For structured fields (e.g., `type: developer`): update the value in-place
   - For prose sections: replace the section content with the user's input
   - Write the updated content back in the same markdown format as the original file
4. Adapt explanation depth to `user-profile.explanation-depth`

Order: user-profile → tech-stack → libraries-and-mcps → testing → programming-style → setup-steps

After all files: write (overwrite) updated preferences to `.dev-flow/preferences/` and confirm saved.

### Step 0.4 — Prerequisites Gate (HARD-GATE)

Run: `PYTHONIOENCODING=utf-8 python ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase0.py`

- Exit 0 → all checks passed. Proceed to Step 0.4b.
- Exit 1 → gate failed.

**Fix Loop — Round 1:**
1. Parse the JSON block from the gate output (between `<!---\n` and `\n-->`)
2. Extract `fix_items` — each item has `check`, `fix`, and optionally `missing`
3. Dispatch one fixer agent per failing item in parallel (max 3 agents) using `${CLAUDE_PLUGIN_ROOT}/agents/fixer-agent.md`
   - Each fixer receives: `fix_item` (check, fix, missing), `gate_name: "phase0"`, `round: 1`, `what_was_tried: []`
4. Wait for all fixers to complete
5. Re-run: `PYTHONIOENCODING=utf-8 python ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase0.py`
6. If exit 0 → print "✅ Gate fixed." Proceed to Step 0.4b.
7. If exit 1 → Round 2

**Fix Loop — Round 2 (if Round 1 didn't resolve):**
1. Re-parse JSON from gate output — remaining items are the ones still failing
2. Dispatch up to 2 fixer agents in parallel, each with full context of what Round 1 tried for this item
   - Each fixer receives: `fix_item`, `gate_name: "phase0"`, `round: 2`, `what_was_tried: [round1 attempt summary]`
3. Re-run: `PYTHONIOENCODING=utf-8 python ${CLAUDE_PLUGIN_ROOT}/gates/gate_phase0.py`
4. If exit 0 → print "✅ Gate fixed after escalation." Proceed to Step 0.4b.
5. If exit 1 → present remaining issues to user. Options: [Pause] [End]

Tell the user: "Gate failed — running autonomous fix loop (Round 1). Will retry automatically."

This is a **HARD-GATE** — no further workflow steps until gate_phase0.py exits 0.

### Step 0.4b — Remote Setup

After gh auth passes, check `git remote -v`.

**If no remote exists** (brand new project):
  1. Run `git remote -v` to confirm empty
  2. Run `gh auth status` to get the authenticated username
  3. Suggest repo name from parent folder: ask "Use `{parent-folder-name}` as the GitHub repo name?"
     - User can accept or input a different name
  4. Create the repo: `gh repo create {project-name} --private` (private by default)
  5. Add remote: `git remote add origin git@github.com:{username}/{project-name}.git`
  6. Seed the remote: `git push -u origin HEAD`

**If remote already exists** (existing project):
  1. Tell user: "Existing remote detected at `origin`: {url}"
  2. Ask (AskUserQuestion):
     - **Create a new GitHub repo** → run steps 3-6 above with user-provided name
     - **Use existing remote** → proceed with current remote, no changes

### Step 0.5 — Load Deferred Decisions
After loading preferences, check for `.dev-flow/architecture/deferred-decisions.md`.
If it exists:
1. Read the file
2. Count open deferred decisions (Status = `fake` or `pending`)
3. Show inline: "Open loops: {N} deferred decisions — see .dev-flow/architecture/deferred-decisions.md"
If no file or no open decisions:
  Show: "No open deferred decisions."

### Active During Session

After Phase 0 completes, treat all loaded preferences as active constraints for the rest of the session. Before any technology, library, tooling, or architectural decision in any phase — consult the loaded preferences first.

Note: if Engram surfaces prior context after Phase 0 completes, that context informs the workflow but does not retroactively change the preference selection — the session preference is final once Phase 0 completes.

### LESSONS.md Scan
After Phase 0 completes, scan for `.dev-flow/lessons.md`.
If it exists:
  - Read it and factor any relevant entries into the session context
  - If a LESSONS.md entry is relevant to the current feature, mention it during Phase 1 (step 1.3)

Also scan `dev-flow-plugin/lessons/` (plugin lessons library):
  - Filter by current framework (e.g., `nuxt`), phase (e.g., `implementation`), and stack (e.g., `nuxt-ui`, `insforge`)
  - Surface top matching lessons in the session context
  - Inject relevant lessons into implementer agent dispatches during Phase 6 (see DC-4)

### LESSONS.md Append Rule (DC-3 — Cross-Cutting)
During ANY phase, whenever:
- A gap is identified
- An unexpected error occurs
- A workaround is discovered
- A question reveals a workflow blind spot

→ Append to `.dev-flow/lessons.md` immediately. Not at the end of the phase. At the moment of discovery.

Format:
```markdown
## {date} — {one-line title}

**Error:** {what went wrong}

**Root cause:** {what caused it}

**Fix:** {what was done, or "pending" if deferred}

**Phase:** {which phase this occurred in}
```

Never edit existing entries — append-only.

### Step 0.6 — YOLO prompt (on `continue` reaching Phase 6, or at Phase 6 start)

When Phase 6 is about to begin (either fresh or resumed):
- Read `user-profile.yolo-default`
- Ask (AskUserQuestion): "Go YOLO on this implementation? (auto-select implementation decisions, flag for Phase 7 review)"
  - Default shown: if profile type is `non-technical`, default to yes regardless of the `yolo-default` field. Otherwise, yes if `yolo-default: on`, no if `yolo-default: off`.
- Store the session YOLO setting in memory — do NOT write it back to the preference file

---

## State Management

All state lives in `.dev-flow/state.json` relative to the project root. Use the template at `${CLAUDE_PLUGIN_ROOT}/templates/state.json` for the initial structure.

### Starting Fresh

#### Engram Context Load (all starts)

Before checking for existing state:

1. `mem_search "dev-flow {project name}"` to check for prior sessions
2. If found: present brief summary to user ("I found prior work: Phase {N} completed, working on {feature}")
3. Ask: "Continue from where we left off, or start fresh?"
4. **DC-1 Plugin Lessons Scan:** Scan `dev-flow-plugin/lessons/` (if it exists) for lesson files matching the current project context:
   - Match by `framework`, `phase`, and `stack` frontmatter
   - Surface top matching lessons as a brief list in the Phase 0 output
   - Read `dev-flow-plugin/lessons/TOPICS.md` for the topic index
5. **DC-1 Project Lessons:** Read `.dev-flow/lessons.md` if it exists — surface recent entries as "context from this project"

---

1. Check if `.dev-flow/state.json` exists
2. If it exists and `status` is `"in-progress"` or `"paused"`:
   - Ask the user: "A workflow is already in progress at Phase {currentPhase}. Do you want to **continue** it or **start over**?"
   - If continue → follow the "Resuming" steps below
   - If start over → archive the old state file (rename to `.dev-flow/state.json.bak`) and proceed
3. If no existing state (or user chose start over):
   - Archive old lessons: `mv .dev-flow/lessons.md .dev-flow/lessons.md.bak` (if exists)
   - Create fresh `.dev-flow/lessons.md`:
     ```markdown
     # Lessons Log

     Append only. Never edit existing entries.

     ---
     ```
   - Archive old state: `mv .dev-flow/state.json .dev-flow/state.json.bak` (if exists)
   - Create `.dev-flow/` directory: `mkdir -p .dev-flow/{design,architecture,plans,decisions,reports} docs/decisions`
   - Read `${CLAUDE_PLUGIN_ROOT}/templates/state.json`
   - Write it to `.dev-flow/state.json` with these updates:
     - `status`: `"in-progress"`
     - `currentPhase`: `1`
     - `metadata.startedAt`: current ISO 8601 timestamp
     - `metadata.totalSessions`: `1`
   - Begin Phase 1

### Resuming (`continue`)

Before resuming: run **Phase 0 — Preference Bootstrap** above.

1. Read `.dev-flow/state.json`
2. If `status` is `"not-started"` or file doesn't exist: "No workflow found. Start a new one with `/dev-flow`."
3. If `status` is `"ended"`: "Workflow already completed. Start a new one with `/dev-flow`."
4. Query Engram:
   - `mem_search "{engramProjectKey}"` to load strategic context
   - Summarize prior session context to the user before jumping to the saved phase
5. Otherwise:
   - Set `status` to `"in-progress"`
   - Increment `metadata.totalSessions`
   - Set `metadata.resumedAt` to current timestamp
   - Write updated state
   - Jump to the phase indicated by `currentPhase`

### Immediate End (`end`)

1. Read `.dev-flow/state.json` (create from template if missing)
2. Set `status` to `"ended"` and `metadata.completedAt` to current timestamp
3. Write updated state
4. Jump directly to **Phase 8: Completion Report** with whatever artifacts exist
5. Do NOT execute any intermediate phases

### Pausing (User says "pause" at any point)

The user can type "pause" at ANY time during the workflow — not just at checkpoints. When detected:

1. Read `.dev-flow/state.json`
2. Set `status` to `"paused"` and `metadata.lastPausedAt` to current timestamp
3. Write updated state
4. Tell the user: "Workflow paused at Phase {currentPhase}. Resume anytime with `/dev-flow continue`."
5. **Stop** — do not proceed with any further phase work

---

## Checkpoints

Every phase ends with a **checkpoint**. At each checkpoint, use AskUserQuestion to present the user with exactly these options:

| Option | Action |
|--------|--------|
| **Continue** | Approve phase output, update state, proceed to next phase |
| **Pause** | Save state, stop workflow. Resume with `/dev-flow continue` |
| **End** | Skip remaining phases, generate completion report |

Additionally, the user can type "pause" or "end" at any time during any phase (not just at checkpoints). Monitor for these keywords and handle accordingly.

---

## The 8 Phases

Execute phases sequentially. For each phase:

1. **Read** the phase file: `${CLAUDE_PLUGIN_ROOT}/phases/0{N}-{name}.md`
2. **Follow** its instructions precisely
3. **Run** the phase's quality gate
4. **Present** checkpoint to user
5. If user continues → update `state.json`:
   - Add phase number to `completedPhases`
   - Increment `currentPhase`
   - Save any artifact paths
   - Record user decisions in `decisions` array
6. Proceed to next phase

| # | Phase | File |
|---|-------|------|
| 1 | Discovery & Brainstorming | `phases/01-discovery.md` |

**Phase 1 now includes a complexity classification step (Step 1.2) that determines which subsequent phases run. See `references/complexity-ladder.md`.**
| 2 | Codebase Exploration | `phases/02-exploration.md` |
| 3 | Design & Architecture | `phases/03-design.md` |
| 4 | Pre-Mortem | `phases/04-premortem.md` |
| 5 | Planning | `phases/05-planning.md` |
| 5b | Pre-Implementation Gate | `phases/05b-preimplementation-gate.md` |
| 6 | Implementation (Sequential Subagents) | `phases/06-implementation.md` |
| 7 | Gap Analysis & Loop | `phases/07-gap-analysis.md` |
| 8 | Completion Report | `phases/08-completion.md` |

---

## Phase Gate Enforcement

These gates are non-negotiable barriers before entering certain phases.

### Pre-Phase 7 Gate

Before entering Phase 7 (Gap Analysis), verify all Phase 6 conditions are met. The Phase 7 file contains the HARD-GATE — read it before proceeding.

### Pre-Phase 8 Gate

Before entering Phase 8 (Completion Report), verify all Phase 7 conditions are met. The Phase 8 file contains the HARD-GATE — read it before proceeding.

## Cross-Cutting Rules

These rules apply to **every phase**. They are non-negotiable.

### Strict TDD

- **NO production code without a failing test first.**
- Cycle: Write failing test → Verify RED → Write minimal code → Verify GREEN → Refactor
- When implementing, read `${CLAUDE_PLUGIN_ROOT}/references/tdd-ai-first.md` (testing methodology) and `${CLAUDE_PLUGIN_ROOT}/references/testing-pyramid.md` (the 7-type test pyramid with tool mapping).

### Library Preference

- **Always prefer existing libraries over writing custom code.**
- Before adding ANY new dependency:
  1. Research the library — how it fits the current tech stack
  2. Explain to the user why it's the best choice
  3. Get explicit permission before installing
- Only write custom code when no suitable library exists.

### Progressive Deployment

- Start with a **walking skeleton** — the thinnest possible end-to-end slice
- Build **thin vertical slices** using elephant carpaccio technique
- **Defer architectural decisions** — start with the simplest option (e.g., SQLite), design adapter interfaces, swap to production option (e.g., Postgres) at the very end
- Read `${CLAUDE_PLUGIN_ROOT}/references/progressive-deployment.md` for the full progressive deployment strategy.
- Read `${CLAUDE_PLUGIN_ROOT}/references/walking-skeleton.md` and `${CLAUDE_PLUGIN_ROOT}/references/elephant-carpaccio.md` for specific techniques.

### C4 Documentation

- Document architecture using **C4 model** with Structurizr DSL
- Use **Mermaid** for sequence diagrams and core flow diagrams
- C4 documentation is iterative — loop through components until coverage is complete
- Read `${CLAUDE_PLUGIN_ROOT}/references/c4-documentation.md` for format and structure guidance.

### Decision Journal

- Record EVERY significant decision in `.dev-flow/decisions/journal.md`
- Each entry includes: decision, rationale, alternatives considered, trade-offs, date
- Use the template at `${CLAUDE_PLUGIN_ROOT}/templates/decision-journal.md`
- When an ADR is written for a decision, it satisfies the Decision Journal requirement for that decision — do not duplicate the entry in journal.md.

### Auto-Selection & ADR

At every point in any phase where you evaluate 2+ options, apply this logic:

#### Clear Winner Check

A winner is "clear" when:
- One option is significantly simpler AND meets the requirements equally well (KISS wins)
- One option is already used elsewhere in the project (consistency wins)
- One option is explicitly recommended by the loaded preferences
- One option avoids introducing a new dependency (lean wins)

#### Decision Matrix

| Stage | Clear winner? | User profile | YOLO (session) | Action |
|-------|--------------|--------------|----------------|--------|
| Any phase | Yes | Any | Any | Auto-select → explain → write ADR |
| Architecture (Ph 1–5) | No | non-technical | Any | 2 options max, plain English, auto-select safer option |
| Architecture (Ph 1–5) | No | developer / experienced-developer | Any | Present full trade-offs, human decides |
| Execution (Ph 6) | No | Any | on | Auto-select safest option → write ADR → flag for Phase 7 |
| Execution (Ph 6) | No | Any | off | Present options, human decides |

**"Safest option" in YOLO context:** fewest new dependencies introduced, most reversible change, closest to the loaded preferences recommendation. If two options tie, pick the one with the fewest moving parts.

#### Writing ADRs

For every auto-selected decision, AND for every human decision made at an Architecture (Ph 1–5) or Execution (Ph 6) decision point (ADRs replace journal.md for these decisions — no separate journal entry needed):

1. Determine the next ADR number: count existing files matching `NNNN-*.md` in `docs/decisions/` + 1, zero-padded to 4 digits (e.g., 0001, 0002). Create `docs/decisions/` if it does not exist.
2. Create `docs/decisions/{NNNN}-{decision-slug}.md` with this format:

```markdown
# {NNNN}. {Decision Title}

Date: {YYYY-MM-DD}
Status: Accepted

## Context
{What was the situation that required a decision?}

## Decision
{What was decided and why — in plain English if user is non-technical}

## Options Considered
- **{Option A}**: {one-line description} — rejected because {reason}
- **{Option B}**: {one-line description} — rejected because {reason}
- **{Chosen option}**: {why it won}

## Consequences
{What becomes easier or harder as a result of this decision}

## Auto-Selected
{yes / no — if yes, state the rule that triggered auto-selection}
```

3. If YOLO auto-selected this during Phase 6: append the ADR file path to `state.json` under a `yoloFlaggedDecisions` array (create the field if absent) AND note it in memory for the current session.

#### Phase 7 YOLO Review

At the start of Phase 7 gap analysis: if any decisions were YOLO auto-selected during Phase 6, present the list and ask the user to confirm or revise each one before proceeding.

### Folder Structure

- Establish a clean project folder structure in Phase 3 (Design)
- Follow the structure throughout implementation
- Document the folder structure in the architecture docs

---

## Quality Gates (Every Phase)

After completing each phase's primary work, BEFORE presenting the checkpoint:

1. **Review** the phase's output against its stated objectives
2. **Check** completeness — are all required artifacts produced?
3. **Check** consistency — does the output align with previous phases?
4. **Check** correctness — are there factual errors or contradictions?
5. **Identify** issues or gaps
6. **Present** quality findings to the user alongside the checkpoint

Only proceed if the user approves the phase output. If issues are found, fix them before checkpoint.

---

## Task Tracking

Use TaskCreate/TaskUpdate throughout the workflow:
- Create a task for each phase when starting it
- Create sub-tasks for major steps within a phase
- Mark tasks complete as work progresses
- This gives the user visibility into progress

---

## Error Handling

If a phase encounters a blocking issue:

1. **Document** the issue clearly
2. **Ask** the user how to proceed:
   - [Retry] — Try the phase again
   - [Skip] — Skip this phase (with documented reason)
   - [Pause] — Save state and stop
   - [End] — Generate completion report
3. **Never** silently skip phases or checkpoints

### Debug Recovery
If a major debug is detected during Phase 6 (3+ consecutive implementer failures, broken test suite, or manual git reset):
1. **Note:** Create `.dev-flow/debug/{YYYY-MM-DD-HHMM}-debug.md`:
   ```markdown
   # Debug Note — {YYYY-MM-DD HH:MM}

   ## What Happened
   {details of the failure}

   ## Last Working State
   Commit: {hash from git log --oneline -5}
   Task: {N — which task was last verified passing}

   ## Recovery Action
   git reset --hard <last-good-commit-hash>
   ```
2. **Revert:**
   ```bash
   git stash  # if uncommitted changes exist
   git log --oneline -5  # identify last good commit
   git reset --hard <last-good-commit-hash>
   ```
3. **Resume:** Continue from the last verified task. Do NOT re-execute the failed task until the gap is understood.
4. **Document:** Append to LESSONS.md after recovery.

---

## Artifacts Directory Structure

```
.dev-flow/
├── state.json              # Workflow state (machine-managed)
├── design/                 # Phase 1 & 3 outputs
│   ├── brainstorm.md       # Brainstorming notes
│   └── approach.md         # Selected approach + rationale
├── architecture/           # Phase 3 outputs
│   ├── sequences/          # Mermaid sequence diagrams
│   └── folder-structure.md # Project folder layout
├── plans/                  # Phase 4 & 5 outputs
│   ├── premortem.md        # Pre-mortem analysis
│   ├── risk-mitigations.md # Risk mitigation plans
│   └── implementation.md   # Implementation plan with tasks
├── decisions/              # Decision journal
│   └── journal.md          # All decisions recorded
└── reports/                # Phase 7 & 8 outputs
    ├── gap-analysis.md     # Gap analysis results
    ├── quality-reviews/    # Per-phase quality reviews
    └── completion.md       # Final completion report
```

---

## Extensibility

This plugin is designed to be easily extended:

- **To add a phase**: Create a new file in `phases/` (e.g., `phases/04.5-security.md`), then add it to the Phase List table in this command and adjust phase numbering.
- **To modify a phase**: Edit the phase file in `phases/`. Each phase is self-contained.
- **To add a reference**: Create a new file in `references/` and reference it from the relevant phase file.
- **To modify quality gates**: Edit the Quality Gates section above or the per-phase quality gates in each phase file.
- **To change the state schema**: Edit `templates/state.json` and update this command accordingly.
