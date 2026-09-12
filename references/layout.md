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

## Grid, margins, gutters

| Breakpoint | Columns | Margin | Gutter |
|---|---|---|---|
| Compact | 4 | 16 | 16 |
| Medium | 8 | 24 | 24 |
| Expanded | 12 | 24 | 24 |

Tokens: `--md-sys-layout-margin-*`, `--md-sys-layout-gutter-*`. Spacing uses a
4px base grid — `--md-sys-spacing-1` (4px) through `--md-sys-spacing-20` (80px).

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
