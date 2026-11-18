# Personal Studio Profile (Hidden Layer 4 — Strictly Dormant Opt-In)

> [!CAUTION]
> **STRICTLY DORMANT BY DEFAULT — DO NOT LOAD UNLESS EXPLICITLY REQUESTED:**
> Layer 4 (`Personal Studio`) is a personal desktop customization tier that is **dormant by default**. Downstream AI agents MUST **NEVER** load `assets/tokens/md3e-studio.css`, `assets/tokens/md3e-studio.js`, `data-studio-profile="personal-studio"`, or run `--mode=personal-studio` unless the user **explicitly asks** for `Personal Studio`, `Layer 4`, or `--mode=personal-studio`.
>
> Standard M3E applications use **Layer 1 (Official M3E Core)** + **Layer 2 (Web Implementation Adaptations)**, and optionally **Layer 3 (`references/desktop-bento.md`, `references/expressive-tactics.md`)** when Bento product styling is requested. Layer 4 rules (`MD3E201`–`MD3E202`, inheriting `MD3E101`–`MD3E104`) live exclusively in the `CUSTOM` tier under `--mode=personal-studio` and are **never counted in `official_compliance.score`**.

---

## 1. Opt-In Activation & Token Contract

Activate Layer 4 on top of a Desktop Bento shell only when explicitly requested:

```html
<html lang="en" data-layout-profile="desktop-bento" data-studio-profile="personal-studio">
<head>
  <meta name="color-scheme" content="light dark">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block">
  <link rel="stylesheet" href="./tokens/md3e-tokens.css">
  <link rel="stylesheet" href="./tokens/md3e-blur.css">
  <link rel="stylesheet" href="./tokens/md3e-shapes.css">
  <link rel="stylesheet" href="./tokens/md3e-motion.css">
  <!-- Dormant Layer 4: link ONLY when Personal Studio / Layer 4 is explicitly requested -->
  <link rel="stylesheet" href="./tokens/md3e-studio.css">
</head>
```

`assets/tokens/md3e-studio.css` scopes all Personal Studio defaults (11 tunable parameters plus derived optical glass brightness/contrast and HDR headroom flags) strictly to `:root[data-studio-profile="personal-studio"]`:

| Token | Default | Range | Role |
|---|---|---|---|
| `--md-studio-blur-px` | `28px` | `8..48px` | Optical backdrop blur radius |
| `--md-studio-glass-alpha` | `56%` | `32..88%` | Translucent surface tint weight (`in oklab`) |
| `--md-studio-glass-saturate` | `190%` | `100..240%` | Optical backdrop saturation boost |
| `--md-studio-specular-alpha` | `18%` | `0..36%` | Top `1px` inset specular rim opacity (`md3e-blur.css`) |
| `--md-studio-hdr-boost` | `35%` | `0..100%` | Adaptive HDR wide-gamut optical headroom for micro-details (`data-studio-hdr="on"`) |
| `--md-studio-glass-brightness` | `1.10` | fixed / tuned | Optical glass brightness multiplier |
| `--md-studio-glass-contrast` | `1.05` | fixed / tuned | Optical glass contrast multiplier |
| `--md-studio-spring-stiffness` | `340` | `180..900` | Modal/workspace spatial spring stiffness (`~500ms` plush settle) |
| `--md-studio-spring-damping` | `0.76` | `0.58..1.00` | Spatial damping ratio (`synthesizeSpringLinearCss`) |
| `--md-studio-stagger-ms` | `32ms` | `12..60ms` | Bento entrance stagger step (`--stagger-step`) |
| `--md-studio-spotlight-px` | `260px` | `120..420px` | Pointer spotlight radial radius |
| `--md-studio-spotlight-alpha` | `12%` | `0..24%` | Pointer spotlight `in oklab` tint weight |
| `--md-studio-split-ratio` | `58%` | `32..68%` | Resizable telemetry/event split ratio |

---

## 2. High-Presence Optical Glass, Pure Dark Canvas & Adaptive HDR Optics

Layer 4 pairs Android 16-inspired optical window glass (`md3e-blur.css` under `[data-studio-profile="personal-studio"]`) with **pure unpolluted canvas surfaces** and **micro-scoped Adaptive HDR Optical Headroom**:

1. **Pure Dark Surface & Real Refraction Grounding (Zero Global Canvas Light-Bleed)**:
   - Dark-mode global `--md-sys-color-surface` MUST stay **100% clean and pure**. Never inject global viewport ambient light-bleed blobs or multi-gradient backdrop overlays (such as the legacy `.studio-caustic-field` pattern, which `MD3E201` actively bans as a dark-canvas pollutant).
   - Translucent glass refraction (`backdrop-filter: blur(...) saturate(...)`) is anchored strictly to **real underlying UI cards, dividers, charts, and `surface-container-*` panels** as well as **card-local micro-details** (`[data-studio-spotlight]::after`).
2. **Multi-Layer Optical Glass Filter (`md3e-blur.css`)**:
   - Upgrades `.md3e-blur-surface*` and accent blur chrome with `blur(var(--md-studio-blur-px)) saturate(var(--md-studio-glass-saturate)) brightness(var(--md-studio-glass-brightness)) contrast(var(--md-studio-glass-contrast))`.
   - Applies translucent tinting strictly via `color-mix(in oklab, var(--md3e-blur-tint) var(--md-studio-glass-alpha), transparent)` (**never** `color-mix(in oklch, ...)` on neutral/surface tokens — `MD3E018` Chromium powerless-hue bug) and tunes the top `1px` inset specular catchlight (`--md3e-specular-tint`, `--md3e-specular-alpha`) only on rectangular glass containers, leaving `.md3e-shape*` non-rectangular masks untouched (`MD3E023`).
3. **Adaptive HDR Optical Headroom (`data-studio-hdr="on"`)**:
   - When the display supports wide-gamut / HDR headroom (`@media (color-gamut: p3)` and `@media (dynamic-range: high)`), `:root[data-studio-profile="personal-studio"][data-studio-hdr="on"]` scales self-luminous micro-details via `--md-studio-hdr-boost`, `color(display-p3 ...)` / `color-mix(in oklab, ...)`, and `dynamic-range-limit: constrained-high`.
   - **Strict HDR Scope (`MD3E201`)**: Apply HDR headroom and `dynamic-range-limit: constrained-high` **ONLY** to:
     - Card pointer spotlight (`[data-studio-spotlight]::after`),
     - Top `1px` inset specular rim (`.md3e-blur-surface*`, `.studio-tuner-panel`, `.bento-vt-modal`),
     - Active navigation/segmented indicators (`.bento-pill-indicator`, `.bento-rail__indicator`, `.md3e-seg-indicator`),
     - Scrubber focus & active fill/thumb (`.studio-scrubber:focus-visible`, `.studio-scrubber::after`).
   - **NEVER** apply HDR boost or `dynamic-range-limit: constrained-high` to `body`, `p`, prose copy, or large background surfaces (keep those explicitly at `dynamic-range-limit: standard`).
4. **Mandatory Solid, SDR & High-Contrast Fallbacks (`MD3E022`, `MD3E201`)**:
   - `[data-studio-hdr="off"]`, `@media (prefers-reduced-transparency: reduce)`, `[data-reduced-transparency="true"]`, `@media (prefers-contrast: more)`, `[data-contrast="high"]`, and `@media (forced-colors: active)` MUST collapse `dynamic-range-limit` back to `standard` (reverting micro-details to standard SDR HCT roles), strip `backdrop-filter` / `-webkit-backdrop-filter` back to `none`, hide pointer spotlights, and restore opaque `--md3e-blur-fallback` (`surface-container-*`) backgrounds.

```css
:root[data-studio-profile="personal-studio"] {
  --md-studio-blur-px: 28px;
  --md-studio-glass-alpha: 56%;
  --md-studio-glass-saturate: 190%;
  --md-studio-specular-alpha: 18%;
  --md-studio-hdr-boost: 35%;
  --md-studio-glass-brightness: 1.10;
  --md-studio-glass-contrast: 1.05;
  --md-studio-spotlight-px: 260px;
  --md-studio-spotlight-alpha: 12%;
  --md-studio-split-ratio: 58%;
}

/* Keep global surfaces and body copy strictly SDR so dark --md-sys-color-surface stays pure */
:root[data-studio-profile="personal-studio"] body,
:root[data-studio-profile="personal-studio"] p {
  dynamic-range-limit: standard;
}

@supports ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  :root[data-studio-profile="personal-studio"] .studio-glass-panel {
    background-color: color-mix(
      in oklab,
      var(--md-sys-color-surface-container-high) var(--md-studio-glass-alpha),
      transparent
    );
    -webkit-backdrop-filter: blur(var(--md-studio-blur-px))
      saturate(var(--md-studio-glass-saturate))
      brightness(var(--md-studio-glass-brightness))
      contrast(var(--md-studio-glass-contrast));
    backdrop-filter: blur(var(--md-studio-blur-px))
      saturate(var(--md-studio-glass-saturate))
      brightness(var(--md-studio-glass-brightness))
      contrast(var(--md-studio-glass-contrast));
  }
}

/* Adaptive HDR Optical Headroom — strictly scoped to micro-details */
@media (color-gamut: p3) {
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-pill-indicator,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-rail__indicator,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .md3e-seg-indicator {
    background: color-mix(
      in oklab,
      color(display-p3 0.72 0.62 1) var(--md-studio-hdr-boost, 35%),
      var(--md-sys-color-secondary-container)
    );
  }
}

@media (dynamic-range: high) {
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] [data-studio-spotlight]::after,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .studio-tuner-panel,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-vt-modal,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-pill-indicator,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-rail__indicator,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .md3e-seg-indicator,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .studio-scrubber:focus-visible,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .studio-scrubber::after {
    dynamic-range-limit: constrained-high;
  }

  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .md3e-blur-surface,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .studio-tuner-panel,
  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .bento-vt-modal {
    --md3e-specular-tint: color-mix(
      in oklab,
      color(display-p3 1 1 1) var(--md-studio-hdr-boost, 35%),
      var(--md-sys-color-on-surface)
    );
    --md3e-specular-alpha: clamp(18%, calc(var(--md-studio-specular-alpha, 18%) + var(--md-studio-hdr-boost, 35%) * 0.25), 42%);
  }

  :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] .studio-scrubber:focus-visible {
    outline-color: color-mix(
      in oklab,
      color(display-p3 0.78 0.70 1) var(--md-studio-hdr-boost, 35%),
      var(--md-sys-color-secondary)
    );
  }
}

/* Automatic SDR, Reduced Transparency, High Contrast & Forced Colors fallbacks */
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] [data-studio-spotlight]::after,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .studio-tuner-panel,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .bento-vt-modal,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .bento-pill-indicator,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .bento-rail__indicator,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .md3e-seg-indicator,
:root[data-studio-profile="personal-studio"][data-studio-hdr="off"] .studio-scrubber:focus-visible {
  dynamic-range-limit: standard;
}

@media (prefers-reduced-transparency: reduce) {
  :root[data-studio-profile="personal-studio"] .studio-glass-panel {
    background-color: var(--md-sys-color-surface-container-high);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
    dynamic-range-limit: standard;
  }
}

[data-reduced-transparency="true"] .studio-glass-panel,
[data-contrast="high"] .studio-glass-panel {
  background-color: var(--md-sys-color-surface-container-high);
  -webkit-backdrop-filter: none;
  backdrop-filter: none;
  dynamic-range-limit: standard;
}

@media (prefers-contrast: more) {
  :root[data-studio-profile="personal-studio"] .studio-glass-panel {
    background-color: var(--md-sys-color-surface-container-high);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
    dynamic-range-limit: standard;
  }
}

@media (forced-colors: active) {
  .studio-glass-panel {
    background-color: Canvas;
    color: CanvasText;
    border: 1px solid CanvasText;
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
    dynamic-range-limit: standard;
  }
}
```

---

## 3. Horizontal Drag Scrubber & Human-AI Co-Tuning Protocol

Layer 4 introduces a **bidirectional Human-AI Co-Tuning loop** in `assets/tokens/md3e-studio.js` so users sculpt aesthetic feel directly through tactile horizontal scrubbers while AI agents read structured live intent and harmonize complementary parameters without overriding human choices.

### 3.1 `STUDIO_PARAM_SCHEMA` (11 Parameters Across 3 Groups)

| Group | Key | Range | Default | Unit | CSS Variable / Side Effect |
|---|---|---|---|---|---|
| **Optical Glass & HDR** | `blurPx` | `8..48` | `28` | `px` | `--md-studio-blur-px` |
| **Optical Glass & HDR** | `glassAlpha` | `32..88` | `56` | `%` | `--md-studio-glass-alpha` |
| **Optical Glass & HDR** | `glassSaturate` | `100..240` | `190` | `%` | `--md-studio-glass-saturate` |
| **Optical Glass & HDR** | `specularAlpha` | `0..36` | `18` | `%` | `--md-studio-specular-alpha` |
| **Optical Glass & HDR** | `hdrBoost` | `0..100` | `35` | `%` | `--md-studio-hdr-boost` (micro-detail P3/HDR optical headroom) |
| **Physics & Choreography** | `springStiffness` | `180..900` | `340` | `—` | Recomputes `--md-bento-motion-default-spatial*` via `synthesizeSpringLinearCss` |
| **Physics & Choreography** | `springDamping` | `0.58..1.00` | `0.76` | `—` | Recomputes `--md-bento-motion-default-spatial*` via `synthesizeSpringLinearCss` |
| **Physics & Choreography** | `staggerMs` | `12..60` | `32` | `ms` | `--md-studio-stagger-ms` |
| **Desktop Micro-Interactions** | `spotlightPx` | `120..420` | `260` | `px` | `--md-studio-spotlight-px` |
| **Desktop Micro-Interactions** | `spotlightAlpha` | `0..24` | `12` | `%` | `--md-studio-spotlight-alpha` |
| **Desktop Micro-Interactions** | `splitRatio` | `32..68` | `58` | `%` | `--md-studio-split-ratio` |

### 3.2 Horizontal Drag Scrubber & HDR Switch Contract

Each parameter control in `#studio-tuner-panel` is a focusable custom scrubber (`role="slider"`, `tabindex="0"`, `aria-label`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow`) with:
- **Horizontal pointer drag** (`pointerdown` + `setPointerCapture` + `pointermove`) mapped smoothly across the track range.
- **`Shift` precision mode (`0.25×` delta scaling)** for fine pixel/decimal adjustments during pointer drag.
- **Full keyboard & wheel support**: `ArrowLeft` / `ArrowRight` (and `ArrowDown` / `ArrowUp`) step by 1 unit (`Shift` for fine or `PageUp` / `PageDown` for 10× steps), `Home` / `End` jump to bounds, and pointer wheel adjusts fine increments.
- **Accessible target & focus**: `min-block-size: var(--md-sys-touch-target-min)` (`48px` via `::before` hit area if visually compact) and `3px solid var(--md-sys-color-secondary)` `:focus-visible` focus ring (`2px` offset).
- **HDR Capability Badge & Optical Switch (`#studio-hdr-badge`, `#btn-studio-hdr`)**: `detectHdrCapabilities()` inspects `matchMedia('(dynamic-range: high)')`, `matchMedia('(color-gamut: p3)')`, `CSS.supports('color', 'color(display-p3 1 1 1)')`, and `CSS.supports('dynamic-range-limit', 'constrained-high')` (safely guarded for Node/SSR), syncing `:root[data-studio-hdr="on|off"]`, `:root[data-studio-hdr-capable="hdr|p3|sdr"]`, `#studio-hdr-badge`, and `#btn-studio-hdr` (`role="switch"`, `aria-checked`).

```html
<section id="studio-tuner-panel" class="studio-tuner-panel md3e-blur-surface-high md3e-blur--lg" aria-label="Personal Studio Co-Tuner">
  <div class="studio-tuner-header">
    <span id="studio-intent-badge">Balanced Studio</span>
    <span id="studio-hdr-badge">HDR Ready</span>
    <button type="button" role="switch" id="btn-studio-hdr" aria-checked="true" aria-label="Adaptive HDR optical headroom">HDR</button>
    <div class="studio-tuner-actions">
      <button type="button" class="md3e-btn md3e-btn--tonal md3e-btn--s" id="btn-studio-harmonize">Auto-Harmonize</button>
      <button type="button" class="md3e-btn md3e-btn--outlined md3e-btn--s" id="btn-studio-preview">Preview Patch</button>
      <button type="button" class="md3e-btn md3e-btn--outlined md3e-btn--s" id="btn-studio-copy-css">Copy CSS</button>
      <button type="button" class="md3e-btn md3e-btn--text md3e-btn--s" id="btn-studio-reset">Reset</button>
    </div>
  </div>

  <div
    class="studio-scrubber"
    role="slider"
    tabindex="0"
    data-scrubber-key="glassAlpha"
    data-scrubber-source="human"
    aria-label="Glass surface opacity"
    aria-valuemin="32"
    aria-valuemax="88"
    aria-valuenow="56"
  >
    <span class="studio-scrubber__name">Glass Alpha</span>
    <span class="studio-scrubber__val tabular-nums">56%</span>
  </div>

  <div
    class="studio-scrubber"
    role="slider"
    tabindex="0"
    data-scrubber-key="hdrBoost"
    data-scrubber-source="default"
    aria-label="Adaptive HDR optical headroom boost"
    aria-valuemin="0"
    aria-valuemax="100"
    aria-valuenow="35"
  >
    <span class="studio-scrubber__name">HDR Headroom</span>
    <span class="studio-scrubber__val tabular-nums">35%</span>
  </div>

  <pre id="studio-css-output" aria-label="Generated Personal Studio CSS patch"></pre>
  <script id="md3e-studio-telemetry" type="application/json">{
    "profile": "personal-studio",
    "inferredIntent": "balanced-studio",
    "humanModifiedKeys": [],
    "humanDeltas": {},
    "values": { "glassAlpha": 56, "hdrBoost": 35, "springStiffness": 340 },
    "hdr": { "dynamicRangeHigh": true, "colorGamutP3": true, "enabled": true, "effective": true, "boostPct": 35 }
  }</script>
</section>
```

### 3.3 Bidirectional Human-AI Co-Tuning Loop (`window.__MD3E_TUNER__`)

1. **Human Primary Input (`source: 'human'`)**: The user drags 1–2 scrubbers manually (for example, lowers `glassAlpha` from `56%` to `44%`, adjusts `hdrBoost`, or drops `springStiffness` from `340` to `260`). `md3e-studio.js` pins those keys as `source === 'human'`.
2. **Synchronous Telemetry Emission (`#md3e-studio-telemetry` & `window.__MD3E_TUNER__`)**:
   - On every update, `initPersonalStudio()` serializes live state into `<script id="md3e-studio-telemetry" type="application/json">` with `values`, `sources`, `humanModifiedKeys`, `humanDeltas`, `inferredIntent` (`frosted-crystal`, `silk-cinematic`, `crisp-utility`, `tactile-focus`, or `balanced-studio`), and `hdr` (`{ dynamicRangeHigh, colorGamutP3, cssDisplayP3, cssDynamicRangeLimit, effectiveHdr, enabled, effective, boostPct }`).
   - Simultaneously, `window.__MD3E_TUNER__` (with `window.__MD3E_STUDIO__ = window.__MD3E_TUNER__` maintained as an identical alias) exposes `{ getState, setParam, harmonize, reset, exportCss, getHdrCapabilities, isHdrEnabled, setHdrEnabled, applyUrlOrStorage, statusCapsule, animateTabularCounter, refreshBindings, destroy }` so an IDE agent or browser harness can inspect HDR capability, toggle optical headroom, read live deltas, and harmonize parameters cleanly.
3. **Coupled AI / Algorithmic Harmonization (`computeHarmonizedParams(state)` / `#btn-studio-harmonize`)**:
   - Reads `humanModifiedKeys`, `humanDeltas`, and `inferredIntent` from `#md3e-studio-telemetry` (or `getState()`).
   - Computes coupled complementary adjustments across **untouched** parameters while **locking and preserving every `human`-pinned key** untouched:
     - *Example (Optical & HDR coupling)*: Lowering `glassAlpha` or raising `blurPx` boosts `glassSaturate`, raises `specularAlpha` to preserve edge definition, and tunes `hdrBoost` / `spotlightAlpha` proportionally.
     - *Example (Physics coupling)*: Softening `springStiffness` adjusts `springDamping` and tunes `--md-studio-stagger-ms` proportionally so card staggers match the slower organic settle time.
4. **Live Preview & Exportable CSS Patch (`#studio-css-output`)**:
   - `formatStudioCssPatch(values)` emits a ready-to-paste `:root[data-studio-profile="personal-studio"] { ... }` CSS block inside `#studio-css-output` (including `--md-studio-hdr-boost` and `data-studio-hdr` state) for live preview (`#btn-studio-preview`), clipboard export (`#btn-studio-copy-css`), or reset (`#btn-studio-reset`).

```js
// Programmatic AI Co-Tuning & HDR control via window.__MD3E_TUNER__ (alias: window.__MD3E_STUDIO__)
const tuner = window.__MD3E_TUNER__;
const caps = tuner.getHdrCapabilities();
// caps -> { dynamicRangeHigh, colorGamutP3, cssDisplayP3, cssDynamicRangeLimit, effectiveHdr }

tuner.setHdrEnabled(caps.effectiveHdr);
const result = tuner.harmonize();
// Human-pinned keys (e.g. glassAlpha) stay locked; untouched keys (blurPx, glassSaturate, specularAlpha, hdrBoost)
// update with source: "ai", and #studio-css-output reflects the clean diff.
const cssPatch = tuner.exportCss();
```

---

## 4. Desktop Ergonomics, Live DOM FLIP Modal Choreography & Frame-Rate Engine

Layer 4 adds desktop-first ergonomics built strictly on native HTML standards, `in oklab` color math, and interruptible refresh-rate-invariant motion:

### 4.1 Why Frosted Modals Must Use Live DOM FLIP (Never `document.startViewTransition()`)

Never wrap a `backdrop-filter` modal (`#bento-vt-modal` + `#bento-vt-backdrop`) in `document.startViewTransition()`:
1. **Static Bitmap Isolation**: `startViewTransition()` rasterizes the source card and target modal into **static frozen bitmap snapshots** (`::view-transition-old/new`), which **cannot sample live pixels through `backdrop-filter`** mid-flight. During opening, the modal composites as an opaque washed-out grey rectangle and **jumps abruptly to dark translucent glass** when the View Transition tears down and hands back to live DOM.
2. **Asymmetric Scrim & Modal Tear-Down**: Running separate View Transition groups (such as a `220ms` backdrop scrim vs a `500ms` modal panel) strips backdrop blur at the end of close and produces a **1-frame scrim re-flash**.
3. **Zero Mid-Flight Interruptibility**: Static View Transition snapshots lock layout state until animation completion rather than reversing cleanly from live velocity.

**The Live DOM FLIP + Dual `createSpringAnimator` Solution**:
- Keep `#bento-vt-backdrop` (`z-index: 900`, above bottom toolbars) and `#bento-vt-modal` (`z-index: 910`) as **live DOM nodes on every single frame** of open and close.
- **Never animate `transform: scale()` on a `backdrop-filter` container** (which shifts Chromium's sampled blur kernel and causes a settle jump). Instead, set `position: fixed; margin: 0;` and interpolate live viewport geometry (`left`, `top`, `width`, `height`, `border-radius`) between `#event-stream-card.getBoundingClientRect()` and the centered resting modal bounds, plus subtle inner-content opacity/offset — keeping `backdrop-filter` **1:1 pixel-accurate on every frame** with **zero end-of-animation color jump**.
- Drive `#bento-vt-backdrop` with a second synchronized `createSpringAnimator` (`scrimSpring`) updating `--scrim-progress` (`0 -> 1`) mapped continuously to `opacity` and `backdrop-filter: blur(calc(var(--scrim-progress) * 14px))`, setting `hidden = true` **only** when `target === 0` and settled (`p <= 0.002`) — eliminating Frame-1 blur pop and close-end scrim re-flash completely.
- **100% Mid-Flight Interruptibility (150ms Reversal)**: Never place `inert` on `#bento-vt-backdrop` or use an animation mutex lock. Pressing `Escape`, clicking `#bento-vt-backdrop`, or clicking `#btn-vt-close` at **any millisecond mid-open** (for example, `150ms`) immediately calls `modalSpring.setTarget(0, { onRest })` and `scrimSpring.setTarget(0, { onRest })`, preserving exact live geometry and instantaneous velocity (`createSpringAnimator` cancels any superseded `onRest` callback from the earlier target and exposes `.getTarget()`, `.getValue()`, `.getVelocity()`, `.isAnimating()`, `.jump(value)`), smoothly reversing back into `#event-stream-card` and returning focus to `#btn-vt-expand`. Clicking `#btn-vt-expand` mid-close immediately reverses back to `1`.
- **Every Interactive Transition Interruptible**: `#studio-tuner-panel` (live spring slide/opacity drawer), `#studio-cmd-dialog` (native `<dialog>` intercepting `cancel` / backdrop outside-click to spring-reverse cleanly without `<input type="search">` swallowing the first `Escape`), `switchBentoView`, `#bento-rail`, `#bento-profile-group`, and `#bento-context-menu` all retarget cleanly mid-flight with zero locked timeouts.

```js
// Dual createSpringAnimator Live DOM FLIP controller (zero startViewTransition bitmap jump)
const modalSpring = createSpringAnimator({
  initialValue: 0,
  stiffness: 340,
  damping: 0.76,
  precision: 0.001,
  onUpdate(p) {
    // Interpolate live fixed left/top/width/height/border-radius (never transform: scale() on blur host)
    applyLiveModalGeometry(p);
  },
});

const scrimSpring = createSpringAnimator({
  initialValue: 0,
  stiffness: 1600,
  damping: 1.0,
  precision: 0.002,
  onUpdate(p) {
    vtBackdrop.style.setProperty('--scrim-progress', p.toFixed(4));
  },
});

function openVtModal() {
  vtBackdrop.hidden = false;
  vtModal.hidden = false;
  modalSpring.setTarget(1); // Cancels any stale close onRest automatically; preserves live velocity
  scrimSpring.setTarget(1);
}

function closeVtModal() {
  scrimSpring.setTarget(0, {
    onRest() { vtBackdrop.hidden = true; },
  });
  modalSpring.setTarget(0, {
    onRest() {
      vtModal.hidden = true;
      btnVtExpand.focus();
    },
  });
}
```

### 4.2 Desktop Controls, Scrollbars & Refresh-Rate Engine

1. **`Ctrl+K` Command Palette (`<dialog id="studio-cmd-dialog" closedby="any">`)**:
   - Uses native `<dialog closedby="any">` for light-dismiss backdrop click and `Escape` restoration — **never** add redundant `role="dialog"` or `aria-modal` (`MD3E020` / `MD3E202`).
   - Locks background scroll leakage with `dialog.studio-cmd-dialog:modal { overscroll-behavior: contain; }` and `dialog.studio-cmd-dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }` (never locking scroll on `html`/`body`).
   - Provides live fuzzy filtering across workspace commands (`Theme`, `Seed`, `Rail`, `Tuner`, `Harmonize`, `Expand`, view filters) without intercepting the first `Escape` keystroke.
2. **Pointer Spotlight (`[data-studio-spotlight]`, `in oklab`)**:
   - A `requestAnimationFrame`-coalesced pointermove listener sets `--studio-mx` and `--studio-my` on `[data-studio-spotlight]` hosts, painting a soft card-local radial highlight sized by `--md-studio-spotlight-px` and mixed via `color-mix(in oklab, var(--md-sys-color-primary) var(--md-studio-spotlight-alpha), transparent)`.
3. **Thin Desktop Scrollbars (`>= 3:1`) + Soft-Edge Scroll Fades (`.studio-scroll-fade`)**:
   - Applies `scrollbar-width: thin` with `scrollbar-color: var(--md3e-scrollbar-thumb) var(--md3e-scrollbar-track)` (`--md-sys-color-outline` over `--md-sys-color-surface-container-low`, `>= 3:1` thumb/track contrast; plus `@supports not (scrollbar-color: auto)` WebKit fallback and `@media (pointer: coarse)` / `prefers-contrast: more` `scrollbar-width: auto` fallback), paired with `.studio-scroll-fade` `-webkit-mask-image` / `mask-image` soft top/bottom edges toggled dynamically by `[data-scroll-edges="top|bottom|both|none"]`.
4. **Spring-Resetting Split Handle (`#bento-split-handle`)**:
   - `<div id="bento-split-handle" role="separator" aria-orientation="vertical" tabindex="0" aria-valuemin="32" aria-valuemax="68" aria-valuenow="58">` resizes the telemetry/event split across `32%..68%` (`--md-studio-split-ratio`); **double-click or `Enter`** invokes `createSpringAnimator` to bounce smoothly back to `58%`.
5. **Non-Occluding Titlebar Status Capsule (`#titlebar-status-pill`)**:
   - A debounced `role="status" aria-live="polite"` capsule embedded in the `44px` frameless titlebar (paired with a `tabular-nums` spring counter helper), keeping operational status visible without floating over bottom toolbars or content.
6. **`dt`-Invariant `document.hidden`-Only Pause Policy**:
   - `md3e-spring.js`, `md3e-morph.js`, and continuous wavy/canvas animations compute clamped `performance.now()` delta (`dt` in `0.0005s..0.05s`, with a `1/60` frame-1 baseline) so `60Hz`, `120Hz`, `144Hz`, and `240Hz` panels animate at identical physical speed (`synthesizeSpringLinearCss(340, 0.76, 36)` settles at `500ms`, `2.54%` peak overshoot).
   - Animation loops subscribe to `document` `visibilitychange` and pause **only** when `document.hidden === true`, rebasing `lastTs` seamlessly upon returning to the foreground — **never** stalling background wavy progress bars or 7-shape loaders while frosted blur, drawers, or dialogs are open in the foreground.

```html
<header class="bento-titlebar">
  <span class="studio-titlebar-status" id="titlebar-status-pill" role="status" aria-live="polite">Balanced Studio · 500ms</span>
  <button type="button" class="md3e-btn md3e-btn--tonal md3e-btn--s" id="btn-studio-cmdk">
    <span class="material-symbols-outlined" aria-hidden="true">search</span>
    Command Palette (Ctrl+K)
  </button>
</header>

<div class="studio-split-handle" id="bento-split-handle" role="separator" aria-orientation="vertical" aria-label="Resize telemetry and event panes" aria-valuemin="32" aria-valuemax="68" aria-valuenow="58" tabindex="0"></div>

<dialog class="studio-cmd-dialog md3e-blur-surface-highest md3e-blur--xl" id="studio-cmd-dialog" aria-labelledby="studio-cmd-title" closedby="any">
  <div class="studio-cmd-dialog__head">
    <h2 id="studio-cmd-title">Studio Command Palette</h2>
    <button type="button" class="md3e-icon-btn" id="btn-studio-cmd-close" aria-label="Close command palette">
      <span class="material-symbols-outlined" aria-hidden="true">close</span>
    </button>
  </div>
  <input type="search" id="studio-cmd-input" aria-label="Filter studio commands" placeholder="Type a command...">
</dialog>
```

```css
.studio-scrubber {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-block-size: var(--md-sys-touch-target-min);
  padding-inline: var(--md-sys-spacing-4);
  border-radius: var(--md-sys-shape-corner-large);
  background: var(--md-sys-color-surface-container-highest);
  color: var(--md-sys-color-on-surface);
  cursor: ew-resize;
  transition: background-color var(--md-sys-motion-fast-effects);
}

.studio-scrubber::before {
  content: "";
  position: absolute;
  inset: 0;
  min-inline-size: var(--md-sys-touch-target-min);
  min-block-size: var(--md-sys-touch-target-min);
}

.studio-scrubber:hover {
  background: color-mix(in oklab, var(--md-sys-color-on-surface) 8%, var(--md-sys-color-surface-container-highest));
}

.studio-scrubber:focus-visible,
.studio-split-handle:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.studio-split-handle {
  position: relative;
  min-inline-size: var(--md-sys-touch-target-min);
  min-block-size: var(--md-sys-touch-target-min);
  cursor: col-resize;
}

dialog.studio-cmd-dialog {
  border: none;
  padding: var(--md-sys-spacing-5);
  border-radius: var(--md-sys-shape-corner-extra-large);
  color: var(--md-sys-color-on-surface);
}

dialog.studio-cmd-dialog:modal {
  overscroll-behavior: contain;
}

dialog.studio-cmd-dialog::backdrop {
  background: color-mix(in oklab, var(--md-sys-color-scrim) 44%, transparent);
  overflow: hidden;
  overscroll-behavior: contain;
}

[data-studio-spotlight] {
  background-image: radial-gradient(
    var(--md-studio-spotlight-px, 260px) circle at var(--studio-mx, 50%) var(--studio-my, 50%),
    color-mix(in oklab, var(--md-sys-color-primary) var(--md-studio-spotlight-alpha, 12%), transparent),
    transparent 70%
  );
}

.studio-scroll-fade {
  --md3e-scrollbar-thumb: var(--md-sys-color-outline);
  --md3e-scrollbar-track: var(--md-sys-color-surface-container-low);
  scrollbar-width: thin;
  scrollbar-color: var(--md3e-scrollbar-thumb) var(--md3e-scrollbar-track);
}

.studio-scroll-fade[data-scroll-edges="both"] {
  -webkit-mask-image: linear-gradient(180deg, transparent, var(--md-sys-color-scrim) 16px, var(--md-sys-color-scrim) calc(100% - 16px), transparent);
  mask-image: linear-gradient(180deg, transparent, var(--md-sys-color-scrim) 16px, var(--md-sys-color-scrim) calc(100% - 16px), transparent);
}

@media (prefers-reduced-motion: reduce) {
  .studio-scrubber {
    transition: none;
  }
}

@media (forced-colors: active) {
  .studio-scrubber,
  dialog.studio-cmd-dialog {
    border: 1px solid CanvasText;
  }
}
```

---

## 5. Auditing Layer 4 (`--mode=personal-studio`)

Only run `--mode=personal-studio` when explicitly verifying a Personal Studio deliverable:

```bash
python scripts/audit_md3e.py assets/starter/desktop-bento.html --mode=personal-studio --fail-on=warning
```

- `--mode=personal-studio` inherits Layer 3 Bento checks (`MD3E101`–`MD3E104`, `CUSTOM`) plus Layer 4 checks (`MD3E201` bans global `.studio-caustic-field` ambient light-bleed blobs, verifies optical glass + reduced-transparency fallback hygiene, and enforces micro-scoped HDR hygiene without `body`/`p` boost + SDR/RT/HC fallbacks; `MD3E202` verifies `<dialog>` modal `overscroll-behavior: contain`, zero redundant `role="dialog"` / `aria-modal`, and focusable controls — `CUSTOM` unless a core WCAG/contrast/focus `ERROR` triggers).
- `--mode=strict` remains 100% isolated from `MD3E101+` and `MD3E201+`, and `CUSTOM` findings never lower `official_compliance.score`.
