# Spatial Design

## Spacing Systems

### Use 4pt Base, Not 8pt

8pt systems are too coarse. Use 4pt for granularity: 4, 8, 12, 16, 24, 32, 48, 64, 96px.

### Name Tokens Semantically

Name by relationship (`--space-sm`, `--space-lg`), not value (`--spacing-8`). Use `gap` instead of margins for sibling spacing.

## Grid Systems

### The Self-Adjusting Grid

Use `repeat(auto-fit, minmax(280px, 1fr))` for responsive grids without breakpoints.

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    grid-template-columns: 120px 1fr;
  }
}
```

## Visual Hierarchy

### The Squint Test

Blur your eyes. Can you still identify the most important element? Clear groupings? If everything looks the same weight blurred, you have a hierarchy problem.

### Cards Are Not Required

Cards are overused. Use cards only when content is truly distinct and actionable. **Never nest cards inside cards.**

## Container Queries

Viewport queries are for page layouts. **Container queries are for components**.

## Depth & Elevation

Create semantic z-index scales (dropdown → sticky → modal-backdrop → modal → toast → tooltip) instead of arbitrary numbers.

**Avoid**: Arbitrary spacing values outside your scale. Making all spacing equal. Creating hierarchy through size alone.
