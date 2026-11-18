# Desktop Bento Dashboard Override Layer (Opt-In)

> [!IMPORTANT]
> **Decoupled Override Architecture (`--mode=desktop-bento`)**:
> This document defines an **opt-in desktop workstation & telemetry dashboard layer** (`data-layout-profile="desktop-bento"`). Keep it cleanly isolated from default mobile/universal M3E apps (`references/layout.md`, `--mode=strict`). Audit Bento views explicitly with:
> `python scripts/audit_md3e.py <path> --mode=desktop-bento --fail-on warn`

Desktop Bento dashboards trade generous mobile margins for ultra-clear tonal nesting, dual-tier ergonomics (compact data inspection + chunky primary controls), borderless geometry, and sharp high-stiffness desktop springs.

---

## 1. Window Chrome, Navigation Rail & Bento Grid

- **Frameless Integrated Titlebar (`44px`)**: Blend seamlessly with `--md-sys-color-surface` (no `1px` bottom separator line). Reserve optional overlay insets via `env(titlebar-area-height, 44px)`. Place breadcrumb/context pills, compact workspace search (`:focus-within` ring, `outline: 2px solid transparent`), theme/seed switcher, and window action controls with `::before` `48px` hit targets.
- **Ultra-Narrow Navigation Rail (`64px`)**: Persistent icon-only rail (`64px` inline-size, `48×48px` clickable destinations, active `secondary-container` pill, roving arrow-key navigation + `aria-label` on every destination).
- **12-Column Asymmetric Bento Grid**: Use CSS Grid (`grid-template-columns: repeat(12, minmax(0, 1fr))`, `gap: var(--md-sys-spacing-4)`) collapsing cleanly at `< 1200px` (`8` cols) and `< 840px` (`4` cols), plus `container-type: inline-size` on wide telemetry cards.

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

  /* Desktop high-stiffness short springs (150ms-250ms) */
  --md-bento-motion-fast-effects: 150ms cubic-bezier(0.34, 0.88, 0.34, 1);
  --md-bento-motion-default-effects: 200ms cubic-bezier(0.34, 0.80, 0.34, 1);
  --md-bento-motion-fast-spatial: 180ms linear(0, 0.25 18%, 1.07 42%, 0.99 66%, 1);
  --md-bento-motion-default-spatial: 240ms linear(0, 0.28 19%, 1.05 44%, 0.99 68%, 1);
}
```

---

## 3. Visual Choreography: Borderless Tonal Nesting & 80/20 Hero Budget

1. **Zero `1px` Card Borders & Zero Rectangular `box-shadow`s**:
   - **NEVER** draw `1px solid` outlines or `box-shadow` elevation on Bento cards, tiles, or inner wells (checked as `MD3E101` in `--mode=desktop-bento`).
   - Only keyboard `:focus-visible` rings (`3px solid var(--md-sys-color-secondary)`) and `@media (forced-colors: active)` system-color fallbacks (`1px solid CanvasText`) may draw strokes.
2. **4+ Surface Container Luminance Nesting Tiers**:
   - Separate hierarchy purely via `surface` -> `surface-container-lowest` -> `surface-container-low` -> `surface-container` -> `surface-container-high` -> `surface-container-highest` (`MD3E102` requires `>= 4` distinct container tiers).
3. **Concentric Corner Radius Step-Down (`28px` / `16px`)**:
   - Outer `.bento-card` uses `--md-sys-shape-corner-extra-large` (`28px`) with `12px` (`--md-sys-spacing-3`) or `16px` padding so nested `.bento-well` containers step down cleanly to `--md-sys-shape-corner-large` (`16px`) (`MD3E103`).
4. **80 / 20 Bento Expressive Budget**:
   - **~80% Orthogonal Grid**: Clean, aligned telemetry tables, log streams, tonal progress bars, and tactile controls with zero decorative clutter.
   - **1–2 Hero Status Cards**: Must combine three signature expressive anchors (`MD3E104`):
     1. Decorative **fluid sine-wave background motif** (`<svg aria-hidden="true">`, subtle tonal opacity via `in oklab`),
     2. Interactive **real-time morphing `MaterialShapes` CTA button** powered by `md3e-morph.js` + `md3e-spring.js` and shadowed strictly via wrapper **`filter: drop-shadow(...)`** (`MD3E023`),
     3. **Edge-bleed axis-less micro Sparkline** (`<svg>` flush against the bottom & inline edges of the Hero card, zero gridlines or tick numbers).

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

## 4. Desktop Micro-Interactions & Safety Bans

1. **Mouse `:hover` + Keyboard `:focus-visible`**: Every interactive tile, table row hover state, switch, segmented item, and shape CTA must implement subtle tonal hover overlays (`8%` via `color-mix(in oklab, ...)`) AND unmistakable `3px` `--md-sys-color-secondary` `:focus-visible` focus rings (`--md-sys-focus-ring-offset: 2px`).
2. **Tight High-Stiffness Desktop Springs (`150ms–250ms`)**: Avoid sloppy mobile sluggishness (`460ms+`) on desktop clicks and toggles. Configure JS morphers with `{ stiffness: 1500, damping: 0.88 }` (`~180ms` settling) and use `--md-bento-motion-*` tokens for CSS interactions.
3. **Never Pair `9999px` (`corner-full`) With `border-radius` Spring Morphs (`MD3E019` error)**: Any pill button transitioning `border-radius` on `:active` under an underdamped `linear()` spring (`1.07` overshoot, such as `--md-bento-motion-fast-spatial`) will evaluate `9999px + 1.07 * (16px - 9999px) = -682.8px -> 0px`, flashing a razor-sharp rectangle mid-click! Always bind resting radii to `calc(height / 2)` (`24px` on `48px` CTAs -> `12px`, `18px` on `36px` pills -> `8px`) so overshoot stays strictly positive across all frames.
4. **Shape Drop Shadows**: Never put `box-shadow` directly on `.md3e-shape*`, `mask-image`, or morphing `<svg>` shapes (`MD3E023` error in `desktop-bento`). Always wrap the button/shape container in `filter: drop-shadow(...)`.
5. **Ban `in oklch` on Neutral Color Mixing**: Never use `color-mix(in oklch, ...)` on `surface*`, `on-surface*`, `outline*`, `shadow`, `scrim`, or `currentColor` (`MD3E018` **error** in `desktop-bento` mode) to avoid Chromium's powerless-hue pink/red shift; always use **`in oklab`**.
6. **Reference Implementation**: See targeted ranges of [`assets/starter/desktop-bento.html`](../assets/starter/desktop-bento.html) (never read in full into context; inspect specific component blocks only).
