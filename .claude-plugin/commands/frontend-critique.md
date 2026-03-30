---
name: frontend-critique
description: Deep design review with specific improvement suggestions. Use during Phase 3 (Design) after C4 component diagrams are done.
argument-hint: "<component name or file path>"
user-invocable: true
---

# Frontend Critique

A structured 4-phase design critique workflow.

## MANDATORY PREPARATION

First, invoke the **frontend-design skill**:
- Read `skills/frontend-design/SKILL.md` — especially the AI Slop Test
- Read all 6 reference files in `skills/frontend-design/reference/`

## Phase 1: Design Critique

Evaluate the design across 10 dimensions:

1. **AI Slop Detection** — Would someone say "AI made this"? Check: Inter defaults, centered card grids, gray on colored, glassmorphism, cyan-on-dark, bounce easing
2. **Visual Hierarchy** — Can you identify the most important element when squinting? Is there a clear primary action?
3. **Information Architecture** — Is cognitive load appropriate? Too much visible at once?
4. **Discoverability & Affordance** — Can users figure out what to do without labels?
5. **Composition & Balance** — Is spacing varied or monotonous? Any asymmetry?
6. **Typography as Communication** — Are fonts distinctive? Is hierarchy clear?
7. **Color with Purpose** — Cohesive palette? Tinted neutrals? Accent used sparingly?
8. **States & Edge Cases** — All 8 interactive states designed?
9. **Microcopy & Voice** — Every word earns its place? Plain language?
10. **Motion** — Purposeful transitions? No bounce/elastic?

## Phase 2: Present Findings

### Nielsen's Severity Ratings
- **P0**: Blocking — must fix before shipping
- **P1**: Serious — fix before shipping
- **P2**: Minor — fix before Phase 7
- **P3**: Polish — fix if time

### Anti-Patterns Verdict
Does this trigger the AI Slop Test? Specific violations found?

### Overall Impression
2-3 sentences on what's working and what isn't.

## Phase 3: Ask the User

Ask 2-3 targeted questions:
1. What's the priority direction — simplify or enhance?
2. What's the design intent behind [specific choice]?
3. Are there scope constraints that limit changes?

## Phase 4: Recommended Actions

Summarize specific, actionable fixes referencing the design principles and the 6 reference modules.
