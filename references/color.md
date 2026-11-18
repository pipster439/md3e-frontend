# Colour — Material 3 Expressive

Source: <https://m3.material.io/styles/color/system/overview>, token values in
`assets/tokens/md3e-tokens.css`.

## The model in one paragraph

A product picks **one seed colour**. Material expands it into **six tonal
palettes** (primary, secondary, tertiary, neutral, neutral-variant, error),
each with 13 **tones** from 0 to 100. A tone is a *luminance step*, not a
lightness percentage — tone 0 is always black and tone 100 is always white,
regardless of hue. A **colour role** is a pointer such as "primary" that names
a job, and each role resolves to a different tone in light and dark. That is
why you never write a hex value in a component: the role is the API, the tone
is the implementation.

## Role → tone mapping (baseline scheme)

| Role | Light | Dark | Role | Light | Dark |
|---|---|---|---|---|---|
| primary | P40 | P80 | on-primary | P100 | P20 |
| primary-container | P90 | P30 | on-primary-container | P10 | P90 |
| secondary | S40 | S80 | on-secondary | S100 | S20 |
| secondary-container | S90 | S30 | on-secondary-container | S10 | S90 |
| tertiary | T40 | T80 | on-tertiary | T100 | T20 |
| tertiary-container | T90 | T30 | on-tertiary-container | T10 | T90 |
| error | E40 | E80 | on-error | E100 | E20 |
| error-container | E90 | E30 | on-error-container | E10 | E90 |
| surface | N98 | N6 | on-surface | N10 | N90 |
| surface-variant | NV90 | NV30 | on-surface-variant | NV30 | NV80 |
| surface-container-lowest | N100 | N4 | surface-container-low | N96 | N10 |
| surface-container | N94 | N12 | surface-container-high | N92 | N17 |
| surface-container-highest | N90 | N22 | surface-dim | N87 | N6 |
| surface-bright | N98 | N24 | outline | NV50 | NV60 |
| outline-variant | NV80 | NV30 | inverse-surface | N20 | N90 |
| inverse-on-surface | N95 | N20 | inverse-primary | P80 | P40 |

Read `P`/`S`/`T`/`E` as primary/secondary/tertiary/error palettes, `N` as
neutral, `NV` as neutral-variant. Together with the 12 Fixed roles below plus
`scrim` (`N0` / `#000000`, typically rendered at 32% opacity), `shadow`, and
legacy `surface-tint`, `assets/tokens/md3e-tokens.css` defines all **47**
`--md-sys-color-*` tokens.

## Choosing a role

Work down this list; the first line that describes the element wins.

1. **Primary action, high emphasis** → `primary` fill with `on-primary` content.
   Filled buttons, the one thing the screen is for.
2. **Standout fill for a key component** → `primary-container` /
   `on-primary-container`. FABs, selected chips, the active nav indicator.
   This is the most-used pairing in M3E and the one most often skipped.
3. **Secondary action, selected state** → `secondary-container` /
   `on-secondary-container`. Tonal buttons, the selected row, filled chips.
4. **Contrasting accent** → `tertiary` / `tertiary-container`. One accent per
   view, to balance rather than compete. M3E makes tertiary more prominent than
   M3 did, so it now carries real accents instead of only decorative ones.
5. **Failure** → `error` / `error-container`.
6. **A surface** → pick by the elevation it should read as:
   `surface-container-lowest` (recessed) → `low` → `container` (default, nav
   areas) → `high` → `highest` (most prominent). Do not invent opacity to fake
   this ladder.
7. **Border that carries meaning** → `outline` (text field borders, focus rings).
   **Decorative divider** → `outline-variant`.
8. **Content on top of an inverse surface** (snackbar, tooltip) →
   `inverse-surface` + `inverse-on-surface` (+ `inverse-primary` for the action).

### The one rule you cannot break

Content colour must always be the **on-** counterpart of the container it sits
on: `primary` → `on-primary`, `surface-container-high` → `on-surface`, and so
on. This pairing is what guarantees contrast in both themes. Mixing them
(`on-primary` text on `secondary-container`) is the single most common M3
mistake and it breaks silently in dark mode.

### Fixed roles

`*-fixed`, `on-*-fixed`, `*-fixed-dim` and `on-*-fixed-variant` resolve to the
**same tone in light and dark**. Use them when brand identity must survive the
theme switch — a logo block, a brand hero, a coloured card in a light-themed
app that must stay light. If you use fixed roles for ordinary UI, dark mode
goes wrong: you will paint a light container onto a dark surface.

### Expressive colour updates (MCU SPEC_2025, Scheme Variants & Contrast)

- **Official scheme variants (`data-color-variant`).** Unlike earlier baseline M3, Material Color Utilities `SPEC_2025` computes distinct hue rotations, chroma multipliers, and surface tinting per scheme variant:
  - `tonal-spot` *(default)*: balanced low-to-medium chroma harmonised with the seed.
  - `expressive`: detached, high-variety primary/secondary/tertiary hue rotations with noticeably tinted neutral containers.
  - `vibrant`: maximum chromatic impact (high-chroma accent palettes and lively surface containers).
  - `neutral`: restrained near-greyscale accents (`C = 4..12`).
  - `monochrome`: strict achromatic greyscale (`C = 0`, 2021 rules) for editorial/minimal UI.
  - `fidelity`: anchors `primary-container` near the true seed tone paired with a temperature-complement `tertiary` (via `scripts/color_to_css.py`).
- **Multi-seed presets & brand generator.** Import `assets/tokens/md3e-palettes.css` for built-in curated seeds (`data-seed="purple|ocean|emerald|amber|rose|teal"`), or generate any custom brand seed with pure-stdlib CAM16/HCT:
  ```bash
  python scripts/color_to_css.py --seed "#0B57D0" --variant expressive --emit-css tokens/brand-colors.css
  ```
- **Three contrast levels & Forced Colors Mode.** Standard (`0.0`, `>= 4.5:1`), Medium (`data-contrast="medium"`, `>= 6.0:1`), and High (`data-contrast="high"` + `@media (prefers-contrast: more)`, `>= 7.0:1`) are all shipped per variant and seed in `md3e-tokens.css` / `md3e-palettes.css`. Window High Contrast (`@media (forced-colors: active)`) overrides focus outlines to `Highlight` and resets frosted overlays to `Canvas` / `CanvasText`.
- **Colour interpolation space (Layer 2 — Web Implementation `[ERROR]` rule).** When tinting or mixing translucent neutral surfaces (`surface*`, `on-surface*`, `outline*`, `shadow`, `scrim`, `currentColor`), always use `color-mix(in oklab, ...)` — never `in oklch` on neutrals/low-chroma colours (`MD3E018` `[ERROR]`), which triggers Chromium's powerless hue angle bug (`0deg` reddish shift).

## Blur, translucency & scrims (Layer 1 Spec vs Layer 2 Web Adaptation)

- **Layer 1 Official `m3.material.io` Component Spec:** Does **not** publish `md.sys.blur.*` tokens. Component depth is communicated via opaque tonal `surface-container-*` elevation steps and solid dark `scrim` (`32%` opacity).
- **Android 16 Material 3 Expressive System UI context:** Android 16 introduced real-time window-level background blur on *transient system overlays* alongside a system accessibility toggle disabling blur.
- **Layer 2 Web Adaptation (`assets/tokens/md3e-blur.css`):** For transient floating chrome (e.g. Floating Toolbars or scrims), `md3e-blur.css` supplies `.md3e-frosted-surface` using `--md3e-fx-blur-subtle: 12px` / `--md3e-fx-blur-standard: 20px` / `--md3e-fx-blur-heavy: 40px`, tinted with high-opacity `color-mix(in oklab, ...)`. It automatically falls back to opaque `surface-container` under `@media (prefers-reduced-transparency: reduce)`, `prefers-contrast: more`, `[data-contrast="high"]`, and `forced-colors: active`. Shipping `backdrop-filter: blur(...)` without a reduced-transparency fallback fails `MD3E022` at `[ERROR]` severity.

## State layers

A state layer is a semi-transparent overlay **in the content's own colour**
(usually the `on-` role), not a separate colour. Exactly one may be active.

| State | Opacity |
|---|---|
| Hover | 8% |
| Focus | 10% |
| Pressed | 10% |
| Dragged | 16% |

Disabled: container 12%, content 38%. The state layer is 40dp; the interactive
target around it is 48dp.

```css
/* correct: the overlay inherits the content colour */
.btn { position: relative; background: var(--md-sys-color-primary); color: var(--md-sys-color-on-primary); }
.btn::after {
  content: ""; position: absolute; inset: 0; border-radius: inherit;
  background: currentColor; opacity: 0; pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects);
}
.btn:hover::after  { opacity: var(--md-sys-state-hover-state-layer-opacity); }
.btn:focus-visible::after { opacity: var(--md-sys-state-focus-state-layer-opacity); }
.btn:active::after { opacity: var(--md-sys-state-pressed-state-layer-opacity); }
```

## Common mistakes

| Don't | Do |
|---|---|
| `color: #6750A4` | `color: var(--md-sys-color-primary)` |
| `rgba(0,0,0,.08)` for a hover shade | `currentColor` at the hover state-layer token |
| `background: var(--md-sys-color-surface)` for a card on a surface | `surface-container-low` — put the card one step above its parent |
| `on-primary` text on `secondary-container` | `on-secondary-container` |
| Fixed roles for ordinary UI | Fixed roles only for brand-anchored moments |
| A separate dark palette with invented hex values | The same roles redefined to different tones |
| Colour alone to signal error or selection | Colour **plus** an icon, label or shape change |

## Dark mode

Redefine the roles; do not invert or filter anything. Concretely: swap
`[data-theme="dark"]` in, honour `prefers-color-scheme`, and set
`color-scheme: dark` so form controls and scrollbars follow. Emphasis roles go
*lighter* in dark mode (P80 over P40), and surface containers get *lighter* as
they rise (`N4 → N10 → N12 → N17 → N22`), which is the opposite direction from
light mode (`N100 → N96 → N94 → N92 → N90`).


## Image & wallpaper dynamic colour extraction

Both the build-time CLI and the zero-dependency browser ES module implement MCU's
two-stage **`QuantizerCelebi`** (`QuantizerWu` + `QuantizerWsmeans` in CIE `L*a*b*`)
followed by **`Score`** (excited hue proportion weight `0.7`, target chroma `48`,
hue-deduplicated Top-N candidates) and **`SPEC_2025` HCT** generation:

- **Build-time CLI (`scripts/color_to_css.py --image`)**:

```bash
python scripts/color_to_css.py --image wallpaper.jpg --variant expressive --emit-css tokens/brand-colors.css
python scripts/color_to_css.py --image wallpaper.png --json   # returns ranked extracted_candidates + schemes
```

- **Browser runtime (`assets/tokens/md3e-dynamic-color.js`)**: accepts a
  user-uploaded `File` / `Blob` from `<input type="file" accept="image/*" class="visually-hidden">`
  (hidden via accessible `.visually-hidden` clip-path rather than `display: none` so
  keyboard users can still focus the paired `<label>` trigger), downscales onto a
  `<= 128px` `<canvas>`, extracts ranked seed candidates, and injects `[data-seed="custom"]`
  CSS covering all `5` UI variants, light/dark themes, and standard/medium/high contrast levels:

```js
import { applyDynamicSeed, extractSeedsFromImage, renderStandaloneCss } from '../tokens/md3e-dynamic-color.js';

const { primarySeed, candidates } = await extractSeedsFromImage(fileInput.files[0]);
applyDynamicSeed(primarySeed); // injects [data-seed="custom"] CSS into <head> and updates <html>
const exportCss = renderStandaloneCss(primarySeed, { variant: 'expressive' });
```
