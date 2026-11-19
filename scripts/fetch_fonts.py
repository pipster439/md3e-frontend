#!/usr/bin/env python3
"""Download and assemble self-hosted MD3E variable fonts into assets/fonts/.

Fetches Google Sans Flex, Roboto Flex, and Material Symbols Outlined (all
SIL Open Font License 1.1 / Apache 2.0) as compact WOFF2 files and generates
assets/fonts/md3e-fonts.css for zero-network / offline usage.

Usage:
    python scripts/fetch_fonts.py
"""

from __future__ import annotations

import pathlib
import re
import urllib.request

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT_DIR / "assets" / "fonts"

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

FONT_SPECS = [
    {
        "family": "Google Sans Flex",
        "css_url": (
            "https://fonts.googleapis.com/css2?"
            "family=Google+Sans+Flex:GRAD,ROND,opsz,wdth,wght@-50..200,0..100,6..144,25..151,100..1000&display=swap"
        ),
        "subsets": {
            "latin-ext": "google-sans-flex-latin-ext.woff2",
            "latin": "google-sans-flex-latin.woff2",
        },
    },
    {
        "family": "Roboto Flex",
        "css_url": (
            "https://fonts.googleapis.com/css2?"
            "family=Roboto+Flex:GRAD,opsz,wdth,wght@-200..150,8..144,25..151,100..1000&display=swap"
        ),
        "subsets": {
            "latin-ext": "roboto-flex-latin-ext.woff2",
            "latin": "roboto-flex-latin.woff2",
        },
    },
    {
        "family": "Material Symbols Outlined",
        "css_url": (
            "https://fonts.googleapis.com/css2?"
            "family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block"
        ),
        "subsets": {
            "fallback": "material-symbols-outlined.woff2",
        },
    },
]


def _fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": CHROME_UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main() -> int:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    css_parts = [
        "/* ============================================================================\n"
        " * MD3E Self-Hosted Variable Fonts & Material Symbols Outlined\n"
        " * Offline-first local @font-face stylesheet (regenerated via scripts/fetch_fonts.py)\n"
        " * Licenses: SIL Open Font License 1.1 (see assets/fonts/OFL-1.1-LICENSE.txt)\n"
        " * ========================================================================== */\n\n"
    ]

    for spec in FONT_SPECS:
        css_text = _fetch_bytes(spec["css_url"]).decode("utf-8")
        blocks = re.findall(r"/\*\s*([^*]+?)\s*\*/\s*@font-face\s*\{([^}]+)\}", css_text)
        by_subset = {subset.strip(): body for subset, body in blocks}

        for subset_key, out_name in spec["subsets"].items():
            if subset_key not in by_subset:
                raise RuntimeError(f"Subset {subset_key!r} not found in Google Fonts CSS for {spec['family']}")
            body = by_subset[subset_key]
            url_m = re.search(r"url\(([^)]+)\)", body)
            if not url_m:
                raise RuntimeError(f"Missing WOFF2 URL for {spec['family']} [{subset_key}]")
            woff2_url = url_m.group(1).strip().strip("'\"")
            data = _fetch_bytes(woff2_url)
            out_path = FONTS_DIR / out_name
            out_path.write_bytes(data)
            print(f"Downloaded {out_name} ({len(data):,} bytes)")

            local_body = re.sub(
                r"url\([^)]+\)",
                f"url('./{out_name}')",
                body,
            )
            indented_body = "\n".join(
                ("  " + ln.lstrip()) if ln.strip() else ""
                for ln in local_body.strip().splitlines()
            )
            css_parts.append(f"/* {spec['family']} ({subset_key}) */\n@font-face {{\n{indented_body}\n}}\n\n")

    css_parts.append(
        ".material-symbols-outlined {\n"
        "  font-family: 'Material Symbols Outlined';\n"
        "  font-weight: normal;\n"
        "  font-style: normal;\n"
        "  font-size: var(--md-sys-icon-size, 24px);\n"
        "  line-height: 1;\n"
        "  letter-spacing: normal;\n"
        "  text-transform: none;\n"
        "  display: inline-flex;\n"
        "  align-items: center;\n"
        "  justify-content: center;\n"
        "  white-space: nowrap;\n"
        "  word-wrap: normal;\n"
        "  direction: ltr;\n"
        "  -webkit-font-feature-settings: 'liga';\n"
        "  font-feature-settings: 'liga';\n"
        "  -webkit-font-smoothing: antialiased;\n"
        "}\n"
    )

    css_out = FONTS_DIR / "md3e-fonts.css"
    css_out.write_text("".join(css_parts), encoding="utf-8", newline="\n")
    print(f"Wrote {css_out.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
