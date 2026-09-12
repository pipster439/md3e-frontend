# Material Web (@material/web) — Integration Guide for MD3E

Source: Official Google Material Web Components repository (<https://github.com/material-components/material-web>)
Package: `@material/web` (npm) / `https://esm.run/@material/web/` (CDN)

Material Web is Google's official, production-ready Web Components implementation of Material Design 3. It is built on standard Web Components (Custom Elements, Shadow DOM, CSS Custom Properties, and `::part`).

Because `@material/web` was developed against baseline M3 and placed into maintenance mode prior to the full Material 3 Expressive (May 2025+) release, **this guide and skill bridge the gap**: how to style `@material/web` to adhere to MD3E, and how to supplement it with the missing Expressive components.

---

## 1. Component Inventory: `@material/web` vs. MD3E

| Category | `@material/web` Component Tag | MD3E Status | Expressive Upgrade Required? |
|---|---|---|---|
| **Buttons** | `<md-filled-button>`<br>`<md-outlined-button>`<br>`<md-elevated-button>`<br>`<md-filled-tonal-button>`<br>`<md-text-button>` | Baseline M3 (40dp height, pill shape) | **Yes**: Needs MD3E 5-size support (32/40/56/96/136dp), square button shape (12/16/28dp), and pressed shape morphing. |
| **Icon Buttons** | `<md-icon-button>`<br>`<md-filled-icon-button>`<br>`<md-filled-tonal-icon-button>`<br>`<md-outlined-icon-button>` | Baseline M3 | **Yes**: Needs 5-size support and shape morph. |
| **Floating Action Button** | `<md-fab>`<br>`<md-branded-fab>` | Standard 56dp & small 40dp | **Yes**: Small FAB (40dp) is **deprecated**; use Standard (56dp) or Medium (80dp). Needs corner radius update (16/20/28dp). |
| **Split Button** | *None* | **New in MD3E** | **Build from recipe**: Use `references/components/expressive-recipes.md`. |
| **Button Groups** | *None* | **New in MD3E** | **Build from recipe**: Use `references/components/expressive-recipes.md`. |
| **FAB Menu** | *None* | **New in MD3E** | **Build from recipe**: Use `references/components/expressive-recipes.md`. |
| **Toolbars** | *None* | **New in MD3E** | **Build from recipe**: Docked & floating toolbars replace deprecated bottom app bar. |
| **Loading Indicator** | *None* (only linear/circular progress) | **New in MD3E** | **Build from recipe**: Morphing shape loader for waits < 5s. |
| **Text Fields** | `<md-filled-text-field>`<br>`<md-outlined-text-field>` | Standard M3 | Compatible. Set MD3E typography & corner tokens. |
| **Select** | `<md-filled-select>`<br>`<md-outlined-select>` | Standard M3 | Compatible. Inherits MD3E tokens. |
| **Selection Controls** | `<md-checkbox>`<br>`<md-radio>`<br>`<md-switch>`<br>`<md-slider>` | Standard M3 | Fully compliant when styled with MD3E color roles and state layers. |
| **Chips** | `<md-chip-set>`<br>`<md-assist-chip>`<br>`<md-filter-chip>`<br>`<md-input-chip>`<br>`<md-suggestion-chip>` | Standard M3 | Compatible. Add shape morphing on selection. |
| **Menus & Dialogs** | `<md-menu>`, `<md-menu-item>`<br>`<md-dialog>` | Standard M3 | Compatible. Apply MD3E surface container roles. |
| **Lists** | `<md-list>`, `<md-list-item>` | Baseline M3 | Add Expressive list styling (rounded container, emphasized label). |
| **Tabs** | `<md-tabs>`, `<md-primary-tab>`, `<md-secondary-tab>` | Standard M3 | Compatible. Set emphasized typography for active tab. |
| **Progress** | `<md-linear-progress>`<br>`<md-circular-progress>` | Standard M3 | Expressive progress indicators gain rounded caps and 4dp track gap. |
| **Primitives** | `<md-ripple>`, `<md-focus-ring>`, `<md-elevation>`, `<md-icon>`, `<md-divider>` | Internal building blocks | Use inside custom Expressive components. |

---

## 2. Quick Installation & Setup

### Option A: npm / bundler (Vite, Next.js, Nuxt, Webpack)

```bash
npm install @material/web
```

Import components in your JavaScript/TypeScript entry point:

```typescript
// Import individual components to keep bundle size small
import '@material/web/button/filled-button.js';
import '@material/web/button/outlined-button.js';
import '@material/web/button/filled-tonal-button.js';
import '@material/web/button/elevated-button.js';
import '@material/web/button/text-button.js';
import '@material/web/iconbutton/icon-button.js';
import '@material/web/fab/fab.js';
import '@material/web/checkbox/checkbox.js';
import '@material/web/radio/radio.js';
import '@material/web/switch/switch.js';
import '@material/web/slider/slider.js';
import '@material/web/textfield/filled-text-field.js';
import '@material/web/textfield/outlined-text-field.js';
import '@material/web/dialog/dialog.js';
import '@material/web/menu/menu.js';
import '@material/web/menu/menu-item.js';
import '@material/web/tabs/tabs.js';
import '@material/web/tabs/primary-tab.js';
import '@material/web/icon/icon.js';
import '@material/web/divider/divider.js';
```

### Option B: CDN / Native ES Modules (No build step required)

Add Material Symbols font and ESM imports directly to `<head>`:

```html
<!-- Material Symbols Icons font -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200">

<!-- MD3E Token Layer & Material Web Bridge -->
<link rel="stylesheet" href="/styles/md3e-tokens.css">
<link rel="stylesheet" href="/styles/md3e-motion.css">
<link rel="stylesheet" href="/styles/md3e-material-web.css">

<!-- Load Material Web Components -->
<script type="module">
  import 'https://esm.run/@material/web/all.js';
</script>
```

---

## 3. Token Hierarchy & `@material/web` Mapping

Material Web components resolve tokens through a 3-tier structure:

```
1. Reference Tokens (--md-ref-palette-*)
        ↓ (mapped to)
2. System Tokens (--md-sys-color-*, --md-sys-shape-*, --md-sys-typescale-*)
        ↓ (consumed by)
3. Component Tokens (--md-<component>-<part>-<property>)
```

### Component Token Names Convention
Every `@material/web` component exposes custom CSS properties following this scheme:
`--md-<component>-<part>-<property>`

For example, `<md-filled-button>` exposes:
- `--md-filled-button-container-color`
- `--md-filled-button-container-height`
- `--md-filled-button-container-shape`
- `--md-filled-button-label-text-color`
- `--md-filled-button-label-text-font`
- `--md-filled-button-label-text-size`
- `--md-filled-button-label-text-weight`
- `--md-filled-button-icon-size`
- `--md-filled-button-hover-state-layer-opacity`
- `--md-filled-button-pressed-state-layer-opacity`

### Turnkey Bridge: `md3e-material-web.css`
Instead of configuring dozens of component tokens manually on every element, use `assets/tokens/md3e-material-web.css`. It automatically connects all `@material/web` components to the MD3E design tokens on `:root`.

---

## 4. Retrofitting `@material/web` for MD3E

### 4.1 The 5 Button Sizes on `<md-filled-button>`
Baseline `@material/web` only renders 40dp buttons. With `md3e-material-web.css`, you can use size utility classes:

```html
<!-- Extra Small: 32dp height, 12dp padding, 20dp icon -->
<md-filled-button class="md3e-size-xs">XS Action</md-filled-button>

<!-- Small: 40dp height (default), 16dp padding, 20dp icon -->
<md-filled-button class="md3e-size-s">Small Action</md-filled-button>

<!-- Medium: 56dp height, 24dp padding, 24dp icon -->
<md-filled-button class="md3e-size-m">Medium Action</md-filled-button>

<!-- Large: 96dp height, 48dp padding, 32dp icon -->
<md-filled-button class="md3e-size-l">Large Action</md-filled-button>

<!-- Extra Large: 136dp height, 64dp padding, 40dp icon -->
<md-filled-button class="md3e-size-xl">XL Action</md-filled-button>
```

Under the hood, these classes set the component tokens:
```css
.md3e-size-m {
  --md-filled-button-container-height: 56px;
  --md-filled-button-leading-space: 24px;
  --md-filled-button-trailing-space: 24px;
  --md-filled-button-icon-size: 24px;
  --md-filled-button-label-text-size: var(--md-sys-typescale-title-medium-size);
}
```

### 4.2 Square Button Shapes on `<md-filled-button>`
In MD3E, buttons can be round (pill) or square (12dp/16dp/28dp corner):

```html
<!-- Square Medium Button (16dp corner) -->
<md-filled-button class="md3e-size-m md3e-shape-square">Square Button</md-filled-button>
```

### 4.3 Medium FAB (80dp)
Small FAB (40dp) is deprecated in MD3E. Use Standard (56dp) or Medium (80dp):

```html
<!-- Standard FAB (56dp, 16dp corner) -->
<md-fab aria-label="Add item">
  <md-icon slot="icon">add</md-icon>
</md-fab>

<!-- Medium FAB (80dp, 20dp corner) -->
<md-fab class="md3e-fab-medium" aria-label="Compose">
  <md-icon slot="icon">edit</md-icon>
</md-fab>
```

---

## 5. Framework Integrations

### 5.1 React (React 19 & React 18)

#### React 19
React 19 natively supports Custom Elements! You can pass props, attributes, and native event listeners directly:

```tsx
import '@material/web/button/filled-button.js';
import '@material/web/icon/icon.js';

export function ActionButton() {
  return (
    <md-filled-button onClick={() => console.log('Clicked!')}>
      <md-icon slot="icon">send</md-icon>
      Send Message
    </md-filled-button>
  );
}
```

#### React 18 and Earlier (with `@lit/react`)
React 18 does not automatically sync custom properties or events. Use `@lit/react`:

```bash
npm install @lit/react
```

```tsx
import React from 'react';
import { createComponent } from '@lit/react';
import { MdFilledButton } from '@material/web/button/filled-button.js';
import { MdSwitch } from '@material/web/switch/switch.js';

export const FilledButton = createComponent({
  tagName: 'md-filled-button',
  elementClass: MdFilledButton,
  react: React,
  events: {
    // map custom events if needed
  },
});

export const Switch = createComponent({
  tagName: 'md-switch',
  elementClass: MdSwitch,
  react: React,
  events: {
    onChange: 'change',
  },
});
```

### 5.2 Vue 3
Configure Vite/Vue compiler to recognize `<md-*>` custom tags:

In `vite.config.ts`:
```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('md-'),
        },
      },
    }),
  ],
});
```

Usage in Vue templates:
```vue
<template>
  <md-filled-button @click="handleClick">
    <md-icon slot="icon">check</md-icon>
    Confirm
  </md-filled-button>
</template>

<script setup lang="ts">
import '@material/web/button/filled-button.js';
import '@material/web/icon/icon.js';

const handleClick = () => {
  // handle click
};
</script>
```

### 5.3 Svelte / SvelteKit
Svelte natively supports Custom Elements without any special wrapper:

```svelte
<script>
  import { onMount } from 'svelte';
  onMount(async () => {
    await import('@material/web/button/filled-button.js');
    await import('@material/web/icon/icon.js');
  });
</script>

<md-filled-button on:click={() => alert('Svelte clicked')}>
  <md-icon slot="icon">thumb_up</md-icon>
  Like
</md-filled-button>
```

### 5.4 Next.js / SSR Frameworks (Crucial!)
Because Custom Elements require browser APIs (`window`, `customElements`), importing `@material/web` during server-side rendering (SSR) will throw `ReferenceError: window is not defined`.

**Solution 1: Dynamic Client Import (React `useEffect`)**
```tsx
'use client';
import { useEffect, useState } from 'react';

export function ClientMaterialProvider({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    Promise.all([
      import('@material/web/button/filled-button.js'),
      import('@material/web/textfield/outlined-text-field.js'),
      import('@material/web/icon/icon.js'),
    ]).then(() => setMounted(true));
  }, []);

  if (!mounted) return null; // Or render standard HTML fallback during SSR
  return <>{children}</>;
}
```

**Solution 2: Use Pure MD3E HTML/CSS Recipes for SSR-critical Pages**
For public landing pages, SSR layouts, and SEO-critical content, use pure semantic HTML + `md3e-tokens.css` (see `references/components/expressive-recipes.md`). Use `@material/web` for complex interactive client components (modals, sliders, selects, menus).

---

## 6. Common Pitfalls & How to Avoid Them

| Pitfall | Problem | MD3E Correction |
|---|---|---|
| `style="background: #6750A4"` on `<md-filled-button>` | Shadow DOM encapsulation ignores external background styling on custom element container. | Use component tokens: `style="--md-filled-button-container-color: var(--md-sys-color-primary)"`. |
| `<md-icon-button>` without `aria-label` | Screen readers cannot deduce icon button intent. | Always add `aria-label="Action description"`. |
| Sub-48px touch target on small controls | Violates WCAG 2.5.5 and MD3E accessibility rule. | Touch target defaults to 48px; do not set `height: 32px` on `<md-icon-button>` without maintaining the 48px click target. |
| Using deprecated small FAB (40dp) | Small FAB was removed in MD3E in favor of Standard 56dp and Medium 80dp. | `<md-fab>` (56dp) or `<md-fab class="md3e-fab-medium">` (80dp). |
| Mixing M2 uppercase text | All labels in `@material/web` must be sentence-case. | Never set `text-transform: uppercase`. |
| Missing Material Symbols stylesheet | Icons render as literal text strings like "search" or "close". | Always include the Google Fonts Material Symbols link in `<head>`. |
