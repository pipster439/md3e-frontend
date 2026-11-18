# Icons — Material Symbols & SVG Guidelines for MD3E

Material 3 Expressive uses **Material Symbols** (variable icon font, Outlined by default) or **inline SVGs** derived from the same `24dp` optical grid (`viewBox="0 -960 960 960"`).

---

## 1. Required `<head>` Setup (Preventing Raw Ligature Text Flash / Layout Blowup)

Always add `preconnect` links and **`&display=block`** to the Google Fonts stylesheet URL, and keep the variable axis list in **strictly alphabetical order (`FILL,GRAD,opsz,wght`)** — Google Fonts CSS2 returns HTTP 400 when axes are ordered `opsz,wght,...`. Without `&display=block`, browsers briefly render raw snake_case ligature strings (such as `notifications_active` or `format_align_center`) in the fallback system font (`FOUT`), breaking button widths and overflowing fixed containers.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block">
```

`assets/tokens/md3e-tokens.css` also enforces a defensive `1em × 1em` box with `display: inline-flex; overflow: hidden; white-space: nowrap; flex-shrink: 0;` on `.material-symbols-outlined`, `.material-symbols-rounded`, and `.material-symbols-sharp` so an unloaded or slow font never stretches parent flex layouts.

### Offline / Intranet Environments (Zero-CDN SVG Fallback)

If the target environment cannot reach `fonts.googleapis.com` (offline desktop apps, corporate intranets, air-gapped demos), **do not use ligature text spans** (`<span>search</span>`). Render inline `<svg>` icons instead, sized to `1em` and coloured via `currentColor`:

```html
<button type="button" class="md3e-btn md3e-btn--filled md3e-btn--s">
  <svg aria-hidden="true" viewBox="0 -960 960 960" width="20" height="20" fill="currentColor">
    <path d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"/>
  </svg>
  <span>Search</span>
</button>
```

---

## 2. Variable Axes & Token Integration

Material Symbols is a 4-axis variable font (`FILL`, `wght`, `GRAD`, `opsz`). Never overwrite `font-variation-settings` with a partial string like `'FILL' 1` alone—that resets `wght`, `GRAD`, and `opsz` back to defaults. Always drive axes through the MD3E tokens defined in `assets/tokens/md3e-tokens.css`:

| Token | Default | Purpose |
|---|---|---|
| `--md-sys-icon-size` | `24px` | Visual icon box (`1em × 1em`) |
| `--md-sys-icon-fill` | `0` | Outline (`0`) vs Filled (`1`) — automatically set to `1` inside `[aria-pressed="true"]`, `[aria-selected="true"]`, `[aria-current="page"]` |
| `--md-sys-icon-weight` | `400` | Stroke weight (`100`–`700`) |
| `--md-sys-icon-grade` | `0` (light) / `-25` (dark) | Optical weight compensation on dark surfaces (auto-switched in `md3e-tokens.css`) |
| `--md-sys-icon-opsz` | `24` | Optical size (`20` for XS/S buttons, `24` for M/standard, `32`/`40` for L/XL) |

### Button Icon Sizing Matrix (M3E)

| Button Size | Container Height | Icon Size (`--md-sys-icon-size`) | Optical Size (`--md-sys-icon-opsz`) |
|---|---|---|---|
| Extra Small (`xs`) | `32px` | `20px` | `20` |
| Small (`s`, default) | `40px` | `20px` (text button) / `24px` (icon button) | `20` / `24` |
| Medium (`m`) | `56px` | `24px` | `24` |
| Large (`l`) | `96px` | `32px` | `32` |
| Extra Large (`xl`) | `136px` | `40px` | `40` |

Never hardcode `font-size: 18px` on Material Symbols inside MD3E buttons (that was the pre-Expressive M3 size).

---

## 3. Hallucination Prevention Table (Icon Names)

Material Symbols uses **lowercase `snake_case` ligatures**. Never guess Lucide, Heroicons, or FontAwesome names (`kebab-case` or library aliases fail silently and render raw text).

| Wrong / Hallucinated Name (Lucide / FA / Heroicons) | Correct Material Symbols Name | Usage Context |
|---|---|---|
| `plus`, `plus-circle` | `add`, `add_circle` | Create / FAB / Add item |
| `trash`, `trash-2`, `delete-bin` | `delete`, `delete_outline` | Remove / Discard |
| `cog`, `gear`, `settings-2` | `settings` | Preferences / Settings |
| `bell`, `bell-ring` | `notifications`, `notifications_active` | Alerts / Notifications |
| `heart`, `heart-filled` | `favorite` (with `--md-sys-icon-fill: 1`) | Like / Favourite |
| `moon` | `dark_mode` | Dark theme toggle |
| `sun` | `light_mode` | Light theme toggle |
| `x`, `times`, `close-icon` | `close` | Dismiss / Clear / Close |
| `pencil`, `pen` | `edit` | Edit action / Compose FAB |
| `user`, `account` | `person`, `account_circle` | Profile / User |
| `chevron-down`, `arrow-down`, `caret-down` | `keyboard_arrow_down`, `arrow_drop_down` | Dropdown / Split button |
| `bars`, `hamburger`, `nav-menu` | `menu` | App bar drawer trigger |
| `external-link`, `arrow-up-right` | `open_in_new` | External URL |
| `magnifying-glass`, `find` | `search` | Search bar / Action |
| `arrow-left`, `back` | `arrow_back` | Back navigation |
| `arrow-right`, `forward` | `arrow_forward` | Forward navigation |
| `check-circle`, `success` | `check_circle` | Confirmation / Success |
| `exclamation-triangle`, `alert-triangle` | `warning` | Warning banner |
| `info-circle` | `info` | Informational notice |
| `home-icon`, `house` | `home` | Home destination |
| `sliders`, `adjustments` | `tune` | Filter / Controls |
| `eye` | `visibility` | Show password / content |
| `eye-off`, `eye-slash` | `visibility_off` | Hide password / content |
| `copy`, `clipboard` | `content_copy` | Copy to clipboard |
| `download-cloud` | `download`, `cloud_download` | Download action |
| `upload-cloud` | `upload`, `cloud_upload` | Upload action |
| `filter` | `filter_list`, `filter_alt` | Filter controls |
| `calendar` | `calendar_today`, `event` | Date picker / Schedule |
| `clock` | `schedule` | Time picker / Recents |
| `log-out`, `sign-out` | `logout` | Sign out action |

---

## 4. Accessibility Rules for Icons

1. **Decorative icons inside labelled buttons/links**: Add **`aria-hidden="true"`** on `<span class="material-symbols-outlined" aria-hidden="true">send</span>` (or inline `<svg aria-hidden="true">`). Otherwise screen readers read the raw ligature string (`"send Publish"`, `"dark underscore mode Dark Mode"`).
2. **Icon-only interactive controls**: Keep `aria-hidden="true"` on the icon span itself and put a human-readable **`aria-label`** on the parent `<button type="button" class="md3e-icon-btn">`, `<a href>`, or `.md3e-fab`.
3. **Standalone informative icons**: Use `role="img"` and `aria-label="..."` on the icon wrapper (never expose raw snake_case ligature text to assistive technology).
4. **Target vs glyph**: Keep the icon visual size at `24px` (or `20px` on XS/S buttons) and expand the parent interactive hit area to `>= 48×48px` via padding or `::before`—never enlarge the glyph to hit 48px.
