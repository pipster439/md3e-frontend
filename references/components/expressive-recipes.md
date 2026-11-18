# Expressive Component Recipes (HTML / CSS / JS)

These recipes implement the **Expressive components introduced in Material 3 Expressive (May 2025+)** that are not provided by `@material/web` (which is in maintenance mode).

Every recipe uses pure semantic HTML, MD3E CSS tokens (`--md-sys-*`), and spring motion. They work out of the box with zero dependencies and can be used alongside `@material/web` or in any framework (React, Vue, Svelte, Vanilla).

---

## 1. Toolbars (Docked & Floating)

> [!IMPORTANT]
> The bottom app bar is **deprecated** in M3E. Use a **Docked Toolbar** for fixed edge placement or a **Floating Toolbar** when actions need flexible placement or elevation. All toolbars default to **64dp height**.

### 1.1 Floating Toolbar (Standard & Vibrant)

A pill-shaped toolbar elevated above content. Use `role="toolbar"` for action groups (and `nav` only for site navigation). Whenever a fixed Floating Toolbar is active on a scrolling view, add `padding-block-end: 112px` (or equivalent bottom scroll clearance) on the main pane so lower cards and controls are never occluded at max scroll.

```html
<div class="md3e-toolbar-floating" role="toolbar" aria-label="Canvas actions">
  <button type="button" class="md3e-toolbar-btn" aria-label="Draw" aria-pressed="true">
    <span class="material-symbols-outlined" aria-hidden="true">brush</span>
  </button>
  <button type="button" class="md3e-toolbar-btn" aria-label="Erase" aria-pressed="false">
    <span class="material-symbols-outlined" aria-hidden="true">ink_eraser</span>
  </button>
  <div class="md3e-toolbar-divider" role="separator" aria-orientation="vertical"></div>
  <button type="button" class="md3e-toolbar-btn" aria-label="Undo">
    <span class="material-symbols-outlined" aria-hidden="true">undo</span>
  </button>
  <button type="button" class="md3e-toolbar-btn" aria-label="Redo">
    <span class="material-symbols-outlined" aria-hidden="true">redo</span>
  </button>
  <div class="md3e-toolbar-divider" role="separator" aria-orientation="vertical"></div>
  <button type="button" class="md3e-toolbar-btn md3e-toolbar-btn--primary" aria-label="Share">
    <span class="material-symbols-outlined" aria-hidden="true">share</span>
  </button>
</div>
```

```css
.md3e-toolbar-floating {
  position: fixed;
  inset-block-end: var(--md-sys-spacing-6);
  inset-inline-start: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: var(--md-sys-spacing-1);
  height: 64px;
  max-width: calc(100vw - var(--md-sys-spacing-8));
  padding-inline: var(--md-sys-spacing-2);
  background: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-full);
  box-shadow: var(--md-sys-elevation-level3);
  z-index: 100;
  transition: transform var(--md-sys-motion-default-spatial);
}

/* Vibrant toolbar variant (M3E) */
.md3e-toolbar-floating--vibrant {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
}

.md3e-toolbar-btn {
  position: relative;
  display: grid;
  place-items: center;
  min-width: var(--md-sys-touch-target-min); /* 48px hit target */
  min-height: var(--md-sys-touch-target-min);
  padding: 0;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  border-radius: var(--md-sys-shape-corner-full);
  cursor: pointer;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-toolbar-floating--vibrant .md3e-toolbar-btn {
  color: var(--md-sys-color-on-primary-container);
}

.md3e-toolbar-btn[aria-pressed="true"] {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

.md3e-toolbar-btn:hover {
  background: color-mix(in srgb, currentColor calc(var(--md-sys-state-hover-state-layer-opacity) * 100%), transparent);
  color: var(--md-sys-color-on-surface);
}

.md3e-toolbar-btn[aria-pressed="true"]:hover {
  background: color-mix(
    in srgb,
    var(--md-sys-color-on-secondary-container) calc(var(--md-sys-state-hover-state-layer-opacity) * 100%),
    var(--md-sys-color-secondary-container)
  );
  color: var(--md-sys-color-on-secondary-container);
}

.md3e-toolbar-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-toolbar-btn--primary {
  color: var(--md-sys-color-primary);
}

.md3e-toolbar-divider {
  width: 1px;
  height: 24px;
  background: var(--md-sys-color-outline-variant);
  margin-inline: var(--md-sys-spacing-1);
}
```

### 1.2 Docked Toolbar

Fixed to screen bottom (e.g. mobile viewport footer) with surface-container styling:

```css
.md3e-toolbar-docked {
  position: fixed;
  inset-block-end: 0;
  inset-inline: 0;
  height: 64px;
  padding-inline: var(--md-sys-spacing-4);
  background: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--md-sys-color-outline-variant);
  z-index: 100;
}
```

### 1.3 Bidirectional Floating ↔ Docked Morphing Toolbar

Combines `assets/tokens/md3e-blur.css` (`.md3e-blur-surface`) with a spatial state transition so a compact centered floating toolbar morphs smoothly into a full-width docked workspace bar when pinned (`data-toolbar-mode="floating" | "docked"`). Use `document.startViewTransition()` when available so width, corner radius (`32px -> 0px`), and action distribution glide on the compositor without blocking interactions on desktop workspaces:

```html
<div
  class="md3e-toolbar-adaptive md3e-blur-surface"
  id="adaptive-toolbar"
  role="toolbar"
  aria-label="Workspace actions"
  data-toolbar-mode="floating"
>
  <button type="button" class="md3e-toolbar-btn" aria-label="Select tool" aria-pressed="true">
    <span class="material-symbols-outlined" aria-hidden="true">arrow_selector_tool</span>
  </button>
  <button type="button" class="md3e-toolbar-btn" aria-label="Annotate" aria-pressed="false">
    <span class="material-symbols-outlined" aria-hidden="true">draw</span>
  </button>
  <div class="md3e-toolbar-divider" role="separator" aria-orientation="vertical"></div>
  <button
    type="button"
    class="md3e-toolbar-btn md3e-toolbar-btn--primary"
    id="toolbar-dock-toggle"
    aria-label="Dock toolbar to edge"
    aria-pressed="false"
  >
    <span class="material-symbols-outlined" aria-hidden="true">dock_to_bottom</span>
  </button>
</div>
```

```css
.md3e-toolbar-adaptive {
  view-transition-name: md3e-adaptive-toolbar;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--md-sys-spacing-1);
  height: 64px;
  padding-inline: var(--md-sys-spacing-3);
  border-radius: var(--md-sys-shape-corner-extra-large-increased); /* 32px pill */
  box-shadow: var(--md-sys-elevation-level3);
  transition:
    border-radius var(--md-sys-motion-default-spatial),
    transform var(--md-sys-motion-default-spatial),
    background-color var(--md-sys-motion-fast-effects);
}

.md3e-toolbar-adaptive[data-toolbar-mode="floating"] {
  inline-size: fit-content;
  margin-inline: auto;
}

.md3e-toolbar-adaptive[data-toolbar-mode="docked"] {
  inline-size: 100%;
  justify-content: space-between;
  padding-inline: var(--md-sys-spacing-6);
  border-radius: var(--md-sys-shape-corner-none); /* 0px full edge dock */
  box-shadow: var(--md-sys-elevation-level0);
}

::view-transition-group(md3e-adaptive-toolbar) {
  animation-duration: var(--md-sys-motion-default-spatial-duration);
  animation-timing-function: var(--md-sys-motion-default-spatial-easing);
}

@media (prefers-reduced-motion: reduce) {
  .md3e-toolbar-adaptive {
    transition: none;
  }
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

```javascript
export function bindBidirectionalToolbar(toolbarEl, toggleBtn) {
  const apply = () => {
    const docked = toolbarEl.dataset.toolbarMode === 'docked';
    const next = docked ? 'floating' : 'docked';
    toolbarEl.dataset.toolbarMode = next;
    toggleBtn.setAttribute('aria-pressed', String(next === 'docked'));
    toggleBtn.setAttribute('aria-label', next === 'docked' ? 'Undock floating toolbar' : 'Dock toolbar to edge');
  };
  toggleBtn.addEventListener('click', () => {
    if (typeof document.startViewTransition === 'function'
      && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.startViewTransition(apply).ready.catch(() => {});
    } else {
      apply();
    }
  });
}
```

---

## 2. Split Button

A two-button control separated by an explicit **2dp gap**: leading action button on the start side, trailing menu trigger on the end side. Outer corners stay pill-shaped (`20px` on 40dp S size), inner corners start at `4px`, morph to `8px` on hover/press, and the trailing trigger morphs into a full circle (`20px`) with a 180° rotated chevron when `aria-expanded="true"`.

```html
<div class="md3e-split-btn md3e-split-btn--filled">
  <button class="md3e-split-btn__action" type="button">
    <span class="material-symbols-outlined" aria-hidden="true">send</span>
    <span>Publish</span>
  </button>
  <button
    class="md3e-split-btn__arrow"
    type="button"
    aria-label="More publishing options"
    aria-haspopup="menu"
    aria-expanded="false"
  >
    <span class="material-symbols-outlined md3e-split-btn__chevron" aria-hidden="true">keyboard_arrow_down</span>
  </button>
</div>
```

```css
.md3e-split-btn {
  display: inline-flex;
  align-items: center;
  gap: 2px; /* Official M3E 2dp between-space */
}

.md3e-split-btn__action,
.md3e-split-btn__arrow {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  border: none;
  cursor: pointer;
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  --md-sys-icon-size: 20px;
  --md-sys-icon-opsz: 20;
  transition: border-radius var(--md-sys-motion-fast-spatial),
              transform var(--md-sys-motion-fast-spatial),
              background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

/* Preserve 48px touch target without inflating 40px visual container */
.md3e-split-btn__action::before,
.md3e-split-btn__arrow::before {
  content: "";
  position: absolute;
  inset-block: -4px;
  inset-inline: -2px;
  min-width: var(--md-sys-touch-target-min);
  min-height: var(--md-sys-touch-target-min);
}

/* State-layer overlay */
.md3e-split-btn__action::after,
.md3e-split-btn__arrow::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: currentColor;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects);
}

.md3e-split-btn__action {
  gap: var(--md-sys-spacing-2);
  padding-inline-start: var(--md-sys-spacing-4);
  padding-inline-end: var(--md-sys-spacing-3);
  border-start-start-radius: var(--md-sys-shape-corner-large-increased); /* 20px */
  border-end-start-radius: var(--md-sys-shape-corner-large-increased);
  border-start-end-radius: var(--md-sys-shape-corner-extra-small); /* 4px */
  border-end-end-radius: var(--md-sys-shape-corner-extra-small);
}

.md3e-split-btn__arrow {
  width: 44px;
  padding: 0;
  border-start-start-radius: var(--md-sys-shape-corner-extra-small); /* 4px */
  border-end-start-radius: var(--md-sys-shape-corner-extra-small);
  border-start-end-radius: var(--md-sys-shape-corner-large-increased); /* 20px */
  border-end-end-radius: var(--md-sys-shape-corner-large-increased);
}

/* Variants */
.md3e-split-btn--filled .md3e-split-btn__action,
.md3e-split-btn--filled .md3e-split-btn__arrow {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}

.md3e-split-btn--tonal .md3e-split-btn__action,
.md3e-split-btn--tonal .md3e-split-btn__arrow {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

.md3e-split-btn--outlined .md3e-split-btn__action,
.md3e-split-btn--outlined .md3e-split-btn__arrow {
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  box-shadow: inset 0 0 0 1px var(--md-sys-color-outline-variant);
}

/* Hover / Focus / Active / Expanded morphs */
.md3e-split-btn__action:hover::after,
.md3e-split-btn__arrow:hover::after {
  opacity: var(--md-sys-state-hover-state-layer-opacity);
}

.md3e-split-btn__action:focus-visible::after,
.md3e-split-btn__arrow:focus-visible::after {
  opacity: var(--md-sys-state-focus-state-layer-opacity);
}

.md3e-split-btn__action:active::after,
.md3e-split-btn__arrow:active::after {
  opacity: var(--md-sys-state-pressed-state-layer-opacity);
}

.md3e-split-btn__action:is(:hover, :active) {
  border-start-end-radius: var(--md-sys-shape-corner-small); /* 8px */
  border-end-end-radius: var(--md-sys-shape-corner-small);
}

.md3e-split-btn__arrow:is(:hover, :active) {
  border-start-start-radius: var(--md-sys-shape-corner-small); /* 8px */
  border-end-start-radius: var(--md-sys-shape-corner-small);
}

.md3e-split-btn__arrow[aria-expanded="true"] {
  border-radius: var(--md-sys-shape-corner-large-increased); /* 20px full circle */
}

.md3e-split-btn__chevron {
  transition: transform var(--md-sys-motion-fast-spatial);
}

.md3e-split-btn__arrow[aria-expanded="true"] .md3e-split-btn__chevron {
  transform: rotate(180deg);
}

.md3e-split-btn__action:focus-visible,
.md3e-split-btn__arrow:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  z-index: 1;
}

.md3e-split-btn__action:disabled,
.md3e-split-btn__arrow:disabled {
  opacity: var(--md-sys-state-disabled-content-opacity);
  cursor: default;
  pointer-events: none;
}
```

---

## 3. Button Groups (Connected & Standard)

### 3.1 Connected Button Group (Superseding Segmented Button)

Connected button groups place individual buttons side by side with a **2dp gap**, outer pill corners (`20px`), inner corners (`8px` at S size, morphing to `4px` on press), and morph the **selected item** to full pill (`20px`) without shifting neighbours.

```html
<div class="md3e-btn-group" role="group" aria-label="Text alignment">
  <button type="button" class="md3e-group-btn" aria-label="Align left" aria-pressed="true">
    <span class="material-symbols-outlined" aria-hidden="true">format_align_left</span>
  </button>
  <button type="button" class="md3e-group-btn" aria-label="Align center" aria-pressed="false">
    <span class="material-symbols-outlined" aria-hidden="true">format_align_center</span>
  </button>
  <button type="button" class="md3e-group-btn" aria-label="Align right" aria-pressed="false">
    <span class="material-symbols-outlined" aria-hidden="true">format_align_right</span>
  </button>
</div>
```

```css
.md3e-btn-group {
  display: inline-flex;
  align-items: center;
  gap: 2px; /* Official M3E 2dp padding for all connected groups */
}

.md3e-group-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--md-sys-spacing-2);
  height: 40px;
  min-width: 48px;
  padding-inline: var(--md-sys-spacing-3);
  border: none;
  border-radius: var(--md-sys-shape-corner-small); /* 8px inner corner at S */
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  font-weight: var(--md-sys-typescale-label-large-weight);
  --md-sys-icon-size: 20px;
  --md-sys-icon-opsz: 20;
  cursor: pointer;
  transition: border-radius var(--md-sys-motion-fast-spatial),
              background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-group-btn::before {
  content: "";
  position: absolute;
  inset-block: -4px;
  inset-inline: 0;
  min-height: var(--md-sys-touch-target-min);
}

.md3e-group-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: currentColor;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects);
}

.md3e-group-btn:first-child {
  border-start-start-radius: var(--md-sys-shape-corner-large-increased); /* 20px */
  border-end-start-radius: var(--md-sys-shape-corner-large-increased);
}

.md3e-group-btn:last-child {
  border-start-end-radius: var(--md-sys-shape-corner-large-increased); /* 20px */
  border-end-end-radius: var(--md-sys-shape-corner-large-increased);
}

.md3e-group-btn:active:not(:disabled) {
  border-radius: var(--md-sys-shape-corner-extra-small); /* 4px pressed feedback */
}

.md3e-group-btn[aria-pressed="true"] {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  border-radius: var(--md-sys-shape-corner-large-increased); /* Full pill on selection */
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  --md-sys-icon-fill: 1;
}

.md3e-group-btn:hover::after {
  opacity: var(--md-sys-state-hover-state-layer-opacity);
}

.md3e-group-btn:focus-visible::after {
  opacity: var(--md-sys-state-focus-state-layer-opacity);
}

.md3e-group-btn:active::after {
  opacity: var(--md-sys-state-pressed-state-layer-opacity);
}

.md3e-group-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  z-index: 1;
}
```

### 3.2 Standard Button Group

Standard button groups use explicit inter-button gaps by size (`18px` XS, `12px` S, `8px` M/L/XL) so buttons maintain `>= 48px` accessible separation and morph width/shape dynamically on press/selection.

```css
.md3e-btn-group-standard {
  display: inline-flex;
  align-items: center;
  gap: var(--md-sys-spacing-3); /* 12px for Small (40dp); use 8px for Medium+ */
}
```

### 3.3 Tactile Neighbor Width Squeeze (`animateWidth`)

In AndroidX Compose M3E (`ButtonGroupDefaults.animateWidth`), pressing or toggling an item expands its width while its **immediate adjacent neighbours compress proportionally**, keeping total group width stable so surrounding UI never jumps:

```css
.md3e-btn-group--squeeze {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  inline-size: min(100%, 320px);
}

.md3e-squeeze-item {
  position: relative;
  flex: 1 1 0;
  min-inline-size: 48px;
  height: 40px;
  border: none;
  border-radius: var(--md-sys-shape-corner-small);
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface-variant);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  cursor: pointer;
  transition:
    flex-grow var(--md-sys-motion-fast-spatial),
    border-radius var(--md-sys-motion-fast-spatial),
    background-color var(--md-sys-motion-fast-effects),
    color var(--md-sys-motion-fast-effects);
}

.md3e-squeeze-item::before {
  content: "";
  position: absolute;
  inset-block: -4px;
  inset-inline: 0;
  min-height: var(--md-sys-touch-target-min);
}

.md3e-squeeze-item:first-child {
  border-start-start-radius: var(--md-sys-shape-corner-large-increased);
  border-end-start-radius: var(--md-sys-shape-corner-large-increased);
}

.md3e-squeeze-item:last-child {
  border-start-end-radius: var(--md-sys-shape-corner-large-increased);
  border-end-end-radius: var(--md-sys-shape-corner-large-increased);
}

.md3e-squeeze-item:is(:active, [aria-pressed="true"]) {
  flex-grow: 1.45;
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  border-radius: var(--md-sys-shape-corner-large-increased);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
}

/* Compress adjacent left & right neighbours smoothly so outer group width stays constant */
.md3e-squeeze-item:has(+ .md3e-squeeze-item:is(:active, [aria-pressed="true"])),
.md3e-squeeze-item:is(:active, [aria-pressed="true"]) + .md3e-squeeze-item {
  flex-grow: 0.78;
}

.md3e-squeeze-item:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  z-index: 1;
}

@media (prefers-reduced-motion: reduce) {
  .md3e-squeeze-item {
    transition: none;
  }
}
```

---

## 4. FAB Menu (Morphing Action Sheet)

A Floating Action Button (`56dp`) that expands into up to 6 Medium-sized (`56dp` high) action pills and morphs into a `56dp` close button. Closed menus **must** carry `inert` so keyboard focus cannot enter invisible buttons, and **must** support `Escape` + scrim dismissal + focus return.

```html
<div class="md3e-fab-menu-container">
  <!-- Backdrop scrim -->
  <div class="md3e-fab-scrim" id="fab-scrim" aria-hidden="true"></div>

  <!-- Main 56dp FAB / Close button trigger (first in DOM/Tab order; column-reverse places it at bottom) -->
  <button
    type="button"
    class="md3e-fab"
    id="fab-trigger"
    aria-label="Open actions menu"
    aria-haspopup="menu"
    aria-expanded="false"
    aria-controls="fab-menu"
  >
    <span class="material-symbols-outlined md3e-fab-icon" aria-hidden="true">add</span>
  </button>

  <!-- Menu items list (inert prevents keyboard focus when closed) -->
  <div class="md3e-fab-menu" id="fab-menu" role="menu" aria-label="Create actions" aria-hidden="true" inert>
    <button type="button" class="md3e-fab-menu-item" role="menuitem">
      <span class="material-symbols-outlined" aria-hidden="true">upload_file</span>
      <span>Upload file</span>
    </button>
    <button type="button" class="md3e-fab-menu-item" role="menuitem">
      <span class="material-symbols-outlined" aria-hidden="true">note_add</span>
      <span>New document</span>
    </button>
  </div>
</div>
```

```css
.md3e-fab-scrim {
  position: fixed;
  inset: 0;
  background: var(--md-sys-color-scrim);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-default-effects);
  z-index: 890;
}

.md3e-fab-scrim.is-open {
  opacity: 0.32;
  pointer-events: auto;
}

.md3e-fab-menu-container {
  position: fixed;
  inset-block-end: var(--md-sys-spacing-4); /* 16dp FAB margin per M3E spec */
  inset-inline-end: var(--md-sys-spacing-4);
  display: flex;
  flex-direction: column-reverse; /* Trigger stays first in DOM/Tab order while rendering at bottom */
  align-items: flex-end;
  gap: var(--md-sys-spacing-1); /* 4dp gap between FAB and menu */
  z-index: 900;
}

.md3e-fab {
  position: relative;
  z-index: 910;
  width: 56px;
  height: 56px;
  border-radius: var(--md-sys-shape-corner-large); /* 16px */
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  border: none;
  cursor: pointer;
  display: grid;
  place-items: center;
  box-shadow: var(--md-sys-elevation-level3);
  transition: transform var(--md-sys-motion-default-spatial),
              border-radius var(--md-sys-motion-default-spatial),
              background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-fab[aria-expanded="true"] {
  border-radius: var(--md-sys-shape-corner-extra-large); /* 28px circle close button */
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}

.md3e-fab-icon {
  --md-sys-icon-size: 24px;
  transition: transform var(--md-sys-motion-default-spatial);
}

.md3e-fab[aria-expanded="true"] .md3e-fab-icon {
  transform: rotate(45deg);
}

.md3e-fab:focus-visible,
.md3e-fab-menu-item:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-fab-menu {
  position: relative;
  z-index: 910;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--md-sys-spacing-1); /* 4dp item spacing per M3E FAB menu spec */
  margin-block-end: var(--md-sys-spacing-1);
  opacity: 0;
  pointer-events: none;
  transform: translateY(12px) scale(0.95);
  transform-origin: bottom right;
  transition: opacity var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-default-spatial);
}

.md3e-fab-menu[aria-hidden="false"] {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

/* Official M3E FAB menu item: 56dp height, 24dp padding, 8dp gap, Title Medium */
.md3e-fab-menu-item {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--md-sys-spacing-2); /* 8dp */
  height: 56px;
  padding-inline: var(--md-sys-spacing-6); /* 24dp */
  border: none;
  border-radius: var(--md-sys-shape-corner-extra-large); /* 28px full pill */
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-title-medium-size);
  line-height: var(--md-sys-typescale-title-medium-line-height);
  font-weight: var(--md-sys-typescale-title-medium-weight);
  box-shadow: var(--md-sys-elevation-level2);
  cursor: pointer;
  transition: transform var(--md-sys-motion-fast-spatial),
              background-color var(--md-sys-motion-fast-effects);
}

.md3e-fab-menu-item::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: currentColor;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects);
}

.md3e-fab-menu-item:hover::after {
  opacity: var(--md-sys-state-hover-state-layer-opacity);
}
```

```javascript
const trigger = document.getElementById('fab-trigger');
const menu = document.getElementById('fab-menu');
const scrim = document.getElementById('fab-scrim');
const menuItems = [...menu.querySelectorAll('[role="menuitem"]')];

function setFabMenuOpen(open, { focusFirst = false, restoreFocus = false } = {}) {
  trigger.setAttribute('aria-expanded', String(open));
  trigger.setAttribute('aria-label', open ? 'Close actions menu' : 'Open actions menu');
  menu.setAttribute('aria-hidden', String(!open));
  menu.inert = !open;
  scrim.classList.toggle('is-open', open);

  if (open && focusFirst && menuItems[0]) {
    menuItems[0].focus();
  } else if (!open && restoreFocus) {
    trigger.focus();
  }
}

trigger.addEventListener('click', (event) => {
  const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
  setFabMenuOpen(!isExpanded, { focusFirst: event.detail === 0 && !isExpanded });
});

scrim.addEventListener('click', () => setFabMenuOpen(false));

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && trigger.getAttribute('aria-expanded') === 'true') {
    event.preventDefault();
    setFabMenuOpen(false, { restoreFocus: true });
  }
});

menu.addEventListener('keydown', (event) => {
  const index = menuItems.indexOf(document.activeElement);
  if (event.key === 'ArrowDown') {
    event.preventDefault();
    menuItems[(index + 1) % menuItems.length]?.focus();
  } else if (event.key === 'ArrowUp') {
    event.preventDefault();
    menuItems[(index - 1 + menuItems.length) % menuItems.length]?.focus();
  } else if (event.key === 'Tab' && index === menuItems.length - 1 && !event.shiftKey) {
    setFabMenuOpen(false);
  }
});

menuItems.forEach((item) => {
  item.addEventListener('click', () => setFabMenuOpen(false, { restoreFocus: true }));
});
```

---

## 5. Expressive Loading Indicator (Official 7-Polygon Morphing Loader)

> [!NOTE]
> In MD3E, the indeterminate circular spinner is replaced for short waits (<5s) by the **Expressive Loading Indicator** (`48dp` box, `38dp` active shape container) morphing sequentially through 7 official `MaterialShapes` polygons (`SoftBurst -> Cookie9Sided -> Pentagon -> Pill -> Sunny -> Cookie4Sided -> Oval`, `650ms` per transition with `spring(damping=0.6, stiffness=200)`, plus `4666ms` linear rotation).

### 5.1 Official 7-Polygon SVG Morphing Loader (`assets/tokens/md3e-shapes.css`)

Include `assets/tokens/md3e-shapes.css`, which precomputes the 36-cubic uniform paths and `--md-comp-loading-indicator-morph-easing`:

```html
<!-- Default 7-polygon morphing Loading Indicator -->
<div class="md3e-loading-indicator" role="status" aria-label="Loading">
  <svg class="md3e-loading-indicator__svg" viewBox="0 0 100 100" aria-hidden="true">
    <path class="md3e-loading-indicator__path" d="M49.96 9.61C52.69 9.6 54.19 12.58 55.63 14.9C57.07 17.22 58.7 20.12 61.42 19.94C64.14 19.75 66.51 18.03 69.05 17.04C71.6 16.04 74.92 17.33 75.4 20.01C75.87 22.7 75.05 25.45 74.95 28.18C74.84 30.9 77.36 32.73 80.02 33.37C82.67 34.02 85.84 33.98 87.6 36.07C89.36 38.15 87.94 41.17 86.18 43.25C84.42 45.34 81.82 47.24 81.81 49.97C81.8 52.7 84.41 54.61 86.18 56.69C87.95 58.77 89.38 61.77 87.63 63.87C85.88 65.96 82.7 65.94 80.05 66.59C77.4 67.24 74.85 69.05 74.96 71.78C75.07 74.5 75.91 77.25 75.45 79.94C74.98 82.63 71.66 83.92 69.11 82.94C66.57 81.96 64.19 80.26 61.47 80.06C58.75 79.86 57.11 82.76 55.68 85.08C54.25 87.4 52.76 90.39 50.04 90.39C47.31 90.4 45.81 87.42 44.37 85.1C42.93 82.78 41.3 79.88 38.58 80.06C35.86 80.25 33.49 81.97 30.95 82.96C28.4 83.96 25.08 82.67 24.6 79.99C24.13 77.3 24.95 74.55 25.05 71.82C25.16 69.1 22.64 67.27 19.98 66.63C17.33 65.98 14.16 66.02 12.4 63.93C10.64 61.85 12.06 58.83 13.82 56.75C15.58 54.66 18.18 52.75 18.19 50.02C18.2 47.3 15.59 45.39 13.82 43.31C12.05 41.23 10.62 38.22 12.37 36.13C14.12 34.04 17.3 34.06 19.95 33.41C22.6 32.76 25.16 30.95 25.04 28.22C24.92 25.5 24.09 22.75 24.55 20.06C25.02 17.37 28.34 16.08 30.89 17.06C33.43 18.04 35.81 19.74 38.53 19.94C41.25 20.14 42.89 17.25 44.32 14.92C45.75 12.6 47.23 9.61 49.96 9.61Z" />
  </svg>
</div>

<!-- Contained Loading Indicator (primary-container circle behind on-primary-container path) -->
<div class="md3e-loading-indicator md3e-loading-indicator--contained" role="status" aria-label="Loading">
  <svg class="md3e-loading-indicator__svg" viewBox="0 0 100 100" aria-hidden="true">
    <path class="md3e-loading-indicator__path" d="M49.96 9.61C52.69 9.6 54.19 12.58 55.63 14.9C57.07 17.22 58.7 20.12 61.42 19.94C64.14 19.75 66.51 18.03 69.05 17.04C71.6 16.04 74.92 17.33 75.4 20.01C75.87 22.7 75.05 25.45 74.95 28.18C74.84 30.9 77.36 32.73 80.02 33.37C82.67 34.02 85.84 33.98 87.6 36.07C89.36 38.15 87.94 41.17 86.18 43.25C84.42 45.34 81.82 47.24 81.81 49.97C81.8 52.7 84.41 54.61 86.18 56.69C87.95 58.77 89.38 61.77 87.63 63.87C85.88 65.96 82.7 65.94 80.05 66.59C77.4 67.24 74.85 69.05 74.96 71.78C75.07 74.5 75.91 77.25 75.45 79.94C74.98 82.63 71.66 83.92 69.11 82.94C66.57 81.96 64.19 80.26 61.47 80.06C58.75 79.86 57.11 82.76 55.68 85.08C54.25 87.4 52.76 90.39 50.04 90.39C47.31 90.4 45.81 87.42 44.37 85.1C42.93 82.78 41.3 79.88 38.58 80.06C35.86 80.25 33.49 81.97 30.95 82.96C28.4 83.96 25.08 82.67 24.6 79.99C24.13 77.3 24.95 74.55 25.05 71.82C25.16 69.1 22.64 67.27 19.98 66.63C17.33 65.98 14.16 66.02 12.4 63.93C10.64 61.85 12.06 58.83 13.82 56.75C15.58 54.66 18.18 52.75 18.19 50.02C18.2 47.3 15.59 45.39 13.82 43.31C12.05 41.23 10.62 38.22 12.37 36.13C14.12 34.04 17.3 34.06 19.95 33.41C22.6 32.76 25.16 30.95 25.04 28.22C24.92 25.5 24.09 22.75 24.55 20.06C25.02 17.37 28.34 16.08 30.89 17.06C33.43 18.04 35.81 19.74 38.53 19.94C41.25 20.14 42.89 17.25 44.32 14.92C45.75 12.6 47.23 9.61 49.96 9.61Z" />
  </svg>
</div>
```

### 5.2 Lightweight Pure-CSS Approximation (when `md3e-shapes.css` is omitted)

When shipping a zero-SVG snippet without `md3e-shapes.css`, keep a single semantic colour and pass the **easing-only** token (`--md-sys-motion-default-spatial-easing`) so CSS `animation` shorthands do not misread `460ms` as an accidental `animation-delay`:

```html
<!-- Lightweight fallback without md3e-shapes.css -->
<div class="md3e-loading-indicator" role="status" aria-label="Loading">
  <div class="md3e-loader-shape"></div>
</div>
```

```css
.md3e-loading-indicator {
  display: inline-grid;
  place-items: center;
  width: 48px;
  height: 48px;
  border-radius: var(--md-sys-shape-corner-full);
}

.md3e-loading-indicator--contained {
  background: var(--md-sys-color-primary-container);
}

.md3e-loader-shape {
  width: 38px; /* Official M3E shape container size inside 48dp box */
  height: 38px;
  background: var(--md-sys-color-primary);
  /* Use -easing token so CSS animation does not interpret 460ms as animation-delay */
  animation: md3e-shape-morph 2.4s var(--md-sys-motion-default-spatial-easing) infinite;
}

.md3e-loading-indicator--contained .md3e-loader-shape {
  background: var(--md-sys-color-on-primary-container);
}

@keyframes md3e-shape-morph {
  0% {
    /* 20px = corner-large-increased (>= 19px half of 38px), avoiding 9999px clamping */
    border-radius: var(--md-sys-shape-corner-large-increased);
    transform: rotate(0deg) scale(1);
  }
  25% {
    border-radius: var(--md-sys-shape-corner-small);
    transform: rotate(90deg) scale(0.86);
  }
  50% {
    border-radius: var(--md-sys-shape-corner-extra-small);
    transform: rotate(180deg) scale(1.02);
  }
  75% {
    border-radius: var(--md-sys-shape-corner-extra-small)
                   var(--md-sys-shape-corner-large-increased)
                   var(--md-sys-shape-corner-extra-small)
                   var(--md-sys-shape-corner-large-increased);
    transform: rotate(270deg) scale(0.92);
  }
  100% {
    border-radius: var(--md-sys-shape-corner-large-increased);
    transform: rotate(360deg) scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .md3e-loader-shape {
    animation: md3e-pulse 1.5s var(--md-sys-motion-easing-linear) infinite;
    border-radius: var(--md-sys-shape-corner-large-increased);
  }
  @keyframes md3e-pulse {
    0%, 100% { opacity: 0.45; }
    50% { opacity: 1; }
  }
}
```

### 5.3 Real-Time JS `Morph` 7-Polygon Cycling Loader (`md3e-morph.js`)

When you want interruptible physics (`stiffness = 200`, `damping = 0.6`), mid-flight retargeting, or custom polygon sequences driven in `requestAnimationFrame` via AndroidX `Morph` control-point subdivision rather than pre-sampled CSS keyframes, drive the SVG `<path>` with `assets/tokens/md3e-morph.js`:

```javascript
import { LOADING_SEQUENCE, createShapeMorpher } from './tokens/md3e-morph.js';

const pathEl = document.getElementById('js-morph-loader-path');
const morpher = createShapeMorpher(pathEl, {
  initialShape: LOADING_SEQUENCE[0],
  scale: 0.84, // rotation-safe inset inside the 38dp container
});

// Cycles SoftBurst -> Cookie9Sided -> Pentagon -> Pill -> Sunny -> Cookie4Sided -> Oval
const stopLoader = morpher.startSequence(LOADING_SEQUENCE, {
  intervalMs: 650,
  stiffness: 200,
  damping: 0.6,
});
```

---

## 6. Toggle Buttons (Shape Morphing & Animation Physics)

Toggle buttons morph resting shapes: **Round when unselected, Square when selected**.

> [!CAUTION]
> **Common Pitfall: Why `9999px` breaks shape morph animations and flashes a `0px` rectangle**:
> In CSS, `var(--md-sys-shape-corner-full)` is `9999px`. When animating `border-radius` between `9999px` and `12px`/`16px`, two bugs happen: (1) visually clamping anything $\ge \text{height}/2$ traps 99.8% of the transition before snapping late, and (2) under an underdamped `linear()` spring with overshoot $> 1.0$ (e.g. `1.07`), CSS evaluates `9999 + 1.07 * (16 - 9999) = -682.8px` and clamps negative values to **`0px`**, flashing a momentary razor-sharp rectangle!
> **The Fix**: Use the bounded half-height pill radius (`var(--md-sys-shape-corner-large-increased)` = `20px` on `40px` buttons, `calc(var(--md-bento-control-height, 48px) / 2)` = `24px` on `48px` controls -> `12px`, `28px` for 56px M, `48px` for 96px L) so overshoot remains positive (`> 0px`) across every frame.

```html
<button
  type="button"
  class="md3e-toggle-btn"
  aria-pressed="false"
  onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed') === 'true' ? 'false' : 'true')"
>
  <span class="material-symbols-outlined" aria-hidden="true">bookmark</span>
  <span>Save bookmark</span>
</button>
```

```css
.md3e-toggle-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--md-sys-spacing-2);
  height: 40px;
  padding-inline: var(--md-sys-spacing-4);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  font-weight: var(--md-sys-typescale-label-large-weight);
  --md-sys-icon-size: 20px;
  --md-sys-icon-opsz: 20;
  cursor: pointer;
  border: none;
  user-select: none;

  /* Filled toggle unselected per M3E spec: surface-container + on-surface-variant */
  background: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface-variant);
  border-radius: var(--md-sys-shape-corner-large-increased); /* 20px exact pill on 40px height */

  transition: border-radius var(--md-sys-motion-default-spatial),
              background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-fast-spatial);
}

/* Touch target hit area (48px) */
.md3e-toggle-btn::before {
  content: "";
  position: absolute;
  inset-block: -4px;
  inset-inline: 0;
  min-height: var(--md-sys-touch-target-min);
  min-width: var(--md-sys-touch-target-min);
}

.md3e-toggle-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: currentColor;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects);
}

.md3e-toggle-btn:hover::after {
  opacity: var(--md-sys-state-hover-state-layer-opacity);
}

.md3e-toggle-btn:focus-visible::after {
  opacity: var(--md-sys-state-focus-state-layer-opacity);
}

.md3e-toggle-btn:active::after {
  opacity: var(--md-sys-state-pressed-state-layer-opacity);
}

.md3e-toggle-btn:active:not(:disabled) {
  transform: scale(0.98);
  border-radius: var(--md-sys-shape-corner-small); /* 8px pressed radius */
}

.md3e-toggle-btn[aria-pressed="true"] {
  /* Filled toggle selected per M3E spec: primary + on-primary, square 12dp */
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: var(--md-sys-shape-corner-medium); /* 12px */
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  --md-sys-icon-fill: 1;
}

.md3e-toggle-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-toggle-btn:disabled {
  opacity: var(--md-sys-state-disabled-content-opacity);
  cursor: default;
  pointer-events: none;
}
```

---

## 7. Search Bar (Integrated Focus & Suppressing Inner Browser Outlines)

> [!CAUTION]
> **Common Pitfall**: Native `<input>` elements render a sharp rectangular user-agent focus outline when focused. When placing an `<input>` inside a pill-shaped container, set `outline: 2px solid transparent;` (never `outline: none;` so Windows High Contrast mode remains visible) and style `:focus-within` on `.md3e-search-bar` with the MD3E focus ring.

```html
<div class="md3e-search-bar" role="search">
  <span class="material-symbols-outlined md3e-search-icon" aria-hidden="true">search</span>
  <input type="text" placeholder="Search..." aria-label="Search content">
  <button type="button" class="md3e-icon-btn" aria-label="Voice search">
    <span class="material-symbols-outlined" aria-hidden="true">mic</span>
  </button>
</div>
```

```css
.md3e-search-bar {
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-3);
  height: 56px;
  padding-inline: var(--md-sys-spacing-4);
  background-color: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-full);
  width: 100%;
  max-width: 480px;
  cursor: text;
  transition: background-color var(--md-sys-motion-fast-effects);
}

.md3e-search-bar:focus-within {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  background-color: var(--md-sys-color-surface-container-highest);
}

.md3e-search-bar input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  padding: 0;
  height: 100%;
  outline: 2px solid transparent;
  box-shadow: none;
}

.md3e-icon-btn {
  position: relative;
  display: grid;
  place-items: center;
  min-width: var(--md-sys-touch-target-min);
  min-height: var(--md-sys-touch-target-min);
  padding: 0;
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  transition: background-color var(--md-sys-motion-fast-effects);
}

.md3e-icon-btn:hover {
  background: color-mix(in srgb, currentColor calc(var(--md-sys-state-hover-state-layer-opacity) * 100%), transparent);
}

.md3e-icon-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}
```

---

## 8. Badges (Small 6dp Dot & Large 16dp Count with Line-Height Isolation)

> [!CAUTION]
> **Line-Height Inheritance Pitfall**:
> Global body `line-height` is typically `24px`–`26px` (especially under CJK `:lang(zh)` adaptation). Because a large badge container is strictly **16dp** high with an `11px` font size, always isolate `line-height: 16px; height: 16px;` on `.md3e-badge`.

```html
<div class="md3e-badge-anchor">
  <button type="button" class="md3e-icon-btn" aria-label="Notifications">
    <span class="material-symbols-outlined" aria-hidden="true">notifications</span>
  </button>
  <span class="md3e-badge md3e-badge--dot" aria-hidden="true"></span>
</div>

<div class="md3e-badge-anchor">
  <button type="button" class="md3e-icon-btn" aria-label="Unread emails: 3">
    <span class="material-symbols-outlined" aria-hidden="true">mail</span>
  </button>
  <span class="md3e-badge">3</span>
</div>

<div class="md3e-badge-anchor">
  <button type="button" class="md3e-icon-btn" aria-label="Messages: 99+">
    <span class="material-symbols-outlined" aria-hidden="true">chat</span>
  </button>
  <span class="md3e-badge">99+</span>
</div>
```

```css
.md3e-badge-anchor {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.md3e-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  box-sizing: border-box;
  min-width: 16px;
  height: 16px;
  padding-inline: 4px;
  border-radius: var(--md-sys-shape-corner-full);
  background-color: var(--md-sys-color-error);
  color: var(--md-sys-color-on-error);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-small-size);
  font-weight: var(--md-sys-typescale-label-small-emphasized-weight);
  line-height: 16px;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  transform: translate(25%, -25%);
  user-select: none;
}

.md3e-badge--dot {
  width: 6px;
  height: 6px;
  min-width: 6px;
  padding: 0;
  top: 8px;
  right: 8px;
  transform: translate(50%, -50%);
}
```

---

## 9. Carousel Component & Native Scrollbar Suppression

```html
<div class="md3e-carousel" role="region" aria-label="Featured showcase">
  <article class="md3e-carousel__item" tabindex="0">
    <h3>Item 1</h3>
  </article>
  <article class="md3e-carousel__item" tabindex="0">
    <h3>Item 2</h3>
  </article>
  <article class="md3e-carousel__item" tabindex="0">
    <h3>Item 3</h3>
  </article>
</div>
```

```css
.md3e-carousel {
  display: flex;
  gap: var(--md-sys-spacing-3);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-block: var(--md-sys-spacing-2);
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.md3e-carousel::-webkit-scrollbar {
  display: none;
}

.md3e-carousel__item {
  scroll-snap-align: start;
  flex-shrink: 0;
  width: 220px;
  height: 160px;
  padding: var(--md-sys-spacing-4);
  border-radius: var(--md-sys-shape-corner-large);
  background-color: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border: 1px solid var(--md-sys-color-outline-variant);
  transition: transform var(--md-sys-motion-fast-spatial);
}

.md3e-carousel__item:hover {
  transform: scale(1.02);
}

.md3e-carousel__item:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}
```

---

## 10. Responsive Navigation Rail & Modal Sheet (GPU-Accelerated Zero-Reflow)

> [!IMPORTANT]
> **Performance Guideline**: Never animate CSS `width` when transitioning between collapsed (`80px` desktop token `--md-sys-nav-rail-width-collapsed` / `96dp` spec diagram) and expanded (`220px` `--md-sys-nav-rail-width-expanded`) navigation states or opening a mobile modal rail. Animating `width` forces document layout reflow every frame. Keep the persistent rail width fixed (or swap at media/attribute breakpoints, defaulting expanded at `Large >= 1200px` on desktop) and animate the modal drawer overlay purely on the compositor with `transform: translateX()`.

```css
/* Medium / Expanded+: Persistent collapsed navigation rail (--md-sys-nav-rail-width-collapsed: 80px; 96px for vertical spec pills) */
.md3e-nav-rail {
  width: var(--md-sys-nav-rail-width-collapsed, 80px);
  position: sticky;
  top: 0;
  height: 100dvh;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--md-sys-spacing-2);
  padding-block: var(--md-sys-spacing-4);
  background: var(--md-sys-color-surface-container);
  border-inline-end: 1px solid var(--md-sys-color-outline-variant);
}

/* Expanded / Mobile Modal Rail Sheet (GPU-composited slide, zero reflow) */
.md3e-nav-sheet {
  position: fixed;
  inset-block: 0;
  inset-inline-start: 0;
  width: 240px;
  padding: var(--md-sys-spacing-4);
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  border-start-end-radius: var(--md-sys-shape-corner-large);
  border-end-end-radius: var(--md-sys-shape-corner-large);
  box-shadow: var(--md-sys-elevation-level3);
  transform: translateX(-100%);
  transition: transform var(--md-sys-motion-default-spatial);
  z-index: 150;
}

.md3e-nav-sheet.is-open {
  transform: translateX(0);
}

.md3e-nav-scrim {
  position: fixed;
  inset: 0;
  background-color: var(--md-sys-color-scrim);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--md-sys-motion-default-effects);
  z-index: 140;
}

.md3e-nav-scrim.is-active {
  opacity: 0.32;
  pointer-events: auto;
}
```

---

## 11. Interactive Clock Dial & Calendar Date Picker

### 11.1 Clock Dial Interaction Math

The M3E clock dial uses polar angle quantization. When a pointer event occurs on the 256dp dial container:

```javascript
function calculateHourFromPointer(dialElement, clientX, clientY) {
  const rect = dialElement.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const dx = clientX - centerX;
  const dy = clientY - centerY;

  // Compute angle in radians where 12 o'clock is 0 rad (top)
  let theta = Math.atan2(dy, dx) + Math.PI / 2;
  if (theta < 0) theta += 2 * Math.PI;

  // Convert to 360 degrees and quantize to 30-degree (1 hour) increments
  const deg = theta * (180 / Math.PI);
  let hour = Math.round(deg / 30) % 12;
  if (hour === 0) hour = 12;

  return { hour, rotationDeg: hour * 30 };
}
```

### 11.2 Anchored HCT Seed Color Picker (Never Raw `<input type="color">`)

> [!CAUTION]
> **Never expose a bare native `<input type="color">` control in an M3E interface**: On Chromium/Windows/macOS desktop browsers, native color inputs spawn an unstyled OS color dialog (`0px` sharp rectangle corners, fixed `#3B3B3B` background, and `1px` wireframe R/G/B inputs) that breaks tonal containment and clashes visually with dynamic HCT surfaces.
> **The Fix**: Build an anchored `[popover="auto"]` palette panel (`28px` outer `--md-sys-shape-corner-extra-large` -> `12px` concentric inner 2D Chroma×Tone canvas, `surface-container-high` + optional `.md3e-blur-surface`) driven directly by `Hct` / `hctSolveToInt` from `assets/tokens/md3e-dynamic-color.js`. Wire the trigger with native Invoker Commands (`commandfor` + `command="toggle-popover"`, never combining `popovertarget` and `commandfor`, and without `aria-haspopup` on a `role="group"` picker), gate `inset: auto` + `margin` inside `@supports (position-area: block-end)`, style separate `::-webkit-slider-*` / `::-moz-range-*` blocks for Hue/Chroma/Tone range inputs, and feature-detect `EyeDropper` as progressive enhancement. See `assets/starter/index.html` (`#md3e-color-popover`) for the complete implementation.

---

## 12. Official 35-Shape Containers & Optional Frosted Floating Chrome

### 12.1 Masked Polygon Avatars & Decorative Crops (`md3e-shapes.css`)

Use `.md3e-shape` paired with any of the 35 official `.md3e-shape-<name>` classes. Wrap in `.md3e-shape-shadow-wrap` to apply a soft contour shadow (`filter: drop-shadow(...)`):

```html
<span class="md3e-shape-shadow-wrap">
  <div class="md3e-shape md3e-shape-cookie-9-sided md3e-hero-avatar">
    <span class="material-symbols-outlined" aria-hidden="true">auto_awesome</span>
  </div>
</span>
```

```css
.md3e-hero-avatar {
  width: 72px;
  display: grid;
  place-items: center;
  background: var(--md-sys-color-tertiary-container);
  color: var(--md-sys-color-on-tertiary-container);
  --md-sys-icon-size: 32px;
}
```

### 12.2 Accessible Frosted Floating Chrome (`assets/tokens/md3e-blur.css`)

Component surfaces default to opaque tonal `surface-container-*` roles. For floating toolbars, quick-settings sheets, or scrims, link `assets/tokens/md3e-blur.css` and apply `.md3e-blur-surface`, `.md3e-blur-surface-high`, `.md3e-blur-primary`, `.md3e-blur-secondary`, `.md3e-blur-tertiary`, or `.md3e-blur-scrim`. All `.md3e-blur-*` classes automatically tint via `color-mix(in oklab, ...)` (never `in oklch`) and revert cleanly to solid opaque `Surface Container` colours under `@media (prefers-reduced-transparency: reduce)`, `prefers-contrast: more`, `[data-contrast="high"]`, and `@media (forced-colors: active)`:

```html
<div class="md3e-toolbar-floating md3e-blur-surface md3e-blur--lg" role="toolbar" aria-label="Floating blur actions">
  <button type="button" class="md3e-toolbar-btn" aria-label="Pin layer" aria-pressed="false">
    <span class="material-symbols-outlined" aria-hidden="true">keep</span>
  </button>
</div>
```

### 12.3 Real-Time Cubic Bézier Shape-Morphing CTA (`md3e-morph.js`)

Use `assets/tokens/md3e-morph.js` + `assets/tokens/md3e-spring.js` when an interactive control must morph cleanly in real time between any two `MaterialShapes` polygons (for example, `square` → `cookie-9-sided` on press/hold, or toggling `square` ↔ `sunny`). Because the rendered shape is non-rectangular, **never** put `box-shadow` on the button itself — wrap it in `.md3e-shape-shadow-wrap` (`filter: drop-shadow(...)`):

```html
<span class="md3e-shape-shadow-wrap">
  <button type="button" class="md3e-morph-cta" id="morph-cta-btn" aria-label="Morph action shape" aria-pressed="false">
    <svg class="md3e-morph-cta__svg" viewBox="0 0 100 100" aria-hidden="true">
      <path id="morph-cta-path" d="" />
    </svg>
    <span class="material-symbols-outlined md3e-morph-cta__icon" aria-hidden="true">auto_awesome</span>
  </button>
</span>
```

```css
.md3e-morph-cta {
  position: relative;
  display: grid;
  place-items: center;
  inline-size: 64px;
  block-size: 64px;
  padding: 0;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-primary-container);
  cursor: pointer;
}

.md3e-morph-cta__svg {
  inline-size: 100%;
  block-size: 100%;
  fill: var(--md-sys-color-primary-container);
}

.md3e-morph-cta__icon {
  position: relative;
  z-index: 1;
  pointer-events: none;
}

.md3e-morph-cta:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  border-radius: var(--md-sys-shape-corner-large);
}
```

```javascript
import { createShapeMorpher } from './tokens/md3e-morph.js';

const morpher = createShapeMorpher(document.getElementById('morph-cta-path'), {
  initialShape: 'square',
  spring: 'fast-spatial',
});

morpher.bindPressMorph(document.getElementById('morph-cta-btn'), {
  restShape: 'square',
  pressedShape: 'cookie-9-sided',
  toggleShape: 'sunny',
});
```

---

## 13. Sine-Wave Progress Indicators Auto-Straightening at 100% (SVG + HiDPI Canvas)

Per the official M3 Expressive **Wavy Progress Indicator** spec (`references/components/communication.md`):
- **Track thickness**: `4dp` (`8dp` thicker variant) · **Amplitude**: `3dp` (`0dp` at `0%` / `100%`) · **Wavelength**: `40dp` · **Gap & Stop Dot**: `4dp` stop indicator at track end.
- **Colour roles**: Active indicator & stop dot use `--md-sys-color-primary`; track uses `--md-sys-color-secondary-container`.
- **Auto-Straightening (`amplitude -> 0` at `100%`)**: As normalized progress $p \to 1$, target wave amplitude springs smoothly down to `0` (`flattenFactor = smoothstep(0.95 -> 1.0)`), snapping the active indicator cleanly into a flat pill line upon completion!
- **Accessibility & Battery**: Expose completion natively via `role="progressbar"`, `aria-valuemin="0"`, `aria-valuemax="100"`, and `aria-valuenow` (mark `<svg>` / `<canvas>` `aria-hidden="true"` rather than relying on non-standard `canvas-html`), scale `<canvas>` by `window.devicePixelRatio`, pause off-screen `requestAnimationFrame` loops via `contentvisibilityautostatechange` / `IntersectionObserver`, and halt wave phase travel when `@media (prefers-reduced-motion: reduce)` matches.

```html
<!-- 1. SVG Linear Wavy Progress (4dp stroke, 3dp amplitude, 40dp wavelength, auto-straightens at 100%) -->
<div class="md3e-wavy-progress" id="svg-wavy-host" role="progressbar" aria-label="SVG model sync" aria-valuemin="0" aria-valuemax="100" aria-valuenow="68">
  <svg id="svg-wavy-el" viewBox="0 0 320 14" aria-hidden="true">
    <path class="md3e-wavy__track" id="svg-wavy-track" d="" />
    <path class="md3e-wavy__active" id="svg-wavy-active" d="" />
    <circle class="md3e-wavy__stop" cx="316" cy="7" r="2" />
  </svg>
</div>

<!-- 2. High-FPS HiDPI Canvas Linear Wavy Progress -->
<div class="md3e-wavy-progress md3e-wavy-progress--canvas" id="canvas-wavy-host" role="progressbar" aria-label="Canvas pipeline progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="68">
  <canvas id="canvas-wavy-el" aria-hidden="true"></canvas>
</div>
```

```css
.md3e-wavy-progress {
  inline-size: 100%;
  block-size: 14px;
  display: flex;
  align-items: center;
  content-visibility: auto;
  contain-intrinsic-size: auto none auto 14px;
}

.md3e-wavy-progress svg,
.md3e-wavy-progress canvas {
  inline-size: 100%;
  block-size: 14px;
  display: block;
}

.md3e-wavy__track {
  fill: none;
  stroke: var(--md-sys-color-secondary-container);
  stroke-width: 4;
  stroke-linecap: round;
}

.md3e-wavy__active {
  fill: none;
  stroke: var(--md-sys-color-primary);
  stroke-width: 4;
  stroke-linecap: round;
}

.md3e-wavy__stop {
  fill: var(--md-sys-color-primary);
}
```

```javascript
export function createWavyProgressController({ svgHost, svgActive, svgTrack, canvasHost, canvasEl, initialProgress = 68 } = {}) {
  let progress = initialProgress;
  let phase = 0;
  let ampScale = progress >= 100 || progress <= 0 ? 0 : 1;
  let rafId = null;
  let offscreen = false;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const targetAmplitudeFactor = (pct) => {
    if (pct <= 2 || pct >= 100) return 0;
    if (pct >= 94) return (100 - pct) / 6;
    if (pct <= 8) return (pct - 2) / 6;
    return 1;
  };

  const buildWavePath = (xStart, xEnd, yMid, amp, wavelength, ph) => {
    const span = Math.max(0, xEnd - xStart);
    if (span <= 0.5) return '';
    if (amp <= 0.04) return `M${xStart.toFixed(2)} ${yMid} L${xEnd.toFixed(2)} ${yMid}`;
    const step = 2.5;
    let d = '';
    for (let x = 0; x <= span; x += step) {
      const y = yMid + Math.sin((x / wavelength) * Math.PI * 2 - ph) * amp;
      d += `${x === 0 ? 'M' : 'L'}${(xStart + x).toFixed(2)} ${y.toFixed(2)} `;
    }
    const endY = yMid + Math.sin((span / wavelength) * Math.PI * 2 - ph) * amp;
    return `${d}L${xEnd.toFixed(2)} ${endY.toFixed(2)}`;
  };

  const renderFrame = () => {
    const targetFactor = targetAmplitudeFactor(progress);
    ampScale += (targetFactor - ampScale) * (reducedMotion.matches ? 1 : 0.22);
    if (Math.abs(targetFactor - ampScale) < 0.01) ampScale = targetFactor;
    const amp = 3 * ampScale;

    if (svgActive && svgTrack) {
      const W = 320;
      const midY = 7;
      const activeEnd = 4 + ((W - 12) * Math.max(0, Math.min(100, progress))) / 100;
      svgActive.setAttribute('d', buildWavePath(4, activeEnd, midY, amp, 40, phase));
      const trackStart = Math.min(W - 4, activeEnd + 6);
      svgTrack.setAttribute('d', trackStart < W - 4 ? `M${trackStart.toFixed(2)} ${midY} L${W - 4} ${midY}` : '');
      svgHost?.setAttribute('data-wave-amplitude', amp.toFixed(2));
    }

    if (canvasEl) {
      const dpr = window.devicePixelRatio || 1;
      const cssW = Math.max(120, canvasEl.clientWidth || 320);
      const cssH = 14;
      if (canvasEl.width !== Math.round(cssW * dpr) || canvasEl.height !== Math.round(cssH * dpr)) {
        canvasEl.width = Math.round(cssW * dpr);
        canvasEl.height = Math.round(cssH * dpr);
      }
      const ctx = canvasEl.getContext('2d');
      const cs = getComputedStyle(canvasEl);
      const primary = cs.getPropertyValue('--md-sys-color-primary').trim();
      const trackCol = cs.getPropertyValue('--md-sys-color-secondary-container').trim();
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, cssW, cssH);

      const pad = 4;
      const midY = cssH / 2;
      const activeEnd = pad + ((cssW - pad * 3) * Math.max(0, Math.min(100, progress))) / 100;
      ctx.lineWidth = 4;
      ctx.lineCap = 'round';

      if (activeEnd + 6 < cssW - pad) {
        ctx.strokeStyle = trackCol;
        ctx.beginPath();
        ctx.moveTo(activeEnd + 6, midY);
        ctx.lineTo(cssW - pad, midY);
        ctx.stroke();
      }

      if (activeEnd > pad + 0.5) {
        ctx.strokeStyle = primary;
        ctx.beginPath();
        for (let x = pad; x <= activeEnd; x += 2) {
          const y = midY + Math.sin(((x - pad) / 40) * Math.PI * 2 - phase) * amp;
          if (x === pad) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.lineTo(activeEnd, midY + Math.sin(((activeEnd - pad) / 40) * Math.PI * 2 - phase) * amp);
        ctx.stroke();
      }
      ctx.fillStyle = primary;
      ctx.beginPath();
      ctx.arc(cssW - pad, midY, 2, 0, Math.PI * 2);
      ctx.fill();
      canvasHost?.setAttribute('data-wave-amplitude', amp.toFixed(2));
    }
  };

  const loop = () => {
    if (!offscreen && !reducedMotion.matches && ampScale > 0.005) {
      phase = (phase + 0.14) % (Math.PI * 2);
      renderFrame();
      rafId = requestAnimationFrame(loop);
    } else {
      rafId = null;
      renderFrame();
    }
  };

  const kick = () => {
    renderFrame();
    if (!rafId && !offscreen && !reducedMotion.matches) {
      rafId = requestAnimationFrame(loop);
    }
  };

  [svgHost, canvasHost].filter(Boolean).forEach((host) => {
    host.addEventListener('contentvisibilityautostatechange', (e) => {
      offscreen = e.skipped;
      if (!offscreen) kick();
    });
  });

  kick();
  return {
    setProgress(nextPct) {
      progress = Math.max(0, Math.min(100, Number(nextPct) || 0));
      svgHost?.setAttribute('aria-valuenow', String(Math.round(progress)));
      canvasHost?.setAttribute('aria-valuenow', String(Math.round(progress)));
      kick();
    },
    destroy() {
      if (rafId) cancelAnimationFrame(rafId);
    },
  };
}
```

---

## 14. Additional Native AndroidX Compose M3E (`1.4+`) Capabilities

### 14.1 Variable-Width Icon Buttons (`narrow` / `default` / `wide`)

Standard `40dp` Small Icon Buttons support three native width profiles (`narrow` `32px`, `default` `40px`, `wide` `52px`) while keeping an invisible `48×48px` `::before` hit area and morphing corners (`20px` unselected pill → `12px` selected square):

```css
.md3e-icon-btn--var {
  position: relative;
  display: inline-grid;
  place-items: center;
  height: 40px;
  border: none;
  border-radius: var(--md-sys-shape-corner-large-increased);
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  transition:
    inline-size var(--md-sys-motion-fast-spatial),
    border-radius var(--md-sys-motion-fast-spatial),
    background-color var(--md-sys-motion-fast-effects);
}

.md3e-icon-btn--narrow { inline-size: 32px; }
.md3e-icon-btn--default { inline-size: 40px; }
.md3e-icon-btn--wide { inline-size: 52px; }

.md3e-icon-btn--var::before {
  content: "";
  position: absolute;
  inset: -4px -8px;
  min-width: var(--md-sys-touch-target-min);
  min-height: var(--md-sys-touch-target-min);
}

.md3e-icon-btn--var[aria-pressed="true"] {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: var(--md-sys-shape-corner-medium);
  --md-sys-icon-fill: 1;
}

.md3e-icon-btn--var:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

@media (prefers-reduced-motion: reduce) {
  .md3e-icon-btn--var {
    transition: none;
  }
}
```

### 14.2 Flexible Collapsing Top App Bar & Multi-Browse Carousel

- **Flexible Top App Bar (`MediumFlexible` / `LargeFlexible`)**: Expand bar height (`64px` collapsed ↔ `112px` medium / `152px` large) paired with variable-font `'GRAD'` / `'ROND'` / `'wght'` interpolation on the title rather than animating `font-size` across layout frames.
- **Multi-Browse Hero Carousel**: Pair `scroll-snap-type: x mandatory` (`md3e-carousel`) with focusable `flex-basis` shifts on hovered/focused hero items so focused cards widen with `--md-sys-motion-default-spatial` while preserving keyboard arrow/Tab scroll into view.

