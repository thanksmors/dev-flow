---
name: frontend-audit
description: Audit rendered frontend output for AI slop patterns — generic aesthetics, default fonts, centered card grids, glassmorphism, bounce easing. Use before Phase 3 design review or Phase 6 UI task completion.
argument-hint: "<URL or description of what to audit>"
user-invocable: true
---

# Frontend Audit

Run a systematic technical quality audit across 5 dimensions.

## MANDATORY PREPARATION

First, invoke the **frontend-design skill** for design principles and anti-patterns:
- Read `skills/frontend-design/SKILL.md` for the AI Slop Test
- Read `skills/frontend-design/reference/` for the 6 design dimensions

## Diagnostic Scan

Check for issues in each dimension:

### Accessibility (A11y)
- Run WCAG contrast checks on all text/background combinations
- Verify touch targets are 44x44px minimum
- Check focus indicators are visible on all interactive elements
- Verify all images have alt text

### Performance
- Check for layout shift (CLS) issues
- Verify fonts load with `font-display: swap`
- Look for unoptimized images (no width/height set)

### Theming
- Check for hard-coded colors (should use design tokens)
- Verify neutrals are tinted (not pure gray)
- Check for pure black (#000) or pure white (#fff)

### Responsive Design
- Verify container queries are used for components
- Check breakpoints are intentional

### AI Slop Detection
Check for these tells:
- Inter/Roboto/system font defaults
- Centered card grids with icon + heading + text
- Gray text on colored backgrounds
- Glassmorphism used decoratively
- Pure black/white
- Bounce or elastic easing
- Cyan-on-dark with neon accents
- Gradient text on headings
- Sparklines as decoration
- Every button is primary colored

## Generate Report

Score each dimension 0-4:

| Dimension | Score | Key Issues |
|-----------|-------|------------|
| Accessibility | /4 | |
| Performance | /4 | |
| Theming | /4 | |
| Responsive | /4 | |
| Anti-Patterns | /4 | |

Total: /20

## Recommended Actions

For each P0-P2 issue found, recommend one of:
- `/frontend-normalize` — for consistency/token issues
- `/frontend-polish` — for visual polish issues
- `/frontend-animate` — for motion issues
- `/frontend-distill` — for copy issues
- `/frontend-critique` — for design direction issues
