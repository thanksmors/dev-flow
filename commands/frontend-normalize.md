---
name: frontend-normalize
description: Audit and realign UI to match design system standards — spacing, tokens, patterns. Use when consistency issues are found or after design drift.
argument-hint: "<feature (page, route, component...)>"
user-invocable: true
---

# Frontend Normalize

Analyze and redesign a feature to match design system standards.

## MANDATORY PREPARATION

Invoke the **frontend-design skill**:
- Read `skills/frontend-design/SKILL.md`
- Read `skills/frontend-design/reference/` — especially typography, color-and-contrast, spatial-design

## Plan

1. **Discover the design system**: Search for design tokens, component libraries, style guides in the project
2. **Analyze the current feature**: Where does it deviate from design system patterns?
3. **Create a normalization plan**: Specific changes that will align the feature

## Execute

Address all inconsistencies across these dimensions:

- **Typography**: Use design system fonts, sizes, weights. Replace hard-coded values with tokens.
- **Color & Theme**: Apply design system color tokens. Remove one-off colors.
- **Spacing & Layout**: Use spacing tokens. Align with grid systems.
- **Components**: Replace custom implementations with design system equivalents.
- **Motion**: Match animation timing and easing to established patterns.
- **Accessibility**: Verify contrast ratios, focus states, ARIA labels.

## Clean Up

- Consolidate reusable components created during normalization
- Remove orphaned code and styles
- Verify lint, type-check, and tests still pass

**NEVER**:
- Create new one-off components when design system equivalents exist
- Hard-code values that should use design tokens
- Compromise accessibility for visual consistency
