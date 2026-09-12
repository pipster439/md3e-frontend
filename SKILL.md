---
name: md3e-frontend
description: Builds, restyles, or reviews front-end UI so it complies with Material 3 Expressive (M3E), the May 2025 evolution of Material Design 3. Use when a request involves Material Design 3, MD3, M3E, Material You, "material design" styling, m3.material.io, or any of its systems — dynamic colour roles, the emphasized type scale, the shape library and corner-radius scale, motion springs, expressive components (toolbars, split button, button groups, FAB menu, loading indicator), or adaptive breakpoints. Supplies complete design tokens, per-system reference data, and a deterministic compliance auditor for HTML/CSS/JS/TS/Vue/Svelte.
agent_created: true
---

# MD3E frontend

Make front-end code comply with Material 3 Expressive. The authority is
<https://m3.material.io>; everything here is derived from it, not invented.

**This is M3 Expressive, not M3.** Same system, evolved. Do not treat it as a
new version (it is not "M4"), and do not regress to M2 conventions — no
uppercase button labels, no `border-radius: 50%`, no duration/easing pairs.

## How to use this skill

| Job | Do this |
|---|---|
| New UI from scratch | Follow the six phases below in order |
| Restyle existing UI | Run phase 1, then the auditor, then fix by severity |
| Review someone's UI | Run `scripts/audit_md3e.py`, then read the code against the references |
| Answer a spec question | Read the relevant reference file; do not answer from memory |
| Pick colours / shapes / motion values | Read the reference; never guess a hex or a radius |

## Non-negotiables

1. **Never hardcode a colour.** Use `var(--md-sys-color-*)`. A role carries
   light/dark and contrast behaviour; a hex value carries nothing.
2. **Never pair a container with a foreign `on-` colour.** `primary` pairs with
   `on-primary`, `secondary-container` with `on-secondary-container`. This is
   what guarantees contrast.
3. **Never invent a corner radius.** The shape scale has exactly ten steps.
4. **Never write `transition: 300ms ease-in-out`.** Use a motion spring token.
   Spatial springs for anything that moves, resizes or morphs; effects springs
   for colour and opacity.
5. **Never use a font size off the type scale.** Eleven sizes exist; pick one.
6. **Always give interactive elements a ≥48px target** — expand the hit area if
   the visual is smaller.
7. **Always provide `:focus-visible`,** reduced-motion, and dark-mode paths.
8. **Exactly one `filled` button per view.** Emphasis is a hierarchy, not a
   preference.
9. **Do not build a dark theme by inverting.** Redefine the same roles to
   different tones.
10. **Run the auditor before declaring the work done.**

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
<html data-motion-scheme="expressive">        <!-- Material's recommended default -->
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
2. **Typography.** Pick five or six styles from the 15 and use only those.
   Apply emphasized styles where the spec calls for them — primary button
   labels, badges, the selected list/menu item, the extended FAB label — and
   nowhere else. If the product ships Chinese, Japanese or Korean, switch the
   line-height tokens to the medium language-height category.
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

- The **bottom app bar is deprecated** — use a docked or floating toolbar.
- The **loading indicator replaces** the indeterminate circular progress
  indicator for waits under about five seconds.
- The **small FAB (40dp) is deprecated** — use standard (56dp) or medium (80dp).

### Three component strategies

1. **Google Material Web (`@material/web`)**: For standard primitives (buttons, text fields, selects, checkbox, switch, slider, dialog, menu, tabs). Include `assets/tokens/md3e-material-web.css` and use MD3E utility classes (`.md3e-size-xs` .. `.md3e-size-xl`, `.md3e-shape-square`, `.md3e-fab-medium`). See `references/material-web.md`.
2. **Pure Expressive Recipes**: For the 5 components missing from `@material/web` (docked/floating toolbars, split button, connected button groups, FAB menu, shape-morphing loading indicator, toggle buttons). See `references/components/expressive-recipes.md`.
3. **Tailwind CSS**: Use MD3E token utility classes (`bg-md-primary`, `rounded-md-lg`, `shadow-md-level2`). See `references/tailwind.md` and `assets/tailwind/`.

Complete every state: enabled, hover, focus, pressed, disabled, plus selected
where it applies. See `references/accessibility.md`.

## Phase 4 — Motion

Read `references/motion.md`.

Apply spring tokens to every state change and transition. Choose by two
questions: *does it move or recolour?* (spatial vs effects) and *how big is the
change?* (fast / default / slow). Most motion should be `default`.

For gesture-driven motion, use a spring that carries velocity on release — a CSS
transition restarts from zero and feels dead.

Never mix the legacy duration/easing tokens with spring tokens on the same
property.

## Phase 5 — Layout and adaptivity

Read `references/layout.md`.

Implement the five breakpoints (600 / 840 / 1200 / 1600) and, at each one, answer
the five questions: what is revealed, how is the screen divided, what is
resized, what is repositioned, what is swapped. Use a canonical layout
(list-detail, supporting pane, feed) rather than inventing a grid.

## Phase 6 — Apply Expressive tactics, then audit

Read `references/expressive-tactics.md`.

Get the base compliant first — a screen that follows the system already reads as
Material. Then pick **one or two hero moments** per product and spend the
emphasis budget there. Expression is not a licence to break the token layer.

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
| MD3E003 | error | Corner radius off the shape scale |
| MD3E004 | error | Duration/easing instead of a motion spring |
| MD3E005 | error | Focus indicator removed or missing |
| MD3E006 | warn | Interactive target under 48px |
| MD3E007 | warn | Font size off the type scale |
| MD3E008 | warn | No `prefers-reduced-motion` path |
| MD3E009 | warn | Colour roles without a dark scheme |
| MD3E010 | info | `box-shadow` used to express elevation |
| MD3E011 | warn | `border-radius: 50%` instead of `corner-full` |
| MD3E012 | info | Uppercase label text (M2 convention) |
| MD3E013 | warn | `transition: all` |
| MD3E014 | warn | Icon-only control with no accessible name |
| MD3E015 | info | Deprecated bottom app bar |
| MD3E016 | warn | Deprecated small FAB (40dp) |

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
3. `border-radius: 10px` — not a step on the scale
4. `border-radius: 50%` instead of `corner-full`
5. `transition: transform 300ms ease-in-out`
6. A spatial spring on opacity, or an effects spring on position
7. `font-size: 13px` / `15px` — not on the type scale
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
