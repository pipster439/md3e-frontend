# Selection components — Material 3 / M3 Expressive specs

Transcribed from the individual component spec pages on m3.material.io; retrieved 2026-09-12.
A value shown as `—` was not present in the rendered text (the spec presents it only as a diagram); the source's `--` in availability tables is written "Not available".

---

## Checkbox

Source: https://m3.material.io/components/checkbox/specs

**Variants.** No variants are defined on this page. Checkbox is a single component with one default (light) token set, opened into the state folders Enabled, Disabled, Hovered, Focused, Pressed (ripple). The page index lists only: Tokens & specs, Checkbox, Color, States, Measurements.

**Configurations** (M3 vs M3 Expressive). The rendered page has no Configurations section and no availability table, so no configuration rows can be transcribed.

**Anatomy.** As listed in the component element browser.

1. Container
2. Icon

The colour section separately names the elements **Checkbox**, **State-layer**, and **Icon**.

**Colour roles.** The page lists the elements above, but the roles themselves are rendered only as swatches; the sole role named in text is for the adjacent label. Colour values are implemented through design tokens.

| Element | Role |
|---|---|
| Checkbox | — |
| State-layer | — |
| Icon | — |
| Adjacent text label | On surface |

**States.** Enabled, Disabled, Hovered, Focused, Pressed (ripple). Stated behaviour: "Use the color role on surface for adjacent text labels. This remains the same even if interacting with the label or component." / "The text color remains the same regardless if the checkbox is selected or not."

**Shape & morph.** No morph behaviour is stated. The only shape value is the container corner shape (2dp, see Measurements).

**Measurements.**

| Attribute | Value |
|---|---|
| Container size | 18dp |
| Container corner shape | 2dp |
| Icon size | 18dp |
| Icon alignment | Center-aligned |
| Target size | 48dp |
| State-layer size | 40dp |

**Notes.**

- "Use the color role on surface for adjacent text labels. This remains the same even if interacting with the label or component."
- "The text color remains the same regardless if the checkbox is selected or not."
- No explicit do/don't or "not recommended" statements appear on this page.

---

## Chips

Source: https://m3.material.io/components/chips/specs

**Variants.** Four variants: **assist chip**, **filter chip**, **input chip**, and **suggestion chip** — each selectable in the variant browser ("Chip - Assist"). The only sub-type distinction present in the rendered text is selection: each variant documents "Selected and unselected <variant> states". No other sub-types (for example elevated chips) appear in the rendered text.

**Configurations** (M3 vs M3 Expressive). The rendered page has no Configurations section and no availability table, so no configuration rows can be transcribed. The page index lists only: Tokens & specs, Assist chip, Filter chip, Input chip, Suggestion chip.

**Anatomy.** Per variant, in the order the elements are listed in the dump.

1. **Assist chip** — Container; Label text; Leading icon
2. **Filter chip** — Container; Label text; Leading icon; Trailing icon
3. **Input chip** — Container; Label text; Trailing icon; Leading icon
4. **Suggestion chip** — Container; Label text

**Colour roles.** The page gives the role names in order per variant, but does not label which element each role applies to; element names are listed in the Anatomy section above. Roles as transcribed:

*Assist chip* — "Assist chip color roles used for light and dark themes". Elements listed: Container, Label text, Leading icon.

| Element | Role |
|---|---|
| — | Surface container low (optional) |
| — | On surface |
| — | Outline |
| — | Primary |

*Filter chip* — "Filter chip color roles used for light and dark themes". Elements listed: Container, Label text, Leading icon, Trailing icon. Selected and unselected states are documented (see States).

| Element | Role |
|---|---|
| — | On surface variant |
| — | On secondary container |
| — | Secondary container |
| — | Outline variant |
| — | Surface container low (optional) |

*Input chip* — "Input chip color roles used for light and dark themes". Elements listed: Container, Label text, Trailing icon, Leading icon. Selected and unselected states are documented (see States).

| Element | Role |
|---|---|
| — | On surface variant |
| — | Surface container low (optional) |
| — | On surface variant |
| — | On surface variant |
| — | Outline variant |
| — | Primary |
| — | Secondary container |
| — | On secondary container |
| — | On secondary container |

*Suggestion chip* — "Suggestion chip color roles used for light and dark themes". Elements listed: Container, Label text. Selected and unselected states are documented (see States).

| Element | Role |
|---|---|
| — | Outline |
| — | Surface container low (optional) |
| — | On surface variant |

**States.** Every variant is documented as "Selected and unselected <variant> states:" followed by the same six states.

| Variant | States |
|---|---|
| Assist chip | Enabled, Disabled, Hovered, Focused, Pressed, Dragged |
| Filter chip | Enabled, Disabled, Hovered, Focused, Pressed, Dragged |
| Input chip | Enabled, Disabled, Hovered, Focused, Pressed, Dragged |
| Suggestion chip | Enabled, Disabled, Hovered, Focused, Pressed, Dragged |

No additional behaviour text is given for the states beyond the interaction-states link.

**Shape & morph.** All four variants state a container shape of **8dp corner radius** in their measurement tables. The rendered text contains **no** shape-morphing behaviour for filter or input chips and **no** morph corner values — the Expressive shape-shift is not described on this page, so it is recorded as `—`.

**Measurements.** The page section is "Select a component variant below to see its elements, attributes, tokens, and values." Measurements are grouped by variant; every group and row is reproduced below.

*Assist chip* — "Assist chip padding and size measurements"

| Attribute | Value |
|---|---|
| Height | 32dp |
| Shape | 8dp corner radius |
| Icon size | 18dp |
| Vertical label text alignment | Center-aligned |
| Horizontal label text alignment | Start-aligned |
| Left/right padding | 16dp |
| Left/right padding with icon | 8dp |
| Padding between elements | 8dp |

*Filter chip* — "Filter chip padding and size measurements"

| Attribute | Value |
|---|---|
| Container height | 32dp |
| Container shape | 8dp corner radius |
| Icon size | 18dp |
| Vertical label text alignment | Center-aligned |
| Horizontal label text alignment | Start-aligned |
| Left/right padding | 16dp |
| Left/right padding with icon | 8dp |
| Padding between elements | 8dp |

*Input chip* — "Input chip padding and size measurements"

| Attribute | Value |
|---|---|
| Container height | 32dp |
| Container shape | 8dp corner radius |
| Icon size | 18dp |
| Avatar shape | 12dp corner radius |
| Avatar size | 24dp |
| Vertical label text alignment | Center-aligned |
| Horizontal label text alignment | Start-aligned |
| Left padding for avatar | 4dp |
| Right padding for avatar | 8dp |
| Left/right padding for icon | 8dp |
| Padding between elements | 8dp |
| Target size for close icon | Min 48dp |

*Suggestion chip* — "Suggestion chip padding and size measurements"

| Attribute | Value |
|---|---|
| Container height | 32dp |
| Container shape | 8dp corner radius |
| Icon size | 18dp |
| Vertical label text alignment | Center-aligned |
| Horizontal label text alignment | Start-aligned |
| Left/right padding without icon | 16dp |
| Left/right padding with icon | 8dp |
| Padding between elements | 8dp |

**Notes.**

- No explicit do/don't, caution, or "not recommended" statements appear on this page.
- The optional role appears verbatim as "Surface container low (optional)" in the assist, filter, input, and suggestion role lists.
- Container height is stated as 32dp for filter, input, and suggestion chips, and as "Height" 32dp for assist chips. All four use an 8dp corner radius.

---

## Radio button

Source: https://m3.material.io/components/radio-button/specs

**Variants.** No variants are defined on this page. Radio button is a single component with one default (light) token set, opened into the state folders Enabled, Disabled, Hovered, Focused, Pressed (ripple). The page index lists: Tokens & specs, Color, States, Measurements (plus the item "Radio button icon").

**Configurations** (M3 vs M3 Expressive). The rendered page has no Configurations section and no availability table, so no configuration rows can be transcribed.

**Anatomy.** No element list is given in the rendered text. The page index names the item "Radio button icon".

**Colour roles.** "Radio button color roles used for light and dark themes:" — the roles below are listed in the dump without a stated element mapping. Colour values are implemented through design tokens.

| Element | Role |
|---|---|
| — | Primary |
| — | On surface variant |
| Adjacent text label | On surface |

**States.** Enabled, Hover, Focus, Pressed, Disabled. Stated behaviour: "Use the color role on surface for adjacent text labels. This remains the same even if interacting with the label or component." / "The text color remains the same regardless if the button is selected or not." The page also notes "State specs are in the token module above".

**Shape & morph.** No shape or morph section and no corner values in the dump.

**Measurements.** "Radio button size measurements". A single Attribute | Value table is given in the dump.

| Attribute | Value |
|---|---|
| Icon size | 20dp |
| State layer size | 40dp |
| Target size | 48dp |

**Notes.**

- "Use the color role on surface for adjacent text labels. This remains the same even if interacting with the label or component."
- "The text color remains the same regardless if the button is selected or not."
- No explicit do/don't or "not recommended" statements appear on this page.

---

## Select

Source: Composed from official Material 3 **Text fields** (`56dp` Exposed Dropdown Menu trigger) + **Menus** (`Vertical menus` `16dp` / `Baseline menu` `4dp`, `48dp` option rows; `m3.material.io` does not publish a separate standalone Select spec page).

### 1. Geometry, Tonal & Motion Tokens

| Part | Geometry / Measurement | Tonal & Motion Tokens |
|---|---|---|
| **Trigger (Outlined / Filled)** | Height `56dp` (`calc(56px + var(--md-sys-density-offset, 0px))`, `min-block-size: 48px`); `4dp` (`corner-extra-small`) Outlined / `4px 4px 0 0` Filled; `16dp` pad (`12dp` with leading icon) | Outlined: `outline` (`1px`) -> `primary` (`2px` open/focus); Filled: `surface-container-highest` + `on-surface-variant` -> `primary` active indicator; Value `on-surface`; Caret icon rotates `180deg` on `--md-sys-motion-fast-spatial` |
| **Listbox Popup** | `min-inline-size` matched to trigger (`112–280dp+`); `2dp` vertical pad & `2dp` item gap; corner `16dp` (`corner-large`) Expressive or `4dp` (`corner-extra-small`) baseline | `surface-container-low`, `box-shadow: var(--md-sys-elevation-level2)`, `overscroll-behavior: contain` (`opacity` `--md-sys-motion-fast-effects` + `transform` `--md-sys-motion-fast-spatial`) |
| **Option Item (`role="option"`)** | Height `48dp` (`--md-sys-touch-target-min`), padding `12dp`–`16dp`, inner pill radius `12dp` (`corner-medium`) | Unselected: `on-surface`; Highlighted (`[data-highlighted]`): `8%` `on-surface` `in oklab`; Selected (`[data-selected]`): `secondary-container` / `on-secondary-container` (or Expressive `tertiary-container` / `on-tertiary-container`) + emphasized weight + trailing `check` icon (**never color-only**); Disabled (`[data-disabled]`): `38%` content opacity |

### 2. Visual Skin Contract + Headless Primitive Bridge

Complex composite Select dropdowns require demanding ARIA (`role="combobox"`, `role="listbox"`, `aria-activedescendant` or roving focus, portal stacking, typeahead, `Escape` & outside-dismiss). **This design system defines a single shared MD3E Visual Skin Contract driven purely by standard semantic `data-*` attributes**, so React/Vue/Svelte apps can drop in **Radix Select**, **Base UI Select**, or **Ark UI Select** — and vanilla HTML apps can use `[popover="auto"]` — with zero style conflict:

| Unified State Attribute | Semantics & Cross-Library Mapping |
|---|---|
| `[data-state="open\|closed"]` | Trigger & listbox visibility (`Radix` & `Ark` native; `Base UI` emits `[data-open]` / `[data-closed]`; vanilla toggles `data-state="open"` on `:popover-open`) |
| `[data-highlighted]` | Active keyboard or pointer hover option (`Radix`, `Base UI`, `Ark UI`, and vanilla all use `[data-highlighted]`) |
| `[data-selected]` | Committed selected option (`Base UI`, `Ark UI`, vanilla `[data-selected="true"]`; `Radix` emits `[data-state="checked"]`) |
| `[data-disabled]` | Non-selectable option or trigger (`Radix`, `Base UI`, `Ark UI`, and vanilla) |

```css
/* Shared MD3E Select Visual Skin Contract (Vanilla Popover + Radix / Base UI / Ark UI) */
.md3e-select-trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--md-sys-spacing-2);
  min-inline-size: 200px;
  min-block-size: var(--md-sys-touch-target-min);
  block-size: calc(56px + var(--md-sys-density-offset, 0px));
  padding-inline: var(--md-sys-spacing-4);
  border: 1px solid var(--md-sys-color-outline);
  border-radius: var(--md-sys-shape-corner-extra-small);
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  cursor: pointer;
  transition: border-color var(--md-sys-motion-fast-effects),
              background-color var(--md-sys-motion-fast-effects);
}

.md3e-select-trigger:is([data-state="open"], [data-popup-open], [aria-expanded="true"]) {
  border-color: var(--md-sys-color-primary);
  border-width: 2px;
}

.md3e-select-trigger__chevron {
  color: var(--md-sys-color-on-surface-variant);
  transition: transform var(--md-sys-motion-fast-spatial);
}

.md3e-select-trigger:is([data-state="open"], [data-popup-open], [aria-expanded="true"]) .md3e-select-trigger__chevron {
  transform: rotate(180deg);
}

.md3e-select-trigger:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-select-content {
  margin: 0;
  padding: 2px 0;
  border: none;
  border-radius: var(--md-sys-shape-corner-large); /* 16dp Expressive vertical menu */
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  box-shadow: var(--md-sys-elevation-level2);
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-block-size: 320px;
  overflow-y: auto;
  overscroll-behavior: contain;
  transform-origin: top center;
}

.md3e-select-content[popover] {
  display: none;
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

.md3e-select-content[popover]:popover-open {
  display: flex;
  opacity: 1;
  transform: translateY(0) scale(1);
}

@media (prefers-reduced-motion: no-preference) {
  .md3e-select-content[popover] {
    transition:
      opacity var(--md-sys-motion-fast-effects),
      transform var(--md-sys-motion-fast-spatial),
      display var(--md-sys-motion-fast-effects-duration),
      overlay var(--md-sys-motion-fast-effects-duration);
    transition-behavior: allow-discrete;
  }

  @starting-style {
    .md3e-select-content[popover]:popover-open {
      opacity: 0;
      transform: translateY(-6px) scale(0.97);
    }
  }
}

.md3e-select-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--md-sys-spacing-3);
  inline-size: 100%;
  min-block-size: var(--md-sys-touch-target-min); /* 48dp option height */
  padding-inline: var(--md-sys-spacing-4);
  border: none;
  border-radius: var(--md-sys-shape-corner-medium);
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  text-align: start;
  cursor: pointer;
  outline: 2px solid transparent;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-select-item:is([data-highlighted], :hover) {
  background: color-mix(in oklab, var(--md-sys-color-on-surface) 8%, transparent);
}

.md3e-select-item:is([data-selected="true"], [data-selected], [data-state="checked"]) {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
}

.md3e-select-item__check {
  opacity: 0;
  color: inherit;
}

.md3e-select-item:is([data-selected="true"], [data-selected], [data-state="checked"]) .md3e-select-item__check {
  opacity: 1;
}

.md3e-select-item:is([data-disabled="true"], [data-disabled]) {
  opacity: var(--md-sys-state-disabled-content-opacity);
  pointer-events: none;
  cursor: default;
}

.md3e-select-item:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

@media (prefers-reduced-motion: reduce) {
  .md3e-select-trigger,
  .md3e-select-trigger__chevron,
  .md3e-select-content[popover],
  .md3e-select-item {
    transition: none;
  }
}

@media (forced-colors: active) {
  .md3e-select-trigger,
  .md3e-select-content {
    border: 1px solid CanvasText;
  }
  .md3e-select-item:is([data-selected="true"], [data-selected], [data-state="checked"]) {
    background: Highlight;
    color: HighlightText;
  }
}
```

### 3. Concrete Zero-Conflict Headless Primitive Recipes

1. **Radix Select (`@radix-ui/react-select`)**:
   - Use `position="popper"` and `sideOffset={4}` on `Select.Content`, sizing width with `min-width: var(--radix-select-trigger-width);`.
   - Radix natively emits `[data-state="open|closed"]`, `[data-highlighted]`, `[data-state="checked"]`, and `[data-disabled]`.
2. **Base UI Select (`@base-ui-components/react/select`)**:
   - Size `Select.Popup` with `min-width: var(--anchor-width);`.
   - Base UI natively emits `[data-open]` / `[data-closed]` / `[data-popup-open]`, `[data-highlighted]`, `[data-selected]`, and `[data-disabled]`.
3. **Ark UI Select (`@ark-ui/react/select`)**:
   - Size `Select.Content` with `min-width: var(--reference-width);`.
   - Ark UI natively emits `[data-state="open|closed"]`, `[data-highlighted]`, `[data-selected]`, and `[data-disabled]`.

```tsx
// 1. Radix Select bound directly to the MD3E Visual Skin Contract
<Select.Root defaultValue="expressive">
  <Select.Trigger className="md3e-select-trigger" aria-label="Motion scheme">
    <Select.Value />
    <Select.Icon className="material-symbols-outlined md3e-select-trigger__chevron" aria-hidden="true">
      arrow_drop_down
    </Select.Icon>
  </Select.Trigger>
  <Select.Portal>
    <Select.Content className="md3e-select-content" position="popper" sideOffset={4} style={{ minWidth: 'var(--radix-select-trigger-width)' }}>
      <Select.Viewport>
        <Select.Item className="md3e-select-item" value="expressive">
          <Select.ItemText>Expressive</Select.ItemText>
          <Select.ItemIndicator className="material-symbols-outlined md3e-select-item__check" aria-hidden="true">check</Select.ItemIndicator>
        </Select.Item>
        <Select.Item className="md3e-select-item" value="standard">
          <Select.ItemText>Standard</Select.ItemText>
          <Select.ItemIndicator className="material-symbols-outlined md3e-select-item__check" aria-hidden="true">check</Select.ItemIndicator>
        </Select.Item>
      </Select.Viewport>
    </Select.Content>
  </Select.Portal>
</Select.Root>
```

```tsx
// 2. Base UI Select & 3. Ark UI Select (identical .md3e-select-* skin classes)
// Base UI: <Select.Popup className="md3e-select-content" style={{ minWidth: 'var(--anchor-width)' }}>
//          <Select.Item className="md3e-select-item" value="expressive"> ... </Select.Item>
// Ark UI:  <Select.Content className="md3e-select-content" style={{ minWidth: 'var(--reference-width)' }}>
//          <Select.Item className="md3e-select-item" item={item}> ... </Select.Item>
```

#### Vanilla Top-Layer Keyboard Contract (`role="combobox"` + `role="listbox"` `[popover="auto"]`)

- `Enter` / `Space` / `ArrowDown` / `ArrowUp` on the trigger opens the `[popover="auto"]` listbox and focuses/highlights the active or first enabled option.
- `ArrowDown` / `ArrowUp` / `Home` / `End` moves `[data-highlighted="true"]` while skipping `[data-disabled="true"]`.
- `Enter` / `Space` commits `[data-selected="true"]` + `aria-selected="true"`, updates trigger text, closes the popover, and restores focus to the trigger.
- `Escape` or outside click dismisses cleanly (`[popover="auto"]` light dismiss) and restores focus; printable keystrokes trigger **first-letter typeahead** jump.

### 4. Progressive Enhancement: CSS Customizable Select (`appearance: base-select`)

Where browsers support CSS Customizable `<select>` (`@supports (appearance: base-select)`), you can progressively style native `<select>` + `<option>` directly with MD3E tokens without JavaScript:

- Opt both `<select>` and `::picker(select)` into `appearance: base-select;`, and explicitly set `display: flex; align-items: center; justify-content: space-between; padding-block: 0;` on `select.md3e-native-select` (and `display: flex; align-items: center;` on `option`) so Chromium's UA stylesheet (`align-items: normal; padding-block: 3.5px;`) does not pin label text near the top edge.
- Enable smooth auto-height sizing on `::picker(select)` with `interpolate-size: allow-keywords;` and separate `transition-behavior: allow-discrete;` **after** `transition:` (including `display` and `overlay`) paired with `@starting-style`.
- **CRITICAL**: **NEVER set `overflow: hidden;` on `::picker(select)`** — it clips inner `:focus-visible` outlines and breaks internal scrolling on long option lists (`overflow: auto; overscroll-behavior: contain;` stays safe).
- Style `::picker-icon` (`transform: rotate(180deg)` on `select:open::picker-icon` via `--md-sys-motion-fast-spatial`) and `option::checkmark` (`margin-inline-start: auto; color: var(--md-sys-color-on-secondary-container);`).

```css
@supports (appearance: base-select) {
  select.md3e-native-select,
  select.md3e-native-select::picker(select) {
    appearance: base-select;
  }

  select.md3e-native-select {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-block-size: calc(56px + var(--md-sys-density-offset, 0px));
    padding-block: 0;
    padding-inline: var(--md-sys-spacing-4) var(--md-sys-spacing-3);
    border: 1px solid var(--md-sys-color-outline);
    border-radius: var(--md-sys-shape-corner-extra-small);
    background: transparent;
    color: var(--md-sys-color-on-surface);
    cursor: pointer;
  }

  select.md3e-native-select::picker-icon {
    color: var(--md-sys-color-on-surface-variant);
    transition: transform var(--md-sys-motion-fast-spatial);
  }

  select.md3e-native-select:open::picker-icon {
    transform: rotate(180deg);
  }

  select.md3e-native-select::picker(select) {
    interpolate-size: allow-keywords;
    margin-block-start: var(--md-sys-spacing-1);
    padding: 2px 0;
    border: none;
    border-radius: var(--md-sys-shape-corner-large);
    background: var(--md-sys-color-surface-container-low);
    color: var(--md-sys-color-on-surface);
    box-shadow: var(--md-sys-elevation-level2);
    overflow: auto; /* NEVER overflow: hidden on ::picker(select) */
    overscroll-behavior: contain;
    opacity: 0;
    transform: translateY(-4px) scale(0.98);
  }

  select.md3e-native-select:open::picker(select) {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  @media (prefers-reduced-motion: no-preference) {
    select.md3e-native-select::picker(select) {
      transition:
        opacity var(--md-sys-motion-fast-effects),
        transform var(--md-sys-motion-fast-spatial),
        display var(--md-sys-motion-fast-effects-duration),
        overlay var(--md-sys-motion-fast-effects-duration);
      transition-behavior: allow-discrete;
    }

    @starting-style {
      select.md3e-native-select:open::picker(select) {
        opacity: 0;
        transform: translateY(-4px) scale(0.98);
      }
    }
  }

  select.md3e-native-select option {
    display: flex;
    align-items: center;
    gap: var(--md-sys-spacing-2);
    min-block-size: var(--md-sys-touch-target-min);
    padding-inline: var(--md-sys-spacing-4);
    border-radius: var(--md-sys-shape-corner-medium);
  }

  select.md3e-native-select option:checked {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
    font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
  }

  select.md3e-native-select option::checkmark {
    order: 1;
    margin-inline-start: auto;
    color: var(--md-sys-color-on-secondary-container);
  }

  @media (prefers-reduced-motion: reduce) {
    select.md3e-native-select::picker-icon,
    select.md3e-native-select::picker(select) {
      transition: none;
    }
  }
}
```

---

## Switch

Source: https://m3.material.io/components/switch/specs

**Variants.** No variants are defined on this page. Switch is a single component with one default (light) token set, opened into the state folders Enabled, Disabled, Hovered, Focused, Pressed (ripple). The page documents three configurations instead (see below).

**Configurations** (M3 vs M3 Expressive). The page has a Configurations section listing three configuration names, but no M3 / M3 Expressive availability columns and no category labels, so those cells are `—`.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | Without icons | — | — |
| — | Icon on selected switch | — | — |
| — | Icon on selected and unselected switch | — | — |

**Anatomy.** Elements listed on the page (the em dash in the source is preserved).

1. Track
2. Handle (formerly "thumb")
3. Icon

**Colour roles.** "Switch color roles used for light and dark themes:" — the roles below are listed in the dump without a stated element mapping. The adjacent label roles are stated separately. Colour values are implemented through design tokens.

| Element | Role |
|---|---|
| — | Surface container highest |
| — | Outline |
| — | Outline |
| — | Primary |
| — | On primary |
| — | On primary container |
| Adjacent text label | On surface |
| Supporting text (may use) | On surface variant |

**States.** Enabled, Hovered, Focused, Pressed, Disabled. The page notes "State specs are in the token module above".

**Shape & morph.** No morph behaviour is stated. Shape values named on the page are all `md.sys.shape.corner.full` — for the Track, the Handle, and the State layer (see Measurements).

**Measurements.** The dump gives a three-column table (Element | Attribute | Value) and four diagram labels: "Switches without icons", "Pressed switches without icons", "Switches with icons", "Pressed switches with icons".

| Element | Attribute | Value |
|---|---|---|
| Track | Height | 32dp |
| Track | Width | 52dp |
| Track | Outline width | 2dp |
| Track | Shape | md.sys.shape.corner.full |
| Handle | Height (unselected) | 16dp |
| Handle | Height - with icon | 24dp |
| Handle | Height (selected) | 24dp |
| Handle | Height (pressed) | 28dp |
| Handle | Width (unselected) | 16dp |
| Handle | Width - with icon | 24dp |
| Handle | Width (selected) | 24dp |
| Handle | Width (pressed) | 28dp |
| Handle | Shape | md.sys.shape.corner.full |
| State layer | Size | 40dp |
| State layer | Shape | md.sys.shape.corner.full |
| Target | Size | 48dp |
| Icon | Size (selected) | 16dp |
| Icon | Size (unselected) | 16dp |

**Notes.**

- "Use the color role on surface for adjacent text labels. This remains the same even if interacting with the label or component."
- "The text label uses on surface. Supporting text may use on surface variant."
- No explicit do/don't or "not recommended" statements appear on this page.

---

## Sliders

Source: https://m3.material.io/components/sliders/specs

**Variants.** Standard, Centered, and Range, plus Discrete (which appears in the variants availability table). "Available as 'continuous' slider" is how M3 names the Standard variant; M3 Expressive exposes Discrete "as 'stops' configuration".

| Variant | M3 | M3 Expressive |
|---|---|---|
| Standard | Available as "continuous" slider | Available |
| Centered | Available (web only) | Available |
| Range | Available | Available |
| Discrete | Available | Available as "stops" configuration |

**Configurations** (M3 vs M3 Expressive). Categories named on the page in prose: Orientation (horizontal, vertical); Size (XS, S, M, L, XL); Inset icon; Stops; Value indicator.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Inset icon | No (default) | Available | Available |
| Inset icon | Yes | Not available | Available |
| Orientation | Horizontal (default) | Available | Available |
| Orientation | Vertical | Not available | Available |
| Size | XS (default) | Available | Available |
| Size | S, M, L, XL | Not available | Available on Android Views (MDC-Android). Available as tokens on other platforms.* |
| Stop indicators | No (default), Yes | Available as "discrete" slider | Available |
| Value Indicator | No (default), Yes | Available | Available |

\* "Configurations only available using tokens don't have implemented presets in code. To change the size, swap the default size tokens md.comp.slider.xsmall.[...] with those of the desired size."

**Anatomy.** As listed on the page, in order.

1. Value indicator (optional)
2. Stop indicators (optional)
3. Active track
4. Handle
5. Inactive track
6. Inset icon (optional)

**Colour roles.** "Slider color roles used for light and dark schemes:" — the roles below are listed in the dump in order, without a stated element mapping. Colour values are implemented through design tokens.

| Element | Role |
|---|---|
| — | Inverse surface |
| — | Inverse on surface |
| — | Primary |
| — | On primary |
| — | Primary |
| — | Secondary container |
| — | On secondary container |
| — | On secondary container |
| — | On primary |

**States.** Enabled, Disabled, Hovered, Focused, Pressed. No further behaviour text is given. Token set: Slider — Default, Light / Enabled, Disabled, Hovered, Focused, Pressed (ripple). "Slider tokens are organized into a common token set, and token sets for each size."

**Shape & morph.** No morph behaviour is stated. Track shape is given per size: 8dp (XS), 8dp (S), 12dp (M), 16dp (L), 28dp (XL) — see Measurements.

**Measurements.** Page sections: "Padding and size measurements for common sliders" (presented only as a diagram in the rendered text, so no values) and "Padding and size measurements for XS, S, M, L, and XL sliders".

| Attribute | XS | S | M | L | XL |
|---|---|---|---|---|---|
| Track height | 16dp | 24dp | 40dp | 56dp | 96dp |
| Handle height | 44dp | 44dp | 52dp | 68dp | 108dp |
| Track shape | 8dp | 8dp | 12dp | 16dp | 28dp |
| Inset icon size | Not available | Not available | 24dp | 24dp | 32dp |

Rows that the flattened dump gives with a single value and no per-size column alignment — recorded here as stated values rather than guessed per size:

| Attribute | Value |
|---|---|
| Label container height | 44dp |
| Label container width | 48dp |
| Handle width | 4dp |

**Notes.**

- "Configurations only available using tokens don't have implemented presets in code. To change the size, swap the default size tokens md.comp.slider.xsmall.[...] with those of the desired size."
- Vertical orientation and the S/M/L/XL sizes are M3 Expressive additions; in M3 they are "Not available".
