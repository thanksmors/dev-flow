# Insforge Connection Gate — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Insforge connection gate items to Phase 5b.

**Architecture:** Add three checklist items to the Phase 5b gate in `phases/05b-preimplementation-gate.md`. No code, no scripts.

**Tech Stack:** dev-flow phase files (markdown)

---

## File Map

| File | Change |
|------|--------|
| `dev-flow/.claude-plugin/phases/05b-preimplementation-gate.md` | Add 3 gate items |

---

### Task 1: Add Insforge gate items to Phase 5b

**Files:**
- Modify: `dev-flow/.claude-plugin/phases/05b-preimplementation-gate.md`

- [ ] **Step 1: Read Phase 5b gate file**

```bash
cat dev-flow/.claude-plugin/phases/05b-preimplementation-gate.md
```

Find the existing checklist section (look for `- [ ]` items).

- [ ] **Step 2: Add Insforge gate items**

Add these three items to the gate checklist:

```markdown
- [ ] Insforge connection script exists and is wired in DI composition
- [ ] Base URL configured in .env (INSFORGE_BASE_URL)
- [ ] API key configured in .env (INSFORGE_API_KEY)
```

Add them near the top of the checklist, or as a grouped section:

```markdown
### Insforge Configuration

- [ ] Insforge connection script exists and is wired in DI composition
- [ ] Base URL configured in .env (INSFORGE_BASE_URL)
- [ ] API key configured in .env (INSFORGE_API_KEY)
```

- [ ] **Step 3: Commit**

```bash
git add dev-flow/.claude-plugin/phases/05b-preimplementation-gate.md
git commit -m "feat(dev-flow): add Insforge connection gate to Phase 5b

Insforge connection script, base URL (INSFORGE_BASE_URL), and API key
(INSFORGE_API_KEY) verified at pre-implementation gate.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Self-Review Checklist

1. **Spec coverage:** All 3 gate items added to Phase 5b ✅
2. **Placeholder scan:** No TBD/TODO ✅
3. **Type consistency:** Exact text matches spec ✅
