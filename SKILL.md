---
name: md3e-frontend
description: M3 Expressive-inspired Web Design System with verified M3E specifications. Provides turnkey self-hosted fonts/icons, Layer 1+2 design tokens, ready-to-link component CSS (`assets/components/`), Tailwind v3/v4 presets, Headless UI integration contracts, static compliance auditing (`audit_md3e.py`), and Playwright visual verification (`verify_visual.py`).
agent_created: true
---

# MD3E Frontend — Router & Integration Guide

> **Positioning:** An **M3 Expressive-inspired Web Design System with verified M3E specifications** grounded in `m3.material.io`, AndroidX `MaterialShapes`, and Material Color Utilities (`SPEC_2025`), adapted for Web standards. Do not claim official Google certification for the repository or downstream custom extensions.

## Context Budget & Component Reuse Rules

Preserve your context window by **linking** shipped stylesheets instead of rewriting or reading large files whole:

1. **Link component CSS directly — do not rewrite component styles from markdown and do not load entire stylesheets into context.**
   - Default turnkey import order:
     1. `assets/fonts/md3e-fonts.css` *(self-hosted Google Sans Flex, Roboto Flex, Material Symbols Outlined — works offline)*
     2. `assets/tokens/md3e-tokens.css` *(47 colour roles, 15 + 15 type styles with CJK fallback, 10 corners, state opacities)*
     3. `assets/tokens/md3e-motion.css` *(physical springs + `OFFICIAL_WEB_CURVES`)*
     4. `assets/components/md3e-components.css` *(or individual files from `assets/components/`: `button.css`, `fab.css`, `card.css`, `switch.css`, `checkbox.css`, `slider.css`, `progress.css`, `text-field.css`, `dialog.css`, `menu.css`, `select.css`, `datepicker.css`, `toolbar.css`, `snackbar.css`, `navigation.css`, `sheet.css`)*
2. **Need to check a component's exact HTML classes or DOM structure?**
   - Inspect the relevant stylesheet in `assets/components/<component>.css` or copy directly from [`assets/starter/minimal.html`](assets/starter/minimal.html).
   - For advanced demos (Dynamic Colour Studio, 35 shapes, wavy progress, split/connected buttons, anchored popover menu, select listbox, date picker), inspect the targeted section in [`assets/starter/index.html`](assets/starter/index.html).
   - Large generated files such as `assets/tokens/md3e-palettes.css` (~575 KB) and `assets/starter/desktop-bento.html` are meant to be linked or inspected in targeted slices rather than loaded whole.

---

## Task Router (Goal -> Assets to Link -> Reference to Read)

| What You Are Building | Link / Use These Assets | Read This Reference |
|---|---|---|
| **Quick blank page / starter UI** | `assets/fonts/md3e-fonts.css`, `assets/tokens/md3e-tokens.css`, `assets/tokens/md3e-motion.css`, `assets/components/md3e-components.css` | [`assets/starter/minimal.html`](assets/starter/minimal.html) |
| **Existing Tailwind / MUI / Ant Design / custom tokens project** | `assets/tokens/md3e-tokens.css`, `assets/components/md3e-components.css`, `assets/tailwind/` (`md3e-theme.css` / `tailwind.config.js`) | [`references/integration.md`](references/integration.md) · [`references/tailwind.md`](references/tailwind.md) |
| **Brand theme / dark mode / dynamic HCT palette / wallpaper extraction** | `assets/tokens/md3e-tokens.css`, optional `assets/tokens/md3e-palettes.css`, optional `assets/tokens/md3e-dynamic-color.js`, or `scripts/color_to_css.py` | [`references/color.md`](references/color.md) |
| **Typography, variable axes (`GRAD`/`ROND`/`wght`), CJK line height, Material Symbols icons** | `assets/fonts/md3e-fonts.css`, `assets/tokens/md3e-tokens.css` *(CJK fallback built in; CDN optional)* | [`references/typography.md`](references/typography.md) · [`references/icons.md`](references/icons.md) |
| **10-step corners, 35 `MaterialShapes` masks, 7-polygon loader, real-time morphing** | `assets/tokens/md3e-shapes.css`, optional `assets/tokens/md3e-morph.js` + `assets/tokens/md3e-spring.js` | [`references/shape.md`](references/shape.md) |
| **Springs, `OFFICIAL_WEB_CURVES`, velocity-preserving gesture motion, frosted blur** | `assets/tokens/md3e-motion.css`, optional `assets/tokens/md3e-spring.js`, optional `assets/tokens/md3e-blur.css` | [`references/motion.md`](references/motion.md) |
| **Responsive layout, 5 M3 breakpoints (`600/840/1200/1600`), rail/drawer/sheets** | `assets/components/navigation.css`, `assets/components/sheet.css` | [`references/layout.md`](references/layout.md) |
| **Accessibility, contrast pairs, 24px floor vs 48px `::before` hit targets** | Built into `assets/components/*.css` and verified by `scripts/audit_md3e.py` | [`references/accessibility.md`](references/accessibility.md) |
| **Buttons, FAB, FAB menu, Split button, Button groups** | `assets/components/button.css`, `assets/components/fab.css` | [`references/components.md`](references/components.md) · [`references/components/action.md`](references/components/action.md) |
| **Toolbars (docked/floating), App bars, Nav bar/rail/drawer, Tabs, Search** | `assets/components/toolbar.css`, `assets/components/navigation.css` *(bottom app bar is deprecated)* | [`references/components/navigation.md`](references/components/navigation.md) |
| **Cards, Native `<dialog>`, Sheets, Carousel, Lists, `[popover="auto"]` Menus** | `assets/components/card.css`, `dialog.css`, `sheet.css`, `menu.css` | [`references/components/containment.md`](references/components/containment.md) |
| **Badges, Progress, Wavy Progress, 7-polygon Loading Indicator, Snackbars, Tooltips** | `assets/components/progress.css`, `assets/components/snackbar.css`, `assets/tokens/md3e-shapes.css` | [`references/components/communication.md`](references/components/communication.md) |
| **Switch, Checkbox, Radio, Chips, Split-track Slider, Select (Headless / `base-select`)** | `assets/components/switch.css`, `checkbox.css`, `slider.css`, `select.css` | [`references/components/selection.md`](references/components/selection.md) |
| **Text Fields (`<fieldset><legend>` transparent notch), Date Pickers, Time Pickers** | `assets/components/text-field.css`, `assets/components/datepicker.css` | [`references/components/text-input.md`](references/components/text-input.md) |
| **Custom interactive recipes & React / Radix UI / Base UI headless adapters** | `assets/components/*.css` + `assets/tokens/md3e-spring.js` + `assets/tokens/md3e-morph.js` | [`references/components/expressive-recipes.md`](references/components/expressive-recipes.md) |
| **Opt-in Layer 3: Desktop Bento Dashboard** *(only when building dense desktop consoles)* | Same core assets + `data-layout-profile="desktop-bento"` (`--mode=desktop-bento`) | [`references/desktop-bento.md`](references/desktop-bento.md) · [`references/expressive-tactics.md`](references/expressive-tactics.md) |
| **Dormant Layer 4: Personal Studio** *(NEVER load unless explicitly asked for `Personal Studio` / `Layer 4` / `--mode=personal-studio`)* | `assets/tokens/md3e-studio.css`, `assets/tokens/md3e-studio.js`, `data-studio-profile="personal-studio"` | [`references/personal-studio.md`](references/personal-studio.md) |

---

## Turnkey HTML Setup (Offline-First Default)

```html
<!DOCTYPE html>
<html lang="en" data-motion-scheme="expressive">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <link rel="stylesheet" href="./assets/fonts/md3e-fonts.css">
  <link rel="stylesheet" href="./assets/tokens/md3e-tokens.css">
  <link rel="stylesheet" href="./assets/tokens/md3e-motion.css">
  <link rel="stylesheet" href="./assets/components/md3e-components.css">
</head>
<body>
  <button type="button" class="md3e-btn md3e-btn--filled md3e-btn--m">
    <span class="material-symbols-outlined" aria-hidden="true">send</span>
    <span>Send</span>
  </button>
</body>
</html>
```

Root theme & scheme attributes on `<html>`:
- `data-theme="dark"` or `"light"` *(omit to follow OS `prefers-color-scheme`)*
- `data-motion-scheme="expressive"` *(default)* or `"standard"` (plus `data-motion-driver="bezier"` for `OFFICIAL_WEB_CURVES`)
- `data-color-variant="tonal-spot | expressive | vibrant | neutral | monochrome"` + `data-contrast="medium | high"`
- `data-seed="purple | ocean | emerald | amber | rose | teal"` *(requires linking `assets/tokens/md3e-palettes.css`)*

---

## Core Guardrails (Quick Checklist)

1. **Colour pairing & contrast (`ERROR`):** Pair every container with its matching `on-*` role (`primary` -> `on-primary`, `secondary-container` -> `on-secondary-container`); never invent surface opacity.
2. **Targets & focus (`ERROR` / `WARNING`):** Keep visual heights (`32px`/`40px`) and expand hit targets to `48×48px` via `::before`; never remove `:focus-visible`.
3. **Motion & blur (`ERROR` / `WARNING`):** Use `--md-sys-motion-*` springs, `md3e-spring.js`, or `OFFICIAL_WEB_CURVES` — never ad-hoc `300ms ease-in-out`. Neutral mixing uses `color-mix(in oklab, ...)` (never `in oklch` on neutrals). Frosted blur uses `md3e-blur.css` with `@media (prefers-reduced-transparency: reduce)`.
4. **Native semantics (`ERROR` / `WARNING`):** Use `<button>`, `<input>`, `<dialog>` (`.showModal()`, NO redundant `role="dialog"` / `aria-modal`), `[popover="auto"]`, `<fieldset><legend>` outlined notches, and `aria-hidden="true"` on decorative Material Symbols spans.
5. **M3E deprecations:** Use Docked or Floating Toolbars instead of Bottom App Bar; use 7-polygon Loading Indicator instead of indeterminate circular spinner for `< 5s` waits; use 56dp/80dp/96dp FAB instead of deprecated 40dp small FAB.

---

## Composability: Co-mounting with `frontend-design`

When both `md3e-frontend` and `frontend-design` are active in the same turn:
1. **Adopt from `frontend-design` (Domain, Composition & Copy):** **Subject Grounding**, **Two-Pass Spatial Composition**, **Anti-Templated Layout Self-Critique** (no repetitive card grids or decorative `01/02/03` badges), and **Plain Active-Voice Microcopy**.
2. **Enforce from `md3e-frontend` (Tokens, Type, Geometry & Audit):** Route all colours through **HCT semantic roles** (`md3e-tokens.css` / `md3e-palettes.css` / `md3e-dynamic-color.js`), use the **15 + 15** typescale (`Google Sans Flex` / `Roboto Flex` + CJK fallback), drive shapes/physics via `md3e-shapes.css` / `md3e-morph.js` / `md3e-spring.js`, keep Layer 4 dormant unless requested, and verify with `audit_md3e.py`.

---

## Scripts & Verification Gate

```bash
# 1. Static compliance audit (must have 0 ERROR; see OFFICIAL_SPEC_AUDIT.md for rule codes)
python scripts/audit_md3e.py src --fail-on warning
python scripts/audit_md3e.py src --mode=desktop-bento    # Layer 3 opt-in (excluded from Official Score)
python scripts/audit_md3e.py src --mode=personal-studio  # Layer 4 opt-in (ONLY when explicitly requested)

# 2. Rendered visual verification (Playwright offline check, minimal.html vs index.html parity)
python scripts/verify_visual.py

# 3. Token & generator tools
python scripts/color_to_css.py --seed "#0B57D0" --variant expressive --emit-css ./src/brand-colors.css
python scripts/spring_to_css.py --emit-css assets/tokens/md3e-motion.css
python scripts/shapes_to_css.py --emit-css assets/tokens/md3e-shapes.css
python scripts/build_components.py
python scripts/test_md3e.py -v
```
