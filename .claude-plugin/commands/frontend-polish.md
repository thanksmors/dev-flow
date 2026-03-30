---
name: frontend-polish
description: Final quality pass — alignment, spacing, consistency, micro-details. Use before shipping or when UI feels "almost done".
argument-hint: "<target>"
user-invocable: true
---

# Frontend Polish

Final quality pass fixing alignment, spacing, consistency, and micro-detail issues.

## MANDATORY PREPARATION

Invoke the **frontend-design skill**:
- Read `skills/frontend-design/SKILL.md`
- Read `skills/frontend-design/reference/` for the 6 design dimensions

## Pre-Polish Assessment

Review completeness:
- Is the feature functionally complete?
- Are there known issues to preserve?
- What's the quality bar?
- What's the ship timeline?

## Polish Systematically

Cover these 13 dimensions:

1. **Visual Alignment & Spacing** — Pixel-perfect alignment, consistent spacing scale, optical alignment
2. **Typography Refinement** — Hierarchy consistency, 45-75 char line length, no widows/orphans
3. **Color & Contrast** — WCAG standards, design tokens, tinted neutrals
4. **Interaction States** — All 8 states: default, hover, focus, active, disabled, loading, error, success
5. **Micro-interactions & Transitions** — 150-300ms, ease-out-quart/quint/expo, 60fps, prefers-reduced-motion
6. **Content & Copy** — Consistent terminology, capitalization, grammar
7. **Icons & Images** — Consistent style, alt text, retina support
8. **Forms & Inputs** — Labels, validation, tab order
9. **Edge Cases** — Loading, empty, error, success states
10. **Responsiveness** — All breakpoints, 44x44px touch targets
11. **Performance** — No layout shift, lazy loading
12. **Code Quality** — No console logs, no commented code, type safety

## Polish Checklist

- [ ] Visual alignment is pixel-perfect
- [ ] Spacing uses design tokens consistently
- [ ] Typography hierarchy is clear
- [ ] All 8 interaction states implemented
- [ ] Transitions are smooth (150-300ms, ease-out)
- [ ] Copy is clear and concise
- [ ] Error/loading/empty states designed
- [ ] Touch targets ≥44x44px
- [ ] WCAG AA contrast on all text
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] No console errors
- [ ] No layout shift on load
- [ ] `prefers-reduced-motion` respected
- [ ] Code is clean

**NEVER**:
- Don't polish incomplete work
- Don't over-polish for imminent shipping
- Don't introduce bugs
- Don't ignore systematic issues
