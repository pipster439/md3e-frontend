# Accessibility — Material 3 Expressive

Sources: <https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum>,
<https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced>,
<https://developer.android.com/design/ui/mobile/guides/foundations/accessibility>.

M3's accessibility requirements are part of the spec, not an afterthought.
Several are the direct reason a token exists.

## Contrast

| Content | Minimum |
|---|---|
| Body text | 4.5:1 (WCAG AA), 7:1 for AAA |
| Large text (18px+, or 14px bold) | 3:1 |
| UI components, borders, icons | 3:1 |
| Focus indicator | 3:1 against adjacent colours |

Matching roles such as `on-primary` on `primary` are the intended starting
point. Check the rendered combination in each theme and state: custom palettes,
opacity, images and overlays can change contrast. A role name alone cannot
guarantee a WCAG ratio.

M3 standardises **three contrast levels** — standard, medium, high. Offer a
high-contrast path rather than assuming the default suits everyone. They are
tonal shifts of the same roles, so it costs one media query:

```css
@media (prefers-contrast: more) { /* shifted roles, see md3e-tokens.css */ }
```

Never rely on colour alone to carry meaning. Error needs an icon or a message;
selection needs an indicator, a check, or a shape change.

## Touch targets

- **Android/Material touch guidance:** aim for at least 48×48dp of clickable
  area even when the visual element is smaller.
- **Web WCAG 2.2 AA:** pointer targets are at least 24×24 CSS px, with spacing,
  inline, equivalent-control and other stated exceptions. WCAG AAA's enhanced
  target criterion is 44×44 CSS px. Larger targets are often more usable.
- Spacing should prevent accidental activation; there is no universal 8px
  minimum that applies to every pair of controls.

Expressive button sizes **XS (32)** and **S (40)** may benefit from a larger
touch area in touch-first layouts. Verify the actual clickable area and spacing:

```css
.btn-xs { height: 32px; position: relative; }
.btn-xs::before {                       /* invisible 48px hit area */
  content: ""; position: absolute; inset: -8px;
  border-radius: inherit; /* test overlap and clipping with neighbouring controls */
}
```

For a typical touch icon button, keep the glyph legible and give its hit area
enough room through padding or layout. Check the component's own dimensions.

## Focus

Every keyboard-focusable element needs a visible focus indicator. An inset
ring is one useful Material treatment, but neither that position nor a
specific 2px ring and 2px gap is a universal requirement. Check the indicator
against WCAG focus visibility and contrast criteria.

```css
:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}
```

Never `outline: none` without a replacement. If a component clips its overflow,
draw the ring on a `::after` inset by 2px instead.

`:focus-visible` is usually appropriate for keyboard focus. Do not suppress a
visible focus indicator when a pointer-focused control still needs one.

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

## Motion and vestibular safety

Honour `prefers-reduced-motion`. Keep a short cross-fade so state changes stay
perceptible, and remove every spatial spring that moves, scales or morphs the
layout. The token file already does this; verify nothing bypasses it.

Springs help here: because they are interruptible, a user who changes their
mind is not forced to watch an animation finish. Avoid motion that cannot be
interrupted, and never animate anything that could trigger discomfort —
parallax, large zooms, spins.

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
- [ ] Actual target area meets platform guidance and applicable WCAG criteria
- [ ] Every interactive element has a visible `:focus-visible` indicator
- [ ] Hover / focus / pressed / disabled / selected states all render
- [ ] Icon-only controls have accessible names
- [ ] Dialogs trap and restore focus, close on `Escape`
- [ ] `prefers-reduced-motion` is honoured
- [ ] 200% zoom keeps all content reachable
- [ ] CJK/Arabic line-height adaptation considered
- [ ] Layout mirrors for RTL via logical properties
