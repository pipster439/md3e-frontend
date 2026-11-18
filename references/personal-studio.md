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

`assets/tokens/md3e-studio.css` scopes all 12 personal-studio defaults strictly to `:root[data-studio-profile="personal-studio"]`:

| Token | Default | Range | Role |
|---|---|---|---|
| `--md-studio-blur-px` | `28px` | `8..48px` | Optical backdrop blur radius |
| `--md-studio-glass-alpha` | `56%` | `32..88%` | Translucent surface tint weight (`in oklab`) |
| `--md-studio-glass-saturate` | `190%` | `100..240%` | Optical backdrop saturation boost |
| `--md-studio-specular-alpha` | `18%` | `0..36%` | Top inner specular rim opacity (`md3e-blur.css`) |
| `--md-studio-glass-brightness` | `1.10` | fixed / tuned | Optical glass brightness multiplier |
| `--md-studio-glass-contrast` | `1.05` | fixed / tuned | Optical glass contrast multiplier |
| `--md-studio-spring-stiffness` | `340` | `180..900` | Modal/workspace spatial spring stiffness (`~500ms` plush settle) |
| `--md-studio-spring-damping` | `0.76` | `0.58..1.00` | Spatial damping ratio (`synthesizeSpringLinearCss`) |
| `--md-studio-stagger-ms` | `32ms` | `12..60ms` | Bento entrance stagger step (`--stagger-step`) |
| `--md-studio-spotlight-px` | `260px` | `120..420px` | Pointer spotlight radial radius |
| `--md-studio-spotlight-alpha` | `12%` | `0..24%` | Pointer spotlight `in oklab` tint weight |
| `--md-studio-split-ratio` | `58%` | `32..68%` | Resizable telemetry/event split ratio |

---

## 2. High-Presence Optical Glass & Chromatic Caustic Field

Layer 4 pairs Android 16-inspired optical window glass (`md3e-blur.css` under `[data-studio-profile="personal-studio"]`) with a subtle ambient `oklab` caustic light field so translucent panels actually have rich tonal material behind them to refract:

1. **Multi-Layer Optical Glass Filter (`md3e-blur.css`)**:
   - Upgrades `.md3e-blur-surface*` and accent blur chrome with `blur(var(--md-studio-blur-px)) saturate(var(--md-studio-glass-saturate)) brightness(var(--md-studio-glass-brightness)) contrast(var(--md-studio-glass-contrast))`.
   - Applies translucent tinting strictly via `color-mix(in oklab, var(--md3e-blur-tint) var(--md-studio-glass-alpha), transparent)` (never `in oklch` on neutral surfaces — `MD3E018`) and adds a crisp top specular rim (`--md3e-specular-tint`, `--md3e-specular-alpha`) only on rectangular glass containers, leaving `.md3e-shape*` non-rectangular masks untouched (`MD3E023`).
2. **Ambient Chromatic Caustic Field (`.studio-caustic-field`)**:
   - `<div class="studio-caustic-field" aria-hidden="true"></div>` sits behind the Bento workspace (`pointer-events: none`) and projects soft `oklab` radial pools derived from `--md-sys-color-primary`, `--md-sys-color-tertiary`, and `--md-sys-color-secondary`.
3. **Mandatory Solid & High-Contrast Fallbacks (`MD3E022`, `MD3E201`)**:
   - Both `@media (prefers-reduced-transparency: reduce)` and `[data-reduced-transparency="true"]` (as well as `@media (prefers-contrast: more)`, `[data-contrast="high"]`, and `@media (forced-colors: active)`) MUST strip `backdrop-filter` / `-webkit-backdrop-filter` back to `none`, restore opaque `--md3e-blur-fallback` (`surface-container-*`) backgrounds, and hide `.studio-caustic-field`.

```css
:root[data-studio-profile="personal-studio"] {
  --md-studio-blur-px: 28px;
  --md-studio-glass-alpha: 56%;
  --md-studio-glass-saturate: 190%;
  --md-studio-specular-alpha: 18%;
  --md-studio-glass-brightness: 1.10;
  --md-studio-glass-contrast: 1.05;
  --md-studio-spotlight-px: 260px;
  --md-studio-spotlight-alpha: 12%;
  --md-studio-split-ratio: 58%;
}

.studio-caustic-field {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    radial-gradient(640px circle at 18% 22%, color-mix(in oklab, var(--md-sys-color-primary) 16%, transparent), transparent 64%),
    radial-gradient(560px circle at 82% 28%, color-mix(in oklab, var(--md-sys-color-tertiary) 14%, transparent), transparent 62%),
    radial-gradient(620px circle at 54% 84%, color-mix(in oklab, var(--md-sys-color-secondary) 12%, transparent), transparent 66%);
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

@media (prefers-reduced-transparency: reduce) {
  .studio-caustic-field {
    display: none;
  }
  :root[data-studio-profile="personal-studio"] .studio-glass-panel {
    background-color: var(--md-sys-color-surface-container-high);
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}

[data-reduced-transparency="true"] .studio-caustic-field {
  display: none;
}

[data-reduced-transparency="true"] .studio-glass-panel {
  background-color: var(--md-sys-color-surface-container-high);
  -webkit-backdrop-filter: none;
  backdrop-filter: none;
}

@media (forced-colors: active) {
  .studio-caustic-field {
    display: none;
  }
  .studio-glass-panel {
    background-color: Canvas;
    color: CanvasText;
    border: 1px solid CanvasText;
    -webkit-backdrop-filter: none;
    backdrop-filter: none;
  }
}
```

---

## 3. Horizontal Drag Scrubber & Human-AI Co-Tuning Protocol

Layer 4 introduces a **bidirectional Human-AI Co-Tuning loop** in `assets/tokens/md3e-studio.js` so users sculpt aesthetic feel directly through tactile horizontal scrubbers while AI agents read structured live intent and harmonize complementary parameters without overriding human choices.

### 3.1 `STUDIO_PARAM_SCHEMA` (10 Parameters Across 3 Groups)

| Group | Key | Range | Default | Unit | CSS Variable / Side Effect |
|---|---|---|---|---|---|
| **Optical Glass** | `blurPx` | `8..48` | `28` | `px` | `--md-studio-blur-px` |
| **Optical Glass** | `glassAlpha` | `32..88` | `56` | `%` | `--md-studio-glass-alpha` |
| **Optical Glass** | `glassSaturate` | `100..240` | `190` | `%` | `--md-studio-glass-saturate` |
| **Optical Glass** | `specularAlpha` | `0..36` | `18` | `%` | `--md-studio-specular-alpha` |
| **Physics & Choreography** | `springStiffness` | `180..900` | `340` | `—` | Recomputes `--md-bento-motion-default-spatial*` via `synthesizeSpringLinearCss` |
| **Physics & Choreography** | `springDamping` | `0.58..1.00` | `0.76` | `—` | Recomputes `--md-bento-motion-default-spatial*` via `synthesizeSpringLinearCss` |
| **Physics & Choreography** | `staggerMs` | `12..60` | `32` | `ms` | `--md-studio-stagger-ms` |
| **Desktop Micro-Interactions** | `spotlightPx` | `120..420` | `260` | `px` | `--md-studio-spotlight-px` |
| **Desktop Micro-Interactions** | `spotlightAlpha` | `0..24` | `12` | `%` | `--md-studio-spotlight-alpha` |
| **Desktop Micro-Interactions** | `splitRatio` | `32..68` | `58` | `%` | `--md-studio-split-ratio` |

### 3.2 Horizontal Drag Scrubber Contract (`.studio-scrubber[role="slider"]`)

Each parameter control in `#studio-tuner-panel` is a focusable custom scrubber (`role="slider"`, `tabindex="0"`, `aria-label`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow`) with:
- **Horizontal pointer drag** (`pointerdown` + `setPointerCapture` + `pointermove`) mapped smoothly across the track range.
- **`Shift` precision mode (`0.25×` delta scaling)** for fine pixel/decimal adjustments during pointer drag.
- **Full keyboard & wheel support**: `ArrowLeft` / `ArrowRight` (and `ArrowDown` / `ArrowUp`) step by 1 unit (`Shift` for fine or `PageUp` / `PageDown` for 10× steps), `Home` / `End` jump to bounds, and pointer wheel adjusts fine increments.
- **Accessible target & focus**: `min-block-size: var(--md-sys-touch-target-min)` (`48px` via `::before` hit area if visually compact) and `3px solid var(--md-sys-color-secondary)` `:focus-visible` focus ring (`2px` offset).

```html
<section id="studio-tuner-panel" class="studio-tuner-panel md3e-blur-surface-high md3e-blur--lg" aria-label="Personal Studio Co-Tuner">
  <div class="studio-tuner-header">
    <span id="studio-intent-badge">Balanced Studio</span>
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

  <pre id="studio-css-output" aria-label="Generated Personal Studio CSS patch"></pre>
  <script id="md3e-studio-telemetry" type="application/json">{
    "profile": "personal-studio",
    "inferredIntent": "balanced-studio",
    "humanModifiedKeys": [],
    "humanDeltas": {},
    "values": { "glassAlpha": 56, "springStiffness": 340 }
  }</script>
</section>
```

### 3.3 Bidirectional Human-AI Co-Tuning Loop

1. **Human Primary Input (`source: 'human'`)**: The user drags 1–2 scrubbers manually (for example, lowers `glassAlpha` from `56%` to `44%`, or drops `springStiffness` from `340` to `260`). `md3e-studio.js` pins those keys as `source === 'human'`.
2. **Synchronous Telemetry Emission (`#md3e-studio-telemetry` & `window.__MD3E_STUDIO__`)**:
   - On every update, `initPersonalStudio()` serializes live state into `<script id="md3e-studio-telemetry" type="application/json">` with `values`, `sources`, `humanModifiedKeys`, `humanDeltas`, and `inferredIntent` (computed by `inferHumanIntent(state)` into labels such as `frosted-crystal`, `silk-cinematic`, `crisp-utility`, `tactile-focus`, or `balanced-studio`).
   - Simultaneously, `window.__MD3E_STUDIO__` exposes `{ getState, setParam, harmonize, reset, exportCss, applyUrlOrStorage, statusCapsule, animateTabularCounter, refreshBindings, destroy }` (alongside exported helpers `createStatusCapsule` and `animateTabularCounter` in `md3e-studio.js`) so an IDE agent or browser automation harness can read live deltas and apply co-tuned updates.
3. **Coupled AI / Algorithmic Harmonization (`computeHarmonizedParams(state)` / `#btn-studio-harmonize`)**:
   - Reads `humanModifiedKeys`, `humanDeltas`, and `inferredIntent` from `#md3e-studio-telemetry` (or `getState()`).
   - Computes coupled complementary adjustments across **untouched** parameters while **locking and preserving every `human`-pinned key** untouched:
     - *Example (Optical coupling)*: Lowering `glassAlpha` or raising `blurPx` boosts `glassSaturate`, raises `specularAlpha` to preserve edge definition, and subtly adjusts `spotlightAlpha`.
     - *Example (Physics coupling)*: Softening `springStiffness` adjusts `springDamping` and tunes `--md-studio-stagger-ms` proportionally so card staggers match the slower organic settle time.
4. **Live Preview & Exportable CSS Patch (`#studio-css-output`)**:
   - `formatStudioCssPatch(values)` emits a ready-to-paste `:root[data-studio-profile="personal-studio"] { ... }` CSS block inside `#studio-css-output` for live preview (`#btn-studio-preview`), clipboard export (`#btn-studio-copy-css`), or reset (`#btn-studio-reset`).

```js
// Programmatic AI Co-Tuning inspection & harmonization via window.__MD3E_STUDIO__
const telemetryEl = document.getElementById('md3e-studio-telemetry');
const telemetry = JSON.parse(telemetryEl.textContent);
// telemetry -> { inferredIntent: "frosted-crystal", humanModifiedKeys: ["glassAlpha"], humanDeltas: { glassAlpha: -12 }, ... }

const result = window.__MD3E_STUDIO__.harmonize();
// Human-pinned keys (e.g. glassAlpha) stay locked; untouched keys (blurPx, glassSaturate, specularAlpha)
// update with source: "ai", and #studio-css-output reflects the clean diff.
const cssPatch = window.__MD3E_STUDIO__.exportCss();
```

---

## 4. Desktop Ergonomics & Frame-Rate Engine

Layer 4 adds desktop-first ergonomics built strictly on native HTML standards, `in oklab` color math, and refresh-rate-invariant motion:

1. **`Ctrl+K` Command Palette (`<dialog id="studio-cmd-dialog" closedby="any">`)**:
   - Uses native `<dialog closedby="any">` for light-dismiss backdrop click and `Escape` restoration — **never** add redundant `role="dialog"` or `aria-modal` (`MD3E020` / `MD3E202`).
   - Locks background scroll leakage with `dialog.studio-cmd-dialog:modal { overscroll-behavior: contain; }` and `dialog.studio-cmd-dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }`.
   - Provides live fuzzy filtering across workspace commands (`Theme`, `Seed`, `Rail`, `Tuner`, `Harmonize`, `Expand`, view filters).
2. **Pointer Spotlight (`[data-studio-spotlight]`, `in oklab`)**:
   - A `requestAnimationFrame`-coalesced pointermove listener sets `--studio-mx` and `--studio-my` on `[data-studio-spotlight]` hosts, painting a soft radial highlight sized by `--md-studio-spotlight-px` and mixed via `color-mix(in oklab, var(--md-sys-color-primary) var(--md-studio-spotlight-alpha), transparent)`.
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

- `--mode=personal-studio` inherits Layer 3 Bento checks (`MD3E101`–`MD3E104`, `CUSTOM`) plus Layer 4 checks (`MD3E201` optical glass + caustic/reduced-transparency hygiene, `MD3E202` `<dialog>` modal `overscroll-behavior` / no redundant `role="dialog"` / focusable controls — `CUSTOM` unless a core WCAG/contrast/focus `ERROR` triggers).
- `--mode=strict` remains 100% isolated from `MD3E101+` and `MD3E201+`, and `CUSTOM` findings never lower `official_compliance.score`.
