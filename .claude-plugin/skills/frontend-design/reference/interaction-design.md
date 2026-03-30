# Interaction Design

## The Eight Interactive States

Every interactive element needs these states:

| State | Visual Treatment |
|-------|------------------|
| **Default** | Base styling |
| **Hover** | Subtle lift, color shift |
| **Focus** | Visible ring (`:focus-visible`) |
| **Active** | Pressed in, darker |
| **Disabled** | Reduced opacity, no pointer |
| **Loading** | Spinner, skeleton |
| **Error** | Red border, icon, message |
| **Success** | Green check, confirmation |

## Focus Rings: Do Them Right

**Never `outline: none` without replacement.**

```css
button:focus {
  outline: none;
}

button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

## Forms

**Placeholders aren't labels**—always use visible `<label>` elements. Place errors **below** fields.

## Loading States

**Skeleton screens > spinners.** Use optimistic updates for low-stakes actions.

## The Popover API

Use native popovers for tooltips and dropdowns:

```html
<button popovertarget="menu">Open menu</button>
<div id="menu" popover>
  <button>Option 1</button>
</div>
```

## Anti-Patterns

- `position: absolute` inside `overflow: hidden` — dropdown will be clipped
- Arbitrary `z-index: 9999` — use semantic z-index scale

**Avoid**: Removing focus indicators without alternatives. Using placeholder text as labels. Touch targets <44x44px.
