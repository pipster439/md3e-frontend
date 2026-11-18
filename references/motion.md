# Motion — Material 3 Expressive

Sources: <https://m3.material.io/styles/motion/overview/how-it-works>,
<https://m3.material.io/styles/motion/overview/specs>

## Springs replace duration + easing

M3E introduced a **physics system**. It replaces the previous
duration-and-easing model for component motion. You no longer say "300ms
ease-in-out"; you say "default spatial spring" and the system resolves it.

A spring has three attributes:

- **Stiffness** — how hard the spring is. Higher resolves faster.
- **Damping** — how fast the bounce dies out. Damping 1.0 removes bounce
  entirely.
- **Initial velocity** — the speed handed in, usually from a gesture.

Why springs beat tweens: they are **interruptible and velocity-aware**. A
gesture handed off mid-flight continues smoothly instead of restarting from
zero. Retargeting an animation that is already running just works.

## Schemes, types, speeds

Two preset **schemes**:

- **Expressive** — Material's opinionated default. Overshoots the final value
  to add bounce. Use it for most situations, especially hero moments and key
  interactions.
- **Standard** — minimal bounce, eases into place. Use it for utilitarian
  products.

Most motion in a product should use one scheme; swap to the other only to
emphasise a moment. The scheme is applied **at product level** — it is not part
of the token name, which is what makes it swappable.

Two **types**:

- **Spatial** — position, orientation, size, rotation, **corner radius**.
  Overshoots and bounces.
- **Effects** — colour and opacity. Must **not** overshoot.

Effects springs are identical in both schemes: expression belongs to movement,
not to colour.

Three **speeds**: `fast` (small components — switches, buttons), `default`
(animations partially covering the screen — bottom sheets, nav rail),
`slow` (full-screen transitions, full-screen refresh).

## Spring parameter table

Official token: `md.sys.motion.spring.<speed>.<type>`.

| Scheme | Speed | Type | Damping | Stiffness | Settled | Peak overshoot |
|---|---|---|---|---|---|---|
| expressive | fast | spatial | 0.6 | 800 | 380ms | 9.5% |
| expressive | default | spatial | 0.8 | 380 | 460ms | 1.5% |
| expressive | slow | spatial | 0.8 | 200 | 620ms | 1.5% |
| expressive | fast | effects | 1.0 | 3800 | 170ms | 0% |
| expressive | default | effects | 1.0 | 1600 | 260ms | 0% |
| expressive | slow | effects | 1.0 | 800 | 350ms | 0% |
| standard | fast | spatial | 0.9 | 1400 | 250ms | 0.2% |
| standard | default | spatial | 0.9 | 700 | 340ms | 0.2% |
| standard | slow | spatial | 0.9 | 300 | 510ms | 0.2% |
| standard | fast | effects | 1.0 | 3800 | 170ms | 0% |
| standard | default | effects | 1.0 | 1600 | 260ms | 0% |
| standard | slow | effects | 1.0 | 800 | 350ms | 0% |

"Peak overshoot" is the maximum percentage by which the spring exceeds its
target. Note that `expressive default spatial` bounces only **1.5%** — the
Expressive feel comes mostly from its lower stiffness (380 vs 700), not from a
dramatic bounce. Do not exaggerate it.

Settle times and overshoot are derived analytically from the damping and
stiffness by `scripts/spring_to_css.py`; they are not hand-tuned.

## Using it on the web (Layer 2 — Web Implementation)

Web UI has two equally valid first-class ways to run Material 3 Expressive motion:

1. **Physical Spring Tokens & JS Spring Solver**: `scripts/spring_to_css.py` solves the damped harmonic oscillator and emits sampled `linear()` easing tokens in `assets/tokens/md3e-motion.css` (overshoot above `1` is valid in `linear()`). For real-time interruptible pointer/shape gestures, use `assets/tokens/md3e-spring.js`.
2. **Official Google Web-Compatible Easing Curves (`OFFICIAL_WEB_CURVES`)**: When authoring pure CSS transitions without `linear()` or targeting legacy browsers, Google's calibrated cubic-bezier curves (`cubic-bezier(0.2, 0, 0, 1)`, `cubic-bezier(0.3, 0, 0.8, 0.15)`, `cubic-bezier(0.05, 0.7, 0.1, 1)`, `cubic-bezier(0.4, 0, 0.2, 1)`, `cubic-bezier(0, 0, 0, 1)`) paired with documented durations (typically `150ms–500ms`) are **first-class valid implementations** and pass audit cleanly.

```css
/* Valid Option 1: Sampled linear() spring token */
.card { transition: transform var(--md-sys-motion-default-spatial); }
.card:hover { transform: translateY(-2px); }

/* Valid Option 2: Official Web-compatible curve + calibrated duration */
.dialog-scrim { transition: opacity 200ms cubic-bezier(0.2, 0, 0, 1); }

/* Valid: Effects spring on non-spatial property */
.switch { transition: background-color var(--md-sys-motion-fast-effects); }
```

> **Guidance (non-fatal `WARNING`):** Reserve ad-hoc uncalibrated `cubic-bezier(...)` curves outside `OFFICIAL_WEB_CURVES` or mismatched spatial/effects pairings — avoid banning Web curves on components where spring `linear()` is unnecessary.

Pick the token by asking two questions:

| | small component | partial-screen change | full-screen |
|---|---|---|---|
| **moves / resizes / reshapes** | `fast-spatial` | `default-spatial` | `slow-spatial` |
| **fades / recolours** | `fast-effects` | `default-effects` | `slow-effects` |

Never use a spatial spring for opacity or colour, and never use an effects
spring for position — an effects spring will not bounce, and a spatial spring
on colour does not compute.

Switch the scheme for the whole product with one attribute:

```html
<html data-motion-scheme="expressive">
```

```js
// Hand-rolled springs are legitimate when you need gesture handoff.
// WAAPI does not accept CSS shorthand strings (`460ms linear(...)`) or unresolved
// `var(...)` in `easing`; read the split -duration and -easing tokens explicitly.
const styles = getComputedStyle(document.documentElement);
const duration = parseFloat(styles.getPropertyValue('--md-sys-motion-default-spatial-duration')) || 460;
const easing = styles.getPropertyValue('--md-sys-motion-default-spatial-easing').trim() || 'ease-out';

element.animate(
  [{ transform: 'scale(1)' }, { transform: 'scale(1.08)' }],
  { duration, easing, fill: 'both' }
);
```

When writing CSS `@keyframes` animations, pass the `-easing` token (`var(--md-sys-motion-default-spatial-easing)`), never the composite shorthand (`var(--md-sys-motion-default-spatial)`), because CSS parses a second `<time>` inside the `animation:` shorthand as `animation-delay`.

For engines without `linear()`, `md3e-motion.css` falls back via `@supports not (transition-timing-function: linear(0, 1))` to M3E's official Web `cubic-bezier` curves (`350ms cubic-bezier(0.42, 1.67, 0.21, 0.90)` for expressive fast spatial, `500ms cubic-bezier(0.38, 1.21, 0.22, 1.00)` for default spatial, `650ms cubic-bezier(0.39, 1.29, 0.35, 0.98)` for slow spatial).

For gesture-driven motion, use **`assets/tokens/md3e-spring.js`** (`createSpringAnimator`, `resolveSpringPreset`) or WAAPI velocity handoff so a dragged element keeps its live velocity when released or interrupted mid-flight. A pure CSS `linear()` transition restarts from zero velocity.

## Web alignment matrix (`linear()`, Official Web `cubic-bezier`, JS Physics)

| Driver | CSS / JS API | Duration & Overshoot Behaviour | When to use |
|---|---|---|---|
| **CSS `linear()` spring** *(Default)* | `var(--md-sys-motion-<speed>-<kind>)` | Exact damped harmonic oscillator unit-step curve (`380/460/620ms` analytical settle `±0.1% + 20ms tail`) | Hover/press/toggle/layout transitions |
| **Official Web `cubic-bezier`** | `var(--md-sys-motion-<speed>-<kind>-bezier)` or `<html data-motion-driver="bezier">` | `m3.material.io` published `350 / 500 / 650ms` single-overshoot curves (also automatic `@supports not` fallback) | Parity with `m3.material.io` Web bezier table or legacy browsers |
| **JS Spring Integrator** | `assets/tokens/md3e-spring.js` (`createSpringAnimator`) | Exact closed-form `(stiffness, damping)` physics per `requestAnimationFrame`; zero velocity loss on retarget/drag release | Drag-and-drop gestures, interruptible cards/drawers, interactive physics |
| **Morph Loading Indicator** | `--md-comp-loading-indicator-morph-easing` | Official `spring(damping = 0.6, stiffness = 200)` sampled across `650ms` interval × 7 shapes (`4550ms` cycle) + `4666ms` linear rotation | Expressive `LoadingIndicator` (`md3e-shapes.css`) |

## Official Web-Compatible Curves (First-Class Web Easing + Duration)

In Web implementations (Layer 2), Google's calibrated Web easing tokens paired with their documented duration tokens (`short1` 50ms -> `short4` 200ms, `medium1` 250ms -> `medium4` 400ms, `long1` 450ms -> `long4` 600ms, `extralong1` 700ms -> `extralong4` 1000ms) are **first-class valid implementations** alongside sampled `linear()` springs (`md3e-motion.css`) and JS physics (`md3e-spring.js`). This is both compliant for all production Web components and safer for non-overshooting opacity/color transitions or browsers without `linear()`. Do **not** mix two incompatible curves on the same property transition.

| Token | Value (`OFFICIAL_WEB_CURVES`) |
|---|---|
| `--md-sys-motion-easing-emphasized` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--md-sys-motion-easing-emphasized-decelerate` | `cubic-bezier(0.05, 0.7, 0.1, 1)` |
| `--md-sys-motion-easing-emphasized-accelerate` | `cubic-bezier(0.3, 0, 0.8, 0.15)` |
| `--md-sys-motion-easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--md-sys-motion-easing-standard-decelerate` | `cubic-bezier(0, 0, 0, 1)` |
| `--md-sys-motion-easing-standard-accelerate` | `cubic-bezier(0.3, 0, 1, 1)` |

## Reduced motion

Always provide the path. Keep a short cross-fade so state changes stay legible,
and drop every spatial spring that moves, scales or morphs the UI. The token
file already does this under `@media (prefers-reduced-motion: reduce)`.

## Do / Don't

| Do | Don't |
|---|---|
| Use sampled `linear()` spring tokens, `md3e-spring.js`, or `OFFICIAL_WEB_CURVES` + calibrated durations | Invent arbitrary uncalibrated `cubic-bezier()` curves (`MD3E004` warning) |
| Keep one consistent motion scheme per product | Mix expressive and standard schemes arbitrarily |
| Use spatial motion for position, size, and shape | Put spatial overshoot on colour/opacity, or effects curves on container morphs |
| Let `default` carry most transitions | Use `fast` for large surfaces or `slow` for tiny switches |
| Rely on interruption and retargeting (`md3e-spring.js`) | Rebuild animations from zero on gesture handoff |
| Honour `prefers-reduced-motion` | Assume everyone wants bounce |
| Keep motion meaningful — state, progress, attention | Animate for decoration with no trigger |

---

## Structural & Page-Level Spatial Choreography

Beyond component micro-interactions, coordinate chrome and multi-view transitions with deterministic M3E physics:

### 1. Dual-Spring Navigation Rail (`80px <-> 220px`)
Decouple container geometry from label legibility so labels never wrap or squish mid-flight:
- **Spatial Spring (`width` + active indicator pill)**: Transitions rail width between `80px` and `220px` using `var(--md-sys-motion-default-spatial)` (or `--md-bento-motion-default-spatial` in desktop Bento mode).
- **Effects Spring (`white-space: nowrap` labels)**: Keeps label spans permanently in layout flow inside `overflow: hidden` tracks. On collapse (`data-rail-expanded="false"`), labels fade out early (`85ms`–`90ms`, `0ms` delay) using `var(--md-sys-motion-easing-emphasized-accelerate)` before the rail narrows; on expand (`data-rail-expanded="true"`), labels fade in after `~65ms` delay using `var(--md-sys-motion-fast-effects)`.

```css
.nav-rail {
  width: 80px;
  overflow: hidden;
  transition: width var(--md-sys-motion-default-spatial);
}
.nav-rail[data-rail-expanded="true"] {
  width: 220px;
}
.nav-rail__label {
  white-space: nowrap;
  opacity: 0;
  transform: translateX(-6px);
  pointer-events: none;
  /* Fast early fade-out on collapse so labels vanish before rail narrows */
  transition: opacity 90ms var(--md-sys-motion-easing-emphasized-accelerate),
              transform 90ms var(--md-sys-motion-easing-emphasized-accelerate);
}
.nav-rail[data-rail-expanded="true"] .nav-rail__label {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
  transition: opacity var(--md-sys-motion-fast-effects) 65ms,
              transform var(--md-sys-motion-fast-spatial) 65ms;
}
@media (prefers-reduced-motion: reduce) {
  .nav-rail, .nav-rail__label { transition: none; }
}
```

### 2. View-Switch Fade Through & Staggered Bento Entrance (`25ms–35ms` Step)
When switching navigation views or filtering Bento workspaces:
1. **Outgoing Fade-Through Exit**: Fade the departing view out quickly (`opacity -> 0`, micro-scale `0.985`, `90ms` with `--md-sys-motion-easing-emphasized-accelerate`).
2. **Staggered Spring Arrival**: Swap visible panels/cards and stagger visible items in reading order at `--stagger-step: 30ms` (`25ms–35ms` range via `animation-delay: calc(var(--stagger-index, 0) * 30ms)`). Always pass `--md-sys-motion-default-spatial-easing` (never composite tokens with duration inside `animation`) and disable under `prefers-reduced-motion: reduce`.

### 3. View Transitions Shared Container Transform
Promote card-to-diagnostics expansions (such as `#event-stream-card` -> `#bento-vt-modal`) into continuous shared-element morphs using `document.startViewTransition(...)`:
- Assign `view-transition-name: bento-vt-panel` strictly to **1 active element before** and **1 active element after** the DOM mutation (marking the obscured source card invisible during modal display and setting `inert` on background landmarks).
- Bind `::view-transition-group(bento-vt-panel)` to `overflow: clip`, matching `border-radius: var(--md-sys-shape-corner-extra-large)` (`28px`), and MD3E Spatial Spring `-duration` / `-easing` tokens; wrap `@media (prefers-reduced-motion: reduce)` with `animation: none !important;`.

### 4. Physical Sliding Segmented Pill Indicator (`md3e-spring.js`)
Replace abrupt background-color swaps across connected single-select segments with a shared sliding capsule (`<span class="seg-indicator" aria-hidden="true">`) whose `translateX` and `width` are integrated per-frame by two `createSpringAnimator` instances (`{ stiffness: 1400, damping: 0.86 }`):
- Interruptions preserve live velocity and retarget smoothly mid-flight.
- Automatically snaps immediately (`immediate` when `prefers-reduced-motion: reduce` matches) and resynchronizes on `ResizeObserver`.
