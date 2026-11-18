# Material 3 Expressive (MD3E) Front-End AI Skill & Design System

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Spec: m3.material.io](https://img.shields.io/badge/Spec-Material%203%20Expressive-6750A4.svg)](https://m3.material.io)
[![Web Components: @material/web](https://img.shields.io/badge/%40material%2Fweb-Compatible-4285F4.svg)](https://github.com/material-components/material-web)
[![Tailwind CSS: v3 & v4](https://img.shields.io/badge/Tailwind%20CSS-v3%20%26%20v4-38B2AC.svg)](https://tailwindcss.com)
[![Auditor: 4-Tier Rules](https://img.shields.io/badge/Auditor-4--Tier%20Verified-success.svg)](#deterministic-compliance-auditor)

**An M3 Expressive-inspired Web Design System with verified M3E specifications — organized cleanly into Official M3E foundations, Web Implementation adaptations, and Opt-In Product Extensions.**

Compatible with **Google Antigravity**, **Cursor**, **Claude Code**, **Windsurf**, and any web development stack (React, Vue, Svelte, Tailwind CSS, or Vanilla HTML/CSS).

---

## 🌟 Why MD3E Front-End?

Google's **Material 3 Expressive** introduced profound updates over baseline M3:
* **Five-size button hierarchy** (32 / 40 / 56 / 96 / 136dp) and **Square shape variants** (12 / 16 / 28dp corner radii).
* **Five brand-new Expressive components**: Toolbars (Docked & Floating, replacing deprecated Bottom App Bar), Split Buttons, Connected Button Groups, FAB Menus, and the Expressive Shape-Morphing Loading Indicator.
* **Physical motion springs**: Replacing rigid duration/easing curves with harmonic oscillator physics (`linear()` approximations).
* **Shape morphing transitions**: Controls smoothly change shapes (e.g. Round ↔ Square) upon selection or press.

However, Google's official Web Components library (`@material/web`) was placed into maintenance mode prior to the Expressive release. **This repository bridges that gap**, providing:
1. Turnkey token bridges for `@material/web`.
2. Pure HTML/CSS/JS recipes for the missing Expressive components.
3. Tailwind CSS v3 & v4 presets.
4. A deterministic static compliance auditor (`audit_md3e.py`) to eliminate hallucinations and off-spec regressions.

---

## 📦 What's Inside

```
md3e-frontend/
├── SKILL.md                                 # Main AI agent instruction file (3-Layer Spec Architecture)
├── OFFICIAL_SPEC_AUDIT.md                   # Verification ledger & certified vs uncertified scope
├── assets/
│   ├── starter/
│   │   ├── index.html                       # Interactive Layer 1 & 2 showcase, color studio & morph lab
│   │   └── desktop-bento.html               # Opt-in Layer 3 Desktop Bento Override studio
│   ├── tailwind/
│   │   ├── md3e-theme.css                   # Tailwind CSS v4 @theme configuration
│   │   └── tailwind.config.js               # Tailwind CSS v3 theme extension
│   └── tokens/
│       ├── md3e-tokens.css                  # Core design tokens (47 semantic roles, 30 type styles, 10 shapes)
│       ├── md3e-palettes.css                # Precomputed tonal palettes & seed overrides
│       ├── md3e-shapes.css                  # 35 AndroidX MaterialShapes CSS mask definitions
│       ├── md3e-motion.css                  # Sampled linear() physical spring motion tokens
│       ├── md3e-blur.css                    # Translucent scrims & prefers-reduced-transparency fallbacks
│       ├── md3e-spring.js                   # Real-time damped harmonic oscillator spring runtime
│       ├── md3e-morph.js                    # Cubic Bezier contour-aligned shape morph interpolator
│       ├── md3e-dynamic-color.js            # Browser HCT QuantizerCelebi + Score + SPEC_2025 engine
│       └── md3e-material-web.css            # Turnkey bridge layer for @material/web
├── references/
│   ├── material-web.md                      # Complete @material/web integration & framework guide
│   ├── tailwind.md                          # Tailwind CSS integration guide
│   ├── color.md                             # Layer 1 & 2: 47 color roles, HCT variants & Web mixing rules
│   ├── typography.md                        # Layer 1: 15 baseline + 15 emphasized type styles & GRAD/ROND
│   ├── shape.md                             # Layer 1 & 2: 10-step corner scale, 35 shapes & CSS masking
│   ├── motion.md                            # Layer 1 & 2: Physical springs AND official Web curves
│   ├── layout.md                            # Layer 1 & 2: Breakpoints & adaptive canonical layouts
│   ├── accessibility.md                     # Layer 1 & 2: WCAG 2.2 AA 24px floor vs 48px M3 target
│   ├── desktop-bento.md                     # Layer 3 (Opt-In): Desktop Bento telemetry extension
│   ├── expressive-tactics.md                # Layer 3 (Opt-In): 7 editorial tactics for expressive UI
│   ├── components.md                        # Shared rules & component index
│   └── components/
│       ├── action.md                        # Buttons, FABs, Split Buttons, Button Groups
│       ├── communication.md                 # Badges, Progress, Loading Indicator, Snackbars
│       ├── containment.md                   # Cards, Dialogs, Sheets, Lists, Carousels
│       ├── navigation.md                    # Toolbars, App Bars, Rails, Drawers, Tabs, Search
│       ├── selection.md                     # Checkbox, Switch, Sliders, Chips
│       ├── text-input.md                    # Text Fields, Selects, Date & Time Pickers
│       └── expressive-recipes.md            # Production recipes (loader, wavy progress, toolbars)
└── scripts/
    ├── audit_md3e.py                        # 4-tier deterministic auditor (ERROR/WARNING/INFO/CUSTOM)
    ├── test_md3e.py                         # Unit & compliance test suite
    └── spring_to_css.py                     # Harmonic oscillator physics-to-CSS generator
```

---

## 🚀 Quick Start

### 1. Using with AI Assistants

#### Google Antigravity
Clone or copy this folder into your Antigravity skills directory:
```bash
# Global configuration (available across all projects)
git clone https://github.com/pipster439/md3e-frontend.git ~/.gemini/config/skills/md3e-frontend
```
Invoke via slash command:
```
/md3e-frontend Restyle this page according to Material 3 Expressive guidelines
```
Or simply describe your intent in natural language; Antigravity will automatically discover and activate the skill.

#### Cursor / Claude Code / Windsurf
Copy `SKILL.md` and the `references/` directory into your project's `.cursor/rules/`, `.agents/skills/`, or prompt context.

---

### 2. Turnkey Token Integration

Import the token files into your project:
```html
<!-- Google Material Symbols Icons (axes MUST be strictly alphabetical for v2 API) -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,ops,wght@0..1,-50..200,20..48,100..700">

<!-- MD3E Token Layer -->
<link rel="stylesheet" href="./styles/md3e-tokens.css">
<link rel="stylesheet" href="./styles/md3e-motion.css">

<!-- Optional: Bridge for @material/web -->
<link rel="stylesheet" href="./styles/md3e-material-web.css">
```

Activate dark mode or vibrant expressive color variants on `<html>`:
```html
<html data-motion-scheme="expressive" data-theme="dark" data-color-variant="vibrant">
```

---

### 3. Using `@material/web` with MD3E

Use Google's official Web Components and apply MD3E size and shape classes:
```html
<script type="module" src="https://esm.run/@material/web/all.js"></script>

<!-- Medium 56dp Filled Button with Emphasized Label -->
<md-filled-button class="md3e-size-m">
  <md-icon slot="icon" aria-hidden="true">send</md-icon>
  Send Message
</md-filled-button>

<!-- Square Button (16dp corner) -->
<md-outlined-button class="md3e-size-m md3e-shape-square">
  Square Button
</md-outlined-button>

<!-- Medium FAB (80dp, corner 20dp) -->
<md-fab class="md3e-fab-medium" aria-label="Compose">
  <md-icon slot="icon" aria-hidden="true">edit</md-icon>
</md-fab>
```

---

### 4. Pure Expressive Component Recipes

For components missing in `@material/web`, use the production-ready recipes in `references/components/expressive-recipes.md`:

* **Floating Toolbar**: Elevated pill toolbar (replacing deprecated bottom app bar).
* **Split Button**: Primary action + trailing dropdown menu trigger with continuous silhouette.
* **Connected Button Groups**: Shared inner borders with asymmetric corner radii.
* **FAB Menu**: Floating action button morphing into vertical action sheets with spring animation.
* **Expressive Loading Indicator**: Geometric morphing animation (<5s waits).

---

### 5. Tailwind CSS Support

#### Tailwind v4 (`@theme`)
Import `assets/tailwind/md3e-theme.css`:
```css
@import "./styles/md3e-tokens.css";
@import "./styles/md3e-theme.css";
```

#### Tailwind v3
Use `assets/tailwind/tailwind.config.js`:
```javascript
module.exports = require('./assets/tailwind/tailwind.config.js');
```
Now use MD3E utility classes directly:
```html
<button class="bg-md-primary text-md-on-primary rounded-md-full px-4 h-10 min-h-[48px]">
  Confirm
</button>
```

---

## 🔍 Deterministic Compliance Auditor (4-Tier Architecture)

Run `audit_md3e.py` to scan HTML/CSS (and optionally `--markdown` doc examples) across four distinct authority tiers, cleanly separating **Official M3E / WCAG AA floors** from **Layer 3 Opt-In Product Extensions**:

```bash
# Default Layer 1 + Layer 2 compliance gate
python scripts/audit_md3e.py src

# Strict CI gate (fail on ERROR or WARNING; INFO/CUSTOM remain non-blocking)
python scripts/audit_md3e.py src --fail-on warning

# Opt-in Layer 3 Desktop Bento product-style audit
python scripts/audit_md3e.py src --mode=desktop-bento --fail-on warning

# Machine-readable JSON output (isolates official_compliance vs custom_extensions)
python scripts/audit_md3e.py src --json
```

Add `data-md3e-exempt="data-view"` on specialized workspaces (or rely on automatic exemption for `<canvas>`, chart `<svg>` with axes/ticks, 2D trajectory/replay viewports, and statistical `<table>` views) so Bento decorative rules never interfere with analytical UI.

### Audit Rule Index (4 Authority Tiers)

| Code | Tier | Layer / Scope | Description |
|---|---|---|---|
| `MD3E005` | `ERROR` | L1/WCAG | Focus outline removed (`outline: none` / `outline: 0`) without replacement |
| `MD3E006` | `ERROR` / `WARNING` | WCAG / M3 | Interactive hit target `< 24×24px` (`ERROR`); `24–47px` or visual inflation instead of `::before` (`WARNING`) |
| `MD3E009` | `ERROR` / `WARNING` | L1 Color | Theme tokens missing dark-mode pair (`WARNING`); same-direction light/dark surface luminance inversion (`ERROR`) |
| `MD3E014` | `ERROR` | WCAG A11y | Icon-only control or `<img>` missing accessible name (`aria-label` / `alt`) |
| `MD3E017` | `ERROR` / `WARNING` | L2 Icons | Material Symbols axes not alphabetical / missing font `<link>` (`ERROR`); invented icon names or no FOUT block guard (`WARNING`) |
| `MD3E018` | `ERROR` | L2 CSS | Neutral `color-mix(in oklch, ...)` powerless-hue pink/red shift (use `in oklab`) or unitless alpha inside `color-mix()` |
| `MD3E020` | `ERROR` | HTML DOM | Malformed/mismatched `@material/web` `<md-*>` tag nesting |
| `MD3E021` | `WARNING` | WCAG A11y | Decorative `<md-icon>` or Material Symbols span missing `aria-hidden="true"` inside labeled control |
| `MD3E022` | `ERROR` | L2 Blur | `backdrop-filter: blur(...)` missing `@media (prefers-reduced-transparency: reduce)` solid fallback |
| `MD3E024` | `ERROR` | L1/WCAG | Contrast failure (`< 4.5:1` / `< 3.0:1` large) or semantic `on-*` role mismatch |
| `MD3E004` | `WARNING` | L2 Motion | Uncalibrated ad-hoc curve (`md3e-spring.js`, sampled `linear()`, and Google `OFFICIAL_WEB_CURVES` + duration are all valid) |
| `MD3E008` | `WARNING` | WCAG/M3 | Motion declarations missing `@media (prefers-reduced-motion: reduce)` path |
| `MD3E011`, `013`, `016`, `019`, `023` | `WARNING` | L2 Web | `border-radius: 50%` on pills, `transition: all`, deprecated 40dp small FAB, `9999px` spring overshoot snap, `box-shadow` on masked shape |
| `MD3E001`–`003`, `007`, `010`, `012`, `015`, `025` | `INFO` | Project Prefs | Hardcoded hex/rgb/radii/type scale, shadow elevation, uppercase labels, bottom app bar, or multiple primary filled buttons in one view |
| `MD3E101`–`104` | `CUSTOM` | L3 Opt-In | Desktop Bento (`--mode=desktop-bento` only, excluded from Official Score): borderless tonal panels, `4+` surface tiers, concentric radii, Hero motifs (auto-exempts analytical data views) |

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
Specifications and design guidelines are copyright [Google LLC](https://m3.material.io).
