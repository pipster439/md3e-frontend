# Communication components

Transcribed from the Material Design 3 component specification pages on m3.material.io (badges, progress indicators, loading indicator, snackbar, tooltips). Retrieved 2026-09-12.
Any value shown as `—` was not present in the rendered page text — the spec presents it only as a diagram, so it could not be transcribed.

Note on colour roles: where the page shows colour roles as labelled swatches inside a diagram, the rendered text lists the role names in diagram order. The tables below pair those roles with elements in that same order; the page does not repeat element labels inline.

---

## Badges

Source: https://m3.material.io/components/badges/specs

**Variants.** Badges show notifications, counts, or status information on navigation items and icons. There are two sizes, and each is shown in two placements: small badge, and large badge (with container and label). The large badge also has a maximum character count form.

**Configurations** — M3 vs M3 Expressive availability, as a table with columns `Category | Configuration | M3 | M3 Expressive`.

The rendered page contains no `M3 / M3 Expressive` availability table for badges. It contains only the configuration list below; availability is therefore `—`.

The page does not group these configurations into categories, so `Category` is `—`.

| Category | Configuration | M3 | M3 Expressive |
| --- | --- | --- | --- |
| — | Inactive with label – small badge | — | — |
| — | Inactive with label – large badge | — | — |
| — | Inactive with label – large badge max character count | — | — |
| — | Inactive – small badge | — | — |
| — | Inactive – large badge | — | — |
| — | Inactive – large badge max character count | — | — |
| — | Active with label – small badge | — | — |
| — | Active with label – large badge | — | — |
| — | Active with label – large badge max character count | — | — |
| — | Active nav bar no label – small badge | — | — |
| — | Active nav bar no label – large badge | — | — |
| — | Active nav bar no label – large badge max character count | — | — |
| — | Active nav rail no label – small badge | — | — |
| — | Active nav rail no label – large badge | — | — |
| — | Active nav rail no label – large badge max character count | — | — |

The page states: "Different badges are shown on navigation destinations in various states."

**Anatomy.** The page has no separately headed "Anatomy" section; these element names come from the diagram labels at the top of the page, listed separately per placement.

Navigation bar:
1. Small badge
2. Large badge container
3. Large badge label
4. Large badge maximum character count container
5. Large badge maximum character count label

Navigation rail:
1. Small badge
2. Large badge container
3. Large badge label
4. Large badge maximum character count container
5. Large badge maximum character count label

**Colour roles** — a table of `Element | Role`, transcribed exactly.

Badge colour roles used for light and dark schemes in navigation bar:

| Element | Role |
| --- | --- |
| Small badge | Error |
| Large badge container | Error |
| Large badge label | On error |
| Large badge maximum character count container | On error |
| Large badge maximum character count label | Error |

Badge colour roles used for light and dark schemes in navigation rail:

| Element | Role |
| --- | --- |
| Small badge | Error |
| Large badge container | On error |
| Large badge label | Error |
| Large badge maximum character count container | On error |
| Large badge maximum character count label | Error |

**States.** The configuration list distinguishes **inactive** and **active** navigation destinations, each in three badge forms (small badge, large badge, large badge max character count), and with or without a label. The token browser exposes a `Enabled` state folder. No hovered / focused / pressed state is given for badges.

**Shape & morph.** Badge shape is a corner radius only; no morph behaviour is stated.

| Element | Corner radius |
| --- | --- |
| Small badge | 3dp corner radius |
| Large badge | 8dp corner radius |

**Measurements** — a table of `Attribute | Value`. The page labels this table "Badge padding and size measurements".

| Attribute | Value |
| --- | --- |
| Small badge shape | 3dp corner radius |
| Small badge size (HxW) | 6dp |
| Large badge shape | 8dp corner radius |
| Large badge one digit size (HxW) | 16dp |
| Large badge max character count size (HxW) | 16x34dp |
| Small badge: distance from top trailing icon corner to bottom leading badge corner (HxW) | 6x6dp |
| Large badge: distance from top trailing icon corner to bottom leading badge corner (HxW) | 14x12dp |
| Large badge padding between badge and text container | 4dp |

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears in the rendered text of this page. Colour values are implemented through design tokens: for design this means working with colour values that correspond with tokens; for implementation a colour value is a token that references a value.

---

## Progress indicators

Source: https://m3.material.io/components/progress-indicators/specs

**Variants.**

| Variant | M3 | M3 Expressive |
| --- | --- | --- |
| Linear progress indicator | Available | Available |
| Circular progress indicator | Available | Available |

**Configurations** — M3 vs M3 Expressive availability, as a table with columns `Category | Configuration | M3 | M3 Expressive`.

Upfront configuration summary from the page:

- Behavior: Determinate and indeterminate
- Thickness: Default (4dp) and variable
- Shape: Flat and wavy

| Category | Configuration | M3 | M3 Expressive |
| --- | --- | --- | --- |
| Behavior | Determinate (default), Indeterminate | Available | Available |
| Track thickness | Fixed (4dp) | Available | Available |
| Track thickness | Configurable | `--` | Available |
| Shape | Flat (default) | Available | Available |
| Shape | Wavy | `--` | Available |

**Delta flagged:** Configurable track thickness and the Wavy shape are **M3 Expressive only** (shown as `--` under M3). Both are the new Expressive options. The dump literally renders these two M3 cells as `--`; transcribed here as `--`.

**Anatomy.** Numbered list as given:

1. Active indicator
2. Track
3. Stop indicator

**Colour roles** — a table of `Element | Role`, transcribed exactly.

Source: official colour-role diagram (progress-indicators, `progress-indicators__03__color.png`), retrieved 2026-09-12.

Progress indicator colour roles used for light and dark schemes:

| Element | Role |
| --- | --- |
| Active indicator | Primary |
| Track | Secondary container |
| Stop indicator | Primary (positional: the diagram's stop-indicator callout is numbered `1`, the same callout number as the active indicator) |

The page lists two roles only (`Primary`, `Secondary container`). The diagram marks the active indicator and the stop indicator with the same callout number `1`, so the stop indicator shares the active indicator's role.

**States.** The component's behaviour axis is **determinate (default)** and **indeterminate** — both available in M3 and M3 Expressive. The token browser exposes an `Enabled` state folder, plus a `[Deprecated] Enabled` folder under the baseline token set. No hovered / focused / pressed states are given.

**Shape & morph.** Shape is a configurable axis: **Flat (default)** and **Wavy**, both available, with **Wavy being M3 Expressive only**. The page does not state corner radii for either shape.

Corner radii:

| Element | Corner radius |
| --- | --- |
| Linear progress indicator | — |
| Circular progress indicator | — |

Wave geometry is defined qualitatively, not numerically:

- "Wavy indicators use amplitude and wavelength to determine the shape of the wave. The height is the overall container height."
- "Amplitude measures from the center of the resting position to the center of the peak"
- "Wavelength measures the distance between two adjacent peaks"

**Measurements** — a table of `Attribute | Value` per variant. No numeric measurement table is present in the rendered text; the size measurements are supplied only as diagrams. Only the values below survive as text.

Source: official measurement diagrams (progress-indicators, `progress-indicators__06__measure.png` for linear, `progress-indicators__07__measure.png` for circular, `progress-indicators__04__measure.png` and `progress-indicators__05__measure.png` for the wave definitions, `progress-indicators__08__measure.png` for the 4dp inset), retrieved 2026-09-12.

Linear progress indicator:

| Attribute | Value |
| --- | --- |
| Track thickness (default / fixed) | 4dp |
| Inset from the edge of the screen | 4dp |
| Amplitude | 3dp (measured from the center of the resting position to the center of the peak) |
| Wavelength | 40dp (distance between two adjacent peaks) |
| Height | 10dp (wavy, default) / 14dp (wavy, thicker sample) |
| Size (default) | 4dp |
| Size (thicker variants) | 8dp (sample measurement for makers to adjust the default version based on their use cases) |

Circular progress indicator:

| Attribute | Value |
| --- | --- |
| Size (default) | 48dp |
| Size (thicker variants) | 40dp, 44dp and 52dp (sample measurements for makers to adjust the default version based on their use cases) |
| Track thickness | 4dp (default) / 8dp (thicker sample) |

The page's own framing: "Size measurements for linear progress indicators. The thicker variants are provided as sample measurement for makers to adjust the default version based on their use cases." and the same sentence for circular. Also: "The linear progress indicator is inset from the edge of the screen by 4dp".

**Notes.**

- Baseline tokens: "The circular and linear progress indicator had separate token sets. These are no longer recommended." The token browser labels them `[Deprecated] Progress indicator - Circular` and `[Deprecated] Enabled`.
- The combined `Progress Indicator - Common` token set is the current set.
- Token groups exposed: Color, Shape, and `[Deprecated] Enabled`.

---

## Loading indicator

Source: https://m3.material.io/components/loading-indicator/specs

**Variants.**

| Variant | M3 | M3 Expressive |
| --- | --- | --- |
| Loading indicator | `--` | Available |

**Delta flagged:** the loading indicator is a new component in the Expressive update — not available in M3.

**Configurations** — M3 vs M3 Expressive availability, as a table with columns `Category | Configuration | M3 | M3 Expressive`.

Upfront configuration summary from the page: Default, Contained.

| Category | Configuration | M3 | M3 Expressive |
| --- | --- | --- | --- |
| Containment | Default | `--` | Available |
| Containment | Contained | `--` | Available |

**Delta flagged:** both containment configurations are M3 Expressive only.

**Anatomy.** Numbered list as given:

1. Active indicator
2. Container

**Colour roles** — a table of `Element | Role`, transcribed exactly.

Loading indicator colour roles used for light and dark schemes:

| Element | Role |
| --- | --- |
| Active indicator | Primary |
| Container | — |

Contained loading indicator colour roles used for light and dark schemes:

| Element | Role |
| --- | --- |
| Active indicator | On primary container |
| Container | Primary container |

**States.** No states are listed for this component. The token browser shows only the `Default, Light` mode selector and a `Color` / `Size` / `Shape` group structure; no enabled/hovered/focused/pressed states are given. "Loading indicators have a single token set."

**Shape & morph.** The token browser exposes a `Shape` group, but the rendered text gives no corner radius or morph value. The only shape-related figure is the 38dp shape container under Measurements.

Corner radii:

| Element | Corner radius |
| --- | --- |
| Shape container | — |
| Active indicator | — |

**Measurements** — a table of `Attribute | Value` per variant. The page gives a single measurement statement covering the component and does not break it down per variant. Its exact wording: "To ensure sufficient margins, the size is 48dp while the shape container is 38dp".

Source: official measurement diagram (loading-indicator, `loading-indicator__05__measure.png`), retrieved 2026-09-12. The diagram measures both drawn forms (default and contained) at the same 48dp overall size and 38dp shape container, so the single statement above applies to both.

| Variant | Attribute | Value |
| --- | --- | --- |
| Default | Size | 48dp |
| Default | Shape container | 38dp |
| Contained | Size | 48dp (the diagram measures both drawn forms at 48dp) |
| Contained | Shape container | 38dp (the diagram measures both drawn forms at 38dp) |

No other numeric measurements appear in the rendered text.

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears in the rendered text of this page.

Relationship to the indeterminate circular progress indicator: the rendered spec text does **not** contain an explicit comparison, a "when to use which" rule, or a numeric design wait duration. The only supporting text on the page is the component description: "Loading indicators show the progress of a process for a **short wait time**". The page therefore places the component at short waits but gives no figure for that duration in the rendered text — recorded here as `—` rather than guessed.

---

## Snackbar

Source: https://m3.material.io/components/snackbar/specs

**Variants.** Snackbars show short updates about app processes at the bottom of the screen. The page presents one component with optional parts rather than named variants.

**Configurations** — M3 vs M3 Expressive availability, as a table with columns `Category | Configuration | M3 | M3 Expressive`.

The rendered page contains no `M3 / M3 Expressive` availability table for snackbars. It contains only the layout configuration list below; availability is therefore `—`.

The page does not group these configurations into categories, so `Category` is `—`.

| Category | Configuration | M3 | M3 Expressive |
| --- | --- | --- | --- |
| — | Single line | — | — |
| — | Single line with action | — | — |
| — | Two lines | — | — |
| — | Two lines with action | — | — |
| — | Two lines with longer action | — | — |

**Anatomy.** Numbered list as given (the page labels optional parts explicitly):

1. Container
2. Icon (optional close affordance)
3. Action (optional)
4. Supporting text

**Colour roles** — a table of `Element | Role`, transcribed exactly.

Snackbar colour roles used for light and dark schemes:

| Element | Role |
| --- | --- |
| Container | Inverse surface |
| Icon (optional close affordance) | Inverse on surface |
| Action (optional) | Inverse primary |
| Supporting text | Inverse on surface |

**States.** The token browser exposes these state folders, in order: `Enabled`, `Hovered`, `Focused`, `Pressed (ripple)`. No other state behaviour is described in the rendered text.

**Shape & morph.** No shape or corner radius value appears in the rendered text of this page.

Corner radii:

| Element | Corner radius |
| --- | --- |
| Container | — |

**Measurements** — a table of `Attribute | Value` per variant. The page has a "Measurements" heading and the lead-in "Snackbar padding and size measurements", but **no numeric attribute/value table follows it in the rendered text** — the measurements are presented only as a diagram.

The official snackbar diagram ("Diagram of snackbar indicating the four parts of its anatomy", retrieved 2026-09-12) was read directly. It is an anatomy-only drawing: four numbered callouts — 1 container, 2 icon (optional close affordance), 3 action, 4 supporting text — and no dimension lines, no numeric labels and no colour-role legend. It supplies no measurement values, so none are asserted here.

| Attribute | Value |
| --- | --- |
| — | — |

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears in the rendered text of this page. Colour values are implemented through design tokens.

---

## Tooltips

Source: https://m3.material.io/components/tooltips/specs

**Variants.** Tooltips display brief labels or messages. Two variants: **Plain tooltip** and **Rich tooltip**. The page instructs: "Select a component variant below to see its attributes, tokens, and values."

**Configurations** — M3 vs M3 Expressive availability, as a table with columns `Category | Configuration | M3 | M3 Expressive`.

The rendered page contains no `M3 / M3 Expressive` availability table for tooltips; availability is therefore `—`.

| Category | Configuration | M3 | M3 Expressive |
| --- | --- | --- | --- |
| — | Plain tooltip | — | — |
| — | Rich tooltip | — | — |

Rich tooltip configuration, as stated: "Rich tooltips can have a headline, body, and up to two buttons. The headline and number of buttons can be configured." The configurations shown are:

- Subhead, supporting text, and two buttons
- Subhead, supporting text, and one button
- Subhead and supporting text
- Supporting text and one button
- Supporting text and two buttons

**Anatomy.** Numbered list as given, per variant.

Plain tooltip:
1. Supporting text
2. Container

Rich tooltip:
1. Subhead
2. Container
3. Supporting text
4. Text button

**Colour roles** — a table of `Element | Role`, transcribed exactly.

Plain tooltip colour roles used for light and dark themes:

| Element | Role |
| --- | --- |
| Supporting text | Inverse on surface |
| Container | Inverse surface |

Rich tooltip colour roles used for light and dark themes:

| Element | Role |
| --- | --- |
| Subhead | On surface variant |
| Container | Surface container |
| Supporting text | On surface variant |
| Text button | Primary |

**States.** The token browser for the Plain tooltip exposes a single `Enabled` state folder. No other states are listed for either variant.

**Shape & morph.** No corner radius or morph value appears in the rendered text of either variant.

Corner radii:

| Element | Corner radius |
| --- | --- |
| Plain tooltip container | — |
| Rich tooltip container | — |

**Measurements** — a table of `Attribute | Value` per variant.

Plain tooltip (page label: "Plain tooltip padding and size measurements"):

| Attribute | Value |
| --- | --- |
| Container height | 24dp |
| Padding | 8dp |

Rich tooltip (page label: "Rich tooltip padding and size measurements"):

| Attribute | Value |
| --- | --- |
| Top padding | 12dp |
| Bottom padding | 8dp |
| Left and right padding | 16dp |

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears in the rendered text of this page. Rich tooltips support a configurable headline and up to two buttons.
