# Motion Design

## Duration: The 100/300/500 Rule

| Duration | Use Case |
|----------|----------|
| 100-150ms | Instant feedback (button press, toggle) |
| 200-300ms | State changes (hover, menu open) |
| 300-500ms | Layout changes (accordion, modal) |
| 500-800ms | Entrance animations (page load) |

**Exit animations are faster than entrances**—use ~75% of enter duration.

## Easing: Pick the Right Curve

**Don't use `ease`.** Instead:

| Curve | Use For | CSS |
|-------|---------|-----|
| **ease-out** | Elements entering | `cubic-bezier(0.16, 1, 0.3, 1)` |
| **ease-in** | Elements leaving | `cubic-bezier(0.7, 0, 0.84, 0)` |
| **ease-in-out** | State toggles | `cubic-bezier(0.65, 0, 0.35, 1)` |

```css
/* Quart out - smooth, refined (recommended default) */
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);

/* Quint out - slightly more dramatic */
--ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
```

**Avoid bounce and elastic curves.** They feel dated and tacky.

## The Only Two Properties You Should Animate

**transform** and **opacity** only—everything else causes layout recalculations.

## Reduced Motion

This is not optional. Vestibular disorders affect ~35% of adults over 40.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Avoid**: Animating everything. Using >500ms for UI feedback. Ignoring `prefers-reduced-motion`.
