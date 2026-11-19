# MD3E Self-Hosted Fonts & Icons (`assets/fonts/`)

This directory ships local WOFF2 variable fonts so MD3E typography (`GRAD`, `ROND`, `opsz`, `wdth`, `wght`) and Material Symbols Outlined icons (`FILL`, `GRAD`, `opsz`, `wght`) work **100% offline** with zero reliance on `fonts.googleapis.com`.

## Included Files

| File | Font / Purpose | Variable Axes | License |
|---|---|---|---|
| `md3e-fonts.css` | Local `@font-face` declarations (`font-display: swap` for text, `block` for icons) | — | Apache-2.0 / OFL-1.1 |
| `google-sans-flex-latin.woff2` | Google Sans Flex (Latin) | `GRAD`, `ROND`, `opsz`, `wdth`, `wght` | SIL OFL 1.1 (`Copyright 2015 Google LLC`) |
| `google-sans-flex-latin-ext.woff2` | Google Sans Flex (Latin Extended) | `GRAD`, `ROND`, `opsz`, `wdth`, `wght` | SIL OFL 1.1 |
| `roboto-flex-latin.woff2` | Roboto Flex (Latin) | `GRAD`, `opsz`, `wdth`, `wght` | SIL OFL 1.1 (`Copyright 2017 The Roboto Flex Project Authors`) |
| `roboto-flex-latin-ext.woff2` | Roboto Flex (Latin Extended) | `GRAD`, `opsz`, `wdth`, `wght` | SIL OFL 1.1 |
| `material-symbols-outlined.woff2` | Material Symbols Outlined | `FILL`, `GRAD`, `opsz`, `wght` | SIL OFL 1.1 / Apache 2.0 (`Google Inc.`) |
| `OFL-1.1-LICENSE.txt` | Full SIL Open Font License 1.1 text | — | — |

## Usage

### Default (Offline-First)

```html
<link rel="stylesheet" href="./assets/fonts/md3e-fonts.css">
<link rel="stylesheet" href="./assets/tokens/md3e-tokens.css">
<link rel="stylesheet" href="./assets/tokens/md3e-motion.css">
<link rel="stylesheet" href="./assets/components/md3e-components.css">
```

`md3e-tokens.css` includes CJK fallback (`"PingFang SC", "Noto Sans SC", "Microsoft YaHei"`) after `"Google Sans Flex", "Roboto Flex", "Roboto"`, plus `:lang(zh/ja/ko)` line-height adaptation.

### Alternative 1: Bundler / npm (`@fontsource-variable/*`)

If your app already uses Vite / Webpack / Next.js and prefers npm-managed fonts:

```bash
npm install @fontsource-variable/google-sans-flex @fontsource-variable/roboto-flex @fontsource-variable/material-symbols-outlined
```

### Alternative 2: Refreshing Local WOFF2 Files

```bash
python scripts/fetch_fonts.py
```

### Alternative 3: Google Fonts CDN (Optional Online Fallback)

Only use CDN links if asset bundle size must be zero and target users have reliable access to `fonts.googleapis.com` (axes MUST stay alphabetical):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:GRAD,ROND,opsz,wdth,wght@-50..200,0..100,6..144,25..151,100..1000&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:GRAD,opsz,wdth,wght@-20..150,8..144,25..151,100..1000&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block">
```
