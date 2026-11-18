#!/usr/bin/env python3
"""Automated regression suite for the md3e-frontend skill."""

from __future__ import annotations

import json
import pathlib
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import audit_md3e  # noqa: E402
import color_to_css  # noqa: E402
import shapes_to_css  # noqa: E402
import spring_to_css  # noqa: E402

TOKENS_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-tokens.css"
PALETTES_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-palettes.css"
SHAPES_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-shapes.css"
MOTION_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-motion.css"
SPRING_JS = ROOT_DIR / "assets" / "tokens" / "md3e-spring.js"
STUDIO_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-studio.css"
STUDIO_JS = ROOT_DIR / "assets" / "tokens" / "md3e-studio.js"
TAILWIND_THEME_CSS = ROOT_DIR / "assets" / "tailwind" / "md3e-theme.css"
TAILWIND_CONFIG_JS = ROOT_DIR / "assets" / "tailwind" / "tailwind.config.js"
STARTER_HTML = ROOT_DIR / "assets" / "starter" / "index.html"
BENTO_HTML = ROOT_DIR / "assets" / "starter" / "desktop-bento.html"
SKILL_MD = ROOT_DIR / "SKILL.md"
OFFICIAL_AUDIT_MD = ROOT_DIR / "OFFICIAL_SPEC_AUDIT.md"
REFERENCES_DIR = ROOT_DIR / "references"


def srgb_luminance(hex_color: str) -> float:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def channel(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    la = srgb_luminance(hex_a)
    lb = srgb_luminance(hex_b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def extract_var_block(css_text: str, anchor_regex: str) -> dict[str, str]:
    m = re.search(anchor_regex, css_text)
    if not m:
        raise AssertionError(f"Could not find CSS block matching: {anchor_regex}")
    start = m.end()
    depth = 1
    i = start
    while i < len(css_text) and depth > 0:
        if css_text[i] == "{":
            depth += 1
        elif css_text[i] == "}":
            depth -= 1
        i += 1
    body = css_text[start:i - 1]
    out: dict[str, str] = {}
    for vm in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", body, re.I):
        out[vm.group(1)] = vm.group(2).strip()
    return out


def resolve_var(name: str, env: dict[str, str], seen: set[str] | None = None) -> str:
    seen = seen or set()
    if name in seen:
        raise AssertionError(f"Circular CSS variable reference: {name}")
    seen.add(name)
    val = env[name]
    m = re.fullmatch(r"var\(\s*(--[a-z0-9-]+)\s*\)", val, re.I)
    if m:
        return resolve_var(m.group(1), env, seen)
    return val


class ColorGeneratorTests(unittest.TestCase):
    PAIR_SPECS = (
        ("on-surface", "surface"),
        ("on-surface", "surface-container-low"),
        ("on-surface", "surface-container"),
        ("on-surface-variant", "surface"),
        ("on-surface-variant", "surface-container"),
        ("on-primary", "primary"),
        ("on-primary-container", "primary-container"),
        ("on-secondary", "secondary"),
        ("on-secondary-container", "secondary-container"),
        ("on-tertiary", "tertiary"),
        ("on-tertiary-container", "tertiary-container"),
        ("on-error", "error"),
        ("on-error-container", "error-container"),
        ("inverse-on-surface", "inverse-surface"),
        ("on-primary-fixed", "primary-fixed"),
        ("on-primary-fixed-variant", "primary-fixed-dim"),
        ("on-secondary-fixed", "secondary-fixed"),
        ("on-secondary-fixed-variant", "secondary-fixed-dim"),
        ("on-tertiary-fixed", "tertiary-fixed"),
        ("on-tertiary-fixed-variant", "tertiary-fixed-dim"),
    )

    def test_generated_schemes_meet_contrast_and_distinct_surfaces(self) -> None:
        seeds = ("#6750A4", "#0B57D0", "#146C2E", "#FFDE3F", "#00BCD4")
        contrasts = ((0.0, 4.5, 3.0), (0.5, 6.0, 4.5), (1.0, 7.0, 7.0))
        for seed in seeds:
            for variant in color_to_css.VARIANTS:
                for is_dark in (False, True):
                    for level, pair_min, outline_min in contrasts:
                        roles = color_to_css.generate_scheme(
                            seed,
                            variant=variant,
                            is_dark=is_dark,
                            contrast_level=level,
                            spec_version="2025",
                        )
                        label = f"{seed}/{variant}/dark={is_dark}/c={level}"
                        self.assertNotEqual(
                            roles["surface"],
                            roles["surface-container-low"],
                            f"Collapsed surface & surface-container-low in {label}",
                        )
                        for fg, bg in self.PAIR_SPECS:
                            cr = color_to_css.srgb_contrast_ratio(roles[fg], roles[bg])
                            self.assertGreaterEqual(
                                cr,
                                pair_min,
                                f"{label} pair {fg}/{bg} ({roles[fg]} on {roles[bg]})={cr:.2f} < {pair_min}",
                            )
                        outline_cr = color_to_css.srgb_contrast_ratio(roles["outline"], roles["surface"])
                        self.assertGreaterEqual(
                            outline_cr,
                            outline_min,
                            f"{label} outline/surface ({roles['outline']} on {roles['surface']})={outline_cr:.2f} < {outline_min}",
                        )

    def test_palettes_and_baseline_variants_are_in_sync(self) -> None:
        self.assertEqual(PALETTES_CSS.read_text(encoding="utf-8"), color_to_css.render_presets_css())
        tokens_css = TOKENS_CSS.read_text(encoding="utf-8")
        self.assertIn(color_to_css.render_base_variants_css(), tokens_css)


class ShapeTokenTests(unittest.TestCase):
    def test_shapes_css_in_sync_and_exposes_35_presets(self) -> None:
        css = SHAPES_CSS.read_text(encoding="utf-8")
        self.assertEqual(css, shapes_to_css.render_css())
        self.assertEqual(len(shapes_to_css.SHAPE_NAMES), 35)
        for name in shapes_to_css.SHAPE_NAMES:
            self.assertIn(f"--md-sys-shape-mask-{name}:", css)
            self.assertIn(f".md3e-shape-{name}", css)
        self.assertIn("-webkit-mask-image:", css)
        self.assertIn("mask-image:", css)
        self.assertIn('@supports (not (mask-image: url(""))) and (not (-webkit-mask-image: url("")))', css)

    def test_loading_indicator_7_polygons_uniform_36_cubics_and_bounds(self) -> None:
        css = SHAPES_CSS.read_text(encoding="utf-8")
        paths = shapes_to_css.compute_loading_paths()
        self.assertEqual(len(paths), 7)
        self.assertEqual([name for name, _ in paths], list(shapes_to_css.LOADING_SEQUENCE))
        self.assertIn("@keyframes md3e-loader-morph-7", css)
        for name, path_d in paths:
            self.assertEqual(path_d.count("C"), shapes_to_css.MORPH_SAMPLES, f"{name} cubic count mismatch")
            coords = [float(m) for m in re.findall(r"-?\d+(?:\.\d+)?", path_d)]
            self.assertTrue(coords, f"No coords in {name}")
            self.assertTrue(
                all(0.0 <= v <= 100.0 for v in coords),
                f"Out-of-bounds coord in {name}: min={min(coords)}, max={max(coords)}",
            )
            self.assertIn(path_d, css)


class ContrastTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.css = TOKENS_CSS.read_text(encoding="utf-8")
        base_only, gen_rest = cls.css.split("/* === BEGIN GENERATED BASELINE VARIANTS === */", 1)
        gen_section = gen_rest.split("/* === END GENERATED BASELINE VARIANTS === */", 1)[0]

        cls.light = extract_var_block(base_only, r":root\s*\{")
        # System dark block inside @media (prefers-color-scheme: dark)
        dark_media = re.search(
            r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root:where\(:not\(\[data-theme=\"light\"\]\)\)\s*\{([\s\S]*?)\n\s*\}\s*\}",
            base_only,
        )
        assert dark_media is not None, "Missing system dark colour block"
        cls.sys_dark = {
            **cls.light,
            **{m.group(1): m.group(2).strip() for m in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", dark_media.group(1))},
        }
        cls.explicit_dark = {**cls.light, **extract_var_block(base_only, r"\[data-theme=\"dark\"\]\s*\{")}
        cls.expressive_light = {**cls.light, **extract_var_block(gen_section, r'\[data-color-variant="expressive"\]\s*\{')}
        cls.expressive_dark = {
            **cls.explicit_dark,
            **extract_var_block(gen_section, r'\[data-color-variant="expressive"\]\[data-theme="dark"\]\s*\{'),
        }
        cls.vibrant_light = {**cls.light, **extract_var_block(gen_section, r'\[data-color-variant="vibrant"\]\s*\{')}
        cls.vibrant_dark = {
            **cls.explicit_dark,
            **extract_var_block(gen_section, r'\[data-color-variant="vibrant"\]\[data-theme="dark"\]\s*\{'),
        }
        seed_guard = r':where\(:not\(\[data-color-variant\]\)\):where\(:not\(\[data-seed\]\),\s*\[data-seed="purple"\]\)'
        cls.med_light = {
            **cls.light,
            **extract_var_block(
                base_only,
                rf'\[data-contrast="medium"\]{seed_guard}:not\(\[data-theme="dark"\]\)\s*\{{',
            ),
        }
        cls.med_dark = {
            **cls.explicit_dark,
            **extract_var_block(
                base_only,
                rf'\[data-theme="dark"\]\[data-contrast="medium"\]{seed_guard}\s*\{{',
            ),
        }
        cls.hc_light = {
            **cls.light,
            **extract_var_block(
                base_only,
                rf'\[data-contrast="high"\]{seed_guard}:not\(\[data-theme="dark"\]\)\s*\{{',
            ),
        }
        cls.hc_dark = {
            **cls.explicit_dark,
            **extract_var_block(
                base_only,
                rf'\[data-theme="dark"\]\[data-contrast="high"\]{seed_guard}\s*\{{',
            ),
        }

        hc_media = base_only.rsplit("@media (prefers-contrast: more)", 1)[1]
        cls.hc_media_light = {
            **cls.light,
            **extract_var_block(
                hc_media,
                r':is\(:root,\s*\[data-theme="light"\]\):where\(:not\(\[data-theme="dark"\]\):not\(\[data-color-variant\]\)[\s\S]*?:not\(\[data-contrast="medium"\]\)\)\s*\{',
            ),
        }
        cls.hc_media_dark = {
            **cls.explicit_dark,
            **extract_var_block(
                hc_media,
                r'\[data-theme="dark"\]:where\(:not\(\[data-color-variant\]\)[\s\S]*?:not\(\[data-contrast="medium"\]\)\)\s*\{',
            ),
        }

    def _assert_theme_contrast(self, env: dict[str, str], min_ratio: float, label: str) -> None:
        pairs = [
            ("--md-sys-color-primary", "--md-sys-color-on-primary"),
            ("--md-sys-color-primary-container", "--md-sys-color-on-primary-container"),
            ("--md-sys-color-secondary", "--md-sys-color-on-secondary"),
            ("--md-sys-color-secondary-container", "--md-sys-color-on-secondary-container"),
            ("--md-sys-color-tertiary", "--md-sys-color-on-tertiary"),
            ("--md-sys-color-tertiary-container", "--md-sys-color-on-tertiary-container"),
            ("--md-sys-color-error", "--md-sys-color-on-error"),
            ("--md-sys-color-error-container", "--md-sys-color-on-error-container"),
            ("--md-sys-color-surface", "--md-sys-color-on-surface"),
            ("--md-sys-color-surface-container-low", "--md-sys-color-on-surface"),
            ("--md-sys-color-surface-container", "--md-sys-color-on-surface"),
            ("--md-sys-color-surface-container-high", "--md-sys-color-on-surface-variant"),
            ("--md-sys-color-inverse-surface", "--md-sys-color-inverse-on-surface"),
        ]
        for bg_tok, fg_tok in pairs:
            bg = resolve_var(bg_tok, env)
            fg = resolve_var(fg_tok, env)
            ratio = contrast_ratio(bg, fg)
            self.assertGreaterEqual(
                ratio,
                min_ratio,
                f"[{label}] {bg_tok} ({bg}) vs {fg_tok} ({fg}) contrast {ratio:.2f}:1 < {min_ratio}:1",
            )

    def test_all_themes_meet_wcag_aa_and_medium_contrast(self) -> None:
        self._assert_theme_contrast(self.light, 4.5, "light")
        self._assert_theme_contrast(self.sys_dark, 4.5, "system-dark")
        self._assert_theme_contrast(self.explicit_dark, 4.5, "dark")
        self._assert_theme_contrast(self.expressive_light, 4.5, "expressive-light")
        self._assert_theme_contrast(self.expressive_dark, 4.5, "expressive-dark")
        self._assert_theme_contrast(self.vibrant_light, 4.5, "vibrant-light")
        self._assert_theme_contrast(self.vibrant_dark, 4.5, "vibrant-dark")
        self._assert_theme_contrast(self.med_light, 6.0, "medium-light")
        self._assert_theme_contrast(self.med_dark, 6.0, "medium-dark")

    def test_high_contrast_light_and_dark_meet_aaa_and_never_collapse(self) -> None:
        self._assert_theme_contrast(self.hc_light, 7.0, "hc-light")
        self._assert_theme_contrast(self.hc_dark, 7.0, "hc-dark")
        self._assert_theme_contrast(self.hc_media_light, 7.0, "hc-media-light")
        self._assert_theme_contrast(self.hc_media_dark, 7.0, "hc-media-dark")
        self.assertNotEqual(
            resolve_var("--md-sys-color-primary-container", self.hc_dark),
            resolve_var("--md-sys-color-on-primary-container", self.hc_dark),
        )

    def test_system_dark_sets_all_surface_roles(self) -> None:
        self.assertEqual(resolve_var("--md-sys-color-surface", self.sys_dark), "#141218")
        self.assertNotEqual(
            resolve_var("--md-sys-color-surface", self.sys_dark),
            resolve_var("--md-sys-color-surface-container-low", self.sys_dark),
        )
        self.assertEqual(resolve_var("--md-sys-icon-grade", self.sys_dark), "-25")

    def test_variants_genuinely_diverge_from_baseline(self) -> None:
        self.assertNotEqual(
            resolve_var("--md-sys-color-primary", self.vibrant_dark),
            resolve_var("--md-sys-color-primary", self.explicit_dark),
        )
        self.assertNotEqual(
            resolve_var("--md-sys-color-surface", self.vibrant_dark),
            resolve_var("--md-sys-color-surface", self.explicit_dark),
        )
        self.assertNotEqual(
            resolve_var("--md-sys-color-secondary", self.expressive_dark),
            resolve_var("--md-sys-color-secondary", self.explicit_dark),
        )
        self.assertNotEqual(
            resolve_var("--md-sys-color-tertiary", self.vibrant_light),
            resolve_var("--md-sys-color-tertiary", self.light),
        )

    def test_icon_defensive_rules_and_cjk_adaptation_present(self) -> None:
        self.assertIn("inline-size: 1em;", self.css)
        self.assertIn("block-size: 1em;", self.css)
        self.assertIn("overflow: hidden;", self.css)
        self.assertIn(":lang(zh)", self.css)
        self.assertIn("--md-sys-icon-fill: 1;", self.css)


class MotionTokenTests(unittest.TestCase):
    def test_generated_motion_css_is_up_to_date(self) -> None:
        expected = spring_to_css.render_css().replace("\r\n", "\n")
        actual = MOTION_CSS.read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(actual, expected, "md3e-motion.css is out of sync with spring_to_css.py")

    def test_motion_split_tokens_and_reduced_motion_and_effects_bounds(self) -> None:
        css = MOTION_CSS.read_text(encoding="utf-8")
        for speed in ("fast", "default", "slow"):
            for kind in ("spatial", "effects"):
                self.assertIn(f"--md-sys-motion-{speed}-{kind}-duration:", css)
                self.assertIn(f"--md-sys-motion-{speed}-{kind}-easing:", css)
                self.assertIn(f"--md-sys-motion-{speed}-{kind}:", css)
                self.assertIn(f"--md-sys-motion-{speed}-{kind}-bezier-duration:", css)
                self.assertIn(f"--md-sys-motion-{speed}-{kind}-bezier-easing:", css)
                self.assertIn(f"--md-sys-motion-{speed}-{kind}-bezier:", css)

        self.assertIn('[data-motion-driver="bezier"]', css)

        # Effects springs must never overshoot [0, 1]
        for m in re.finditer(r"--md-sys-motion-(?:fast|default|slow)-effects-easing:\s*linear\(([^)]+)\)", css):
            stops = [float(x.strip()) for x in m.group(1).split(",")]
            self.assertTrue(all(0.0 <= v <= 1.0 for v in stops), f"Effects easing overshoots: {stops}")

        # Reduced motion zeroes spatial tokens (including -bezier and bezier driver selectors)
        reduced_block = css.split("@media (prefers-reduced-motion: reduce)", 1)[1]
        self.assertIn('[data-motion-driver="bezier"]', reduced_block)
        self.assertIn("--md-sys-motion-default-spatial: 0ms linear;", reduced_block)
        self.assertIn("--md-sys-motion-fast-spatial-bezier: 0ms linear;", reduced_block)
        self.assertIn("--md-sys-motion-fast-effects: 120ms cubic-bezier(0, 0, 1, 1);", reduced_block)

        # Fallback @supports not uses official Web curves, not linear(0,0,1,1) for spatial
        fallback_block = css.split("@supports not (transition-timing-function: linear(0, 1))", 1)[1].split("@media", 1)[0]
        self.assertIn("cubic-bezier(0.42, 1.67, 0.21, 0.90)", fallback_block)


class SemanticPrimitivesAndZeroMwcTests(unittest.TestCase):
    def test_legacy_material_web_assets_and_refs_removed(self) -> None:
        self.assertFalse((ROOT_DIR / "assets" / "tokens" / "md3e-material-web.css").exists())
        self.assertFalse((REFERENCES_DIR / "material-web.md").exists())

        banned = re.compile(r"@material/web|md3e-material-web|esm\.run/@material/web|</?md-[a-z]", re.IGNORECASE)
        scan_files = [SKILL_MD, ROOT_DIR / "README.md", OFFICIAL_AUDIT_MD]
        scan_files.extend(sorted(REFERENCES_DIR.rglob("*.md")))
        scan_files.extend(sorted((ROOT_DIR / "assets").rglob("*")))
        offenders: list[tuple[str, int, str]] = []
        for fp in scan_files:
            if not fp.is_file():
                continue
            for idx, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), start=1):
                if banned.search(line):
                    offenders.append((fp.name, idx, line.strip()[:100]))
        self.assertEqual(offenders, [], f"Legacy @material/web/<md-*> references remain: {offenders}")

    def test_starter_native_primitives_and_headless_guidance(self) -> None:
        html = STARTER_HTML.read_text(encoding="utf-8")
        for variant in ("filled", "tonal", "elevated", "outlined", "text"):
            self.assertIn(f".md3e-btn--{variant}", html)
        for size in ("xs", "s", "m", "l", "xl"):
            self.assertIn(f".md3e-btn--{size}", html)
        self.assertIn(".md3e-btn--square", html)
        self.assertIn(".md3e-btn::before", html)
        self.assertIn("calc(var(--md-btn-h) / 2)", html)
        for selector in (
            'id="section-primitives"',
            'id="prim-switch"',
            'id="prim-checkbox"',
            'id="prim-text-field"',
            'id="volume-slider"',
            'id="prim-dialog"',
            ".md3e-fab--medium",
        ):
            self.assertIn(selector, html)

        for doc in (
            SKILL_MD,
            ROOT_DIR / "README.md",
            REFERENCES_DIR / "components.md",
            REFERENCES_DIR / "components" / "expressive-recipes.md",
        ):
            text = doc.read_text(encoding="utf-8")
            self.assertIn("Radix UI", text, f"Missing Radix UI guidance in {doc.name}")
            self.assertIn("Base UI", text, f"Missing Base UI guidance in {doc.name}")


class TypographyAndDesktopTokenTests(unittest.TestCase):
    EXPECTED_TYPESCALE = {
        "display-large": ("57px", "64px", "400", "500"),
        "display-medium": ("45px", "52px", "400", "500"),
        "display-small": ("36px", "44px", "400", "500"),
        "headline-large": ("32px", "40px", "400", "500"),
        "headline-medium": ("28px", "36px", "400", "500"),
        "headline-small": ("24px", "32px", "400", "500"),
        "title-large": ("22px", "28px", "400", "500"),
        "title-medium": ("16px", "24px", "500", "700"),
        "title-small": ("14px", "20px", "500", "700"),
        "body-large": ("16px", "24px", "400", "500"),
        "body-medium": ("14px", "20px", "400", "500"),
        "body-small": ("12px", "16px", "400", "500"),
        "label-large": ("14px", "20px", "500", "700"),
        "label-medium": ("12px", "16px", "500", "700"),
        "label-small": ("11px", "16px", "500", "700"),
    }

    def test_all_30_typescale_styles_matching_size_line_height_and_cjk(self) -> None:
        css = TOKENS_CSS.read_text(encoding="utf-8")
        root_vars = extract_var_block(css, r":root\s*\{")
        for role, (size, lh, weight, emph_weight) in self.EXPECTED_TYPESCALE.items():
            prefix = f"--md-sys-typescale-{role}"
            for suffix in (
                "-font", "-size", "-line-height", "-weight", "-tracking",
                "-emphasized-weight", "-emphasized-tracking",
            ):
                self.assertIn(f"{prefix}{suffix}", root_vars, f"Missing {prefix}{suffix}")
            self.assertEqual(root_vars[f"{prefix}-size"], size, f"{role} size mismatch")
            self.assertEqual(root_vars[f"{prefix}-line-height"], lh, f"{role} line-height mismatch")
            self.assertEqual(root_vars[f"{prefix}-weight"], weight, f"{role} weight mismatch")
            self.assertEqual(root_vars[f"{prefix}-emphasized-weight"], emph_weight, f"{role} emphasized weight mismatch")
            if f"{prefix}-emphasized-size" in root_vars:
                self.assertEqual(root_vars[f"{prefix}-emphasized-size"], size)
            if f"{prefix}-emphasized-line-height" in root_vars:
                self.assertEqual(root_vars[f"{prefix}-emphasized-line-height"], lh)

        cjk_vars = extract_var_block(css, r":lang\(zh\)[\s\S]*?\{")
        for role, (_, base_lh, _, _) in self.EXPECTED_TYPESCALE.items():
            tok = f"--md-sys-typescale-{role}-line-height"
            self.assertIn(tok, cjk_vars, f"Missing {tok} in :lang(zh) CJK override")
            base_px = float(base_lh.rstrip("px"))
            cjk_px = float(cjk_vars[tok].rstrip("px"))
            self.assertGreater(cjk_px, base_px, f"CJK {tok} ({cjk_px}px) must exceed base ({base_px}px)")

    def test_desktop_layout_and_density_tokens_defined(self) -> None:
        css = TOKENS_CSS.read_text(encoding="utf-8")
        root_vars = extract_var_block(css, r":root\s*\{")
        required_desktop_tokens = (
            "--md-sys-nav-rail-width-collapsed",
            "--md-sys-nav-rail-width-expanded",
            "--md-sys-density-offset",
            "--md-sys-layout-pane-gap",
            "--md-sys-layout-measure-max",
        )
        for tok in required_desktop_tokens:
            self.assertIn(tok, root_vars, f"Missing desktop token {tok} in md3e-tokens.css")
        self.assertIn('[data-density="compact"]', css)
        self.assertIn('[data-density="dense"]', css)


class CrossReferenceAndStructuralTests(unittest.TestCase):
    DESKTOP_LAYOUT_DENSITY_TOKENS = (
        "--md-sys-nav-rail-width-collapsed",
        "--md-sys-nav-rail-width-expanded",
        "--md-sys-density-offset",
        "--md-sys-layout-pane-gap",
        "--md-sys-layout-measure-max",
    )

    def test_cross_reference_var_integrity(self) -> None:
        defined_tokens: set[str] = set()
        for css_file in sorted((ROOT_DIR / "assets" / "tokens").glob("*.css")):
            cleaned = audit_md3e.strip_css_comments(css_file.read_text(encoding="utf-8"))
            defined_tokens.update(re.findall(r"(--md(?:3e)?-[a-z0-9-]+)\s*:", cleaned))

        targets = (TAILWIND_THEME_CSS, TAILWIND_CONFIG_JS, STARTER_HTML)
        for target in targets:
            raw = target.read_text(encoding="utf-8")
            cleaned = audit_md3e.strip_css_comments(raw)
            local_defs = set(re.findall(r"(--md(?:3e)?-[a-z0-9-]+)\s*:", cleaned))
            refs = set(re.findall(r"var\(\s*(--md(?:3e)?-[a-z0-9-]+)", cleaned))
            missing = sorted(refs - defined_tokens - local_defs)
            self.assertEqual(missing, [], f"Undefined CSS vars in {target.name}: {missing}")

        for tw_file in (TAILWIND_THEME_CSS, TAILWIND_CONFIG_JS):
            tw_text = tw_file.read_text(encoding="utf-8")
            for tok in self.DESKTOP_LAYOUT_DENSITY_TOKENS:
                self.assertIn(
                    tok,
                    tw_text,
                    f"Desktop layout/density token {tok} should be exposed in {tw_file.name}",
                )

    def test_starter_html_structural_and_desktop_wiring(self) -> None:
        html = STARTER_HTML.read_text(encoding="utf-8")
        markup = audit_md3e.strip_html_comments(
            audit_md3e.strip_tag_blocks(audit_md3e.strip_tag_blocks(html, "script"), "style")
        )

        # 1. Unique ID attributes (no duplicates)
        ids = re.findall(r"""\bid\s*=\s*(?:"([^"]+)"|'([^']+)')""", markup, re.I)
        flat_ids = [a or b for a, b in ids]
        self.assertTrue(flat_ids, "Expected id attributes in starter HTML")
        duplicates = sorted({i for i in flat_ids if flat_ids.count(i) > 1})
        self.assertEqual(duplicates, [], f"Duplicate id attributes in starter HTML: {duplicates}")
        id_set = set(flat_ids)

        # 2. Valid aria-controls / aria-labelledby targets
        for attr_name in ("aria-controls", "aria-labelledby"):
            for m in re.finditer(rf"""\b{attr_name}\s*=\s*(?:"([^"]+)"|'([^']+)')""", markup, re.I):
                val = (m.group(1) or m.group(2) or "").strip()
                self.assertTrue(val, f"Empty {attr_name} attribute in starter HTML")
                for ref_id in val.split():
                    self.assertIn(ref_id, id_set, f"{attr_name}=\"{val}\" targets missing id #{ref_id}")

        # 3. Alphabetical Material Symbols Google Fonts URL axis order
        ms_matches = list(audit_md3e.MS_FONT_AXES_RE.finditer(markup))
        self.assertTrue(ms_matches, "Expected Material Symbols Google Fonts <link> in starter HTML")
        for m in ms_matches:
            raw_axes = [a.strip() for a in m.group(1).split(",") if a.strip()]
            expected = sorted((audit_md3e.CANONICAL_MS_AXES.get(a.lower(), a) for a in raw_axes), key=str.lower)
            self.assertEqual(raw_axes, expected, f"Non-alphabetical Material Symbols axes: {m.group(1)}")

        # 4. Presence of all 35 .md3e-shape-<name> tiles
        static_tiles = set(re.findall(r"\bmd3e-shape-([a-z0-9-]+)\b", markup))
        js_names_match = re.search(r"const\s+SHAPE_NAMES\s*=\s*\[([\s\S]*?)\]", html)
        js_tiles: set[str] = set()
        if js_names_match and "md3e-shape-" in html:
            js_tiles = set(re.findall(r"['\"]([a-z0-9-]+)['\"]", js_names_match.group(1)))
        for name in shapes_to_css.SHAPE_NAMES:
            self.assertTrue(
                name in static_tiles or name in js_tiles,
                f"Missing .md3e-shape-{name} tile in starter HTML",
            )

        # 5. Desktop Optimization wiring (data-density, expandable rail, side sheet toggle)
        self.assertRegex(html, r"data-density|dataset\.density", "Starter HTML must wire data-density toggle")
        aria_ctrl_pairs = [
            (m.group(0), (m.group(1) or m.group(2) or "").strip())
            for m in re.finditer(r"""<button\b[^>]*\baria-controls\s*=\s*(?:"([^"]+)"|'([^']+)')[^>]*>""", markup, re.I)
        ]
        self.assertTrue(
            any("rail" in target or "nav" in target for _, target in aria_ctrl_pairs),
            "Starter HTML must wire an expandable rail/nav control with aria-controls",
        )
        self.assertTrue(
            any("side-sheet" in target or "inspector" in target or "sheet" in target for _, target in aria_ctrl_pairs)
            and re.search(r"side-sheet|inspector", markup, re.I),
            "Starter HTML must wire a Side Sheet toggle with aria-controls",
        )

    def test_starter_m3e_slider_fab_menu_switch_and_checkbox_specs(self) -> None:
        html = STARTER_HTML.read_text(encoding="utf-8")
        rules: list[audit_md3e.RuleBlock] = []
        for blk, start_line in audit_md3e.extract_style_blocks(html):
            rules.extend(audit_md3e.parse_css_rules(blk, base_line=start_line))

        def decls_for(sel_predicate) -> dict[str, list[str]]:
            collected: dict[str, list[str]] = {}
            for rule in rules:
                branches = audit_md3e.split_top_level_commas(rule.selector)
                if any(sel_predicate(b.strip()) for b in branches):
                    for prop, val, _, _ in rule.declarations:
                        collected.setdefault(prop, []).append(audit_md3e.strip_important(val).lower())
            return collected

        # 1. Both .wavy-slider and .md3e-range strip OS appearance and render 4x44px vertical handle
        for cls_name in (".wavy-slider", ".md3e-range"):
            base_decls = decls_for(lambda b, c=cls_name: b == c)
            self.assertIn(
                "none",
                base_decls.get("appearance", []),
                f"{cls_name} must declare `appearance: none` to remove OS grey borders",
            )
            thumb_decls = decls_for(
                lambda b, c=cls_name: b in (f"{c}::-webkit-slider-thumb", f"{c}::-moz-range-thumb")
            )
            thumb_widths = thumb_decls.get("width", []) + thumb_decls.get("inline-size", [])
            thumb_heights = thumb_decls.get("height", []) + thumb_decls.get("block-size", [])
            self.assertIn("4px", thumb_widths, f"{cls_name} thumb must use 4px vertical bar handle width")
            self.assertIn("44px", thumb_heights, f"{cls_name} thumb must use 44px vertical bar handle height")

        # 2. Fixed .fab-menu-container sets pointer-events: none to prevent hit-traps
        fab_wrap_fixed = [
            rule
            for rule in rules
            if any(b.strip() == ".fab-menu-container" for b in audit_md3e.split_top_level_commas(rule.selector))
            and any(p == "position" and audit_md3e.strip_important(v).lower() == "fixed" for p, v, _, _ in rule.declarations)
        ]
        self.assertTrue(fab_wrap_fixed, "Expected fixed .fab-menu-container rule in starter HTML")
        self.assertTrue(
            all(
                any(p == "pointer-events" and audit_md3e.strip_important(v).lower() == "none" for p, v, _, _ in r.declarations)
                for r in fab_wrap_fixed
            ),
            ".fab-menu-container with position: fixed must declare pointer-events: none",
        )

        # 3. Switch :active pressed thumb expands to 28x28px
        switch_active_decls = decls_for(
            lambda b: ".md3e-switch" in b and ":active" in b and "::after" in b
        )
        sw_widths = switch_active_decls.get("width", []) + switch_active_decls.get("inline-size", [])
        sw_heights = switch_active_decls.get("height", []) + switch_active_decls.get("block-size", [])
        self.assertIn("28px", sw_widths, ".md3e-switch :active thumb must expand to 28px width")
        self.assertIn("28px", sw_heights, ".md3e-switch :active thumb must expand to 28px height")

        # 4. Checkbox aligns to 18x18px container sizing
        checkbox_decls = decls_for(lambda b: b == ".md3e-checkbox")
        cb_widths = checkbox_decls.get("width", []) + checkbox_decls.get("inline-size", [])
        cb_heights = checkbox_decls.get("height", []) + checkbox_decls.get("block-size", [])
        self.assertIn("18px", cb_widths, ".md3e-checkbox width must be 18px")
        self.assertIn("18px", cb_heights, ".md3e-checkbox height must be 18px")


class AuditorTests(unittest.TestCase):
    def _codes(self, text: str, filename: str = "sample.html", *, is_snippet: bool = False) -> list[str]:
        findings = audit_md3e.Checker(pathlib.Path(filename), is_snippet=is_snippet).run(text)
        return [f.code for f in findings]

    def _findings(self, text: str, filename: str = "sample.html", *, is_snippet: bool = False) -> list[audit_md3e.Finding]:
        return audit_md3e.Checker(pathlib.Path(filename), is_snippet=is_snippet).run(text)

    def test_shipped_assets_and_all_22_markdown_docs_pass_compliance(self) -> None:
        reports, scanned = audit_md3e.audit([str(ROOT_DIR / "assets")], [], mode="strict")
        self.assertEqual(scanned, 14)
        self.assertEqual(reports, [], f"Unexpected strict asset findings: {reports}")

        for bento_mode in ("desktop-bento", "personal-studio"):
            bento_reports, bento_scanned = audit_md3e.audit(
                [str(BENTO_HTML)],
                [],
                mode=bento_mode,
            )
            self.assertEqual(bento_scanned, 1)
            self.assertEqual(bento_reports, [], f"Unexpected {bento_mode} HTML findings: {bento_reports}")

        md_reports, md_scanned = audit_md3e.audit(
            [str(SKILL_MD), str(ROOT_DIR / "README.md"), str(OFFICIAL_AUDIT_MD), str(REFERENCES_DIR)],
            [],
            include_markdown=True,
            mode="strict",
        )
        self.assertEqual(md_scanned, 22)
        self.assertEqual(md_reports, [], f"Unexpected markdown compliance findings across 22 docs: {md_reports}")

        for doc_path, doc_mode in (
            (REFERENCES_DIR / "desktop-bento.md", "desktop-bento"),
            (REFERENCES_DIR / "personal-studio.md", "personal-studio"),
        ):
            doc_reports, doc_scanned = audit_md3e.audit(
                [str(doc_path)],
                [],
                include_markdown=True,
                mode=doc_mode,
            )
            self.assertEqual(doc_scanned, 1)
            self.assertEqual(doc_reports, [], f"Unexpected {doc_mode} markdown findings in {doc_path.name}: {doc_reports}")

    def test_md3e017_catches_non_alphabetical_google_fonts_axes(self) -> None:
        bad_html = (
            '<!doctype html><html><head>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block">'
            '</head><body><button type="button" aria-label="Add"><span class="material-symbols-outlined" aria-hidden="true">add</span></button></body></html>'
        )
        bad_findings = [f for f in self._findings(bad_html) if f.code == "MD3E017"]
        self.assertEqual(len(bad_findings), 1)
        self.assertEqual(bad_findings[0].severity, "error")
        self.assertIn("FILL,GRAD,opsz,wght", bad_findings[0].fix)

        good_html = (
            '<!doctype html><html><head>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:FILL,GRAD,opsz,wght@0..1,-50..200,20..48,100..700&display=block">'
            '</head><body><button type="button" aria-label="Add"><span class="material-symbols-outlined" aria-hidden="true">add</span></button></body></html>'
        )
        self.assertNotIn("MD3E017", self._codes(good_html))

        bad_css_import = "@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:wght,opsz@400,24&display=block');"
        self.assertIn("MD3E017", self._codes(bad_css_import, "icons.css"))

        bad_case_html = (
            '<!doctype html><html><head>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:fill,grad,opsz,wght@0..1,-50..200,20..48,100..700&display=block">'
            '</head><body></body></html>'
        )
        self.assertIn("MD3E017", self._codes(bad_case_html))

    def test_hardened_auditor_edge_cases(self) -> None:
        # MD3E018: in oklch on neutral/surface variables is an ERROR, while in oklab passes
        oklch_neutral = ".card { background: color-mix(in oklch, var(--md-sys-color-surface-container) 82%, transparent); }"
        oklch_findings = [f for f in self._findings(oklch_neutral, "oklch.css") if f.code == "MD3E018"]
        self.assertEqual(len(oklch_findings), 1)
        self.assertEqual(oklch_findings[0].severity, "error")

        oklab_good = ".btn:hover { background: color-mix(in oklab, var(--md-sys-color-surface-container) 82%, transparent); color: color-mix(in srgb, currentColor calc(100% * var(--md-sys-state-hover-state-layer-opacity)), transparent); }"
        self.assertNotIn("MD3E018", self._codes(oklab_good, "oklab.css"))

        # MD3E004: mixed var() + ad-hoc segment in transition still caught; MD3E019 -bezier composite caught
        mixed_motion = ".card { transition: opacity var(--md-sys-motion-fast-effects), transform 300ms ease-in-out; }"
        self.assertIn("MD3E004", self._codes(mixed_motion, "mixed.css"))
        bad_bezier_anim = ".loader { animation: spin 2.4s var(--md-sys-motion-default-spatial-bezier) infinite; }"
        self.assertIn("MD3E019", self._codes(bad_bezier_anim, "bezier.css"))

        # MD3E014: multi-line labelled native icon button must not false-positive
        good_multiline_icon_btn = '<button type="button" class="md3e-icon-btn"\n  aria-label="Settings"\n>\n  <span class="material-symbols-outlined" aria-hidden="true">settings</span>\n</button>'
        self.assertNotIn("MD3E014", self._codes(good_multiline_icon_btn))
        bad_empty_icon_btn = '<button type="button" class="md3e-icon-btn"><span class="material-symbols-outlined" aria-hidden="true">settings</span></button>'
        self.assertIn("MD3E014", self._codes(bad_empty_icon_btn))

        # MD3E020 legacy <md-*> rejection & MD3E021 exact line number on multi-line control
        legacy_md = '<md-outlined-text-field label="Name"></md-outlined-text-field>'
        m020_legacy = [f for f in self._findings(legacy_md) if f.code == "MD3E020"]
        self.assertEqual(len(m020_legacy), 1)
        self.assertEqual(m020_legacy[0].severity, "error")
        multiline_a11y = '<button type="button" class="md3e-fab--medium" aria-label="Add">\n  <span class="material-symbols-outlined">add</span>\n</button>'
        m021 = [f for f in self._findings(multiline_a11y) if f.code == "MD3E021"]
        self.assertEqual(len(m021), 1)
        self.assertEqual(m021[0].line, 2)

        # MD3E022: comment mentioning prefers-reduced-transparency must not suppress error
        comment_bypass = "/* prefers-reduced-transparency: reduce */\n.bar { backdrop-filter: blur(16px); }"
        m022 = [f for f in self._findings(comment_bypass, "comment.css") if f.code == "MD3E022"]
        self.assertEqual(len(m022), 1)
        self.assertEqual(m022[0].severity, "error")

    def test_inline_html_style_and_color_checks(self) -> None:
        html = '<div style="background: #ff0000; color: rgba(0, 0, 0, 0.5); border-radius: 10px; font-size: 13px;">Hi</div>'
        codes = self._codes(html)
        self.assertIn("MD3E001", codes)
        self.assertIn("MD3E002", codes)
        self.assertIn("MD3E003", codes)
        self.assertIn("MD3E007", codes)

    def test_touch_target_hit_area_vs_visual_inflation(self) -> None:
        good_css = """
        .btn-xs { height: 32px; position: relative; }
        .btn-xs::before { content: ""; position: absolute; inset-block: -8px; min-height: var(--md-sys-touch-target-min); min-width: 48px; }
        """
        self.assertNotIn("MD3E006", self._codes(good_css, "good.css"))

        inflated_css = ".btn-xs { height: 32px; min-height: 48px; }"
        inflated_f = [f for f in self._findings(inflated_css, "bad.css") if f.code == "MD3E006"]
        self.assertEqual(len(inflated_f), 1)
        self.assertEqual(inflated_f[0].severity, "warning")

        bare_small_css = ".btn-xs { height: 32px; }"
        bare_f = [f for f in self._findings(bare_small_css, "small.css") if f.code == "MD3E006"]
        self.assertEqual(len(bare_f), 1)
        self.assertEqual(bare_f[0].severity, "warning")

        sub_wcag_css = ".btn-tiny { height: 18px; }"
        sub_wcag_f = [f for f in self._findings(sub_wcag_css, "tiny.css") if f.code == "MD3E006"]
        self.assertEqual(len(sub_wcag_f), 1)
        self.assertEqual(sub_wcag_f[0].severity, "error")

    def test_motion_reduced_motion_and_official_web_curve(self) -> None:
        no_rm_css = ".card { transition: transform var(--md-sys-motion-default-spatial); }"
        self.assertIn("MD3E008", self._codes(no_rm_css, "anim.css"))

        # Official Google Web curve is a first-class valid Web implementation (zero MD3E004)
        official_curve_css = ".card { transition: transform 350ms cubic-bezier(0.42, 1.67, 0.21, 0.90); }"
        findings = self._findings(official_curve_css, "web.css")
        m004 = [f for f in findings if f.code == "MD3E004"]
        self.assertEqual(m004, [])

        ad_hoc_css = ".card { transition: transform 300ms ease-in-out; }"
        m004_bad = [f for f in self._findings(ad_hoc_css, "bad.css") if f.code == "MD3E004"]
        self.assertEqual(len(m004_bad), 1)
        self.assertEqual(m004_bad[0].severity, "warning")

    def test_new_checks_md3e017_to_md3e026(self) -> None:
        # MD3E017: bad icon names + missing Material Symbols <link>
        bad_icons = '<!doctype html><html><body><span class="material-symbols-outlined">trash</span><span class="material-symbols-outlined">chevron-down</span></body></html>'
        codes = self._codes(bad_icons)
        self.assertGreaterEqual(codes.count("MD3E017"), 3)

        # MD3E018: unitless opacity in color-mix()
        bad_mix = ".btn:hover { background: color-mix(in srgb, currentColor 0.08, transparent); }"
        self.assertIn("MD3E018", self._codes(bad_mix, "mix.css"))
        bad_mix_var = ".btn:hover { background: color-mix(in srgb, currentColor var(--md-sys-state-hover-state-layer-opacity), transparent); }"
        self.assertIn("MD3E018", self._codes(bad_mix_var, "mixvar.css"))

        # MD3E019: composite animation token delay + 9999px morph snap
        bad_anim = ".loader { animation: spin 2.4s var(--md-sys-motion-default-spatial) infinite; }"
        self.assertIn("MD3E019", self._codes(bad_anim, "loader.css"))
        bad_morph = ".pill { border-radius: var(--md-sys-shape-corner-full); transition: border-radius var(--md-sys-motion-default-spatial); }"
        self.assertIn("MD3E019", self._codes(bad_morph, "morph.css"))

        # MD3E020: legacy @material/web ref, missing ARIA checked/tabindex, invalid ARIA boolean, TSX inline style
        bad_mwc_import = "import '@material/web/button/filled-button.js';"
        self.assertIn("MD3E020", self._codes(bad_mwc_import, "app.ts"))
        bad_mwc_css = "@import './md3e-material-web.css';"
        self.assertIn("MD3E020", self._codes(bad_mwc_css, "app.css"))
        bad_aria = (
            '<div role="button">Click</div>\n'
            '<input type="checkbox" role="switch" id="s1">\n'
            '<button type="button" aria-pressed="yes">Toggle</button>'
        )
        m020_aria = [f for f in self._findings(bad_aria) if f.code == "MD3E020"]
        self.assertEqual(len(m020_aria), 3)
        good_headless_tsx = (
            'export const Toggle = (props: any) => (\n'
            '  <div role="button" {...props} style={{ color: "var(--md-sys-color-primary)" }} aria-pressed={true}>OK</div>\n'
            ');'
        )
        self.assertEqual([f for f in self._findings(good_headless_tsx, "Toggle.tsx") if f.code == "MD3E020"], [])

        # MD3E026: unbound modifier classes and legacy bridge scaling classes
        unbound_cls = (
            '<button type="button" class="md3e-btn--filled">No base</button>\n'
            '<div class="md3e-shape-sunny">No shape base</div>\n'
            '<div class="md3e-blur--lg">No blur base</div>\n'
            '<button type="button" class="md3e-size-m">Legacy bridge size</button>'
        )
        m026 = [f for f in self._findings(unbound_cls) if f.code == "MD3E026"]
        self.assertEqual(len(m026), 4)
        self.assertTrue(all(f.severity == "warning" for f in m026))

        # MD3E021: decorative icon missing aria-hidden="true"
        bad_a11y_icon = '<button type="button"><span class="material-symbols-outlined">send</span> Publish</button>'
        self.assertIn("MD3E021", self._codes(bad_a11y_icon))

        # MD3E014: multi-line icon-only button without aria-label
        multiline_icon_btn = '<button type="button">\n  <span class="material-symbols-outlined" aria-hidden="true">delete</span>\n</button>'
        self.assertIn("MD3E014", self._codes(multiline_icon_btn))

    def test_md3e022_backdrop_blur_requires_reduced_transparency(self) -> None:
        unguarded_css = ".bar { backdrop-filter: blur(16px); }"
        self.assertIn("MD3E022", self._codes(unguarded_css, "bar.css"))

        unguarded_inline = '<div style="-webkit-backdrop-filter: blur(12px);">Toolbar</div>'
        self.assertIn("MD3E022", self._codes(unguarded_inline, "bar.html"))

        guarded_css = """
        .bar {
          background: var(--md-sys-color-surface-container-high);
          backdrop-filter: blur(16px);
        }
        @media (prefers-reduced-transparency: reduce) {
          .bar { backdrop-filter: none; background: var(--md-sys-color-surface-container-high); }
        }
        """
        self.assertNotIn("MD3E022", self._codes(guarded_css, "guarded.css"))

    def test_md3e027_slider_appearance_and_fixed_menu_hit_trap(self) -> None:
        # Positive catches: OS accent-color slider without appearance: none
        for bad_slider_css in (
            ".wavy-slider { min-height: 48px; accent-color: var(--md-sys-color-primary); }",
            'input[type="range"] { accent-color: var(--md-sys-color-primary); }',
            ".md3e-range { min-height: var(--md-sys-touch-target-min); accent-color: var(--md-sys-color-primary); }",
        ):
            findings = [f for f in self._findings(bad_slider_css, "md3e-slider.css") if f.code == "MD3E027"]
            self.assertEqual(len(findings), 1, f"Expected MD3E027 warning for: {bad_slider_css}")
            self.assertEqual(findings[0].severity, "warning")

        # Positive catches: fixed FAB / floating menu wrapper without pointer-events: none
        for bad_menu_css in (
            ".fab-menu-container { position: fixed; bottom: 16px; right: 16px; z-index: 130; }",
            ".md3e-fab-menu-container { position: fixed; inset-block-end: 16px; inset-inline-end: 16px; }",
            ".floating-menu-wrap { position: fixed; bottom: 24px; right: 24px; pointer-events: auto; }",
        ):
            findings = [f for f in self._findings(bad_menu_css, "fab.css") if f.code == "MD3E027"]
            self.assertEqual(len(findings), 1, f"Expected MD3E027 warning for: {bad_menu_css}")
            self.assertEqual(findings[0].severity, "warning")

        # Valid passes: custom slider with appearance: none, fixed wrapper with pointer-events: none,
        # non-control layout wrappers (.slider-block / .slider-wrap / .slider-row / .slider-label / .track-row),
        # and pseudo-elements.
        valid_css = """
        .md3e-range {
          -webkit-appearance: none;
          appearance: none;
          width: 100%;
          min-height: var(--md-sys-touch-target-min);
          accent-color: var(--md-sys-color-primary);
          background: transparent;
        }
        .wavy-slider {
          -webkit-appearance: none;
          appearance: none;
          min-height: var(--md-sys-touch-target-min);
          background: transparent;
        }
        .md3e-range::-webkit-slider-thumb {
          appearance: none;
          width: 4px;
          height: 44px;
        }
        .slider-block,
        .slider-wrap,
        .slider-row,
        .slider-label,
        .track-row {
          display: flex;
          flex-direction: column;
          accent-color: var(--md-sys-color-primary);
        }
        .fab-menu-container {
          position: fixed;
          inset-block-end: var(--md-sys-spacing-4);
          inset-inline-end: var(--md-sys-spacing-4);
          pointer-events: none;
          z-index: 130;
        }
        .fab-menu-container.is-open {
          z-index: 900;
        }
        """
        self.assertEqual([f for f in self._findings(valid_css, "valid.css") if f.code == "MD3E027"], [])

    def test_auditor_spec_alignment_motion_and_subelements(self) -> None:
        # MD3E004: official first segment must not mask an ad-hoc second segment
        mixed_official_then_adhoc = (
            ".card { transition: opacity 200ms cubic-bezier(0.2, 0, 0, 1), transform 300ms ease-in-out; }"
        )
        self.assertIn("MD3E004", self._codes(mixed_official_then_adhoc, "mixed2.css"))

        # MD3E004: short linear crossfade inside prefers-reduced-motion is valid
        rm_crossfade = """
        .card { transition: opacity var(--md-sys-motion-fast-effects); }
        @media (prefers-reduced-motion: reduce) {
          .card { transition: opacity 120ms linear; }
        }
        """
        self.assertNotIn("MD3E004", self._codes(rm_crossfade, "rm.css"))

        # MD3E006: switch visual subelements (__thumb / __track) must not trigger target-size failures
        switch_subelements = """
        .md3e-switch { width: 52px; height: 32px; position: relative; }
        .md3e-switch::before { content: ""; position: absolute; inset-block: -8px; min-height: 48px; min-width: 48px; }
        .md3e-switch__track { width: 52px; height: 32px; }
        .md3e-switch__thumb { width: 16px; height: 16px; }
        """
        self.assertNotIn("MD3E006", self._codes(switch_subelements, "switch.css"))


def _build_minimal_rgba_png(width: int, height: int, rgba_bytes: bytes) -> bytes:
    """Create a valid uncompressed/zlib 8-bit RGBA PNG using Python stdlib."""
    def chunk(ctype: bytes, data: bytes) -> bytes:
        c = ctype + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    raw_rows = bytearray()
    stride = width * 4
    for y in range(height):
        raw_rows.append(0)  # Filter type 0 (None)
        raw_rows.extend(rgba_bytes[y * stride:(y + 1) * stride])
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw_rows))) + chunk(b"IEND", b"")


class ImageExtractionAndDynamicJsTests(unittest.TestCase):
    @staticmethod
    def _sample_rgba(width: int = 64, height: int = 64) -> bytes:
        buf = bytearray(width * height * 4)
        for y in range(height):
            for x in range(width):
                idx = (y * width + x) * 4
                if x < 28 and y < 48:
                    buf[idx:idx + 4] = b"\xFF\x57\x22\xFF"  # Dominant coral #FF5722
                elif x >= 28 and y < 32:
                    buf[idx:idx + 4] = b"\x00\x89\x7B\xFF"  # Secondary teal #00897B
                else:
                    buf[idx:idx + 4] = b"\x80\x80\x80\xFF"  # Low-chroma neutral gray filtered by Score
        return bytes(buf)

    def test_python_image_extraction_and_cli_flag(self) -> None:
        rgba = self._sample_rgba()
        png_bytes = _build_minimal_rgba_png(64, 64, rgba)
        with tempfile.TemporaryDirectory() as tmp:
            img_path = pathlib.Path(tmp) / "test-wallpaper.png"
            img_path.write_bytes(png_bytes)

            run1 = color_to_css.extract_seeds_from_image_file(img_path)
            run2 = color_to_css.extract_seeds_from_image_file(img_path)
            self.assertEqual([c["hex"] for c in run1], [c["hex"] for c in run2])
            hexes = [c["hex"] for c in run1]
            self.assertEqual(hexes[0], "#FF5722")
            self.assertIn("#00897B", hexes)
            self.assertNotIn("#808080", hexes)

            # Stdlib PNG decoder matches PIL path too
            stdlib_rgba = color_to_css._decode_image_rgba_stdlib(img_path, max_dimension=128)
            stdlib_res = color_to_css.extract_seeds_from_rgba(stdlib_rgba)
            self.assertEqual([c["hex"] for c in stdlib_res], hexes)

            # CLI --image --json produces full scheme + extracted_candidates
            cli_out = subprocess.check_output(
                [sys.executable, str(SCRIPTS_DIR / "color_to_css.py"), "--image", str(img_path), "--json"],
                cwd=str(ROOT_DIR),
                text=True,
            )
            payload = json.loads(cli_out)
            self.assertEqual(payload["seed"], "#FF5722")
            self.assertEqual([c["hex"] for c in payload["extracted_candidates"]], hexes)

    def test_js_dynamic_color_matches_python_bit_for_bit(self) -> None:
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("node runtime unavailable")

        rgba = self._sample_rgba()
        py_cands = [c["hex"] for c in color_to_css.extract_seeds_from_rgba(rgba)]

        js_driver = r"""
import { extractSeedsFromRgba, generateScheme } from './assets/tokens/md3e-dynamic-color.js';
const rgba = new Uint8Array(64 * 64 * 4);
for (let y = 0; y < 64; y++) {
  for (let x = 0; x < 64; x++) {
    const i = (y * 64 + x) * 4;
    if (x < 28 && y < 48) { rgba[i] = 255; rgba[i + 1] = 87; rgba[i + 2] = 34; rgba[i + 3] = 255; }
    else if (x >= 28 && y < 32) { rgba[i] = 0; rgba[i + 1] = 137; rgba[i + 2] = 123; rgba[i + 3] = 255; }
    else { rgba[i] = 128; rgba[i + 1] = 128; rgba[i + 2] = 128; rgba[i + 3] = 255; }
  }
}
const ext = extractSeedsFromRgba(rgba);
const schemes = {};
for (const seed of ['#6750A4', '#FF5722', '#0B57D0']) {
  for (const variant of ['tonal-spot', 'expressive', 'vibrant', 'monochrome']) {
    for (const isDark of [false, true]) {
      for (const contrastLevel of [0.0, 0.5, 1.0]) {
        schemes[`${seed}|${variant}|${isDark}|${contrastLevel}`] = generateScheme(seed, { variant, isDark, contrastLevel });
      }
    }
  }
}
console.log(JSON.stringify({ cands: ext.candidates.map((c) => c.hex), schemes }));
"""
        raw = subprocess.check_output(
            [node_bin, "--input-type=module", "-e", js_driver],
            cwd=str(ROOT_DIR),
            text=True,
        )
        js_out = json.loads(raw)
        self.assertEqual(js_out["cands"], py_cands)

        for key, js_roles in js_out["schemes"].items():
            seed, variant, is_dark_str, level_str = key.split("|")
            py_roles = color_to_css.generate_scheme(
                seed,
                variant=variant,
                is_dark=(is_dark_str == "true"),
                contrast_level=float(level_str),
                spec_version="2025",
            )
            self.assertEqual(js_roles, py_roles, f"Mismatch on {key}")

    def test_starter_wires_accessible_image_upload_and_copy(self) -> None:
        html = STARTER_HTML.read_text(encoding="utf-8")
        self.assertIn("../tokens/md3e-dynamic-color.js", html)
        self.assertIn("../tokens/md3e-blur.css", html)
        self.assertIn("../tokens/md3e-morph.js", html)
        self.assertRegex(html, r'<input\b[^>]*id="image-theme-input"[^>]*class="visually-hidden"')
        self.assertRegex(html, r'\.visually-hidden\s*\{[^}]*clip-path:\s*inset\(50%\)')
        self.assertRegex(html, r'<button\b[^>]*id="btn-copy-theme-css"[^>]*command="--copy"[^>]*commandfor="generated-theme-css"')
        self.assertNotIn('type="color"', html)
        self.assertIn('id="md3e-color-popover"', html)
        self.assertIn('command="toggle-popover"', html)
        self.assertIn('id="hct-plane-canvas"', html)


class PhaseFourAndDesktopBentoTests(unittest.TestCase):
    def test_skill_md_enforces_context_budget_and_decoupled_bento_layer(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("Context Budget", skill)
        self.assertIn("md3e-palettes.css", skill)
        self.assertIn("desktop-bento.html", skill)
        self.assertIn("references/desktop-bento.md", skill)
        self.assertIn("--mode=desktop-bento", skill)

    def test_blur_css_accessibility_and_oklab_rules(self) -> None:
        blur_css = (ROOT_DIR / "assets" / "tokens" / "md3e-blur.css").read_text(encoding="utf-8")
        blur_rules_only = audit_md3e.strip_css_comments(blur_css)
        self.assertIn(".md3e-blur-surface", blur_rules_only)
        self.assertIn(".md3e-blur-primary", blur_rules_only)
        self.assertIn("in oklab", blur_rules_only)
        self.assertNotIn("in oklch", blur_rules_only)
        self.assertIn("-webkit-backdrop-filter", blur_rules_only)
        self.assertIn("backdrop-filter", blur_rules_only)
        self.assertRegex(blur_rules_only, r"@media\s*\(prefers-reduced-transparency\s*:\s*reduce\)")
        self.assertRegex(blur_rules_only, r"@media\s*\(prefers-contrast\s*:\s*more\)")
        self.assertRegex(blur_rules_only, r"@media\s*\(forced-colors\s*:\s*active\)")

    def test_morph_js_35_shapes_and_bezier_interpolation(self) -> None:
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("node runtime unavailable")

        js_driver = r"""
import { SHAPE_NAMES, Morph, buildShape, createShapeMorpher } from './assets/tokens/md3e-morph.js';

const polys = SHAPE_NAMES.map((name) => {
  const p = buildShape(name);
  const b = p.bounds();
  return { name, cubics: p.cubics.length, bounds: b };
});

const pairs = [
  ['square', 'cookie-9-sided'],
  ['triangle', 'clover-8-leaf'],
  ['pixel-circle', 'heart'],
];
const checks = pairs.map(([a, b]) => {
  const m = new Morph(a, b);
  const paths = {};
  for (const p of [0, 0.25, 0.5, 1, 1.12]) {
    paths[String(p)] = m.toSvgPath(p);
  }
  const b0 = m.toPolygon(0).bounds();
  const aBounds = buildShape(a).bounds();
  const b1 = m.toPolygon(1).bounds();
  const bBounds = buildShape(b).bounds();
  return {
    pair: `${a}->${b}`,
    segments: m.morphMatch.length,
    c0: m.asCubics(0).length,
    c1: m.asCubics(1).length,
    paths,
    b0, aBounds, b1, bBounds,
  };
});

let lastD = '';
const mockEl = { setAttribute(k, v) { if (k === 'd') lastD = v; } };
const morpher = createShapeMorpher(mockEl, { initialShape: 'square' });
const dInit = lastD;
morpher.morphTo('cookie-9-sided', { immediate: true });
const dSnapped = lastD;

console.log(JSON.stringify({ shapeNames: SHAPE_NAMES, polys, checks, dInit, dSnapped }));
"""
        raw = subprocess.check_output(
            [node_bin, "--input-type=module", "-e", js_driver],
            cwd=str(ROOT_DIR),
            text=True,
        )
        out = json.loads(raw)
        self.assertEqual(tuple(out["shapeNames"]), shapes_to_css.SHAPE_NAMES)
        for item in out["polys"]:
            self.assertGreater(item["cubics"], 0)
            b = item["bounds"]
            self.assertGreaterEqual(b[0], -1e-4)
            self.assertGreaterEqual(b[1], -1e-4)
            self.assertLessEqual(b[2], 1.0001)
            self.assertLessEqual(b[3], 1.0001)

        for chk in out["checks"]:
            self.assertGreater(chk["segments"], 0)
            self.assertEqual(chk["c0"], chk["segments"])
            self.assertEqual(chk["c1"], chk["segments"])
            for p_str, path_d in chk["paths"].items():
                self.assertTrue(path_d.startswith("M") and path_d.endswith("Z"), f"{chk['pair']} p={p_str}")
                self.assertNotIn("NaN", path_d)
            for v0, va in zip(chk["b0"], chk["aBounds"]):
                self.assertAlmostEqual(v0, va, places=6)
            for v1, vb in zip(chk["b1"], chk["bBounds"]):
                self.assertAlmostEqual(v1, vb, places=6)

        self.assertNotEqual(out["dInit"], out["dSnapped"])

    def test_dual_mode_auditor_strict_vs_desktop_bento(self) -> None:
        shape_shadow_css = ".md3e-shape-sunny { box-shadow: var(--md-sys-elevation-level2); }"
        strict_f = [f for f in audit_md3e.Checker(pathlib.Path("s.css"), mode="strict").run(shape_shadow_css) if f.code == "MD3E023"]
        bento_f = [f for f in audit_md3e.Checker(pathlib.Path("s.css"), mode="desktop-bento").run(shape_shadow_css) if f.code == "MD3E023"]
        self.assertEqual(len(strict_f), 1)
        self.assertEqual(strict_f[0].severity, "warning")
        self.assertEqual(len(bento_f), 1)
        self.assertEqual(bento_f[0].severity, "warning")

        good_drop_css = ".md3e-shape-shadow-wrap { filter: drop-shadow(0 4px 10px color-mix(in oklab, var(--md-sys-color-shadow) 24%, transparent)); }"
        self.assertEqual(audit_md3e.Checker(pathlib.Path("good.css"), mode="desktop-bento").run(good_drop_css), [])

        oklch_css = ".card { background: color-mix(in oklch, var(--md-sys-color-surface-container) 80%, transparent); }"
        oklch_strict = [f for f in audit_md3e.Checker(pathlib.Path("o.css"), mode="strict").run(oklch_css) if f.code == "MD3E018"]
        oklch_bento = [f for f in audit_md3e.Checker(pathlib.Path("o.css"), mode="desktop-bento").run(oklch_css) if f.code == "MD3E018"]
        self.assertEqual(oklch_strict[0].severity, "error")
        self.assertEqual(oklch_bento[0].severity, "error")

        bento_violations = """
        .bento-card { border: 1px solid var(--md-sys-color-outline-variant); box-shadow: var(--md-sys-elevation-level1); }
        @media (forced-colors: active) { .bento-card { border: 1px solid CanvasText; } }
        """
        m101_bento = [f for f in audit_md3e.Checker(pathlib.Path("b.css"), mode="desktop-bento").run(bento_violations) if f.code == "MD3E101"]
        m101_strict = [f for f in audit_md3e.Checker(pathlib.Path("b.css"), mode="strict").run(bento_violations) if f.code == "MD3E101"]
        self.assertEqual(len(m101_bento), 2)
        self.assertTrue(all(f.severity == "custom" for f in m101_bento))
        self.assertEqual(m101_strict, [])

        incomplete_bento_html = (
            "<!doctype html><html><head><style>"
            ".bento-card { background: var(--md-sys-color-surface-container); border-radius: var(--md-sys-shape-corner-medium); }"
            "</style></head><body><main>Hi</main></body></html>"
        )
        bento_findings = audit_md3e.Checker(pathlib.Path("bento.html"), mode="desktop-bento").run(incomplete_bento_html)
        bento_codes = {f.code: f.severity for f in bento_findings}
        self.assertEqual(bento_codes.get("MD3E102"), "custom")
        self.assertEqual(bento_codes.get("MD3E103"), "custom")
        self.assertEqual(bento_codes.get("MD3E104"), "custom")

        # Strict mode must NOT run MD3E101-MD3E104 custom product rules
        strict_codes = {f.code for f in audit_md3e.Checker(pathlib.Path("bento.html"), mode="strict").run(incomplete_bento_html)}
        self.assertFalse({"MD3E101", "MD3E102", "MD3E103", "MD3E104"} & strict_codes)

        # Verify CLI --mode=desktop-bento exit code on shipped desktop-bento.html
        rc = audit_md3e.main([str(ROOT_DIR / "assets" / "starter" / "desktop-bento.html"), "--mode=desktop-bento", "--fail-on=info", "--json"])
        self.assertEqual(rc, 0)

    def test_multiline_transition_catches_corner_full_overshoot_rectangle(self) -> None:
        bad_pill_css = """
        .bento-action-btn {
          height: 48px;
          border-radius: var(--md-sys-shape-corner-full);
          transition: background-color var(--md-bento-motion-fast-effects),
                      border-radius var(--md-bento-motion-fast-spatial),
                      transform var(--md-bento-motion-fast-spatial);
        }
        .bento-action-btn:active {
          border-radius: var(--md-sys-shape-corner-large);
        }
        """
        strict_findings = [
            f for f in audit_md3e.Checker(pathlib.Path("bad.css"), mode="strict").run(bad_pill_css)
            if f.code == "MD3E019"
        ]
        bento_findings = [
            f for f in audit_md3e.Checker(pathlib.Path("bad.css"), mode="desktop-bento").run(bad_pill_css)
            if f.code == "MD3E019"
        ]
        self.assertEqual(len(strict_findings), 1)
        self.assertEqual(strict_findings[0].severity, "warning")
        self.assertEqual(len(bento_findings), 1)
        self.assertEqual(bento_findings[0].severity, "warning")

        good_pill_css = """
        .bento-action-btn {
          height: 48px;
          border-radius: calc(var(--md-bento-control-height, 48px) / 2);
          transition: background-color var(--md-bento-motion-fast-effects),
                      border-radius var(--md-bento-motion-fast-spatial),
                      transform var(--md-bento-motion-fast-spatial);
        }
        .bento-action-btn:active {
          border-radius: var(--md-sys-shape-corner-medium);
        }
        @media (prefers-reduced-motion: reduce) {
          .bento-action-btn {
            transition: none;
          }
        }
        """
        self.assertEqual(audit_md3e.Checker(pathlib.Path("good.css"), mode="strict").run(good_pill_css), [])
        self.assertEqual(audit_md3e.Checker(pathlib.Path("good.css"), mode="desktop-bento").run(good_pill_css), [])


class OfficialSpecPurificationTests(unittest.TestCase):
    def test_four_tier_isolation_and_score_calculation(self) -> None:
        import contextlib
        import io

        bento_only_html = (
            "<!doctype html><html lang='en'><head><style>"
            ".bento-card { background: var(--md-sys-color-surface-container); border: 1px solid var(--md-sys-color-outline-variant); "
            "border-radius: var(--md-sys-shape-corner-medium); color: var(--md-sys-color-on-surface); }"
            "</style></head><body><main data-layout-profile='desktop-bento'><div class='bento-card'>Status</div></main></body></html>"
        )
        with tempfile.TemporaryDirectory() as td:
            sample = pathlib.Path(td) / "bento_sample.html"
            sample.write_text(bento_only_html, encoding="utf-8")

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = audit_md3e.main([str(sample), "--mode=desktop-bento", "--fail-on=warn", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["official_compliance"]["verdict"], "PASS")
            self.assertEqual(payload["official_compliance"]["score"], 100)
            self.assertEqual(payload["official_compliance"]["error"], 0)
            self.assertEqual(payload["official_compliance"]["warning"], 0)
            self.assertTrue(payload["custom_extensions"]["active"])
            self.assertGreaterEqual(payload["custom_extensions"]["custom"], 1)

            buf_strict = io.StringIO()
            with contextlib.redirect_stdout(buf_strict):
                rc_strict = audit_md3e.main([str(sample), "--mode=strict", "--fail-on=warning", "--json"])
            self.assertEqual(rc_strict, 0)
            strict_payload = json.loads(buf_strict.getvalue())
            self.assertFalse(strict_payload["custom_extensions"]["active"])
            self.assertEqual(strict_payload["custom_extensions"]["custom"], 0)

    def test_md3e024_wcag_contrast_and_semantic_role_pairing(self) -> None:
        bad_contrast = ".low-contrast { background: #777777; color: #888888; font-size: 14px; }"
        m024_hex = [f for f in audit_md3e.Checker(pathlib.Path("c.css")).run(bad_contrast) if f.code == "MD3E024"]
        self.assertEqual(len(m024_hex), 1)
        self.assertEqual(m024_hex[0].severity, "error")

        bad_role = ".wrong-role { background: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-surface); }"
        m024_role = [f for f in audit_md3e.Checker(pathlib.Path("r.css")).run(bad_role) if f.code == "MD3E024"]
        self.assertEqual(len(m024_role), 1)
        self.assertEqual(m024_role[0].severity, "error")

        good_role = ".right-role { background: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-primary-container); }"
        self.assertEqual([f for f in audit_md3e.Checker(pathlib.Path("g.css")).run(good_role) if f.code == "MD3E024"], [])

    def test_md3e025_multiple_primary_filled_buttons_and_word_boundary(self) -> None:
        multi_primary_html = (
            "<!doctype html><html><body><section id='checkout'>"
            "<button type='button' class='md3e-btn md3e-btn--filled md3e-btn--s'>Buy Now</button>"
            "<button type='button' class='md3e-btn md3e-btn--filled md3e-btn--s'>Subscribe</button>"
            "</section></body></html>"
        )
        m025 = [f for f in audit_md3e.Checker(pathlib.Path("btn.html")).run(multi_primary_html) if f.code == "MD3E025"]
        self.assertEqual(len(m025), 1)
        self.assertEqual(m025[0].severity, "info")

        icon_filled_html = (
            "<!doctype html><html><body><section id='toolbar'>"
            "<button type='button' class='md3e-icon-btn md3e-icon-btn--filled' aria-label='Bold'><span class='material-symbols-outlined' aria-hidden='true'>check</span></button>"
            "<button type='button' class='md3e-icon-btn md3e-icon-btn--filled' aria-label='Italic'><span class='material-symbols-outlined' aria-hidden='true'>edit</span></button>"
            "</section></body></html>"
        )
        m025_icons = [f for f in audit_md3e.Checker(pathlib.Path("icons.html")).run(icon_filled_html) if f.code == "MD3E025"]
        self.assertEqual(m025_icons, [])

    def test_data_view_and_analytical_exemptions_in_desktop_bento(self) -> None:
        analytical_html = """<!doctype html>
<html lang="en" data-layout-profile="desktop-bento">
<head>
<style>
  .bento-card { background: var(--md-sys-color-surface-container-low); border-radius: var(--md-sys-shape-corner-extra-large); }
  .bento-well { background: var(--md-sys-color-surface-container-highest); border-radius: var(--md-sys-shape-corner-large); }
  .shell-bg { background: var(--md-sys-color-surface-container-lowest); }
  .chrome-hi { background: var(--md-sys-color-surface-container-high); }
  .telemetry-table td { border-bottom: 1px solid var(--md-sys-color-outline-variant); }
  .trajectory-viewport { border: 1px solid var(--md-sys-color-outline-variant); }
  canvas { border: 1px solid var(--md-sys-color-outline-variant); }
</style>
</head>
<body>
  <main>
    <article class="bento-card" data-md3e-exempt="data-view">
      <div class="bento-well trajectory-viewport">
        <canvas id="replay-canvas" width="320" height="180"></canvas>
      </div>
      <svg viewBox="0 0 300 120" aria-label="Latency histogram">
        <line x1="20" y1="10" x2="20" y2="100" stroke="currentColor" stroke-width="1" />
        <text x="4" y="100">0ms</text>
      </svg>
      <table class="telemetry-table">
        <thead><tr><th>Metric</th><th>p99</th></tr></thead>
        <tbody><tr><td>Render</td><td>4.2ms</td></tr></tbody>
      </table>
    </article>
  </main>
</body>
</html>"""
        findings = audit_md3e.Checker(pathlib.Path("analytics.html"), mode="desktop-bento").run(analytical_html)
        custom_or_bad = [f for f in findings if f.severity in ("error", "warning", "custom")]
        self.assertEqual(custom_or_bad, [], f"Analytical data-view falsely flagged: {custom_or_bad}")

    def test_purified_three_layer_docs_framing(self) -> None:
        phrase = "M3 Expressive-inspired Web Design System with verified M3E specifications"
        self.assertIn(phrase, SKILL_MD.read_text(encoding="utf-8"))
        self.assertIn(phrase, (ROOT_DIR / "README.md").read_text(encoding="utf-8"))
        self.assertIn(phrase, OFFICIAL_AUDIT_MD.read_text(encoding="utf-8"))
        self.assertIn("Context Budget", SKILL_MD.read_text(encoding="utf-8"))
        self.assertIn("Layer 3", (REFERENCES_DIR / "desktop-bento.md").read_text(encoding="utf-8"))
        self.assertIn("Layer 3", (REFERENCES_DIR / "expressive-tactics.md").read_text(encoding="utf-8"))
        self.assertIn("OFFICIAL_WEB_CURVES", (REFERENCES_DIR / "motion.md").read_text(encoding="utf-8"))
        self.assertIn("24×24", (REFERENCES_DIR / "accessibility.md").read_text(encoding="utf-8"))


class DualSkillAndDesktopChoreographyTests(unittest.TestCase):
    def test_skill_co_mounting_arbitration_protocol(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("Composability: Co-mounting with `frontend-design`", skill)
        for keyword in (
            "Subject Grounding",
            "Two-Pass Spatial Composition",
            "Anti-Templated Layout Self-Critique",
            "Plain Active-Voice Microcopy",
            "HCT semantic roles",
            "15 + 15",
            "md3e-spring.js",
            "audit_md3e.py",
        ):
            self.assertIn(keyword, skill)

    def test_global_dynamic_hct_selection_tokens_and_cleanup(self) -> None:
        tokens = TOKENS_CSS.read_text(encoding="utf-8")
        self.assertNotIn("md-icon", tokens)
        self.assertIn("::selection", tokens)
        self.assertIn("background-color: var(--md-sys-color-primary-container)", tokens)
        self.assertIn("color: var(--md-sys-color-on-primary-container)", tokens)
        self.assertIn("code::selection", tokens)
        self.assertIn(".tabular-nums::selection", tokens)
        self.assertIn("background-color: var(--md-sys-color-tertiary-container)", tokens)
        self.assertIn("color: var(--md-sys-color-on-tertiary-container)", tokens)

        good_sel = "::selection { background-color: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-primary-container); }"
        self.assertEqual([f for f in audit_md3e.Checker(pathlib.Path("s.css")).run(good_sel) if f.code == "MD3E024"], [])
        bad_sel = "::selection { background-color: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-surface); }"
        self.assertEqual(len([f for f in audit_md3e.Checker(pathlib.Path("s.css")).run(bad_sel) if f.code == "MD3E024"]), 1)

    def test_scoped_desktop_context_menu_and_choreography_assets(self) -> None:
        bento_html = (ROOT_DIR / "assets" / "starter" / "desktop-bento.html").read_text(encoding="utf-8")
        bento_md = (REFERENCES_DIR / "desktop-bento.md").read_text(encoding="utf-8")
        motion_md = (REFERENCES_DIR / "motion.md").read_text(encoding="utf-8")
        index_html = STARTER_HTML.read_text(encoding="utf-8")

        for snippet in (
            "[data-context-menu]",
            "if (e.shiftKey) return;",
            'role="menu"',
            'role="menuitem"',
            "md3e-blur-surface-high",
            "transformOrigin",
            "80px",
            "220px",
            "white-space: nowrap",
            "is-view-exiting",
            "30ms",
            "createSpringAnimator",
        ):
            self.assertIn(snippet, bento_html)
        self.assertNotIn("bento-vt-panel", bento_html)
        self.assertNotIn("bento-vt-scrim", bento_html)

        self.assertIn("if (e.shiftKey) return;", bento_md)
        self.assertIn("[data-context-menu]", bento_md)
        self.assertIn("Structural & Page-Level Spatial Choreography", motion_md)
        self.assertIn("Dual-Spring Navigation Rail", motion_md)
        self.assertIn("Fade Through", motion_md)
        self.assertIn("Physical Sliding Segmented Pill Indicator", motion_md)

        for snippet in (
            "nav-rail__label",
            "nav-rail__indicator",
            "viewFadeSpring",
            "md3e-seg-indicator",
            "attachSpringSegmentedIndicator",
            "createSpringAnimator",
        ):
            self.assertIn(snippet, index_html)

        # Preserve prior slider & FAB menu red-line fixes
        self.assertIn('id="wavy-progress-slider"', index_html)
        self.assertIn('id="volume-slider"', index_html)
        self.assertIn("pointer-events: none", index_html)

    def test_auditor_catches_context_menu_without_role(self) -> None:
        bad_menu = "<!doctype html><html><body><div class='bento-context-menu'><button type='button'>Inspect</button></div></body></html>"
        m020 = [f for f in audit_md3e.Checker(pathlib.Path("menu.html")).run(bad_menu) if f.code == "MD3E020"]
        self.assertEqual(len(m020), 1)

    def test_starter_stylesheets_have_balanced_braces(self) -> None:
        for html_path in (STARTER_HTML, BENTO_HTML):
            text = html_path.read_text(encoding="utf-8")
            for idx, (css_block, _) in enumerate(audit_md3e.extract_style_blocks(text)):
                cleaned = audit_md3e.strip_css_comments(css_block)
                self.assertEqual(
                    cleaned.count("{"),
                    cleaned.count("}"),
                    f"Unbalanced CSS braces in {html_path.name} <style> block #{idx}",
                )


class RootCauseAndPersonalStudioTests(unittest.TestCase):
    def test_md3e028_unbalanced_keyframes_and_css_braces(self) -> None:
        unclosed_kf = """
        @keyframes pulse {
          0% { opacity: 0.2; }
          100% { opacity: 1; }
        .card { color: var(--md-sys-color-on-surface); }
        """
        extra_brace_kf = """
        @keyframes pulse {
          0% { opacity: 0.2; }
          100% { opacity: 1; }
        }
        }
        """
        quoted_braces_ok = """
        .token::before { content: "{ ok }"; }
        @keyframes ok {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
        @media (prefers-reduced-motion: reduce) {
          .token { animation: none; }
        }
        """
        for bad_css in (unclosed_kf, extra_brace_kf):
            for mode in audit_md3e.AUDIT_MODES:
                m028 = [f for f in audit_md3e.Checker(pathlib.Path("kf.css"), mode=mode).run(bad_css) if f.code == "MD3E028"]
                self.assertEqual(len(m028), 1, f"Expected MD3E028 error in mode={mode} for:\n{bad_css}")
                self.assertEqual(m028[0].severity, "error")

        bad_html = f"<!doctype html><html><head><style>{extra_brace_kf}</style></head><body></body></html>"
        self.assertEqual(
            len([f for f in audit_md3e.Checker(pathlib.Path("kf.html")).run(bad_html) if f.code == "MD3E028"]),
            1,
        )
        self.assertEqual(
            [f for f in audit_md3e.Checker(pathlib.Path("ok.css")).run(quoted_braces_ok) if f.code == "MD3E028"],
            [],
        )

    def test_personal_studio_mode_isolation_inheritance_and_layer4_rules(self) -> None:
        import contextlib
        import io

        # Bad Layer 4 CSS/HTML should trigger MD3E101+ and MD3E201/MD3E202 ONLY in personal-studio,
        # while strict mode remains completely isolated from MD3E101+ and MD3E201+.
        incomplete_studio_html = """<!doctype html>
<html lang="en">
<head>
<style>
  .bento-card {
    background: var(--md-sys-color-surface-container);
    color: var(--md-sys-color-on-surface);
    border: 1px solid var(--md-sys-color-outline-variant);
    border-radius: var(--md-sys-shape-corner-medium);
  }
  .studio-caustic-field { position: fixed; inset: 0; }
  dialog.studio-cmd-dialog:modal { display: grid; }
</style>
</head>
<body>
  <main>
    <dialog id="cmd" role="dialog"><p>No focusable controls</p></dialog>
  </main>
</body>
</html>"""
        strict_codes = {
            f.code for f in audit_md3e.Checker(pathlib.Path("studio.html"), mode="strict").run(incomplete_studio_html)
        }
        self.assertFalse(any(c.startswith("MD3E1") or c.startswith("MD3E2") for c in strict_codes), strict_codes)

        bento_codes = {
            f.code for f in audit_md3e.Checker(pathlib.Path("studio.html"), mode="desktop-bento").run(incomplete_studio_html)
        }
        self.assertTrue({"MD3E101", "MD3E102", "MD3E103", "MD3E104"} <= bento_codes, bento_codes)
        self.assertFalse(any(c.startswith("MD3E2") for c in bento_codes), bento_codes)

        studio_findings = audit_md3e.Checker(pathlib.Path("studio.html"), mode="personal-studio").run(incomplete_studio_html)
        studio_codes = {f.code for f in studio_findings}
        self.assertTrue(
            {"MD3E101", "MD3E102", "MD3E103", "MD3E104", "MD3E201", "MD3E202"} <= studio_codes,
            studio_codes,
        )
        self.assertTrue(
            all(f.severity == "custom" for f in studio_findings if f.code.startswith(("MD3E1", "MD3E2"))),
            studio_findings,
        )

        # CLI --mode=personal-studio JSON check: custom findings do not reduce score below 100
        with tempfile.TemporaryDirectory() as td:
            sample = pathlib.Path(td) / "studio_sample.html"
            sample.write_text(incomplete_studio_html, encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = audit_md3e.main([str(sample), "--mode=personal-studio", "--fail-on=info", "--json"])
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["mode"], "personal-studio")
            self.assertEqual(payload["official_compliance"]["score"], 100)
            self.assertTrue(payload["custom_extensions"]["active"])
            self.assertGreaterEqual(payload["custom_extensions"]["custom"], 2)

        # Clean compliant personal-studio snippet/doc passes with 0 findings across all severities (no caustic field!)
        good_studio_html = """<!doctype html>
<html lang="en" data-layout-profile="desktop-bento" data-studio-profile="personal-studio">
<head>
<link rel="stylesheet" href="../tokens/md3e-blur.css">
<link rel="stylesheet" href="../tokens/md3e-studio.css">
<style>
  .shell { background: var(--md-sys-color-surface-container-lowest); }
  .card { background: var(--md-sys-color-surface-container-low); border-radius: var(--md-sys-shape-corner-extra-large); }
  .well { background: var(--md-sys-color-surface-container); border-radius: var(--md-sys-shape-corner-large); }
  .hi { background: var(--md-sys-color-surface-container-high); }
  .kpi { font-size: var(--md-sys-typescale-display-large-size); }
  .wrap { filter: drop-shadow(0 4px 12px color-mix(in oklab, var(--md-sys-color-shadow) 24%, transparent)); }
</style>
</head>
<body>
  <main>
    <article class="card bento-card--hero">
      <div class="wave"></div>
      <svg class="sparkline" viewBox="0 0 100 20" aria-hidden="true"></svg>
      <div class="wrap"><button type="button" class="md3e-shape md3e-shape-sunny" aria-label="Morph">Go</button></div>
    </article>
    <dialog class="studio-cmd-dialog md3e-blur-surface-highest" id="studio-cmd-dialog" aria-labelledby="cmd-t" closedby="any">
      <h2 id="cmd-t">Commands</h2>
      <input type="search" aria-label="Search commands">
      <button type="button">Close</button>
    </dialog>
  </main>
  <script type="module" src="../tokens/md3e-morph.js"></script>
</body>
</html>"""
        self.assertEqual(
            audit_md3e.Checker(pathlib.Path("good-studio.html"), mode="personal-studio").run(good_studio_html),
            [],
        )

    def test_md3e201_bans_caustic_field_and_enforces_hdr_hygiene(self) -> None:
        caustic_html = """<!doctype html>
<html lang="en" data-layout-profile="desktop-bento" data-studio-profile="personal-studio">
<head>
<link rel="stylesheet" href="../tokens/md3e-blur.css">
<link rel="stylesheet" href="../tokens/md3e-studio.css">
<style>
  .shell { background: var(--md-sys-color-surface-container-lowest); }
  .card { background: var(--md-sys-color-surface-container-low); border-radius: var(--md-sys-shape-corner-extra-large); }
  .well { background: var(--md-sys-color-surface-container); border-radius: var(--md-sys-shape-corner-large); }
  .hi { background: var(--md-sys-color-surface-container-high); }
  .kpi { font-size: var(--md-sys-typescale-display-large-size); }
  .wrap { filter: drop-shadow(0 4px 12px color-mix(in oklab, var(--md-sys-color-shadow) 24%, transparent)); }
  .studio-caustic-field { position: fixed; inset: 0; pointer-events: none; }
</style>
</head>
<body>
  <div class="studio-caustic-field" aria-hidden="true"></div>
  <main>
    <article class="card bento-card--hero">
      <div class="wave"></div>
      <svg class="sparkline" viewBox="0 0 100 20" aria-hidden="true"></svg>
      <div class="wrap"><button type="button" class="md3e-shape md3e-shape-sunny" aria-label="Morph">Go</button></div>
    </article>
  </main>
</body>
</html>"""
        caustic_f = [
            f for f in audit_md3e.Checker(pathlib.Path("caustic.html"), mode="personal-studio").run(caustic_html)
            if f.code == "MD3E201"
        ]
        self.assertGreaterEqual(len(caustic_f), 2)
        self.assertTrue(all(f.severity == "custom" for f in caustic_f))

        bad_hdr_css = """
        @media (dynamic-range: high) {
          body { dynamic-range-limit: constrained-high; }
          p { color: color(display-p3 1 0.2 0.2); }
        }
        """
        hdr_f = [
            f for f in audit_md3e.Checker(pathlib.Path("bad_hdr.css"), mode="personal-studio").run(bad_hdr_css)
            if f.code == "MD3E201"
        ]
        # 2 broad body/p HDR findings + 3 missing fallback findings (SDR, reduced-transparency, contrast)
        self.assertGreaterEqual(len(hdr_f), 4)
        self.assertTrue(all(f.severity == "custom" for f in hdr_f))

        good_hdr_css = """
        :root[data-studio-profile="personal-studio"] {
          --md-studio-hdr-boost: 35%;
        }
        body, p {
          dynamic-range-limit: standard;
        }
        @media (dynamic-range: high) and (color-gamut: p3) {
          :root[data-studio-profile="personal-studio"][data-studio-hdr="on"] [data-studio-spotlight]::after {
            dynamic-range-limit: constrained-high;
            background: radial-gradient(260px circle at 50% 50%, color(display-p3 0.6 0.45 1 / 0.22), transparent 74%);
          }
        }
        :root[data-studio-hdr="off"] [data-studio-spotlight]::after {
          dynamic-range-limit: standard;
        }
        @media (prefers-reduced-transparency: reduce) {
          :root[data-studio-profile="personal-studio"] [data-studio-spotlight]::after {
            dynamic-range-limit: standard;
            display: none;
          }
        }
        @media (prefers-contrast: more) {
          :root[data-studio-profile="personal-studio"] [data-studio-spotlight]::after {
            dynamic-range-limit: standard;
            display: none;
          }
        }
        """
        self.assertEqual(
            [f for f in audit_md3e.Checker(pathlib.Path("good_hdr.css"), mode="personal-studio").run(good_hdr_css) if f.code == "MD3E201"],
            [],
        )

    def test_md3e029_complex_components_and_default_mode_alias(self) -> None:
        self.assertEqual(audit_md3e.normalize_mode("default"), "strict")
        self.assertEqual(audit_md3e.Checker(pathlib.Path("x.css"), mode="default").mode, "strict")

        # 1. Floating label opaque background patch bleed check
        bad_label_css = """
        .md3e-text-field--outlined .md3e-text-field__label {
          position: absolute;
          background: var(--md-sys-color-surface);
        }
        .md3e-field label {
          background-color: var(--md-sys-color-surface-container-low);
        }
        """
        m029_lbl = [f for f in audit_md3e.Checker(pathlib.Path("lbl.css"), mode="default").run(bad_label_css) if f.code == "MD3E029"]
        self.assertEqual(len(m029_lbl), 2)
        self.assertTrue(all(f.severity == "warning" for f in m029_lbl))

        good_notch_css = """
        .md3e-field__outline {
          border: 1px solid var(--md-sys-color-outline);
          background: transparent;
        }
        .md3e-text-field__label {
          background: transparent;
        }
        """
        self.assertEqual(
            [f for f in audit_md3e.Checker(pathlib.Path("notch.css"), mode="default").run(good_notch_css) if f.code == "MD3E029"],
            [],
        )

        # 2. Dialog A11y (redundant role/aria-modal), root scroll-lock, and overscroll-behavior: contain
        bad_dialog_html = """<!doctype html>
<html lang="en">
<head>
<style>
  html:has(dialog[open]) { overflow: hidden; }
  body.dialog-open { overflow: hidden; }
  .md3e-dialog { padding: var(--md-sys-spacing-6); }
</style>
</head>
<body>
  <dialog id="dlg" role="dialog" aria-modal="true">
    <button type="button">OK</button>
  </dialog>
</body>
</html>"""
        d_default = [f for f in audit_md3e.Checker(pathlib.Path("dlg.html"), mode="default").run(bad_dialog_html) if f.code == "MD3E029"]
        self.assertEqual(len(d_default), 5)  # role, aria-modal, 2x scroll-lock, missing dialog:modal overscroll
        self.assertTrue(all(f.severity == "warning" for f in d_default))

        d_studio = [f for f in audit_md3e.Checker(pathlib.Path("dlg.html"), mode="personal-studio").run(bad_dialog_html) if f.code == "MD3E202"]
        self.assertEqual(len(d_studio), 5)
        self.assertTrue(all(f.severity == "custom" for f in d_studio))

        good_dialog_html = """<!doctype html>
<html lang="en">
<head>
<style>
  body { overflow: hidden; }
  dialog:modal { overscroll-behavior: contain; }
  dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }
</style>
</head>
<body>
  <dialog id="dlg" aria-labelledby="t">
    <h2 id="t">Confirm</h2>
    <button type="button">OK</button>
  </dialog>
</body>
</html>"""
        self.assertEqual(
            [f for f in audit_md3e.Checker(pathlib.Path("good_dlg.html"), mode="default").run(good_dialog_html) if f.code == "MD3E029"],
            [],
        )

        # 3. Custom listbox/menu/grid keyboard-focus & active-state contract
        bad_widget_html = """<!doctype html>
<html lang="en">
<head>
<style>
  .btn:hover { background: var(--md-sys-color-surface-container); }
  .btn:focus-visible { outline: 3px solid var(--md-sys-color-secondary); }
</style>
</head>
<body>
  <div class="custom-select" role="listbox" aria-label="Region">
    <div role="option">US</div>
  </div>
  <div class="custom-cal" role="grid" aria-label="Calendar">
    <button type="button">1</button>
  </div>
</body>
</html>"""
        w_f = [f for f in audit_md3e.Checker(pathlib.Path("w.html"), mode="default").run(bad_widget_html) if f.code == "MD3E029"]
        self.assertEqual(len(w_f), 2)

        good_widget_html = """<!doctype html>
<html lang="en">
<head>
<style>
  .custom-select [data-highlighted],
  .custom-select [data-selected] { background: var(--md-sys-color-secondary-container); }
  .custom-cal [data-range-start],
  .custom-cal [data-in-range],
  .custom-cal button:focus-visible { background: var(--md-sys-color-primary); color: var(--md-sys-color-on-primary); }
</style>
</head>
<body>
  <div class="custom-select" role="listbox" aria-label="Region">
    <div role="option">US</div>
  </div>
  <div class="custom-cal" role="grid" aria-label="Calendar">
    <button type="button">1</button>
  </div>
</body>
</html>"""
        self.assertEqual(
            [f for f in audit_md3e.Checker(pathlib.Path("wg.html"), mode="default").run(good_widget_html) if f.code == "MD3E029"],
            [],
        )

    def test_spring_js_synthesizer_dt_invariance_and_visibility(self) -> None:
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("node runtime unavailable")

        js_driver = r"""
let nowVal = 1000;
let rafSeq = 0;
const rafQueue = new Map();
const visListeners = new Set();
let cancelledCount = 0;

globalThis.performance = { now: () => nowVal };
globalThis.requestAnimationFrame = (cb) => {
  const id = ++rafSeq;
  rafQueue.set(id, cb);
  return id;
};
globalThis.cancelAnimationFrame = (id) => {
  if (rafQueue.delete(id)) cancelledCount += 1;
};
globalThis.document = {
  hidden: false,
  documentElement: { dataset: { motionScheme: 'expressive' } },
  addEventListener(evt, fn) { if (evt === 'visibilitychange') visListeners.add(fn); },
  removeEventListener(evt, fn) { if (evt === 'visibilitychange') visListeners.delete(fn); },
};

const { synthesizeSpringLinearCss, createSpringAnimator } = await import('./assets/tokens/md3e-spring.js');

// 1. Closed-form CSS linear() synthesis
const s340 = synthesizeSpringLinearCss(340, 0.76, 36);
const sCritical = synthesizeSpringLinearCss(1600, 1.0, 24);

// 2. 60Hz vs 120Hz dt invariance at identical elapsed time (250ms after Frame 1)
function runAtHz(hz, elapsedMs) {
  rafQueue.clear();
  nowVal = 1000;
  let lastVal = 0;
  let completed = false;
  const anim = createSpringAnimator({
    initialValue: 0,
    stiffness: 340,
    damping: 0.76,
    precision: 0.01,
    onUpdate(v) { lastVal = v; },
    onComplete() { completed = true; },
  });
  anim.setTarget(100);
  // Frame 1 at ts=1000 uses FRAME_1_DT = 1/60
  const firstId = [...rafQueue.keys()][0];
  const firstCb = rafQueue.get(firstId);
  rafQueue.delete(firstId);
  firstCb(nowVal);

  const stepMs = 1000 / hz;
  const steps = Math.round(elapsedMs / stepMs);
  for (let i = 1; i <= steps; i++) {
    nowVal = 1000 + i * stepMs;
    const ids = [...rafQueue.keys()];
    if (ids.length === 0) break;
    const id = ids[0];
    const cb = rafQueue.get(id);
    rafQueue.delete(id);
    cb(nowVal);
  }
  const midVal = anim.value;
  const midVel = anim.velocity;
  // Settle to completion
  for (let guard = 0; guard < 400 && rafQueue.size > 0; guard++) {
    nowVal += stepMs;
    const id = [...rafQueue.keys()][0];
    const cb = rafQueue.get(id);
    rafQueue.delete(id);
    cb(nowVal);
  }
  return { midVal, midVel, finalVal: anim.value, completed, lastVal };
}

const r60 = runAtHz(60, 250);
const r120 = runAtHz(120, 250);

// 3. document.hidden pause and timestamp rebase on foreground return
rafQueue.clear();
cancelledCount = 0;
nowVal = 2000;
const visAnim = createSpringAnimator({
  initialValue: 0,
  stiffness: 340,
  damping: 0.76,
  precision: 0.01,
});
visAnim.setTarget(100);
for (let i = 0; i < 3; i++) {
  const id = [...rafQueue.keys()][0];
  const cb = rafQueue.get(id);
  rafQueue.delete(id);
  nowVal += 16.6667;
  cb(nowVal);
}
const valBeforeHide = visAnim.value;
globalThis.document.hidden = true;
for (const fn of visListeners) fn();
const pausedWhileHidden = visAnim.paused;
const queueSizeWhileHidden = rafQueue.size;

// Return to foreground 60 seconds later: must rebase ts smoothly without jumping straight to 100
nowVal += 60000;
globalThis.document.hidden = false;
for (const fn of visListeners) fn();
const pausedAfterShow = visAnim.paused;
const queueSizeAfterShow = rafQueue.size;
const resumeId = [...rafQueue.keys()][0];
const resumeCb = rafQueue.get(resumeId);
rafQueue.delete(resumeId);
resumeCb(nowVal);
const valOnResumeFrame = visAnim.value;
visAnim.stop();

// 4. Mid-flight reversal velocity continuity + cancelled stale onRest + jump/getters
rafQueue.clear();
nowVal = 3000;
let staleRestCount = 0;
const finalRestValues = [];
const revAnim = createSpringAnimator({
  initialValue: 0,
  stiffness: 340,
  damping: 0.76,
  precision: 0.01,
});
revAnim.setTarget(100, {
  onRest() { staleRestCount += 1; },
});
for (let i = 0; i < 4; i++) {
  const id = [...rafQueue.keys()][0];
  const cb = rafQueue.get(id);
  rafQueue.delete(id);
  nowVal += 16.6667;
  cb(nowVal);
}
const valAtReversal = revAnim.getValue();
const velAtReversal = revAnim.getVelocity();
const animBeforeReversal = revAnim.isAnimating();

revAnim.setTarget(0, {
  onRest(v) { finalRestValues.push(v); },
});
const targetAfterReversal = revAnim.getTarget();
const valImmediatelyAfter = revAnim.getValue();
const velImmediatelyAfter = revAnim.getVelocity();

// Step first frame after reversal: positive inertia prevents discontinuous snap
const firstRevId = [...rafQueue.keys()][0];
const firstRevCb = rafQueue.get(firstRevId);
rafQueue.delete(firstRevId);
nowVal += 16.6667;
firstRevCb(nowVal);
const valOneFrameAfterReversal = revAnim.getValue();

// Settle to completion
for (let guard = 0; guard < 600 && rafQueue.size > 0; guard++) {
  nowVal += 16.6667;
  const id = [...rafQueue.keys()][0];
  const cb = rafQueue.get(id);
  rafQueue.delete(id);
  cb(nowVal);
}
const animAfterSettle = revAnim.isAnimating();
const settledValue = revAnim.getValue();
revAnim.jump(42);
const jumpedState = {
  value: revAnim.getValue(),
  target: revAnim.getTarget(),
  velocity: revAnim.getVelocity(),
  animating: revAnim.isAnimating(),
};

console.log(JSON.stringify({
  s340,
  sCritical,
  r60,
  r120,
  valBeforeHide,
  pausedWhileHidden,
  queueSizeWhileHidden,
  cancelledCount,
  pausedAfterShow,
  queueSizeAfterShow,
  valOnResumeFrame,
  reversal: {
    valAtReversal,
    velAtReversal,
    animBeforeReversal,
    targetAfterReversal,
    valImmediatelyAfter,
    velImmediatelyAfter,
    valOneFrameAfterReversal,
    staleRestCount,
    finalRestValues,
    animAfterSettle,
    settledValue,
    jumpedState,
  },
}));
"""
        raw = subprocess.check_output(
            [node_bin, "--input-type=module", "-e", js_driver],
            cwd=str(ROOT_DIR),
            text=True,
        )
        out = json.loads(raw)

        s340 = out["s340"]
        self.assertGreaterEqual(s340["durationMs"], 460)
        self.assertLessEqual(s340["durationMs"], 540)
        self.assertTrue(s340["linearEasing"].startswith("linear("))
        self.assertEqual(len(s340["linearEasing"][7:-1].split(",")), 37)
        self.assertEqual(s340["cssShorthand"], f"{s340['durationMs']}ms {s340['linearEasing']}")
        self.assertGreater(s340["peakOvershoot"], 0)
        self.assertEqual(out["sCritical"]["peakOvershoot"], 0)

        self.assertAlmostEqual(out["r60"]["midVal"], out["r120"]["midVal"], delta=0.05)
        self.assertAlmostEqual(out["r60"]["midVel"], out["r120"]["midVel"], delta=0.25)
        self.assertTrue(out["r60"]["completed"])
        self.assertTrue(out["r120"]["completed"])
        self.assertEqual(out["r60"]["finalVal"], 100)
        self.assertEqual(out["r120"]["finalVal"], 100)

        self.assertTrue(out["pausedWhileHidden"])
        self.assertEqual(out["queueSizeWhileHidden"], 0)
        self.assertGreaterEqual(out["cancelledCount"], 1)
        self.assertFalse(out["pausedAfterShow"])
        self.assertEqual(out["queueSizeAfterShow"], 1)
        self.assertGreater(out["valOnResumeFrame"], out["valBeforeHide"])
        self.assertLess(out["valOnResumeFrame"], 60.0)

        rev = out["reversal"]
        self.assertTrue(rev["animBeforeReversal"])
        self.assertGreater(rev["valAtReversal"], 5.0)
        self.assertGreater(rev["velAtReversal"], 50.0)
        self.assertEqual(rev["targetAfterReversal"], 0)
        self.assertEqual(rev["valImmediatelyAfter"], rev["valAtReversal"])
        self.assertEqual(rev["velImmediatelyAfter"], rev["velAtReversal"])
        self.assertGreater(rev["valOneFrameAfterReversal"], rev["valAtReversal"] * 0.8)
        self.assertEqual(rev["staleRestCount"], 0)
        self.assertEqual(rev["finalRestValues"], [0])
        self.assertFalse(rev["animAfterSettle"])
        self.assertEqual(rev["settledValue"], 0)
        self.assertEqual(rev["jumpedState"], {"value": 42, "target": 42, "velocity": 0, "animating": False})

    def test_studio_js_schema_intent_harmonize_and_css_patch(self) -> None:
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("node runtime unavailable")

        js_driver = r"""
import {
  STUDIO_PARAM_SCHEMA,
  inferHumanIntent,
  computeHarmonizedParams,
  formatStudioCssPatch,
  detectHdrCapabilities,
  initPersonalStudio,
} from './assets/tokens/md3e-studio.js';

const bareNodeCaps = detectHdrCapabilities();

const schemaKeys = Object.keys(STUDIO_PARAM_SCHEMA);
const defaultIntent = inferHumanIntent({});
const crystalIntent = inferHumanIntent({
  values: { glassAlpha: 38, blurPx: 42 },
  sources: { glassAlpha: 'human', blurPx: 'human' },
});
const silkIntent = inferHumanIntent({
  values: { springStiffness: 200, springDamping: 0.62, staggerMs: 48 },
  sources: { springStiffness: 'human', springDamping: 'human', staggerMs: 'human' },
});
const crispIntent = inferHumanIntent({
  values: { springStiffness: 820, glassAlpha: 82, springDamping: 0.94 },
  sources: { springStiffness: 'human', glassAlpha: 'human', springDamping: 'human' },
});
const tactileIntent = inferHumanIntent({
  values: { spotlightAlpha: 22, spotlightPx: 390 },
  sources: { spotlightAlpha: 'human', spotlightPx: 'human' },
});

const humanState = {
  values: { glassAlpha: 40, springStiffness: 250, hdrBoost: 60 },
  sources: { glassAlpha: 'human', springStiffness: 'human', hdrBoost: 'human' },
};
const harmonized = computeHarmonizedParams(humanState);
const harmonizedAgain = computeHarmonizedParams(harmonized);
const cssPatch = formatStudioCssPatch(harmonized);
const cssPatchHdrOff = formatStudioCssPatch(harmonized, { hdrEnabled: false });

// Mock DOM + HDR browser capabilities to test __MD3E_TUNER__, __MD3E_STUDIO__, and fallbacks
const mediaState = {
  '(dynamic-range: high)': true,
  '(color-gamut: p3)': true,
  '(prefers-reduced-transparency: reduce)': false,
  '(prefers-contrast: more)': false,
  '(forced-colors: active)': false,
};
globalThis.window = {
  matchMedia: (q) => ({ matches: Boolean(mediaState[q]), addEventListener() {}, removeEventListener() {} }),
  location: { search: '', hash: '' },
};
globalThis.CSS = { supports: (p, v) => (p === 'color' && v.includes('display-p3')) || p === 'dynamic-range-limit' };
const makeStyle = () => {
  const map = new Map();
  return {
    setProperty: (k, v) => map.set(k, v),
    removeProperty: (k) => map.delete(k),
    getPropertyValue: (k) => map.get(k) || '',
    toObject: () => Object.fromEntries(map.entries()),
  };
};
const makeEl = () => {
  const attrs = new Map();
  const listeners = new Map();
  return {
    dataset: {},
    style: makeStyle(),
    textContent: '',
    setAttribute: (k, v) => attrs.set(k, String(v)),
    getAttribute: (k) => attrs.get(k) ?? null,
    addEventListener: (t, fn) => listeners.set(t, fn),
    removeEventListener: (t) => listeners.delete(t),
    click: () => listeners.get('click')?.(),
  };
};
const rootEl = makeEl();
rootEl.dataset.studioProfile = 'personal-studio';
const telemetryEl = makeEl();
const cssOutputEl = makeEl();
const hdrBadgeEl = makeEl();
const hdrToggleBtnEl = makeEl();

const ctrl = initPersonalStudio({
  rootEl,
  telemetryEl,
  cssOutputEl,
  hdrBadgeEl,
  hdrToggleBtnEl,
  persistStorage: false,
});
const aliasEqual = globalThis.window.__MD3E_TUNER__ === ctrl && globalThis.window.__MD3E_STUDIO__ === globalThis.window.__MD3E_TUNER__;
const initialHdrCaps = ctrl.getHdrCapabilities();
const initialHdrEnabled = ctrl.isHdrEnabled();
const initialBadge = hdrBadgeEl.textContent;
const initialChecked = hdrToggleBtnEl.getAttribute('aria-checked');
const initialCssVar = rootEl.style.getPropertyValue('--md-studio-hdr-boost');

ctrl.setHdrEnabled(false);
const disabledHdrEnabled = ctrl.isHdrEnabled();
const disabledAttr = rootEl.dataset.studioHdr;
const disabledCssVar = rootEl.style.getPropertyValue('--md-studio-hdr-boost');
const disabledBadge = hdrBadgeEl.textContent;
const disabledChecked = hdrToggleBtnEl.getAttribute('aria-checked');

ctrl.setHdrEnabled(true);
rootEl.dataset.reducedTransparency = 'true';
const rtSnap = ctrl.setParam('hdrBoost', 72);
const rtHdrEnabled = ctrl.isHdrEnabled();
const rtAttr = rootEl.dataset.studioHdr;
const rtBadge = hdrBadgeEl.textContent;

ctrl.destroy();

console.log(JSON.stringify({
  bareNodeCaps,
  schemaKeys,
  schema: STUDIO_PARAM_SCHEMA,
  defaultIntent,
  crystalIntent,
  silkIntent,
  crispIntent,
  tactileIntent,
  harmonized,
  harmonizedAgain,
  cssPatch,
  cssPatchHdrOff,
  dom: {
    aliasEqual,
    initialHdrCaps,
    initialHdrEnabled,
    initialBadge,
    initialChecked,
    initialCssVar,
    disabledHdrEnabled,
    disabledAttr,
    disabledCssVar,
    disabledBadge,
    disabledChecked,
    rtHdrEnabled,
    rtAttr,
    rtBadge,
    rtTelemetryHdr: rtSnap.hdr,
  },
}));
"""
        raw = subprocess.check_output(
            [node_bin, "--input-type=module", "-e", js_driver],
            cwd=str(ROOT_DIR),
            text=True,
        )
        out = json.loads(raw)

        self.assertEqual(
            out["bareNodeCaps"],
            {
                "dynamicRangeHigh": False,
                "colorGamutP3": False,
                "cssDisplayP3": False,
                "cssDynamicRangeLimit": False,
                "effectiveHdr": False,
            },
        )
        expected_keys = [
            "blurPx", "glassAlpha", "glassSaturate", "specularAlpha", "hdrBoost",
            "springStiffness", "springDamping", "staggerMs",
            "spotlightPx", "spotlightAlpha", "splitRatio",
        ]
        self.assertEqual(out["schemaKeys"], expected_keys)
        self.assertEqual({out["schema"][k]["group"] for k in expected_keys}, {"glass", "physics", "desktop"})

        self.assertEqual(out["defaultIntent"], "balanced-studio")
        self.assertEqual(out["crystalIntent"], "frosted-crystal")
        self.assertEqual(out["silkIntent"], "silk-cinematic")
        self.assertEqual(out["crispIntent"], "crisp-utility")
        self.assertEqual(out["tactileIntent"], "tactile-focus")

        h = out["harmonized"]
        self.assertEqual(h["humanModifiedKeys"], ["glassAlpha", "hdrBoost", "springStiffness"])
        self.assertEqual(h["values"]["glassAlpha"], 40)
        self.assertEqual(h["values"]["hdrBoost"], 60)
        self.assertEqual(h["values"]["springStiffness"], 250)
        self.assertEqual(h["sources"]["glassAlpha"], "human")
        self.assertEqual(h["sources"]["hdrBoost"], "human")
        self.assertEqual(h["sources"]["springStiffness"], "human")
        self.assertGreaterEqual(len(h["aiHarmonizedKeys"]), 4)
        for ai_key in h["aiHarmonizedKeys"]:
            self.assertNotIn(ai_key, h["humanModifiedKeys"])
            self.assertEqual(h["sources"][ai_key], "ai")
        self.assertEqual(out["harmonizedAgain"]["values"], h["values"])
        self.assertEqual(out["harmonizedAgain"]["sources"], h["sources"])

        patch = out["cssPatch"]
        self.assertIn(':root[data-studio-profile="personal-studio"]', patch)
        for token in (
            "--md-studio-blur-px:",
            "--md-studio-glass-alpha:",
            "--md-studio-glass-saturate:",
            "--md-studio-specular-alpha:",
            "--md-studio-hdr-boost:",
            "--md-studio-glass-brightness:",
            "--md-studio-glass-contrast:",
            "--md-bento-motion-default-spatial-duration:",
            "--md-bento-motion-default-spatial-easing:",
            "--md-bento-motion-default-spatial:",
            '[data-studio-hdr="on"]',
        ):
            self.assertIn(token, patch)
        self.assertIn('[data-studio-hdr="off"]', out["cssPatchHdrOff"])
        self.assertIn("--md-studio-hdr-boost: 0%", out["cssPatchHdrOff"])

        dom = out["dom"]
        self.assertTrue(dom["aliasEqual"])
        self.assertTrue(dom["initialHdrCaps"]["effectiveHdr"])
        self.assertTrue(dom["initialHdrEnabled"])
        self.assertEqual(dom["initialBadge"], "HDR Ready")
        self.assertEqual(dom["initialChecked"], "true")
        self.assertEqual(dom["initialCssVar"], "35%")
        self.assertFalse(dom["disabledHdrEnabled"])
        self.assertEqual(dom["disabledAttr"], "off")
        self.assertEqual(dom["disabledCssVar"], "0%")
        self.assertEqual(dom["disabledBadge"], "HDR Off")
        self.assertEqual(dom["disabledChecked"], "false")
        self.assertFalse(dom["rtHdrEnabled"])
        self.assertEqual(dom["rtAttr"], "off")
        self.assertEqual(dom["rtBadge"], "RT Fallback")
        self.assertFalse(dom["rtTelemetryHdr"]["enabled"])
        self.assertEqual(dom["rtTelemetryHdr"]["boostPct"], 72)

    def test_root_cause_fixes_and_layer4_dom_in_starter_and_bento_html(self) -> None:
        index_html = STARTER_HTML.read_text(encoding="utf-8")
        bento_html = BENTO_HTML.read_text(encoding="utf-8")

        def parse_rules(html_text: str) -> list[audit_md3e.RuleBlock]:
            out: list[audit_md3e.RuleBlock] = []
            for blk, start_line in audit_md3e.extract_style_blocks(html_text):
                out.extend(audit_md3e.parse_css_rules(blk, base_line=start_line))
            return out

        index_rules = parse_rules(index_html)
        bento_rules = parse_rules(bento_html)

        # 1. Scoped .is-toolbar-morphing in BOTH HTML files (never permanent view-transition-name on base toolbar)
        for label, rules, base_sel, vt_name in (
            ("index.html", index_rules, ".md3e-toolbar-adaptive", "md3e-starter-adaptive-toolbar"),
            ("desktop-bento.html", bento_rules, ".bento-adaptive-toolbar", "bento-adaptive-toolbar"),
        ):
            base_vt = [
                r for r in rules
                if base_sel in r.selector and ".is-toolbar-morphing" not in r.selector
                and any(p == "view-transition-name" for p, _, _, _ in r.declarations)
            ]
            self.assertEqual(base_vt, [], f"{label} must not permanently assign view-transition-name on {base_sel}")
            scoped_vt = [
                r for r in rules
                if f"{base_sel}.is-toolbar-morphing" in r.selector
                and any(p == "view-transition-name" and vt_name in v for p, v, _, _ in r.declarations)
            ]
            self.assertTrue(scoped_vt, f"{label} must scope view-transition-name: {vt_name} to .is-toolbar-morphing")

        # 2. Removal of content-visibility: auto on .md3e-wavy-progress + visibilitychange dt loop in BOTH HTML files
        for label, html_text, rules in (
            ("index.html", index_html, index_rules),
            ("desktop-bento.html", bento_html, bento_rules),
        ):
            wavy_rules = [r for r in rules if ".md3e-wavy-progress" in r.selector]
            self.assertTrue(wavy_rules, f"Missing .md3e-wavy-progress rule in {label}")
            for r in wavy_rules:
                self.assertFalse(
                    any(p == "content-visibility" for p, _, _, _ in r.declarations),
                    f"{label} .md3e-wavy-progress must not use content-visibility: auto",
                )
            self.assertIn("document.hidden", html_text)
            self.assertIn("visibilitychange", html_text)

        # 3. index.html Expressive Capsule Toast (.md3e-snackbar corner-full + .md3e-snackbar--action corner-large)
        snackbar_rules = [r for r in index_rules if r.selector.strip() == ".md3e-snackbar"]
        self.assertTrue(snackbar_rules)
        self.assertTrue(
            any(
                p == "border-radius" and "var(--md-sys-shape-corner-full)" in v
                for r in snackbar_rules
                for p, v, _, _ in r.declarations
            ),
            "index.html .md3e-snackbar must use var(--md-sys-shape-corner-full)",
        )
        snackbar_action_rules = [r for r in index_rules if r.selector.strip() == ".md3e-snackbar--action"]
        self.assertTrue(
            any(
                p == "border-radius" and "var(--md-sys-shape-corner-large)" in v
                for r in snackbar_action_rules
                for p, v, _, _ in r.declarations
            ),
            "index.html .md3e-snackbar--action must use var(--md-sys-shape-corner-large)",
        )

        # 4. Zero .studio-caustic-field + Live DOM FLIP interruptible modal + HDR tuner controls
        studio_css = STUDIO_CSS.read_text(encoding="utf-8")
        studio_js = STUDIO_JS.read_text(encoding="utf-8")
        self.assertNotIn("studio-caustic-field", studio_css)
        self.assertNotIn("studio-caustic-field", bento_html)
        self.assertNotIn("bento-vt-scrim", bento_html)
        self.assertNotIn("bento-vt-panel", bento_html)
        self.assertNotIn('html[data-vt-kind="modal"]', bento_html)

        vt_modal_slice_m = re.search(
            r"function openVtModal[\s\S]*?function closeVtModal[\s\S]*?(?=\n\s*(?:vtExpandBtn|function switchBentoView))",
            bento_html,
        )
        self.assertIsNotNone(vt_modal_slice_m, "Missing openVtModal / closeVtModal functions in desktop-bento.html")
        self.assertNotIn("startViewTransition", vt_modal_slice_m.group(0))
        self.assertIn("getVtSourceRect", vt_modal_slice_m.group(0))
        self.assertIn("measureVtTargetRect", vt_modal_slice_m.group(0))
        self.assertIn("modalSpring.setTarget", vt_modal_slice_m.group(0))
        self.assertIn("scrimSpring.setTarget", vt_modal_slice_m.group(0))
        self.assertIn("getBoundingClientRect", bento_html)

        for snippet in (
            "synthesizeSpringLinearCss",
            'data-studio-profile="personal-studio"',
            "md3e-studio.css",
            "md3e-studio.js",
            'id="bento-vt-modal"',
            'id="bento-vt-backdrop"',
            'id="titlebar-status-pill"',
            'id="md3e-studio-telemetry"',
            'id="studio-tuner-panel"',
            'id="studio-cmd-dialog"',
            'id="studio-hdr-badge"',
            'id="btn-studio-hdr"',
            'id="bento-split-handle"',
            'id="btn-studio-harmonize"',
            'id="studio-css-output"',
        ):
            self.assertIn(snippet, bento_html)

        for js_token in (
            "__MD3E_TUNER__",
            "__MD3E_STUDIO__",
            "getHdrCapabilities",
            "isHdrEnabled",
            "setHdrEnabled",
        ):
            self.assertIn(js_token, studio_js)

        self.assertNotIn("240ms", bento_html, "Stale 240ms spring copy/tokens must be replaced in desktop-bento.html")
        self.assertNotRegex(
            bento_html,
            r"<dialog\b[^>]*\brole\s*=\s*[\"']dialog[\"']",
            "Native <dialog id='studio-cmd-dialog'> must not carry redundant role='dialog'",
        )
        for key in (
            "blurPx", "glassAlpha", "glassSaturate", "specularAlpha", "hdrBoost",
            "springStiffness", "springDamping", "staggerMs",
            "spotlightPx", "spotlightAlpha", "splitRatio",
        ):
            self.assertIn(f'data-scrubber-key="{key}"', bento_html)

    def test_five_complex_components_in_starter_and_docs(self) -> None:
        index_html = STARTER_HTML.read_text(encoding="utf-8")

        # 1. Native <dialog id="prim-dialog"> (no redundant role/aria-modal, dialog:modal overscroll-behavior: contain)
        self.assertIn('id="prim-dialog"', index_html)
        self.assertNotRegex(index_html, r"<dialog\b[^>]*\brole\s*=\s*[\"']dialog[\"']")
        self.assertNotRegex(index_html, r"<dialog\b[^>]*\baria-modal\s*=")
        self.assertRegex(index_html, r"dialog:modal[\s\S]*?overscroll-behavior\s*:\s*contain")

        # 2. Outlined Text Field with transparent <fieldset><legend> notch
        for snippet in (
            'id="prim-outlined-field"',
            'id="prim-outlined-input"',
            "<fieldset",
            "<legend",
            'id="prim-text-prefix"',
            'id="prim-outlined-clear"',
            'id="prim-text-counter"',
            'id="prim-text-error"',
            'id="prim-text-error-toggle"',
        ):
            self.assertIn(snippet, index_html)

        # 3. Top-layer [popover="auto"] Menu inside overflow: hidden card
        for snippet in (
            'id="prim-menu-trigger"',
            'id="prim-menu"',
            'popover="auto"',
            "md3e-menu-trap-card",
            'id="prim-submenu-trigger"',
            'id="prim-submenu"',
            "position-area:",
            "transition-behavior: allow-discrete",
            "@starting-style",
        ):
            self.assertIn(snippet, index_html)

        # 4. Select Skin Contract + Top-Layer Listbox + progressive base-select
        for snippet in (
            'id="prim-select-trigger"',
            'id="prim-select-listbox"',
            'data-state="closed"',
            "data-highlighted",
            "data-selected",
            "data-disabled",
            "appearance: base-select",
        ):
            self.assertIn(snippet, index_html)

        # 5. Date Picker Single <-> Range mode + continuous range track
        for snippet in (
            'id="prim-datepicker"',
            'id="prim-dp-mode-single"',
            'id="prim-dp-mode-range"',
            'role="grid"',
            "data-range-start",
            "data-in-range",
            "data-range-end",
            "data-today",
        ):
            self.assertIn(snippet, index_html)

        # Verify all 5 complex components and HDR/FLIP choreography are documented in references/
        text_input_md = (REFERENCES_DIR / "components" / "text-input.md").read_text(encoding="utf-8")
        containment_md = (REFERENCES_DIR / "components" / "containment.md").read_text(encoding="utf-8")
        selection_md = (REFERENCES_DIR / "components" / "selection.md").read_text(encoding="utf-8")
        components_md = (REFERENCES_DIR / "components.md").read_text(encoding="utf-8")
        studio_md = (REFERENCES_DIR / "personal-studio.md").read_text(encoding="utf-8")

        self.assertIn("<fieldset", text_input_md)
        self.assertIn("<legend", text_input_md)
        self.assertIn("data-range-start", text_input_md)
        self.assertIn("data-in-range", text_input_md)
        self.assertIn("overscroll-behavior: contain", containment_md)
        self.assertIn('popover="auto"', containment_md)
        self.assertIn("data-highlighted", selection_md)
        self.assertIn("appearance: base-select", selection_md)
        self.assertIn("Complex Component Architecture Matrix", components_md)
        self.assertEqual(
            audit_md3e.audit_markdown(REFERENCES_DIR / "personal-studio.md", studio_md, mode="personal-studio"),
            [],
        )
        for fence_m in re.finditer(r"```(?:html|css)\s*\n([\s\S]*?)```", studio_md):
            self.assertNotIn("studio-caustic-field", fence_m.group(1))
        self.assertIn("__MD3E_TUNER__", studio_md)
        self.assertIn("hdrBoost", studio_md)
        self.assertIn("Live DOM FLIP", studio_md)

    def test_personal_studio_cli_exit_zero_and_json_contract(self) -> None:
        import contextlib
        import io

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = audit_md3e.main([str(BENTO_HTML), "--mode=personal-studio", "--fail-on=custom", "--json"])
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["mode"], "personal-studio")
        self.assertTrue(payload["custom_extensions"]["active"])
        self.assertEqual(payload["official_compliance"]["score"], 100)
        self.assertEqual(payload["summary"], {"error": 0, "warning": 0, "info": 0, "custom": 0})


class SwarmBugHuntRegressionTests(unittest.TestCase):
    def test_auditor_catches_rt_specificity_keyframe_cascade_and_allow_discrete_drops(self) -> None:
        # 1. MD3E022: higher-specificity blur rule must NOT silently beat lower-specificity RT fallback
        bad_rt_css = """
        :where(.glass):not([class*="md3e-shape"]) {
          backdrop-filter: blur(20px);
          background-color: color-mix(in oklab, var(--md-sys-color-surface) 70%, transparent);
        }
        @media (prefers-reduced-transparency: reduce) {
          :where(.glass) {
            backdrop-filter: none;
            background-color: var(--md-sys-color-surface-container-high);
          }
        }
        """
        m022_bad = [f for f in audit_md3e.Checker(pathlib.Path("rt.css"), mode="strict").run(bad_rt_css) if f.code == "MD3E022"]
        self.assertEqual(len(m022_bad), 1)
        self.assertEqual(m022_bad[0].severity, "error")

        good_rt_css = bad_rt_css.replace(
            ':where(.glass):not([class*="md3e-shape"])',
            ':where(.glass):where(:not([class*="md3e-shape"]))',
        )
        m022_good = [f for f in audit_md3e.Checker(pathlib.Path("rt_ok.css"), mode="strict").run(good_rt_css) if f.code == "MD3E022"]
        self.assertEqual(m022_good, [])

        # 2. MD3E019: @keyframes transform/opacity + fill-mode: both alongside transition without animationend cleanup
        bad_kf_html = """<!doctype html><html lang="en"><head><style>
        @keyframes bento-card-stagger-in { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: none; } }
        .bento-card { transition: transform var(--md-sys-motion-fast-spatial); }
        .bento-card.is-stagger-enter { animation-name: bento-card-stagger-in; animation-duration: var(--md-sys-motion-default-spatial-duration); animation-timing-function: var(--md-sys-motion-default-spatial-easing); animation-fill-mode: both; }
        </style></head><body><main><div class="bento-card is-stagger-enter">Card</div></main></body></html>"""
        m019_bad = [f for f in audit_md3e.Checker(pathlib.Path("kf.html"), mode="strict").run(bad_kf_html) if f.code == "MD3E019"]
        self.assertGreaterEqual(len(m019_bad), 1)
        self.assertEqual(m019_bad[0].severity, "warning")

        # 3. MD3E029: allow-discrete popover placing flex-direction/gap only on :popover-open
        bad_discrete_css = """
        .md3e-select__listbox {
          display: none;
          opacity: 0;
          transition: opacity var(--md-sys-motion-fast-effects), display var(--md-sys-motion-fast-effects);
          transition-behavior: allow-discrete;
        }
        .md3e-select__listbox:popover-open {
          display: flex;
          flex-direction: column;
          gap: 2px;
          opacity: 1;
        }
        """
        m029_bad = [f for f in audit_md3e.Checker(pathlib.Path("sel.css"), mode="strict").run(bad_discrete_css) if f.code == "MD3E029"]
        self.assertEqual(len(m029_bad), 1)
        self.assertEqual(m029_bad[0].severity, "warning")

        good_discrete_css = bad_discrete_css.replace(
            "  opacity: 0;",
            "  flex-direction: column;\n  gap: 2px;\n  opacity: 0;",
        ).replace("  flex-direction: column;\n  gap: 2px;\n  opacity: 1;", "  opacity: 1;")
        m029_good = [f for f in audit_md3e.Checker(pathlib.Path("sel_ok.css"), mode="strict").run(good_discrete_css) if f.code == "MD3E029"]
        self.assertEqual(m029_good, [])

    def test_starter_and_bento_regression_guards(self) -> None:
        bento_html = BENTO_HTML.read_text(encoding="utf-8")
        index_html = STARTER_HTML.read_text(encoding="utf-8")

        # Bento user-bug & critical swarm regression markers
        self.assertIn("grid-template-columns: minmax(0, 1fr) 180px 636px;", bento_html)
        self.assertNotIn("const geomP = vtTarget === 0 ? Math.max(0, p) : p;", bento_html)
        self.assertIn('data-vt-landing', bento_html)
        self.assertIn('id="bento-vt-modal-logs" aria-label="Expanded cluster event diagnostics" tabindex="0"', bento_html)
        self.assertIn("animationcancel", bento_html)
        self.assertIn("cmdDialog?.open", bento_html)
        self.assertIn("md3e-shared-variant", bento_html)

        # Index showcase regression markers
        self.assertIn(".app-frame:has(#inspector-sheet.is-open) .shell", index_html)
        self.assertIn("max(0px, calc((100% - var(--md3e-dp-cap-size)) / 2))", index_html)
        self.assertIn("addMonthsClamped", index_html)
        self.assertIn("minSelectableDate", index_html)

    def test_runtime_spring_morph_and_studio_regressions(self) -> None:
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("Node.js not installed")

        js_driver = r"""
import { createSpringAnimator } from './assets/tokens/md3e-spring.js';
import { createShapeMorpher } from './assets/tokens/md3e-morph.js';

// 1. stop() inside onUpdate must cancel immediately with 0 trailing frames
let postStopCalls = 0;
let stopped = false;
let spring;
spring = createSpringAnimator({
  initialValue: 1,
  stiffness: 1100,
  damping: 1,
  precision: 0.001,
  onUpdate(v) {
    if (stopped) {
      postStopCalls += 1;
      return;
    }
    if (v < 0.7) {
      stopped = true;
      spring.stop();
    }
  },
  onComplete() {
    if (stopped) postStopCalls += 100;
  },
});
spring.setTarget(0);

// 2. morphTo() mid-flight return-reversal & pointercancel cleanup + destroy()
let dUpdates = 0;
const attrs = { 'aria-pressed': 'false' };
const listeners = new Map();
const pathEl = { setAttribute(k, v) { if (k === 'd') dUpdates += 1; } };
const btnEl = {
  getAttribute(k) { return attrs[k] ?? null; },
  setAttribute(k, v) { attrs[k] = String(v); },
  addEventListener(type, fn) { listeners.set(type, fn); },
  removeEventListener(type, fn) { if (listeners.get(type) === fn) listeners.delete(type); },
};
const morpher = createShapeMorpher(pathEl, { initialShape: 'square' });
const unbind = morpher.bindPressMorph(btnEl, {
  restShape: 'square',
  pressedShape: 'cookie-9-sided',
  toggleShape: 'sunny',
});
listeners.get('pointerdown')?.({ button: 0 });
listeners.get('pointerleave')?.({});
listeners.get('click')?.({});
const pressedAfterKeyboardClick = attrs['aria-pressed'];
morpher.destroy();
const remainingListeners = listeners.size;

await new Promise((r) => setTimeout(r, 120));
console.log(JSON.stringify({ postStopCalls, pressedAfterKeyboardClick, remainingListeners, dUpdates }));
"""
        raw = subprocess.check_output(
            [node_bin, "--input-type=module", "-e", js_driver],
            cwd=str(ROOT_DIR),
            text=True,
        )
        out = json.loads(raw)
        self.assertEqual(out["postStopCalls"], 0)
        self.assertEqual(out["pressedAfterKeyboardClick"], "true")
        self.assertEqual(out["remainingListeners"], 0)
        self.assertGreater(out["dUpdates"], 0)


if __name__ == "__main__":
    unittest.main()
