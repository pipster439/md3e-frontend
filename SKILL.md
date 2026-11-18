---
name: md3e-frontend
description: M3 Expressive-inspired Web Design System with verified M3E specifications. Builds, restyles, or reviews front-end UI aligned with Material 3 Expressive (May 2025+) across a three-layer architecture — Layer 1 Official M3E core tokens & shapes (`m3.material.io`, AndroidX `MaterialShapes`, MCU `SPEC_2025`), Layer 2 Web implementation adaptations (`md3e-morph.js`, `md3e-blur.css`, `OFFICIAL_WEB_CURVES`, WCAG 2.2 AA targets), and Layer 3 opt-in product extensions (`desktop-bento.md`, `expressive-tactics.md`). Supplies tokens, per-system references, and a four-tier static auditor (`ERROR`/`WARNING`/`INFO`/`CUSTOM`).
agent_created: true
---

# MD3E Frontend — Layered Material 3 Expressive Web System

> **Repository Positioning**: This toolkit is an **M3 Expressive-inspired Web Design System with verified M3E specifications**. Core dynamic colour algorithms, typography steps, corner/shape definitions, and spring parameters are grounded in `https://m3.material.io`, AndroidX `MaterialShapes`, and Material Color Utilities (`SPEC_2025`), adapted honestly for Web standards — **do not claim that the entire repository or downstream custom extensions carry official Google certification.**

## Context Budget & Progressive Disclosure (Mandatory)

Downstream agents operate with a finite context window. Preserve token budget strictly from the first turn:

1. **NEVER read oversized static palette or full showcase HTML files into context in full.**
   - Forbidden full reads: `assets/tokens/md3e-palettes.css` (~575 KB) and large showcase HTML files (`assets/starter/index.html`, `assets/starter/desktop-bento.html`).
   - Instead of reading `md3e-palettes.css`, link it directly in `<head>` and select schemes via `data-seed` / `data-color-variant` / `data-contrast`, or generate a single compact CSS file with `python scripts/color_to_css.py --seed ... --emit-css ...`.
   - Instead of reading full showcase HTML files, consult only the compact Markdown reference files (`references/*.md`, `references/components/*.md`); when inspecting a showcase HTML pattern, read only targeted `<= 120`-line ranges located via search.
2. **Import core token and runtime modules on demand:**
   - **Always link core base:** `assets/tokens/md3e-tokens.css` and `assets/tokens/md3e-motion.css`.
   - **Link/import conditionally per feature:**
     - Floating frosted chrome -> `assets/tokens/md3e-blur.css`
     - 35 `MaterialShapes` CSS masks & 7-polygon CSS loader -> `assets/tokens/md3e-shapes.css`
     - Real-time cubic Bézier SVG shape morphing -> `assets/tokens/md3e-morph.js` + `assets/tokens/md3e-spring.js`
     - Client-side wallpaper/image HCT palette extraction & custom seed picker -> `assets/tokens/md3e-dynamic-color.js`
     - Multi-seed preset schemes -> `assets/tokens/md3e-palettes.css`
     - Native semantic HTML + Headless UI primitives (`<button>`, `<input>`, `<dialog>`, Radix UI / Base UI) -> bind directly to `--md-sys-*` / `--md-comp-*` tokens & `.md3e-*` classes (no legacy custom-element bridge or Shadow DOM wrapper required)

## Three-Layer Specification Architecture

| Layer | Scope | Verification & Authority |
|---|---|---|
| **Layer 1 — Official M3E Core** | 6 tonal palettes & semantic `on-*` roles + 5 HCT dynamic variants (`tonal-spot`, `expressive`, `vibrant`, `neutral`, `monochrome`), 15 baseline + 15 emphasized type styles, 10-step corner scale & 35 AndroidX `MaterialShapes` geometries, official `Expressive` / `Standard` (`Spatial` / `Effects`) spring `(damping, stiffness)` physics. | Derived directly from `m3.material.io`, AndroidX `MaterialShapes.kt`, and MCU `SPEC_2025`. Violations emit **`ERROR`** (plus WCAG AA core safety). |
| **Layer 2 — Web Implementation Adaptations** | **Equal first-class motion options**: JS/CSS `linear()` physical springs OR Google's official Web curves (`OFFICIAL_WEB_CURVES` + duration); **Visual size vs Hit Area**: WCAG 2.2 AA `24×24 CSS px` minimum (`ERROR`) vs M3 recommended `48×48 px` via `::before` (`WARNING`); CSS `mask-image` clipping + wrapper `filter: drop-shadow()`; `color-mix(in oklab, ...)` neutral safety (neutral `in oklch` = `ERROR`); `md3e-blur.css` with mandatory `@media (prefers-reduced-transparency: reduce)` pure-surface fallback (`ERROR` if missing). | Calibrated cross-platform Web engineering adaptations in `references/motion.md`, `accessibility.md`, `color.md`, `shape.md`. |
| **Layer 3 — Opt-In Product Extensions** | `references/desktop-bento.md` & `references/expressive-tactics.md`. Fixed desktop rail widths (`64px` / `80px` / `220px`), `24px` pane gaps, forced 4+ `surface-container-*` nesting, full rectangular border suppression, and Hero wave / Sparkline motifs (`MD3E101`–`MD3E104`). | Strictly **optional** (`CUSTOM` tier under `--mode=desktop-bento`); **never counted in the Official M3E Compliance Score**. Analytical data regions auto-exempt or use `data-md3e-exempt="data-view"`. |

**This is M3 Expressive, not baseline M3 or an ungrounded "M4".** Avoid M2 leftovers — no uppercase button labels, no `border-radius: 50%` on non-square pills, and no uncalibrated ad-hoc `300ms ease-in-out` transitions.

## How to use this skill

| Job | Do this |
|---|---|
| New UI from scratch | Follow the six phases below using Layer 1 tokens + Layer 2 Web adaptations |
| Desktop Bento dashboard *(Opt-In Layer 3)* | Explicitly opt into `references/desktop-bento.md` (`CUSTOM` rules) and run `audit_md3e.py --mode=desktop-bento` |
| Analytical / Chart / 2D Viewport UI | Mark containers with `data-md3e-exempt="data-view"` (or `<canvas>`, `<table>`, chart `<svg>`) so axes, dividers, and series palettes pass |
| Restyle or review UI | Run `scripts/audit_md3e.py` (triage `ERROR` -> `WARNING` -> `INFO`; isolate `CUSTOM`) and verify in a real browser |
| Pick colours / shapes / motion values | Read the relevant concise `references/*.md` guide on demand; never guess a hex or radius |

## Authority Tiers & Core Principles

1. **Always pair a container with its own `on-` role & meet WCAG contrast.** *(Layer 1 / `ERROR`)* `primary` pairs with `on-primary`, `secondary-container` with `on-secondary-container`, `>= 4.5:1` body (`>= 3.0:1` large text `>= 24px` or `>= 18.67px` bold).
2. **Never drop below WCAG 2.2 AA `24×24px` hit target or remove `:focus-visible`.** *(Layer 1+2 / `ERROR`)* Recommend expanding interactive controls (especially XS `32px` / S `40px` buttons) to M3's **`48×48px`** target via an invisible `::before` hit area (`WARNING` if `< 48px` without expansion) — never inflate the visual button box.
3. **Never write unguarded `backdrop-filter: blur()` or `in oklch` on neutrals.** *(Layer 2 / `ERROR`)* Always use `md3e-blur.css` / `@media (prefers-reduced-transparency: reduce)` solid `surface-container` fallbacks, and use `color-mix(in oklab, ...)` on neutrals/surfaces.
4. **Honour `prefers-reduced-motion`, dark scheme (`prefers-color-scheme`), and `forced-colors: active`.** *(Layer 1+2)* Never build dark mode by inversion; redefine role tones per theme.
5. **Treat Physical Springs AND Official Web Curves as equal motion citizens.** *(Layer 2 / `WARNING` on ad-hoc curves)* Use `--md-sys-motion-*` `linear()` springs, `md3e-spring.js` velocity-preserving physics, OR Google's `OFFICIAL_WEB_CURVES` (`350ms / 500ms / 650ms` cubic-bezier curves). Reserve spatial bounce for movement/shape, effects curves (`0%` overshoot) for colour/opacity.
6. **Follow project defaults thoughtfully.** *(Project Default / `INFO`)* Prefer `var(--md-sys-color-*)`, default 10-step corners, default 11-step type sizes, and sparingly using primary `filled` CTAs (ideally one enabled `filled` primary CTA per view/surface), customizing at the token layer when product branding or analytical data requires it.
7. **Keep Layer 3 extensions opt-in.** *(Product Extension / `CUSTOM`)* Fixed rail widths (`80/220px` or `64px`), borderless multi-tier Bento nesting, and Hero wave/sparkline motifs apply only when intentionally opted in (`desktop-bento.md`, `expressive-tactics.md`).
8. **Run `scripts/audit_md3e.py` + rendered browser inspection** before concluding.

## Phase 1 — Install the token layer

Copy the token files into the project (never emit broken `/styles/md3e-*.css` paths unless those files actually exist at that path; for standalone single-file HTML deliverables, copy the stylesheets alongside the HTML with relative `./tokens/` links or inline `md3e-tokens.css` + `md3e-motion.css` directly) and import them on demand, in this order:

```
assets/tokens/md3e-tokens.css         (core) colour roles (5 variants + 3 contrast levels), type, shape, state, icons
assets/tokens/md3e-motion.css         (core) motion springs + -duration/-easing/-bezier tokens (generated)
assets/tokens/md3e-blur.css           (optional) floating backdrop-filter blur + prefers-reduced-transparency solid fallbacks
assets/tokens/md3e-palettes.css       (optional, link-only) multi-seed colour scheme presets (ocean, emerald, amber, rose, teal)
assets/tokens/md3e-shapes.css         (optional) 35 official MaterialShapes masks & 7-polygon LoadingIndicator
assets/tokens/md3e-spring.js          (optional) velocity-preserving interruptible JS spring helper
assets/tokens/md3e-morph.js           (optional) AndroidX RoundedPolygon + Morph cubic Bézier real-time shape interpolator
assets/tokens/md3e-dynamic-color.js   (optional) runtime browser/SSR HCT palette extraction from uploaded images/seeds
```

```html
<meta name="color-scheme" content="light dark">

<!-- Google Material Symbols Icons (&display=block prevents raw ligature FOUT; axes MUST be alphabetical) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block">

<link rel="stylesheet" href="./tokens/md3e-tokens.css">
<link rel="stylesheet" href="./tokens/md3e-palettes.css">
<link rel="stylesheet" href="./tokens/md3e-blur.css">
<link rel="stylesheet" href="./tokens/md3e-shapes.css">
<link rel="stylesheet" href="./tokens/md3e-motion.css">
```

Set the scheme and theme roots once:

```html
<html data-motion-scheme="expressive">        <!-- Material's recommended default (or data-motion-driver="bezier") -->
<html data-theme="dark">                       <!-- or omit to follow prefers-color-scheme automatically -->
<html data-color-variant="expressive">         <!-- optional: tonal-spot | expressive | vibrant | neutral | monochrome (plus fidelity via color_to_css.py) -->
<html data-seed="ocean">                       <!-- optional (with md3e-palettes.css): purple | ocean | emerald | amber | rose | teal -->
<html data-contrast="high">                    <!-- optional: medium | high (also follows prefers-contrast: more) -->
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
2. **Typography & Icons.** Read `references/typography.md` and `references/icons.md`.
   Pick five or six styles from the 15 and use only those. Apply emphasized
   styles where the spec calls for them — primary button labels, badges, the
   selected list/menu item, the extended FAB label — and nowhere else. CJK
   line-height adaptation (`:lang(zh/ja/ko/...)`) is built into
   `md3e-tokens.css`. For icons, verify every Material Symbols `snake_case`
   ligature against `references/icons.md` (never guess Lucide/kebab-case names)
   and mark decorative icons inside labelled controls with `aria-hidden="true"`.
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

1. **Native Semantic HTML + MD3E Token Classes**: Build buttons, checkboxes, switches (`<input type="checkbox" role="switch">`), text fields, sliders, navigation rails/bars, and native `<dialog>` elements directly on standard HTML tags styled with `--md-sys-*` tokens, `::before` `48×48px` hit targets, `:focus-visible` focus rings, and standard ARIA states (`aria-pressed`, `aria-expanded`, `aria-checked`, `aria-selected`, `aria-current="page"`) — zero Web Component or Shadow DOM encapsulation friction.
2. **Headless Unstyled Primitives (Radix UI / Base UI / React Aria / Ark UI)**: For complex composite overlays, comboboxes, dropdown menus, roving tabs, and modal focus traps in React/Vue/Svelte apps, bind headless state attributes (`[data-state="open|checked"]`, `[data-highlighted]`) directly to MD3E colour roles, state layers, and `--md-sys-motion-*` springs.
3. **Pure Expressive Recipes & Tailwind CSS**: Use `references/components/expressive-recipes.md` for copy-ready HTML/CSS/JS Expressive components (docked/floating toolbars, split buttons, connected button groups, FAB menus, 7-polygon loading indicators, wavy progress bars, toggle groups, clock dial & 35-shape containers) and `references/tailwind.md` (`assets/tailwind/`) for Tailwind CSS v3/v4 utilities (`bg-md-primary`, `rounded-md-lg`, `shadow-md-level2`).

Complete every state: enabled, hover, focus, pressed, disabled, plus selected
where it applies. See `references/accessibility.md`.

## Phase 4 — Motion *(Layer 1 Physics + Layer 2 Web Curves)*

Read `references/motion.md`.

Use **either** physics spring tokens (`--md-sys-motion-*` `linear()` / JS `md3e-spring.js`) **or** Google's official Web cubic-bezier curves (`OFFICIAL_WEB_CURVES` + published `150–650ms` durations / `--md-sys-motion-*-bezier`) — both are equal first-class Web implementations. Choose by: *does it move/morph?* (spatial: may overshoot) vs *does it fade/recolour?* (effects: must not overshoot) and *how big is the change?* (`fast` / `default` / `slow`).

For gesture-driven motion, use JS velocity-preserving springs (`assets/tokens/md3e-spring.js`) so released drags retain momentum rather than restarting from zero velocity.

Never mix legacy M3 easing tokens with physics spring tokens on the same property.

## Phase 5 — Layout and adaptivity *(Layer 1 Breakpoints + Layer 2/3 Desktop Options)*

Read `references/layout.md`.

Implement the five official M3 breakpoints (`600 / 840 / 1200 / 1600`) and, at each one, answer the five questions: what is revealed, how is the screen divided, what is resized, what is repositioned, what is swapped. Pick a canonical pattern (`list-detail`, `supporting-pane`, `feed`) or an appropriate analytical layout.

For wide desktop viewports (`>= 840px`): swap bottom navigation bars for a Navigation Rail within M3E's adaptive range (`80–96dp` collapsed / `220–360dp` expanded) — note that our `80px` / `220px` rail widths, `24px` pane gaps, `--md-sys-layout-measure-max: 68ch`, `data-density` steps (`-4px` / `-8px` preserving `48px` hit targets), and Side Sheet swaps are sensible **Layer 2 Web project presets**, not rigid official mandates.

> **Layer 3 Opt-In Extension — Desktop Bento Dashboards:** When intentionally building compact operational consoles (`data-layout-profile="desktop-bento"`), read `references/desktop-bento.md` and audit with `--mode=desktop-bento`. Keep Bento product conventions strictly decoupled (`CUSTOM` tier) and exempt professional charts/tables/2D viewports with `data-md3e-exempt="data-view"`.

## Phase 6 — Opt-In Product Extensions & Four-Tier Audit *(Layer 3 + Auditor)*

Read `references/expressive-tactics.md` *(Opt-In Product Extension guidance)*.

Verify Layer 1 & Layer 2 fundamentals first, then apply optional Hero tactics or Desktop Bento choreography sparingly where product hierarchy calls for it. Analytical data tables, `<canvas>`, chart `<svg>`s, and 2D trajectory viewports should be marked `data-md3e-exempt="data-view"` (or rely on automatic exemption) so decorative waves/sparklines or border removal are never forced onto functional data UIs.

Then run the four-tier static auditor and regression suite:

```bash
python scripts/audit_md3e.py src                         # Default Official M3E + Web safety gate
python scripts/audit_md3e.py src --mode=desktop-bento    # Also evaluate Layer 3 CUSTOM extensions (excluded from Official Score)
python scripts/audit_md3e.py src --json                  # Emits official_compliance.{verdict,score} + custom_extensions
python scripts/audit_md3e.py src --fail-on warning       # Fail on ERROR or WARNING
python scripts/audit_md3e.py docs --markdown             # Audit HTML/CSS fences inside .md files
python scripts/test_md3e.py -v                           # Full token, generator, morph, and auditor test suite
```

### Authority Levels & Finding Codes

- **`ERROR`**: Explicit violation of Official Core M3E spec or WCAG 2.2 AA floor (reduces Official Score `-15/ea`).
- **`WARNING`**: Deviation from Official M3E recommended guidance (reduces Official Score `-5/ea`).
- **`INFO`**: Project-level engineering default/preference (`0` penalty to Official Score).
- **`CUSTOM`**: Opt-in product extension (`--mode=desktop-bento` only; **excluded from Official Score & default CI pass/fail**).

| Code | Authority Tier | Meaning |
|---|---|---|
| MD3E005 | `ERROR` | Focus outline removed (`outline: none/0`) or `:hover` styled without `:focus-visible` |
| MD3E006 | `ERROR` / `WARNING` | Interactive target `< 24×24px` WCAG AA floor (`ERROR`), or `24–47px` without `::before` `48px` expansion / visually inflated box (`WARNING`) |
| MD3E014 | `ERROR` | Icon-only interactive control missing accessible name |
| MD3E017 | `ERROR` | Hallucinated/invalid Material Symbols ligature, missing font `<link>`, or non-alphabetical Google Fonts axes |
| MD3E018 | `ERROR` | Unitless opacity in `color-mix()` or `color-mix(in oklch, ...)` on neutrals/surfaces |
| MD3E020 | `ERROR` | Legacy custom-element tags / Web Component bridge imports or invalid native interactive ARIA state/tabindex contract (`role="switch"` missing `aria-checked`, clickable `<div role="button">` missing `tabindex`, invalid boolean ARIA literal) |
| MD3E022 | `ERROR` | `backdrop-filter: blur(...)` missing `@media (prefers-reduced-transparency: reduce)` fallback |
| MD3E024 | `ERROR` | WCAG contrast `< 4.5:1` (`< 3.0:1` large text) or foreign container/`on-*` semantic role mismatch |
| MD3E004 | `WARNING` | Motion uses uncalibrated curve (`OFFICIAL_WEB_CURVES` and springs both pass with 0 findings) |
| MD3E008 | `WARNING` | Motion / `@keyframes` missing `prefers-reduced-motion` path |
| MD3E009 | `WARNING` | Colour role block missing dark theme path |
| MD3E011 | `WARNING` | `border-radius: 50%` instead of `corner-full` |
| MD3E013 | `WARNING` | `transition: all` usage |
| MD3E016 | `WARNING` | Deprecated small FAB (`40dp`) |
| MD3E019 | `WARNING` | Composite spring token in `animation:` shorthand (delay bug) or `9999px` radius morph snap/overshoot `0px` flash |
| MD3E021 | `WARNING` | Decorative icon inside labelled control missing `aria-hidden="true"` |
| MD3E023 | `WARNING` | Rectangular `box-shadow` directly on `.md3e-shape*`/masked shape instead of wrapper `filter: drop-shadow()` |
| MD3E026 | `WARNING` | Unbound MD3E modifier class missing base class (`.md3e-btn--*` without `.md3e-btn`, `.md3e-shape-*` without `.md3e-shape`) or deprecated `md3e-size-*` / `md3e-fab-medium` bridge class |
| MD3E001 | `INFO` | Hardcoded hex colour *(Project Default)* |
| MD3E002 | `INFO` | Hardcoded `rgb()` / `hsl()` / `oklch()` functional colour *(Project Default)* |
| MD3E003 | `INFO` | Custom/brand corner radius outside default 10-step scale *(Project Default)* |
| MD3E007 | `INFO` | Custom/brand font size outside default 11-step scale *(Project Default)* |
| MD3E010 | `INFO` | `box-shadow` used to express elevation *(Project Default)* |
| MD3E012 | `INFO` | Uppercase label text (M2 convention) |
| MD3E015 | `INFO` | Deprecated bottom app bar |
| MD3E025 | `INFO` | Multiple enabled primary `filled` buttons in a single view *(Project Default)* |
| MD3E101 | `CUSTOM` | *(desktop-bento)* Non-exempt `1px` border or rectangular `box-shadow` on Bento panel |
| MD3E102 | `CUSTOM` | *(desktop-bento)* `< 4` `surface-container-*` luminance tiers in non-exempt Bento doc |
| MD3E103 | `CUSTOM` | *(desktop-bento)* Missing concentric `28px` / `16px` Bento corner radii |
| MD3E104 | `CUSTOM` | *(desktop-bento)* Missing Hero wave / Sparkline / Morph CTA / Display KPI anchors (auto-exempts analytical `<canvas>`/chart/`<table>`/`data-md3e-exempt="data-view"` views) |

`audit_md3e.py` is a heuristic static checker (supporting `.html`, `.css`, `.js/.ts/.jsx/.tsx/.vue/.svelte`, inline `style="..."`, `--mode=strict|desktop-bento`, `data-md3e-exempt="data-view"`, and `--markdown` doc snippets). Follow every static gate with live browser verification. Token/theme files are auto-exempted from raw value `INFO` checks while still verified for contrast (`MD3E024`).

## Regenerating colour, shape & motion tokens

All computed token sheets are reproducible from zero-dependency Python scripts, and browser runtime dynamic extraction lives in `assets/tokens/md3e-dynamic-color.js`:

```bash
python scripts/color_to_css.py --seed "#0B57D0" --variant expressive --emit-css tokens/brand-colors.css
python scripts/color_to_css.py --image wallpaper.jpg --variant expressive --emit-css tokens/brand-colors.css
python scripts/color_to_css.py --emit-presets assets/tokens/md3e-palettes.css
python scripts/shapes_to_css.py --emit-css assets/tokens/md3e-shapes.css
python scripts/spring_to_css.py --table                     # print every token
python scripts/spring_to_css.py --emit-css assets/tokens/md3e-motion.css
python scripts/spring_to_css.py --stiffness 500 --damping 0.7   # custom spring
```

## Reference index

| File | Contents |
|---|---|
| `references/icons.md` | Material Symbols `<head>` setup, offline SVG fallback, hallucination-prevention name table, variable axes, a11y rules |
| `references/components/expressive-recipes.md` | Production HTML/CSS/JS recipes for Expressive components & Headless UI bindings (Toolbars, Split button, Button groups, FAB menu, 7-polygon Loader, real-time `md3e-morph.js` button, Wavy SVG+Canvas progress bar, Toggle & variable-width icon buttons, Flexible Top App Bar, Carousel, Nav rail, Clock dial & `md3e-blur.css` chrome) |
| `references/desktop-bento.md` | Opt-in Desktop High-Expressiveness Bento override layer (frameless shell, `32–36px` dense tables vs `44–64px` chunky controls, borderless 4+ tonal nesting, `28px/16px` concentric radii, Hero wave/sparkline/morph anchors, `150–250ms` desktop springs) |
| `references/tailwind.md` | Tailwind CSS v3 & v4 integration guide, theme extension mapping, `@theme` block |
| `references/color.md` | tonal palettes, 47 colour roles (including 12 Fixed roles), role→tone mapping, state layers, fixed roles, contrast levels |
| `references/typography.md` | 30 type styles with values, emphasized rule, typefaces, `GRAD`/`ROND`/`wght` spring axes, View Transitions container expansion, language height |
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

Fallbacks when a value is still missing: official `m3.material.io` token tables, Android
Developers' Compose Material 3 / `MaterialShapes` reference, or official M3
component token catalogs that cite the spec version.

Do **not** fill a gap with a plausible-looking number. An off-spec radius or
spring is worse than an explicitly flagged unknown, because it will be
implemented faithfully and be wrong. Where a value in this skill is a practical
derivation rather than a published token (the spacing scale, grid margins,
`full` expressed as `9999px`), the reference file says so.
