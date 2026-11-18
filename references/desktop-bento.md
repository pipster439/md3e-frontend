# Desktop Bento Dashboard Extension Layer (Layer 3 — Opt-In Product Style)

> [!IMPORTANT]
> **Layer 3 Opt-In Product Extension (`CUSTOM` Tier under `--mode=desktop-bento`)**:
> This document defines an **opt-in product-style desktop telemetry extension** (`data-layout-profile="desktop-bento"`). It is **NOT part of Layer 1 Official M3E specifications**: in the compliance auditor, rules `MD3E101`–`MD3E104` emit `[CUSTOM]` findings **only** when `--mode=desktop-bento` (or `--mode=personal-studio`) is explicitly passed, and **are excluded from the Official M3E Compliance Score**. Keep this layer isolated from default M3E apps (`references/layout.md`, `--mode=strict`):
> `python scripts/audit_md3e.py <path> --mode=desktop-bento --fail-on warning`
> *(Optional personal customization: see [`references/personal-studio.md`](personal-studio.md) for the strictly dormant **Layer 4** profile, which MUST NOT be loaded unless the user explicitly asks for Personal Studio / Layer 4.)*

Desktop Bento dashboards optionally choose borderless tonal surface nesting, dual-tier control vs telemetry row ergonomics, and Android 16 M3E plush organic spatial springs (`~460–500ms` via `synthesizeSpringLinearCss`) for command-center layouts.

---

## 1. Window Chrome, Navigation Rail & Bento Grid (Opt-In Presets)

- **Frameless Integrated Titlebar (`44px` preset)**: Product chrome preset blending with `--md-sys-color-surface` without a `1px` header hairline (`env(titlebar-area-height, 44px)`). Reserve `::before` `48px` hit targets on compact window controls and keep `:focus-within` / `outline: 2px solid transparent` on borderless search inputs.
- **Collapsible Dual-Spring Navigation Rail (`80px <-> 220px`, with `64px` icon-only compact preset)**: Desktop Bento layouts can pair a `80px` collapsed / `220px` expanded dual-spring navigation rail (Spatial Spring on `width` + active pill, Effects Spring on `white-space: nowrap` labels so text never squishes or wraps) with `48×48px` clickable destinations, active `secondary-container` pills, roving arrow-key navigation, and view-switch Fade Through + `25ms–35ms` card stagger. Ultra-minimal icon-only consoles may stay fixed at `64px`.
- **12-Column Asymmetric Bento Grid**: CSS Grid (`grid-template-columns: repeat(12, minmax(0, 1fr))`, `gap: var(--md-sys-spacing-4)`) collapsing cleanly at `< 1200px` (`8` cols) and `< 840px` (`4` cols), plus `container-type: inline-size` on wide telemetry cards.

---

## 2. Dual-Tier Density & Hero Typography Scale

Combine compact operational scanning with unmistakably tactile primary controls:

| Tier | Target Elements | Height / Scale Rule | Tokens |
|---|---|---|---|
| **Dense Data Tier** | Data tables (`tbody tr`), live log items, telemetry rows | Strictly **`32px–36px`** row height (`--md-bento-row-height: 34px`), `tabular-nums`, sticky `<thead>`, single-line overflow handling | `--md-sys-typescale-body-small-*`, `--md-sys-typescale-label-medium-*` |
| **Chunky Action Tier** | Primary Hero CTA, switches, connected segmented pills, floating/docked toolbar | Chunky **`44px–64px`** vertical presence (`48px–60px` switches/CTA, `64px` toolbar), preserving `>= 48px` accessible hit targets | `--md-sys-shape-corner-large`, `--md-sys-shape-corner-extra-large` |
| **Hero KPI Scale** | Hero card core numeric readout vs metric label | Metric `font-size` **`>= 3×`** its label `font-size` (e.g., `57px` `display-large` / `12px` `label-medium` = `4.75×`, or `45px` / `14px` = `3.21×`), enhanced with `Google Sans Flex` `GRAD`/`ROND`/`wght` spring transitions | `--md-sys-typescale-display-large-size` / `display-medium-size` |

```css
/* Dual-tier density tokens layered only under [data-layout-profile="desktop-bento"] */
:root[data-layout-profile="desktop-bento"] {
  --md-bento-row-height: 34px;       /* Dense 32px-36px telemetry row */
  --md-bento-control-height: 48px;   /* Chunky 44px-64px primary controls */
  --md-bento-hero-cta-size: 60px;    /* Chunky Hero morphing shape button */

  /* Android 16 M3E plush spatial springs (synthesized 36-point curves via synthesizeSpringLinearCss) */
  --md-bento-motion-fast-effects: 150ms cubic-bezier(0.34, 0.88, 0.34, 1);
  --md-bento-motion-default-effects: 200ms cubic-bezier(0.34, 0.80, 0.34, 1);
  --md-bento-motion-fast-spatial: var(--md-sys-motion-fast-spatial);       /* ~340ms crisp control settle (k=620, z=0.74) */
  --md-bento-motion-default-spatial: var(--md-sys-motion-default-spatial); /* ~460-500ms plush spatial settle (k=380/340) */
}
```

---

## 3. Opt-In Product Visual Style (`CUSTOM` Tier, Excluded from Official M3E Score)

All visual layout opinions below (`MD3E101`–`MD3E104`) are **Layer 3 Opt-In Product Extensions**. None of them are mandatory Google M3E rules, and none of them affect the `official_compliance` score:

1. **Borderless Tonal Panels (`[CUSTOM]` `MD3E101`)**:
   - In Bento product layouts, omit decorative `1px solid` card borders and rectangular `box-shadow`s in favor of tonal surface steps.
   - Keyboard `:focus-visible` rings (`3px solid var(--md-sys-color-secondary)`) and `@media (forced-colors: active)` (`1px solid CanvasText`) are always required (`[ERROR]` if removed), and analytical data views (tables, chart SVG axes/ticks, canvas viewports) are automatically exempt from `MD3E101`.
2. **4+ Surface Container Luminance Tiers (`[CUSTOM]` `MD3E102`)**:
   - Product Bento chrome differentiates panels via `surface` -> `surface-container-lowest` -> `surface-container-low` -> `surface-container` -> `surface-container-high` -> `surface-container-highest`. Standard M3 apps can use fewer tiers with zero penalty.
3. **Concentric Corner Radius Step-Down (`28px` / `16px`, `[CUSTOM]` `MD3E103`)**:
   - Outer `.bento-card` uses `--md-sys-shape-corner-extra-large` (`28px`) paired with `12px–16px` padding so nested `.bento-well` wells step down to `--md-sys-shape-corner-large` (`16px`).
4. **80 / 20 Product Hero Budget & Analytical Data View Exemption (`[CUSTOM]` `MD3E104`)**:
   - **~80% Orthogonal Operational Grid**: Clean, aligned telemetry tables, log streams, tonal progress bars, and tactile controls without forced decorative flair.
   - **Product Marketing / Status Hero Cards**: Product-style status heroes may combine three opt-in Bento motifs (`MD3E104`):
     1. Subtle **fluid sine-wave SVG backdrop** (`<svg aria-hidden="true">` tinted via `in oklab`),
     2. Interactive **morphing `MaterialShapes` CTA button** powered by `md3e-morph.js` + `md3e-spring.js` with wrapper **`filter: drop-shadow(...)`** (`MD3E023`),
     3. **Edge-bleed axis-less micro Sparkline**.
   - **Mandatory Analytical & Scientific Data-View Exemption**: **NEVER** strip functional coordinate axes, tick marks, or table rules—and **NEVER** inject decorative Hero waves or Sparklines—just to satisfy `--mode=desktop-bento`. Mark scientific/analytical cards or pages with `data-md3e-exempt="data-view"`, or rely on the auditor's automatic exemption for `<canvas>` workspaces, `<svg>` charts with axes/ticks (`line`/`polyline`/`rect` + text labels), 2D trajectory/replay viewports, and dense `<table>` views (`MD3E101` and `MD3E104` automatically stand down).

```html
<article class="bento-card bento-card--hero">
  <svg class="bento-hero__wave" viewBox="0 0 400 120" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0,70 C80,30 140,105 220,62 C300,20 350,86 400,52 L400,120 L0,120 Z" />
  </svg>

  <div class="bento-hero__top">
    <div>
      <span class="bento-label">Cluster availability</span>
      <div class="bento-kpi">99.98%</div>
    </div>
    <span class="bento-hero__cta-shadow">
      <button type="button" class="bento-hero__cta" id="hero-morph-btn" aria-label="Trigger mesh rebalance">
        <svg viewBox="0 0 100 100" aria-hidden="true"><path id="hero-morph-path" d="" /></svg>
        <span class="material-symbols-outlined bento-hero__cta-icon" aria-hidden="true">bolt</span>
      </button>
    </span>
  </div>

  <div class="bento-well">
    <span class="bento-well__caption">Concentric nested summary well (28px outer / 16px inner)</span>
  </div>

  <svg class="bento-hero__sparkline" viewBox="0 0 360 56" preserveAspectRatio="none" aria-hidden="true">
    <path class="bento-spark-fill" d="M0,44 L45,38 L90,41 L135,28 L180,32 L225,18 L270,22 L315,12 L360,16 L360,56 L0,56 Z" />
    <path class="bento-spark-line" d="M0,44 L45,38 L90,41 L135,28 L180,32 L225,18 L270,22 L315,12 L360,16" />
  </svg>
</article>
```

```css
.bento-card {
  position: relative;
  overflow: hidden;
  padding: var(--md-sys-spacing-3);
  border-radius: var(--md-sys-shape-corner-extra-large); /* 28px outer */
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  transition: background-color var(--md-bento-motion-fast-effects);
}

.bento-card:hover {
  background: color-mix(in oklab, var(--md-sys-color-on-surface) 8%, var(--md-sys-color-surface-container-low));
}

.bento-card:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.bento-card--hero {
  background: var(--md-sys-color-surface-container);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--md-sys-spacing-3);
}

.bento-well {
  position: relative;
  z-index: 1;
  padding: var(--md-sys-spacing-3);
  border-radius: var(--md-sys-shape-corner-large); /* 16px concentric inner */
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
}

.bento-well__caption {
  font-size: var(--md-sys-typescale-body-small-size);
  line-height: var(--md-sys-typescale-body-small-line-height);
}

.bento-hero__top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bento-label {
  font-size: var(--md-sys-typescale-label-medium-size); /* 12px */
  line-height: var(--md-sys-typescale-label-medium-line-height);
  color: var(--md-sys-color-on-surface-variant);
}

.bento-kpi {
  font-family: "Google Sans Flex", "Roboto Flex", var(--md-sys-typescale-brand-font);
  font-size: var(--md-sys-typescale-display-large-size); /* 57px = 4.75x label */
  line-height: var(--md-sys-typescale-display-large-line-height);
  font-weight: var(--md-sys-typescale-display-large-emphasized-weight);
  font-variant-numeric: tabular-nums;
}

.bento-hero__wave {
  position: absolute;
  inset: auto 0 0 0;
  inline-size: 100%;
  block-size: 64%;
  fill: color-mix(in oklab, var(--md-sys-color-primary-container) 42%, transparent);
  pointer-events: none;
}

.bento-hero__sparkline {
  position: relative;
  z-index: 1;
  display: block;
  inline-size: calc(100% + var(--md-sys-spacing-6));
  margin-inline: calc(-1 * var(--md-sys-spacing-3));
  margin-block-end: calc(-1 * var(--md-sys-spacing-3));
  block-size: 56px;
}

.bento-spark-fill {
  fill: color-mix(in oklab, var(--md-sys-color-primary) 20%, transparent);
}

.bento-spark-line {
  fill: none;
  stroke: var(--md-sys-color-primary);
  stroke-width: 2;
}

/* Non-rectangular shape shadow strictly via wrapper filter: drop-shadow() */
.bento-hero__cta-shadow {
  display: inline-flex;
  filter: drop-shadow(0 6px 14px color-mix(in oklab, var(--md-sys-color-shadow) 28%, transparent));
}

.bento-hero__cta {
  position: relative;
  display: grid;
  place-items: center;
  inline-size: var(--md-bento-hero-cta-size, 60px);
  block-size: var(--md-bento-hero-cta-size, 60px);
  padding: 0;
  border: none;
  background: transparent;
  color: var(--md-sys-color-on-primary);
  cursor: pointer;
}

.bento-hero__cta svg {
  inline-size: 100%;
  block-size: 100%;
  fill: var(--md-sys-color-primary);
}

.bento-hero__cta-icon {
  position: absolute;
  color: var(--md-sys-color-on-primary);
}

.bento-hero__cta:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
  border-radius: var(--md-sys-shape-corner-large);
}

@media (forced-colors: active) {
  .bento-card,
  .bento-well {
    border: 1px solid CanvasText;
  }
}

@media (prefers-reduced-motion: reduce) {
  .bento-card {
    transition: none;
  }
}
```

---

## 4. Desktop Micro-Interactions & Web Engineering Protections

1. **Mouse `:hover` + Keyboard `:focus-visible`**: Every interactive tile, table row hover state, switch, segmented item, and shape CTA implements subtle tonal hover overlays (`8%` via `color-mix(in oklab, ...)`) AND unmistakable `3px` `--md-sys-color-secondary` `:focus-visible` focus rings (`--md-sys-focus-ring-offset: 2px`; missing `:focus-visible` is `[ERROR]` `MD3E005`).
2. **Android 16 M3E Plush Organic Spatial Springs (`~460–500ms` via `synthesizeSpringLinearCss`)**: Pair JS morphers and CSS Bento layout transitions with 36-point curves synthesized by `synthesizeSpringLinearCss(stiffness, damping, 36)` from `assets/tokens/md3e-spring.js` instead of abrupt `240ms` 5-stop approximations: `k = 380, z = 0.78` (`~460ms` default spatial), `k = 340, z = 0.76` (`~500ms` plush modal Expand/Close), `k = 620, z = 0.74` (`~340ms` crisp fast spatial), and Fade Through (`130ms` emphasized-accelerate exit + `460ms` staggered arrival at `32ms` step).
3. **Never Pair `9999px` (`corner-full`) With `border-radius` Spring Morphs (`MD3E019` `[WARNING]`)**: Any pill button transitioning `border-radius` on `:active` under an underdamped `linear()` spring (`1.07` overshoot, such as `--md-bento-motion-fast-spatial`) evaluates `9999px + 1.07 * (16px - 9999px) = -682.8px -> 0px`, flashing a razor-sharp rectangle mid-click! Bind resting radii to `calc(height / 2)` (`24px` on `48px` CTAs -> `12px`, `18px` on `36px` pills -> `8px`) so overshoot stays strictly positive across all frames.
4. **Shape Drop Shadows (`MD3E023` `[WARNING]`)**: Avoid placing `box-shadow` directly on `.md3e-shape*`, `mask-image`, or morphing `<svg>` shapes (clipping or rectangular glow). Wrap the button/shape container in `filter: drop-shadow(...)`.
5. **Ban `in oklch` on Neutral Color Mixing (`MD3E018` `[ERROR]`)**: Never use `color-mix(in oklch, ...)` on `surface*`, `on-surface*`, `outline*`, `shadow`, `scrim`, or `currentColor` — triggers Chromium's powerless-hue pink/red shift; always use **`in oklab`**.
6. **`dt`-Invariant Refresh-Rate Engine & `document.hidden`-Only Pause Policy**: Step springs, shape morphers, and wavy SVG/Canvas progress indicators using clamped `performance.now()` delta (`dt` with `1/60` frame-1 baseline) so `60Hz`, `120Hz`, `144Hz`, and `240Hz` displays run at identical speed. Pause continuous loops **only** when `document.hidden === true` (`visibilitychange` rebases `lastTs` on return) — never set `content-visibility: auto` or foreground blur throttling on actively animating `.md3e-wavy-progress` elements.
7. **View Transitions Stacking Isolation & Wave-Ghosting Suppression**: Keep `view-transition-name` off `.bento-adaptive-toolbar` except while `.is-toolbar-morphing` is active (clearing in `t.finished.finally(...)`). During `html[data-vt-kind="modal"]` Expand/Close transitions, assign `view-transition-name: bento-vt-scrim` on `#bento-vt-backdrop` with `::view-transition-group(bento-vt-scrim) { z-index: 10; }` below `::view-transition-group(bento-vt-panel), ::view-transition-group(bento-vt-heading) { z-index: 20; }`, and set `::view-transition-old(root) { animation: none; display: none; }` + `::view-transition-new(root) { animation: none; }` so live wavy progress bars underneath never ghost.
8. **Reference Implementation**: See targeted ranges of [`assets/starter/desktop-bento.html`](../assets/starter/desktop-bento.html) (never read in full into context; inspect specific component blocks only).

---

## 5. Global HCT Selection Highlight & Scoped Desktop Context Menu

### 5.1 Global Dynamic HCT `::selection` (`assets/tokens/md3e-tokens.css`)
Replace harsh OS default blue selection highlights with theme- and seed-reactive HCT roles built into the token layer:
- **Prose default (`::selection`)**: `background-color: var(--md-sys-color-primary-container)` paired with `color: var(--md-sys-color-on-primary-container)`.
- **Code & Monospace Metrics (`code`, `pre`, `.tabular-nums`)**: `background-color: var(--md-sys-color-tertiary-container)` paired with `color: var(--md-sys-color-on-tertiary-container)` for crisp visual contrast across telemetry tables and logs.

### 5.2 Scoped Desktop Context Menu (`[data-context-menu]`)
Desktop consoles provide contextual right-click actions strictly scoped to explicit operational containers rather than hijacking the whole document:
1. **Strict Scope & DevTools Escape Hatch**:
   - Bind `contextmenu` handling **only** to elements carrying `[data-context-menu]` (e.g., `#telemetry-tbody tr[data-context-menu]` and operational `.bento-card[data-context-menu]`).
   - Always begin the handler with `if (e.shiftKey) return;` so **Shift + Right-Click** immediately passes through to the browser DevTools Inspector.
   - Explicitly allow ordinary `<p>` prose selections and `<input>` / `<textarea>` / `[contenteditable]` fields to open the browser's native copy/paste/spellcheck menu.
2. **Frosted Chrome, Borderless Contrast & Edge-Flip Spring Origin**:
   - Surface the overlay via `md3e-blur-surface-high md3e-blur--md` (preserving `@media (prefers-reduced-transparency: reduce)` solid fallback), `background` tonal contrast (`surface-container-high` -> `on-surface`), `--md-sys-shape-corner-large` (`16px` corner radius), and wrapper `filter: drop-shadow(...)` (zero `1px solid` borders or rectangular `box-shadow`).
   - Measure live menu `offsetWidth` and `offsetHeight` against viewport bounds: auto-flip horizontally and/or vertically across all 4 viewport edges, dynamically anchor `transform-origin` to the clicked quadrant (`top left`, `top right`, `bottom left`, `bottom right`), and trigger a crisp `~150ms` `md3e-spring.js` (`createSpringAnimator({ stiffness: 1800, damping: 0.92 })`) scale+fade pop-in from the cursor tip.
3. **ARIA Menu Contract & Dismissal Loop**:
   - Expose `role="menu"` on the menu panel and `role="menuitem"` on `<button type="button">` commands (`<hr role="separator">` for tonal separators).
   - Implement full keyboard navigation (`ArrowDown`, `ArrowUp`, `Home`, `End`, `Enter`, `Space`, `Escape`, `Tab`) + focus restoration to the triggering row/card when dismissed via keyboard, plus automatic close on outside `pointerdown`, `scroll` (capture phase), `resize`, and `blur`.

```js
import { createSpringAnimator } from '../tokens/md3e-spring.js';

document.addEventListener('contextmenu', (e) => {
  if (e.shiftKey) return; // Always allow Shift+Right-Click for DevTools Inspect
  const target = e.target;
  if (!(target instanceof Element)) return;
  if (target.closest('input, textarea, select, [contenteditable="true"]')) return;
  if (target.closest('p') && !target.closest('tr[data-context-menu], .bento-card__header')) return;
  const host = target.closest('[data-context-menu]');
  if (!host) return;
  e.preventDefault();
  openScopedContextMenu(host, e.clientX, e.clientY);
});

function positionWithViewportFlip(wrapEl, menuEl, clientX, clientY) {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const w = menuEl.offsetWidth;
  const h = menuEl.offsetHeight;
  const margin = 8;
  const flipX = clientX + w + margin > vw && clientX - w >= margin;
  const flipY = clientY + h + margin > vh && clientY - h >= margin;
  const x = Math.max(margin, Math.min(vw - w - margin, flipX ? clientX - w : clientX));
  const y = Math.max(margin, Math.min(vh - h - margin, flipY ? clientY - h : clientY));
  wrapEl.style.left = `${x}px`;
  wrapEl.style.top = `${y}px`;
  menuEl.style.transformOrigin = `${flipY ? 'bottom' : 'top'} ${flipX ? 'right' : 'left'}`;
  const spring = createSpringAnimator({
    initialValue: 0,
    stiffness: 1800,
    damping: 0.92,
    onUpdate: (v) => {
      menuEl.style.opacity = String(Math.max(0, Math.min(1, v)));
      menuEl.style.transform = `scale(${(0.86 + 0.14 * v).toFixed(4)})`;
    },
  });
  spring.setTarget(1);
}
```
