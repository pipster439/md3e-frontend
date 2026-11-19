# Material 3 Expressive (MD3E) Front-End AI Skill & Design System

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Spec: m3.material.io](https://img.shields.io/badge/Spec-Material%203%20Expressive-6750A4.svg)](https://m3.material.io)
[![Primitives: Semantic HTML & Headless UI](https://img.shields.io/badge/Primitives-Semantic%20HTML%20%26%20Headless%20UI-4285F4.svg)](#3-semantic-html--headless-primitives-radix-ui--base-ui)
[![Tailwind CSS: v3 & v4](https://img.shields.io/badge/Tailwind%20CSS-v3%20%26%20v4-38B2AC.svg)](https://tailwindcss.com)
[![Auditor: 4-Tier Rules](https://img.shields.io/badge/Auditor-4--Tier%20Verified-success.svg)](#deterministic-compliance-auditor)

**An M3 Expressive-inspired Web Design System with verified M3E specifications — organized cleanly into Official M3E foundations (Layer 1), Web Implementation adaptations (Layer 2), Opt-In Product Extensions (Layer 3), and a strictly dormant Personal Studio tier (Layer 4, never loaded unless explicitly requested).**

Compatible with **Google Antigravity**, **Cursor**, **Claude Code**, **Windsurf**, and any web development stack (React, Vue, Svelte, Tailwind CSS, or Vanilla HTML/CSS).

---

## 🌟 Why MD3E Front-End?

Google's **Material 3 Expressive** introduced profound updates over baseline M3:
* **Five-size button hierarchy** (32 / 40 / 56 / 96 / 136dp) and **Square shape variants** (12 / 16 / 28dp corner radii).
* **Five brand-new Expressive components**: Toolbars (Docked & Floating, replacing deprecated Bottom App Bar), Split Buttons, Connected Button Groups, FAB Menus, and the Expressive Shape-Morphing Loading Indicator.
* **Physical motion springs**: Replacing rigid duration/easing curves with harmonic oscillator physics (`linear()` approximations).
* **Shape morphing transitions**: Controls smoothly change shapes (e.g. Round ↔ Square) upon selection or press.

Instead of wrapping legacy custom elements or fighting Shadow DOM style encapsulation, **this repository unifies the entire design system on native semantic HTML + Headless UI primitives + MD3E CSS tokens**, providing:
1. Direct bindings from MD3E CSS tokens (`--md-sys-*`) onto semantic `<button>`, `<input>`, `<dialog>`, and `<nav>` elements — or unstyled Headless UI primitives (Radix UI, Base UI, React Aria) for complex composite overlays.
2. Pure HTML/CSS/JS recipes for all Expressive components (`references/components/expressive-recipes.md`) backed by zero-dependency vanilla JS spring physics, contour-aligned morphing, and browser HCT colour extraction engines.
3. Tailwind CSS v3 & v4 presets.
4. A deterministic 4-tier static compliance auditor (`audit_md3e.py`) verifying semantic ARIA contracts, token bindings, contrast/motion/blur accessibility, and off-spec regressions.

---

## 📦 What's Inside

```
md3e-frontend/
├── SKILL.md                                 # Router-style AI agent entry point (<150 lines)
├── OFFICIAL_SPEC_AUDIT.md                   # Verification ledger & certified vs uncertified scope
├── assets/
│   ├── components/
│   │   ├── md3e-components.css              # Bundled MD3E component CSS (all 16 modules)
│   │   ├── button.css / fab.css / ...       # Per-component standalone stylesheets
│   │   └── dialog.css / text-field.css / ...# Interactive & form component styles
│   ├── fonts/
│   │   ├── md3e-fonts.css                   # Offline-first @font-face declarations
│   │   ├── *.woff2                          # Self-hosted Google Sans Flex, Roboto Flex, Material Symbols Outlined
│   │   ├── OFL-1.1-LICENSE.txt              # SIL Open Font License 1.1 & Apache 2.0 notice
│   │   └── README.md                        # Font inventory, CJK fallback & re-fetch guide
│   ├── starter/
│   │   ├── index.html                       # Interactive Layer 1 & 2 showcase, color studio & morph lab
│   │   ├── minimal.html                     # Minimal zero-build starter (tokens + components + fonts)
│   │   └── desktop-bento.html               # Opt-in Layer 3 Desktop Bento (+ Layer 4 Personal Studio demo)
│   ├── tailwind/
│   │   ├── md3e-theme.css                   # Tailwind CSS v4 @theme configuration
│   │   └── tailwind.config.js               # Tailwind CSS v3 theme extension
│   └── tokens/
│       ├── md3e-tokens.css                  # Core design tokens (47 semantic roles, 30 type styles, 10 shapes)
│       ├── md3e-palettes.css                # Precomputed tonal palettes & seed overrides
│       ├── md3e-shapes.css                  # 35 AndroidX MaterialShapes CSS mask definitions
│       ├── md3e-motion.css                  # Sampled linear() physical spring motion tokens
│       ├── md3e-blur.css                    # Translucent scrims & prefers-reduced-transparency fallbacks
│       ├── md3e-spring.js                   # Real-time interruptible damped harmonic oscillator spring runtime + synthesizeSpringLinearCss
│       ├── md3e-morph.js                    # Cubic Bezier contour-aligned shape morph interpolator
│       ├── md3e-dynamic-color.js            # Browser HCT QuantizerCelebi + Score + SPEC_2025 engine
│       ├── md3e-studio.css                  # Dormant Layer 4 (Opt-In Only): Pure dark canvas, optical glass, Adaptive HDR & co-tuner CSS
│       └── md3e-studio.js                   # Dormant Layer 4 (Opt-In Only): Scrubbers, HDR capability & Human-AI Co-Tuning (`__MD3E_TUNER__`)
├── references/
│   ├── tailwind.md                          # Tailwind CSS integration guide
│   ├── color.md                             # Layer 1 & 2: 47 color roles, HCT variants & Web mixing rules
│   ├── typography.md                        # Layer 1: 15 baseline + 15 emphasized type styles & GRAD/ROND
│   ├── shape.md                             # Layer 1 & 2: 10-step corner scale, 35 shapes & CSS masking
│   ├── motion.md                            # Layer 1 & 2: Physical springs AND official Web curves
│   ├── layout.md                            # Layer 1 & 2: Breakpoints & adaptive canonical layouts
│   ├── accessibility.md                     # Layer 1 & 2: WCAG 2.2 AA 24px floor vs 48px M3 target
│   ├── desktop-bento.md                     # Layer 3 (Opt-In): Desktop Bento telemetry extension
│   ├── personal-studio.md                   # Layer 4 (Strictly Dormant Opt-In): Adaptive HDR, Live DOM FLIP modal & Co-Tuning protocol
│   ├── expressive-tactics.md                # Layer 3 (Opt-In): 7 editorial tactics for expressive UI
│   ├── components.md                        # Shared rules, component index & Complex Component Architecture Matrix
│   └── components/
│       ├── action.md                        # Buttons, FABs, Split Buttons, Button Groups
│       ├── communication.md                 # Badges, Progress, Loading Indicator, Snackbars
│       ├── containment.md                   # Cards, Native Dialogs, Sheets, Lists, Carousels, Anchored Popover Menus
│       ├── navigation.md                    # Toolbars, App Bars, Rails, Drawers, Tabs, Search
│       ├── selection.md                     # Checkbox, Chips, Radio, Select (Skin Contract + base-select), Switch, Sliders
│       ├── text-input.md                    # Text Fields (<fieldset><legend> notch), Date Pickers (Single/Range), Time Pickers
│       └── expressive-recipes.md            # Production recipes (sliders, switch/checkbox, loader, wavy progress, toolbars)
    └── integration.md                       # Coexistence & token mapping for Tailwind / MUI / antd
└── scripts/
    ├── audit_md3e.py                        # 4-tier deterministic auditor (ERROR/WARNING/INFO/CUSTOM)
    ├── build_components.py                  # Rebuild assets/components/md3e-components.css bundle
    ├── fetch_fonts.py                       # Download/refresh self-hosted WOFF2 fonts & md3e-fonts.css
    ├── spring_to_css.py                     # Harmonic oscillator physics-to-CSS generator
    ├── test_md3e.py                         # Unit & compliance test suite
    └── verify_visual.py                     # Offline Playwright font/CJK/component visual verifier
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
You **must copy `assets/` alongside `SKILL.md` and `references/`** so that fonts, design tokens, and component stylesheets are all present in your target workspace (without `assets/`, `.md3e-*` classes and local fonts will not load):

```text
your-project/
├── .cursor/skills/md3e-frontend/   (or .agents/skills/md3e-frontend/)
│   ├── SKILL.md
│   └── references/
└── assets/                         # Required in your web root / public assets
    ├── fonts/md3e-fonts.css + *.woff2
    ├── tokens/md3e-tokens.css + md3e-motion.css + md3e-shapes.css
    ├── components/md3e-components.css  (or individual *.css files)
    ├── starter/minimal.html
    └── tailwind/
```

---

### 2. Turnkey Token & Component Integration

Copy `assets/` into your web root (or inspect [minimal.html](assets/starter/minimal.html)) and link the offline-first fonts, tokens, and pre-built component styles:
```html
<!-- Offline-first self-hosted fonts & Material Symbols Outlined icons (zero external network dependency) -->
<link rel="stylesheet" href="./assets/fonts/md3e-fonts.css">
<!-- Optional CDN fallback if you omit assets/fonts/: axes MUST be strictly alphabetical -->
<!-- <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block"> -->

<!-- MD3E Token & Component Layers -->
<link rel="stylesheet" href="./assets/tokens/md3e-tokens.css">
<link rel="stylesheet" href="./assets/tokens/md3e-motion.css">
<link rel="stylesheet" href="./assets/tokens/md3e-shapes.css">
<link rel="stylesheet" href="./assets/components/md3e-components.css">
```

Activate dark mode or vibrant expressive color variants on `<html>`:
```html
<html data-motion-scheme="expressive" data-theme="dark" data-color-variant="vibrant">
```

---

### 3. Semantic HTML & Headless Primitives (Radix UI / Base UI)

Style native semantic HTML controls directly with MD3E CSS classes (`md3e-btn`, `md3e-icon-btn`, `md3e-fab`, `md3e-switch`, `md3e-dialog`) — zero Shadow DOM encapsulation or custom-element polyfills:
```html
<!-- Medium 56dp Primary Filled Action (use sparingly per view) -->
<button type="button" class="md3e-btn md3e-btn--filled md3e-btn--m">
  <span class="material-symbols-outlined" aria-hidden="true">send</span>
  Send Message
</button>

<!-- Square Outlined Button (16dp corner at Medium) -->
<button type="button" class="md3e-btn md3e-btn--outlined md3e-btn--m md3e-btn--square">
  Square Button
</button>

<!-- Medium FAB (80dp, corner 20dp) -->
<button type="button" class="md3e-fab md3e-fab--medium" aria-label="Compose">
  <span class="material-symbols-outlined" aria-hidden="true">edit</span>
</button>

<!-- Native Dialog Modal (or Radix UI / Base UI Dialog bound to [data-state="open"]) -->
<dialog class="md3e-dialog" aria-labelledby="confirm-title">
  <h3 id="confirm-title">Confirm Action</h3>
  <button type="button" class="md3e-btn md3e-btn--tonal md3e-btn--s">Close</button>
</dialog>
```

For React, Vue, or Svelte composite widgets (Selects, Date Pickers, nested menus, popovers, roving tabs), drop unstyled primitives (**Radix UI**, **Base UI**, **React Aria**, **Ark UI**) underneath your MD3E stylesheets and map the unified Visual Skin Contract (`[data-state="open|closed"]`, `[data-highlighted]`, `[data-selected]`, `[data-disabled]`, plus calendar `[data-today]`/`[data-in-range]`/`[data-range-start]`/`[data-range-end]`) directly to `--md-sys-*` tokens — while Pure Native widgets use `<fieldset><legend>` outlined text field notches, `<dialog>` (`overscroll-behavior: contain` + interruptible `createSpringAnimator`), and top-layer `[popover="auto"]` anchored menus.

---

### 4. Pure Expressive Component Recipes

Use the copy-ready zero-dependency semantic HTML/CSS/JS recipes in [`references/components/expressive-recipes.md`](references/components/expressive-recipes.md):

* **Floating & Docked Toolbars**: Pill and docked action bars (replacing deprecated bottom app bar).
* **Split Button**: Primary action + trailing dropdown menu trigger with continuous/gapped silhouettes.
* **Connected Button Groups**: Shared inner borders with asymmetric corner radii and click width squeeze.
* **FAB Menu**: Floating action button expanding into vertical action sheets with focus trapping and `pointer-events: none` container isolation.
* **Expressive Loading Indicator & Wavy Progress**: 7-polygon morphing loader + SVG/Canvas waves that straighten at 100%.
* **M3 Expressive Slider & Selection Controls**: Split active/inactive tracks (`16dp` XS / `40dp` M) with `6dp` gap, `4dp` stop dot & `4×44dp`/`4×52dp` vertical bar handle (`appearance: none` + Radix/Base UI binding), `28dp` pressed-thumb Switch, and `18×18dp` (`2px` corner) Checkbox.

---

### 5. Tailwind CSS Support

#### Tailwind v4 (`@theme`)
Import `assets/tokens/md3e-tokens.css` and `assets/tailwind/md3e-theme.css` (see [integration.md](references/integration.md) for Tailwind v3/v4, MUI, Ant Design, and custom token coexistence & conflict avoidance):
```css
@import "./assets/tokens/md3e-tokens.css";
@import "./assets/tailwind/md3e-theme.css";
```

#### Tailwind v3
Use `assets/tailwind/tailwind.config.js`:
```javascript
module.exports = require('./assets/tailwind/tailwind.config.js');
```
Now use MD3E utility classes directly:
```html
<button type="button" class="bg-md-primary text-md-on-primary rounded-md-full px-4 h-10 min-h-[48px]">
  Confirm
</button>
```

---

## 🔍 Deterministic Compliance Auditor (4-Tier Architecture)

Run `audit_md3e.py` to scan HTML/CSS (and optionally `--markdown` doc examples) across four distinct authority tiers, cleanly separating **Official M3E / WCAG AA floors** from **Layer 3 Opt-In Product Extensions** and **Dormant Layer 4 (`Personal Studio`)**:

```bash
# Default Layer 1 + Layer 2 compliance gate
python scripts/audit_md3e.py src

# Strict CI gate (fail on ERROR or WARNING; INFO/CUSTOM remain non-blocking)
python scripts/audit_md3e.py src --fail-on warning

# Opt-in Layer 3 Desktop Bento product-style audit
python scripts/audit_md3e.py src --mode=desktop-bento --fail-on warning

# Dormant Layer 4 Personal Studio audit (ONLY when Personal Studio / Layer 4 is explicitly requested)
python scripts/audit_md3e.py src --mode=personal-studio --fail-on warning

# Machine-readable JSON output (isolates official_compliance vs custom_extensions)
python scripts/audit_md3e.py src --json
```

> **Dormant Layer 4 Policy:** `references/personal-studio.md`, `md3e-studio.css`, `md3e-studio.js`, and `--mode=personal-studio` are **strictly dormant by default** — agents must never load or apply them unless the user explicitly asks for `Personal Studio`, `Layer 4`, or `--mode=personal-studio`.

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
| `MD3E020` | `ERROR` | HTML / ARIA | Legacy custom-element tag / Web Component bridge import, or invalid native/headless ARIA state & `tabindex` contract |
| `MD3E021` | `WARNING` | WCAG A11y | Decorative Material Symbols span missing `aria-hidden="true"` inside labeled control |
| `MD3E022` | `ERROR` | L2 Blur | `backdrop-filter: blur(...)` missing `@media (prefers-reduced-transparency: reduce)` solid fallback |
| `MD3E024` | `ERROR` | L1/WCAG | Contrast failure (`< 4.5:1` / `< 3.0:1` large) or semantic `on-*` role mismatch |
| `MD3E028` | `ERROR` | L1/CSS | Unbalanced `{` / `}` CSS braces across `<style>` blocks or CSS files (catches unclosed `@keyframes` / rules) |
| `MD3E004` | `WARNING` | L2 Motion | Uncalibrated ad-hoc curve (`md3e-spring.js`, sampled `linear()`, and Google `OFFICIAL_WEB_CURVES` + duration are all valid) |
| `MD3E008` | `WARNING` | WCAG/M3 | Motion declarations missing `@media (prefers-reduced-motion: reduce)` path |
| `MD3E011`, `013`, `016`, `019`, `023`, `026` | `WARNING` | L2 Web | `border-radius: 50%` on pills, `transition: all`, deprecated 40dp small FAB, `9999px` spring overshoot snap, `box-shadow` on masked shape, or unbound `md3e-*` modifier class |
| `MD3E027` | `WARNING` | L2 Web / Input | OS-native `accent-color` range slider missing `appearance: none` (grey border/OS thumb bug) or `position: fixed` floating/FAB menu wrapper missing `pointer-events: none` (hit-trap) |
| `MD3E029` | `WARNING` | L2 Complex UI | Floating `<label>` opaque background bleed vs `<fieldset><legend>`, `<dialog>` redundant `role="dialog"`/`aria-modal` or `html`/`body` scroll-lock or missing `dialog:modal { overscroll-behavior: contain; }`, or custom `[role="listbox\|menu\|grid"]` missing active/focus-state CSS |
| `MD3E001`–`003`, `007`, `010`, `012`, `015`, `025` | `INFO` | Project Prefs | Hardcoded hex/rgb/radii/type scale, shadow elevation, uppercase labels, bottom app bar, or multiple primary filled buttons in one view |
| `MD3E101`–`104` | `CUSTOM` | L3 Opt-In | Desktop Bento (`--mode=desktop-bento` / `--mode=personal-studio` only, excluded from Official Score): borderless tonal panels, `4+` surface tiers, concentric radii, Hero motifs (auto-exempts analytical data views) |
| `MD3E201`–`202` | `CUSTOM` | L4 Dormant | Personal Studio (`--mode=personal-studio` only, strictly dormant unless requested, excluded from Official Score): bans `.studio-caustic-field` global light-bleed blobs, verifies optical glass + micro-scoped Adaptive HDR (no `body`/`p` boost) + SDR/RT/HC fallbacks, and `<dialog>` modal `overscroll-behavior` / native ARIA / focusable controls |

---

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
Specifications and design guidelines are copyright [Google LLC](https://m3.material.io).
