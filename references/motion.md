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

## Using it on the web

CSS has no spring primitive. `scripts/spring_to_css.py` solves the damped
harmonic oscillator and emits a sampled `linear()` easing per token, preserving
overshoot (values above 1 are legal in `linear()`). Output lives in
`assets/tokens/md3e-motion.css`.

```css
/* correct */
.card { transition: transform var(--md-sys-motion-default-spatial); }
.card:hover { transform: translateY(-2px); }

.switch { transition: background-color var(--md-sys-motion-fast-effects); }
```

```css
/* forbidden: this is the pre-Expressive model */
.card { transition: transform 300ms cubic-bezier(0.2, 0, 0, 1); }
```

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
// This is the expressive default spatial spring: damping 0.8, stiffness 380.
element.animate(
  [{ transform: "scale(1)" }, { transform: "scale(1.08)" }],
  { duration: 460, easing: "var(--md-sys-motion-default-spatial)", fill: "both" }
);
```

For gesture-driven motion, prefer a real spring integrator (Web Animations API
with a spring easing, or a small physics loop) so a dragged element keeps its
velocity when released. A CSS transition restarts from zero and feels dead.

## Legacy layer

The duration/easing tokens are still in the token file, for two reasons: engines
without `linear()` support, and properties that cannot overshoot legibly. Do
**not** mix the two models on the same property.

| Token | Value |
|---|---|
| `--md-sys-motion-easing-emphasized` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--md-sys-motion-easing-emphasized-decelerate` | `cubic-bezier(0.05, 0.7, 0.1, 1)` |
| `--md-sys-motion-easing-emphasized-accelerate` | `cubic-bezier(0.3, 0, 0.8, 0.15)` |
| `--md-sys-motion-easing-standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--md-sys-motion-easing-standard-decelerate` | `cubic-bezier(0, 0, 0, 1)` |
| `--md-sys-motion-easing-standard-accelerate` | `cubic-bezier(0.3, 0, 1, 1)` |

Durations run `short1` 50ms → `short4` 200ms, `medium1` 250ms → `medium4` 400ms,
`long1` 450ms → `long4` 600ms, `extralong1` 700ms → `extralong4` 1000ms.

## Reduced motion

Always provide the path. Keep a short cross-fade so state changes stay legible,
and drop every spatial spring that moves, scales or morphs the UI. The token
file already does this under `@media (prefers-reduced-motion: reduce)`.

## Do / Don't

| Do | Don't |
|---|---|
| Use spring tokens for all component motion | Hand-write duration + easing |
| One scheme for most of the product | Mix expressive and standard arbitrarily |
| Spatial springs for position, size, shape | Spatial springs on colour, or effects springs on position |
| Let `default` carry most motion | Use `fast` for large surfaces or `slow` for switches |
| Rely on interruption and retargeting | Rebuild animations from zero on gesture handoff |
| Honour `prefers-reduced-motion` | Assume everyone wants bounce |
| Keep motion meaningful — state, progress, attention | Animate for decoration with no trigger |
