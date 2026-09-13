# Expressive Component Recipes (HTML / CSS / JS)

These recipes implement the **Expressive components introduced in Material 3 Expressive (May 2025+)** that are not provided by `@material/web` (which is in maintenance mode).

Every recipe uses pure semantic HTML, MD3E CSS tokens (`--md-sys-*`), and spring motion. They work out of the box with zero dependencies and can be used alongside `@material/web` or in any framework (React, Vue, Svelte, Vanilla).

---

## 1. Toolbars (Docked & Floating)

> [!IMPORTANT]
> The baseline bottom app bar is **no longer recommended** in M3E. Consider a **Docked Toolbar** for fixed edge placement or a **Floating Toolbar** when actions need flexible placement or elevation.

### 1.1 Floating Toolbar

A pill-shaped toolbar elevated above content. Ideal for contextual actions, canvas controls, or mobile bottom navigation.

```html
<nav class="md3e-toolbar-floating" aria-label="Quick actions">
  <button class="md3e-toolbar-btn" aria-label="Draw">
    <span class="material-symbols-outlined">brush</span>
  </button>
  <button class="md3e-toolbar-btn" aria-label="Erase">
    <span class="material-symbols-outlined">ink_eraser</span>
  </button>
  <div class="md3e-toolbar-divider" role="separator"></div>
  <button class="md3e-toolbar-btn" aria-label="Undo">
    <span class="material-symbols-outlined">undo</span>
  </button>
  <button class="md3e-toolbar-btn" aria-label="Redo">
    <span class="material-symbols-outlined">redo</span>
  </button>
  <div class="md3e-toolbar-divider" role="separator"></div>
  <button class="md3e-toolbar-btn md3e-toolbar-btn--primary" aria-label="Share">
    <span class="material-symbols-outlined">share</span>
  </button>
</nav>
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
  height: 56px;
  padding-inline: var(--md-sys-spacing-2);
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-full);
  box-shadow: var(--md-sys-elevation-level2);
  z-index: 100;
  transition: transform var(--md-sys-motion-default-spatial);
}

.md3e-toolbar-btn {
  position: relative;
  display: grid;
  place-items: center;
  width: var(--md-sys-touch-target-min); /* 48px hit target */
  height: var(--md-sys-touch-target-min);
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  border-radius: var(--md-sys-shape-corner-full);
  cursor: pointer;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-toolbar-btn:hover {
  background: color-mix(in srgb, currentColor var(--md-sys-state-hover-state-layer-opacity), transparent);
  color: var(--md-sys-color-on-surface);
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--md-sys-color-outline-variant);
}
```

---

## 2. Split Button

A combined control: primary action on the start side, flyout/menu trigger on the end side.
Shares a single continuous silhouette with an inner divider.

```html
<div class="md3e-split-btn md3e-split-btn--filled">
  <button class="md3e-split-btn__action" type="button">
    <span class="material-symbols-outlined">send</span>
    Publish
  </button>
  <div class="md3e-split-btn__divider"></div>
  <button class="md3e-split-btn__arrow" aria-label="More publishing options" aria-haspopup="menu" aria-expanded="false" type="button">
    <span class="material-symbols-outlined">arrow_drop_down</span>
  </button>
</div>
```

```css
.md3e-split-btn {
  display: inline-flex;
  align-items: stretch;
  height: 40px;
  border-radius: var(--md-sys-shape-corner-full);
  overflow: hidden;
  position: relative;
  transition: transform var(--md-sys-motion-fast-spatial);
}

/* Filled Variant */
.md3e-split-btn--filled {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}

/* Tonal Variant */
.md3e-split-btn--tonal {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

/* Outlined Variant */
.md3e-split-btn--outlined {
  background: transparent;
  color: var(--md-sys-color-primary);
  box-shadow: inset 0 0 0 1px var(--md-sys-color-outline);
}

.md3e-split-btn__action {
  display: inline-flex;
  align-items: center;
  gap: var(--md-sys-spacing-2);
  padding-inline-start: var(--md-sys-spacing-4);
  padding-inline-end: var(--md-sys-spacing-3);
  border: none;
  background: transparent;
  color: inherit;
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  cursor: pointer;
}

.md3e-split-btn__divider {
  width: 1px;
  margin-block: var(--md-sys-spacing-2);
  background: currentColor;
  opacity: 0.38;
}

.md3e-split-btn__arrow {
  display: grid;
  place-items: center;
  padding-inline: var(--md-sys-spacing-2);
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.md3e-split-btn__action:hover,
.md3e-split-btn__arrow:hover {
  background: color-mix(in srgb, currentColor 0.12, transparent);
}

.md3e-split-btn__action:focus-visible,
.md3e-split-btn__arrow:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: -2px;
}
```

---

## 3. Button Groups (Connected & Continuous Silhouette)

In MD3E, grouped buttons share inner borders and maintain an outer continuous silhouette using asymmetric shape tokens.

```html
<div class="md3e-btn-group" role="group" aria-label="Text formatting">
  <button class="md3e-group-btn" aria-pressed="true">
    <span class="material-symbols-outlined">format_bold</span>
  </button>
  <button class="md3e-group-btn" aria-pressed="false">
    <span class="material-symbols-outlined">format_italic</span>
  </button>
  <button class="md3e-group-btn" aria-pressed="false">
    <span class="material-symbols-outlined">format_underlined</span>
  </button>
</div>
```

```css
.md3e-btn-group {
  display: inline-flex;
  border-radius: var(--md-sys-shape-corner-medium); /* 12px */
  background: var(--md-sys-color-surface-container);
  border: 1px solid var(--md-sys-color-outline-variant);
  overflow: hidden;
}

.md3e-group-btn {
  display: inline-grid;
  place-items: center;
  min-width: var(--md-sys-touch-target-min);
  min-height: var(--md-sys-touch-target-min);
  padding: var(--md-sys-spacing-2) var(--md-sys-spacing-3);
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface);
  cursor: pointer;
  position: relative;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-group-btn + .md3e-group-btn {
  border-inline-start: 1px solid var(--md-sys-color-outline-variant);
}

.md3e-group-btn[aria-pressed="true"] {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

.md3e-group-btn:hover {
  background: color-mix(in srgb, currentColor 0.08, transparent);
}

.md3e-group-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: -2px;
  z-index: 1;
}
```

---

## 4. FAB Menu (Morphing Action Sheet)

A Floating Action Button that morphs into a stacked speed-dial / action menu.

```html
<div class="md3e-fab-menu-container">
  <!-- Backdrop scrim -->
  <div class="md3e-fab-scrim" id="fab-scrim" aria-hidden="true"></div>

  <!-- Menu items list -->
  <div class="md3e-fab-menu" id="fab-menu" role="menu" aria-hidden="true">
    <div class="md3e-fab-menu-item" role="menuitem">
      <span class="md3e-fab-menu-label">Upload file</span>
      <button class="md3e-fab-mini" aria-label="Upload file">
        <span class="material-symbols-outlined">upload_file</span>
      </button>
    </div>
    <div class="md3e-fab-menu-item" role="menuitem">
      <span class="md3e-fab-menu-label">New document</span>
      <button class="md3e-fab-mini" aria-label="New document">
        <span class="material-symbols-outlined">note_add</span>
      </button>
    </div>
  </div>

  <!-- Main FAB trigger -->
  <button class="md3e-fab" id="fab-trigger" aria-label="Actions menu" aria-expanded="false">
    <span class="material-symbols-outlined md3e-fab-icon">add</span>
  </button>
</div>
```

```css
.md3e-fab-menu-container {
  position: fixed;
  inset-block-end: var(--md-sys-spacing-6);
  inset-inline-end: var(--md-sys-spacing-6);
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--md-sys-spacing-3);
  z-index: 900;
}

.md3e-fab {
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
              background-color var(--md-sys-motion-fast-effects);
}

.md3e-fab-icon {
  font-size: 24px;
  transition: transform var(--md-sys-motion-default-spatial);
}

.md3e-fab[aria-expanded="true"] .md3e-fab-icon {
  transform: rotate(45deg);
}

.md3e-fab-menu {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--md-sys-spacing-3);
  opacity: 0;
  pointer-events: none;
  transform: translateY(16px) scale(0.95);
  transition: opacity var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-default-spatial);
}

.md3e-fab-menu[aria-hidden="false"] {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0) scale(1);
}

.md3e-fab-menu-item {
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-3);
}

.md3e-fab-menu-label {
  padding: var(--md-sys-spacing-1) var(--md-sys-spacing-3);
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-small);
  font-size: var(--md-sys-typescale-label-large-size);
  box-shadow: var(--md-sys-elevation-level1);
}

.md3e-fab-mini {
  width: 40px;
  height: 40px;
  border-radius: var(--md-sys-shape-corner-medium);
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  border: none;
  cursor: pointer;
  display: grid;
  place-items: center;
  box-shadow: var(--md-sys-elevation-level2);
}
```

```javascript
// Lightweight trigger handler
const trigger = document.getElementById('fab-trigger');
const menu = document.getElementById('fab-menu');

trigger.addEventListener('click', () => {
  const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
  trigger.setAttribute('aria-expanded', String(!isExpanded));
  menu.setAttribute('aria-hidden', String(isExpanded));
});
```

---

## 5. Expressive Loading Indicator (Morphing Shape Loader)

> [!NOTE]
> In MD3E, the indeterminate circular spinner is replaced for short waits (<5s) by the **Expressive Loading Indicator**, which morphs playfully between geometric shapes using spring dynamics.

```html
<div class="md3e-loading-indicator" role="status" aria-label="Loading...">
  <div class="md3e-loader-shape"></div>
</div>
```

```css
.md3e-loading-indicator {
  display: inline-grid;
  place-items: center;
  width: 48px;
  height: 48px;
}

.md3e-loader-shape {
  width: 32px;
  height: 32px;
  background: var(--md-sys-color-primary);
  animation: md3e-shape-morph 2.4s ease-in-out infinite;
}

@keyframes md3e-shape-morph {
  0% {
    border-radius: var(--md-sys-shape-corner-full); /* Circle */
    transform: rotate(0deg) scale(1);
    background: var(--md-sys-color-primary);
  }
  25% {
    border-radius: var(--md-sys-shape-corner-medium); /* Rounded square */
    transform: rotate(90deg) scale(0.85);
    background: var(--md-sys-color-secondary);
  }
  50% {
    border-radius: var(--md-sys-shape-corner-extra-large-increased); /* Soft pill */
    transform: rotate(180deg) scale(1.05);
    background: var(--md-sys-color-tertiary);
  }
  75% {
    border-radius: 4px 28px 4px 28px; /* Organic leaf/petal */
    transform: rotate(270deg) scale(0.9);
    background: var(--md-sys-color-primary-container);
  }
  100% {
    border-radius: var(--md-sys-shape-corner-full);
    transform: rotate(360deg) scale(1);
    background: var(--md-sys-color-primary);
  }
}

@media (prefers-reduced-motion: reduce) {
  .md3e-loader-shape {
    animation: md3e-pulse 1.5s ease-in-out infinite;
    border-radius: var(--md-sys-shape-corner-full);
  }
  @keyframes md3e-pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
  }
}
```

---

## 6. Toggle Buttons (Shape Morphing & Animation Physics)

Toggle buttons morph resting shapes: **Round when unselected, Square when selected**.

> [!CAUTION]
> **Common Pitfall: Why `9999px` breaks shape morph animations**:
> In CSS, `var(--md-sys-shape-corner-full)` is defined as `9999px`. When animating `border-radius` between `9999px` and `12px` (`corner-medium`), the browser numerically interpolates from 9999 down to 12. However, for a 40px height button, the browser visually clamps any corner radius $\ge 20\text{px}$ to half the button's height. Because 99.8% of the numerical range [12, 9999] lies above 20px, the button remains visually clamped as a full pill for 99.8% of the duration, then snaps suddenly into a square in the final 1–2 frames! In reverse (12px to 9999px), it crosses 20px in the very first frame, showing zero animation.
> 
> **The Fix**: For a standard 40px button, use `var(--md-sys-shape-corner-large-increased)` (`20px`) for the unselected pill state. Since $20\text{px} = \frac{40\text{px}}{2}$, it renders as a geometrically perfect pill, while keeping the interpolation range tightly bounded to $[12\text{px}, 20\text{px}]$. Every millisecond of the spring physics curve is fully visible in both directions!

```html
<button class="md3e-toggle-btn" aria-pressed="false" onclick="this.setAttribute('aria-pressed', this.getAttribute('aria-pressed') === 'true' ? 'false' : 'true')">
  <span class="material-symbols-outlined">bookmark</span>
  Save Bookmark
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
  font: inherit;
  font-size: var(--md-sys-typescale-label-large-size);
  cursor: pointer;
  border: none;
  user-select: none;
  
  /* Unselected state: Round shape (20px on 40px height = exact pill), surface-container fill */
  background: var(--md-sys-color-surface-container);
  color: var(--md-sys-color-on-surface-variant);
  border-radius: var(--md-sys-shape-corner-large-increased); /* 20px */
  
  transition: border-radius var(--md-sys-motion-default-spatial),
              background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-fast-spatial);
}

/* Touch target hit area (48px) */
.md3e-toggle-btn::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  min-height: var(--md-sys-touch-target-min);
  min-width: var(--md-sys-touch-target-min);
}

.md3e-toggle-btn:active {
  transform: scale(0.97);
}

.md3e-toggle-btn[aria-pressed="true"] {
  /* Selected state: Square shape (12dp), primary container fill */
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  border-radius: var(--md-sys-shape-corner-medium); /* 12px */
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
}

.md3e-toggle-btn[aria-pressed="true"] .material-symbols-outlined {
  font-variation-settings: 'FILL' 1;
}

.md3e-toggle-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}
```

---

## 7. Search Bar (Integrated Focus & Suppressing Inner Browser Outlines)

> [!CAUTION]
> **Common Pitfall**: In web browsers, native `<input>` elements automatically render a sharp rectangular user-agent focus outline when focused. When placing an `<input>` inside a pill-shaped Material Design container (`--md-sys-shape-corner-full`), you **must** set `outline: 2px solid transparent;` (or `outline-color: transparent;`) and `border: none;` on the inner input, while letting the parent container handle `:focus-within` with the MD3E focus ring. Otherwise, an ugly rectangular browser input box will appear trapped inside the pill!

```html
<div class="md3e-search-bar" role="search">
  <span class="material-symbols-outlined md3e-search-icon">search</span>
  <input type="text" placeholder="Search..." aria-label="Search content">
  <button class="md3e-icon-btn" aria-label="Voice search">
    <span class="material-symbols-outlined">mic</span>
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
  border-radius: var(--md-sys-shape-corner-full); /* 9999px pill */
  width: 100%;
  max-width: 480px;
  cursor: text;
  transition: background-color var(--md-sys-motion-fast-effects);
}

/* Container handles the visible MD3E focus ring */
.md3e-search-bar:focus-within {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  background-color: var(--md-sys-color-surface-container-highest);
}

/* Inner native input: suppress default browser rectangular outline */
.md3e-search-bar input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font: inherit;
  font-size: var(--md-sys-typescale-body-large-size);
  padding: 0;
  height: 100%;
  outline: 2px solid transparent; /* Suppresses browser UA focus rectangle; preserves Windows High Contrast mode */
  box-shadow: none;
}
```

```
