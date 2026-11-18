# Text input components — Text fields, Date pickers, Time pickers

Transcribed from the Material Design 3 component spec pages on m3.material.io (retrieved 2026-09-12).
Any value shown as `—` was not present in the rendered text — the spec presents it only as a diagram, so no value is asserted here.
Rows marked **[baseline-token]** are cross-referenced from Google's official Material 3 baseline design token tables (`v0_192`, retrieved 2026-09-12); they fill values the spec page shows only as diagrams. Baseline token values, not Expressive-specific updates.

---

## Text fields

Source: https://m3.material.io/components/text-fields/specs

**Variants.** Two variants are documented on the spec page: the filled text field and the outlined text field. Each has its own anatomy, colour roles, states, measurements and configurations. The dump contains no M3 Expressive–era addition, alias or new variant for text fields — no "expressive" wording appears anywhere on the page, so the M3 vs M3 Expressive columns below are `—`.

**Configurations** — M3 vs M3 Expressive availability.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Filled text field | Empty and populated filled text fields with supporting text | — | — |
| Filled text field | Empty and populated filled text fields with trailing icon | — | — |
| Filled text field | Empty and populated filled text fields with leading icon | — | — |
| Filled text field | Empty and populated filled text fields with leading and trailing icons | — | — |
| Filled text field | Prefix | — | — |
| Filled text field | Suffix | — | — |
| Filled text field | Multi-line text field | — | — |
| Outlined text field | Empty and populated outlined text fields with supporting text | — | — |
| Outlined text field | Empty and populated outlined text fields with trailing icon | — | — |
| Outlined text field | Empty and populated outlined text fields with leading icon | — | — |
| Outlined text field | Empty and populated outlined text fields with leading and trailing icons | — | — |
| Outlined text field | Prefix | — | — |
| Outlined text field | Suffix | — | — |
| Outlined text field | Multi-line text field | — | — |

The dump lists these as a bullet list under "Empty and populated filled text fields with:" / "Empty and populated outlined text fields with:", not as an availability matrix. No M3 / M3 Expressive availability statement exists in the dump, so those two columns are `—` for every row.

**Anatomy.**

Filled text field (source order):

1. Container
2. Leading icon (optional)
3. Label text in empty field
4. Label text in populated field
5. Trailing icon (optional)
6. Focused active Indicator
7. Caret
8. Input text
9. Supporting text (optional)
10. Enabled active indicator

Outlined text field (source order):

1. Enabled container outline
2. Leading icon (optional)
3. Label text in empty field
4. Label text in populated field
5. Trailing icon (optional)
6. Focused container outline
7. Caret
8. Input text
9. Supporting text (optional)

**Colour roles.**

Caveat that applies to every colour-role table in this file: the page renders colour roles as swatch diagrams. The rendered text yields the roles only as an unlabelled ordered sequence, so the element → role pairing is not stated in the source. Below, the role column is the exact source order, and the element column follows the anatomy order positionally (the two lists have equal length for both text field variants, and the pairing is corroborated by the first entries — container → Surface container highest, outlined container outline → Outline). Treat the pairing as positional, not as a labelled statement.

Filled text field — "Filled text field color roles used for light and dark schemes":

| Element | Role |
|---|---|
| Container | Surface container highest |
| Leading icon (optional) | On surface variant |
| Label text in empty field | On surface variant |
| Label text in populated field | Primary |
| Trailing icon (optional) | On surface variant |
| Focused active Indicator | Primary |
| Caret | Primary |
| Input text | On surface |
| Supporting text (optional) | On surface variant |
| Enabled active indicator | On surface |

Outlined text field — "Outlined text field color roles used for light and dark schemes":

| Element | Role |
|---|---|
| Enabled container outline | Outline |
| Leading icon (optional) | On surface variant |
| Label text in empty field | On surface variant |
| Label text in populated field | Primary |
| Trailing icon (optional) | On surface variant |
| Focused container outline | Primary |
| Caret | Primary |
| Input text | On surface |
| Supporting text (optional) | On surface variant |

Error states and disabled states: the dump contains **no** colour-role values for error or disabled. Both are presented only as state diagrams ("Filled text field error states", "Outlined text field error states") with no role list and no token values. The table below is therefore filled from Google's official M3 baseline design token tables (`v0_192`, filled + outlined text-field token sets); roles that differ between the two variants are shown separately:

| Element | Role (baseline-token) |
|---|---|
| Error — active indicator (filled) / container outline (outlined) | Error (2dp focused) |
| Error — label text | Error |
| Error — supporting text | Error |
| Error — caret | Error (focused) |
| Error — leading icon | On surface variant |
| Error — trailing icon | Filled: Error; Outlined: On surface variant |
| Error — input text | On surface |
| Error — hovered label/trailing icon | On error container |
| Disabled — container (filled) | On surface @ 4% opacity |
| Disabled — active indicator (filled) / outline (outlined) | On surface @ 38% (outlined container outline @ 12%) |
| Disabled — label text | On surface @ 38% |
| Disabled — input text | On surface @ 38% |
| Disabled — leading/trailing icon | On surface @ 38% |
| Disabled — supporting text | On surface @ 38% |

**States.**

Filled text field states: Enabled (empty), Focused (empty), Hovered (empty), Disabled (empty), Enabled (populated), Focused (populated), Hovered (populated), Disabled (populated).

Outlined text field states: Enabled (empty), Focused (empty), Hovered (empty), Disabled (empty), Enabled (populated), Focused (populated), Hovered (populated), Disabled (populated).

Filled text field error states: Enabled (empty), Focused (empty), Hovered (empty), Enabled (populated), Focused (populated), Hovered (populated). Note the error set has no disabled entries.

Outlined text field error states: Enabled (empty), Focused (empty), Hovered (empty), Enabled (populated), Focused (populated), Hovered (populated). Note the error set has no disabled entries.

Stated behaviour, verbatim from the page: "Error states are visual representations used to communicate the status of a component or interactive element. An error message can display instructions on how to fix it. Error messages are displayed below the text field as supporting text until fixed." (identical wording under both the filled and the outlined error-states headings).

The token module's state selector exposes five states per variant: Enabled, Disabled, Hovered, Focused, Error.

No hover/pressed/focus overlay opacities, elevation values or timing values are given in the dump.

**Shape & morph.** The dump contains no shape statement, no morph behaviour, and no corner-radius table for either variant. The filled field exposes only "Enabled active indicator" and "Focused active Indicator" as unnamed anatomy parts with no stated thickness or shape values; the outlined field exposes "Enabled container outline" and "Focused container outline" with no stated thickness or radii. All corner radii are therefore `—`.

| Variant | Attribute | Value |
|---|---|---|
| Filled text field | Corner radius (all corners) | — |
| Filled text field | Active indicator thickness | — |
| Outlined text field | Corner radius (all corners) | — |
| Outlined text field | Container outline thickness | — |

**Measurements.**

Filled text field — diagram groups on the page: "Padding and size measurements without icons", "Padding and size measurements with icons", "Padding and size measurements with supporting text and character count". All three groups draw on the single measurement table below.

| Attribute | Value |
|---|---|
| Default container height | 56dp |
| Label alignment (unpopulated) | Vertically centered |
| Top/bottom padding | 8dp |
| Left/right padding without icons | 16dp |
| Left/right padding with icons | 12dp |
| Icon alignment | Vertically centered |
| Padding between icons and text | 16dp |
| Supporting text and character counter top padding | 4dp |
| Padding between supporting text and character counter | 16dp |
| Target size | 56dp |

Outlined text field — diagram groups on the page: "Padding and size measurements without icons", "Padding and size measurements with icons", "Padding and size measurements with supporting text and character count". All three groups draw on the single measurement table below.

| Attribute | Value |
|---|---|
| Container height | 56dp |
| Left/right padding without icons | 16dp |
| Left/right padding with icons | 12dp |
| Padding between icons and text | 16dp |
| Icon alignment | Vertically centered |
| Supporting text and character counter top padding | 4dp |
| Padding between supporting text and character counter | 16dp |
| Label alignment | Vertically centered |
| Left/right padding populated label text | 4dp |
| Target size | 56dp |

Delta between the two variants: the filled field specifies "Default container height" (56dp) while the outlined field specifies "Container height" (56dp) — different attribute labels, same value. The filled field adds "Top/bottom padding" (8dp) and "Label alignment (unpopulated)". The outlined field adds "Left/right padding populated label text" (4dp). All other rows are identical.

**Notes.** The dump contains no explicit do/don't, caution, or "not recommended" statement for text fields. The only advisory sentences are the two error-state explanations quoted under States.

### Modern Web Architecture (Filled vs Outlined, Transparent `<fieldset><legend>` Notch & Validation)

#### 1. Structural Tokens & Variant Rules

- **Container height & density**: `56px` default (`calc(56px + var(--md-sys-density-offset, 0px))` under `data-density`, keeping `min-block-size: var(--md-sys-touch-target-min)`), `16px` horizontal padding (`12px` when leading/trailing icons are present), `16px` icon-to-text gap, `4px` supporting-row top margin, and `16px` gap between supporting text and character counter.
- **Filled variant**: `surface-container-highest` fill, top-only corners (`var(--md-sys-shape-corner-extra-small-top)` = `4px 4px 0 0`), and a `1px -> 2px` bottom active indicator (`on-surface-variant` -> `primary` on focus -> `error` when invalid).
- **Outlined variant (Transparent-Safe `<fieldset><legend>` Cutout)**:
  - **NEVER fake a floating label cutout with a solid `background` patch on `<label>`** (`MD3E029` pitfall). Solid `<label>` patches break and bleed an ugly opaque rectangle whenever the field sits over `.md3e-blur-*` frosted glass, tonal gradients, or nested `surface-container-*` cards.
  - Instead, place a decorative `<fieldset class="md3e-field__outline" aria-hidden="true"><legend class="md3e-field__notch"><span>...</span></legend></fieldset>` inside `.md3e-field--outlined` behind the `<input>`, paired with the real accessible `<label for="...">`. When empty and unfocused, `<legend>` stays collapsed (`max-width: 0.01px; padding: 0;`); when `:focus-within` or populated (`:has(input:not(:placeholder-shown))`), `<legend>` expands to wrap its hidden `<span>` with `4px` horizontal padding (`padding-inline: 4px`), cutting a **100% transparent gap** cleanly through the `1px -> 2px` outline over any glass or gradient backdrop!

#### 2. Prefix / Suffix Slots, Clear Button & Dynamic Error Linkage

- **Prefix / Suffix slots**: Use `.md3e-field__affix` (`on-surface-variant`) inline beside `<input>` inside the flex row so screen readers still read the clean input value without mangling it.
- **Clear button micro-interaction**: Reveal `<button type="button" class="md3e-field__clear" aria-label="Clear input">` with a spatial spring (`scale` + `opacity` via `--md-sys-motion-fast-spatial`) when populated; clicking clears `<input>`, dispatches `input`/`change`, and restores focus to `<input>`. Keep a `48×48px` `::before` hit area around the visual icon box.
- **Tabular character counter**: Render `<span class="md3e-field__counter" aria-live="polite">19 / 60</span>` with `font-variant-numeric: tabular-nums;` so digits never jitter horizontally while typing.
- **Helper / Error linkage (`:has(:user-invalid)` + `aria-invalid` + dynamic `aria-describedby`)**:
  - Combine `:has(:user-invalid)` and `[aria-invalid="true"]` so fields turn `--md-sys-color-error` only after user interaction or explicit submission/validation — never flashing red on initial page load.
  - Keep `#field-hint` referenced by `aria-describedby` in the valid state; when invalid (`aria-invalid="true"`), dynamically switch/update `aria-describedby` to link `#field-error` (`role="alert"` or `aria-live="polite"`) **only while invalid** so assistive tech never announces hidden error text.

```html
<!-- Transparent-safe Outlined Text Field (safe over frosted blur, gradients, and nested surfaces) -->
<div class="md3e-field md3e-field--outlined" data-field-invalid="false">
  <div class="md3e-field__control">
    <fieldset class="md3e-field__outline" aria-hidden="true">
      <legend class="md3e-field__notch"><span>Workspace URI</span></legend>
    </fieldset>

    <span class="material-symbols-outlined md3e-field__leading" aria-hidden="true">language</span>
    <span class="md3e-field__affix" id="uri-prefix">https://</span>

    <input
      id="uri-input"
      class="md3e-field__input"
      type="url"
      placeholder=" "
      maxlength="60"
      aria-invalid="false"
      aria-describedby="uri-hint"
      value="studio.md3e.dev"
    >
    <label class="md3e-field__label" for="uri-input">Workspace URI</label>

    <span class="md3e-field__affix" id="uri-suffix">.app</span>
    <button type="button" class="md3e-field__clear" id="uri-clear" aria-label="Clear workspace URI">
      <span class="material-symbols-outlined" aria-hidden="true">cancel</span>
    </button>
  </div>

  <div class="md3e-field__supporting">
    <span class="md3e-field__hint" id="uri-hint">Public HTTPS endpoint for synced tokens</span>
    <span class="md3e-field__error" id="uri-error" role="alert" hidden>Enter a valid workspace host</span>
    <span class="md3e-field__counter">15 / 60</span>
  </div>
</div>
```

```css
.md3e-field {
  --md3e-field-accent: var(--md-sys-color-on-surface-variant);
  --md3e-field-stroke: var(--md-sys-color-outline);
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-1); /* 4dp supporting text top gap */
  inline-size: 100%;
}

.md3e-field__control {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-2);
  min-block-size: calc(56px + var(--md-sys-density-offset, 0px));
  padding-inline: var(--md-sys-spacing-4);
  border-radius: var(--md-sys-shape-corner-extra-small);
  background: transparent;
  color: var(--md-sys-color-on-surface);
}

.md3e-field--outlined .md3e-field__control:has(.md3e-field__leading),
.md3e-field--outlined .md3e-field__control:has(.md3e-field__clear) {
  padding-inline: var(--md-sys-spacing-3); /* 12dp with icons */
}

/* Native transparent cutout notch via <fieldset><legend> (never a solid <label> patch) */
.md3e-field__outline {
  position: absolute;
  inset: 0;
  margin: 0;
  padding-inline: var(--md-sys-spacing-3);
  border: 1px solid var(--md3e-field-stroke);
  border-radius: inherit;
  pointer-events: none;
  transition: border-color var(--md-sys-motion-fast-effects);
}

.md3e-field__notch {
  display: block;
  float: none;
  inline-size: auto;
  max-inline-size: 0.01px;
  padding: 0;
  block-size: 11px;
  overflow: hidden;
  visibility: hidden;
  white-space: nowrap;
  font-size: var(--md-sys-typescale-body-small-size);
  line-height: 1;
  transition: max-inline-size var(--md-sys-motion-fast-spatial),
              padding-inline var(--md-sys-motion-fast-spatial);
}

.md3e-field--outlined:focus-within .md3e-field__outline,
.md3e-field--outlined:has(.md3e-field__input:not(:placeholder-shown)) .md3e-field__outline {
  padding-inline: var(--md-sys-spacing-3);
}

.md3e-field--outlined:focus-within .md3e-field__notch,
.md3e-field--outlined:has(.md3e-field__input:not(:placeholder-shown)) .md3e-field__notch {
  max-inline-size: 100%;
  padding-inline: var(--md-sys-spacing-1); /* 4dp populated label horizontal padding */
}

.md3e-field--outlined:focus-within {
  --md3e-field-stroke: var(--md-sys-color-primary);
  --md3e-field-accent: var(--md-sys-color-primary);
}

.md3e-field--outlined:focus-within .md3e-field__outline {
  border-width: 2px;
}

.md3e-field__input {
  flex: 1 1 auto;
  min-inline-size: 0;
  min-block-size: var(--md-sys-touch-target-min);
  border: none;
  padding: 0;
  background: transparent;
  color: var(--md-sys-color-on-surface);
  caret-color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  outline: 2px solid transparent;
}

.md3e-field__label {
  position: absolute;
  inset-inline-start: var(--md-sys-spacing-4);
  inset-block-start: 50%;
  transform: translateY(-50%);
  transform-origin: start center;
  color: var(--md3e-field-accent); /* Transparent natively; <fieldset><legend> cuts the border gap */
  font-size: var(--md-sys-typescale-body-large-size);
  line-height: var(--md-sys-typescale-body-large-line-height);
  pointer-events: none;
  transition: transform var(--md-sys-motion-fast-spatial),
              color var(--md-sys-motion-fast-effects);
}

.md3e-field__control:has(.md3e-field__leading) .md3e-field__label {
  inset-inline-start: 52px; /* 12dp pad + 24dp icon + 16dp gap */
}

.md3e-field--outlined:focus-within .md3e-field__label,
.md3e-field--outlined:has(.md3e-field__input:not(:placeholder-shown)) .md3e-field__label {
  inset-inline-start: var(--md-sys-spacing-4);
  transform: translateY(calc(-50% - 28px)) scale(0.75);
}

.md3e-field__leading,
.md3e-field__affix {
  color: var(--md-sys-color-on-surface-variant);
  flex-shrink: 0;
}

.md3e-field__clear {
  position: relative;
  display: inline-grid;
  place-items: center;
  inline-size: 32px;
  block-size: 32px;
  padding: 0;
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
  opacity: 0;
  transform: scale(0.8);
  pointer-events: none;
  transition: opacity var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-fast-spatial);
}

.md3e-field__clear::before {
  content: "";
  position: absolute;
  inset: -8px;
  min-inline-size: var(--md-sys-touch-target-min);
  min-block-size: var(--md-sys-touch-target-min);
}

.md3e-field:has(.md3e-field__input:not(:placeholder-shown)) .md3e-field__clear {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

.md3e-field__clear:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

/* Error validation via native :user-invalid or explicit [aria-invalid="true"] */
.md3e-field:has(.md3e-field__input:user-invalid),
.md3e-field:has(.md3e-field__input[aria-invalid="true"]) {
  --md3e-field-stroke: var(--md-sys-color-error);
  --md3e-field-accent: var(--md-sys-color-error);
}

.md3e-field:has(.md3e-field__input:user-invalid) .md3e-field__input,
.md3e-field:has(.md3e-field__input[aria-invalid="true"]) .md3e-field__input {
  caret-color: var(--md-sys-color-error);
}

.md3e-field__supporting {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--md-sys-spacing-4); /* 16dp between supporting text and counter */
  padding-inline: var(--md-sys-spacing-4);
  font-size: var(--md-sys-typescale-body-small-size);
  line-height: var(--md-sys-typescale-body-small-line-height);
  color: var(--md-sys-color-on-surface-variant);
}

.md3e-field__error {
  color: var(--md-sys-color-error);
}

.md3e-field__counter {
  margin-inline-start: auto;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

@media (prefers-reduced-motion: reduce) {
  .md3e-field__outline,
  .md3e-field__notch,
  .md3e-field__label,
  .md3e-field__clear {
    transition: none;
  }
}

@media (forced-colors: active) {
  .md3e-field__outline {
    border-color: CanvasText;
  }
  .md3e-field--outlined:focus-within .md3e-field__outline {
    border-color: Highlight;
  }
}
```

```js
// Dynamic aria-describedby error linkage & clear micro-interaction
function syncFieldValidation(inputEl, hintId, errorEl, counterEl) {
  const max = Number(inputEl.maxLength) || 60;
  if (counterEl) counterEl.textContent = `${inputEl.value.length} / ${max}`;
  const invalid = !inputEl.checkValidity();
  inputEl.setAttribute('aria-invalid', String(invalid));
  if (errorEl) errorEl.hidden = !invalid;
  inputEl.setAttribute('aria-describedby', invalid && errorEl ? `${hintId} ${errorEl.id}` : hintId);
}
```

---

## Date pickers

Source: https://m3.material.io/components/date-pickers/specs

**Variants.** Three variants are documented on the spec page: docked date picker, modal date picker, and modal date input. The page also documents a menu attached to the docked date picker (month/year selection menu) and, inside the modal picker, day selection, year selection and date-range diagrams. The dump contains no M3 Expressive–era wording, so the M3 vs M3 Expressive columns below are `—`.

**Configurations** — M3 vs M3 Expressive availability.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Docked date picker | Day selection | — | — |
| Docked date picker | Month selection | — | — |
| Docked date picker | Year selection | — | — |
| Modal date picker | Single date selection | — | — |
| Modal date picker | Date range selection | — | — |
| Modal date picker | Year selection | — | — |
| Modal date input | Single date input | — | — |
| Modal date input | Date range input | — | — |

No M3 / M3 Expressive availability statement exists in the dump, so those two columns are `—` for every row.

**Anatomy.** The dump lists elements per diagram, in diagram order. Sub-groups below follow the diagram boundaries visible in the rendered text (the modal picker runs through three diagrams; the repeat of "Headline, Supporting text" marks each new diagram). All element names are verbatim.

Docked date picker:

1. Outlined text field
2. Menu button: Month selection
3. Menu button: Year selection
4. Icon button
5. Weekdays label text
6. Unselected date
7. Today's date
8. Outside month date
9. Text buttons
10. Selected date
11. Container

Docked date picker menu:

1. Outlined text field
2. Menu button: Month selection (pressed)
3. Menu button: Year selection (disabled)
4. Header
5. Menu
6. Selected list item
7. Unselected menu list item
8. Container

Modal date picker — day selection:

1. Headline
2. Supporting text
3. Header
4. Container
5. Icon button
6. Icon buttons
7. Weekdays
8. Today's date
9. Unselected date
10. Text buttons
11. Selected date
12. Menu button
13. Divider

Modal date picker — year selection:

1. Headline
2. Supporting text
3. Header
4. Container
5. Icon button
6. Unselected year
7. Selected year
8. Text buttons
9. Divider
10. Menu button

Modal date picker — date range selector:

1. Headline
2. Supporting text
3. Icon button
4. Header
5. Text button
6. Icon button
7. Weekdays label text
8. Container
9. Today's date
10. Unselected date
11. In-range active indicator
12. In-range date
13. Month subhead
14. Selected date
15. Divider

Modal date input:

1. Headline
2. Supporting text
3. Header
4. Container
5. Icon button
6. Outlined text field
7. Text buttons
8. Divider

**Colour roles.**

Caveat that applies to every colour-role table in this file: the page renders colour roles as swatch diagrams. The rendered text yields the roles only as an unlabelled ordered sequence whose length does not match the element list for these diagrams, so element → role pairing is **not** recoverable. Roles are therefore transcribed in exact source order, with the diagram's element list given above for visual cross-reference. No element→role pairing is asserted.

Docked date picker — "Docked date picker color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | Primary |
| 2 | On surface variant |
| 3 | On surface variant |
| 4 | On surface |
| 5 | On surface |
| 6 | Primary |
| 7 | On surface variant |
| 8 | Primary |
| 9 | Surface container high |
| 10 | Primary |
| 11 | On primary |

Docked date picker menu — "Docked date picker menu color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | Primary |
| 2 | On surface variant |
| 3 | On surface |
| 4 | Outline variant |
| 5 | Surface container high |
| 6 | Surface variant |
| 7 | On surface |

Modal date picker — "Modal date picker color roles used for light and dark themes in a day selection menu":

| # | Role |
|---|---|
| 1 | On surface |
| 2 | On surface variant |
| 3 | Surface container high |
| 4 | On surface variant |
| 5 | On surface variant |
| 6 | On surface |
| 7 | Primary |
| 8 | On surface |
| 9 | Primary |
| 10 | Primary |
| 11 | On surface variant |
| 12 | Outline variant |

Modal date picker — "Modal date picker color roles used for light and dark themes in a year selection menu":

| # | Role |
|---|---|
| 1 | On surface |
| 2 | On surface variant |
| 3 | Surface container high |
| 4 | On surface variant |
| 5 | On surface variant |
| 6 | Primary |
| 7 | Primary |
| 8 | Outline variant |
| 9 | On surface variant |

Modal date picker — "Modal date picker range selector color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | On surface |
| 2 | On surface variant |
| 3 | On surface variant |
| 4 | Surface container high |
| 5 | Primary |
| 6 | On surface variant |
| 7 | On surface |
| 8 | Primary |
| 9 | On surface |
| 10 | Secondary container |
| 11 | On secondary container |
| 12 | Outline variant |
| 13 | On surface variant |
| 14 | Primary |

Modal date input — "Modal date input color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | On surface |
| 2 | On surface variant |
| 3 | Surface container high |
| 4 | On surface variant |
| 5 | Primary |
| 6 | Primary |
| 7 | Outline variant |

Disabled states: the only disabled item named in the dump is the "Menu button: Year selection (disabled)" anatomy part of the docked date picker; no distinct disabled colour role, opacity or token value is given. Error states: not present at all in this dump. Both are `—`.

| Element | Role |
|---|---|
| Menu button: Year selection (disabled) | — |
| Any error-state colour role | — |

**States.**

"States for date and year selection:" — Default (enabled), Disabled, Hovered, Focused, Pressed (ripple).

The token module's state selector for the docked date picker exposes: Enabled, Disabled, Hovered, Focused, Pressed (ripple).

No state behaviour prose (overlay opacities, ripple specification, transition timings) is present in the dump.

**Shape & morph.** The dump contains no shape statement, no morph behaviour, and no corner-radius table for any date picker variant. All corner radii are `—`.

| Variant | Attribute | Value |
|---|---|---|
| Docked date picker | Corner radius (container) | — |
| Docked date picker | Corner radius (menu) | — |
| Modal date picker | Corner radius (container) | — |
| Modal date input | Corner radius (container) | — |

**Measurements.** No measurement values exist in the rendered page text. The page provides only three diagram captions for the docked picker, three for the modal picker and one for the modal date input; the numbers themselves are rendered inside diagrams and are absent from the rendered text.

Modal date picker, day selection view — the values below are read from the official measurement diagram "Diagram of size and padding measurements in day selection view" (retrieved 2026-09-12). The diagram prints a number against each leader line or dimension brace but prints no attribute names, so each row below states what that number is attached to in the drawing.

| Attribute | Value |
|---|---|
| Container width | 360dp |
| Container height | 524dp |
| Top padding | 16dp |
| Band between the supporting text row and the headline row | 36dp |
| Headline row height | 40dp |
| Band below the headline row | 12dp |
| Band above the month / weekday row | 4dp |
| Month menu button height | 40dp |
| Icon button size (edit and chevron icon buttons) | 48dp |
| Band below the month / weekday row | 4dp |
| Day cell size | 48dp |
| Today's-date indicator size | 40dp |
| Band above the text button row | 8dp |
| Text button height | 40dp |
| Bottom padding | 12dp |
| Left padding at the top edge (header rows) | 24dp |
| Header text column width | 268dp |
| Gap between the header text column and the trailing icon column | 8dp |
| Trailing icon column width | 48dp |
| Right padding | 12dp |
| Left padding at the bottom edge | 12dp |
| Gap between the two text buttons (Cancel / OK) | 8dp |
| Distance from the top of the header content area to the top of the trailing icon button | 44dp |

All other diagram groups remain `—`:

| Variant | Measurement diagram group present in dump | Attribute values in dump |
|---|---|---|
| Docked date picker | Docked date picker padding and size measurements | — |
| Docked date picker | Docked date picker month menu padding and size measurements | — |
| Modal date picker | Modal date picker padding and size measurements (day selection view) | see table above |
| Modal date picker | Modal date picker year selector padding and size measurements | — |
| Modal date picker | Modal date picker date range selector padding and size measurements | — |
| Modal date input | Modal date input padding and size measurements | — |

The other diagram groups are not recoverable from this dump — they would have to be read from the diagrams on the live spec page.

**Notes.** The dump contains no explicit do/don't, caution, or "not recommended" statement for date pickers.

### Modern Web Architecture (Docked & Modal Anatomy, Single vs Range Strip & Headless Adapters)

#### 1. Docked vs Modal Anatomy & Geometry

- **Container & Tokens**: `surface-container-high` (`--md-sys-color-surface-container-high`), `28px` (`--md-sys-shape-corner-extra-large`) modal / `16px` (`--md-sys-shape-corner-large`) docked popover, `360px` modal inline width, `48×48px` day gridcell targets with `40×40px` visual indicator pills (`--md-sys-shape-corner-full`), `1px` `--md-sys-color-outline-variant` divider between header and calendar/actions.
- **Docked Picker**: Anchored `[popover="auto"]` surface paired with an Outlined Text Field trigger and CSS Anchor Positioning (`@supports (position-area: block-end)` + `position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline`).
- **Modal Picker**: Native `<dialog>` via `.showModal()` (`dialog:modal { overscroll-behavior: contain; }`), optional date-input mode switch icon button, and `Cancel` / `OK` actions (`48×48px` accessible target via `::before` on `40px` buttons).

#### 2. Unified State Attribute Contract (Single & Continuous Range Selection)

Style calendar day cells and buttons cleanly using semantic `data-*` attributes so both vanilla `role="grid"` calendars and headless React/Vue/Svelte primitives share a single MD3E skin:

| Attribute | Role & Visual Treatment |
|---|---|
| `[data-today="true"]` | `40×40px` circle outline `1px solid var(--md-sys-color-primary)`, label `--md-sys-color-primary` |
| `[data-selected="true"]` | Single selection: `40×40px` solid `--md-sys-color-primary` circle, `--md-sys-color-on-primary` label |
| `[data-range-start="true"]` | Circular `--md-sys-color-primary` start cap (`z-index: 1`) + trailing half `secondary-container` connector when `[data-has-range-end="true"]:not(:last-child)` (`:last-child::before` stays `transparent`) |
| `[data-in-range="true"]` | Applied strictly to interior days (`start < date < end`): continuous `var(--md-sys-color-secondary-container)` connector strip behind day number, rounded at `--md3e-dp-edge-inset` on row boundaries (`:first-child` / `:last-child`), `--md-sys-color-on-secondary-container` label |
| `[data-range-end="true"]` | Circular `--md-sys-color-primary` end cap (`z-index: 1`) + leading half `secondary-container` connector when `[data-has-range-start="true"]:not(:first-child)` (`:first-child::before` stays `transparent`) |
| `[data-outside-month="true"]` | Muted `--md-sys-color-on-surface-variant` at reduced emphasis (`opacity: 0.56`) |
| `[data-disabled="true"]` | `--md-sys-state-disabled-content-opacity` (`0.38`), `pointer-events: none` |

#### 3. `role="grid"` Keyboard Navigation Model

- Expose a 7-column calendar table/grid (`role="grid"`, `aria-labelledby` pointing to the `aria-live="polite"` month/year heading), header row (`role="columnheader"` Mon–Sun), and `role="gridcell"` cells containing focusable day `<button type="button">` elements managed with **roving `tabindex`** (`tabindex="0"` on the active day, `tabindex="-1"` on siblings):
  - `ArrowLeft` / `ArrowRight`: move focus `-1` / `+1` day (crossing weeks/months smoothly).
  - `ArrowUp` / `ArrowDown`: move focus `-7` / `+7` days.
  - `Home` / `End`: jump to start / end of the current week row.
  - `PageUp` / `PageDown`: move `-1` / `+1` month (`Shift + PageUp` / `Shift + PageDown` for `-1` / `+1` year).
  - `Enter` / `Space`: commit single date or advance range selection (`start` -> `end`).

```html
<!-- Docked / Modal M3E Calendar Grid (Single & Continuous Range) -->
<section class="md3e-dp" aria-label="Schedule window">
  <header class="md3e-dp__header">
    <div class="md3e-dp__headline">
      <span class="md3e-dp__eyebrow">Select dates</span>
      <strong class="md3e-dp__summary" id="dp-summary">Nov 12 – Nov 16</strong>
    </div>
    <div class="md3e-dp__nav">
      <h3 class="md3e-dp__month" id="dp-month-label" aria-live="polite">November 2026</h3>
      <button type="button" class="md3e-dp__nav-btn" aria-label="Previous month">
        <span class="material-symbols-outlined" aria-hidden="true">chevron_left</span>
      </button>
      <button type="button" class="md3e-dp__nav-btn" aria-label="Next month">
        <span class="material-symbols-outlined" aria-hidden="true">chevron_right</span>
      </button>
    </div>
  </header>

  <div class="md3e-dp__grid" role="grid" aria-labelledby="dp-month-label">
    <div class="md3e-dp__row" role="row">
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Monday">M</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Tuesday">T</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Wednesday">W</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Thursday">T</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Friday">F</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Saturday">S</span>
      <span class="md3e-dp__weekday" role="columnheader" aria-label="Sunday">S</span>
    </div>
    <div class="md3e-dp__row" role="row">
      <div class="md3e-dp__cell" role="gridcell" data-range-start="true" data-has-range-end="true">
        <button type="button" class="md3e-dp__day" tabindex="0" aria-label="November 12, 2026" aria-selected="true">12</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell" data-in-range="true">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="November 13, 2026" aria-selected="true">13</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell" data-in-range="true" data-today="true">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="November 14, 2026 (Today)" aria-selected="true">14</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell" data-in-range="true">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="November 15, 2026" aria-selected="true">15</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell" data-range-end="true" data-has-range-start="true">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="November 16, 2026" aria-selected="true">16</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="November 17, 2026">17</button>
      </div>
      <div class="md3e-dp__cell" role="gridcell" data-outside-month="true">
        <button type="button" class="md3e-dp__day" tabindex="-1" aria-label="December 1, 2026">1</button>
      </div>
    </div>
  </div>
</section>
```

```css
.md3e-dp {
  --md3e-dp-cap-size: 40px;
  --md3e-dp-edge-inset: calc((100% - var(--md3e-dp-cap-size)) / 2);
  inline-size: min(100%, 360px);
  padding: var(--md-sys-spacing-4) var(--md-sys-spacing-3) var(--md-sys-spacing-3);
  border-radius: var(--md-sys-shape-corner-extra-large); /* 28dp */
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
}

.md3e-dp__header {
  display: flex;
  flex-direction: column;
  gap: var(--md-sys-spacing-3);
  padding-inline: var(--md-sys-spacing-3);
  padding-block-end: var(--md-sys-spacing-2);
  border-block-end: 1px solid var(--md-sys-color-outline-variant);
}

.md3e-dp__eyebrow {
  display: block;
  font-size: var(--md-sys-typescale-label-medium-size);
  line-height: var(--md-sys-typescale-label-medium-line-height);
  color: var(--md-sys-color-on-surface-variant);
}

.md3e-dp__summary {
  font-family: var(--md-sys-typescale-brand-font);
  font-size: var(--md-sys-typescale-headline-large-size);
  line-height: var(--md-sys-typescale-headline-large-line-height);
  font-weight: var(--md-sys-typescale-headline-large-weight);
  font-variant-numeric: tabular-nums;
}

.md3e-dp__nav {
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-1);
}

.md3e-dp__month {
  margin: 0;
  margin-inline-end: auto;
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  font-weight: var(--md-sys-typescale-label-large-weight);
  color: var(--md-sys-color-on-surface-variant);
}

.md3e-dp__nav-btn {
  display: grid;
  place-items: center;
  inline-size: var(--md-sys-touch-target-min);
  block-size: var(--md-sys-touch-target-min);
  border: none;
  border-radius: var(--md-sys-shape-corner-full);
  background: transparent;
  color: var(--md-sys-color-on-surface-variant);
  cursor: pointer;
}

.md3e-dp__nav-btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

.md3e-dp__row {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
}

.md3e-dp__weekday {
  display: grid;
  place-items: center;
  block-size: var(--md-sys-touch-target-min);
  font-size: var(--md-sys-typescale-body-medium-size);
  color: var(--md-sys-color-on-surface-variant);
}

.md3e-dp__cell {
  position: relative;
  display: grid;
  place-items: center;
  block-size: var(--md-sys-touch-target-min); /* 48dp day cell */
}

/* Continuous secondary-container connector strip sitting behind 40px circular primary caps */
.md3e-dp__cell[data-in-range="true"]:not([data-range-start="true"]):not([data-range-end="true"])::before,
.md3e-dp__cell[data-range-start="true"][data-has-range-end="true"]:not([data-range-end="true"]):not(:last-child)::before,
.md3e-dp__cell[data-range-end="true"][data-has-range-start="true"]:not([data-range-start="true"]):not(:first-child)::before {
  content: "";
  position: absolute;
  inset-block: calc((100% - var(--md3e-dp-cap-size)) / 2);
  inset-inline: 0;
  border-radius: 0;
  background: var(--md-sys-color-secondary-container);
  z-index: 0;
  pointer-events: none;
}

.md3e-dp__cell[data-in-range="true"]:not([data-range-start="true"]):not([data-range-end="true"]):first-child::before {
  inset-inline-start: var(--md3e-dp-edge-inset);
  border-start-start-radius: var(--md-sys-shape-corner-full);
  border-end-start-radius: var(--md-sys-shape-corner-full);
}

.md3e-dp__cell[data-in-range="true"]:not([data-range-start="true"]):not([data-range-end="true"]):last-child::before {
  inset-inline-end: var(--md3e-dp-edge-inset);
  border-start-end-radius: var(--md-sys-shape-corner-full);
  border-end-end-radius: var(--md-sys-shape-corner-full);
}

.md3e-dp__cell[data-range-start="true"][data-has-range-end="true"]:not([data-range-end="true"]):not(:last-child)::before {
  inset-inline: 50% 0;
}

.md3e-dp__cell[data-range-end="true"][data-has-range-start="true"]:not([data-range-start="true"]):not(:first-child)::before {
  inset-inline: 0 50%;
}

.md3e-dp__cell[data-range-start="true"]:last-child::before,
.md3e-dp__cell[data-range-end="true"]:first-child::before {
  background: transparent;
}

.md3e-dp__day {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  inline-size: var(--md3e-dp-cap-size);
  block-size: var(--md3e-dp-cap-size);
  padding: 0;
  border: 1px solid transparent;
  border-radius: var(--md-sys-shape-corner-full);
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-body-medium-size);
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

/* Expand 40px visual day circle to full 48x48dp accessible hit target */
.md3e-dp__day::before {
  content: "";
  position: absolute;
  inset: -4px;
  min-inline-size: var(--md-sys-touch-target-min);
  min-block-size: var(--md-sys-touch-target-min);
}

.md3e-dp__cell[data-today="true"] .md3e-dp__day {
  border-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-primary);
}

.md3e-dp__cell[data-in-range="true"] .md3e-dp__day {
  color: var(--md-sys-color-on-secondary-container);
}

.md3e-dp__cell[data-selected="true"] .md3e-dp__day,
.md3e-dp__cell[data-range-start="true"] .md3e-dp__day,
.md3e-dp__cell[data-range-end="true"] .md3e-dp__day {
  background: var(--md-sys-color-primary);
  border-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
}

.md3e-dp__cell[data-outside-month="true"] .md3e-dp__day {
  color: var(--md-sys-color-on-surface-variant);
  opacity: 0.56;
}

.md3e-dp__cell[data-disabled="true"] .md3e-dp__day {
  opacity: var(--md-sys-state-disabled-content-opacity);
  pointer-events: none;
}

.md3e-dp__day:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

@media (prefers-reduced-motion: reduce) {
  .md3e-dp__day {
    transition: none;
  }
}

@media (forced-colors: active) {
  .md3e-dp__cell[data-in-range="true"]:not([data-range-start="true"]):not([data-range-end="true"])::before,
  .md3e-dp__cell[data-range-start="true"][data-has-range-end="true"]:not([data-range-end="true"]):not(:last-child)::before,
  .md3e-dp__cell[data-range-end="true"][data-has-range-start="true"]:not([data-range-start="true"]):not(:first-child)::before {
    background: CanvasText;
    opacity: 0.25;
  }
  .md3e-dp__cell[data-selected="true"] .md3e-dp__day,
  .md3e-dp__cell[data-range-start="true"] .md3e-dp__day,
  .md3e-dp__cell[data-range-end="true"] .md3e-dp__day {
    background: Highlight;
    border-color: Highlight;
    color: HighlightText;
  }
}
```

#### 4. Zero-Conflict Headless Adapter Recipes (`Radix / Base UI / Ark UI / React Aria`)

Use the same MD3E visual classes above by matching each headless library's native `data-*` attributes without fighting Shadow DOM or custom styling overrides:

- **React Aria (`RangeCalendar` / `DateRangePicker`)**:
  - Maps `[data-selected]` inside `[data-selection-start]` / `[data-selection-end]` to circular `primary` caps, and `[data-selected]:not([data-selection-start]):not([data-selection-end])` to the `secondary-container` continuous strip; `[data-outside-month]` and `[data-disabled]` match directly.
- **Ark UI Date Picker (`@ark-ui/react/date-picker`)**:
  - `DatePicker.Content` exposes `[data-state="open|closed"]` (`surface-container-high`, `16dp` docked / `28dp` modal), and `DatePicker.TableCellTrigger` emits `[data-today]`, `[data-selected]`, `[data-in-range]`, `[data-range-start]`, `[data-range-end]`, `[data-outside-range]`, `[data-disabled]`.
- **Radix UI / Base UI Popover + Custom `role="grid"`**:
  - Wrap the docked `.md3e-dp` `role="grid"` inside `Popover.Content` (`[data-state="open|closed"]` in Radix; `[data-open]` / `[data-closed]` in Base UI) anchored to an Outlined Text Field (`56dp`), keeping full focus management, `Escape` dismissal, and `aria-expanded` synchronization automatically wired.

```css
/* Zero-conflict Headless Adapter mapping for React Aria & Ark UI Date Picker cells */
:is([data-rac][role="gridcell"], [data-scope="date-picker"][data-part="table-cell"]) {
  position: relative;
  display: grid;
  place-items: center;
  block-size: var(--md-sys-touch-target-min);
}

:is([data-rac], [data-part="table-cell-trigger"]):is([data-in-range], [data-selected]:not([data-selection-start]):not([data-selection-end]):not([data-range-start]):not([data-range-end])) {
  background: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

:is([data-rac], [data-part="table-cell-trigger"]):is([data-selection-start], [data-selection-end], [data-range-start], [data-range-end], [data-selected]:not([data-in-range])) {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border-radius: var(--md-sys-shape-corner-full);
}

:is([data-scope="popover"][data-part="content"], .md3e-dp-popover)[data-state="open"] {
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  border-radius: var(--md-sys-shape-corner-large);
  transition: opacity var(--md-sys-motion-fast-effects),
              transform var(--md-sys-motion-default-spatial);
}

@media (prefers-reduced-motion: reduce) {
  :is([data-scope="popover"][data-part="content"], .md3e-dp-popover)[data-state="open"] {
    transition: none;
  }
}
```

---

## Time pickers

Source: https://m3.material.io/components/time-pickers/specs

**Variants.** Two variants are documented on the spec page: the time picker dial and the time picker input. The dial is documented in a vertical and a horizontal layout, and in 12-hour and 24-hour form. The dump contains no M3 Expressive–era wording, so the M3 vs M3 Expressive columns below are `—`.

**Configurations** — M3 vs M3 Expressive availability.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Orientation | Vertical layout (default on mobile) | — | — |
| Orientation | Horizontal layout | — | — |
| 24-hour time picker dial | 24h dial in vertical layout (default on mobile) | — | — |
| 24-hour time picker dial | 24h dial in horizontal layout | — | — |
| 12-hour and 24-hour time picker inputs | 12h input | — | — |
| 12-hour and 24-hour time picker inputs | 24h input | — | — |

No M3 / M3 Expressive availability statement exists in the dump, so those two columns are `—` for every row.

**Anatomy.**

Time picker dial:

1. Headline
2. Time selector separator
3. Container
4. Period selector container
5. Period selector label text
6. Clock dial selector center
7. Clock dial selector track
8. Text button
9. Icon button
10. Clock dial selector container
11. Clock dial label text
12. Clock dial container
13. Time selector label text
14. Time selector container

Time picker input:

1. Headline
2. Time input field seperator *(spelling as rendered in the source)*
3. Container
4. Period selector container
5. Period selector label text
6. Text button
7. Icon button
8. Time input field supporting text
9. Time input field label text
10. Time input field container

**Colour roles.**

Caveat that applies to every colour-role table in this file: the page renders colour roles as swatch diagrams. The rendered text yields the roles only as an unlabelled ordered sequence whose length does not match the element list for these diagrams, so element → role pairing is **not** recoverable. Roles are therefore transcribed in exact source order, with the diagram's element list given above for visual cross-reference. No element→role pairing is asserted. Note also that the dial list repeats several roles (On surface variant, On surface, Surface container highest) and adds On primary container / Primary container at the end, consistent with a multi-part diagram rather than a 1:1 element list.

Time picker dial — "Time picker dial color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | On surface variant |
| 2 | On surface |
| 3 | Surface container highest |
| 4 | On surface |
| 5 | Tertiary container |
| 6 | On tertiary container |
| 7 | Surface container high |
| 8 | Outline |
| 9 | On surface |
| 10 | Primary |
| 11 | On primary |
| 12 | Primary |
| 13 | On surface variant |
| 14 | On surface |
| 15 | Surface container highest |
| 16 | On primary container |
| 17 | Primary container |

Time picker input — "Time picker input color roles used for light and dark themes":

| # | Role |
|---|---|
| 1 | On surface variant |
| 2 | On surface |
| 3 | Surface container highest |
| 4 | On surface |
| 5 | Tertiary container |
| 6 | On tertiary container |
| 7 | Surface container high |
| 8 | Outline |
| 9 | On surface |
| 10 | Primary |
| 11 | On surface variant |
| 12 | On primary container |
| 13 | Primary container |

Error states and disabled states: the dump contains no error colour roles and no disabled colour roles for either variant, and no disabled state is listed at all. Both are `—`.

| Element | Role |
|---|---|
| Error — any element | — |
| Disabled — any element | — |

**States.**

States listed for time pickers: Enabled, Hover, Focus, Pressed.

Stated behaviour, verbatim from the page: "States specs can be found in the token module above."

The token module's state selector exposes: Enabled, Hovered, Focused, Pressed (ripple). No disabled state is listed, and no state overlay, elevation or timing values are given in the dump.

**Shape & morph.** The dump contains no shape statement, no morph behaviour, and no corner-radius table for either variant. The dial exposes a "Clock dial selector center" and "Clock dial selector track" whose only stated properties are sizes (see Measurements); no corner radii are given. All corner radii are `—`.

| Variant | Attribute | Value |
|---|---|---|
| Time picker dial | Corner radius (container) | — |
| Time picker dial | Corner radius (clock dial selector container) | — |
| Time picker input | Corner radius (container) | — |
| Time picker input | Corner radius (time input field container) | — |

**Measurements.**

Time picker dial - vertical — "Vertical time picker dial padding and size measurements":

Container

| Attribute | Value |
|---|---|
| Width | Dynamic |
| Height | Dynamic |
| Headline alignment | Left |
| Top/bottom padding | 24dp |
| Left/right padding | 24dp |

Time selector container

| Attribute | Value |
|---|---|
| Width | 96dp |
| Width (24h vertical) | 114dp |
| Height | 80dp |

Period selector container

| Attribute | Value |
|---|---|
| Width (vertical layout) | 52dp |
| Height (vertical layout) | 80dp |
| Width (horizontal layout) | 216dp |
| Height (horizontal layout) | 38dp |

Clock dial container

| Attribute | Value |
|---|---|
| Size | 256dp |

Clock dial selector handle

| Attribute | Value |
|---|---|
| Size | 48dp |

Clock dial selector center

| Attribute | Value |
|---|---|
| Size | 8dp |

Clock dial selector track

| Attribute | Value |
|---|---|
| Width | 2dp |

Time picker dial - horizontal — "Horizontal time picker dial padding and size measurements":

Container

| Attribute | Value |
|---|---|
| Width | Dynamic |
| Height | Dynamic |
| Headline alignment | Left |
| Top/bottom padding | 24dp |
| Left/right padding | 24dp |

Time selector container

| Attribute | Value |
|---|---|
| Width | 96dp |
| Width (24h vertical) | 114dp |
| Height | 80dp |

Period selector container

| Attribute | Value |
|---|---|
| Width (vertical layout) | 52dp |
| Height (vertical layout) | 80dp |
| Width (horizontal layout) | 216dp |
| Height (horizontal layout) | 38dp |

Clock dial container

| Attribute | Value |
|---|---|
| Size | 256dp |

Clock dial selector handle

| Attribute | Value |
|---|---|
| Size | 48dp |

Clock dial selector center

| Attribute | Value |
|---|---|
| Size | 8dp |

Clock dial selector track

| Attribute | Value |
|---|---|
| Width | 2dp |

Time picker input — "Time picker input padding and size measurements":

Container

| Attribute | Value |
|---|---|
| Width | Dynamic |
| Height | Dynamic |
| Headline alignment | Left |
| Top/bottom padding | 24dp |
| Left/right padding | 24dp |

Time input field container

| Attribute | Value |
|---|---|
| Width | 96dp |
| Height | 72dp |

Period selector container

| Attribute | Value |
|---|---|
| Width | 52dp |
| Height | 72dp |

Delta between the dial groups: the vertical and horizontal dial tables carry identical attributes and identical values in the dump. The input variant differs from the dial: its time input field container is 96dp × 72dp (versus the dial's time selector container at 96dp × 80dp) and its period selector container is 52dp × 72dp (versus 52dp × 80dp vertically); it has no clock dial group.

**Notes.** The dump contains no explicit do/don't, caution, or "not recommended" statement for time pickers.
