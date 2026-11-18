# Typography — Material 3 Expressive

Source: <https://m3.material.io/styles/typography/type-scale-tokens>

## The scale

Five roles — **display, headline, title, body, label** — each in three sizes.
That is 15 **baseline** styles. M3E adds 15 **emphasized** styles: same one
scale from Display Large to Label Small, same roles, heavier weight.

Baseline and emphasized are meant to be used *together*. Emphasized is not a
replacement set; it is a spotlight.

| Role | Size / line-height | Baseline weight | Tracking | Emphasized weight | Emph. tracking |
|---|---|---|---|---|---|
| Display Large | 57 / 64 | 400 | −0.25 | 500 | 0 |
| Display Medium | 45 / 52 | 400 | 0 | 500 | 0 |
| Display Small | 36 / 44 | 400 | 0 | 500 | 0 |
| Headline Large | 32 / 40 | 400 | 0 | 500 | 0 |
| Headline Medium | 28 / 36 | 400 | 0 | 500 | 0 |
| Headline Small | 24 / 32 | 400 | 0 | 500 | 0 |
| Title Large | 22 / 28 | 400 | 0 | 500 | 0 |
| Title Medium | 16 / 24 | 500 | 0.15 | 700 | 0 |
| Title Small | 14 / 20 | 500 | 0.1 | 700 | 0 |
| Body Large | 16 / 24 | 400 | 0.5 | 500 | 0 |
| Body Medium | 14 / 20 | 400 | 0.25 | 500 | 0 |
| Body Small | 12 / 16 | 400 | 0.4 | 500 | 0.1 |
| Label Large | 14 / 20 | 500 | 0.1 | 700 | 0 |
| Label Medium | 12 / 16 | 500 | 0.5 | 700 | 0.1 |
| Label Small | 11 / 16 | 500 | 0.5 | 700 | 0.1 |

Values are px on the web (dp/sp on device). Sizes and line heights are
**identical** between baseline and emphasized, so swapping one token for the
other never reflows the layout. Only weight — and tracking (to `0`, or `0.1px`
at the three smallest sizes: Body Small, Label Medium, Label Small) — changes.

**Emphasized weight rule:** baseline 400 → 500, and baseline 500 → 700. On a
variable font the spec's 700 maps to around `wght: 600`.

## Choosing a role

| Role | Use for | Never use for |
|---|---|---|
| Display | Hero numbers, splash headlines, one per screen | Anything you expect people to read in sequence |
| Headline | Section and screen headings, editorial moments | Body copy |
| Title | Card titles, list headers, dialog titles, app bar | Long paragraphs |
| Body | All paragraph and descriptive text | Button labels |
| Label | Buttons, chips, tabs, captions, badges | Multi-line prose |

A product does not use all 15 styles. Pick the five or six that fit and use
them consistently — the scale is a menu, not a checklist.

## Emphasized styles

Where the spec calls for them:

- Badges and unread indicators
- Buttons, for the primary action
- Extended FAB labels
- Selected list items and selected menu items

Component guidelines: Material components do **not** use emphasized styles by
default. To apply one, swap the baseline token for the emphasized token of the
same style.

```css
/* baseline */      font-weight: var(--md-sys-typescale-title-medium-weight);
/* emphasized */    font-weight: var(--md-sys-typescale-title-medium-emphasized-weight);
```

Two independent axes, and they compose:

- **Weight emphasis** — apply to text that is already bold, for a bolder look.
- **Context emphasis** — apply selectively to communicate state or hierarchy
  (a selected tab, an unread row, the screen's primary action).

Use emphasized styles sparingly enough that they still mean something. If
everything is emphasized, nothing is.

## Typefaces

The scale has two typeface slots:

- **Brand typeface** → larger styles (Display, Headline), where expression
  matters.
- **Plain typeface** → smaller styles (Body, Label), where readability matters.

Roboto is the default for both. Replacing them is the highest-leverage brand
move available, and it is a token change, not a redesign:

```css
:root {
  --md-sys-typescale-brand-font: "Your Display Face", Georgia, serif;
  --md-sys-typescale-plain-font: "Your Text Face", system-ui, sans-serif;
}
```

## Variable fonts

M3E leans on variable font axes to express emotion without changing layout.
Google Sans Flex and Roboto Flex expose:

| Axis | Range | Effect | Zero reflow? |
|---|---|---|---|
| `wght` | `100–1000` | stroke thickness | Near-zero (minor glyph advance shift unless tabular/paired with `GRAD`) |
| `GRAD` | `-50–200` (Google Sans Flex) / `-200–150` (Roboto Flex) | optical grade / weight density at fixed advance width | **100% zero reflow** |
| `ROND` | `0–100` (Google Sans Flex) | corner and terminal curvature, sharp → round | **100% zero reflow** |
| `opsz` | `6–144` / `8–144` | optical letterform proportions at display vs caption scale | Static per role |
| `wdth` | `25%–151%` | horizontal compression, ultra-condensed → expanded | Layout-affecting |

Google Fonts CSS2 `<head>` loading (axes **must** be strictly sorted alphabetically, uppercase A–Z before lowercase):

```html
<!-- Google Sans Flex (GRAD, ROND, opsz, wdth, wght) + Roboto Flex fallback -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:GRAD,ROND,opsz,wdth,wght@-50..200,0..100,6..144,25..151,100..1000&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:GRAD,opsz,wdth,wght@-200..150,8..144,25..151,100..1000&display=swap">
```

### Spring-Driven `GRAD` / `ROND` / `wght` Transitions

Never animate `font-size` to get emphasis — it reflows text and drops frames. Register custom axis properties with `@property` so CSS spring tokens drive `GRAD`, `ROND`, and `wght` smoothly in real time:

- **Color/grade/weight emphasis (`GRAD`, `wght`)**: drive with `--md-sys-motion-fast-effects` (critically damped — no wobble).
- **Shape-matched terminal rounding (`ROND`)**: drive `0 -> 100` with `--md-sys-motion-default-spatial` (or `createSpringAnimator` in `md3e-spring.js`) when an adjacent button or chip morphs between square and pill/cookie!

```css
@property --md3e-vf-wght { syntax: "<number>"; inherits: false; initial-value: 500; }
@property --md3e-vf-grad { syntax: "<number>"; inherits: false; initial-value: 0; }
@property --md3e-vf-rond { syntax: "<number>"; inherits: false; initial-value: 25; }

.md3e-vf-expressive-label {
  --md3e-vf-wght: 500;
  --md3e-vf-grad: 0;
  --md3e-vf-rond: 20;
  font-family: "Google Sans Flex", "Roboto Flex", var(--md-sys-typescale-plain-font);
  font-variation-settings:
    "wght" var(--md3e-vf-wght),
    "GRAD" var(--md3e-vf-grad),
    "ROND" var(--md3e-vf-rond),
    "opsz" 16;
  transition:
    --md3e-vf-wght var(--md-sys-motion-fast-effects),
    --md3e-vf-grad var(--md-sys-motion-fast-effects),
    --md3e-vf-rond var(--md-sys-motion-default-spatial);
}

.md3e-vf-expressive-label:hover {
  --md3e-vf-grad: 60;
  --md3e-vf-rond: 80;
}

.md3e-vf-expressive-label:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-vf-expressive-label[aria-pressed="true"] {
  --md3e-vf-wght: 650;
  --md3e-vf-grad: 110;
  --md3e-vf-rond: 100;
}

@media (prefers-reduced-motion: reduce) {
  .md3e-vf-expressive-label {
    transition: none;
  }
}
```

## View Transitions Container Expansion (M3E Spatial Container Transform)

For card-to-detail expansions, filter chips expanding into search sheets, or docked/floating toolbar mode swaps, pair the **View Transitions API** with M3E's `default-spatial` spring tokens (`--md-sys-motion-default-spatial-duration` and `--md-sys-motion-default-spatial-easing`):

1. Prefer element-scoped `scopeEl.startViewTransition(...)` when supported (`'startViewTransition' in Element.prototype`) so page chrome and popovers stay interactive; fall back cleanly to `document.startViewTransition(...)` or immediate DOM updates.
2. Assign a matching `view-transition-name` to only **one** visible source element before the DOM update and **one** visible destination element after it (duplicate names abort the transition), then remove temporary names in `transition.finished.finally(...)`.
3. Set `width: fit-content;` on shared headline elements so aspect ratios do not smear horizontally, catch rapid-retrigger `transition.ready.catch(() => {})`, route keyboard focus to the revealed heading (`tabindex="-1"`), and suppress View Transition animations under `@media (prefers-reduced-motion: reduce)`.

```css
.md3e-vt-card {
  border-radius: var(--md-sys-shape-corner-extra-large);
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  cursor: pointer;
}

.md3e-vt-card.is-vt-active,
.md3e-vt-detail[data-open="true"] {
  view-transition-name: md3e-hero-container;
}

.md3e-vt-card.is-vt-active .md3e-vt-title,
.md3e-vt-detail[data-open="true"] .md3e-vt-title {
  view-transition-name: md3e-hero-title;
  width: fit-content;
}

::view-transition-group(md3e-hero-container),
::view-transition-group(md3e-hero-title) {
  animation-duration: var(--md-sys-motion-default-spatial-duration);
  animation-timing-function: var(--md-sys-motion-default-spatial-easing);
}

::view-transition-old(md3e-hero-container),
::view-transition-new(md3e-hero-container) {
  height: 100%;
  border-radius: var(--md-sys-shape-corner-extra-large);
  overflow: clip;
}

@media (prefers-reduced-motion: reduce) {
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}
```

```javascript
export function expandWithContainerTransform(sourceCard, detailDialog, { returnFocusTo = sourceCard } = {}) {
  const detailHeading = detailDialog.querySelector('[data-vt-heading]');
  sourceCard.classList.add('is-vt-active');

  const applyOpen = () => {
    sourceCard.classList.remove('is-vt-active');
    sourceCard.hidden = true;
    detailDialog.dataset.open = 'true';
    detailDialog.hidden = false;
  };

  if (typeof document.startViewTransition !== 'function') {
    applyOpen();
    detailHeading?.focus();
    return;
  }

  const transition = document.startViewTransition(applyOpen);
  transition.ready.catch(() => {});
  transition.finished.finally(() => {
    detailHeading?.focus();
  });

  detailDialog.addEventListener('close', () => {
    const closeDom = () => {
      detailDialog.dataset.open = 'false';
      detailDialog.hidden = true;
      sourceCard.hidden = false;
      sourceCard.classList.add('is-vt-active');
    };
    if (typeof document.startViewTransition !== 'function') {
      closeDom();
      sourceCard.classList.remove('is-vt-active');
      returnFocusTo?.focus();
      return;
    }
    const back = document.startViewTransition(closeDom);
    back.ready.catch(() => {});
    back.finished.finally(() => {
      sourceCard.classList.remove('is-vt-active');
      returnFocusTo?.focus();
    });
  }, { once: true });
}
```

## Language height (do not skip this for CJK)

The spec adapts line height to the language's script height category. The
baseline table above is the **small** category — Latin, Cyrillic, Greek,
Hebrew.

| Category | Height | Scripts |
|---|---|---|
| Small (base) | — | Latin (except Vietnamese), Cyrillic, Greek, Hebrew |
| Medium | ~7% taller | **Chinese, Japanese, Korean**, Arabic, Hindi, Thai, Vietnamese, and most other scripts |
| Large | ~30% taller | Burmese, Telugu |
| Extra large | ~100% taller | Nastaliq |

Default to **medium** when the product ships any non-Latin script, and switch
per detected language. Components with fixed heights are built for the small
category and will overlap text if you ignore this — for a product that ships
Chinese, Japanese or Korean, this is the difference between a working UI and a
broken one.

`assets/tokens/md3e-tokens.css` ships complete `:lang(zh)`, `:lang(ja)`, `:lang(ko)`, `:lang(ar)`, `:lang(hi)`, `:lang(th)`, `:lang(vi)` overrides for all 15 `--md-sys-typescale-*-line-height` tokens (`68 / 56 / 48 / 44 / 38 / 34 / 30 / 26 / 22 / 26 / 22 / 18 / 22 / 18 / 18px`):

```css
:lang(zh), :lang(ja), :lang(ko) {
  --md-sys-typescale-display-large-line-height: 68px;  /* 64 × 1.07 */
  --md-sys-typescale-body-large-line-height: 26px;     /* 24 × 1.07 */
}
```

## Common mistakes

| Don't | Do |
|---|---|
| `font-size: 13px` | A token — 13 is not on the scale |
| `font-weight: bold` sprinkled ad hoc | The emphasized weight token |
| Uppercase button labels | Sentence case (uppercase was M2) |
| Interchangeable "medium/bold" everywhere | Two weights: 400/500 baseline, 500/700 emphasized |
| Display style for a paragraph | Body style at the right size |
| Fixed 64px line height shipped to a CJK audience | Language-height adaptation |
| `letter-spacing` invented per component | Role tracking values from the table |
