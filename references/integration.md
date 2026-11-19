# Integration & Coexistence Guide (Tailwind / MUI / Ant Design / Custom Tokens)

When adding MD3E to an **existing** application that already ships Tailwind CSS, Material UI (MUI), Ant Design (`antd`), or its own `--color-*` / `--radius-*` CSS variables, keep **one source of truth** by loading stylesheets in deterministic cascade order and mapping existing design tokens onto `--md-sys-*` rather than running two competing palettes side by side.

---

## 1. Recommended Asset Layout & Import Order

Copy the `assets/` directory intact (preserving relative paths for `fonts/`, `tokens/`, and `components/`) and load layers in this order:

1. **Fonts** (`assets/fonts/md3e-fonts.css`) — offline `@font-face` declarations for Google Sans Flex, Roboto Flex, and Material Symbols Outlined.
2. **Tokens** (`assets/tokens/md3e-tokens.css` + `assets/tokens/md3e-motion.css`) — 47 colour roles, 30 typescale tokens with CJK fallback, 10 corners, and physical springs.
3. **Components** (`assets/components/md3e-components.css` or individual files like `assets/components/button.css`).
4. **Framework Bridge / App Overrides** (Tailwind `@theme`, MUI `CssVarsProvider`, Ant Design `ConfigProvider`, or your token alias sheet).

`assets/components/*.css` scopes `box-sizing: border-box` strictly to `.md3e-*` / component selectors and never sets global `*`, `html`, or `body` resets, so it will not disturb your host layout.

---

## 2. Coexisting with Tailwind CSS (v3 & v4)

Do not invent parallel Tailwind colors (`bg-purple-600`, `rounded-lg`) on MD3E surfaces. Bind Tailwind utilities directly to MD3E tokens using `assets/tailwind/md3e-theme.css` (v4) or `assets/tailwind/tailwind.config.js` (v3).

### Tailwind v4 (`app.css`)

```css
@import "tailwindcss";
@import "./assets/fonts/md3e-fonts.css";
@import "./assets/tokens/md3e-tokens.css";
@import "./assets/tokens/md3e-motion.css";
@import "./assets/tailwind/md3e-theme.css";
@import "./assets/components/md3e-components.css" layer(components);
```

Wrapping `md3e-components.css` in `layer(components)` lets Tailwind utility classes (for example `mt-4`, `w-full`, `md-medium:px-8`) override component spacing cleanly without `!important`.

### Conflicts to Avoid in Tailwind

- **Tailwind v3 Preflight `button` reset**: Tailwind v3's `@tailwind base` sets `button { background-color: transparent; background-image: none; }`. Because `.md3e-btn--filled` has higher specificity than `button`, it wins **unless** you put `md3e-components.css` *before* unlayered overrides or inside `@layer base`. Always import `md3e-components.css` in `@layer components` or **after** `@tailwind base;`.
- **Tailwind Preflight `border-width: 0`**: Preflight sets `*, ::before, ::after { border-width: 0; border-style: solid; }`. MD3E components explicitly declare borders (`border: 1px solid ...` on `.md3e-field__outline`, `2px solid ...` on `.md3e-switch` / `.md3e-checkbox`), so keep `@tailwind base` *before* MD3E component stylesheets.
- **Arbitrary shadows vs tonal surfaces**: Prefer `bg-md-surface-container-low` / `bg-md-surface-container-high` over Tailwind `shadow-md` / `border-gray-200` on cards.

See [`tailwind.md`](tailwind.md) for the complete v3/v4 utility reference.

---

## 3. Coexisting with Material UI (MUI v5 / v6)

If your app already renders `<Button>`, `<TextField>`, or `<Dialog>` from `@mui/material` while adopting MD3E tokens and `.md3e-*` components on new views, enable MUI CSS variables and map MUI's palette and shape variables onto `--md-sys-*`:

```css
/* Load AFTER md3e-tokens.css and MUI CssBaseline */
:root {
  --mui-palette-primary-main: var(--md-sys-color-primary);
  --mui-palette-primary-contrastText: var(--md-sys-color-on-primary);
  --mui-palette-secondary-main: var(--md-sys-color-secondary);
  --mui-palette-secondary-contrastText: var(--md-sys-color-on-secondary);
  --mui-palette-error-main: var(--md-sys-color-error);
  --mui-palette-error-contrastText: var(--md-sys-color-on-error);
  --mui-palette-background-default: var(--md-sys-color-surface);
  --mui-palette-background-paper: var(--md-sys-color-surface-container-low);
  --mui-palette-text-primary: var(--md-sys-color-on-surface);
  --mui-palette-text-secondary: var(--md-sys-color-on-surface-variant);
  --mui-palette-divider: var(--md-sys-color-outline-variant);
  --mui-shape-borderRadius: 12px;
}
```

### Conflicts to Avoid in MUI

- **`<CssBaseline />` global body font/background**: Configure `typography.fontFamily` in `createTheme` to `'var(--md-sys-typescale-plain-font)'` so MUI components share the same Google Sans Flex + CJK fallback stack.
- **`z-index` stacking with MUI `<Modal>` / `<Menu>` (`1300`)**: Native `<dialog>.showModal()` and `[popover="auto"]` render in the browser **Top Layer** above every `z-index`. Do not open an MUI portal popover inside a native `<dialog>` unless it targets the dialog container; keep floating `.toolbar-floating` (`z-index: 100`) and `.fab-menu-container` (`z-index: 900`) below MUI's `1300` backdrop when both exist on the same route.
- **Scoped `.md3e-field` vs MUI `<TextField>`**: Use one or the other per form — both target `56px` height and outlined fieldset notches, so pairing them in the same row works cleanly once typography and `--md-sys-color-outline` match.

---

## 4. Coexisting with Ant Design (`antd` v5+)

In Ant Design v5+, turn on `cssVar: true` in `ConfigProvider` and feed `--md-sys-*` values into the theme token object (or override `--ant-*` CSS variables):

```tsx
// App.tsx (Ant Design v5 ConfigProvider + MD3E tokens)
import { ConfigProvider } from 'antd';

export function AppTheme({ children }: { children: React.ReactNode }) {
  return (
    <ConfigProvider
      theme={{
        cssVar: true,
        token: {
          fontFamily: 'var(--md-sys-typescale-plain-font)',
          colorPrimary: 'var(--md-sys-color-primary)',
          colorError: 'var(--md-sys-color-error)',
          colorBgLayout: 'var(--md-sys-color-surface)',
          colorBgContainer: 'var(--md-sys-color-surface-container-low)',
          colorBgElevated: 'var(--md-sys-color-surface-container-high)',
          colorText: 'var(--md-sys-color-on-surface)',
          colorTextSecondary: 'var(--md-sys-color-on-surface-variant)',
          colorBorder: 'var(--md-sys-color-outline-variant)',
          borderRadius: 12,
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
}
```

### Conflicts to Avoid in Ant Design

- **`antd/dist/reset.css` button/input resets**: `reset.css` sets `button, input { font-family: inherit; }` and removes outlines. Ensure `md3e-components.css` loads **after** `antd/dist/reset.css` so `.md3e-btn:focus-visible` (`outline: 3px solid var(--md-sys-color-secondary)`) and `.md3e-switch` borders are preserved.
- **Dark mode sync**: Ant Design defaults to its light algorithm unless `theme.algorithm = theme.darkAlgorithm` is switched alongside `[data-theme="dark"]` / `prefers-color-scheme: dark`. Keep both driven from the same state root so MD3E components never sit in dark mode inside a light Ant Design shell.
- **Data tables**: Mark dense `<Table>` analytics regions with `data-md3e-exempt="data-view"` (or rely on automatic `<table>` exemption) when auditing with `audit_md3e.py`.

---

## 5. Mapping Existing Custom Project Tokens (`--color-*`, `--brand-*`, `--radius-*`)

If your codebase already has CSS variables (for example `--bg-page`, `--brand-primary`, `--radius-md`), follow this two-step rule:

1. **Generate MD3E palettes from your brand hex** (keeps your brand hue while guaranteeing 47 valid contrast-checked roles across light/dark/high-contrast):
   ```bash
   python scripts/color_to_css.py --seed "#0B57D0" --variant expressive --emit-css ./src/styles/brand-colors.css
   ```
   Import `brand-colors.css` **after** `md3e-tokens.css`.
2. **Alias legacy variable names to `--md-sys-*`** so legacy styles automatically follow light/dark/seed changes without rewriting every old file at once:

| Legacy Custom Variable | MD3E Target Token | Notes |
|---|---|---|
| `--bg-page`, `--bg-canvas` | `var(--md-sys-color-surface)` | Base canvas |
| `--bg-card`, `--bg-panel` | `var(--md-sys-color-surface-container-low)` | Elevated card / pane fill |
| `--bg-muted`, `--bg-well` | `var(--md-sys-color-surface-container)` | Default container tier |
| `--bg-hover`, `--bg-input` | `var(--md-sys-color-surface-container-high)` | High-emphasis surface |
| `--text-primary`, `--fg-default` | `var(--md-sys-color-on-surface)` | Body & heading ink |
| `--text-muted`, `--fg-secondary` | `var(--md-sys-color-on-surface-variant)` | Labels, helpers, icons |
| `--brand-primary`, `--accent` | `var(--md-sys-color-primary)` | Primary CTA fill / accent |
| `--brand-on-primary` | `var(--md-sys-color-on-primary)` | Text/icons on `--md-sys-color-primary` |
| `--accent-soft`, `--badge-bg` | `var(--md-sys-color-secondary-container)` | Tonal pills & active nav indicators |
| `--accent-soft-text` | `var(--md-sys-color-on-secondary-container)` | Ink on tonal pills |
| `--border-subtle`, `--divider` | `var(--md-sys-color-outline-variant)` | Subtle 1px hairlines |
| `--border-strong`, `--input-border` | `var(--md-sys-color-outline)` | Interactive control borders |
| `--danger`, `--error` | `var(--md-sys-color-error)` | Destructive / validation state |
| `--font-sans`, `--font-body` | `var(--md-sys-typescale-plain-font)` | Google Sans Flex + Roboto Flex + CJK fallback |
| `--font-display`, `--font-heading` | `var(--md-sys-typescale-brand-font)` | Brand display stack |
| `--radius-sm` / `--radius-md` / `--radius-lg` | `var(--md-sys-shape-corner-small)` / `-medium` / `-large` | `8px` / `12px` / `16px` |
| `--radius-xl` / `--radius-pill` | `var(--md-sys-shape-corner-extra-large)` / `-full` | `28px` / `9999px` |
| `--ease-spring` | `var(--md-sys-motion-default-spatial)` | Or `--md-sys-motion-fast-spatial` |

### Compatibility Alias Snippet

```css
:root {
  --bg-page: var(--md-sys-color-surface);
  --bg-card: var(--md-sys-color-surface-container-low);
  --text-primary: var(--md-sys-color-on-surface);
  --text-muted: var(--md-sys-color-on-surface-variant);
  --brand-primary: var(--md-sys-color-primary);
  --brand-on-primary: var(--md-sys-color-on-primary);
  --border-subtle: var(--md-sys-color-outline-variant);
  --font-sans: var(--md-sys-typescale-plain-font);
  --radius-md: var(--md-sys-shape-corner-medium);
}
```

---

## 6. Common Integration Pitfalls Checklist

1. **Duplicate dark-mode toggles**: Do not toggle `.dark` on `<body>` while leaving `data-theme="light"` on `<html>`. Drive both from `data-theme="light" | "dark"` on `<html>` (or omit `data-theme` to follow OS `prefers-color-scheme`).
2. **Global `button { padding: 0; }` or `input { appearance: auto; }`**: Never load global resets *after* `md3e-components.css` — it strips `.md3e-btn` padding and brings back OS grey slider/switch chrome.
3. **Missing `.md3e-tokens.css` / `.md3e-motion.css`**: Component classes in `assets/components/` consume `--md-sys-color-*`, `--md-sys-shape-*`, `--md-sys-spacing-*`, and `--md-sys-motion-*`. Always import `md3e-tokens.css` and `md3e-motion.css` before `md3e-components.css`.
4. **Scoped rollouts**: When migrating one screen at a time, import `md3e-tokens.css` + `md3e-components.css` safely — component selectors only style explicit classes (`.md3e-btn`, `.md3e-switch`, `.md3e-dialog`, `.md3e-field`, etc.) plus `dialog:modal { overscroll-behavior: contain; }` and will not alter unrelated legacy `<button>` or `<input>` tags.
