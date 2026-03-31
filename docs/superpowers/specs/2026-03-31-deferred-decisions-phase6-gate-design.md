# Design: Phase 6 Deferred-Decision Gate, Pre-Flight Check, and Structurizr Cleanup

Date: 2026-03-31
Status: Approved

## Context

The dev-flow plugin has three workflow issues that cause user pain during Phase 6+:

1. **Deferred decisions are ignored until it's too late.** They surface briefly in Phase 6.5 but the user is immediately funneled toward Phase 7/8. By then there are accumulated fake adapters and unresolved decisions — too much to tackle at once. The user wants to handle every deferred decision **before** Phase 7, one by one.

2. **Phase 6 starts without checking if third-party connections are configured.** When a task needs an env var (API key, DB connection string, webhook URL), the implementer subagent tries to run, fails, and the user has to debug a failure instead of being told upfront "you need to set these env vars before we start."

3. **Structurizr setup is more complex than needed.** The current docs show docker-compose, but for most users the one-liner Docker command is faster and simpler. The docker-compose option is unnecessary weight.

4. **`.dev-flow/architecture/c4` is an orphaned empty folder.** The C4 docs (`c4-documentation.md`) specify `docs/` as the home for all architecture files. The `dev-flow.md` command references `.dev-flow/architecture/c4/` in the artifacts directory structure, but that folder never gets populated. It should be removed from the artifacts layout.

5. **Structurizr DSL parse errors are opaque.** When `workspace.dsl` has an error (e.g., unexpected token), Structurizr shows a cryptic line/column message. The user had to debug two DSL errors manually. There should be basic pre-validation before Structurizr loads.

## Decisions

### D1: Phase 6 Pre-Flight Gate — Env Var and Third-Party Dependency Check

**Before any Phase 6 task runs**, scan all tasks for:
- Env var references (e.g., `process.env.STRIPE_KEY`, `$DATABASE_URL`)
- Third-party service connections (API calls to external hosts, database connections, auth provider setups)
- Any adapter marked `fake` in the deferred-decisions tracker

**If anything is missing:**
1. **Pause the workflow** — do not dispatch any implementer subagents
2. **List all missing dependencies** clearly:
   - Which env vars are referenced but not set
   - Which third-party services need accounts/credentials
   - What to configure and where
3. **User resolves** the missing pieces, then continues with `/dev-flow continue`
4. **Resume re-runs the pre-flight check** before proceeding

This is a **HARD-GATE** — nothing Phase 6 begins until pre-flight passes.

**Implementation location:** `phases/06-implementation.md` — add as Step 6.0 (before 6.1).

**Why not a warning?** A warning would let the user skip over missing dependencies. This is a hard block because starting tasks with unconfigured third-party connections wastes time and creates frustration.

---

### D2: Phase 6 End Deferred-Decision Gate

**After all Phase 6 tasks complete, before the Phase 7 checkpoint:**

1. **Read `.dev-flow/architecture/deferred-decisions.md`** — the tracker created during Phase 6
2. **List every open deferred decision** (Status = `fake` or `pending`), one by one
3. **For each decision, the user chooses:**
   - **Resolve** → run the Swap Protocol (mark fake deprecated, create real adapter, swap DI binding, run tests)
   - **Re-defer** → update the decision's `Trigger Criteria` with a new/written reason, keep it open
   - **Skip** (documented reason required) → mark as `deferred` with explanation

4. **All deferred decisions must have a final disposition** before Phase 7 begins.

This is a **HARD-GATE** on the Phase 7 checkpoint — the checkpoint options (Continue / Pause / End) are replaced with a deferred-decision review screen. The user cannot proceed to Phase 7 until all open items are handled.

**Implementation location:** `phases/06-implementation.md` — update Section 6.5 (Deferred Decision Swaps) to run as a hard gate before Phase 7, not as a soft footnote. Also update the Phase 6 checkpoint section.

**Why one-by-one?** The user specifically requested individual handling. Presenting them as a bulk list with "resolve all" shortcuts defeats the purpose — the friction of confronting each decision individually is intentional.

---

### D3: Structurizr — Docker-Only, Drop docker-compose

**Remove** the docker-compose service definition from `c4-documentation.md`.

**Keep only** the standalone Docker command:

```bash
docker run -it --rm -p 8080:8080 -v $(pwd)/docs:/usr/local/structurizr structurizr/lite
```

**Remove from docs:**
- The `docker-compose.yml` example
- The "Default: docker compose (wired to dev server)" section
- The "Start everything together: `docker compose up`" instruction

**Keep:**
- The standalone Docker one-liner
- The fallback label
- The auto-refresh note
- The localhost:8080 URL

**Rationale:** docker-compose is overkill for a tool the user runs once per modeling session. The one-liner is universally understood, works on any machine with Docker, and doesn't require project-level config files.

---

### D4: Remove `.dev-flow/architecture/c4` from Artifacts Directory

**Remove** the `.dev-flow/architecture/c4/` entry from the artifacts directory structure in `dev-flow.md`.

**Actual C4 location:** `docs/workspace.dsl` and `docs/architecture/` — as documented in `c4-documentation.md`. The `.dev-flow/architecture/` path was never populated and is misleading.

**Update:** `dev-flow.md` artifacts directory structure section. Remove the `c4/` row under `.dev-flow/architecture/`.

---

### D5: Structurizr DSL Pre-Validation

**Before launching Structurizr** (either via `docker run` command or any automated workflow step):

1. Check that `docs/workspace.dsl` exists
2. Run a basic syntax check on the DSL file
3. On parse error: surface a **clear error message** with:
   - The file and line number
   - The unexpected token
   - What was expected (Structurizr's expected tokens list)
   - A suggestion for common mistakes

**Implementation options:**
- **Option A (recommended):** Document the error patterns clearly in `c4-documentation.md` so the user can self-diagnose. Add a "Common DSL Errors" section with the two errors the user hit (`replace` misuse and `diComposition` component syntax).
- **Option B:** Add a small validation script (Node/Python) that wraps the docker run and parses the DSL before launching. Lower priority — the docs fix is enough for now.

**Proceed with Option A** — add a "Common DSL Errors" troubleshooting section to `c4-documentation.md`.

**The two errors from last session:**

Error 1 — `replace user [position:left]` at line 46:
- Cause: `replace` is not a valid Structurizr DSL keyword at the workspace level
- Fix: Remove the `replace` directive or move it inside the correct block

Error 2 — `diComposition = component "DI Composition" ...` at line 23:
- Cause: Component definitions inside a container block use `component "Name" "Description"` not `name = component "Name" ...`
- Fix: Remove the assignment operator when defining inline components

---

## Summary of Changes

| # | File | Change |
|---|------|--------|
| 1 | `phases/06-implementation.md` | Add Step 6.0 pre-flight gate (env vars + third-party deps) |
| 2 | `phases/06-implementation.md` | Update Section 6.5 — hard gate on Phase 7, one-by-one deferred decisions |
| 3 | `phases/06-implementation.md` | Update Phase 6 checkpoint to show deferred-decision gate before Phase 7 options |
| 4 | `phases/06-implementation.md` | Update Phase 6 Quality Gate checklist |
| 5 | `references/c4-documentation.md` | Remove docker-compose, keep Docker one-liner only |
| 6 | `references/c4-documentation.md` | Add "Common DSL Errors" troubleshooting section |
| 7 | `commands/dev-flow.md` | Remove `.dev-flow/architecture/c4/` from artifacts directory structure |
| 8 | `.dev-flow/architecture/deferred-decisions.md` | Tracker is created at Phase 3 (not Phase 6.5) — deferred decisions are documented as they are identified, not just at swap time |

---

## Deferred Decision Tracker Creation (Earlier)

The deferred-decisions tracker should be created **at Phase 3 (Design)** when decisions are first deferred — not at Phase 6.5 when swaps happen.

**Update:** In `phases/03-design.md`, when a deferred decision is documented as an ADR with Status `Pending` or `Deferred`, also add it to the tracker. This makes the tracker a living document from Day 1 of the project, not an afterthought.

The tracker template in `phases/06-implementation.md` already has the right structure — it just needs to be populated earlier and reviewed at the Phase 6 end gate.
