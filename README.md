# Material 3 Expressive (MD3E) Front-End AI Skill & Design System

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Spec: m3.material.io](https://img.shields.io/badge/Spec-Material%203%20Expressive-6750A4.svg)](https://m3.material.io)
[![Web Components: @material/web](https://img.shields.io/badge/%40material%2Fweb-Compatible-4285F4.svg)](https://github.com/material-components/material-web)
[![Tailwind CSS: v3 & v4](https://img.shields.io/badge/Tailwind%20CSS-v3%20%26%20v4-38B2AC.svg)](https://tailwindcss.com)
[![Auditor: Deterministic](https://img.shields.io/badge/Auditor-16%20Rules%20Passing-success.svg)](#deterministic-compliance-auditor)

**The authoritative AI Skill, Design Token layer, and component toolkit for building front-end interfaces that comply with Google's Material 3 Expressive (MD3E, May 2025+ evolution).**

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
├── SKILL.md                                 # Main AI agent instruction file
├── assets/
│   ├── starter/
│   │   └── index.html                       # 36-component interactive showcase & playground
│   ├── tailwind/
│   │   ├── md3e-theme.css                   # Tailwind CSS v4 @theme configuration
│   │   └── tailwind.config.js               # Tailwind CSS v3 theme extension
│   └── tokens/
│       ├── md3e-tokens.css                  # Core design tokens (37 roles, 30 type styles, 10 shapes)
│       ├── md3e-motion.css                  # Physical spring motion tokens
│       └── md3e-material-web.css            # Turnkey bridge layer for @material/web
├── references/
│   ├── material-web.md                      # Complete @material/web integration & framework guide
│   ├── tailwind.md                          # Tailwind CSS integration guide
│   ├── color.md                             # 37 color roles, tone mapping & state layers
│   ├── typography.md                        # 15 baseline + 15 emphasized type styles
│   ├── shape.md                             # 10-step corner radius scale & morphing rules
│   ├── motion.md                            # Spring physics parameters & linear() easing
│   ├── layout.md                            # Breakpoints & canonical responsive layouts
│   ├── accessibility.md                     # Contrast, >=48px targets & focus indicators
│   ├── expressive-tactics.md                # The 7 tactical rules for expressive UI
│   ├── components.md                        # Shared rules & component index
│   └── components/
│       ├── action.md                        # Buttons, FABs, Split Buttons, Button Groups
│       ├── communication.md                 # Badges, Progress, Loading Indicator, Snackbars
│       ├── containment.md                   # Cards, Dialogs, Sheets, Lists, Carousels
│       ├── navigation.md                    # Toolbars, App Bars, Rails, Drawers, Tabs, Search
│       ├── selection.md                     # Checkbox, Switch, Sliders, Chips
│       ├── text-input.md                    # Text Fields, Selects, Date & Time Pickers
│       └── expressive-recipes.md            # Production HTML/CSS/JS recipes for 5 new components
└── scripts/
    ├── audit_md3e.py                        # Deterministic compliance auditor (16 rules)
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
<!-- Google Material Symbols Icons -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200">

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
  <md-icon slot="icon">send</md-icon>
  Send Message
</md-filled-button>

<!-- Square Button (16dp corner) -->
<md-outlined-button class="md3e-size-m md3e-shape-square">
  Square Button
</md-outlined-button>

<!-- Medium FAB (80dp, corner 20dp) -->
<md-fab class="md3e-fab-medium" aria-label="Compose">
  <md-icon slot="icon">edit</md-icon>
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

## 🔍 Deterministic Compliance Auditor

Run `audit_md3e.py` to scan your codebase against 16 strict MD3E compliance rules:

```bash
# Scan a directory
python scripts/audit_md3e.py src

# Strict CI gate
python scripts/audit_md3e.py src --fail-on warn

# Machine-readable output
python scripts/audit_md3e.py src --json
```

### Audit Rule Index

| Code | Severity | Description |
|---|---|---|
| `MD3E001` | Error | Hardcoded hex colour (use `var(--md-sys-color-*)`) |
| `MD3E002` | Error | Hardcoded `rgb()` / `hsl()` colour |
| `MD3E003` | Error | Corner radius off the 10-step shape scale |
| `MD3E004` | Error | Duration/easing instead of a physical spring token |
| `MD3E005` | Error | Focus outline removed or missing |
| `MD3E006` | Warning | Interactive target under 48px |
| `MD3E007` | Warning | Font size off the 11-step type scale |
| `MD3E008` | Warning | Missing `prefers-reduced-motion` fallback |
| `MD3E009` | Warning | Colour roles defined without dark theme support |
| `MD3E010` | Info | `box-shadow` used to express elevation (use tonal surface) |
| `MD3E011` | Warning | `border-radius: 50%` instead of `corner-full` |
| `MD3E012` | Info | Uppercase label text (M2 legacy convention) |
| `MD3E013` | Warning | `transition: all` usage |
| `MD3E014` | Warning | Icon-only control without accessible name |
| `MD3E015` | Info | Deprecated bottom app bar |
| `MD3E016` | Warning | Deprecated small FAB (40dp) in favor of 56dp / 80dp |

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
Specifications and design guidelines are copyright [Google LLC](https://m3.material.io).
