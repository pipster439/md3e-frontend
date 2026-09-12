# Action components — Material 3 / M3 Expressive specs

Transcribed from the individual component spec pages on m3.material.io; retrieved 2026-09-12.
A value shown as `—` was not present in the rendered text (the spec presents it only as a diagram); the source's `--` in availability tables is written "Not available".

---

## Buttons

Source: https://m3.material.io/components/buttons/specs

**Variants.** Two variants: the **default button** and the **toggle button**. The default button is available in both M3 and M3 Expressive; the toggle (selection) button does **not** exist in M3 and is new in M3 Expressive. Toggle buttons don't use the text style.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Default | Available | Available |
| Toggle (selection) | Not available | Available |

**Configurations** (M3 vs M3 Expressive)

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Size | Small (default) | Available | Available |
| Size | XS, M, L, XL | Not available | Available |
| Shape | Round (default) | Available | Available |
| Shape | Square | Not available | Available |
| Color | Elevated, filled (default), tonal, outlined, text | Available | Available |
| Small button padding | 24dp | Available | Not recommended. Use 16dp |
| Small button padding | 16dp | Not available | Available |

Expressive-only additions: the XS/M/L/XL sizes, the square shape, the toggle variant, and the 16dp small-button padding (which supersedes the M3 24dp).

**Anatomy.**

1. Container
2. Label text
3. Icon (optional)

**Colour roles.** Five built-in button colour styles: elevated, filled, tonal, outlined, and text. The default and toggle buttons use different colours. Toggle buttons don't use the text style.

| Style | State | Container | Content (icon & label) |
|---|---|---|---|
| Elevated | Default | Surface container low | Primary |
| Elevated | Toggle: unselected | Surface container low | Primary |
| Elevated | Toggle: selected | Primary | On primary |
| Filled | Default | Primary | On primary |
| Filled | Toggle: unselected | Surface container | On surface variant |
| Filled | Toggle: selected | Primary | On primary |
| Tonal | Default | Secondary container | On secondary container |
| Tonal | Toggle: unselected | Secondary container | On secondary container |
| Tonal | Toggle: selected | Secondary | On secondary |
| Outlined | Default | Outline variant (outline) | On surface variant |
| Outlined | Toggle: unselected | Outline variant (outline) | On surface variant |
| Outlined | Toggle: selected | Inverse surface | Inverse on surface |
| Text | Default | — (container invisible at rest) | Primary |
| Text | Toggle: unselected | — | — |
| Text | Toggle: selected | — | — |

The dump lists only an "icon & label" row for the text style (no container row), and lists `--` for both toggle text states — consistent with "there is no toggle text button".

**States.** Each style is documented with: Default, Enabled, Disabled, Hovered, Focused, Pressed, and (except text) Toggle.

- **Elevated button states** — the elevated button style has an elevation of **1 by default and 0 when disabled**.
- **Filled button states** — Default, Enabled, Disabled, Hovered, Focused, Pressed, Toggle.
- **Tonal button states** — Default, Enabled, Disabled, Hovered, Focused, Pressed, Toggle.
- **Outlined button states** — the outlined button's container fill is invisible at rest, but the opacity and state layers behave the same as other button styles when disabled, hovered, focused, or pressed. Toggle states: A. Unselected, B. Selected.
- **Text button style states** — the text button's container is invisible at rest, but the opacity and state layers behave the same as other button styles when disabled, hovered, focused, or pressed. **There is no toggle text button.** States listed: Enabled, Disabled, Hovered, Focused, Pressed.

**Shape & morph.**

- *Pressed state*: when pressed, buttons can morph to become more square. Both round and square buttons should have the **same pressed shape**. The corner radius value differs for each button size (A. Round button, B. Square button; Enabled → Hovered → Pressed).
- *When selected*: in addition to changing shape when pressed, toggle buttons also change the resting shape from **round (unselected) to square (selected)**. If the resting unselected shape is square, the selected shape should be round.

Corner sizes:

| | XS | S | M | L | XL |
|---|---|---|---|---|---|
| A. Round button | Full | Full | Full | Full | Full |
| B. Square button | 12dp | 12dp | 16dp | 28dp | 28dp |
| C. Pressed state | 8dp | 8dp | 12dp | 16dp | 16dp |

**Measurements.**

*Values in this subsection come from the official "Diagram of measurements of all button sizes" (retrieved 2026-09-12).*

Page section: "Padding and size measurements of each button size". The size groups are Extra small, Small, Medium, Large, Extra large, with diagram labels "Round button", "Button with icon" and "Square button". The per-size height, padding and icon figures come from that diagram:

| # | Size | Container height | Label padding (no icon) | Icon size | Leading padding | Icon-to-label gap | Trailing padding |
|---|---|---|---|---|---|---|---|
| 1 | Extra small | 32dp | 12dp | 20dp | 12dp | 4dp | 12dp |
| 2 | Small | 40dp | 16dp | 20dp | 16dp | 8dp | 16dp |
| 3 | Medium | 56dp | 24dp | 24dp | 24dp | 8dp | 24dp |
| 4 | Large | 96dp | 48dp | 32dp | 48dp | 12dp | 48dp |
| 5 | Extra large | 136dp | 64dp | 40dp | 64dp | 16dp | 64dp |

Text-backed values on this page:

| Attribute | Value |
|---|---|
| Small button padding (M3) | 24dp |
| Small button padding (M3 Expressive) | 16dp |
| Elevated button elevation (default) | 1 |
| Elevated button elevation (disabled) | 0 |
| Target area — extra small and small buttons | 48x48dp or larger (must, to be accessible) |

Corner radius by size (text-backed): see the corner-size table under *Shape & morph* — XS/S/M/L/XL round = Full; square = 12dp/12dp/16dp/28dp/28dp; pressed = 8dp/8dp/12dp/16dp/16dp.

**Notes.**

- "These colour roles were chosen to create design coherence and familiarity. Other colour roles can be used as long as the container and text have a 3:1 contrast ratio. For example, tertiary and on tertiary."
- "Small button padding: 24dp" is marked **Not recommended. Use 16dp** in M3 Expressive.
- Baseline tokens: the baseline button token sets ([Deprecated] Button - Elevated, with [Deprecated] Enabled / Disabled / Hovered / Focused / Pressed (ripple)) are deprecated in favour of the new token sets.

---

## Icon buttons

Source: https://m3.material.io/components/icon-buttons/specs

**Variants.** Two variants: the **default icon button** and the **toggle icon button**. Unlike buttons, the toggle (selection) variant exists in **both** M3 and M3 Expressive.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Default | Available | Available |
| Toggle (selection) | Available | Available |

**Configurations** (M3 vs M3 Expressive). The page groups them as five sizes, two shapes, four colour styles, three widths.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Size | Small (default) | Available | Available |
| Size | XS, M, L, XL | Not available | Available |
| Shape | Round (default) | Available | Available |
| Shape | Square | Not available | Available |
| Color | Filled (default), tonal, outlined, standard | Available | Available |
| Width | Default | Available | Available |
| Width | Narrow, wide | Not available | Available |

Expressive-only additions: XS/M/L/XL sizes, square shape, and the narrow/wide widths.

**Anatomy.** (Order as listed in the dump.)

1. Icon
2. Container

**Colour roles.** Four built-in colour styles: filled, tonal, outlined, and standard. Default and toggle buttons use different colour roles per style.

| Style | State | Container | Content (icon) |
|---|---|---|---|
| Filled | Default | Primary | On primary |
| Filled | Toggle: unselected | Surface container | On surface variant |
| Filled | Toggle: selected | Primary | On primary |
| Tonal | Default | Secondary container | On secondary container |
| Tonal | Toggle: unselected | Secondary container | On secondary container |
| Tonal | Toggle: selected | Secondary | On secondary |
| Outlined | Default | Outline variant (outline) | On surface variant |
| Outlined | Toggle: unselected | Outline variant (outline) | On surface variant |
| Outlined | Toggle: selected | Inverse surface | Inverse on surface |
| Standard | Default | — (no container row in dump) | On surface variant |
| Standard | Toggle: unselected | — (no container row in dump) | On surface variant |
| Standard | Toggle: selected | — (no container row in dump) | Primary |

The dump lists only an icon row for the standard style (no container row) — consistent with "the standard icon button's container is invisible at rest".

**States.** "State layers slightly change button colour. Disabled states have different base colours." Documented per style: Filled button states, Tonal button states, Outlined button states, Standard icon button states. Each lists Default (Enabled) / Disabled / Hovered / Focused / Pressed, plus Toggle (A: Unselected, B: Selected) for all four styles.

State-layer values, stated explicitly on the page:

| State | State layer |
|---|---|
| Disabled | 10% state layer |
| Hovered | 8% state layer |
| Focused | 10% state layer |
| Pressed | 10% state layer |

The standard icon button's container is invisible at rest, but visible when the state layer is applied.

**Shape & morph.**

- *Pressed state*: while pressed, icon buttons can morph to become more square. Both round and square icon buttons should have the **same pressed shape radius**. The corner radius value differs for each button size (A. Round, B. Square; Enabled → Hovered → Pressed).
- *When selected*: in addition to changing shape when pressed, toggle icon buttons also change the resting shape from round (unselected) to square (selected) **by default**. If the resting shape is square, the selected shape should be round.

Button corner radius:

| | XS | S | M | L | XL |
|---|---|---|---|---|---|
| A. Round button | Full | Full | Full | Full | Full |
| B. Square button | 12dp | 12dp | 16dp | 28dp | 28dp |
| C. Pressed state | 8dp | 8dp | 12dp | 16dp | 16dp |

**Measurements.**

*Values in this subsection come from the official "Diagram of 5 sizes of icon buttons in 4 widths" (retrieved 2026-09-12).*

Page groups: icon size, default width size, narrow width size, wide width size, target sizes, and the button corner radius. Sizes are A. Extra small, B. Small, C. Medium, D. Large, E. Extra large. The icon and width figures come from that diagram; container sizes are given as height × width (the narrow and wide variants keep the height and change only the width).

| Attribute | Extra small | Small | Medium | Large | Extra large |
|---|---|---|---|---|---|
| Icon size | 20dp | 24dp | 24dp | 32dp | 40dp |
| Container size — default width | 32×32dp | 40×40dp | 56×56dp | 96×96dp | 136×136dp |
| Container size — narrow width | 32×28dp | 40×32dp | 56×48dp | 96×64dp | 136×104dp |
| Container size — wide width | 32×40dp | 40×52dp | 56×72dp | 96×128dp | 136×184dp |

| Attribute | Value |
|---|---|
| Target size — extra small and small icon buttons | 48x48dp or larger (must, to be accessible) |
| Button corner radius (round) | Full at XS, S, M, L, XL |
| Button corner radius (square) | 12dp at XS, 12dp at S, 16dp at M, 28dp at L, 28dp at XL |
| Pressed state corner radius | 8dp at XS, 8dp at S, 12dp at M, 16dp at L, 16dp at XL |

**Notes.**

- "These colour roles were chosen to create design coherence and familiarity. Other colour roles can be used as long as the container and text have a 3:1 contrast ratio. For example, tertiary and on tertiary."
- Baseline tokens: "Filled, tonal, and outlined icon button tokens are now deprecated in favor of the new token sets. All other tokens are still available in the module at the top of the page."

---

## FAB (floating action button)

Source: https://m3.material.io/components/floating-action-button/specs

**Variants.** Three current variants plus a baseline one. The **medium FAB is new in M3 Expressive**; the **small FAB is not recommended** in M3 Expressive.

| Variant | M3 | M3 Expressive |
|---|---|---|
| FAB | Available | Available |
| Medium FAB | Not available | Available |
| Large FAB | Available | Available |
| Small FAB | Available | Not recommended. Use a larger size. |

Baseline variants: "The small FAB is still available, but no longer recommended. Jump to baseline specs" (1. Small FAB).

**Configurations** (M3 vs M3 Expressive). In the expressive update, the primary, secondary, and tertiary set colours were renamed to primary container, secondary container, and tertiary container to match the actual colour roles used. New primary, secondary, and tertiary colour styles were created to match the corresponding colour roles.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Color | Primary container, secondary container, tertiary container | Available as primary, secondary, tertiary | Available |
| Color | Primary. secondary, tertiary | Not available | Available |

**Anatomy.**

1. Container
2. Icon

**Colour roles.** FABs can use several combinations of colour and on-colour styles. The following mappings provide the same legibility and functionality, so the mapping depends on style alone:

| # | Container & on-container mapping |
|---|---|
| 1 | Primary container & On primary container (default) |
| 2 | Secondary container & On secondary container |
| 3 | Tertiary container & On tertiary container |
| 4 | Primary & On primary |
| 5 | Secondary & On secondary |
| 6 | Tertiary & On tertiary |

Baseline colour styles: surface FAB colour styles are still available, but no longer recommended (Surface FABs).

**States.** Enabled; Hovered (8% state layer) — elevation 4; Focused (10% state layer); Pressed (10% state layer).

"When using a non-default colour mapping for FABs, make sure the state layer colour is the same as the icon colour. For example, the state layer colour for the primary colour style should be `md.sys.color.primary`."

**Shape & morph.** Not a separate section on this page. The container shape is given as "Large rounding" in the token module (see Measurements). No pressed/selected morph behaviour is stated for FABs in the dump.

**Measurements.** The page section lists, for each size group, separate size measurements and padding measurements, but those are rendered as diagrams. The regular FAB values below come from the token module ("FAB - Size - Regular"); the dump emits the value line before its label.

*The per-size measurement and padding values below come from the official FAB measurement diagrams (retrieved 2026-09-12). In each padding diagram the pink regions along the right and bottom edges read 16dp, and the pink top-left corner region reads 16dp / 20dp / 28dp for the regular / medium / large FAB.*

| Attribute | Value |
|---|---|
| FAB container height (regular FAB) | 56dp |
| FAB container width (regular FAB) | 56dp |
| FAB icon size (regular FAB) | 24dp |
| FAB container shape (regular FAB) | Large rounding (label not present in dump) |
| FAB size measurements | Container 56×56dp; icon 24dp |
| FAB padding measurements | 16dp (top-left corner region also 16dp) |
| Medium FAB size measurements | Container 80×80dp; icon 28dp |
| Medium FAB padding measurements | 16dp along the right and bottom edges; top-left corner region 20dp |
| Large FAB size measurements | Container 96×96dp; icon 36dp |
| Large FAB padding measurements | 16dp along the right and bottom edges; top-left corner region 28dp |

**Notes.**

- The small FAB is still available but **no longer recommended**; use a larger size.
- Surface FABs (baseline colour styles) are still available but **no longer recommended**.
- Baseline tokens: "This only includes tokens for small and surface FABs, which are both no longer recommended. It doesn't include other colours, or large or regular FABs, since those are still currently used."

---

## Extended FAB

Source: https://m3.material.io/components/extended-fab/specs

**Variants.** Three current sizes, all **new in M3 Expressive**, plus the baseline extended FAB, which is not recommended.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Small extended FAB | Not available | Available |
| Medium extended FAB | Not available | Available |
| Large extended FAB | Not available | Available |
| Extended FAB (baseline) | Available | Not recommended. Use small extended FAB. |

Baseline note: "The baseline extended FAB is no longer recommended in the M3 expressive update. Use a small extended FAB; the type style was updated from **label large** to **title medium**, and the inner padding was reduced."

**Configurations.** The page has no "Configurations" section; the size groups are the variants above (Small, Medium, Large, baseline). M3 vs M3 Expressive availability is covered by the variant table.

**Anatomy.**

1. Container
2. Label text
3. Icon

**Colour roles.** Extended FABs can use several combinations of colour and on-colour styles; the following mappings provide the same level of contrast and functionality, so choose based on visual preference. Roles used for light and dark schemes:

| # | Mapping |
|---|---|
| 1 | Primary container & on primary container (default) |
| 2 | Secondary container & on secondary container |
| 3 | Tertiary container & on tertiary container |
| 4 | Primary & on primary |
| 5 | Secondary & on secondary |
| 6 | Tertiary & on tertiary |

Baseline colour styles: "Extended FABs should no longer use surface colour styles. They're still available, but not recommended." (Surface container FAB.)

**States.** Enabled; Hovered — elevation 4; Focused; Pressed.

"When using a non-default colour mapping for extended FABs, make sure the state layer colour is the same as the icon colour. For example, the state layer colour for primary mapping should be `md.sys.color.primary`."

**Shape & morph.** No separate morph section. The container shape is "Large rounding" for the current small extended FAB; the baseline extended FAB uses a 16dp corner radius. No pressed/selected morph behaviour is stated in the dump.

**Measurements.**

Current sizes — "Size and padding measurements of the small, medium, and large extended FABs". Values below come from the token module ("Extended FAB - Size - Small"); the dump emits the value line before its label. *The per-size size and padding values come from the official "Extended FAB padding and size measurements" diagram (retrieved 2026-09-12).*

| Attribute | Value |
|---|---|
| Small extended FAB container height | 56dp |
| Small extended FAB type style | Title Medium |
| Small extended FAB icon size | 24dp |
| Small extended FAB container shape | Large rounding (label not present in dump) |
| Small extended FAB leading space | 16dp |
| Small extended FAB icon label space | 8dp |
| Small extended FAB trailing space | 16dp |
| Extended FAB margins | 16dp |
| Medium extended FAB size measurements | Container height 80dp; icon 28dp |
| Medium extended FAB padding measurements | Leading 26dp; icon-to-label space 12dp; trailing 20dp |
| Large extended FAB size measurements | Container height 96dp; icon 36dp |
| Large extended FAB padding measurements | Leading 28dp; icon-to-label space 16dp; trailing 28dp |

Baseline extended FAB — section "Extended FAB height, width, and icon size"; "Extended FABs have a padding of 16dp". Baseline configurations: with icon, without icon.

| Attribute | Value |
|---|---|
| Container height | 56dp |
| Container width | Dynamic, 80dp min |
| Container shape | 16dp corner radius |
| Icon size | 24dp |
| Padding | 16dp |

**Notes.**

- The baseline extended FAB is **no longer recommended**; use a small extended FAB. The type style was updated from label large to title medium, and the inner padding was reduced.
- Extended FABs should no longer use **surface** colour styles; still available, but not recommended.
- Baseline token sets are organised by common tokens, then by surface and branded colour styles. Other colour styles like primary, secondary, and tertiary are still used by the latest extended FABs.

---

## FAB menu

Source: https://m3.material.io/components/fab-menu/specs

**Variants.** "There's one variant of FAB menu." It does not exist in M3 and is new in M3 Expressive.

| Variant | M3 | M3 Expressive |
|---|---|---|
| FAB menu | Not available | Available |

**Configurations** (M3 vs M3 Expressive). Three colour sets: primary, secondary, tertiary.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Color | Primary set, secondary set, tertiary set | Not available | Available |

**Anatomy.**

1. Close button
2. Menu item

"The FAB menu can have up to six items."

**Colour roles.** The dump lists the colour roles per set without labelling which is container and which is content, so they are transcribed in source order.

| Color set | Colour roles (as listed) |
|---|---|
| Primary | On primary container, Primary container, On primary, Primary |
| Secondary | On secondary container, Secondary container, On secondary, Secondary |
| Tertiary | On tertiary container, Tertiary container, On tertiary, Tertiary |

**States.** Documented separately for the two elements, in light and dark themes:

| Element | States |
|---|---|
| Close button | Enabled, Hovered, Focused, Pressed |
| Menu item | Enabled, Hovered, Focused, Pressed |

**Shape & morph.** No shape or morph section and no corner-radius values in the dump for this component.

**Measurements.**

*The diagram values below come from the official "FAB menu size measurements" diagram (retrieved 2026-09-12).*

| Attribute | Value |
|---|---|
| FAB menu item measurements | Same as the **medium button** specs |
| Close button size | 56dp (should always be) |
| FAB margins | 16dp (the FAB should always have 16dp margins) |
| Gap between FAB and menu | Can vary; 4dp recommended |
| Medium FAB placement margins | 16dp |
| Large FAB placement margins | 16dp |
| FAB menu size measurements | Menu item height 56dp; leading padding 24dp; icon-to-label gap 8dp; trailing padding 24dp; gap between items 4dp (a further 8dp is marked below the lower item); label type style Title Medium; close button 56dp |

Placement behaviour stated on the page: the FAB menu animates from the **top trailing edge** of the FAB to ensure a smooth animation; the close button and FAB share the **top trailing corner as an anchor** and appear in the same place; larger FABs place the FAB menu slightly higher, with larger margins underneath; for the medium FAB placement the close button is placed higher to align with the top of the medium FAB (same for the large FAB).

On web, the FAB menu opens from the FAB and inherits its states and specs from the **baseline menu** component. Spacing and interaction on web: Enabled, Hovered, Selected.

**Notes.**

- The FAB menu can have **up to six items**.
- The close button should **always be 56dp**.
- The FAB should **always** have 16dp margins.
- Web implementation inherits from the baseline menu component, not from this spec.

---

## Split button

Source: https://m3.material.io/components/split-button/specs

**Variants.** One variant — the split button. It does not exist in M3 and is new in M3 Expressive.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Split button | Not available | Available |

**Configurations.** Colour configurations: elevated, filled, tonal, outlined. Size configurations: XS, S, M, L, XL.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Size | XS, S, M, L, XL | Not available | Available |
| Color | Elevated, filled, tonal, outlined | Not available | Available |

**Anatomy.**

1. Leading button
2. Icon
3. Label text
4. Trailing button

"The leading button in split buttons can have an icon, label text, or both. The trailing button should always have a menu icon." Leading-button configurations shown: label + icon, label, icon.

**Colour roles.** "Split buttons use the same colour schemes as standard buttons. However, unlike toggle buttons, the split button colour doesn't change when selected — only a state layer is applied." Colour styles: Elevated, Filled, Tonal, Outlined (A: Unselected, B: Selected trailing icon). "Split buttons use the same colours and state layers as buttons... Go to buttons for more details."

| Style | Colour source |
|---|---|
| Elevated | Same colours and state layers as buttons (see Buttons colour roles) |
| Filled | Same colours and state layers as buttons |
| Tonal | Same colours and state layers as buttons |
| Outlined | Same colours and state layers as buttons |

Because the page defers to the Buttons token module, no per-role colour values are given here in the dump.

**States.** "Split button states use the same colours and state layers as buttons and icon buttons. Go to those specs for details."

- *Leading button shape*: the inner corners change shape for hovered, focused, and pressed states. States shown: Enabled, Disabled, Hovered, Focused, Pressed, pressed with focus.
- *Trailing button shape*: the inner corners change shape for hovered, focused, and pressed states, and the **icon becomes centred when selected**. States shown: Enabled, Disabled, Hovered, Focused, Pressed, pressed with focus, Selected, selected with focus.

**Shape & morph.** The inner corners change shape on hover/focus/press; the trailing button's inner corner also changes when selected (see the XS values in Measurements). The space between the two buttons is always 2dp.

**Measurements.**

Page note: "Text and icons are optically centred when the buttons are asymmetrical. They're centred normally when symmetrical."

Token module ("Split button - Size - Xsmall"); the dump emits the value line before its label.

| Attribute | Value |
|---|---|
| Container height (xsmall) | 32dp |
| Between space (xsmall) | 2dp |
| Shape (xsmall) | Fully rounded (label not present in dump) |
| Inner corner size (xsmall) | 4dp |
| Outer corner size (xsmall) | 50% |
| Leading button leading space (xsmall) | 12dp |
| Leading button trailing space (xsmall) | 10dp |
| Trailing button icon size (xsmall) | 22dp |
| Trailing button leading space (xsmall) | 13dp |
| Trailing button trailing space (xsmall) | 13dp |
| Inner corner hovered size (xsmall) | 8dp |
| Inner corner pressed size (xsmall) | 8dp |
| Trailing button inner corner selected size (xsmall) | 50% |

Menu icon offset when unselected:

| Size | Offset from centre |
|---|---|
| XS | -1dp |
| S | -1dp |
| M | -2dp |
| L | -3dp |
| XL | -6dp |

Inner corner radius by size ("The inner corner radius changes depending on button sizing. The space should always be 2dp."):

| Size | Inner corner radius |
|---|---|
| Extra small | 4dp |
| Small | 4dp |
| Medium | 4dp |
| Large | 8dp |
| Extra large | 12dp |

**Notes.**

- "Unlike toggle buttons, the split button colour doesn't change when selected — only a state layer is applied."
- "The trailing button should always have a menu icon."
- "The space should always be 2dp."
- Values exist for the **Xsmall** size in the dump; the other sizes (S, M, L, XL) are reachable only through the token-set menu and are not present in the rendered text.

---

## Button groups

Source: https://m3.material.io/components/button-groups/specs

**Variants.** Two variants. The standard button group does not exist in M3. The connected button group's M3 equivalent is the segmented button.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Standard button group | Not available | Available |
| Connected button group | Available as segmented button | Available |

**Configurations** (M3 vs M3 Expressive). Configurations for both variants: extra small, small, medium, large, extra large; single-select and multi-select; round and square.

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Size | XS, S, M, L, XL | Not available | Available |
| Default shape | Round, square | Not available | Available |
| Selection | Single-select, multi-select, selection-required | Available as segmented button | Available |

**Anatomy.**

1. Container

"Button groups are invisible containers that add padding between buttons and modify button shape. They don't contain any buttons by default."

Common layouts: label buttons; label buttons and icon buttons; extra small icon buttons; large icon buttons. "Mix and match buttons and icon buttons for different scenarios."

**Colour roles.** "Button groups have **no colour properties**. They can use the default button or toggle button colour styles, like filled, tonal, and outlined. **Avoid using standard icon buttons or text buttons, as they have no container treatment.**"

Styles usable: Filled, Tonal, Outlined, Elevated.

**States.** Documented per variant.

- *Standard button group*: when a button is pressed, standard button groups modify the width and shape of that button **and adjacent buttons**. States shown: Enabled, Disabled, Hovered, Focused, Pressed. "When a toggle button is selected in a standard button group, its shape should change between square and round. The colour should change according to the button specs."
- *Connected button group*: "Connected button groups have different shape changes than standard button groups. Selecting a button does **not** affect adjacent buttons." Unselected states: Enabled, Disabled, Hovered, Focused, Pressed. Selected states: Enabled, Hovered, Focused, Pressed.

**Selection & activation.**

- Standard button groups add interaction between adjacent buttons when a button is selected or activated. This changes the width, shape, and padding of the selected or activated button, which adjusts the width of buttons directly next to it — "a selected button changes shape, and briefly changes the width of itself and adjacent buttons".
- Connected button groups don't add any interaction between buttons when selected or activated. They only affect the shape of the button being selected or activated — "a selected button changes shape without affecting adjacent buttons".

**Shape & morph.** Standard button groups morph the selected/activated button **and its neighbours**; connected button groups change only the selected button's shape (see Selection & activation, and the corner sizes below).

**Measurements.**

Standard button group — "Standard groups apply padding between all buttons. The amount of padding changes based on button size to ensure a minimum accessible target size of 48dp."

| Attribute | Value |
|---|---|
| Inner padding — XS | 18dp |
| Inner padding — S | 12dp |
| Inner padding — M | 8dp |
| Inner padding — L | 8dp |
| Inner padding — XL | 8dp |

Token module ("Button group standard - Size - Xsmall"):

| Attribute | Value |
|---|---|
| Container height (xsmall) | 32dp |
| Between space (xsmall) | 18dp |

Connected button group — "For all connected button groups, use 2dp padding. This provides visual consistency at scale."

| Attribute | Value |
|---|---|
| Inner padding — all sizes | 2dp |
| Outer shape — round connected group | Fully round |
| Outer shape corner size — XS | 4dp |
| Outer shape corner size — S | 8dp |
| Outer shape corner size — M | 8dp |
| Outer shape corner size — L | 16dp |
| Outer shape corner size — XL | 20dp |
| Inner shape — round connected group | Remains square |
| Inner shape corner size — XS | 4dp |
| Inner shape corner size — S | 8dp |
| Inner shape corner size — M | 8dp |
| Inner shape corner size — L | 16dp |
| Inner shape corner size — XL | 20dp |
| Inner padding — square connected group, all sizes | 2dp |
| Square connected group outer corner size — XS | 4dp |
| Square connected group outer corner size — S | 8dp |
| Square connected group outer corner size — M | 8dp |
| Square connected group outer corner size — L | 16dp |
| Square connected group outer corner size — XL | 20dp |

Minimum widths: "Extra small and small connected button groups have 48dp target areas and a minimum width of 48dp."

Density: "Button groups adapt to density of the buttons inside... Button groups adapt to the height of the buttons inside, including when density is applied."

**Notes.**

- "Button groups have no colour properties."
- "Avoid using standard icon buttons or text buttons, as they have no container treatment."
- Connected button groups should use 2dp padding at every size for visual consistency at scale.
- Standard group padding varies by size to keep a minimum accessible target size of 48dp.

---

## Segmented buttons

Source: https://m3.material.io/components/segmented-buttons/specs

**Variants.** Not present as a section on this page. The page carries a deprecation note instead: "Segmented buttons are **no longer recommended** in the Material 3 expressive update. For those who have updated, use the **connected button group** instead, which has mostly the same functionality but with an updated visual design."

**Configurations.** Not present on this page. (The replacement, the connected button group, is documented under Button groups.)

**Anatomy.**

1. Container
2. Icon (optional for unselected state)
3. Label text

**Colour roles.** "Segmented button colour roles used for light and dark schemes:"

| Colour role (as listed) |
|---|
| On surface |
| Outline |
| Secondary container |
| On secondary container |

The dump gives no explicit container/content pairing for these four roles.

**States.** Unselected button states: Enabled, Disabled, Hovered, Focused, Pressed. Selected button states: Selected, Hovered on selected, Focused on selected, Pressed on selected.

**Shape & morph.** No shape/morph section and no corner-radius values in the dump. The only shape-adjacent values are the outline width and the density behaviour (see Measurements).

**Measurements.** "Padding and container size" and "Target size". A single Attribute | Value table is given verbatim in the dump.

| Attribute | Value |
|---|---|
| Container width | Dynamic based on labels |
| Segment width | Container width / total segments (Example: 1/3) |
| Height | 40dp |
| Outline width | 1dp |
| Label alignment | Center |
| Left/right padding | Min 12dp |
| Padding between elements | 8dp |
| Target size | 48dp |

Density: "Density can be used in denser UIs where space is limited. Density is only applied to the height. Each step down in density removes 4dp from the height."

**Notes.**

- **Deprecated:** "Segmented buttons are no longer recommended in the Material 3 expressive update. For those who have updated, use the connected button group instead, which has mostly the same functionality but with an updated visual design."
- Density affects **height only**; each step down removes 4dp.
