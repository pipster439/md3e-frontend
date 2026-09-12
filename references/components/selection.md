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
