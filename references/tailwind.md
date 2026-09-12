# Tailwind CSS — Integration with MD3E Tokens

This guide explains how to configure and use **Tailwind CSS (v3 and v4)** with Material 3 Expressive (MD3E) design tokens.

By binding Tailwind classes to MD3E CSS Custom Properties (`--md-sys-*`), your application gains full dynamic theming, dark mode, high contrast, and motion spring support directly through utility classes (e.g. `bg-md-primary`, `rounded-md-lg`, `shadow-md-level2`).

---

## 1. Tailwind CSS v4 Configuration (`@theme`)

In Tailwind CSS v4, define custom tokens using the `@theme` directive in your main CSS file (e.g. `src/index.css`), imported after the MD3E token stylesheets:

```css
@import "./styles/md3e-tokens.css";
@import "./styles/md3e-motion.css";

@theme {
  /* MD3E Color Roles */
  --color-md-primary: var(--md-sys-color-primary);
  --color-md-on-primary: var(--md-sys-color-on-primary);
  --color-md-primary-container: var(--md-sys-color-primary-container);
  --color-md-on-primary-container: var(--md-sys-color-on-primary-container);

  --color-md-secondary: var(--md-sys-color-secondary);
  --color-md-on-secondary: var(--md-sys-color-on-secondary);
  --color-md-secondary-container: var(--md-sys-color-secondary-container);
  --color-md-on-secondary-container: var(--md-sys-color-on-secondary-container);

  --color-md-tertiary: var(--md-sys-color-tertiary);
  --color-md-on-tertiary: var(--md-sys-color-on-tertiary);
  --color-md-tertiary-container: var(--md-sys-color-tertiary-container);
  --color-md-on-tertiary-container: var(--md-sys-color-on-tertiary-container);

  --color-md-error: var(--md-sys-color-error);
  --color-md-on-error: var(--md-sys-color-on-error);
  --color-md-error-container: var(--md-sys-color-error-container);
  --color-md-on-error-container: var(--md-sys-color-on-error-container);

  --color-md-surface: var(--md-sys-color-surface);
  --color-md-on-surface: var(--md-sys-color-on-surface);
  --color-md-surface-variant: var(--md-sys-color-surface-variant);
  --color-md-on-surface-variant: var(--md-sys-color-on-surface-variant);
  --color-md-surface-container-lowest: var(--md-sys-color-surface-container-lowest);
  --color-md-surface-container-low: var(--md-sys-color-surface-container-low);
  --color-md-surface-container: var(--md-sys-color-surface-container);
  --color-md-surface-container-high: var(--md-sys-color-surface-container-high);
  --color-md-surface-container-highest: var(--md-sys-color-surface-container-highest);

  --color-md-outline: var(--md-sys-color-outline);
  --color-md-outline-variant: var(--md-sys-color-outline-variant);

  /* MD3E Ten-Step Shape Scale */
  --radius-md-none: var(--md-sys-shape-corner-none);
  --radius-md-xs: var(--md-sys-shape-corner-extra-small);
  --radius-md-sm: var(--md-sys-shape-corner-small);
  --radius-md-md: var(--md-sys-shape-corner-medium);
  --radius-md-lg: var(--md-sys-shape-corner-large);
  --radius-md-lg-inc: var(--md-sys-shape-corner-large-increased);
  --radius-md-xl: var(--md-sys-shape-corner-extra-large);
  --radius-md-xl-inc: var(--md-sys-shape-corner-extra-large-increased);
  --radius-md-2xl: var(--md-sys-shape-corner-extra-extra-large);
  --radius-md-full: var(--md-sys-shape-corner-full);

  /* MD3E Elevation */
  --shadow-md-level1: var(--md-sys-elevation-level1);
  --shadow-md-level2: var(--md-sys-elevation-level2);
  --shadow-md-level3: var(--md-sys-elevation-level3);
  --shadow-md-level4: var(--md-sys-elevation-level4);
  --shadow-md-level5: var(--md-sys-elevation-level5);
}
```

---

## 2. Tailwind CSS v3 Configuration (`tailwind.config.js`)

In Tailwind v3, extend the theme in `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,ts,jsx,tsx,vue,svelte}'],
  theme: {
    extend: {
      colors: {
        'md-primary': 'var(--md-sys-color-primary)',
        'md-on-primary': 'var(--md-sys-color-on-primary)',
        'md-primary-container': 'var(--md-sys-color-primary-container)',
        'md-on-primary-container': 'var(--md-sys-color-on-primary-container)',
        'md-secondary': 'var(--md-sys-color-secondary)',
        'md-on-secondary': 'var(--md-sys-color-on-secondary)',
        'md-secondary-container': 'var(--md-sys-color-secondary-container)',
        'md-on-secondary-container': 'var(--md-sys-color-on-secondary-container)',
        'md-tertiary': 'var(--md-sys-color-tertiary)',
        'md-on-tertiary': 'var(--md-sys-color-on-tertiary)',
        'md-tertiary-container': 'var(--md-sys-color-tertiary-container)',
        'md-on-tertiary-container': 'var(--md-sys-color-on-tertiary-container)',
        'md-surface': 'var(--md-sys-color-surface)',
        'md-on-surface': 'var(--md-sys-color-on-surface)',
        'md-surface-variant': 'var(--md-sys-color-surface-variant)',
        'md-on-surface-variant': 'var(--md-sys-color-on-surface-variant)',
        'md-surface-container-lowest': 'var(--md-sys-color-surface-container-lowest)',
        'md-surface-container-low': 'var(--md-sys-color-surface-container-low)',
        'md-surface-container': 'var(--md-sys-color-surface-container)',
        'md-surface-container-high': 'var(--md-sys-color-surface-container-high)',
        'md-surface-container-highest': 'var(--md-sys-color-surface-container-highest)',
        'md-outline': 'var(--md-sys-color-outline)',
        'md-outline-variant': 'var(--md-sys-color-outline-variant)',
      },
      borderRadius: {
        'md-none': 'var(--md-sys-shape-corner-none)',
        'md-xs': 'var(--md-sys-shape-corner-extra-small)',
        'md-sm': 'var(--md-sys-shape-corner-small)',
        'md-md': 'var(--md-sys-shape-corner-medium)',
        'md-lg': 'var(--md-sys-shape-corner-large)',
        'md-lg-inc': 'var(--md-sys-shape-corner-large-increased)',
        'md-xl': 'var(--md-sys-shape-corner-extra-large)',
        'md-xl-inc': 'var(--md-sys-shape-corner-extra-large-increased)',
        'md-2xl': 'var(--md-sys-shape-corner-extra-extra-large)',
        'md-full': 'var(--md-sys-shape-corner-full)',
      },
      boxShadow: {
        'md-level1': 'var(--md-sys-elevation-level1)',
        'md-level2': 'var(--md-sys-elevation-level2)',
        'md-level3': 'var(--md-sys-elevation-level3)',
        'md-level4': 'var(--md-sys-elevation-level4)',
        'md-level5': 'var(--md-sys-elevation-level5)',
      },
    },
  },
  plugins: [],
};
```

---

## 3. Tailwind Component Examples

### 3.1 MD3E Card
```html
<div class="bg-md-surface-container-low text-md-on-surface rounded-md-md p-6 shadow-md-level1">
  <h3 class="font-medium text-lg mb-2">Card Title</h3>
  <p class="text-md-on-surface-variant text-sm">Supporting copy rendered with proper contrast role.</p>
</div>
```

### 3.2 Filled Button (Primary Action)
```html
<button class="inline-flex items-center justify-center gap-2 h-10 px-4 min-h-[48px] bg-md-primary text-md-on-primary rounded-md-full font-medium text-sm transition-transform active:scale-95 focus-visible:outline-2 focus-visible:outline-md-secondary focus-visible:outline-offset-2">
  <span class="material-symbols-outlined text-lg">check</span>
  Confirm
</button>
```

### 3.3 Tonal Button
```html
<button class="inline-flex items-center justify-center gap-2 h-10 px-4 min-h-[48px] bg-md-secondary-container text-md-on-secondary-container rounded-md-full font-medium text-sm transition-transform active:scale-95">
  Cancel
</button>
```
