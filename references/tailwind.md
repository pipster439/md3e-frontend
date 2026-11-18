# Tailwind CSS — Integration with MD3E Tokens

This guide explains how to configure and use **Tailwind CSS (v3 and v4)** with Material 3 Expressive (MD3E) design tokens. Ready-to-use files live in `assets/tailwind/md3e-theme.css` (v4) and `assets/tailwind/tailwind.config.js` (v3).

By binding Tailwind utilities to MD3E CSS Custom Properties (`--md-sys-*`), your application gains full dynamic theming, dark mode, high contrast, 30 typography scales, 10-step corners, 6 elevation levels, 5 adaptive breakpoints, desktop density/layout tokens, and motion spring + `-bezier` support (e.g. `bg-md-primary`, `text-md-title-medium`, `rounded-md-lg`, `shadow-md-level2`, `md-large:grid-cols-2`).

---

## 1. Tailwind CSS v4 Configuration (`@theme`)

In Tailwind CSS v4, import `md3e-tokens.css` and `md3e-motion.css` first, then either `@import "./tailwind/md3e-theme.css";` directly or paste the `@theme` block below (synced 1:1 with `assets/tailwind/md3e-theme.css`):

```css
@import "./tokens/md3e-tokens.css";
@import "./tokens/md3e-motion.css";

@theme {
  /* --- Colour roles (47 MD3E system tokens) -------------------------------- */
  --color-md-primary: var(--md-sys-color-primary);
  --color-md-on-primary: var(--md-sys-color-on-primary);
  --color-md-primary-container: var(--md-sys-color-primary-container);
  --color-md-on-primary-container: var(--md-sys-color-on-primary-container);
  --color-md-primary-fixed: var(--md-sys-color-primary-fixed);
  --color-md-primary-fixed-dim: var(--md-sys-color-primary-fixed-dim);
  --color-md-on-primary-fixed: var(--md-sys-color-on-primary-fixed);
  --color-md-on-primary-fixed-variant: var(--md-sys-color-on-primary-fixed-variant);

  --color-md-secondary: var(--md-sys-color-secondary);
  --color-md-on-secondary: var(--md-sys-color-on-secondary);
  --color-md-secondary-container: var(--md-sys-color-secondary-container);
  --color-md-on-secondary-container: var(--md-sys-color-on-secondary-container);
  --color-md-secondary-fixed: var(--md-sys-color-secondary-fixed);
  --color-md-secondary-fixed-dim: var(--md-sys-color-secondary-fixed-dim);
  --color-md-on-secondary-fixed: var(--md-sys-color-on-secondary-fixed);
  --color-md-on-secondary-fixed-variant: var(--md-sys-color-on-secondary-fixed-variant);

  --color-md-tertiary: var(--md-sys-color-tertiary);
  --color-md-on-tertiary: var(--md-sys-color-on-tertiary);
  --color-md-tertiary-container: var(--md-sys-color-tertiary-container);
  --color-md-on-tertiary-container: var(--md-sys-color-on-tertiary-container);
  --color-md-tertiary-fixed: var(--md-sys-color-tertiary-fixed);
  --color-md-tertiary-fixed-dim: var(--md-sys-color-tertiary-fixed-dim);
  --color-md-on-tertiary-fixed: var(--md-sys-color-on-tertiary-fixed);
  --color-md-on-tertiary-fixed-variant: var(--md-sys-color-on-tertiary-fixed-variant);

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
  --color-md-surface-dim: var(--md-sys-color-surface-dim);
  --color-md-surface-bright: var(--md-sys-color-surface-bright);

  --color-md-outline: var(--md-sys-color-outline);
  --color-md-outline-variant: var(--md-sys-color-outline-variant);
  --color-md-inverse-surface: var(--md-sys-color-inverse-surface);
  --color-md-inverse-on-surface: var(--md-sys-color-inverse-on-surface);
  --color-md-inverse-primary: var(--md-sys-color-inverse-primary);
  --color-md-scrim: var(--md-sys-color-scrim);
  --color-md-shadow: var(--md-sys-color-shadow);
  --color-md-surface-tint: var(--md-sys-color-surface-tint);

  /* --- Spacing, desktop layout, nav rail & visual density (4px base grid) -- */
  --spacing-md-1: var(--md-sys-spacing-1);
  --spacing-md-2: var(--md-sys-spacing-2);
  --spacing-md-3: var(--md-sys-spacing-3);
  --spacing-md-4: var(--md-sys-spacing-4);
  --spacing-md-5: var(--md-sys-spacing-5);
  --spacing-md-6: var(--md-sys-spacing-6);
  --spacing-md-8: var(--md-sys-spacing-8);
  --spacing-md-10: var(--md-sys-spacing-10);
  --spacing-md-12: var(--md-sys-spacing-12);
  --spacing-md-16: var(--md-sys-spacing-16);
  --spacing-md-20: var(--md-sys-spacing-20);
  --spacing-md-touch: var(--md-sys-touch-target-min);
  --spacing-md-margin-compact: var(--md-sys-layout-margin-compact);
  --spacing-md-margin-medium: var(--md-sys-layout-margin-medium);
  --spacing-md-margin-expanded: var(--md-sys-layout-margin-expanded);
  --spacing-md-margin-large: var(--md-sys-layout-margin-large);
  --spacing-md-margin-extra-large: var(--md-sys-layout-margin-extra-large);
  --spacing-md-gutter-compact: var(--md-sys-layout-gutter-compact);
  --spacing-md-gutter-medium: var(--md-sys-layout-gutter-medium);
  --spacing-md-gutter-expanded: var(--md-sys-layout-gutter-expanded);
  --spacing-md-gutter-large: var(--md-sys-layout-gutter-large);
  --spacing-md-gutter-extra-large: var(--md-sys-layout-gutter-extra-large);
  --spacing-md-pane-gap: var(--md-sys-layout-pane-gap);
  --spacing-md-nav-rail-collapsed: var(--md-sys-nav-rail-width-collapsed);
  --spacing-md-nav-rail-expanded: var(--md-sys-nav-rail-width-expanded);
  --spacing-md-density-offset: var(--md-sys-density-offset);
  --container-md-measure: var(--md-sys-layout-measure-max);

  /* --- Shape corners (10-step MD3E corner scale) ---------------------------- */
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

  /* --- Elevation shadows (levels 0-5) -------------------------------------- */
  --shadow-md-level0: var(--md-sys-elevation-level0);
  --shadow-md-level1: var(--md-sys-elevation-level1);
  --shadow-md-level2: var(--md-sys-elevation-level2);
  --shadow-md-level3: var(--md-sys-elevation-level3);
  --shadow-md-level4: var(--md-sys-elevation-level4);
  --shadow-md-level5: var(--md-sys-elevation-level5);

  /* --- Typography (30 styles: 15 baseline + 15 emphasized) ----------------- */
  --font-md-brand: var(--md-sys-typescale-brand-font);
  --font-md-plain: var(--md-sys-typescale-plain-font);

  --text-md-display-large: var(--md-sys-typescale-display-large-size);
  --text-md-display-large--line-height: var(--md-sys-typescale-display-large-line-height);
  --text-md-display-large--letter-spacing: var(--md-sys-typescale-display-large-tracking);
  --text-md-display-large--font-weight: var(--md-sys-typescale-display-large-weight);
  --text-md-display-large-emphasized: var(--md-sys-typescale-display-large-size);
  --text-md-display-large-emphasized--line-height: var(--md-sys-typescale-display-large-line-height);
  --text-md-display-large-emphasized--letter-spacing: var(--md-sys-typescale-display-large-emphasized-tracking);
  --text-md-display-large-emphasized--font-weight: var(--md-sys-typescale-display-large-emphasized-weight);

  --text-md-display-medium: var(--md-sys-typescale-display-medium-size);
  --text-md-display-medium--line-height: var(--md-sys-typescale-display-medium-line-height);
  --text-md-display-medium--letter-spacing: var(--md-sys-typescale-display-medium-tracking);
  --text-md-display-medium--font-weight: var(--md-sys-typescale-display-medium-weight);
  --text-md-display-medium-emphasized: var(--md-sys-typescale-display-medium-size);
  --text-md-display-medium-emphasized--line-height: var(--md-sys-typescale-display-medium-line-height);
  --text-md-display-medium-emphasized--letter-spacing: var(--md-sys-typescale-display-medium-emphasized-tracking);
  --text-md-display-medium-emphasized--font-weight: var(--md-sys-typescale-display-medium-emphasized-weight);

  --text-md-display-small: var(--md-sys-typescale-display-small-size);
  --text-md-display-small--line-height: var(--md-sys-typescale-display-small-line-height);
  --text-md-display-small--letter-spacing: var(--md-sys-typescale-display-small-tracking);
  --text-md-display-small--font-weight: var(--md-sys-typescale-display-small-weight);
  --text-md-display-small-emphasized: var(--md-sys-typescale-display-small-size);
  --text-md-display-small-emphasized--line-height: var(--md-sys-typescale-display-small-line-height);
  --text-md-display-small-emphasized--letter-spacing: var(--md-sys-typescale-display-small-emphasized-tracking);
  --text-md-display-small-emphasized--font-weight: var(--md-sys-typescale-display-small-emphasized-weight);

  --text-md-headline-large: var(--md-sys-typescale-headline-large-size);
  --text-md-headline-large--line-height: var(--md-sys-typescale-headline-large-line-height);
  --text-md-headline-large--letter-spacing: var(--md-sys-typescale-headline-large-tracking);
  --text-md-headline-large--font-weight: var(--md-sys-typescale-headline-large-weight);
  --text-md-headline-large-emphasized: var(--md-sys-typescale-headline-large-size);
  --text-md-headline-large-emphasized--line-height: var(--md-sys-typescale-headline-large-line-height);
  --text-md-headline-large-emphasized--letter-spacing: var(--md-sys-typescale-headline-large-emphasized-tracking);
  --text-md-headline-large-emphasized--font-weight: var(--md-sys-typescale-headline-large-emphasized-weight);

  --text-md-headline-medium: var(--md-sys-typescale-headline-medium-size);
  --text-md-headline-medium--line-height: var(--md-sys-typescale-headline-medium-line-height);
  --text-md-headline-medium--letter-spacing: var(--md-sys-typescale-headline-medium-tracking);
  --text-md-headline-medium--font-weight: var(--md-sys-typescale-headline-medium-weight);
  --text-md-headline-medium-emphasized: var(--md-sys-typescale-headline-medium-size);
  --text-md-headline-medium-emphasized--line-height: var(--md-sys-typescale-headline-medium-line-height);
  --text-md-headline-medium-emphasized--letter-spacing: var(--md-sys-typescale-headline-medium-emphasized-tracking);
  --text-md-headline-medium-emphasized--font-weight: var(--md-sys-typescale-headline-medium-emphasized-weight);

  --text-md-headline-small: var(--md-sys-typescale-headline-small-size);
  --text-md-headline-small--line-height: var(--md-sys-typescale-headline-small-line-height);
  --text-md-headline-small--letter-spacing: var(--md-sys-typescale-headline-small-tracking);
  --text-md-headline-small--font-weight: var(--md-sys-typescale-headline-small-weight);
  --text-md-headline-small-emphasized: var(--md-sys-typescale-headline-small-size);
  --text-md-headline-small-emphasized--line-height: var(--md-sys-typescale-headline-small-line-height);
  --text-md-headline-small-emphasized--letter-spacing: var(--md-sys-typescale-headline-small-emphasized-tracking);
  --text-md-headline-small-emphasized--font-weight: var(--md-sys-typescale-headline-small-emphasized-weight);

  --text-md-title-large: var(--md-sys-typescale-title-large-size);
  --text-md-title-large--line-height: var(--md-sys-typescale-title-large-line-height);
  --text-md-title-large--letter-spacing: var(--md-sys-typescale-title-large-tracking);
  --text-md-title-large--font-weight: var(--md-sys-typescale-title-large-weight);
  --text-md-title-large-emphasized: var(--md-sys-typescale-title-large-size);
  --text-md-title-large-emphasized--line-height: var(--md-sys-typescale-title-large-line-height);
  --text-md-title-large-emphasized--letter-spacing: var(--md-sys-typescale-title-large-emphasized-tracking);
  --text-md-title-large-emphasized--font-weight: var(--md-sys-typescale-title-large-emphasized-weight);

  --text-md-title-medium: var(--md-sys-typescale-title-medium-size);
  --text-md-title-medium--line-height: var(--md-sys-typescale-title-medium-line-height);
  --text-md-title-medium--letter-spacing: var(--md-sys-typescale-title-medium-tracking);
  --text-md-title-medium--font-weight: var(--md-sys-typescale-title-medium-weight);
  --text-md-title-medium-emphasized: var(--md-sys-typescale-title-medium-size);
  --text-md-title-medium-emphasized--line-height: var(--md-sys-typescale-title-medium-line-height);
  --text-md-title-medium-emphasized--letter-spacing: var(--md-sys-typescale-title-medium-emphasized-tracking);
  --text-md-title-medium-emphasized--font-weight: var(--md-sys-typescale-title-medium-emphasized-weight);

  --text-md-title-small: var(--md-sys-typescale-title-small-size);
  --text-md-title-small--line-height: var(--md-sys-typescale-title-small-line-height);
  --text-md-title-small--letter-spacing: var(--md-sys-typescale-title-small-tracking);
  --text-md-title-small--font-weight: var(--md-sys-typescale-title-small-weight);
  --text-md-title-small-emphasized: var(--md-sys-typescale-title-small-size);
  --text-md-title-small-emphasized--line-height: var(--md-sys-typescale-title-small-line-height);
  --text-md-title-small-emphasized--letter-spacing: var(--md-sys-typescale-title-small-emphasized-tracking);
  --text-md-title-small-emphasized--font-weight: var(--md-sys-typescale-title-small-emphasized-weight);

  --text-md-body-large: var(--md-sys-typescale-body-large-size);
  --text-md-body-large--line-height: var(--md-sys-typescale-body-large-line-height);
  --text-md-body-large--letter-spacing: var(--md-sys-typescale-body-large-tracking);
  --text-md-body-large--font-weight: var(--md-sys-typescale-body-large-weight);
  --text-md-body-large-emphasized: var(--md-sys-typescale-body-large-size);
  --text-md-body-large-emphasized--line-height: var(--md-sys-typescale-body-large-line-height);
  --text-md-body-large-emphasized--letter-spacing: var(--md-sys-typescale-body-large-emphasized-tracking);
  --text-md-body-large-emphasized--font-weight: var(--md-sys-typescale-body-large-emphasized-weight);

  --text-md-body-medium: var(--md-sys-typescale-body-medium-size);
  --text-md-body-medium--line-height: var(--md-sys-typescale-body-medium-line-height);
  --text-md-body-medium--letter-spacing: var(--md-sys-typescale-body-medium-tracking);
  --text-md-body-medium--font-weight: var(--md-sys-typescale-body-medium-weight);
  --text-md-body-medium-emphasized: var(--md-sys-typescale-body-medium-size);
  --text-md-body-medium-emphasized--line-height: var(--md-sys-typescale-body-medium-line-height);
  --text-md-body-medium-emphasized--letter-spacing: var(--md-sys-typescale-body-medium-emphasized-tracking);
  --text-md-body-medium-emphasized--font-weight: var(--md-sys-typescale-body-medium-emphasized-weight);

  --text-md-body-small: var(--md-sys-typescale-body-small-size);
  --text-md-body-small--line-height: var(--md-sys-typescale-body-small-line-height);
  --text-md-body-small--letter-spacing: var(--md-sys-typescale-body-small-tracking);
  --text-md-body-small--font-weight: var(--md-sys-typescale-body-small-weight);
  --text-md-body-small-emphasized: var(--md-sys-typescale-body-small-size);
  --text-md-body-small-emphasized--line-height: var(--md-sys-typescale-body-small-line-height);
  --text-md-body-small-emphasized--letter-spacing: var(--md-sys-typescale-body-small-emphasized-tracking);
  --text-md-body-small-emphasized--font-weight: var(--md-sys-typescale-body-small-emphasized-weight);

  --text-md-label-large: var(--md-sys-typescale-label-large-size);
  --text-md-label-large--line-height: var(--md-sys-typescale-label-large-line-height);
  --text-md-label-large--letter-spacing: var(--md-sys-typescale-label-large-tracking);
  --text-md-label-large--font-weight: var(--md-sys-typescale-label-large-weight);
  --text-md-label-large-emphasized: var(--md-sys-typescale-label-large-size);
  --text-md-label-large-emphasized--line-height: var(--md-sys-typescale-label-large-line-height);
  --text-md-label-large-emphasized--letter-spacing: var(--md-sys-typescale-label-large-emphasized-tracking);
  --text-md-label-large-emphasized--font-weight: var(--md-sys-typescale-label-large-emphasized-weight);

  --text-md-label-medium: var(--md-sys-typescale-label-medium-size);
  --text-md-label-medium--line-height: var(--md-sys-typescale-label-medium-line-height);
  --text-md-label-medium--letter-spacing: var(--md-sys-typescale-label-medium-tracking);
  --text-md-label-medium--font-weight: var(--md-sys-typescale-label-medium-weight);
  --text-md-label-medium-emphasized: var(--md-sys-typescale-label-medium-size);
  --text-md-label-medium-emphasized--line-height: var(--md-sys-typescale-label-medium-line-height);
  --text-md-label-medium-emphasized--letter-spacing: var(--md-sys-typescale-label-medium-emphasized-tracking);
  --text-md-label-medium-emphasized--font-weight: var(--md-sys-typescale-label-medium-emphasized-weight);

  --text-md-label-small: var(--md-sys-typescale-label-small-size);
  --text-md-label-small--line-height: var(--md-sys-typescale-label-small-line-height);
  --text-md-label-small--letter-spacing: var(--md-sys-typescale-label-small-tracking);
  --text-md-label-small--font-weight: var(--md-sys-typescale-label-small-weight);
  --text-md-label-small-emphasized: var(--md-sys-typescale-label-small-size);
  --text-md-label-small-emphasized--line-height: var(--md-sys-typescale-label-small-line-height);
  --text-md-label-small-emphasized--letter-spacing: var(--md-sys-typescale-label-small-emphasized-tracking);
  --text-md-label-small-emphasized--font-weight: var(--md-sys-typescale-label-small-emphasized-weight);

  /* --- Motion easings (spring linear() + Web cubic-bezier fallback) -------- */
  --ease-md-fast-spatial: var(--md-sys-motion-fast-spatial-easing);
  --ease-md-default-spatial: var(--md-sys-motion-default-spatial-easing);
  --ease-md-slow-spatial: var(--md-sys-motion-slow-spatial-easing);
  --ease-md-fast-effects: var(--md-sys-motion-fast-effects-easing);
  --ease-md-default-effects: var(--md-sys-motion-default-effects-easing);
  --ease-md-slow-effects: var(--md-sys-motion-slow-effects-easing);

  --ease-md-fast-spatial-bezier: var(--md-sys-motion-fast-spatial-bezier-easing);
  --ease-md-default-spatial-bezier: var(--md-sys-motion-default-spatial-bezier-easing);
  --ease-md-slow-spatial-bezier: var(--md-sys-motion-slow-spatial-bezier-easing);
  --ease-md-fast-effects-bezier: var(--md-sys-motion-fast-effects-bezier-easing);
  --ease-md-default-effects-bezier: var(--md-sys-motion-default-effects-bezier-easing);
  --ease-md-slow-effects-bezier: var(--md-sys-motion-slow-effects-bezier-easing);

  /* --- 5 Adaptive window size breakpoints (static lengths for @media) ------ */
  --breakpoint-md-compact: 0px;
  --breakpoint-md-medium: 600px;
  --breakpoint-md-expanded: 840px;
  --breakpoint-md-large: 1200px;
  --breakpoint-md-xlarge: 1600px;
}

@utility duration-md-fast-spatial {
  transition-duration: var(--md-sys-motion-fast-spatial-duration);
}
@utility duration-md-default-spatial {
  transition-duration: var(--md-sys-motion-default-spatial-duration);
}
@utility duration-md-slow-spatial {
  transition-duration: var(--md-sys-motion-slow-spatial-duration);
}
@utility duration-md-fast-effects {
  transition-duration: var(--md-sys-motion-fast-effects-duration);
}
@utility duration-md-default-effects {
  transition-duration: var(--md-sys-motion-default-effects-duration);
}
@utility duration-md-slow-effects {
  transition-duration: var(--md-sys-motion-slow-effects-duration);
}
@utility duration-md-fast-spatial-bezier {
  transition-duration: var(--md-sys-motion-fast-spatial-bezier-duration);
}
@utility duration-md-default-spatial-bezier {
  transition-duration: var(--md-sys-motion-default-spatial-bezier-duration);
}
@utility duration-md-slow-spatial-bezier {
  transition-duration: var(--md-sys-motion-slow-spatial-bezier-duration);
}
@utility duration-md-fast-effects-bezier {
  transition-duration: var(--md-sys-motion-fast-effects-bezier-duration);
}
@utility duration-md-default-effects-bezier {
  transition-duration: var(--md-sys-motion-default-effects-bezier-duration);
}
@utility duration-md-slow-effects-bezier {
  transition-duration: var(--md-sys-motion-slow-effects-bezier-duration);
}
```

---

## 2. Tailwind CSS v3 Configuration (`tailwind.config.js`)

In Tailwind v3, copy or extend `assets/tailwind/tailwind.config.js` (synced 1:1 with all 47 colours, 26 spacing/layout/density tokens, `maxWidth.md-measure`, 10 corners, 6 shadows, 2 font families, 30 type scales, 12 motion duration/timing curves, and 5 breakpoints):

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
        'md-primary-fixed': 'var(--md-sys-color-primary-fixed)',
        'md-primary-fixed-dim': 'var(--md-sys-color-primary-fixed-dim)',
        'md-on-primary-fixed': 'var(--md-sys-color-on-primary-fixed)',
        'md-on-primary-fixed-variant': 'var(--md-sys-color-on-primary-fixed-variant)',
        'md-secondary': 'var(--md-sys-color-secondary)',
        'md-on-secondary': 'var(--md-sys-color-on-secondary)',
        'md-secondary-container': 'var(--md-sys-color-secondary-container)',
        'md-on-secondary-container': 'var(--md-sys-color-on-secondary-container)',
        'md-secondary-fixed': 'var(--md-sys-color-secondary-fixed)',
        'md-secondary-fixed-dim': 'var(--md-sys-color-secondary-fixed-dim)',
        'md-on-secondary-fixed': 'var(--md-sys-color-on-secondary-fixed)',
        'md-on-secondary-fixed-variant': 'var(--md-sys-color-on-secondary-fixed-variant)',
        'md-tertiary': 'var(--md-sys-color-tertiary)',
        'md-on-tertiary': 'var(--md-sys-color-on-tertiary)',
        'md-tertiary-container': 'var(--md-sys-color-tertiary-container)',
        'md-on-tertiary-container': 'var(--md-sys-color-on-tertiary-container)',
        'md-tertiary-fixed': 'var(--md-sys-color-tertiary-fixed)',
        'md-tertiary-fixed-dim': 'var(--md-sys-color-tertiary-fixed-dim)',
        'md-on-tertiary-fixed': 'var(--md-sys-color-on-tertiary-fixed)',
        'md-on-tertiary-fixed-variant': 'var(--md-sys-color-on-tertiary-fixed-variant)',
        'md-error': 'var(--md-sys-color-error)',
        'md-on-error': 'var(--md-sys-color-on-error)',
        'md-error-container': 'var(--md-sys-color-error-container)',
        'md-on-error-container': 'var(--md-sys-color-on-error-container)',
        'md-surface': 'var(--md-sys-color-surface)',
        'md-on-surface': 'var(--md-sys-color-on-surface)',
        'md-surface-variant': 'var(--md-sys-color-surface-variant)',
        'md-on-surface-variant': 'var(--md-sys-color-on-surface-variant)',
        'md-surface-container-lowest': 'var(--md-sys-color-surface-container-lowest)',
        'md-surface-container-low': 'var(--md-sys-color-surface-container-low)',
        'md-surface-container': 'var(--md-sys-color-surface-container)',
        'md-surface-container-high': 'var(--md-sys-color-surface-container-high)',
        'md-surface-container-highest': 'var(--md-sys-color-surface-container-highest)',
        'md-surface-dim': 'var(--md-sys-color-surface-dim)',
        'md-surface-bright': 'var(--md-sys-color-surface-bright)',
        'md-outline': 'var(--md-sys-color-outline)',
        'md-outline-variant': 'var(--md-sys-color-outline-variant)',
        'md-inverse-surface': 'var(--md-sys-color-inverse-surface)',
        'md-inverse-on-surface': 'var(--md-sys-color-inverse-on-surface)',
        'md-inverse-primary': 'var(--md-sys-color-inverse-primary)',
        'md-scrim': 'var(--md-sys-color-scrim)',
        'md-shadow': 'var(--md-sys-color-shadow)',
        'md-surface-tint': 'var(--md-sys-color-surface-tint)',
      },
      spacing: {
        'md-1': 'var(--md-sys-spacing-1)',
        'md-2': 'var(--md-sys-spacing-2)',
        'md-3': 'var(--md-sys-spacing-3)',
        'md-4': 'var(--md-sys-spacing-4)',
        'md-5': 'var(--md-sys-spacing-5)',
        'md-6': 'var(--md-sys-spacing-6)',
        'md-8': 'var(--md-sys-spacing-8)',
        'md-10': 'var(--md-sys-spacing-10)',
        'md-12': 'var(--md-sys-spacing-12)',
        'md-16': 'var(--md-sys-spacing-16)',
        'md-20': 'var(--md-sys-spacing-20)',
        'md-touch': 'var(--md-sys-touch-target-min)',
        'md-margin-compact': 'var(--md-sys-layout-margin-compact)',
        'md-margin-medium': 'var(--md-sys-layout-margin-medium)',
        'md-margin-expanded': 'var(--md-sys-layout-margin-expanded)',
        'md-margin-large': 'var(--md-sys-layout-margin-large)',
        'md-margin-extra-large': 'var(--md-sys-layout-margin-extra-large)',
        'md-gutter-compact': 'var(--md-sys-layout-gutter-compact)',
        'md-gutter-medium': 'var(--md-sys-layout-gutter-medium)',
        'md-gutter-expanded': 'var(--md-sys-layout-gutter-expanded)',
        'md-gutter-large': 'var(--md-sys-layout-gutter-large)',
        'md-gutter-extra-large': 'var(--md-sys-layout-gutter-extra-large)',
        'md-pane-gap': 'var(--md-sys-layout-pane-gap)',
        'md-nav-rail-collapsed': 'var(--md-sys-nav-rail-width-collapsed)',
        'md-nav-rail-expanded': 'var(--md-sys-nav-rail-width-expanded)',
        'md-density-offset': 'var(--md-sys-density-offset)',
      },
      maxWidth: {
        'md-measure': 'var(--md-sys-layout-measure-max)',
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
        'md-level0': 'var(--md-sys-elevation-level0)',
        'md-level1': 'var(--md-sys-elevation-level1)',
        'md-level2': 'var(--md-sys-elevation-level2)',
        'md-level3': 'var(--md-sys-elevation-level3)',
        'md-level4': 'var(--md-sys-elevation-level4)',
        'md-level5': 'var(--md-sys-elevation-level5)',
      },
      fontFamily: {
        'md-brand': 'var(--md-sys-typescale-brand-font)',
        'md-plain': 'var(--md-sys-typescale-plain-font)',
      },
      fontSize: {
        'md-display-large': ['var(--md-sys-typescale-display-large-size)', {
          lineHeight: 'var(--md-sys-typescale-display-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-large-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-large-weight)',
        }],
        'md-display-large-emphasized': ['var(--md-sys-typescale-display-large-size)', {
          lineHeight: 'var(--md-sys-typescale-display-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-large-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-large-emphasized-weight)',
        }],
        'md-display-medium': ['var(--md-sys-typescale-display-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-display-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-medium-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-medium-weight)',
        }],
        'md-display-medium-emphasized': ['var(--md-sys-typescale-display-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-display-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-medium-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-medium-emphasized-weight)',
        }],
        'md-display-small': ['var(--md-sys-typescale-display-small-size)', {
          lineHeight: 'var(--md-sys-typescale-display-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-small-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-small-weight)',
        }],
        'md-display-small-emphasized': ['var(--md-sys-typescale-display-small-size)', {
          lineHeight: 'var(--md-sys-typescale-display-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-display-small-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-display-small-emphasized-weight)',
        }],
        'md-headline-large': ['var(--md-sys-typescale-headline-large-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-large-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-large-weight)',
        }],
        'md-headline-large-emphasized': ['var(--md-sys-typescale-headline-large-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-large-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-large-emphasized-weight)',
        }],
        'md-headline-medium': ['var(--md-sys-typescale-headline-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-medium-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-medium-weight)',
        }],
        'md-headline-medium-emphasized': ['var(--md-sys-typescale-headline-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-medium-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-medium-emphasized-weight)',
        }],
        'md-headline-small': ['var(--md-sys-typescale-headline-small-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-small-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-small-weight)',
        }],
        'md-headline-small-emphasized': ['var(--md-sys-typescale-headline-small-size)', {
          lineHeight: 'var(--md-sys-typescale-headline-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-headline-small-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-headline-small-emphasized-weight)',
        }],
        'md-title-large': ['var(--md-sys-typescale-title-large-size)', {
          lineHeight: 'var(--md-sys-typescale-title-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-large-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-large-weight)',
        }],
        'md-title-large-emphasized': ['var(--md-sys-typescale-title-large-size)', {
          lineHeight: 'var(--md-sys-typescale-title-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-large-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-large-emphasized-weight)',
        }],
        'md-title-medium': ['var(--md-sys-typescale-title-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-title-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-medium-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-medium-weight)',
        }],
        'md-title-medium-emphasized': ['var(--md-sys-typescale-title-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-title-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-medium-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-medium-emphasized-weight)',
        }],
        'md-title-small': ['var(--md-sys-typescale-title-small-size)', {
          lineHeight: 'var(--md-sys-typescale-title-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-small-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-small-weight)',
        }],
        'md-title-small-emphasized': ['var(--md-sys-typescale-title-small-size)', {
          lineHeight: 'var(--md-sys-typescale-title-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-title-small-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-title-small-emphasized-weight)',
        }],
        'md-body-large': ['var(--md-sys-typescale-body-large-size)', {
          lineHeight: 'var(--md-sys-typescale-body-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-large-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-large-weight)',
        }],
        'md-body-large-emphasized': ['var(--md-sys-typescale-body-large-size)', {
          lineHeight: 'var(--md-sys-typescale-body-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-large-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-large-emphasized-weight)',
        }],
        'md-body-medium': ['var(--md-sys-typescale-body-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-body-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-medium-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-medium-weight)',
        }],
        'md-body-medium-emphasized': ['var(--md-sys-typescale-body-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-body-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-medium-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-medium-emphasized-weight)',
        }],
        'md-body-small': ['var(--md-sys-typescale-body-small-size)', {
          lineHeight: 'var(--md-sys-typescale-body-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-small-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-small-weight)',
        }],
        'md-body-small-emphasized': ['var(--md-sys-typescale-body-small-size)', {
          lineHeight: 'var(--md-sys-typescale-body-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-body-small-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-body-small-emphasized-weight)',
        }],
        'md-label-large': ['var(--md-sys-typescale-label-large-size)', {
          lineHeight: 'var(--md-sys-typescale-label-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-large-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-large-weight)',
        }],
        'md-label-large-emphasized': ['var(--md-sys-typescale-label-large-size)', {
          lineHeight: 'var(--md-sys-typescale-label-large-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-large-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-large-emphasized-weight)',
        }],
        'md-label-medium': ['var(--md-sys-typescale-label-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-label-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-medium-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-medium-weight)',
        }],
        'md-label-medium-emphasized': ['var(--md-sys-typescale-label-medium-size)', {
          lineHeight: 'var(--md-sys-typescale-label-medium-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-medium-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-medium-emphasized-weight)',
        }],
        'md-label-small': ['var(--md-sys-typescale-label-small-size)', {
          lineHeight: 'var(--md-sys-typescale-label-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-small-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-small-weight)',
        }],
        'md-label-small-emphasized': ['var(--md-sys-typescale-label-small-size)', {
          lineHeight: 'var(--md-sys-typescale-label-small-line-height)',
          letterSpacing: 'var(--md-sys-typescale-label-small-emphasized-tracking)',
          fontWeight: 'var(--md-sys-typescale-label-small-emphasized-weight)',
        }],
      },
      transitionDuration: {
        'md-fast-spatial': 'var(--md-sys-motion-fast-spatial-duration)',
        'md-default-spatial': 'var(--md-sys-motion-default-spatial-duration)',
        'md-slow-spatial': 'var(--md-sys-motion-slow-spatial-duration)',
        'md-fast-effects': 'var(--md-sys-motion-fast-effects-duration)',
        'md-default-effects': 'var(--md-sys-motion-default-effects-duration)',
        'md-slow-effects': 'var(--md-sys-motion-slow-effects-duration)',
        'md-fast-spatial-bezier': 'var(--md-sys-motion-fast-spatial-bezier-duration)',
        'md-default-spatial-bezier': 'var(--md-sys-motion-default-spatial-bezier-duration)',
        'md-slow-spatial-bezier': 'var(--md-sys-motion-slow-spatial-bezier-duration)',
        'md-fast-effects-bezier': 'var(--md-sys-motion-fast-effects-bezier-duration)',
        'md-default-effects-bezier': 'var(--md-sys-motion-default-effects-bezier-duration)',
        'md-slow-effects-bezier': 'var(--md-sys-motion-slow-effects-bezier-duration)',
      },
      transitionTimingFunction: {
        'md-fast-spatial': 'var(--md-sys-motion-fast-spatial-easing)',
        'md-default-spatial': 'var(--md-sys-motion-default-spatial-easing)',
        'md-slow-spatial': 'var(--md-sys-motion-slow-spatial-easing)',
        'md-fast-effects': 'var(--md-sys-motion-fast-effects-easing)',
        'md-default-effects': 'var(--md-sys-motion-default-effects-easing)',
        'md-slow-effects': 'var(--md-sys-motion-slow-effects-easing)',
        'md-fast-spatial-bezier': 'var(--md-sys-motion-fast-spatial-bezier-easing)',
        'md-default-spatial-bezier': 'var(--md-sys-motion-default-spatial-bezier-easing)',
        'md-slow-spatial-bezier': 'var(--md-sys-motion-slow-spatial-bezier-easing)',
        'md-fast-effects-bezier': 'var(--md-sys-motion-fast-effects-bezier-easing)',
        'md-default-effects-bezier': 'var(--md-sys-motion-default-effects-bezier-easing)',
        'md-slow-effects-bezier': 'var(--md-sys-motion-slow-effects-bezier-easing)',
      },
      screens: {
        'md-compact': '0px',
        'md-medium': '600px',
        'md-expanded': '840px',
        'md-large': '1200px',
        'md-xlarge': '1600px',
      },
    },
  },
  plugins: [],
};
```

---

## 3. Tailwind Component Examples

### 3.1 MD3E Card (Multi-pane desktop friendly + measure cap)
```html
<div class="bg-md-surface-container-low text-md-on-surface rounded-md-md p-md-6 border border-md-outline-variant shadow-md-level1">
  <h3 class="font-md-plain text-md-title-medium mb-md-2">Card Title</h3>
  <p class="font-md-plain text-md-on-surface-variant text-md-body-medium max-w-md-measure">Supporting copy rendered with proper contrast role and capped at 68ch on wide desktop displays.</p>
</div>
```

### 3.2 Filled Button (Primary Action, 40px visual + 48px hit area + spring morph + 3px/2px focus ring)
```html
<button type="button" class="relative inline-flex items-center justify-center gap-md-2 h-10 px-md-4 before:content-[''] before:absolute before:inset-x-0 before:-inset-y-1 before:min-h-md-touch before:min-w-md-touch bg-md-primary text-md-on-primary rounded-md-lg-inc active:rounded-md-sm font-md-plain text-md-label-large-emphasized transition-[border-radius,transform] duration-md-fast-spatial ease-md-fast-spatial active:scale-[0.98] focus-visible:outline-[3px] focus-visible:outline-md-secondary focus-visible:outline-offset-2">
  <span class="material-symbols-outlined [--md-sys-icon-size:20px]" aria-hidden="true">check</span>
  Confirm
</button>
```

### 3.3 Tonal Button
```html
<button type="button" class="relative inline-flex items-center justify-center gap-md-2 h-10 px-md-4 before:content-[''] before:absolute before:inset-x-0 before:-inset-y-1 before:min-h-md-touch before:min-w-md-touch bg-md-secondary-container text-md-on-secondary-container rounded-md-lg-inc active:rounded-md-sm font-md-plain text-md-label-large transition-[border-radius,transform] duration-md-fast-spatial ease-md-fast-spatial active:scale-[0.98] focus-visible:outline-[3px] focus-visible:outline-md-secondary focus-visible:outline-offset-2">
  Cancel
</button>
```

### 3.4 Responsive 2-Pane Desktop Workspace (`md-expanded` / `md-large` / `md-xlarge`)
```html
<div class="bg-md-surface-container min-h-screen p-md-margin-compact md-medium:p-md-margin-medium md-large:p-md-margin-large">
  <div class="grid grid-cols-1 md-expanded:grid-cols-2 md-xlarge:grid-cols-3 gap-md-pane-gap">
    <section class="bg-md-surface text-md-on-surface rounded-md-xl p-md-6">Primary Pane</section>
    <section class="bg-md-surface-container-lowest text-md-on-surface rounded-md-xl p-md-6">Detail Pane</section>
  </div>
</div>
```
