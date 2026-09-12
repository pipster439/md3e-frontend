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
other never reflows the layout. Only weight — and at the two smallest sizes
tracking — changes.

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

| Axis | Range | Effect |
|---|---|---|
| `wght` | 100–1000 | stroke thickness |
| `opsz` | 6–144 | letterform proportions at a given size |
| `ROND` | 0–100 | corner and terminal curvature, sharp → round |
| `wdth` | 25%–151% | compression, ultra-condensed → expanded |
| `slnt` | −10°–0° | slant |

Two Expressive uses worth knowing:

1. **Roundness matches your shapes.** `ROND` is why M3 shapes and Google Sans
   Flex look like they belong together. If you use the shape library, set a
   non-zero `ROND` so type and containers share a roundness story.
2. **Axes as motion.** Animating `wght` or `wdth` on a label is a legitimate
   Expressive feedback channel — a toggle that thickens when it activates. Keep
   it short and driven by an effects spring (axis changes do not move the
   element, so no overshoot).

```css
.label { font-variation-settings: "wght" 500, "opsz" 14, "ROND" 25; }
```

Never animate `font-size` to get emphasis — it reflows text and drops frames.
Animate weight instead.

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
