---
name: subagent-delegation
description: Maps which devloop steps should be delegated to subagents to preserve the orchestrator's context window
---

# Subagent Delegation Guide

## The Principle

The orchestrator stays thin — coordinate, read summaries, make decisions. Delegate everything else.

The orchestrator's context window is the bottleneck. Subagents give you fresh, focused context. The rule: if a step involves reading more than 2-3 files or reasoning about complex logic, delegate it. The orchestrator reads summaries, not source code.

## Delegation Map

| Phase | What to delegate | Agent type | Why |
|-------|-----------------|------------|-----|
| **1 Discovery** | Research existing solutions, explore similar features | Explore agent | Reading external docs/benchmarks is expensive context |
| **2 Exploration** | Architecture analysis, convention extraction, integration mapping | 3 parallel Explore agents | Fresh context per focus area |
| **3 Design** | C4 diagram drafting, walking skeleton scaffolding | Explore + general-purpose | Keeps orchestrator focused on architecture decisions |
| **4 Pre-Mortem** | Risk analysis per subsystem, failure mode identification | Explore agents (parallel per subsystem) | Each subsystem gets dedicated analysis |
| **5 Planning** | Task decomposition for complex features | general-purpose | Fresh context for breaking down complex work |
| **6 Implementation** | Code implementation, spec review, quality review | Implementer, spec-reviewer, quality-reviewer agents | Fresh context per task |
| **6 Debugging** | Hypothesis investigation (3→5→10), fix implementation, post-fix verification | Explore agents (investigation), Implementer (fix), spec/quality reviewers (verification) | Isolated investigation, focused fixes |
| **7 Gap Analysis** | Coverage analysis, test gap identification, docs audit | Explore + general-purpose | Fresh eyes find gaps better |
| **8 Completion** | Final compliance audit, integration readiness check | code-reviewer agent | Independent final check |

## Within Debugging Escalation (Phase 6)

| Step | Who does it | Context needed |
|------|------------|----------------|
| Create debug.md with error context | Orchestrator | Error message + task spec |
| Dispatch hypothesis agents | Orchestrator | Error context + prior round reports |
| Investigate hypothesis (read-only) | Subagent (Explore type) | Error + hypothesis + relevant files |
| Compile reports into debug.md | Orchestrator | Agent summaries only |
| Pick best fix path | Orchestrator | Report summaries |
| Implement fix attempt | Subagent (Implementer type) | Investigation reports + task spec + code context |
| Verify fix | Subagent (spec/quality reviewers) | Task spec + changed files |

## Decision Framework

**Delegate when:**
- Reading more than 2-3 files
- Reasoning about complex logic across modules
- Any investigation or research task
- Implementation of code changes
- Quality review or spec compliance checking

**Do NOT delegate when:**
- Making a decision between options (coordinator picks the path)
- Reading agent summaries (keep these in orchestrator context)
- Updating state files (orchestrator owns state)
- Presenting checkpoints to the user
