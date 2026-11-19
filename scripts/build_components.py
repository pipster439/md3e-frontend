#!/usr/bin/env python3
"""Concatenate individual component stylesheets into assets/components/md3e-components.css."""

from __future__ import annotations

import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
COMPONENTS_DIR = ROOT_DIR / "assets" / "components"
OUTPUT_FILE = COMPONENTS_DIR / "md3e-components.css"

COMPONENT_ORDER = (
    "button.css",
    "fab.css",
    "card.css",
    "switch.css",
    "checkbox.css",
    "slider.css",
    "progress.css",
    "text-field.css",
    "dialog.css",
    "menu.css",
    "select.css",
    "datepicker.css",
    "toolbar.css",
    "snackbar.css",
    "navigation.css",
    "sheet.css",
)


def build_bundle() -> str:
    header = (
        "/* ============================================================================\n"
        " * MD3E Combined Component Stylesheet (md3e-components.css)\n"
        " * Auto-assembled from assets/components/*.css via scripts/build_components.py\n"
        " * Requires: assets/tokens/md3e-tokens.css, assets/tokens/md3e-motion.css\n"
        " * Optional: assets/tokens/md3e-shapes.css, assets/tokens/md3e-blur.css\n"
        " * ========================================================================== */\n\n"
    )
    parts: list[str] = [header]
    for name in COMPONENT_ORDER:
        path = COMPONENTS_DIR / name
        parts.append(f"/* >>> BEGIN {name} >>> */\n")
        parts.append(path.read_text(encoding="utf-8").rstrip() + "\n")
        parts.append(f"/* <<< END {name} <<< */\n\n")
    return "".join(parts)


def main() -> int:
    bundle = build_bundle()
    OUTPUT_FILE.write_text(bundle, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT_DIR)} ({len(bundle):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
