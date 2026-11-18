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
MWC_CSS = ROOT_DIR / "assets" / "tokens" / "md3e-material-web.css"
SPRING_JS = ROOT_DIR / "assets" / "tokens" / "md3e-spring.js"
TAILWIND_THEME_CSS = ROOT_DIR / "assets" / "tailwind" / "md3e-theme.css"
TAILWIND_CONFIG_JS = ROOT_DIR / "assets" / "tailwind" / "tailwind.config.js"
STARTER_HTML = ROOT_DIR / "assets" / "starter" / "index.html"
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


class MaterialWebBridgeTests(unittest.TestCase):
    def test_five_sizes_complete_across_all_button_and_icon_button_variants(self) -> None:
        css = MWC_CSS.read_text(encoding="utf-8")
        variants = ("filled", "outlined", "elevated", "filled-tonal", "text")
        sizes = ("xs", "s", "m", "l", "xl")
        for size in sizes:
            block = extract_var_block(css, rf"\.md3e-size-{size},\s*\n\[data-md3e-size=\"{size}\"\]\s*\{{")
            for v in variants:
                for prop in (
                    "container-height",
                    "container-shape",
                    "leading-space",
                    "trailing-space",
                    "with-leading-icon-leading-space",
                    "with-leading-icon-trailing-space",
                    "icon-size",
                    "label-text-size",
                    "label-text-line-height",
                ):
                    tok = f"--md-{v}-button-{prop}"
                    self.assertIn(tok, block, f"Missing {tok} in .md3e-size-{size}")
                    self.assertNotIn("corner-full", block[tok], f"Morphable button {tok} must not use corner-full")

            self.assertIn("--md-icon-button-state-layer-width", block)
            self.assertIn("--md-icon-button-state-layer-height", block)
            for iv in ("filled", "filled-tonal", "outlined"):
                self.assertIn(f"--md-{iv}-icon-button-container-width", block)
                self.assertIn(f"--md-{iv}-icon-button-container-height", block)

    def test_hit_area_before_parents_have_position_relative(self) -> None:
        css = MWC_CSS.read_text(encoding="utf-8")
        rel_match = re.search(r":(?:is|where)\(([^()]*)\)\s*\{\s*position:\s*relative;", css)
        self.assertIsNotNone(rel_match, "Missing position: relative hit-area parent rule")
        rel_selectors = {s.strip() for s in rel_match.group(1).split(",")}
        self.assertIn(
            "md-fab",
            rel_selectors,
            "md-fab must have position: relative so density ::before hit-area does not escape to viewport",
        )


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


class AuditorTests(unittest.TestCase):
    def _codes(self, text: str, filename: str = "sample.html", *, is_snippet: bool = False) -> list[str]:
        findings = audit_md3e.Checker(pathlib.Path(filename), is_snippet=is_snippet).run(text)
        return [f.code for f in findings]

    def _findings(self, text: str, filename: str = "sample.html", *, is_snippet: bool = False) -> list[audit_md3e.Finding]:
        return audit_md3e.Checker(pathlib.Path(filename), is_snippet=is_snippet).run(text)

    def test_shipped_assets_and_all_21_markdown_docs_pass_compliance(self) -> None:
        reports, scanned = audit_md3e.audit([str(ROOT_DIR / "assets")], [], mode="strict")
        self.assertEqual(scanned, 13)
        self.assertEqual(reports, [], f"Unexpected strict asset findings: {reports}")

        bento_reports, bento_scanned = audit_md3e.audit(
            [str(ROOT_DIR / "assets" / "starter" / "desktop-bento.html")],
            [],
            mode="desktop-bento",
        )
        self.assertEqual(bento_scanned, 1)
        self.assertEqual(bento_reports, [], f"Unexpected desktop-bento HTML findings: {bento_reports}")

        md_reports, md_scanned = audit_md3e.audit(
            [str(SKILL_MD), str(ROOT_DIR / "README.md"), str(OFFICIAL_AUDIT_MD), str(REFERENCES_DIR)],
            [],
            include_markdown=True,
            mode="strict",
        )
        self.assertEqual(md_scanned, 22)
        warn_or_error = [
            (r.path, f)
            for r in md_reports
            for f in r.findings
            if f.severity in ("error", "warning")
        ]
        self.assertEqual(warn_or_error, [], f"Unexpected markdown error/warning findings: {warn_or_error}")

        bento_md_reports, bento_md_scanned = audit_md3e.audit(
            [str(REFERENCES_DIR / "desktop-bento.md")],
            [],
            include_markdown=True,
            mode="desktop-bento",
        )
        self.assertEqual(bento_md_scanned, 1)
        bento_md_we = [
            (r.path, f)
            for r in bento_md_reports
            for f in r.findings
            if f.severity in ("error", "warning")
        ]
        self.assertEqual(bento_md_we, [], f"Unexpected desktop-bento markdown findings: {bento_md_we}")

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

        # MD3E014: multi-line labelled md-icon-button must not false-positive
        good_multiline_icon_btn = '<md-icon-button\n  aria-label="Settings"\n>\n  <md-icon aria-hidden="true">settings</md-icon>\n</md-icon-button>'
        self.assertNotIn("MD3E014", self._codes(good_multiline_icon_btn))
        bad_empty_icon_btn = '<md-icon-button><md-icon aria-hidden="true">settings</md-icon></md-icon-button>'
        self.assertIn("MD3E014", self._codes(bad_empty_icon_btn))

        # MD3E020 unclosed tag & MD3E021 exact line number on multi-line control
        unclosed_md = '<md-outlined-text-field label="Name">'
        self.assertIn("MD3E020", self._codes(unclosed_md))
        multiline_a11y = '<md-fab aria-label="Add">\n  <md-icon>add</md-icon>\n</md-fab>'
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

    def test_new_checks_md3e017_to_md3e021(self) -> None:
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

        # MD3E020: mismatched <md-*> closing tag
        bad_tag = "<md-outlined-text-field label=\"Name\"></md-filled-text-field>"
        self.assertIn("MD3E020", self._codes(bad_tag))

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
            "<md-filled-button>Buy Now</md-filled-button>"
            "<md-filled-button>Subscribe</md-filled-button>"
            "</section></body></html>"
        )
        m025 = [f for f in audit_md3e.Checker(pathlib.Path("btn.html")).run(multi_primary_html) if f.code == "MD3E025"]
        self.assertEqual(len(m025), 1)
        self.assertEqual(m025[0].severity, "info")

        icon_filled_html = (
            "<!doctype html><html><body><section id='toolbar'>"
            "<button type='button' class='md3e-icon-btn--filled' aria-label='Bold'><span class='material-symbols-outlined' aria-hidden='true'>check</span></button>"
            "<button type='button' class='md3e-icon-btn--filled' aria-label='Italic'><span class='material-symbols-outlined' aria-hidden='true'>edit</span></button>"
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


if __name__ == "__main__":
    unittest.main()
