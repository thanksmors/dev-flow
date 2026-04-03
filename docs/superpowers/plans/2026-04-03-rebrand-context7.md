# Rebrand + Context7 Injection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the product from `devloop` to `devloop` (in-place text only), inject Context7 consultation rules into Phase 6 and Phase 7, and update skill references.

**Architecture:** Purely textual changes across ~50 files. No code logic modified. No directory renames. No new files created. Changes are safe to apply incrementally with per-task commits.

**Tech Stack:** Text replacement, bash find+sed or Perl-compatible regex, Git.

---

## Scope Summary

| Task | Type | Files Touched |
|------|------|--------------|
| 1. Rebrand `devloop` → `devloop` | Text replacement | ~50 files |
| 2. Context7 injection Phase 6 §6.3 | Instruction addition | 1 file |
| 3. Context7 injection Phase 7 §7.1 | Instruction addition | 1 file |
| 4. Context7 injection Phase 6 §6.8 debug | Instruction addition | 1 file |
| 5. Update skill references | Text replacement | 2 files |

**Does NOT change:** `.dev-flow/` directory (runtime-created per-project), `docs/superpowers/` (per-project artifacts), GitHub remote URL.

---

## File Map

### Command file rename
- Rename: `commands/devloop.md` → `commands/devloop.md`

### Plugin config (name/description changes only)
- Modify: `.claude-plugin/plugin.json` — `name` field and `description`
- Modify: `.claude-plugin/marketplace.json` — `name` field
- Modify: `.claude-plugin/hooks/hooks.json` — `description` field

### Phase files (name frontmatter + text replacements)
- Modify: `.claude-plugin/phases/01-discovery.md` — frontmatter `name`, all internal `devloop`/`devloop` references
- Modify: `.claude-plugin/phases/02-exploration.md` — frontmatter `name`, all internal references
- Modify: `.claude-plugin/phases/03-design.md` — frontmatter `name`, all internal references
- Modify: `.claude-plugin/phases/04-premortem.md` — frontmatter `name`, all internal references
- Modify: `.claude-plugin/phases/05-planning.md` — frontmatter `name`, all internal references
- Modify: `.claude-plugin/phases/05b-preimplementation-gate.md` — frontmatter `name`, all internal references
- Modify: `.claude-plugin/phases/06-implementation.md` — frontmatter `name`, all internal references, add Context7 blocks at §6.3 and §6.8
- Modify: `.claude-plugin/phases/06-extras.md` — frontmatter `name`, all internal references, skill reference update
- Modify: `.claude-plugin/phases/07-gap-analysis.md` — frontmatter `name`, all internal references, add Context7 block at §7.1
- Modify: `.claude-plugin/phases/08-completion.md` — frontmatter `name`, all internal references

### Agent files (name frontmatter + text replacements)
- Modify: `.claude-plugin/agents/implementer.md` — frontmatter `name`, agent title, internal references
- Modify: `.claude-plugin/agents/spec-reviewer.md` — frontmatter `name`, agent title, internal references
- Modify: `.claude-plugin/agents/quality-reviewer.md` — frontmatter `name`, agent title, internal references
- Modify: `.claude-plugin/agents/fixer-agent.md` — frontmatter `name`, agent title, internal references
- Modify: `.claude-plugin/agents/team-agent.md` — frontmatter `name`, agent title, internal references

### Reference files (text replacements)
- Modify: `.claude-plugin/references/subagent-delegation.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/c4-documentation.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/c4-dynamic.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/state-diagrams.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/cqrs-patterns.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/tdd-ai-first.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/layer-scaffold.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/component-identification.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/dsl-relationship-patterns.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/walking-skeleton.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/elephant-carpaccio.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/progressive-deployment.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/decision-trees.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/complexity-ladder.md` — frontmatter `name`, internal references
- Modify: `.claude-plugin/references/feature-sliced-design.md` — frontmatter `name`, internal references

### Preference set files (text replacements in `programming-style.md` comments)
- Modify: `.claude-plugin/preferences/sets/default/programming-style.md`
- Modify: `.claude-plugin/preferences/sets/full-stack/programming-style.md`
- Modify: `.claude-plugin/preferences/sets/nuxt-insforge/programming-style.md`
- Modify: `.claude-plugin/preferences/sets/default/setup-steps.md`
- Modify: `.claude-plugin/preferences/sets/full-stack/setup-steps.md`
- Modify: `.claude-plugin/preferences/sets/nuxt-insforge/setup-steps.md`

### Gate scripts (text replacements in comments/docstrings only)
- Modify: `.claude-plugin/gates/gate_phase0.py`
- Modify: `.claude-plugin/gates/gate_phase5b.py`
- Modify: `.claude-plugin/gates/gate_phase6_start.py`
- Modify: `.claude-plugin/gates/gate_phase6_end.py`

### Hook scripts (text replacements in comments)
- Modify: `.claude-plugin/hooks/precompact-save-state.py`
- Modify: `.claude-plugin/hooks/sessionstart-restore-state.py`

### Root-level project docs (text replacements)
- Modify: `README.md` — title, all internal references, `/devloop` → `/devloop`
- Modify: `PRINCIPLES.md` — title
- Modify: `PATTERNS.md` — text
- Modify: `EXAMPLES.md` — text, path references
- Modify: `.gitignore` — comment text

### Template files
- Modify: `.claude-plugin/templates/completion-report.md` — internal path references

---

## Task 1: Rebrand — Text Replacements

**Approach:** Run targeted find+sed replacements, then manually fix frontmatter fields and special cases. Do NOT use a blanket `devloop → devloop` replacement as it would corrupt `.dev-flow/` path references. Instead, use context-aware patterns.

### Step 1: Rename command file

- [ ] **Step 1: Rename `commands/devloop.md` → `commands/devloop.md`**

Run:
```bash
mv commands/devloop.md commands/devloop.md
```

### Step 2: Update plugin.json

- [ ] **Step 2: Update `.claude-plugin/plugin.json`**

Read the file, then edit:
- `"name": "devloop"` → `"name": "devloop"`
- The `description` field contains "devloop" in the text — update to "devloop" where it refers to the product name

### Step 3: Update marketplace.json

- [ ] **Step 3: Update `.claude-plugin/marketplace.json`**

Read the file, then edit:
- The `name` field under `categories[0].commands` from `"devloop"` to `"devloop"`

### Step 4: Update hooks.json description

- [ ] **Step 4: Update `.claude-plugin/hooks/hooks.json`**

Edit the `description` field:
- "devloop multi-session workflow" → "devloop multi-session workflow"

### Step 5: Bulk text replacements — safe patterns

Run each replacement in order. These are safe because they replace display text/product name, not path references:

- [ ] **Step 5a: Replace "devloop" → "devloop" (capitalized product name)**

```bash
# In all .md and .json files, replace "devloop" with "devloop"
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's/devloop/devloop/g' {} +
```

- [ ] **Step 5b: Replace "# devloop" → "# devloop" in headings**

```bash
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's/# devloop/# devloop/g' {} +
```

- [ ] **Step 5c: Replace "devloop" (in display text, not paths) with "devloop"**

This is the most delicate step. Replace `devloop` when it appears as:
- A product name in prose
- A CLI command reference (`/devloop` → `/devloop`)
- A frontmatter `name:` value like `name: devloop`
- A frontmatter `description:` containing "devloop" as product name

**Do NOT replace** when it appears as:
- Part of a file path: `.dev-flow/`, `dev-flow/phases/`, `dev-flow/`
- A directory path in bash commands
- A URL or remote reference: `github.com/thanksmors/devloop`

```bash
# Replace CLI command references: /devloop → /devloop
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's#/devloop#/devloop#g' {} +

# Replace @dev: skill references → @devloop:
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's/@dev:/@devloop:/g' {} +

# Replace "devloop" as product name in prose (not in paths)
# Only matches when surrounded by word boundaries or spaces, not slashes
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's/(?<![/.])devloop(?![.\/])/devloop/g' {} +
```

After running, visually spot-check a few files to confirm paths like `.dev-flow/` were NOT replaced.

### Step 6: Fix any remaining `.dev-flow` path references (expect ~0 changes)

- [ ] **Step 6: Verify `.dev-flow/` path references are intact**

```bash
# These should return results — they should NOT be changed
grep -r '\.dev-flow/' --include="*.md" --include="*.py" --include="*.json" . | head -20
grep -r 'dev-flow/' --include="*.md" --include="*.py" . | head -20
```

If any `.dev-flow/` paths were accidentally replaced, restore them:
```bash
# Restore any accidentally changed .dev-flow/ paths
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's#\.devloop/#\.dev-flow/#g' {} +
find . -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -exec perl -pi -e 's#devloop/phases/#dev-flow/phases/#g' {} +
```

### Step 7: Fix frontmatter name fields

- [ ] **Step 7: Ensure all frontmatter `name:` fields say `devloop`**

After the bulk replacements, some frontmatter `name:` fields may have become `devloop` already. Verify a sample:
```bash
grep -r '^name: devloop' --include="*.md" . | wc -l
grep -r '^name: ' --include="*.md" . | grep -v 'devloop' | grep -v 'phase\|agent\|skill\|reference\|hook\|gate\|template' | head -10
```

Manually fix any remaining `name: devloop` in frontmatter (unlikely after Step 5c but check).

### Step 8: Fix README.md specifically

- [ ] **Step 8: Update README.md title and install command**

Read `README.md`, then:
- Title: `# devloop` → `# devloop`
- Install line: `github.com/thanksmors/devloop` stays as-is (repo URL)
- CLI invocations: `/devloop` → `/devloop`
- All occurrences of `devloop` → `devloop`

### Step 9: Fix PRINCIPLES.md and PATTERNS.md

- [ ] **Step 9: Update PRINCIPLES.md and PATTERNS.md**

- PRINCIPLES.md: Title `# devloop` → `# devloop`
- PATTERNS.md: "devloop" in prose → "devloop"

### Step 10: Commit rebrand

- [ ] **Step 10: Commit the rebrand changes**

```bash
git add -A
git status  # review all changed files before committing
git commit -m "chore(rebrand): rename devloop → devloop

- Rename commands/devloop.md → commands/devloop.md
- Update plugin.json, marketplace.json, hooks.json names
- Replace all devloop/devloop text references with devloop
- Keep .dev-flow/ directory paths unchanged (runtime per-project)
- Keep GitHub repo URL unchanged

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Context7 Injection — Phase 6 §6.3 workspace.dsl

- [ ] **Step 1: Read current Phase 6 §6.3**

Read `.claude-plugin/phases/06-implementation.md`, locate Section 6.3 "C4 Workspace Sync".

### Step 2: Add Context7 instruction to §6.3 header

- [ ] **Step 2: Add Context7 instruction block to §6.3**

Find the line:
```
## 6.3 C4 Workspace Sync
```

Add this block **immediately after** the section heading line:

```
> **ALWAYS consult Context7 before writing or modifying `docs/workspace.dsl`.**
> Use `mcp__plugin_context7_context7__resolve-library-id` with query `"structurizrdsl"` or `"structurizr python"`, then `mcp__plugin_context7_context7__query-docs` for the specific syntax needed (component, relationship, view, etc.).
> Common needs: adding a component, changing a relationship label, creating a view, using `contains()`, `uses()`, `internal()`.
> Do NOT write DSL from memory. Verify every DSL block against current Structurizr documentation.
```

### Step 3: Verify the change looks correct

- [ ] **Step 3: Verify §6.3 now shows the Context7 block**

Read the section around line 391-420 to confirm the block was inserted correctly.

### Step 4: Commit

- [ ] **Step 4: Commit Context7 §6.3 injection**

```bash
git add .claude-plugin/phases/06-implementation.md
git commit -m "docs(phase6): add Context7 instruction for workspace.dsl updates

Consult Context7 before writing or modifying docs/workspace.dsl in
Section 6.3 C4 Workspace Sync.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Context7 Injection — Phase 7 §7.1 workspace.dsl

- [ ] **Step 1: Read current Phase 7 §7.1 architecture gaps section**

Read `.claude-plugin/phases/07-gap-analysis.md`, locate the "Architecture Gaps" bullet in Step 7.1.

### Step 2: Add Context7 instruction to §7.1 Architecture Gaps

- [ ] **Step 2: Add Context7 instruction block to §7.1 Architecture Gaps**

Find the lines:
```
**Architecture Gaps**
- Do the actual components match the C4 diagrams?
```

Add this as a **preamble paragraph** before the bullet list:

```
> **ALWAYS consult Context7 when updating `docs/workspace.dsl`.**
> If the gap analysis reveals that workspace.dsl is out of sync with the code, update workspace.dsl using the same Context7 workflow as Phase 6 Section 6.3 — resolve library ID for structurizrdsl, query specific syntax needed.
```

### Step 3: Verify the change

- [ ] **Step 3: Verify §7.1 shows the Context7 block**

Read the section around lines 56-62 to confirm.

### Step 4: Commit

- [ ] **Step 4: Commit Context7 §7.1 injection**

```bash
git add .claude-plugin/phases/07-gap-analysis.md
git commit -m "docs(phase7): add Context7 instruction for workspace.dsl gap fixes

Reference the same Context7 workflow from Phase 6 Section 6.3 when
updating workspace.dsl during gap analysis.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Context7 Injection — Phase 6 §6.8 Debug Escalation

- [ ] **Step 1: Read Phase 6 §6.8 debug escalation header**

Read `.claude-plugin/phases/06-implementation.md`, locate the section around "### 6.8 — Phase 6 Adjustment Gate" or the Debugging Escalation section (Section 6.8 in the original numbering, which is the "Round 1 — 3 Hypothesis Agents" section).

### Step 2: Add Context7 instruction before hypothesis agents

- [ ] **Step 2: Add Context7 instruction at top of debug escalation**

Locate the line:
```
### Round 1 — 3 Hypothesis Agents
```

Add this block **immediately before** that heading (as a new preamble to the entire Debugging Escalation section):

```
> **ALWAYS consult Context7 when an error is unexpected or unexplained.**
> Before running hypothesis agents or attempting any fix, use `mcp__plugin_context7_context7__query-docs` with the relevant library/framework and error keywords.
> Examples:
> - Nuxt error → query `"nuxt 3"` with the error message
> - Prisma error → query `"prisma"` with the error message
> - TypeScript error → query `"typescript"` with the error message
> - Bun/Node error → query `"bun"` or `"node.js"` with the error message
> If Context7 returns relevant documentation, incorporate the findings before dispatching hypothesis agents.
```

### Step 3: Verify the change

- [ ] **Step 3: Verify the Context7 block was inserted before Round 1**

Read the section around lines 242-260 to confirm the block is present.

### Step 4: Commit

- [ ] **Step 4: Commit Context7 debug injection**

```bash
git add .claude-plugin/phases/06-implementation.md
git commit -m "docs(phase6): add Context7 consultation to debug escalation

Before hypothesis agents investigate unexpected errors, always
consult Context7 for the relevant library/framework first.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Update Skill References

After the rebrand (Task 1), the skill references `@dev:verification-before-completion` in the phase files will already have been replaced to `@devloop:verification-before-completion` by the bulk replacement in Step 5c. Verify this happened correctly.

- [ ] **Step 1: Verify skill references were updated by rebrand**

```bash
grep -r "@dev:" --include="*.md" .
grep -r "@devloop:" --include="*.md" . | grep verification
```

If any `@dev:verification-before-completion` remains, replace it manually:
```bash
# Manual fix if needed
perl -pi -e 's/@dev:verification-before-completion/@devloop:verification-before-completion/g' \
  .claude-plugin/phases/06-extras.md \
  .claude-plugin/phases/06-implementation.md
```

- [ ] **Step 2: Commit skill reference fix if changes exist**

```bash
git diff --stat .claude-plugin/phases/06-extras.md .claude-plugin/phases/06-implementation.md
git add .claude-plugin/phases/06-extras.md .claude-plugin/phases/06-implementation.md
git commit -m "chore(skills): update skill references from devloop to devloop

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Final Verification

- [ ] **Step 1: Run final verification**

```bash
# 1. No remaining devloop product name references (paths are OK)
echo "=== Remaining devloop product refs ==="
grep -rn 'devloop' --include="*.md" --include="*.json" . \
  | grep -v '\.dev-flow/' \
  | grep -v 'docs/superpowers' \
  | grep -v 'github.com/thanksmors/devloop' \
  | grep -v 'thanksmors/devloop' \
  | grep -v 'plugin install' \
  | head -20

# 2. No remaining devloop (capitalized product name)
echo "=== Remaining devloop refs ==="
grep -rn 'devloop' --include="*.md" --include="*.json" --include="*.py" . \
  | grep -v '\.dev-flow/' \
  | grep -v 'docs/superpowers' \
  | head -10

# 3. Confirm command file was renamed
echo "=== Command file ==="
ls commands/

# 4. Confirm Context7 blocks were added
echo "=== Context7 in Phase 6 ==="
grep -n "Context7" .claude-plugin/phases/06-implementation.md
echo "=== Context7 in Phase 7 ==="
grep -n "Context7" .claude-plugin/phases/07-gap-analysis.md
```

- [ ] **Step 2: Final commit (if any remaining changes)**

```bash
git status
git diff --stat
# If only verification output changes (no actual file changes): done
# If actual files changed: commit them
```

---

## Spec Coverage Checklist

- [ ] Spec §1 (workspace.dsl Phase 6): Task 2 — Context7 block added to §6.3
- [ ] Spec §1 (workspace.dsl Phase 7): Task 3 — Context7 block added to §7.1
- [ ] Spec §2 (Debugging): Task 4 — Context7 block added to §6.8
- [ ] Spec §3 (Skill references): Task 5 — @devloop:verification-before-completion in phase files
- [ ] Rebrand: Task 1 — all ~50 files updated, command renamed, no paths broken
- [ ] No placeholder/TBD items found
- [ ] All commits are atomic and descriptive
