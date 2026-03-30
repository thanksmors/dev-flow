---
name: frontend-animate
description: Add purposeful animations, micro-interactions, and motion effects. Use when UI feels static or transitions feel abrupt.
argument-hint: "<target>"
user-invocable: true
---

# Frontend Animate

Add animations and micro-interactions that enhance usability and create delight.

## MANDATORY PREPARATION

Invoke the **frontend-design skill**:
- Read `skills/frontend-design/SKILL.md`
- Read `skills/frontend-design/reference/motion-design.md`

Also gather: performance constraints, target devices.

## Assess Animation Opportunities

Identify static areas:
- Missing feedback (actions without visual acknowledgment)
- Jarring transitions (instant state changes)
- Unclear relationships (spatial/hierarchical)
- Lack of delight

## Plan Animation Strategy

- **Hero moment**: ONE signature animation
- **Feedback layer**: Which interactions need acknowledgment?
- **Transition layer**: Which state changes need smoothing?
- **Delight layer**: Where can we surprise and delight?

## Implement Animations

### Timing & Easing

| Duration | Use Case |
|----------|----------|
| 100-150ms | Button press, toggle |
| 200-300ms | Hover, menu open |
| 300-500ms | Accordion, modal |

```css
/* Recommended easing */
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
--ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
```

**Exit animations use ~75% of enter duration.**

### Micro-interactions

```css
/* Button hover */
button:hover {
  transform: scale(1.02);
  transition: transform 150ms var(--ease-out-quart);
}

/* Button press */
button:active {
  transform: scale(0.98);
}
```

### Entrance Animations

```css
.card {
  animation: slide-up 400ms var(--ease-out-quart);
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**NEVER**:
- Use bounce or elastic easing
- Animate layout properties (width, height) — use transform only
- Use >500ms for UI feedback
- Animate everything — fatigue is real
- Ignore `prefers-reduced-motion`
