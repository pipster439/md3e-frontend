# Text input components — Text fields, Date pickers, Time pickers

Transcribed from the Material Design 3 component spec pages on m3.material.io (retrieved 2026-09-12).
Any value shown as `—` was not present in the rendered text — the spec presents it only as a diagram, so no value is asserted here.
Rows marked **[baseline-token]** are cross-referenced from Google's official Material 3 baseline design tokens published in the `@material/web` repository (`tokens/versions/v0_192`, retrieved 2026-09-12); they fill values the spec page shows only as diagrams. Baseline token values, not Expressive-specific updates.

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

Error states and disabled states: the dump contains **no** colour-role values for error or disabled. Both are presented only as state diagrams ("Filled text field error states", "Outlined text field error states") with no role list and no token values. The table below is therefore filled from the official M3 baseline design tokens (`@material/web` v0_192, filled + outlined text-field token sets); roles that differ between the two variants are shown separately:

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
