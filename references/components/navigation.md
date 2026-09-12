# Navigation components — Material 3 / M3 Expressive specs

Transcribed from the individual component spec pages on m3.material.io (app bars, toolbars, navigation bar, navigation rail, navigation drawer, tabs, search); retrieved 2026-09-12.
A value shown as `—` was not present in the rendered text (the spec presents it only as a diagram); the source's `--` in availability tables is written "Not available".

**Expressive changes to flag first:**

- **Toolbars are new in M3 Expressive** (docked and floating); there is no toolbar in M3.
- **The bottom app bar is deprecated in favour of toolbars** — explicitly, "It should be replaced with the docked toolbar, which is very similar and more flexible."
- The baseline (M3) medium and large app bars, the baseline navigation bar, the baseline navigation rail, and the navigation drawer are all **no longer recommended** in M3 Expressive.
- The baseline (divided) search style is **not recommended**; use the contained style.

---

## App bars

Source: https://m3.material.io/components/app-bars/specs

"App bars are placed at the top of the screen to help people navigate through a product."

**Variants.** Expressive introduces the **search app bar** and the **medium flexible** and **large flexible** app bars, and merges center-aligned into small. The baseline M3 medium and large app bars are no longer recommended: "The baseline M3 medium and large app bars are no longer recommended in M3 Expressive, and should be replaced with medium flexible and large flexible app bars, which are similar visually, but have multi-line support, a shorter height, and can contain a wide variety of elements, like images."

| Variant | M3 | M3 Expressive |
|---|---|---|
| Search app bar | Not available | Available |
| Small | Available | Available |
| Center-aligned | Available | Merged into small. Use centered-text configuration. |
| Medium (baseline) | Available | Not recommended. Use medium flexible |
| Medium flexible | Not available | Available |
| Large (baseline) | Available | Not recommended. Use large flexible |
| Large flexible | Not available | Available |

**Configurations** — text alignment: "Text labels, including supporting text, can be aligned to the leading edge or centered".

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Text alignment | Leading edge (default) | Available | Available |
| Text alignment | Centered | Not available | Available |

**Anatomy.**

1. Container
2. Leading button
3. Trailing elements
4. Headline
5. Subtitle

App bars can be customized to include: an image or logo, a subtitle, a filled icon button. "Avoid customizing the size of the heading and subtitle, or adding too many actions."

Search app bar anatomy (the search app bar can include trailing actions inside and outside the search bar; when the search bar is selected, it should open the search view component):

1. Container
2. Leading icon button
3. Hinted search text
4. Trailing icon or avatar
5. Search container

Search app bar element arrangements:

- A leading element and a trailing element outside search
- A leading element, a trailing element inside search, and a trailing element outside search
- A leading element and two trailing elements outside search

Other anatomies:

- **Image** — "An image can be placed in the app bar. In small app bars, this can replace the label text."
- **Filled trailing icon button** — "The app bar's trailing icon buttons can be replaced with a single, primary, or tonal filled icon button in default or wide sizes."
- **Subtitle** — "The medium flexible and large flexible app bars hug the text contents, so they are taller when a subtitle is visible" (Small, Small with subtitle, Medium flexible, Medium flexible with subtitle, Large flexible, Large flexible with subtitle).

Baseline medium and large app bars have the same elements: Container, Leading button, Trailing icons, Headline.

**Colour roles.** "All app bars share the same color roles. On scroll, the container changes color to surface container."

App bar colour roles used for light and dark themes — the rendered text lists the roles in this order but does not name the element each one applies to (that pairing is diagram-only), so `Element` is `—` except where the source names the state:

| Element | Role |
|---|---|
| — | Surface |
| — | On surface |
| — | On surface variant |
| — | On surface |
| — | On surface variant |
| Container (on scroll) | Surface container (on scroll) |

Search app bar colour roles used for light and dark themes (same caveat — no element names in the rendered text):

| Element | Role |
|---|---|
| — | Surface |
| — | On surface variant |
| — | On surface variant |
| — | On surface variant |
| — | Surface container |
| — | Surface container |
| — | Surface container highest |

Medium (baseline) top app bar colour roles used for light and dark schemes (same caveat):

| Element | Role |
|---|---|
| — | Surface |
| — | On surface |
| — | On surface |
| — | On surface variant |

Token values appearing in the rendered text:

| Attribute | Value |
|---|---|
| Search view container surface tint layer color (Search – View, Default, Light) | #6750A4 |

Token sets on this page: **App bar – Common** (organised into Color, Spacing, Shape, Size) and size-specific sets. "The default search component tokens are used in the search app bar."

**States.** Scroll states: **Flat** and **On scroll**. "The app bar changes color when flat or on scroll. The search bar can also change color on scroll." On scroll the container changes colour to surface container.

**Shape & morph.** The rendered text states no corner radii or morph behaviour for app bars; the shape values live in the App bar – Common **Shape** token folder and are not written out in the text. Rounding/expansion behaviour is therefore `—`.

**Measurements.**

Values below marked with the official measurement diagram (retrieved 2026-09-12) were read from that diagram; the remaining diagram-only values stay `—`.

Diagram groups on this page: "Search app bar padding and size measurements", "Small app bar padding and size measurements", "Medium flexible app bar padding and size measurements", "Large flexible app bar padding and size measurements".

| Variant / size group | Attribute | Value |
|---|---|---|
| Search app bar | Padding and size | Height 64dp; leading and trailing icon buttons 48dp; 4dp before the leading icon button and 4dp after a trailing icon button outside the search bar; 8dp between the leading icon button and the search bar; 8dp between the search bar and a trailing icon button outside it. Configuration with a trailing action inside the search bar: search bar leading padding 24dp; 4dp from that trailing icon button to the search bar's trailing edge; 8dp to the next (outside) trailing icon button; 48dp icon buttons; 4dp trailing padding (from the "Search app bar size and padding measurements" diagram) |
| Small app bar | Padding and size | Leading padding 4dp; trailing padding 4dp; leading and trailing icon buttons 48dp; 4dp between the leading icon button and the headline; 4dp between the headline and the trailing icon buttons; icon 24dp; trailing avatar 32dp inside its 48dp icon button (from the "Small app bar size and padding measurements" diagram) |
| Medium flexible app bar | Padding and size | — |
| Large flexible app bar | Padding and size | — |

Baseline app bars — text-backed values from the "App bar – Size – Medium (baseline)" token set:

| Variant / size group | Attribute | Value |
|---|---|---|
| Medium app bar (baseline) | Container height | 112dp |
| Medium app bar (baseline) | Icon button size | 24dp |
| Medium app bar (baseline) | Headline text style | Headline Small |
| Medium app bar (baseline) | Label text style | Label Large |
| Medium app bar (baseline) | Padding and size (diagram "Medium app bar padding and size measurements") | — |
| Large app bar (baseline) | Padding and size (diagram "Large app bar padding and size measurements") | — |

**Notes.**

- "The baseline M3 medium and large app bars are no longer recommended in M3 Expressive, and should be replaced with medium flexible and large flexible app bars."
- "The medium and large app bars are no longer recommended in M3 Expressive. Use the medium flexible and large flexible app bars in their place."
- "Avoid customizing the size of the heading and subtitle, or adding too many actions."
- "The search app bar can include trailing actions inside and outside the search bar. When the search bar is selected, it should open the search view component."
- Center-aligned is no longer a separate variant: it is "Merged into small. Use centered-text configuration."
- The M3 medium baseline colour roles are a separate set from the shared app bar roles (see the Medium (baseline) colour table above).

---

## Toolbars

Source: https://m3.material.io/components/toolbars/specs

"Toolbars display frequently used actions relevant to the current page"

**Variants.** Toolbars are **new in M3 Expressive** — neither docked nor floating exists in M3. The baseline **bottom app bar** is not recommended and is replaced by the docked toolbar: "The baseline bottom app bar is no longer recommended. It should be replaced with the docked toolbar, which is very similar and more flexible."

| Variant | M3 | M3 Expressive |
|---|---|---|
| Docked toolbar | Not available | Available |
| Floating toolbar | Not available | Available |
| Bottom app bar | Available | Not recommended. Use docked toolbar. |

**Configurations.**

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Color | Standard (default) | Available as bottom app bar | Available |
| Color | Vibrant | Not available | Available |
| Floating toolbar layout | Horizontal (default) | Not available | Available |
| Floating toolbar layout | Vertical | Not available | Available |
| Other elements | With FAB | Available as bottom app bar | Available* |

Rendered variants on the page: standard and vibrant toolbars, vertical floating toolbar, floating toolbar with FAB.

**Anatomy.**

1. Container
2. Placed components

"When configuring a toolbar, think of it as a container with several slots. Each slot can be a different element. The most common elements are icon buttons, buttons, and text fields." A toolbar is essentially a container with configurable slots (**flexibility & slots**).

Baseline bottom app bar anatomy: Container.

**Colour roles.** Colour values are implemented through design tokens.

Standard — standard colour schemes and icon button types:

| Element | Role |
|---|---|
| Toolbar container | Surface container |
| Filled button | Primary, On primary |
| Toggle tonal button | Secondary container, On secondary container |
| Standard button | Primary |

Vibrant — vibrant colour scheme and icon button types:

| Element | Role |
|---|---|
| Toolbar container | Primary container |
| Filled button | Primary, On primary |
| Toggle tonal button | Surface container, On surface |
| Standard button | On primary container |

Baseline bottom app bar colour role used for light and dark themes:

| Element | Role |
|---|---|
| Container | Surface container |

Colour token sets on this page: **Toolbar – Color – Standard** (Default, Light) with states Enabled / Disabled / Hovered / Focused / Pressed, and **Bottom app bar (baseline)** with Enabled.

**States.** The toolbar token set is documented with **Enabled, Disabled, Hovered, Focused, Pressed** (from the Toolbar – Color – Standard token menu). No further state behaviour is written out in the rendered text.

**Shape & morph.** The rendered text states no shape or morph behaviour for toolbars or the bottom app bar. `—`.

**Measurements.** "By default all toolbars are 64dp high, center-aligned, have equal padding between items, and have a minimum outside padding of 16dp."

Values below marked with the official measurement diagram (retrieved 2026-09-12) were read from that diagram; the remaining diagram-only values stay `—`.

| Variant / size group | Attribute | Value |
|---|---|---|
| All toolbars (default) | Height | 64dp |
| All toolbars (default) | Alignment | Center-aligned |
| All toolbars (default) | Padding between items | 32dp (from the "Default internal padding of a docked toolbar" diagram) |
| All toolbars (default) | Minimum outside padding | 16dp |
| Docked toolbar | Default margins and padding | — (diagram "Default margins and padding") |
| Docked toolbar | Default internal padding (diagram "Default internal padding of a docked toolbar") | 16dp at the leading and trailing ends, 32dp between items; the between-item padding can instead be set to Fill |
| Docked toolbar | Margins and padding with leading, middle, and trailing content | — (diagram) |
| Docked toolbar | Center-aligned configuration, padding between items | 8dp |
| Docked toolbar | Left and right alignment configuration | — (diagram "Left and right alignment") |
| Floating toolbar | Default padding | — (diagram "Default padding of floating toolbar") |
| Floating toolbar | Size and padding measurements | — (diagram "Floating toolbar size and padding measurements") |
| Floating toolbar | Margins | — (diagram "Floating toolbar margins") |
| Bottom app bar (baseline) | Padding and size | — (diagram "Bottom app bar padding and size measurements") |

Bottom app bar (baseline) common layouts: icon buttons and FAB; icon buttons and no FAB.

**Notes.**

- "The baseline bottom app bar is no longer recommended. It should be replaced with the docked toolbar, which is very similar and more flexible." In the availability table the bottom app bar is marked **Not recommended. Use docked toolbar.**
- Toolbars (docked and floating) are **new in M3 Expressive**; M3 provides only "Available as bottom app bar" for the standard colour and for the with-FAB configuration.
- "Implementation differs per platform. On Jetpack Compose, the floating toolbar is a separate component from the docked toolbar and bottom app bar."
- "*Implementation differs per platform. On Jetpack Compose, floating toolbar with FAB is fully supported. On other platforms, each component needs to be added separately."
- Bottom app bar tokens are in one token set.
- When configuring a toolbar, think of it as a container with several slots; the most common elements are icon buttons, buttons, and text fields.

---

## Navigation bar

Source: https://m3.material.io/components/navigation-bar/specs

"Navigation bars let people switch between UI views on smaller devices"

**Variants.** The **flexible navigation bar** is new in M3 Expressive; the baseline navigation bar is not recommended: "The baseline nav bar is no longer recommended, and should be replaced by the flexible nav bar, which is shorter and supports horizontal navigation items in medium windows."

| Variant | M3 | M3 Expressive |
|---|---|---|
| Flexible navigation bar | Not available | Available |
| Navigation bar | Available | Not recommended. Use flexible navigation bar. |

**Configurations.** "In compact windows, navigation bars use vertical items. In medium windows, navigation bars should use horizontal items."

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Navigation item layout | Vertical (default) | Available | Available |
| Navigation item layout | Horizontal | Not available | Available |

**Anatomy.**

1. Container
2. Icon
3. Label text
4. Active indicator
5. Small badge (optional)
6. Large badge (optional)
7. Large badge label

Baseline navigation bar anatomy: Container, Icon, Label text, Active indicator, Small badge, Large badge, Large badge label.

**Colour roles.** Navigation bar colour roles used for light and dark schemes — the rendered text lists the roles in order without naming the element each applies to (that pairing is diagram-only), so `Element` is `—`:

| Element | Role |
|---|---|
| — | Surface container |
| — | On-secondary container |
| — | Secondary |
| — | Secondary container |
| — | On-surface variant |
| — | On-surface variant |

"For badge color roles, go to badge specs."

Baseline navigation bar colour roles used for light and dark schemes (same caveat):

| Element | Role |
|---|---|
| — | Surface |
| — | On secondary container |
| — | On surface |
| — | Secondary container |
| — | On surface variant |
| — | On surface variant |

Token sets on this page: **Nav bar – Common** (Color, Nav item, Container). Baseline tokens are in **Navigation bar (baseline)**, Default/ Light, with an Enabled state layer.

**States.** "States are visual representations used to communicate the status of a component or an interactive element."

- Enabled
- Hovered (8% state layer)
- Focused (10% state layer)
- Pressed (10% state layer)

Baseline navigation bar states: Enabled, Hovered, Focused, Pressed (no state-layer percentages given in the rendered text).

**Shape & morph.** The rendered text states no corner radii or morph behaviour for the navigation bar. `—`.

**Measurements.**

Values below marked with the official measurement diagram (retrieved 2026-09-12) were read from that diagram; the remaining diagram-only values stay `—`.

"The navigation bar stretches the full window width."

"Vertical navigation items dynamically change width to equally fit the container. Horizontal navigation items have a fixed width, so extra space is added to the ends of the navigation bar instead."

| Variant / size group | Attribute | Value |
|---|---|---|
| Navigation bar | Width | Full window width (stretches the full window width) |
| Navigation bar | Padding and size — vertical destinations | 6dp container padding above the active indicator; active indicator 56dp × 32dp with a 16dp corner radius; 4dp between the active indicator and the label; 6dp container padding below the label (from the "Navigation bar padding and size measurements" diagram) |
| Navigation bar | Padding and size — horizontal destinations | 12dp container padding above and below the destination; destination height 40dp with a 20dp corner radius; 4dp between the icon and the label (from the "Navigation bar padding and size measurements" diagram) |
| Flex-vertical items | Width | Dynamically changes to equally fit the container (no dp value in rendered text) |
| Flex-horizontal items | Width | Fixed; extra space is added to the ends of the navigation bar (no dp value in rendered text) |
| Navigation bar — compact and medium windows | Width and margins | — (diagram "Navigation bar width and margins for compact and medium windows") |
| Vertical navigation item | Margin from window edge | — |
| Horizontal navigation item | Margin from window edge | — |
| Baseline navigation bar | Padding and size | Active indicator 64dp × 32dp with a 16dp corner radius; icon 24dp; large badge 16dp; small badge 6dp; container padding 12dp above the active indicator, 4dp between the active indicator and the label, 16dp below the label (from the "Baseline navigation bar padding and size measurements" diagram) |
| Baseline navigation bar | Target size and margins | — (diagram "Navigation bar target size and margins") |

Baseline configurations shown: 3 destinations, 4 destinations, 5 destinations (all diagram-only).

**Notes.**

- "The baseline nav bar is no longer recommended, and should be replaced by the flexible nav bar, which is shorter and supports horizontal navigation items in medium windows." It is marked **Not recommended. Use flexible navigation bar.**
- "In compact windows, navigation bars use vertical items. In medium windows, navigation bars should use horizontal items." This is stated as a should, and only M3 Expressive offers the horizontal configuration.
- "For badge color roles, go to badge specs."
- The flexible navigation bar is **new in M3 Expressive**; M3 has only the baseline navigation bar.

---

## Navigation rail

Source: https://m3.material.io/components/navigation-rail/specs

"Navigation rails let people switch between UI views on mid-sized devices"

**Variants.** The **collapsed** and **expanded** navigation rails are new in M3 Expressive. "The baseline navigation rail is no longer recommended, and should be replaced by the collapsed navigation rail."

| Variant | M3 | M3 Expressive |
|---|---|---|
| Collapsed navigation rail | Not available | Available |
| Expanded navigation rail | Not available | Available |
| Navigation rail (baseline) | Available | Not recommended. Use collapsed navigation rail. |

**Configurations.**

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Expanded layout | Standard (default) | Available as navigation drawer | Available |
| Expanded layout | Modal | Available as navigation drawer | Available |
| Expanded behavior | Hide when collapsed | Not available | Available |

**Anatomy.** Collapsed and expanded navigation rail elements:

1. Container
2. Menu (optional)
3. FAB or Extended FAB (optional)
4. Icon
5. Active indicator
6. Label text
7. Large badge (optional)
8. Large badge label (optional)
9. Small badge (optional)

Baseline navigation rail: Container, Menu icon (optional), Icon, Active indicator, Label text, Large badge label (optional), Large badge (optional), Badge (optional).

**Colour roles.** Navigation rail colour roles used for light and dark schemes — the rendered text lists the roles in order without naming the element each applies to (that pairing is diagram-only), so `Element` is `—`:

| Element | Role |
|---|---|
| — | Surface container (optional) |
| — | On secondary container |
| — | Secondary container |
| — | Secondary (vertical), On secondary container (horizontal) |
| — | On surface variant |
| — | On surface variant |
| — | Error |
| — | On error |
| — | Error |

Baseline navigation rail colour roles used for light and dark themes (same caveat):

| Element | Role |
|---|---|
| — | On secondary container |
| — | Secondary container |
| — | On surface |
| — | On surface variant |
| — | On surface variant |
| — | Error |
| — | On error |
| — | Error |

Token set on this page: **Nav rail – Common** (Default, Light; states Enabled / Hovered / Focused / Pressed). Baseline set: **Navigation rail (baseline)** with Enabled / Hovered / Focused / Pressed (ripple).

**States.** "States are visual representations used to communicate the status of a component or an interactive element."

"The navigation item's target area always spans the full width of the nav rail, even if the item container hugs its contents."

- Enabled
- Hovered
- Focused
- Pressed

Baseline navigation rail states are given per destination: Enabled (on active destination), Hovered (on active destination), Focused (on active destination), Pressed (on active destination), Enabled (on inactive destination), Hovered (on inactive destination), Focused (on inactive destination), Pressed (on inactive destination).

**Shape & morph.** The rendered text states no corner radii or morph behaviour for the navigation rail. `—`.

**Measurements.**

The values below were read from the official measurement diagram for the expanded and collapsed navigation rails (retrieved 2026-09-12); the baseline rail diagrams were not available, so those rows stay `—`.

| Variant / size group | Attribute | Value |
|---|---|---|
| Collapsed navigation rail | Width | 96dp |
| Collapsed navigation rail | Icon | 24dp |
| Collapsed navigation rail | Vertical spacing between elements (from the "Padding and measurements for expanded and collapsed navigation rails" diagram) | 4dp below the active destination's label; 8dp between an icon and its label; 6dp below a destination's label |
| Expanded navigation rail | Width | 220–360dp |
| Expanded navigation rail | Destination height | 56dp |
| Expanded navigation rail | Leading offsets | 36dp from the rail's leading edge to the active indicator's leading edge; 16dp from the destination's leading edge to the active indicator |
| Expanded navigation rail | Section header | 12dp above, 8dp below |
| Expanded navigation rail | Icon | 24dp |
| Navigation rail (baseline) | Size | — (diagram "Navigation rail size measurements") |
| Navigation rail (baseline) | Padding and margin | — (diagram "Navigation rail padding and margin measurements") |

Common layouts (all diagram-only, no values in the rendered text): three navigation items; three navigation items with a menu; three navigation items with a FAB; three navigation items with a menu and FAB.

Configurations — "Common arrangements of elements within a navigation rail": with a menu; with a FAB; with menu and FAB, without labels; all destinations with text labels; with menu, FAB, and label text for all destinations.

**Notes.**

- "The baseline navigation rail is no longer recommended, and should be replaced by the collapsed navigation rail." The baseline is also labelled "The baseline navigation rail is no longer recommended" and marked **Not recommended. Use collapsed navigation rail.**
- Expanded rails offer two layouts, both of which M3 could only express "Available as navigation drawer" — the expanded rail is the M3 Expressive replacement for the navigation drawer.
- "Expanded behavior: Hide when collapsed" is new — `Not available` in M3.
- "The navigation item's target area always spans the full width of the nav rail, even if the item container hugs its contents."
- The rail distinguishes label colour by item orientation: `Secondary (vertical), On secondary container (horizontal)`.

---

## Navigation drawer

Source: https://m3.material.io/components/navigation-drawer/specs

"Navigation drawers let people switch between UI views on larger devices"

**Variants.** The page defines no variant table. The whole component is deprecated in the Expressive update: "The navigation drawer is no longer recommended in the Material 3 Expressive update. For those who have updated, use an expanded navigation rail, which has mostly the same functionality of the navigation drawer and adapts better across breakpoints."

| Variant | M3 | M3 Expressive |
|---|---|---|
| Navigation drawer | Available | Not recommended. Use expanded navigation rail. |

**Configurations.** No configurations table exists on this page in the rendered text. Measurement groups imply two forms: **Standard navigation drawer** and **Modal navigation drawer**. `—`

**Anatomy.**

1. Container
2. Headline
3. Label text
4. Active indicator
5. Badge label text
6. Scrim
7. Icon

**Colour roles.** "The navigation drawer has one token set." Navigation drawer colour roles used for light and dark schemes — the rendered text lists the roles in order without naming the element each applies to (that pairing is diagram-only), so `Element` is `—`:

| Element | Role |
|---|---|
| — | Surface container low |
| — | On surface variant |
| — | On secondary container |
| — | On secondary container |
| — | Secondary container |
| — | On secondary container |
| — | On surface variant |
| — | On surface variant |
| — | Scrim |

"For divider color roles, go to divider specs."

Token set: **Navigation drawers (baseline)**, Default / Light, states Enabled / Hovered / Focused / Pressed (ripple).

**States.** "States are visual representations used to communicate the status of a component or interactive element."

- Enabled
- Hovered
- Focused
- Pressed

"State specs are in the tokens module above."

**Shape & morph.**

- Container shape: **0,16,16,0dp corner radii** (standard navigation drawer).
- Active indicator shape: **28dp** (standard and modal).

| Form | Element | Corner radii / shape |
|---|---|---|
| Standard navigation drawer | Container | 0,16,16,0dp corner radii |
| Standard navigation drawer | Active indicator | 28dp |
| Modal navigation drawer | Active indicator | 28dp |

The modal drawer's container shape is not listed in the rendered text. `—`

**Measurements.** Two text-backed tables exist on this page.

Standard navigation drawer:

| Attribute | Value |
|---|---|
| Container height | 100% |
| Container width | 360dp |
| Container shape | 0,16,16,0dp corner radii |
| Icon size | 24dp |
| Active indicator height | 56dp |
| Active indicator shape | 28dp |
| Active indicator width | 336dp |
| Horizontal label alignment | Start-aligned |
| Left padding | 28dp |
| Right padding | 28dp |
| Active indicator padding | 12dp |
| Padding between elements | 0dp |

Modal navigation drawer:

| Attribute | Value |
|---|---|
| Container height | 100% |
| Container width | 360dp |
| Icon size | 24dp |
| Active indicator height | 56dp |
| Active indicator shape | 28dp |
| Active indicator width | 336dp |
| Horizontal label alignment | Start-aligned |
| Left padding | 28dp |
| Right padding | 28dp |
| Active indicator padding | 12dp |
| Padding between elements | 0dp |

Diagram captions alongside these tables: "Element size measurements" and "Padding and margins".

**Notes.**

- "The navigation drawer is no longer recommended in the Material 3 Expressive update. For those who have updated, use an expanded navigation rail, which has mostly the same functionality of the navigation drawer and adapts better across breakpoints."
- The token set is named **Navigation drawers (baseline)** — it is the baseline token set, not an Expressive one.
- "The navigation drawer has one token set."
- "For divider color roles, go to divider specs."
- The modal drawer has no container shape row in the rendered text, unlike the standard drawer.

---

## Tabs

Source: https://m3.material.io/components/tabs/specs

"Tabs organize content across different screens and views"

**Variants.** Two variants are documented: **primary tabs** and **secondary tabs**. This page contains no M3 vs M3 Expressive availability table in the rendered text. Primary tabs are a primary-navigation token set; secondary tabs are secondary navigation. `—`

**Configurations.** No configurations table exists on this page in the rendered text. Primary tabs stack icon and label (their active indicator height is 3dp); secondary tabs are label-only (active indicator height 2dp). `—`

**Anatomy.**

Primary tabs:

1. Container
2. Badge (optional)
3. Icon (optional)
4. Label
5. Divider
6. Active indicator

Secondary tabs:

1. Container
2. Badge (optional)
3. Label
4. Divider
5. Active indicator

**Colour roles.** Primary tab colour roles used for light and dark schemes — the rendered text lists the roles in order without naming the element each applies to (that pairing is diagram-only), so `Element` is `—`:

| Element | Role |
|---|---|
| — | Surface |
| — | Primary |
| — | Primary |
| — | On surface variant |
| — | On surface variant |
| — | Outline variant |
| — | Primary |

Secondary tab colour roles used for light and dark schemes (same caveat):

| Element | Role |
|---|---|
| — | Surface |
| — | On surface |
| — | On surface variant |
| — | Outline variant |
| — | Primary |

Token sets: **Tabs – Primary navigation**, Default / Light, states Enabled / Hovered / Focused / Pressed (ripple).

**States.** Primary tabs states:

- Enabled (active destination)
- Hover (active destination)
- Focused (active destination)
- Pressed (active destination)
- Enabled (inactive destination)
- Hover (inactive destination)
- Focused (inactive destination)
- Pressed (inactive destination)

Secondary tabs states: identical list — Enabled / Hover / Focused / Pressed for both active and inactive destinations.

**Shape & morph.**

- "Tabs are divided into equal sections, with labels and icons positioned vertically centered. The divider is included in the height, placed inside the container."
- "Primary tab active indicators are inset 2dp on each side, have a fully rounded corner radius, and a minimum length of 24dp."

Corner radii:

| Attribute | Value |
|---|---|
| Active indicator shape | 3, 3, 0, 0 |
| Primary active indicator corner radius | Fully rounded (no dp value in rendered text) |

**Measurements.** "Tabs are divided into equal sections, with labels and icons positioned vertically centered. The divider is included in the height, placed inside the container."

| Attribute | Value |
|---|---|
| Container height (label text only) | 48dp |
| Container height (icon and label text) | 64dp |
| Icon size | 24dp |
| Divider height | 1dp |
| Primary active indicator height | 3dp |
| Secondary active indicator height | 2dp |
| Active indicator shape | 3, 3, 0, 0 |
| Active indicator minimum length | 24dp |
| Padding between inline icon and text | 8dp |
| Padding between inline text and badge | 4dp |
| Overlap of badge on stacked icon | 6dp |

Additional text-backed values: primary tab active indicators are **inset 2dp on each side** and have a **minimum length of 24dp**.

**Notes.**

- "The divider is included in the height, placed inside the container."
- "Primary tab active indicators are inset 2dp on each side, have a fully rounded corner radius, and a minimum length of 24dp."
- Primary tabs support an optional badge and an optional icon; secondary tabs support an optional badge but no icon.
- The rendered text carries no M3 vs M3 Expressive availability statement for tabs.

---

## Search

Source: https://m3.material.io/components/search/specs

"Search lets people enter a keyword or phrase to get relevant information"

**Variants.** "When a person executes a search, results appear in a list below the search bar"

| Variant | M3 | M3 Expressive |
|---|---|---|
| Search | Available | Available |

**Configurations.** Search comes in two styles:

- **Contained** (Expressive only): "Has an expressive look and feel. It uses a filled container to separate a search bar from a list of suggestions or results." "The contained style has a persistent, filled container, expressive motion, and rounded shape."
- **Divided (baseline)** (not recommended): "Doesn't have the latest visual style, motion, or flexibility." "The divided (baseline) style uses a divider to separate the search bar from suggestions and results."

Layout: "Search suggestions and results appear in customizable lists, with two layout options: full-screen and docked."

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Style | Contained | Not available | Available |
| Style | Divided | Available | Not recommended. Use contained. |
| Layout | Docked, full-screen | Available | Available |

**Anatomy.**

1. Search bar container
2. Leading icon
3. Supporting text
4. Trailing icon and avatar (optional)
5. Input text
6. Container for search suggestions or results

"Search includes a search bar and a container for suggestions and results. The container is empty by default. Use the list component to add content. In the divided (baseline) style, a divider separates the search bar and results."

Examples: with avatar; with one trailing icon button; with two trailing icon buttons; with trailing icon button and avatar.

**Colour roles.** Colour values are implemented through design tokens.

Full-screen search colour roles used in light and dark themes — the rendered text lists the roles in order without naming the element each applies to (that pairing is diagram-only), so `Element` is `—`:

| Element | Role |
|---|---|
| — | Surface container low |
| — | On surface variant |
| — | On surface variant |
| — | Surface container high |
| — | On surface variant |
| — | On surface |

Docked search colour roles used in light and dark themes (same caveat):

| Element | Role |
|---|---|
| — | Surface container high |
| — | On surface variant |
| — | On surface variant |
| — | Surface container high |
| — | On surface variant |
| — | On surface |

Token sets: **Search – View** (Default, Android, Light; folders Color, Layout and Text) and a search bar set. "The search bar set only contains tokens for the unfocused search bar. The search view set contains all other tokens when interacting with search, including all styles and layouts."

| Attribute | Value |
|---|---|
| Search view container surface tint layer color (Default, Android, Light) | #6750A4 |

**States.** "In focused search, individual elements maintain their own interaction states."

- **Search bar**: Enabled, Hovered, Focused, Pressed (ripple)
- **Search suggestions & results**: Enabled, Hovered, Focused, Pressed (ripple)

"Search includes a container for suggestions and results. The container is empty by default. Use the list component to add content."

**Shape & morph.**

- The **contained** style has "a persistent, filled container, expressive motion, and rounded shape".
- The **divided (baseline)** style "doesn't have the latest visual style, motion, or flexibility" and uses a divider to separate the search bar from suggestions and results.
- "In M3 Expressive, the search bar expands when focused. The margins change from 24dp to 12dp."

Corner radii are not written out in the rendered text; they exist only in the diagrams and token sets. `—`

| Element | Corner radii |
|---|---|
| Contained search bar / container | — (stated only as "rounded shape") |
| Divided (baseline) search bar | — |

**Measurements.**

Search bar:

| Element | Attribute | Value |
|---|---|---|
| Container | Width | Min: 360dp, max: 720dp |
| Container | Height | 56dp |
| Container | Label alignment | Start-aligned |
| Container | Leading padding | Unfocused: 24dp, focused: 12dp |
| Container | Trailing padding | Unfocused: 24dp, focused: 12dp |
| Container | Leading icon and label padding (from tap target) | 4dp |
| Container | Label and trailing icon padding (from tap target) | 4dp |
| Avatar | Size | 30dp |

Focused search — contained style:

| Element | Attribute | Value |
|---|---|---|
| Full-screen container | Width | Full width |
| Full-screen container | Height | Full height |
| Docked container | Width | Min: 360dp, max: 720dp |
| Docked container | Height | Min: 240dp, max: 2/3 of screen height |
| Search bar container | Height | 56dp |
| Search bar container | Label alignment | Start-aligned |
| Search bar container | Leading padding | 16dp |
| Search bar container | Trailing padding | 16dp |
| Search bar container | Leading icon and label padding (from tap target) | 4dp |

(The last row "Leading icon and label padding (from tap target) — 4dp" is listed twice consecutively in the rendered text; only one distinct attribute is present.)

Focused search — divided style: "Full-screen search padding and size measurements for divided style" and "Docked search padding and size measurements for divided style" are diagram-only, so no values are available.

| Element | Attribute | Value |
|---|---|---|
| Full-screen container (divided style) | Padding and size | — |
| Docked container (divided style) | Padding and size | — |

**Notes.**

- Divided (baseline) style: **Not recommended. Use contained.** It "doesn't have the latest visual style, motion, or flexibility."
- The contained style is **Expressive only** — `Not available` in M3.
- "In M3 Expressive, the search bar expands when focused. The margins change from 24dp to 12dp."
- "The search bar set only contains tokens for the unfocused search bar. The search view set contains all other tokens when interacting with search, including all styles and layouts."
- "In focused search, individual elements maintain their own interaction states."
- "Search includes a container for suggestions and results. The container is empty by default. Use the list component to add content."
- The search app bar reuses these tokens: "The default search component tokens are used in the search app bar."
