---
name: md3e-frontend
description: Builds, restyles, or reviews front-end UI so it complies with Material 3 Expressive (M3E), the May 2025 evolution of Material Design 3. Use when a request involves Material Design 3, MD3, M3E, Material You, "material design" styling, m3.material.io, or any of its systems — dynamic colour roles, the emphasized type scale, the shape library and corner-radius scale, motion springs, expressive components (toolbars, split button, button groups, FAB menu, loading indicator), or adaptive breakpoints. Supplies complete design tokens, per-system reference data, and a deterministic compliance auditor for HTML/CSS/JS/TS/Vue/Svelte.
agent_created: true
---

# MD3E frontend

Use Material 3 Expressive as the design reference. Check current component
guidance at <https://m3.material.io> when a precise requirement matters. The
bundled CSS tokens and auditor are implementation aids, not an official
conformance certification; derived values and recommendations are identified
in the reference files.

**This is M3 Expressive, not M3.** Same system, evolved. Do not treat it as a
new version (it is not "M4"). Prefer the current component guidance over
baseline M3 or M2 examples when implementing an Expressive component.

## How to use this skill

| Job | Do this |
|---|---|
| New UI from scratch | Follow the six phases below in order |
| Restyle existing UI | Run phase 1, then the auditor, then fix by severity |
| Review someone's UI | Run `scripts/audit_md3e.py`, then read the code against the references |
| Answer a spec question | Read the relevant reference file; do not answer from memory |
| Pick colours / shapes / motion values | Read the reference; never guess a hex or a radius |

## Defaults and accessibility checks

1. Prefer system colour roles for themeable UI. Define literal colours in a
   palette or token layer when needed; verify actual contrast in each theme.
   Matching container/`on-` roles are good defaults, not a contrast guarantee
   after customization, overlays or state changes.
2. Start with the corner-radius and type scales, then adjust for a documented
   component need, brand choice or readability. The scales are defaults, not
   exhaustive lists of permitted CSS values.
3. Use the supplied spring tokens where they suit component motion. CSS
   duration/easing transitions remain valid for other purposeful motion;
   avoid animation that obscures state or ignores reduced-motion preferences.
4. For touch-first layouts, aim for a 48×48 CSS px hit area. For Web WCAG 2.2
   AA, assess the actual pointer target against 24×24 CSS px and its spacing
   and other exceptions; a visible 32px or 40px control is not itself a failure.
5. Keep keyboard focus visible and honour reduced-motion preferences. Offer
   dark mode when the product calls for it. The focus treatment can use
   `:focus-visible` or another accessible indicator.
6. Use filled buttons for the actions that need highest emphasis; there is no
   universal exactly-one-per-view rule.
7. Run the auditor as a heuristic review, then verify findings in context.

## Phase 1 — Install the token layer

Copy the token files into the project and import them first, in this order:

```
assets/tokens/md3e-tokens.css         colour roles, type scale, shape, elevation, state, layout
assets/tokens/md3e-motion.css         motion springs (generated)
assets/tokens/md3e-material-web.css   (optional) bridge for @material/web components
```

```html
<!-- Google Material Symbols Icons -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200">

<link rel="stylesheet" href="/styles/md3e-tokens.css">
<link rel="stylesheet" href="/styles/md3e-motion.css">
<link rel="stylesheet" href="/styles/md3e-material-web.css">
```

Set the scheme and theme roots once:

```html
<html data-motion-scheme="expressive">        <!-- optional for prominent motion -->
<html data-theme="dark">                       <!-- or leave to prefers-color-scheme -->
<html data-color-variant="vibrant">            <!-- optional: Expressive colour range -->
```

If the project already has tokens, do not add a second system. Map the existing
variables onto the `--md-sys-*` names and replace usages.

If the product has its own brand colour, regenerate the tonal palettes from
that seed, then overwrite only the role values — never the role names.

## Phase 2 — Colour, typography, shape

Read `references/color.md`, `references/typography.md`, `references/shape.md`.

1. **Colour.** Walk the role-decision list in `color.md`. Assign every surface,
   action and text colour to a role. Surfaces come from the
   `surface-container-*` ladder, chosen by the elevation they should read as —
   never by an opacity you invent.
2. **Typography.** Start with a small, consistent selection from the 15 styles.
   Apply emphasized styles where the spec calls for them — primary button
   labels, badges, the selected list/menu item, the extended FAB label — and
   nowhere else. If the product ships Chinese, Japanese or Korean, switch the
   check line height with real translated content and adjust where needed.
3. **Shape.** Assign radii from the ten-step scale. Use the three "increased"
   steps when you want emphasis without going full pill. Check nested radii for
   optical roundness (`outer − padding = inner`).

## Phase 3 — Components

Read `references/components.md` for the shared rules, then the group file for
each component you are building — all 36 components are specified in
`references/components/`, transcribed from the official spec pages.

Build or verify each component against its measurement table: button emphasis
order and the five sizes (32 / 40 / 56 / 96 / 136), FAB sizes (56 / 80 / 96),
text field 56px, chip 32px, and so on. Use the group file rather than memory —
the square-button corner radius, the pressed-state radius and the toggle colour
roles are all different from what you would guess.

A `—` in a group file is an honest gap: Material publishes some dimensions only
as images. Do not interpolate a value to fill one — read the diagram on the spec
page instead.

Two structural rules that get missed:

- The baseline **bottom app bar is no longer recommended** for an Expressive
  update; consider a docked toolbar.
- The **loading indicator replaces** the indeterminate circular progress
  indicator for waits under about five seconds.
- The baseline **small FAB (40dp) remains available but is no longer
  recommended** for an Expressive update; consider a larger FAB.

### Three component strategies

1. **Google Material Web (`@material/web`)**: For standard primitives (buttons, text fields, selects, checkbox, switch, slider, dialog, menu, tabs). Include `assets/tokens/md3e-material-web.css` and use MD3E utility classes (`.md3e-size-xs` .. `.md3e-size-xl`, `.md3e-shape-square`, `.md3e-fab-medium`). See `references/material-web.md`.
2. **Pure Expressive Recipes**: For the 5 components missing from `@material/web` (docked/floating toolbars, split button, connected button groups, FAB menu, shape-morphing loading indicator, toggle buttons). See `references/components/expressive-recipes.md`.
3. **Tailwind CSS**: Use MD3E token utility classes (`bg-md-primary`, `rounded-md-lg`, `shadow-md-level2`). See `references/tailwind.md` and `assets/tailwind/`.

Complete every state: enabled, hover, focus, pressed, disabled, plus selected
where it applies. See `references/accessibility.md`.

## Phase 4 — Motion

Read `references/motion.md`.

Apply spring tokens to Material-style component motion where appropriate. Choose by two
questions: *does it move or recolour?* (spatial vs effects) and *how big is the
change?* (fast / default / slow). Most motion should be `default`.

For gesture-driven motion, use a spring that carries velocity on release — a CSS
transition restarts from zero and feels dead.

Never mix the legacy duration/easing tokens with spring tokens on the same
property.

## Phase 5 — Layout and adaptivity

Read `references/layout.md`.

Consider the five width classes (four thresholds: 600 / 840 / 1200 / 1600) and, at each relevant one, answer
the five questions: what is revealed, how is the screen divided, what is
resized, what is repositioned, what is swapped. Use a canonical layout
(list-detail, supporting pane, feed) rather than inventing a grid.

## Phase 6 — Apply Expressive tactics, then audit

Read `references/expressive-tactics.md`.

Get the base system consistent first — a screen that follows it already reads as
Material. Then choose meaningful moments for extra emphasis.

Then run the auditor and fix by severity:

```bash
python scripts/audit_md3e.py src
python scripts/audit_md3e.py src --json            # machine-readable
python scripts/audit_md3e.py src --fail-on warn    # stricter gate
```

### Finding codes

| Code | Severity | Meaning |
|---|---|---|
| MD3E001 | error | Hardcoded hex colour |
| MD3E002 | error | Hardcoded `rgb()` / `hsl()` colour |
| MD3E003 | info | Corner radius outside the default shape scale; review in context |
| MD3E004 | info | Hand-written duration/easing; review motion intent |
| MD3E005 | error | Focus indicator removed or missing |
| MD3E006 | info | Small declared control dimension; verify actual hit area |
| MD3E007 | info | Font size outside default type scale |
| MD3E008 | warn | No `prefers-reduced-motion` path |
| MD3E009 | warn | Colour roles without a dark scheme |
| MD3E010 | info | `box-shadow` used to express elevation |
| MD3E011 | info | `border-radius: 50%`; verify intended circle/ellipse |
| MD3E012 | info | Uppercase label text (M2 convention) |
| MD3E013 | warn | `transition: all` |
| MD3E014 | warn | Icon-only control with no accessible name |
| MD3E015 | info | Bottom app bar no longer recommended in Expressive |
| MD3E016 | info | Small FAB no longer recommended in Expressive |

Token and theme files are auto-detected and exempted from the hardcoded-colour
checks — that is the one place raw values are supposed to live. Name any new
token file with `tokens`, `theme`, `palette` or `md3e-` so it is recognised.

## Regenerating motion tokens

`assets/tokens/md3e-motion.css` is generated. Regenerate it after changing the
spring table, or to add a custom spring:

```bash
python scripts/spring_to_css.py --table                     # print every token
python scripts/spring_to_css.py --emit-css assets/tokens/md3e-motion.css
python scripts/spring_to_css.py --stiffness 500 --damping 0.7   # custom spring
```

## Reference index

| File | Contents |
|---|---|
| `references/material-web.md` | Google `@material/web` component catalogue, token mappings, framework setups (React/Vue/Svelte/Next) |
| `references/components/expressive-recipes.md` | Production HTML/CSS/JS recipes for missing Expressive components (Toolbars, Split button, Button group, FAB menu, Loader) |
| `references/tailwind.md` | Tailwind CSS v3 & v4 integration guide, theme extension mapping, `@theme` block |
| `references/color.md` | tonal palettes, 37 roles, role→tone mapping, state layers, fixed roles, contrast levels |
| `references/typography.md` | 30 type styles with values, emphasized rule, typefaces, variable-font axes, language height |
| `references/shape.md` | ten-step corner scale, 35 shapes, morph, optical roundness, tension |
| `references/motion.md` | spring parameters, scheme/type/speed selection, CSS implementation, legacy layer |
| `references/components.md` | index + shared rules: button emphasis and size tables, corner radii, state completeness, web reality check |
| `references/components/action.md` | Buttons · Icon buttons · FAB · Extended FAB · FAB menu · Split button · Button groups · Segmented buttons |
| `references/components/communication.md` | Badges · Progress indicators · Loading indicator · Snackbar · Tooltips |
| `references/components/containment.md` | Cards · Dialogs · Bottom sheets · Side sheets · Carousel · Lists · Divider · Menus |
| `references/components/navigation.md` | App bars · Toolbars · Navigation bar · Navigation rail · Navigation drawer · Tabs · Search |
| `references/components/selection.md` | Checkbox · Chips · Radio button · Switch · Sliders |
| `references/components/text-input.md` | Text fields · Date pickers · Time pickers |
| `references/layout.md` | breakpoints, panes, canonical layouts, grid and margins, component flexibility |
| `references/accessibility.md` | contrast, targets, focus, semantics, text scaling, i18n, checklist |
| `references/expressive-tactics.md` | the seven tactics, hero moments, anti-patterns |

## Top ten mistakes

1. `color: #6750A4` instead of `var(--md-sys-color-primary)`
2. `on-primary` text on `secondary-container`
3. A custom radius used accidentally instead of a component's specified shape
4. A percentage radius that produces unintended geometry
5. Motion timing chosen without regard to the interaction or reduced motion
6. A spatial spring on opacity, or an effects spring on position
7. Inconsistent text styles or sizes that reduce readability
8. `outline: none` with no replacement
9. Enabled and disabled only — no hover, focus or pressed
10. Every element expressive, so nothing stands out — apply the tactics
    selectively

## Sourcing rules

m3.material.io is JavaScript-rendered and renders sections lazily. A plain
fetch — including `curl` and text-extraction proxies — returns only the page
title. To read a spec you have not yet got in this skill:

1. Render the page in a real browser with devtools access.
2. **Scroll to the bottom before extracting.** Without this the measurement and
   token sections never render, and you will silently conclude the page has no
   numbers. This is the single easiest way to be confidently wrong about this
   site.
3. Extract `document.body.innerText`. That yields variants, configuration
   matrices, anatomy, colour roles, states and the token tables.
4. **Check for measurement diagrams.** A large share of dimensions exist only as
   images. Find them with
   `[...document.querySelectorAll('img')].filter(i => /measur|size|padding/i.test(i.alt))`
   and read the image itself. If a section has a heading but no attribute rows,
   that is what happened.

Fallbacks when a value is still missing: the Material web docs, Android
Developers' Compose Material 3 reference, or a client library that cites the
spec version.

Do **not** fill a gap with a plausible-looking number. An off-spec radius or
spring is worse than an explicitly flagged unknown, because it will be
implemented faithfully and be wrong. Where a value in this skill is a practical
derivation rather than a published token (the spacing scale, grid margins,
`full` expressed as `9999px`), the reference file says so.
