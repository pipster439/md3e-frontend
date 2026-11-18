# Shape — Material 3 Expressive

Source: <https://m3.material.io/styles/shape/corner-radius-scale>,
<https://m3.material.io/styles/shape/overview-principles>

## The corner radius scale

Ten steps, named for **how rounded the corner is** — not for how big the
component is. That rename is the whole point: in M2 the scale was tied to
component size, in M3 any component can take any step.

| Token | Value | Typical use |
|---|---|---|
| `corner-none` | 0px | Full-bleed content, deliberate square tension |
| `corner-extra-small` | 4px | Chips (legacy), menus, snackbars, tooltips |
| `corner-small` | 8px | Text fields, small controls |
| `corner-medium` | 12px | Cards, square XS/S buttons |
| `corner-large` | 16px | Regular FAB (56dp), navigation drawer, square M buttons, large containers |
| `corner-large-increased` | 20px | **Expressive** — medium FAB (80dp), 40dp pill buttons, emphasis without full pill |
| `corner-extra-large` | 28px | Dialogs, bottom sheets, large FAB (96dp), square L/XL buttons |
| `corner-extra-large-increased` | 32px | **Expressive** — hero containers, emphasis without going full pill |
| `corner-extra-extra-large` | 48px | **Expressive** — hero moments |
| `corner-full` | fully rounded | Buttons, chips, badges, avatars |

`corner-full` replaces the old "50% of the component size" trick. Use the
token, not `border-radius: 50%` — `50%` produces an ellipse on a non-square
box, which is a bug, not a shape.

The three "increased" steps are new in M3E and exist purely to give you
emphasis without jumping straight to a pill.

## Asymmetric and inner corners

Components with closely grouped items — menus, split buttons, FAB menus,
button groups — use asymmetric corners. The **inner corners** of a group must
read as one continuous silhouette, so the inner corner of the first element
faces the inner corner of the last one.

```css
.group > :first-child { border-radius: var(--md-sys-shape-corner-large) 0 0 var(--md-sys-shape-corner-large); }
.group > :last-child  { border-radius: 0 var(--md-sys-shape-corner-large) var(--md-sys-shape-corner-large) 0; }
```

Both symmetric and asymmetric shapes draw from the same ten-step scale.

## Shape library (35 official `MaterialShapes` presets)

For decorative moments: image crops, avatar masks, loading indicators, empty
states. All **35** official presets from `androidx.compose.material3.MaterialShapes`
are pre-generated into `assets/tokens/md3e-shapes.css` (and reproducible via
`python scripts/shapes_to_css.py --emit-css assets/tokens/md3e-shapes.css`):

- **Basic (10)** — `circle`, `square`, `slanted`, `arch`, `fan`, `arrow`,
  `semi-circle`, `oval`, `pill`, `triangle`
- **Geometric & organic (8)** — `diamond`, `clam-shell`, `pentagon`, `gem`,
  `ghostish`, `bun`, `heart`, `flower`
- **Cookie & star (11)** — `sunny`, `very-sunny`, `cookie-4-sided`,
  `cookie-6-sided`, `cookie-7-sided`, `cookie-9-sided`, `cookie-12-sided`,
  `burst`, `soft-burst`, `boom`, `soft-boom`
- **Clover & nature (4)** — `clover-4-leaf`, `clover-8-leaf`, `puffy`,
  `puffy-diamond`
- **Pixel (2)** — `pixel-circle`, `pixel-triangle`

Use `.md3e-shape` paired with `.md3e-shape-<name>` (which sets both
`-webkit-mask-image` and `mask-image`, plus an `@supports` rounded-corner
fallback). When a masked polygon needs a drop shadow, wrap it in
`.md3e-shape-shadow-wrap` (`filter: drop-shadow(...)` rather than `box-shadow`,
which casts a rectangle). Do not use `MD3E` CSS mask presets behind dense body
copy; keep them on avatars, media crops, and the `LoadingIndicator` (`SoftBurst ->
Cookie9Sided -> Pentagon -> Pill -> Sunny -> Cookie4Sided -> Oval`).

Rules from the spec:

- **Shape is versatile, not semantic.** Do not assign one fixed meaning to a
  shape. The loading indicator's waveform is not *the* symbol of progress —
  rotating shapes or a morph work just as well, and the waveform can appear
  somewhere unrelated.
- **Use abstract shapes sparingly.** Shapes without a reason add clutter, not
  delight. Ask why this shape, here.
- **Decorative only.** Shape library shapes belong on imagery, avatars,
  illustration and non-interactive containers. Do not put them behind
  text-heavy content.
- **Stay off information-dense components.** Large or full corners clip
  content. A big cut corner on a card crops more than a rounded one of the
  same size.

## Shape morph

Morphing is built in and is the signature Expressive effect. Morph to
communicate:

- **Interaction state** — a button becoming selected
- **Progress** — a page loading, a friend typing
- **Environment change** — sound, temperature, time of day

Drive morphs with a **spatial** spring (corner radius and size are spatial
properties, so the spring overshoots and bounces).

```css
/* Use the bounded half-height radius (16px on a 32px chip) instead of 9999px
   when animating border-radius so the spring curve does not clamp and snap. */
.chip { transition: border-radius var(--md-sys-motion-default-spatial); }
.chip[aria-pressed="true"] { border-radius: var(--md-sys-shape-corner-large); }
.chip[aria-pressed="false"] { border-radius: var(--md-sys-shape-corner-small); }
```

## Tension

Material was historically all rounded. M3E deliberately introduces **tension**
by mixing round and square shapes. Tension makes a design more memorable and
directs attention. Use it to:

- convey a state
- draw attention to one element
- improve the composition

Break from the surrounding shape language for exactly one element — that is how
tension reads as intentional rather than inconsistent.

## Optical roundness

When nesting rounded objects, never give both the same radius: equal radii
look unbalanced because the eye reads the *ring width*, not the radius.

```
outer radius − padding = inner radius
48px − 14px = 34px
```

## Do / Don't

| Do | Don't |
|---|---|
| Pick steps from the ten-step scale | Invent `border-radius: 10px` |
| Use `corner-full` for pills and circles | `border-radius: 50%` |
| Use the "increased" steps for emphasis | Jump straight to a pill when you want a little emphasis |
| Add tension deliberately, on one element | Mix round and square randomly |
| Adjust nested radii for optical roundness | Give parent and child the same radius |
| Keep large corners off dense content | Apply `corner-extra-extra-large` to a data table |
| Morph shape for state and progress | Morph for decoration with no trigger |
