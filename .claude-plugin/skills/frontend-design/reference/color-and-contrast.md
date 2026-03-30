# Color & Contrast

## Color Spaces: Use OKLCH

**Stop using HSL.** Use OKLCH (or LCH) instead. It's perceptually uniform.

```css
/* OKLCH: lightness (0-100%), chroma (0-0.4+), hue (0-360) */
--color-primary: oklch(60% 0.15 250);
```

**Key insight**: As you move toward white or black, reduce chroma (saturation).

### The Tinted Neutral Trap

**Pure gray is dead.** Add a subtle hint of your brand hue to all neutrals:

```css
/* Warm-tinted grays (add brand warmth) */
--gray-100: oklch(95% 0.01 60);
--gray-900: oklch(15% 0.01 60);
```

The chroma is tiny (0.01) but perceptible.

### Palette Structure

| Role | Purpose |
|------|---------|
| **Primary** | Brand, CTAs, key actions |
| **Neutral** | Text, backgrounds, borders |
| **Semantic** | Success, error, warning, info |
| **Surface** | Cards, modals, overlays |

### The 60-30-10 Rule

- **60%**: Neutral backgrounds, white space
- **30%**: Secondary colors
- **10%**: Accent—CTAs, highlights, focus states

## Contrast & Accessibility

### WCAG Requirements

| Content Type | AA Minimum | AAA Target |
|--------------|------------|------------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | 4.5:1 |

### Dangerous Color Combinations

- Light gray text on white
- **Gray text on any colored background**—use a darker shade of the background color
- Red text on green background
- Blue text on red background
- Yellow text on white

### Never Use Pure Gray or Pure Black

Pure gray and pure black don't exist in nature. Even a chroma of 0.005-0.01 is enough to feel natural.

## Theming: Light & Dark Mode

### Dark Mode Is Not Inverted Light Mode

```css
:root[data-theme="dark"] {
  --surface-1: oklch(15% 0.01 250);
  --surface-2: oklch(20% 0.01 250);
  --surface-3: oklch(25% 0.01 250);
  --body-weight: 350;
}
```

**Avoid**: Relying on color alone to convey information. Creating palettes without clear roles for each color.
