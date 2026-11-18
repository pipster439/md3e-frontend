# Layout and adaptivity — Material 3 Expressive

Source: <https://m3.material.io/foundations/layout/breakpoints>

## Breakpoints

Five breakpoints (formerly "window size classes"). They apply to Android and
web. Design for the breakpoint, **never** for a specific device — available
space is dynamic (split screen, unfold, resize) and changes during a session.

| Breakpoint | Width | Typical context |
|---|---|---|
| Compact | < 600px | Phone portrait |
| Medium | 600–839px | Tablet portrait, unfolded foldable, phone landscape |
| Expanded | 840–1199px | Tablet landscape, desktop window |
| Large | 1200–1599px | Desktop, laptop |
| Extra-large | 1600px+ | Large desktop, ultrawide |

Height breakpoints also exist (compact < 480, medium 480–899, expanded ≥ 900)
but are rarely needed, because most layouts scroll vertically.

```css
/* Compact is the default; layer up. */
@media (min-width: 600px)  { /* medium */ }
@media (min-width: 840px)  { /* expanded */ }
@media (min-width: 1200px) { /* large */ }
@media (min-width: 1600px) { /* extra-large */ }
```

## Panes, navigation, communication, action

| Breakpoint | Panes | Navigation | Communication | Action |
|---|---|---|---|---|
| Compact | 1 | Navigation bar, or modal expanded nav rail | Simple dialog | Full-screen dialog, bottom sheet |
| Medium | 1 (2 recommended for low-density content) | Navigation bar, or modal expanded nav rail | Simple dialog | Menu |
| Expanded | 1 or 2 (2 recommended) | Modal or standard expanded nav rail | Simple dialog | Menu |
| Large | 1 or 2 (2 recommended) | Modal or standard expanded nav rail | Simple dialog | Menu |
| Extra-large | 1 to 3 (3 recommended) | Modal or standard expanded nav rail | Simple dialog | Menu |

Rule of thumb: two panes at medium only when content is low-density with clear
actions. Two panes with high information density at medium reduces usability.

## Moving from one breakpoint to the next

Ask five questions, in order:

1. **What should be revealed?** Larger windows show what smaller ones hide — a
   nav rail that is collapsed opens by default; a second pane appears.
   Extra space is not "make the same thing bigger".
2. **How should the screen be divided?** 1 pane (compact/medium) → 2 panes
   (expanded/large) → consider 3 (extra-large).
3. **What should be resized?** Text measure, media, and side panes. Cap body
   width so lines do not become unreadable on a wide monitor.
4. **What should be repositioned?** FABs, toolbars, actions move to where the
   thumb or cursor already is.
5. **What should be swapped?** The component changes, not just its size: a
   navigation bar becomes a navigation rail becomes a drawer; a simple dialog
   becomes a menu; a bottom sheet becomes a side sheet.

## Canonical layouts

Three layouts the spec names. Pick one per view instead of inventing a grid:

- **List-detail** — a list pane plus a detail pane. Expanded and above.
- **Supporting pane** — a primary pane with a secondary supporting pane for
  context, at expanded and above.
- **Feed** — a scrollable feed that reflows its column count with the
  breakpoint.

## Grid, margins, gutters, and pane gaps

| Breakpoint | Width | Columns | Margin | Gutter | Pane gap (multi-pane) |
|---|---|---|---|---|---|
| Compact | `< 600px` | 4 | 16dp | 16dp | — (single pane) |
| Medium | `600–839px` | 8 | 24dp | 24dp | 24dp (when 2-pane) |
| Expanded | `840–1199px` | 12 | 24dp | 24dp | 24dp |
| Large | `1200–1599px` | 12 | 24dp | 24dp | 24dp |
| Extra-large | `>= 1600px` | 12 | 24dp | 24dp | 24dp |

Tokens: `--md-sys-breakpoint-compact` (`600px`), `--md-sys-breakpoint-medium` (`840px`),
`--md-sys-breakpoint-expanded` (`1200px`), `--md-sys-breakpoint-large` (`1600px`),
`--md-sys-breakpoint-extra-large` (`1600px`), `--md-sys-layout-margin-compact` (`16px`),
`--md-sys-layout-margin-medium` (`24px`), `--md-sys-layout-margin-expanded` (`24px`),
`--md-sys-layout-margin-large` (`24px`), `--md-sys-layout-margin-extra-large` (`24px`),
`--md-sys-layout-gutter-*`, `--md-sys-layout-pane-gap` (`24px`), and
`--md-sys-layout-measure-max` (`68ch`).
Spacing uses a 4px base grid — `--md-sys-spacing-1` (4px) through `--md-sys-spacing-20` (80px),
with `--md-sys-spacing-6` (`24px`) / `--md-sys-layout-pane-gap` as the standard gap between adjacent panes.

## Desktop & Wide-Screen Optimization (`Expanded 840px+` / `Large 1200px+` / `Extra-large 1600px+`)

Desktop viewports (`>= 840px`, especially `Large 1200–1599px` and `Extra-large >= 1600px`) are not stretched mobile screens — structure the workspace deliberately around wide-screen ergonomics:

1. **Collapsible <-> Standard Expanded Navigation Rail (never a bottom bar on desktop):**
   - Never keep a bottom Navigation Bar on `Expanded` (`>= 840px`) or larger viewports.
   - Use a persistent **Navigation Rail** that toggles between **Collapsed** (`--md-sys-nav-rail-width-collapsed: 80px` compact desktop rail; M3E spec allows up to `96dp` for vertical pills) and **Standard Expanded** (`--md-sys-nav-rail-width-expanded: 220px`, within the `220–360dp` official range, displaying horizontal indicator pills with inline labels + a docked Extended FAB / primary action in the rail header).
   - **Default expanded on `Large >= 1200px`**, collapsible via the top-left `menu` / `menu_open` trigger or keyboard shortcut, and sliding as a modal rail sheet on `< 840px`. See [`components/navigation.md`](components/navigation.md#navigation-rail).

2. **Multi-pane desktop shell & prose measure cap:**
   - Frame the desktop app shell on `--md-sys-color-surface-container` with scrollable content panes on `surface` or `surface-container-lowest`, `24px` (`var(--md-sys-shape-corner-extra-large)` / `corner-large`–`extra-large`) rounded pane corners, and `--md-sys-layout-pane-gap` (`24px`) separation between adjacent panes.
   - Use `1–2` panes at `Expanded`/`Large` (`840–1599px`) and `2–3` panes at `Extra-large` (`>= 1600px`), matching List-detail or Supporting-pane canonical layouts.
   - Cap body prose containers to `max-width: var(--md-sys-layout-measure-max, 68ch)` so readable line lengths never stretch across `1440px–1920px` monitors.

3. **Desktop Visual Density (`0`, `-1`, `-2`):**
   - Apply official M3 density steps to tighten desktop information density without shrinking readable copy or icons:
     - Standard (`0`, default): `--md-sys-density-step: 0; --md-sys-density-offset: 0px;`
     - Compact (`data-density="compact"` or `"-1"`): `--md-sys-density-step: -1; --md-sys-density-offset: -4px;`
     - Dense (`data-density="dense"` or `"-2"`): `--md-sys-density-step: -2; --md-sys-density-offset: -8px;`
   - Density adjusts container heights (buttons, inputs, list items) while preserving `--md-sys-typescale-*` sizes, `--md-sys-icon-size`, and invisible `48×48px` hit targets (`::before` touch area).

4. **Fine-pointer ergonomics, keyboard shortcuts & themed scrollbars:**
   - Gate pointer-only hover enhancements and subtle `<kbd>` shortcut hints behind `@media (hover: hover) and (pointer: fine)` so touch devices stay uncluttered.
   - Support keyboard navigation across toolbars/menus/rails with **roving `tabindex`**, **`aria-keyshortcuts`** on primary triggers (ignoring bare single-key shortcuts when focus is inside `<input>`, `<textarea>`, `<select>`, or `[contenteditable]`), and **`Escape`** to close popovers, FAB menus, and sheets with focus restoration.
   - Style desktop scrollbars with `scrollbar-color: var(--md3e-scrollbar-thumb, var(--md-sys-color-outline)) transparent; scrollbar-width: thin;` (using `--md-sys-color-outline` `>= 4.3:1` contrast rather than `outline-variant`, with `prefers-contrast: more`, `pointer: coarse`, `forced-colors: active`, and `@supports not (scrollbar-color: auto)` fallbacks handled in `md3e-tokens.css`).

5. **Canonical desktop component swaps & Floating Toolbar clearance:**
   - Swap mobile **Bottom Sheets** (`< 840px`) for **Side Sheets** (`400px` max-width on `>= 840px`; see [`components/containment.md`](components/containment.md#side-sheets)).
   - Swap contextual **Simple Dialogs** for anchored **Menus** where desktop pointer precision makes inline selection faster.
   - Always reserve bottom scroll clearance (`padding-block-end: 112px` or equivalent bottom inset) on the main scrollable pane whenever a fixed **Floating Toolbar** or **FAB** is active so bottom cards and actions are never occluded at max scroll.

## Component flexibility (Expressive)

Expressive layout is about the UI adapting to context, not just stretching.
Shift components or controls depending on the environment to make tasks easier:
an expressive app bar that collapses, a toolbar that goes vertical, a button
group that redistributes width. Component containers use flexible layout
techniques to adapt to available space — they either distribute space evenly
for symmetry, or place elements strategically to establish hierarchy and guide
interaction.

Toolbars are the clearest example: docked when actions are few and stable,
floating when there are many or their placement needs to vary.

## Do / Don't

| Do | Don't |
|---|---|
| Design at each breakpoint deliberately | Stretch a compact layout to 1600px |
| Cap body text measure | Let a paragraph run 140 characters wide |
| Swap the navigation component | Keep a bottom nav bar on desktop |
| Use a canonical layout | Invent a bespoke grid per screen |
| Reveal content as space appears | Scale everything up proportionally |
| Support 200% zoom and reflow | Assume the window size is fixed |
