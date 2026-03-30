---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics. Use when the user asks to build web components, pages, artifacts, posters, or applications, or when any design skill requires project context."
---

# Frontend Design Skill

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work.

**Required context** — every design skill needs at minimum:
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**CRITICAL**: You cannot infer this context by reading the codebase. Code tells you what was built, not who it's for or what it should feel like. Only the creator can provide this context.

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE?

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
→ *Consult `skills/frontend-design/reference/typography.md` for scales, pairing, and loading strategies.*

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts—Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes

### Color & Theme
→ *Consult `skills/frontend-design/reference/color-and-contrast.md` for OKLCH, palettes, and dark mode.*

Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark)
**DON'T**: Use gray text on colored backgrounds—use a shade of the background color instead
**DON'T**: Use pure black (#000) or pure white (#fff)—always tint
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds

### Layout & Space
→ *Consult `skills/frontend-design/reference/spatial-design.md` for grids, rhythm, and container queries.*

Create visual rhythm through varied spacing—not the same padding everywhere. Embrace asymmetry.

**DO**: Create visual rhythm through varied spacing
**DO**: Use asymmetry and unexpected compositions
**DON'T**: Wrap everything in cards
**DON'T**: Center everything—left-aligned text with asymmetric layouts feels more designed

### Motion
→ *Consult `skills/frontend-design/reference/motion-design.md` for timing, easing, and reduced motion.*

**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DON'T**: Use bounce or elastic easing—they feel dated and tacky

### Interaction
→ *Consult `skills/frontend-design/reference/interaction-design.md` for forms, focus, and loading patterns.*

**DO**: Use progressive disclosure—start simple, reveal sophistication through interaction
**DON'T**: Make every button primary—use ghost buttons, text links, secondary styles

### UX Writing
→ *Consult `skills/frontend-design/reference/ux-writing.md` for labels, errors, and empty states.*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

## Implementation Principles

Match implementation complexity to the aesthetic vision. Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same.
