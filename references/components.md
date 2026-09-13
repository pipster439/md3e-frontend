# Components — index and shared rules

Source: the component spec pages on <https://m3.material.io>, retrieved
2026-09-12 by rendering each page in a real browser (the site is
JavaScript-rendered; a plain fetch returns only the page title).

**This file is the index.** The per-component specifications — variants,
configuration matrices, anatomy, colour roles, states, shape and morph
behaviour, measurement tables and page-level cautions — live in six group
files, ~3,700 lines total, covering all 36 components:

| Group file | Components |
|---|---|
| `components/action.md` | Buttons · Icon buttons · FAB · Extended FAB · FAB menu · Split button · Button groups · Segmented buttons |
| `components/communication.md` | Badges · Progress indicators · Loading indicator · Snackbar · Tooltips |
| `components/containment.md` | Cards · Dialogs · Bottom sheets · Side sheets · Carousel · Lists · Divider · Menus |
| `components/navigation.md` | App bars · Toolbars · Navigation bar · Navigation rail · Navigation drawer · Tabs · Search |
| `components/selection.md` | Checkbox · Chips · Radio button · Switch · Sliders |
| `components/text-input.md` | Text fields · Date pickers · Time pickers |

Read the group file for the component you are building. Do not work from
memory — several of the values below exist nowhere else in a form you could
guess (the square-button corner radius is not the round-button one, and the
pressed radius is a third value again).

### A note on `—`

A `—` in a group file means the value was not present in the rendered page
text *and* had no measurement diagram available. Material publishes a
significant share of its dimensions only as images. Where a diagram existed it
has been read and the value transcribed. `—` is an honest gap, not a missing
edit: **do not interpolate a value to fill one.** If you need it, open the
spec page and read the diagram yourself.

## The 14 Expressive components

**New:** button groups · FAB menu · loading indicator · split button · toolbars

**Updated:** app bars · common buttons · extended FAB · FABs · icon buttons ·
navigation bar · navigation rail · progress indicators · sliders · carousel

Each gained more configuration, more shape options, emphasized text and
Expressive motion. Two structural changes matter beyond styling:

- The baseline **bottom app bar is no longer recommended** in Expressive. Consider a **docked toolbar** (same job,
  shorter, more flexible) or a **floating toolbar** (more actions, freer
  placement).
- The **loading indicator** replaces most uses of the indeterminate circular
  progress indicator, for waits under about five seconds. It is used by
  pull-to-refresh.

Other deprecations worth knowing, found on the spec pages:

- **Baseline lists are "not recommended"** — use expressive lists.
- **Baseline navigation bar / rail** configurations are superseded by the
  flexible Expressive ones.
- The **small FAB (40dp)** and **surface FAB** remain available but are no longer recommended; a medium FAB
  (80dp) was added.

## Button emphasis, in order

`filled` → `filled tonal` → `elevated` → `outlined` → `text`

Use filled buttons for the actions needing strongest emphasis. The right count
depends on the view and task; there is no universal one-per-view limit.

| Variant | Container | Content | Use for |
|---|---|---|---|
| Filled | `primary` | `on-primary` | High-emphasis action |
| Filled tonal | `secondary-container` | `on-secondary-container` | Secondary action beside a filled button |
| Elevated | `surface-container-low` | `primary` | Medium emphasis on a coloured or busy background |
| Outlined | transparent + `outline` | `on-surface-variant` | Medium emphasis, neutral |
| Text | transparent | `primary` | Lowest emphasis: dialog actions, inline links |

Toggle buttons (new in Expressive) use **different** colour roles from the
default button of the same variant, and the text style has no toggle at all.
See `components/action.md` for the toggle mappings.

## Button sizes and corner radii

Five sizes replaced the single 40dp button, so a button can match the density of
what surrounds it. **Small (40dp) is the default** and is the pre-Expressive
size.

| Size | Container height | Label padding | Icon size | With icon: leading pad / gap / trailing pad |
|---|---|---|---|---|
| Extra small | 32dp | 12dp | 20dp | 12 / 4 / 12dp |
| Small (default) | 40dp | 16dp | 20dp | 16 / 8 / 16dp |
| Medium | 56dp | 24dp | 24dp | 24 / 8 / 24dp |
| Large | 96dp | 48dp | 32dp | 48 / 12 / 48dp |
| Extra large | 136dp | 64dp | 40dp | 64 / 16 / 64dp |

Corner radii differ by size **and** by shape, and the pressed state is a third
value:

| | XS | S | M | L | XL |
|---|---|---|---|---|---|
| Round button | full | full | full | full | full |
| Square button | 12dp | 12dp | 16dp | 28dp | 28dp |
| Pressed state | 8dp | 8dp | 12dp | 16dp | 16dp |

The two shapes must share the same pressed radius. Small button padding changed
in the Expressive update: **16dp** is now recommended, 24dp is the M3 value and
is no longer recommended.

On touch-first layouts, check that extra-small and small controls have an
adequate effective tap area. Android recommends 48dp; Web WCAG 2.2 AA has a
24 CSS px target criterion with stated exceptions.

## Other frequently needed values

Verified against the official measurement diagrams or page text. Where a value
is absent here, read the group file.

| Component | Value |
|---|---|
| Icon buttons | container 32 / 40 / 56 / 96 / 136dp; narrow widths 28 / 32 / 48 / 64 / 104dp; wide widths 40 / 52 / 72 / 128 / 184dp; icon 20 / 24 / 24 / 32 / 40dp |
| FAB | 56×56 · 80×80 · 96×96dp; icon 24 / 28 / 36dp; corner 16 / 20 / 28dp |
| Extended FAB | height 56 (small) · 80 · 96dp |
| FAB menu item | height 56dp |
| Chip | height 32dp; corner 8dp; icon 18dp; padding 16dp (8dp with icon); between elements 8dp |
| Input chip | avatar 24dp, avatar corner 12dp; close icon target ≥48dp |
| Text field | height 56dp; padding 16dp (12dp with icons); icon-to-text 16dp; supporting text top padding 4dp; supporting text ↔ counter 16dp |
| Navigation drawer | width 360dp; active indicator 56dp high, 336dp wide, 28dp corner; left/right padding 28dp |
| Navigation rail | collapsed 96dp wide; expanded 220–360dp wide; item 56dp; icon 24dp |
| Divider | inset 16dp left / 0 right; middle-inset 16dp both; 4dp to supporting text |
| Menu | corner `extra-small` (4dp); item height 48dp |
| Switch | track 52×32dp; thumb 16 unselected / 24 selected / 28 pressed |
| Checkbox | container 18dp, corner 2dp, icon 18dp, target 48dp, state layer 40dp |
| Radio button | icon 20dp, state layer 40dp, target 48dp |
| Segmented button | height 40dp; outer corners `full` |
| Linear progress | track 4dp; 4dp gap to the indicator |
| Circular progress | 48dp |
| List item | 56 / 72 / 88dp (one / two / three line) |

## State completeness

Every interactive component needs enabled, hover, focus, pressed and disabled —
plus selected where it applies. Material components ship this; a custom
component must reimplement it.

| State | Visual |
|---|---|
| Hover | state layer 8% in the content colour |
| Focus | focus ring, or state layer 10%. Expressive added an **inset focus ring** that replaces opacity-only focus indication |
| Pressed | state layer 10% |
| Dragged | state layer 16% |
| Disabled | container 12%, content 38%, no state layer |
| Selected | an indicator in `secondary-container`, not merely a colour change |

The state layer is **40dp**; the interactive target around it is **48dp**. Only
one state layer may be active at a time.

## Shape morph

When pressed, a button may morph to become more square — round and square
buttons share the same pressed radius. A toggle button also changes its resting
shape: round when unselected becomes square when selected, and if the unselected
resting shape is square then the selected one should be round. Filter and input
chips gained shape morphing in the Expressive update.

Spatial springs are a good default for Material-style shape morphs. Verify the
motion's purpose and reduced-motion behaviour in the browser.

## Web implementation reality check

- `@material/web` exposes `md-filled-button`, `md-outlined-button`,
  `md-text-button`, `md-elevated-button`, `md-filled-tonal-button`,
  `md-icon-button`, `md-fab`, `md-extended-fab`, `md-checkbox`, `md-radio`,
  `md-switch`, `md-linear-progress`, `md-circular-progress`. It is in
  maintenance mode — no new Expressive components are being added to it.
- Split button, button group, toolbar, FAB menu and loading indicator have **no**
  `@material/web` element. Build them from tokens and the measurements in the
  group files, and treat the result as a spec-aligned approximation.
- React / Vue / Svelte have no official Material library. Use CSS custom
  properties plus thin wrapper components.
- Per-component tokens follow `--md-<component>-<part>-<property>`
  (e.g. `--md-filled-button-container-shape`), and component tokens should point
  at system tokens, never at raw values.
