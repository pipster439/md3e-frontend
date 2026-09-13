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
| `corner-medium` | 12px | Cards, small FABs |
| `corner-large` | 16px | FABs, navigation drawer, large containers |
| `corner-large-increased` | 20px | **Expressive** — emphasis without going full pill |
| `corner-extra-large` | 28px | Dialogs, bottom sheets, search bars |
| `corner-extra-large-increased` | 32px | **Expressive** — large FABs, hero containers |
| `corner-extra-extra-large` | 48px | **Expressive** — hero moments |
| `corner-full` | fully rounded | Buttons, chips, badges, avatars |

`corner-full` is useful for pill-like component corners. `border-radius: 50%`
is valid CSS for a circle on a square box and can intentionally produce an
ellipse on a non-square box. Choose by the intended geometry; a percentage
radius is not automatically a Material violation.

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

## Shape library (35 shapes)

For decorative moments: image crops, avatar masks, loading indicators, empty
states. Categories, all normalised to a unit square and morphable:

- **Basic** — circle, square, triangle, diamond, oval, rectangle, pentagon,
  semi-circle, pill, slanted
- **Expressive / organic** — heart, flower, ghostish, bun, arrow, fan, gem
- **Cookie and star** — cookie4Sided, cookie6Sided, cookie7Sided,
  cookie9Sided, cookie12Sided, sunny, verySunny, burst, softBurst, boom,
  softBoom
- **Clover and nature** — clover4Leaf, clover8Leaf, puffy, puffyDiamond,
  arch, clamShell
- **Pixel** — pixelCircle, pixelTriangle

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
.chip { transition: border-radius var(--md-sys-motion-default-spatial); }
.chip[aria-pressed="true"] { border-radius: var(--md-sys-shape-corner-full); }
.chip[aria-pressed="false"] { border-radius: var(--md-sys-shape-corner-small); }
```

## Tension

Material was historically all rounded. M3E deliberately introduces **tension**
by mixing round and square shapes. Tension makes a design more memorable and
directs attention. Use it to:

- convey a state
- draw attention to one element
- improve the composition

Break from the surrounding shape language selectively so the contrast reads as
intentional rather than inconsistent.

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
| Use `corner-full` for pills and circles where it fits | Assume every `50%` radius is wrong |
| Use the "increased" steps for emphasis | Jump straight to a pill when you want a little emphasis |
| Add tension deliberately, on one element | Mix round and square randomly |
| Adjust nested radii for optical roundness | Give parent and child the same radius |
| Keep large corners off dense content | Apply `corner-extra-extra-large` to a data table |
| Morph shape for state and progress | Morph for decoration with no trigger |
