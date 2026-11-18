# Containment components — Material 3 / M3 Expressive specs

Transcribed from the individual component spec pages on m3.material.io (`/components/<slug>/specs`); retrieved 2026-09-12.
A value shown as `—` was not present in the rendered text (the spec presents it only as a diagram); the source's `--` in an availability table is written "Not available".

> Colour-role note that applies to every component below: the rendered text emits the anatomy labels and the colour-role names as two separate ordered lists, and does **not** state which element each role belongs to. Where the dump itself names the element (e.g. `Container`, `Scrim`, `Divider`) that name is carried over; everywhere else the Element cell is `—` and the roles are listed in source order. No element-to-role pairing has been inferred.
>
> Addendum (2026-09-12): where the official colour diagram numbers its callouts and the callout count equals the role count for that diagram, the Element cells have since been filled from those callouts, paired **positionally** (callout *n* → role *n* in the source order given in the text). Every table filled this way carries a *positional* note naming its diagram. Tables without such a note are unchanged.

---

## Cards

Source: https://m3.material.io/components/cards/specs

**Variants.** Three variants: **elevated card**, **filled card**, **outlined card** (section headings in the dump: "Elevated card", "Filled card", "Outlined card"). All three share the same anatomy and the same single measurements table; they differ only in container colour, and the outlined card adds an outline. The token module's default selection is "Card - Elevated / Default, Light". The rendered page carries **no M3 vs M3 Expressive availability table** for cards.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists anywhere in the rendered text for this page; `—` here means "no such table in the dump", not "not available".

**Anatomy.**

Elevated card:
1. Container

Filled card:
1. Container

Outlined card:
1. Container
2. Outline

**Colour roles** — "Elevated card color roles used for light and dark themes" / "Filled card color roles used for light and dark themes" / "Outlined card color roles used for light and dark themes":

| Element | Role |
|---|---|
| Elevated card — container | Surface container low |
| Filled card — container | Surface container highest |
| Outlined card — container | Surface |
| Outlined card — outline | Outline variant |

**States.** Each variant documents the same five states: **Hovered, Focused, Pressed, Dragged, Disabled**. The token module's state tree for "Card - Elevated" is: Enabled, Disabled, Hovered, Focused, Pressed (ripple), Dragged. No transition, elevation-change, or morph behaviour is stated on this page.

**Shape & morph.** One shared shape value: **12dp corner radius** (taken from the measurements table, which is a single table for the whole card family). The page states no per-variant corner radius and no shape morph.

**Measurements** — "Card padding and size measurements" (shared by all three variants):

| Attribute | Value |
|---|---|
| Shape | 12dp corner radius |
| Left/right padding | 16dp |
| Padding between cards | 8dp max |
| Label text alignment | Start-aligned |

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears on this page.

- **Optical inner corners (from `references/shape.md`):** When nesting rounded media thumbnails or inner containers inside a card, subtract container padding from the card's outer radius (`outer − padding = inner`; for example, a `16dp` or `28dp` expressive hero card with `12–16dp` padding uses `4dp` or `12dp` inner corners rather than duplicating the outer corner radius).

---

## Dialogs

Source: https://m3.material.io/components/dialogs/specs

**Variants.** Two variants: **basic dialog** and **full-screen dialog** (dump headings "Basic dialogs" / "Full-screen dialogs"); the token module's default selection is "Dialog - Basic / Default, Light". The rendered page carries **no M3 vs M3 Expressive availability table**.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists in the rendered text for this page.

**Anatomy.**

Basic dialogs:
1. Container
2. Icon (optional)
3. Headline (optional)
4. Supporting text
5. Divider (optional)
6. Button label text
7. Scrim

Full-screen dialogs:
1. Container
2. Header
3. Icon (close affordance)
4. Headline (optional)
5. Text button
6. Divider (optional)

**Colour roles.**

Basic dialog — "Basic dialog color roles used for light and dark themes", six roles in source order. Source: official colour diagram `dialogs__01__color` ("color mapping diagram labeling 6 color roles across the dialog and scrim"), retrieved 2026-09-12; its six numbered callouts equal the six roles, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Container (callout 1) — *positional* | Surface container high |
| Icon (callout 2) — *positional* | Secondary |
| Headline (callout 3) — *positional* | On surface |
| Supporting text (callout 4) — *positional* | On surface variant |
| Button label text (callout 5) — *positional* | Primary |
| Scrim (callout 6) — *positional* | Scrim |

The basic dialog lists seven anatomy elements but only six colour roles; the optional Divider is not among the diagram's six callouts, and the rendered text itself states no pairing.

Full-screen dialog — "Full-screen dialog color roles used for light and dark themes", five role entries in source order (note that **On surface** appears twice as two separate entries). Source: official colour diagram `dialogs__04__color` ("color mapping diagram shows 5 callout markers across the dialog"), retrieved 2026-09-12; its five numbered callouts equal the five roles, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Container (callout 1) — *positional* | Surface container high |
| Icon — close affordance (callout 2) — *positional* | On surface |
| Headline (callout 3) — *positional* | On surface |
| Text button (callout 4) — *positional* | Primary |
| Body text (callout 5) — *positional*, not in the anatomy list above | On surface variant |

**States.** The token module's state tree is: Enabled, Hovered, Focused, Pressed (ripple). No open/closed transition durations, scrim fade, or entrance/exit motion are stated on this page.

**Shape & morph.** Stated shape is a corner radius only, and it differs per variant: basic dialog **28dp corner radius**; full-screen dialog **0dp corner radius**. No morph behaviour is stated.

**Measurements.**

Basic dialog — "Basic dialog padding and size measurements":

| Attribute | Value |
|---|---|
| Container shape | 28dp corner radius |
| Container height | Dynamic |
| Container width | Min 280dp; Max 560dp |
| Divider height | 1dp |
| Icon size | 24dp |
| Minimum width | 280dp |
| Maximum width | 560dp |
| Alignment with icon | Center-aligned |
| Alignment without icon | Start-aligned |
| Top/Left/right/bottom padding | 24dp |
| Padding between buttons | 8dp |
| Padding between title and body | 16dp |
| Padding between icon and title | 16dp |
| Padding between body and actions | 24dp |

Full-screen dialog — "Full-screen dialog padding and size measurements":

| Attribute | Value |
|---|---|
| Container shape | 0dp corner radius |
| Container height | Dynamic |
| Container width | Container width; Max 560dp |
| Header height | 56dp |
| Header width | Container width |
| Headline text alignment | Start-aligned |
| Divider height | 1dp |
| Icon (close affordance) size | 24dp |
| Bottom action bar height | 56dp |
| Bottom action bar width | Container width |
| Top/left/right padding | 24dp |
| Padding between elements | 8dp |

**Notes.** No explicit do/don't or "not recommended" statement appears on this page.

### Modern Web Architecture (Pure Native `<dialog>`, Zero Scroll-Lock & Interruptible Spring)

- **Native `<dialog>` + `.showModal()` (NO `role="dialog"` / `aria-modal`)**: Native `<dialog>` opened via `.showModal()` provides top-layer stacking, automatic background `inert` isolation, `Escape` dismissal, and native dialog semantics — **never** add redundant `role="dialog"` or `aria-modal="true"` (`MD3E020` / `MD3E029`). Pair `<dialog>` with `aria-labelledby` (pointing to the headline) or `aria-label`.
- **Zero Root Scroll-Locking (`overscroll-behavior: contain`)**: **NEVER** set `overflow: hidden` or `position: fixed` on `<html>` or `<body>` when opening a modal dialog (which causes scrollbar-gutter layout shifts, breaks `position: sticky` rails, and loses scroll position). Instead, contain scroll chaining directly on the top-layer elements:
  ```css
  dialog.md3e-dialog:modal { overscroll-behavior: contain; }
  dialog.md3e-dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }
  ```
- **`closedby` Progressive Enhancement & Safe Backdrop Click**: Use `closedby="any"` on light-dismiss dialogs (or `closedby="closerequest"` when confirmation requires clicking an explicit action), paired with a `pointerdown` + `pointerup` target check so dragging text out onto `::backdrop` does not trigger accidental dismissal.
- **Interruptible Spring Enter/Exit (`cancel` interception + velocity continuity)**: Intercept the `cancel` event (`e.preventDefault()`) and backdrop clicks, driving a `createSpringAnimator` (`md3e-spring.js`) over `0 -> 1` (`--dialog-progress`) so pressing `Escape` or clicking outside mid-flight (e.g. at `150ms`) immediately reverses scale, translate, opacity, and backdrop dimming from live velocity, calling `dialog.close()` only once settled at `0`. Re-triggering open mid-close reverses back to `1` without flickering. Reset `dialog.returnValue = ''` before `.showModal()` and restore focus to the opener button on close.
- **Headless Portal Bridge**: In React/Vue/Svelte apps using Radix Dialog, Base UI Dialog, or Ark UI Dialog, bind `[data-state="open|closed"]` (or `[data-open]` / `[data-closed]`) directly to the same `28dp` (`--md-sys-shape-corner-extra-large`) `surface-container-high` container tokens.

```html
<button type="button" class="md3e-btn md3e-btn--tonal md3e-btn--s" id="btn-confirm-open">
  Open Confirm Dialog
</button>

<dialog class="md3e-dialog" id="confirm-dialog" aria-labelledby="confirm-dialog-title" closedby="any">
  <div class="md3e-dialog__surface">
    <span class="material-symbols-outlined md3e-dialog__icon" aria-hidden="true">restart_alt</span>
    <h2 class="md3e-dialog__title" id="confirm-dialog-title">Reset workspace tokens?</h2>
    <p class="md3e-dialog__body">
      Custom seed overrides will revert to the baseline expressive tonal palette.
    </p>
    <div class="md3e-dialog__actions">
      <button type="button" class="md3e-dialog__btn" value="cancel" id="confirm-dialog-cancel">Cancel</button>
      <button type="button" class="md3e-dialog__btn md3e-dialog__btn--primary" value="confirm" id="confirm-dialog-ok">Reset</button>
    </div>
  </div>
</dialog>
```

```css
dialog.md3e-dialog {
  --dialog-progress: 0;
  margin: auto;
  padding: 0;
  border: none;
  inline-size: min(560px, calc(100vw - 48px));
  min-inline-size: min(280px, calc(100vw - 48px));
  border-radius: var(--md-sys-shape-corner-extra-large); /* 28dp */
  background: var(--md-sys-color-surface-container-high);
  color: var(--md-sys-color-on-surface);
  overflow: visible;
  opacity: var(--dialog-progress);
  transform: translateY(calc((1 - var(--dialog-progress)) * 16px))
             scale(calc(0.92 + var(--dialog-progress) * 0.08));
}

dialog.md3e-dialog:modal {
  overscroll-behavior: contain;
}

dialog.md3e-dialog::backdrop {
  background: color-mix(in oklab, var(--md-sys-color-scrim) calc(var(--dialog-progress, 1) * 42%), transparent);
  overflow: hidden;
  overscroll-behavior: contain;
}

.md3e-dialog__surface {
  display: flex;
  flex-direction: column;
  padding: var(--md-sys-spacing-6); /* 24dp */
  max-block-size: calc(100dvh - 48px);
  overflow-y: auto;
  overscroll-behavior: contain;
}

.md3e-dialog__icon {
  align-self: center;
  color: var(--md-sys-color-secondary);
  margin-block-end: var(--md-sys-spacing-4);
}

.md3e-dialog__title {
  margin: 0 0 var(--md-sys-spacing-4);
  font-family: var(--md-sys-typescale-brand-font);
  font-size: var(--md-sys-typescale-headline-small-size);
  line-height: var(--md-sys-typescale-headline-small-line-height);
  font-weight: var(--md-sys-typescale-headline-small-weight);
  text-align: center;
}

.md3e-dialog__body {
  margin: 0 0 var(--md-sys-spacing-6);
  font-size: var(--md-sys-typescale-body-medium-size);
  line-height: var(--md-sys-typescale-body-medium-line-height);
  color: var(--md-sys-color-on-surface-variant);
}

.md3e-dialog__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--md-sys-spacing-2); /* 8dp */
}

.md3e-dialog__btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  block-size: 40px;
  padding-inline: var(--md-sys-spacing-4);
  border: none;
  border-radius: var(--md-sys-shape-corner-large-increased);
  background: transparent;
  color: var(--md-sys-color-primary);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  font-weight: var(--md-sys-typescale-label-large-weight);
  cursor: pointer;
}

.md3e-dialog__btn::before {
  content: "";
  position: absolute;
  inset-block: -4px;
  inset-inline: 0;
  min-inline-size: var(--md-sys-touch-target-min);
  min-block-size: var(--md-sys-touch-target-min);
}

.md3e-dialog__btn:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

@media (forced-colors: active) {
  dialog.md3e-dialog {
    border: 1px solid CanvasText;
  }
}
```

```js
// Interruptible <dialog> spring controller (150ms mid-flight reversal + focus restore)
import { createSpringAnimator } from './tokens/md3e-spring.js';

export function bindInterruptibleDialog(dialogEl, openerBtn) {
  let prevFocus = null;
  let pointerDownOnBackdrop = false;

  const spring = createSpringAnimator({
    initialValue: 0,
    stiffness: 380,
    damping: 0.8,
    precision: 0.002,
    onUpdate(p) {
      dialogEl.style.setProperty('--dialog-progress', p.toFixed(4));
    },
  });

  const open = () => {
    prevFocus = document.activeElement;
    dialogEl.returnValue = '';
    if (!dialogEl.open) dialogEl.showModal();
    spring.setTarget(1);
  };

  const close = (returnValue = 'cancel') => {
    spring.setTarget(0, {
      onRest() {
        if (dialogEl.open) dialogEl.close(returnValue);
        (prevFocus && typeof prevFocus.focus === 'function' ? prevFocus : openerBtn)?.focus();
      },
    });
  };

  dialogEl.addEventListener('cancel', (e) => {
    e.preventDefault();
    close('cancel');
  });

  dialogEl.addEventListener('pointerdown', (e) => {
    pointerDownOnBackdrop = e.target === dialogEl;
  });

  dialogEl.addEventListener('pointerup', (e) => {
    if (pointerDownOnBackdrop && e.target === dialogEl) close('cancel');
    pointerDownOnBackdrop = false;
  });

  return { open, close };
}
```

---

## Bottom sheets

Source: https://m3.material.io/components/bottom-sheets/specs

**Variants.** Two variants: **modal bottom sheets** and **standard bottom sheets**. The page states: "Modal bottom sheets are above a scrim while standard bottom sheets don't have a scrim. Besides this, both variants of bottom sheets have the same specs." The token module is "Sheets - Bottom / Default, Light". There is **no M3 vs M3 Expressive availability table** in the rendered text.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists in the rendered text for this page.

**Anatomy.**

1. Container
2. Drag handle (optional)
3. Scrim

**Colour roles** — "Bottom sheet color roles used for both light and dark schemes", three roles in source order. Source: official colour diagram `bottom-sheets__01__color` ("two diagrams featuring color opposites of scrim, container, drag handle"), retrieved 2026-09-12; its three numbered callouts equal the three roles, so the Element cells below are **positional** (callout *n* → role *n*) — here the callout order happens to match the anatomy order:

| Element | Role |
|---|---|
| Scrim (callout 1) — *positional* | Scrim |
| Drag handle (callout 2) — *positional* | On surface variant |
| Container (callout 3) — *positional* | Surface container low |

Footnote carried in the dump: "\*On Android platforms, the scrim color and opacity is automatically handled by the system UI." The rendered text itself pairs no roles with elements.

**States.** The token module's state tree contains only **Enabled**. No drag states and no open/closed states are stated on this page, even though the drag handle is a listed element.

**Shape & morph.** No corner radius is present in the rendered text — `—`. The only geometry prose given is: "Bottom sheets span the full window width up to 640dp. When the window width exceeds 640dp, bottom sheets adjust to have a top margin of 56dp and side margins of 56dp."

**Measurements** — "Bottom sheet padding and size measurements":

| Attribute | Value |
|---|---|
| Drag handle alignment (horizontal) | Center |
| Drag handle padding top/bottom | 22dp |
| Top margin | 72dp |
| Top margin (window width > 640dp) | 56dp |
| Start/end margin (window width > 640dp) | 56dp |
| Width | Full width, up to max-width 640dp |
| Height | Variable |

**Notes.** The dump warns that on Android the scrim colour and opacity are handled by the system UI (see footnote above); do not hard-code scrim opacity on Android. No do/don't or "not recommended" text beyond that.

---

## Side sheets

Source: https://m3.material.io/components/side-sheets/specs

**Variants.** Two variants: **standard side sheet** and **modal side sheet**. The token module is "Sheets - Side / Default, Light". There is **no M3 vs M3 Expressive availability table** in the rendered text.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists in the rendered text for this page. The only configuration-level distinction given is the prose note that the standard variant is detached-able (see "Margins (when detached)" in the measurements).

**Anatomy.**

Standard side sheet:
1. Divider (optional)
2. Headline
3. Container
4. Close icon button

Modal side sheet:
1. Back icon button (optional)
2. Headline
3. Container
4. Close icon button
5. Divider (optional)
6. Action buttons (optional)
7. Scrim

**Colour roles.**

Standard side sheet — "Side sheet color roles used for light and dark themes", four roles in source order. Source: official colour diagram `side-sheets__01__color` ("4 color roles applied to a side sheet in light and dark themes"), retrieved 2026-09-12; its four numbered callouts equal the four roles, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Divider (callout 1) — *positional* | Outline variant |
| Headline (callout 2) — *positional* | On surface variant |
| Container (callout 3) — *positional* | Surface |
| Close icon button (callout 4) — *positional* | On surface variant |

Modal side sheet — "Side sheet color roles used for light and dark themes", four roles in source order. Source: official colour diagram `side-sheets__04__color` ("4 color roles applied to a modal side sheet in light and dark themes"), retrieved 2026-09-12; its four numbered callouts equal the four roles, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Back icon button (callout 1) — *positional* | On surface variant |
| Headline (callout 2) — *positional* | On surface variant |
| Container (callout 3) — *positional* | Surface container low |
| Close icon button (callout 4) — *positional* | On surface variant |

The modal variant lists seven anatomy elements against four colour roles (and the standard variant four against four); the rendered text states no pairing, so the four rows above cover only the elements the diagram calls out.

**States.** The token module's state tree is: Enabled, Hovered, Focused, Pressed (ripple). No open/closed or slide-in/out transition behaviour is stated on this page.

**Shape & morph.** No corner radius and no shape morph are present in the rendered text — `—`.

**Measurements.**

Standard side sheet — "Side sheet padding and size measurements":

| Attribute | Value |
|---|---|
| Start/end padding | 24dp |
| Padding between top elements | 12dp |
| Bottom actions height | 72dp |
| Bottom actions top padding | 16dp |
| Bottom actions bottom padding | 24dp |
| Bottom actions alignment (horizontal) | Left |
| Max-width | 400dp |
| Margins (when detached) | 16dp |

Modal side sheet — "Modal side sheet padding and size measurements":

| Attribute | Value |
|---|---|
| Start/end padding | 24dp |
| Start padding with icon | 16dp |
| Padding between top elements | 12dp |
| Bottom actions height | 72dp |
| Bottom actions top padding | 16dp |
| Bottom actions bottom padding | 24dp |
| Bottom actions alignment (horizontal) | Left |
| Max-width | 400dp |
| Margins (when detached) | 16dp |

Delta between the two variants: the modal sheet adds **Start padding with icon — 16dp**, which the standard sheet does not list. All other rows are identical.

**Notes.** No explicit do/don't or "not recommended" statement appears on this page.

- **Desktop breakpoint swap (from `references/layout.md`):** On `Expanded` (`>= 840px`) and above, swap transient **Bottom Sheets** for **Side Sheets** (`400px` max-width) inside the multi-pane `surface-container` desktop shell (`24px` pane corners and `--md-sys-layout-pane-gap: 24px`), with `Escape` dismissal and focus return.

---

## Carousel

Source: https://m3.material.io/components/carousel/specs

**Variants.** Six layouts: **Multi-browse**, **Uncontained**, **Uncontained multi-aspect ratio** (rendered in the dump with the typo "Uncontained mutli-aspect ratio"), **Hero**, **Center-aligned hero**, **Full-screen**. The token module is "Carousel item / Default, Light". There is **no M3 vs M3 Expressive availability table** in the rendered text.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists in the rendered text for this page. The layout names above are the only configuration enumeration the dump provides, and they carry no M3 / M3 Expressive availability values.

**Anatomy.**

Multi-browse:
1. Container
2. Large carousel item
3. Medium carousel item
4. Small carousel item

Uncontained, Uncontained multi-aspect ratio, Full-screen:
1. Container
2. Large carousel item

Hero, Center-aligned hero:
1. Container
2. Large carousel item
3. Small carousel item

**Colour roles** — "Carousel color roles used for light and dark schemes": the dump names the element `Container` and the role `Surface`:

| Element | Role |
|---|---|
| Container | Surface |

**States.** The token module's state tree is: Enabled, Hover, Focus, Pressed (ripple), Disabled. The states prose lists: Enabled, Hovered, Focused, Pressed, Disabled. No transition behaviour is stated.

**Shape & morph.** Item corner radius is **28dp** in every layout that states one (Multi-browse, Uncontained, Uncontained multi-aspect ratio, Hero, Center-aligned hero). The Full-screen layout states no corner radius — `—`.

Dynamic width behaviour (stated as prose, not as a table):

- All kinds of carousel items dynamically adapt to the width of the container.
- Large items have a customizable maximum width that's used to optimally fit carousel items into the available space.
- Small carousel items have a minimum width of **40dp** and a maximum width of **56dp**.
- Items change size as they move through the carousel layout.

**Measurements.**

Multi-browse:

| Attribute | Value |
|---|---|
| Alignment | Vertically centered |
| Leading/trailing padding | 16dp |
| Top/bottom padding | 8dp |
| Padding between elements | 8dp |
| Large item width | Dynamic, or user-set |
| Medium item width | Dynamic |
| Small item width | 40–56dp, dynamic |
| Item corner radius | 28dp |

Uncontained:

| Attribute | Value |
|---|---|
| Alignment | Vertically centered |
| Leading padding | 16dp |
| Top/bottom padding | 8dp |
| Padding between elements | 8dp |
| Item corner radius | 28dp |

Uncontained multi-aspect ratio (shown in sections: Container, Carousel item (16:9), Carousel item (9:16), Carousel item (1:1), Carousel item (3:4)):

| Attribute | Value |
|---|---|
| Alignment | Vertically centered |
| Leading padding | 16dp |
| Top/bottom padding | 8dp |
| Padding between elements | 8dp |
| Item corner radius | 28dp |

Hero:

| Attribute | Value |
|---|---|
| Alignment | Vertically centered |
| Leading/Trailing padding | 16dp |
| Top/bottom padding | 8dp |
| Padding between elements | 8dp |
| Large item width | Dynamic |
| Small item width | 40-56dp, dynamic |
| Item corner radius | 28dp |

Center-aligned hero:

| Attribute | Value |
|---|---|
| Alignment | Vertically centered |
| Leading/Trailing padding | 16dp |
| Top/bottom padding | 8dp |
| Padding between elements | 8dp |
| Large item width | Dynamic |
| Small item width | 40-56dp, dynamic |
| Item corner radius | 28dp |

Full-screen:

| Attribute | Value |
|---|---|
| Alignment | Centered |
| Leading/Trailing padding | 0dp |
| Top/bottom padding | 0dp |
| Padding between elements | 16dp |

**Notes.** No explicit do/don't, caution, or "not recommended" statement appears on this page.

---

## Lists

Source: https://m3.material.io/components/lists/specs

**Variants.** Two variants: **Lists (expressive)** and **Lists (baseline)**. Expressive lists are the M3 Expressive default; baseline lists are M3-era and are marked not recommended for new designs.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Lists (expressive) | Not available | Available |
| Lists (baseline) | Available | Not recommended. Use expressive lists instead. |

Stated prose: "Use the expressive list variant for more flexible styling, highlighted selection states, and customizable slots." / "Baseline lists are still available to use, but don't have the latest visual style, selection treatment, and slot functionality." / "On web, expressive lists are built on top of baseline lists." / "The baseline list variant is available and continues to work in existing products. However, the expressive list variant is recommended for new designs."

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Styles | Standard | Available | Available |
| Styles | Segmented | Not available | Available |
| Selection modes | Single-action, multi-action, single-select, multi-select | Available | Available |
| Interactions | Expand, swipe\* | Available | Available |

\* Swipe-to-reveal interactions are only available on Android Views.

Expressive-only delta: the **Segmented** style is the only row added by M3 Expressive; everything else is available in both. Stated prose: "The standard and segmented styles are a visual choice, and don't affect a list's behavior." / "A list can have only one selection mode at a time. For example, a single-action list can change to a multi-select list, but can't be both at once." / "Lists can: Expand and collapse; Swipe to reveal\*."

**Anatomy.** "Container and label text are required. All other elements are optional":

1. Container
2. Overline
3. Label text
4. Trailing text
5. Supporting text
6. Trailing icon
7. Divider
8. Leading avatar
9. Leading icon
10. Leading media - image or video

Slots (expressive, from the "Flexibility & slots" section): the item is a container with three slots — leading, content, trailing.

- Leading slot can contain: visual elements (avatar, icon, image, or video thumbnail); selection controls (checkbox, radio button, or switch); customizations (badge or larger image).
- Content slot must be the largest-width slot and can contain: default content (label text, supporting text); optional add-ons (badge, icon, in-line label, or more text elements).
- Trailing slot can contain: action elements or text (icon, icon button, or trailing text); selection controls (checkbox, radio button, or switch).
- "The leading and trailing slot positions must be a smaller width than the content section."

**Colour roles.**

Lists (expressive) — "List color roles used for light and dark themes", ten roles in source order:

| Element | Role |
|---|---|
| — | Surface |
| — | On surface variant |
| — | On surface |
| — | On surface variant |
| — | On surface variant |
| — | On surface variant |
| — | Outline variant |
| — | Primary container |
| — | On primary container |
| — | On surface variant |

Lists (baseline) — "List color roles used for light and dark themes", nine roles in source order:

| Element | Role |
|---|---|
| — | Surface |
| — | On surface |
| — | On surface variant |
| — | On surface variant |
| — | On surface variant |
| — | Outline variant |
| — | Primary container |
| — | On primary container |
| — | On surface variant |

Delta: the expressive list emits one more role entry than the baseline list. Neither list is paired with elements in the rendered text.

**States.**

Expressive lists:

- Default list items: Enabled, Disabled, Hovered, Focused, Pressed, Dragged.
- Selected list items: Enabled, Disabled, Hovered, Focused, Pressed, Dragged.

Baseline lists (numbered in the dump): 1. Enabled, 2. Disabled, 3. Hovered, 4. Focused, 5. Pressed, 6. Dragged.

**Shape & morph.** "Shape morphing — When a list item is selected, the corner shape changes to highlight the active item":

| List item state | Corner radius |
|---|---|
| Unselected | 4dp inner, 16dp outer |
| Selected | 16dp |

Stated prose: "Unselected list items have a 4dp inner corner radius, and 16dp outer corner radius" / "Selected list items have a 16dp corner radius all around".

**Measurements.**

Lists (expressive) — the "Measurements" section states only prose: "List item alignment, padding, and size measurements. The icon button height is dynamic, and automatically adjusts to fill the list item height." **No measurements table is present in the rendered text** for expressive lists; the section continues directly into Shape morphing (see above). Every expressive measurement is therefore `—`:

| Attribute | Value |
|---|---|
| List item alignment | — |
| List item padding | — |
| List item size | — |
| Icon button height | Dynamic (stated in prose only) |

Lists (baseline) — the dump renders the subheadings **One-line lists**, **Two-line lists**, **Three-line lists**, each annotated "Baseline list item measurements and padding", but a **single shared Attribute/Value table** follows all three. The rows below are that shared table, transcribed in full (18 rows):

| Attribute | Value |
|---|---|
| Label alignment | Center |
| Label alignment when height is 88dp or taller | Top |
| Label left padding | 16dp |
| Leading element alignment (vertical) | Center |
| Leading element alignment (vertical) when height is 88dp or taller | Top |
| Leading element left padding | 16dp |
| Leading icon alignment (vertical) | Top |
| Leading icon top padding | 8dp |
| Leading icon top padding when height is 88dp or taller | 12dp |
| Trailing element alignment (vertical) | Center |
| Trailing element alignment (vertical) when height is 88dp or taller | Top |
| Trailing element left padding | 16dp |
| Trailing element right padding | 24dp |
| Padding above/below divider | 0dp |
| Targets | 48dp |
| Divider full-width | 100% |
| Divider inset left padding | 16dp |
| Divider inset right padding | 24dp |

Baseline configuration examples (from the "Configurations" section): Leading avatar, Leading image or thumbnail, Leading video, Leading icon, Text-only, Leading checkbox, Leading radio button, Trailing switch.

**Notes.**

- Expressive is recommended; baseline is "Not recommended. Use expressive lists instead." and "doesn't have the latest visual style, selection treatment, and slot functionality".
- Selection: "For selection lists, use only one selection interaction per list item." Do: "Use only one selection interaction per list item." Don't: "Don't use multiple selection interactions in one item."
- Slots: "Slots are not accessible by default." Elements must follow the rules, structure, and interaction patterns for lists; use standard list item padding; **target size must be at least 48x48dp**; don't add interactive elements that make the list item difficult to navigate, especially for people using screen readers.
- Caution: "Reserve the use of slots for use cases that maintain the list's accessibility and functionality."
- Caution: "Slots require custom code implementation that you must create and maintain."
- Content slot must be the largest section, placed in the middle of the list item; "Avoid long lines of text to preserve readability."
- Swipe-to-reveal is only available on Android Views.

---

## Divider

Source: https://m3.material.io/components/divider/specs

**Variants.** A single component, "Divider"; the token module has one entry ("Divider / Default, Light") whose state tree contains only **Enabled**. The full-width / inset / middle-inset treatments are described only through the measurements table below, not as named variants. There is **no M3 vs M3 Expressive availability table** in the rendered text.

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| — | — | — | — |

No availability or configuration table exists in the rendered text for this page.

**Anatomy.** Not present in the rendered text — `—`. The dump supplies no element list for the divider; only the component name "Divider" appears.

**Colour roles** — "Divider color roles used for light and dark schemes": the dump names the element `Divider` and the role `Outline variant`:

| Element | Role |
|---|---|
| Divider | Outline variant |

**States.** Only **Enabled** appears in the token module's state tree. No disabled, hover, focus, or pressed behaviour is stated.

**Shape & morph.** No corner radius and no morph are present in the rendered text — `—`. Line thickness is likewise absent from the measurements table (which lists margins only), so thickness is `—` on this page.

**Measurements** — "Measurements":

| Attribute | Value |
|---|---|
| Divider full-width | 100% |
| Divider inset left margin | 16dp |
| Divider inset right margin | 0dp |
| Divider middle-inset left margin | 16dp |
| Divider middle-inset right margin | 16dp |
| Space between divider & supporting-text | 4dp |
| Divider right margin | 8dp |
| Divider bottom margin | 8dp |

**Notes.** No explicit do/don't or "not recommended" statement appears on this page.

---

## Menus

Source: https://m3.material.io/components/menus/specs

**Variants.** Two variants.

| Variant | M3 | M3 Expressive |
|---|---|---|
| Vertical menus | Not available | Available |
| Menu (baseline) | Available | Available |

(The dump renders the second row's name as "Menu ( baseline)".) Stated prose: "Use vertical menus for a more expressive look and feel, including rounded corners, standard and vibrant color styles, more selection states, and submenu motion." / "In M3 Expressive, baseline menu is still available to use, but doesn't have the latest shapes, color styles, selection states, and motion." / "A baseline menu has square corners, as compared to a vertical menu's round corners and expressive styling."

**Configurations** — M3 vs M3 Expressive availability

| Category | Configuration | M3 | M3 Expressive |
|---|---|---|---|
| Color | Standard | Available | Available |
| Color | Vibrant | Not available | Available |
| Layout | Standard | Available | Available |
| Layout | Grouped | Not available | Available |

Vertical menu layout examples named in the dump: "Standard", "Grouped". Expressive-only delta: **Vibrant** colour and the **Grouped** layout are M3 Expressive additions.

**Anatomy.**

Vertical menus:
1. Menu item
2. Leading icon (optional)
3. Menu item text
4. Trailing icon (optional)
5. Badge (optional)
6. Trailing text (optional)
7. Container
8. Supporting text (optional)
9. Label text (optional)
10. Gap (optional)
11. Divider (optional)

Menu (baseline):
1. List item
2. List item leading icon
3. List item trailing icon
4. Container
5. List item trailing text
6. Divider

**Colour roles.** "Menus have two color mappings: Standard: Surface-based; Vibrant: Tertiary-based. These mappings provide options for lower or higher visual emphasis."

Vertical menus, Standard colours — "Vertical menus color roles used for light and dark themes", eleven roles in source order. Source: official colour diagram `menus__05__color` ("2 vertical menus with standard color roles mapped to 11 elements"), retrieved 2026-09-12; its eleven numbered callouts equal the eleven roles, so the Element cells below are **positional** (callout *n* → role *n*), the callout anchors being read off the diagram's light and dark panels:

| Element | Role |
|---|---|
| Leading icon (callout 1) — *positional* | On surface variant |
| Menu item text (callout 2) — *positional* | On surface |
| State layer of a hovered item (callout 3) — *positional* | On surface (state layer) |
| Container (callout 4) — *positional* | Surface container low |
| Trailing text (callout 5) — *positional* | On surface variant |
| Trailing icon (callout 6) — *positional* | On surface variant |
| Container of the selected item (callout 7) — *positional* | Tertiary container (selected) |
| Text of the selected item (callout 8) — *positional* | On tertiary container (selected) |
| Supporting text (callout 9) — *positional* | On surface variant |
| Label text (callout 10) — *positional* | On surface variant |
| Leading icon of the selected item (callout 11) — *positional* | On tertiary container (selected) |

Vertical menus, Vibrant colours — "Vertical menus color roles used for light and dark themes", eleven roles in source order. Source: official colour diagram `menus__06__color` ("2 vertical menus with vibrant color roles mapped to 11 elements"), retrieved 2026-09-12; its eleven numbered callouts sit on the same elements as `menus__05__color`, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Leading icon (callout 1) — *positional* | On tertiary container |
| Menu item text (callout 2) — *positional* | On tertiary container |
| State layer of a hovered item (callout 3) — *positional* | On tertiary container (state layer) |
| Container (callout 4) — *positional* | Tertiary container |
| Trailing text (callout 5) — *positional* | On tertiary container |
| Trailing icon (callout 6) — *positional* | On tertiary container |
| Container of the selected item (callout 7) — *positional* | Tertiary (selected) |
| Text of the selected item (callout 8) — *positional* | On tertiary (selected) |
| Supporting text (callout 9) — *positional* | On tertiary container |
| Label text (callout 10) — *positional* | On tertiary container |
| Leading icon of the selected item (callout 11) — *positional* | On tertiary (selected) |

Menu (baseline) — "Baseline menu color roles used for light and dark themes", nine roles in source order. Source: official colour diagram `menus__10__color` ("9 color roles of a baseline menu in light and dark themes"), retrieved 2026-09-12; its nine numbered callouts equal the nine roles, so the Element cells below are **positional** (callout *n* → role *n*):

| Element | Role |
|---|---|
| Leading icon (callout 1) — *positional* | On surface variant |
| Menu item text (callout 2) — *positional* | On surface |
| State layer of a hovered item (callout 3) — *positional* | On surface - opacity: 0.08 |
| Container (callout 4) — *positional* | Surface container |
| Trailing text (callout 5) — *positional* | On surface variant |
| Trailing icon (callout 6) — *positional* | On surface variant |
| Trailing icon of the last item (callout 7) — *positional* | On surface variant |
| Container of the selected item (callout 8) — *positional* | Surface container highest |
| Divider (callout 9) — *positional* | Outline variant |

**States.**

Vertical menus: Enabled, Disabled, Hovered, Focused, Pressed, **Active (main menu reveals submenu)**. Stated behaviour: "Shape morphing in vertical menus creates an expressive active state. As focus moves between submenus, the corner shape changes to highlight the active menu."

Menu (baseline): Default menu items — Enabled, Disabled, Hovered, Focused, Pressed; Selected menu items — Enabled, Disabled, Hovered, Focused, Pressed. The dump adds "State specs are in the token module above".

**Shape & morph.** Vertical menus: rounded corners and shape morphing are stated in prose only (see States above) — **no corner radius value appears in the rendered text**, so it is `—`; the official measurement diagram `menus__08__measure` labels that corner **16dp** (retrieved 2026-09-12). Menu (baseline): **corner radius 4dp**.

**Measurements.**

Vertical menus — the section heading and the line "Vertical menu padding and size measurements" are present, but **no measurements table follows in the rendered text** (the dump goes straight on to "Menu (baseline)"). Source for the two rows below: official measurement diagram `menus__08__measure` ("vertical menu marked with spacing and padding measurements"), retrieved 2026-09-12; the diagram is drawn at 2 px = 1 dp and every value below was re-measured against that scale:

| Attribute | Value |
|---|---|
| Vertical menu padding | 2dp (top and bottom of the menu, and between menu items); 20dp (leading icon padding and trailing icon padding) |
| Vertical menu size | 48dp (menu item height); 16dp (container corner radius); 32dp (label row height) |

Menu (baseline) — "Baseline menu padding and size measurements":

| Attribute | Value |
|---|---|
| Container width | 112dp min, 280dp max |
| Corner radius | 4dp |
| Vertical label text alignment | Center-aligned |
| Horizontal label text alignment | Start-aligned |
| Left/right padding | 12dp |
| Left/right padding with-icon | 12dp |
| List item height | 48dp |
| Padding between elements within a list item | 12dp |
| Divider top/bottom padding | 8dp |
| Divider height | 1dp |
| Divider width | Dynamic |
| Leading/trailing icon size | 24dp |

**Notes.**

- "Vibrant menus are more prominent so should be used sparingly."
- Baseline menu is still supported but "doesn't have the latest shapes, color styles, selection states, and motion"; M3 expressive vertical menus are recommended for new designs.
- A baseline menu appears when a person interacts with a button, action, or other control; the dump's examples are Button, Text field, Icon button, Selected text.

### Modern Web Architecture (`[popover="auto"]`, CSS Anchor Positioning & Safe-Triangle Submenus)

- **Top-Layer `[popover="auto"]` (Zero `overflow: hidden` Parent Clipping)**: Always mount M3E menus as native `[popover="auto"]` elements so opening a menu inside a `overflow: hidden` card or constrained scroll pane promotes it directly into the browser **Top Layer** with built-in light-dismiss and `Escape` closure. Wire triggers with `popovertarget` (or native Invoker Commands `commandfor` + `command="toggle-popover"`, never combining both on one trigger).
- **CSS Anchor Positioning + 4-Edge Viewport Flip Fallback**:
  - Gate anchor positioning cleanly inside `@supports (position-area: block-end)`: bind `anchor-name: --menu-anchor` on the trigger, `position-anchor: --menu-anchor`, `inset: auto; margin: 0; position-area: block-end span-inline-end; position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline;`.
  - Provide an explicit `@supports not (position-area: block-end)` + JS `getBoundingClientRect()` 4-edge viewport collision fallback so older browsers flip cleanly across top/bottom/start/end edges without clipping.
- **`overflow: visible`, Nested Submenus & Safe-Triangle Corridor**: Keep `overflow: visible;` on `.md3e-menu` so nested submenus (implemented either as nested `[popover="auto"]` top-layer popovers or positioned flyouts) and `:focus-visible` outlines never clip. When closing a nested submenu via `Escape` or `ArrowLeft`, call `event.stopPropagation()` so only the deepest submenu closes and returns focus to its parent trigger. Track pointer coordinates with a diagonal **safe-triangle** polygon grace window so moving diagonally from a parent item into its open submenu does not drop hover prematurely.
- **Native `<hr>` Separators, `role="menuitemcheckbox"`, & Keyboard / First-Letter Typeahead**:
  - Use semantic `<hr class="md3e-menu__divider">` for group dividers (`outline-variant`), `<button type="button" role="menuitemcheckbox" aria-checked="true|false">` for toggleable options, and progressive `focusgroup="menu nomemory"` alongside full JS fallback (`ArrowDown` / `ArrowUp` wrapping across enabled items, `Home` / `End`, `ArrowRight` opening submenus and focusing first child, `ArrowLeft` / `Escape` single-level close, `Tab` graceful close, and printable **first-letter typeahead**).
- **Separate `transition-behavior: allow-discrete;` + `@starting-style`**: Always place `transition-behavior: allow-discrete;` as a separate declaration **after** `transition:` (including `display` and `overlay` alongside `opacity` and `transform`) inside `@media (prefers-reduced-motion: no-preference)` so top-layer popovers animate smoothly on both entry and exit.

```html
<!-- Trigger + Popover Menu safely inside an overflow: hidden parent card -->
<div class="md3e-menu-host">
  <button
    type="button"
    class="md3e-btn md3e-btn--outlined md3e-btn--s md3e-menu-anchor"
    id="view-menu-trigger"
    popovertarget="view-menu"
    aria-haspopup="menu"
    aria-expanded="false"
    aria-controls="view-menu"
  >
    <span>Options</span>
    <span class="material-symbols-outlined" aria-hidden="true">arrow_drop_down</span>
  </button>

  <div class="md3e-menu" id="view-menu" popover="auto" role="menu" aria-labelledby="view-menu-trigger" focusgroup="menu nomemory">
    <button type="button" class="md3e-menu__item" role="menuitem">
      <span class="material-symbols-outlined" aria-hidden="true">content_copy</span>
      <span>Duplicate view</span>
    </button>
    <button type="button" class="md3e-menu__item" role="menuitemcheckbox" aria-checked="true">
      <span class="material-symbols-outlined md3e-menu__check" aria-hidden="true">check</span>
      <span>Show grid metrics</span>
    </button>
    <hr class="md3e-menu__divider">
    <button
      type="button"
      class="md3e-menu__item"
      id="export-submenu-trigger"
      role="menuitem"
      popovertarget="export-submenu"
      aria-haspopup="menu"
      aria-expanded="false"
      aria-controls="export-submenu"
    >
      <span class="material-symbols-outlined" aria-hidden="true">ios_share</span>
      <span>Export as…</span>
      <span class="material-symbols-outlined md3e-menu__trailing" aria-hidden="true">chevron_right</span>
    </button>
  </div>

  <div class="md3e-menu" id="export-submenu" popover="auto" role="menu" aria-labelledby="export-submenu-trigger">
    <button type="button" class="md3e-menu__item" role="menuitem"><span>CSS Tokens</span></button>
    <button type="button" class="md3e-menu__item" role="menuitem"><span>JSON Telemetry</span></button>
  </div>
</div>
```

```css
.md3e-menu-anchor {
  anchor-name: --md3e-menu-trigger;
}

.md3e-menu {
  --md3e-menu-top: 64px;
  --md3e-menu-left: 16px;
  margin: 0;
  padding: 2px 0; /* 2dp vertical menu padding */
  min-inline-size: 168px;
  max-inline-size: 280px;
  border: none;
  overflow: visible; /* Allow safe-triangle flyouts & focus rings without clipping */
  border-radius: var(--md-sys-shape-corner-large); /* 16dp Expressive vertical menu */
  background: var(--md-sys-color-surface-container-low);
  color: var(--md-sys-color-on-surface);
  box-shadow: var(--md-sys-elevation-level2);
  display: none;
  flex-direction: column;
  gap: 2px; /* 2dp between items */
  opacity: 0;
  transform: translateY(-6px) scale(0.96);
  transform-origin: top left;
}

@supports (position-area: block-end) {
  .md3e-menu[popover] {
    position-anchor: --md3e-menu-trigger;
    inset: auto;
    margin: 0;
    position-area: block-end span-inline-end;
    position-try-fallbacks: flip-block, flip-inline, flip-block flip-inline;
  }
}

@supports not (position-area: block-end) {
  .md3e-menu[popover] {
    position: fixed;
    inset-block-start: var(--md3e-menu-top, 64px);
    inset-inline-start: var(--md3e-menu-left, 16px);
  }
}

.md3e-menu:popover-open {
  display: flex;
  opacity: 1;
  transform: translateY(0) scale(1);
}

@media (prefers-reduced-motion: no-preference) {
  .md3e-menu {
    transition:
      opacity var(--md-sys-motion-fast-effects),
      transform var(--md-sys-motion-fast-spatial),
      display var(--md-sys-motion-fast-effects-duration),
      overlay var(--md-sys-motion-fast-effects-duration);
    transition-behavior: allow-discrete;
  }

  @starting-style {
    .md3e-menu:popover-open {
      opacity: 0;
      transform: translateY(-6px) scale(0.96);
    }
  }
}

.md3e-menu__item {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--md-sys-spacing-3);
  inline-size: 100%;
  min-block-size: var(--md-sys-touch-target-min); /* 48dp */
  padding-inline: var(--md-sys-spacing-3);
  border: none;
  border-radius: var(--md-sys-shape-corner-medium);
  background: transparent;
  color: var(--md-sys-color-on-surface);
  font-family: var(--md-sys-typescale-plain-font);
  font-size: var(--md-sys-typescale-label-large-size);
  line-height: var(--md-sys-typescale-label-large-line-height);
  text-align: start;
  cursor: pointer;
  transition: background-color var(--md-sys-motion-fast-effects),
              color var(--md-sys-motion-fast-effects);
}

.md3e-menu__item:hover,
.md3e-menu__item[data-highlighted="true"] {
  background: color-mix(in oklab, var(--md-sys-color-on-surface) 8%, transparent);
}

.md3e-menu__item[role="menuitemcheckbox"][aria-checked="true"] {
  background: var(--md-sys-color-tertiary-container);
  color: var(--md-sys-color-on-tertiary-container);
  font-weight: var(--md-sys-typescale-label-large-emphasized-weight);
}

.md3e-menu__item[role="menuitemcheckbox"][aria-checked="false"] .md3e-menu__check {
  opacity: 0;
}

.md3e-menu__trailing {
  margin-inline-start: auto;
}

.md3e-menu__divider {
  margin: var(--md-sys-spacing-1) var(--md-sys-spacing-3);
  border: none;
  border-block-start: 1px solid var(--md-sys-color-outline-variant);
}

.md3e-menu__item:focus-visible {
  outline: var(--md-sys-focus-ring-width) solid var(--md-sys-color-secondary);
  outline-offset: var(--md-sys-focus-ring-gap);
}

@media (prefers-reduced-motion: reduce) {
  .md3e-menu,
  .md3e-menu__item {
    transition: none;
  }
}

@media (forced-colors: active) {
  .md3e-menu {
    border: 1px solid CanvasText;
  }
}
```

```js
// Arrow/Home/End + first-letter typeahead + single-level submenu Escape
export function bindMenuKeyboard(menuEl, triggerEl) {
  const getItems = () => [...menuEl.querySelectorAll('[role="menuitem"], [role="menuitemcheckbox"]')].filter((el) => !el.disabled);

  menuEl.addEventListener('keydown', (e) => {
    const items = getItems();
    if (!items.length) return;
    const idx = items.indexOf(document.activeElement);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      items[(idx + 1) % items.length].focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      items[(idx - 1 + items.length) % items.length].focus();
    } else if (e.key === 'Home') {
      e.preventDefault();
      items[0].focus();
    } else if (e.key === 'End') {
      e.preventDefault();
      items[items.length - 1].focus();
    } else if (e.key === 'ArrowLeft' || e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation(); // Keep parent menu open when closing a nested submenu
      menuEl.hidePopover?.();
      triggerEl?.focus();
    } else if (e.key.length === 1 && /\S/.test(e.key) && !e.ctrlKey && !e.metaKey && !e.altKey) {
      const q = e.key.toLowerCase();
      const ordered = [...items.slice(idx + 1), ...items.slice(0, idx + 1)];
      const match = ordered.find((el) => el.textContent.trim().toLowerCase().startsWith(q));
      if (match) {
        e.preventDefault();
        match.focus();
      }
    }
  });
}
```
