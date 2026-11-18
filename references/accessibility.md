# Accessibility — Material 3 Expressive

M3's accessibility requirements are part of the spec, not an afterthought.
Several are the direct reason a token exists.

## Contrast

| Content | Minimum |
|---|---|
| Body text | 4.5:1 (WCAG AA), 7:1 for AAA |
| Large text (18pt+ / 24px+, or 14pt+ / 18.67px+ bold) | 3:1 |
| UI components, borders, icons | 3:1 |
| Focus indicator | 3:1 against adjacent colours |

The role system already satisfies this: `on-primary` against `primary`,
`on-surface` against `surface`, and every other container/on-pair is generated
to meet 4.5:1. This is the concrete reason not to mix an `on-` role with a
container it does not belong to — you lose the guarantee silently.

M3 standardises **three contrast levels** — standard, medium, high. Offer a
high-contrast path rather than assuming the default suits everyone. They are
tonal shifts of the same roles, so it costs one media query:

```css
@media (prefers-contrast: more) { /* shifted roles, see md3e-tokens.css */ }
```

Never rely on colour alone to carry meaning. Error needs an icon or a message;
selection needs an indicator, a check, or a shape change.

## Touch targets (Visual Size vs Pointer Hit Area)

Strictly distinguish a control's **visual box height/width** from its **interactive pointer hit area**:

- **Hard Accessibility Floor (WCAG 2.2 AA — `ERROR`):** Interactive controls must expose a hit area of at least **24×24 CSS px** (unless exempt under WCAG 2.2 SC 2.5.8 inline/spacing/user-agent rules). Anything smaller fails `MD3E006` at `[ERROR]` severity.
- **Recommended M3 Target (Material Guidance — `WARNING`):** Expand touch/click targets to **48×48 px** where layout allows (**56×56 px** recommended for primary actions), with **8 px** minimum gap (`16–24 px` where motor precision is limited). A compact **40 px** state layer inside a **48 px** invisible hit area satisfies both visual compact density and ergonomic touch targets.

Expressive button sizes **XS (32 px)** and **S (40 px)** intentionally have visual heights below 48 px — expand their pointer hit area via a pseudo-element rather than inflating their visual box:

```css
.btn-xs { height: 32px; position: relative; }
.btn-xs::before {                       /* invisible 48px hit area */
  content: ""; position: absolute; inset: -8px;
  border-radius: inherit;
}
```

Icon buttons: the glyph is 24px, the target is 48px, achieved with padding or
an overlay — never by enlarging the glyph.

## Focus

Every interactive element needs a visible focus indicator, and it must be at
least as prominent as the hover state. M3E specifies a **3px focus ring** with a
**2px offset/gap** (`--md-sys-focus-ring-width: 3px`, `--md-sys-focus-ring-gap: 2px`,
`--md-sys-focus-ring-color: var(--md-sys-color-secondary)` in `md3e-tokens.css`):

```css
:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-focus-ring-color, var(--md-sys-color-secondary));
  outline-offset: var(--md-sys-focus-ring-gap);
}
```

Never `outline: none` without a replacement. If a component clips its overflow,
draw an inset `3px` ring on a `::after` inset by `2px` instead. Under
`@media (forced-colors: active)`, `md3e-tokens.css` overrides the ring colour
to `Highlight`.

Show focus only for keyboard use (`:focus-visible`), not on mouse click.

## State completeness

Every interactive component must render: enabled, hover, focus, pressed,
disabled — plus selected and error where they apply. Emitting only hover and
disabled is the most common a11y defect in hand-built M3 components.

Disabled content sits at 38% opacity, disabled containers at 12%, and a
disabled element takes no state layer. Do not signal disabled with colour
alone, and do not leave a disabled control focusable without explanation.

## Semantics

- Use native elements first: `<button>`, `<a href>`, `<input>`, `<select>`.
  Material web components already carry the right role — do not re-declare it.
- Icon-only controls need an accessible name: `aria-label` (or `label=` on
  Material elements). A FAB, an icon button, a close affordance — all of them.
- Toggles need a label describing both states: "Add to favourites" /
  "Remove from favourites", plus `aria-pressed`.
- Keep DOM order equal to visual order so tab order follows reading order.
- Announce state that changes without a page load — a toast, an inline
  validation error, a filter result count — with a live region.
- Give dialogs and bottom sheets focus management: move focus in on open,
  trap it, return it to the trigger on close, and close on `Escape`.

## Motion, transparency & forced colors

### Vestibular safety (`prefers-reduced-motion`)

Honour `prefers-reduced-motion`. Keep a short cross-fade (`120ms linear`) so state
changes stay perceptible, and remove every spatial spring that moves, scales or
morphs the layout. `assets/tokens/md3e-motion.css` and `assets/tokens/md3e-spring.js`
already do this; verify custom `@keyframes` or WAAPI animations never bypass it.

Springs help here: because they are interruptible, a user who changes their
mind is not forced to watch an animation finish. Avoid motion that cannot be
interrupted, and never animate anything that could trigger discomfort —
parallax, large zooms, spins.

### Transparency & blur (`prefers-reduced-transparency`)

> **Layer 2 — Web Implementation:** Material 3 component specs rely on opaque tonal `surface-container-*` elevation; frosted translucency is a Web adaptation provided via `assets/tokens/md3e-blur.css`.

Whenever floating chrome uses `backdrop-filter: blur(...)` (`.md3e-frosted-surface`), pair it with **`color-mix(in oklab, ...)`** (never `in oklch` on neutral surfaces, which triggers powerless-hue tinting and fails `MD3E018` as `[ERROR]`) and an explicit solid fallback under `@media (prefers-reduced-transparency: reduce)`, `@media (prefers-contrast: more)`, and `[data-contrast="high"]` (`background: var(--md-sys-color-surface-container); backdrop-filter: none;`). Missing the reduced-transparency fallback fails `MD3E022` at `[ERROR]` severity.

### Windows High Contrast (`forced-colors: active`)

Under `@media (forced-colors: active)`, browsers replace author colours with
system palette keywords (`Canvas`, `CanvasText`, `Highlight`, `ButtonText`):

- Never suppress outlines with `outline: none` on borderless inputs or search
  bars — use `outline: 2px solid transparent;` so forced-colors focus borders
  remain visible.
- Override `:focus-visible` to `outline: var(--md-sys-focus-ring-width) solid Highlight;`
  with `outline-offset: var(--md-sys-focus-ring-gap);` (already handled in
  `md3e-tokens.css`), and reset frosted/tinted overlays to `Canvas` / `CanvasText`
  with a `1px solid CanvasText` border and `backdrop-filter: none`.

## Text scaling

Support at least **200% text zoom** without loss of content or function. Use
relative units where layout allows, cap text containers so they wrap rather
than clip, and avoid fixed-height boxes around text — a fixed height is also
what breaks when a CJK or Arabic locale increases line height by ~7%.

Prefer rem for text and spacing, px for hairline borders and icon glyphs.

## Internationalisation

- Line height adapts to the language's script height category (see
  `typography.md`). Default to the **medium** category (~7% taller) — Chinese,
  Japanese, Korean, Arabic, Hindi and Thai all need it.
- Never bake copy into images.
- Test with the longest plausible string in the target language; M3 labels use
  sentence case, which is shorter than uppercase in some scripts but longer in
  German.
- Support RTL by using logical properties (`margin-inline-start`, not
  `margin-left`) so the whole layout mirrors from one switch.

## Checklist

- [ ] All contrast pairs use a matching `on-` role
- [ ] A high-contrast path exists
- [ ] Colour is never the only signal
- [ ] Pointer hit area meets WCAG 2.2 AA `>= 24×24 px` floor (`[ERROR]` in `MD3E006`) and expands toward M3 recommended `>= 48×48 px` via `::before` without inflating XS/S visual geometry (`[WARNING]`), with `>= 8px` separation
- [ ] Every interactive element has a visible `:focus-visible` indicator
- [ ] Hover / focus / pressed / disabled / selected states all render
- [ ] Icon-only controls have accessible names
- [ ] Dialogs trap and restore focus, close on `Escape`
- [ ] `prefers-reduced-motion` is honoured
- [ ] `prefers-reduced-transparency` and `forced-colors: active` fallbacks are intact
- [ ] 200% zoom keeps all content reachable
- [ ] CJK/Arabic line-height adaptation considered
- [ ] Layout mirrors for RTL via logical properties
