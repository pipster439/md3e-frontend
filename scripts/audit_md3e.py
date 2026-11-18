#!/usr/bin/env python3
"""Audit front-end code for Material 3 Expressive (MD3E) compliance.

Deterministic static checks for the rules that models and humans most often
break when implementing MD3E: hardcoded colours, off-scale corner radii,
duration/easing motion instead of springs, unfocusable controls, sub-48px
targets, off-scale type sizes, icon ligature/font mistakes, unitless
color-mix(), composite animation delay bugs, 9999px morph snaps, legacy
custom-element dependencies, invalid native/headless ARIA contracts,
unbound MD3E modifier classes, and native slider border / fixed menu hit-traps.

Usage
-----
    python audit_md3e.py <path>...            # files or directories
    python audit_md3e.py src --mode=desktop-bento
    python audit_md3e.py src --mode=personal-studio
    python audit_md3e.py src --json           # machine-readable (includes official_compliance.score)
    python audit_md3e.py src --fail-on warning
    python audit_md3e.py docs --markdown      # audit HTML/CSS fences in .md
    python audit_md3e.py src --exclude vendor,node_modules

Authority Levels
----------------
    ERROR    Violates Official Core M3E spec or WCAG 2.2 AA floor (blocks CI by default)
    WARNING  Deviates from Official M3E recommended guidance
    INFO     Project-level engineering preference / default convention
    CUSTOM   Opt-in product extension (--mode=desktop-bento / --mode=personal-studio; excluded from Official Score)

Data & Analytical View Exemptions
---------------------------------
    Add `data-md3e-exempt="data-view"` on analytical containers, or use native `<canvas>`,
    `<table>`, `role="grid"`, 2D trajectory/replay viewports, or chart `<svg>` elements:
    preserves functional axis strokes, 1px table gridlines, series hex palettes, and compact cells.

Finding codes
-------------
    MD3E001  hardcoded hex colour                           (info)
    MD3E002  hardcoded rgb()/hsl()/oklch() colour           (info)
    MD3E003  corner radius off default 10-step scale        (info)
    MD3E004  ad-hoc motion vs spring / OFFICIAL_WEB_CURVES  (warning)
    MD3E005  focus indicator removed / missing              (error)
    MD3E006  target <24px (error) vs <48px/inflated (warning)
    MD3E007  font-size off default 11-step scale            (info)
    MD3E008  no prefers-reduced-motion path                 (warning)
    MD3E009  colour roles without a dark scheme             (warning)
    MD3E010  box-shadow used for elevation                  (info)
    MD3E011  border-radius: 50% instead of full             (warning)
    MD3E012  uppercase label text                           (info)
    MD3E013  `transition: all`                              (warning)
    MD3E014  icon-only control, no accessible name          (error)
    MD3E015  deprecated bottom app bar                      (info)
    MD3E016  deprecated small FAB (40dp)                    (warning)
    MD3E017  invalid Material Symbols icon, URL axes, or missing font (error)
    MD3E018  invalid color-mix() opacity or oklch on neutrals (error)
    MD3E019  composite animation delay or 9999px morph snap (warning)
    MD3E020  legacy <md-*>/@material/web or invalid ARIA contract (error)
    MD3E021  decorative icon missing aria-hidden="true"     (warning)
    MD3E022  backdrop-filter blur lacks reduced-transparency (error)
    MD3E023  box-shadow on masked/morphing shape vs drop-shadow (warning)
    MD3E024  WCAG <4.5:1 contrast or container/on-* mismatch (error)
    MD3E025  multiple enabled filled primary buttons in view (info)
    MD3E026  unbound md3e-* modifier or legacy MWC bridge class (warning)
    MD3E027  slider accent-color without appearance:none or fixed menu hit-trap (warning)
    MD3E028  unbalanced CSS braces { / }                         (error)
    MD3E029  complex-component hygiene (label bleed, dialog scroll/ARIA, widget state) (warning)
    MD3E101  [desktop-bento] 1px border or rectangular box-shadow (custom)
    MD3E102  [desktop-bento] <4 surface-container nesting tiers   (custom)
    MD3E103  [desktop-bento] missing concentric 28px/16px radii   (custom)
    MD3E104  [desktop-bento] missing Hero wave/sparkline/morph anchors (custom)
    MD3E201  [personal-studio] optical glass / clean canvas (no caustic bleed) / HDR / RT hygiene (custom)
    MD3E202  [personal-studio] <dialog> modal overscroll-behavior / role / scroll-lock / focusable controls (custom)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

SEVERITIES = ("error", "warning", "info", "custom")
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITIES)}
AUDIT_MODES = ("strict", "desktop-bento", "personal-studio")


def normalize_mode(val: str) -> str:
    low = val.strip().lower()
    if low == "default":
        return "strict"
    if low in AUDIT_MODES:
        return low
    raise argparse.ArgumentTypeError(
        f"invalid mode {val!r}; choose from {', '.join(AUDIT_MODES)} (alias: default)"
    )


def normalize_severity(val: str) -> str:
    low = val.strip().lower()
    if low == "warn":
        return "warning"
    if low in SEVERITIES:
        return low
    raise argparse.ArgumentTypeError(
        f"invalid severity {val!r}; choose from {', '.join(SEVERITIES)} (alias: warn)"
    )

CODE_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".styl",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".php",
}
CSS_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".styl"}
HTML_EXTENSIONS = {".html", ".htm"}
SKIP_DIRS = {
    "node_modules", "dist", "build", ".next", ".nuxt", "vendor",
    "coverage", ".git", ".cache", "__pycache__",
}

BORDER_PROPS = {
    "border", "border-top", "border-right", "border-bottom", "border-left",
    "border-inline", "border-inline-start", "border-inline-end",
    "border-block", "border-block-start", "border-block-end",
}
SHAPE_SELECTOR_RE = re.compile(
    r"(?:\.md3e-shape(?:-[a-z0-9-]+)?\b|\.bento-morph-cta\b|\.morph-btn\b|\[data-morph)",
    re.IGNORECASE,
)
DENSE_ROW_SELECTOR_RE = re.compile(
    r"(?:^|[\s,>+~.:#\[])(?:tr|td|th|bento-table|bento-log|dense-row|data-row|table-row)\b",
    re.IGNORECASE,
)
DATA_VIEW_SELECTOR_RE = re.compile(
    r"(?:\[\s*data-md3e-exempt\b|\[role\s*=\s*[\"'](?:grid|treegrid)[\"']\s*\]|"
    r"(?:^|[\s,>+~.:#\[])(?:canvas|table|thead|tbody|tfoot|tr|td|th|chart|plot|graph|"
    r"axis|axes|tick|gridline|series|legend|trajectory|replay|viewport-2d|canvas-view|"
    r"telemetry-table|data-table|stats-table|bento-table|bento-log|echarts|recharts|vega)\b|"
    r"\.d3-[\w-]+)",
    re.IGNORECASE,
)

# --- Design system facts the checks are built on ---------------------------

CORNER_SCALE_PX = {0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 28.0, 32.0, 48.0}
FULL_PX = {999.0, 9999.0, 1000.0}

TYPE_SCALE_PX = {11.0, 12.0, 14.0, 16.0, 22.0, 24.0, 28.0, 32.0, 36.0, 45.0, 57.0}
TYPE_SCALE_REM = {round(v / 16.0, 5) for v in TYPE_SCALE_PX}

WCAG_MIN_TARGET = 24.0
M3_RECOMMENDED_TARGET = 48.0
MIN_TOUCH_TARGET = M3_RECOMMENDED_TARGET

LINEAR_SPRING_RE = re.compile(r"\blinear\s*\([^)]*,[^)]*\)")

# Official M3 / M3E Web cubic-bezier curves (allowed as first-class Web implementations).
OFFICIAL_WEB_CURVES = {
    "cubic-bezier(0.42,1.67,0.21,0.90)",
    "cubic-bezier(0.42,1.67,0.21,0.9)",
    "cubic-bezier(0.38,1.21,0.22,1.00)",
    "cubic-bezier(0.38,1.21,0.22,1)",
    "cubic-bezier(0.39,1.29,0.35,0.98)",
    "cubic-bezier(0.27,1.06,0.18,1.00)",
    "cubic-bezier(0.27,1.06,0.18,1)",
    "cubic-bezier(0.31,0.94,0.34,1.00)",
    "cubic-bezier(0.31,0.94,0.34,1)",
    "cubic-bezier(0.34,0.80,0.34,1.00)",
    "cubic-bezier(0.34,0.8,0.34,1)",
    "cubic-bezier(0.34,0.88,0.34,1.00)",
    "cubic-bezier(0.34,0.88,0.34,1)",
    # Google official standard & emphasized Web easing tokens (--md-sys-motion-easing-*)
    "cubic-bezier(0.2,0,0,1)",
    "cubic-bezier(0.2,0.0,0.0,1.0)",
    "cubic-bezier(0.05,0.7,0.1,1)",
    "cubic-bezier(0.05,0.7,0.1,1.0)",
    "cubic-bezier(0.3,0,0.8,0.15)",
    "cubic-bezier(0,0,0,1)",
    "cubic-bezier(0,0.0,0.0,1.0)",
    "cubic-bezier(0.3,0,1,1)",
    "cubic-bezier(0.3,0,1.0,1.0)",
    "cubic-bezier(0.4,0,0.2,1)",
    "cubic-bezier(0.4,0.0,0.2,1.0)",
}

OFFICIAL_WEB_CURVE_TUPLES = {
    (0.42, 1.67, 0.21, 0.9),
    (0.38, 1.21, 0.22, 1.0),
    (0.39, 1.29, 0.35, 0.98),
    (0.27, 1.06, 0.18, 1.0),
    (0.31, 0.94, 0.34, 1.0),
    (0.34, 0.8, 0.34, 1.0),
    (0.34, 0.88, 0.34, 1.0),
    (0.2, 0.0, 0.0, 1.0),
    (0.05, 0.7, 0.1, 1.0),
    (0.3, 0.0, 0.8, 0.15),
    (0.0, 0.0, 0.0, 1.0),
    (0.3, 0.0, 1.0, 1.0),
    (0.4, 0.0, 0.2, 1.0),
}

# Curated aliases hallucinated from Lucide / FontAwesome / Heroicons.
BAD_ICON_ALIASES = {
    "plus": "add",
    "plus_circle": "add_circle",
    "trash": "delete",
    "trash_2": "delete",
    "cog": "settings",
    "gear": "settings",
    "bell": "notifications",
    "bell_ring": "notifications_active",
    "heart": "favorite",
    "heart_filled": "favorite",
    "moon": "dark_mode",
    "sun": "light_mode",
    "x": "close",
    "times": "close",
    "close_icon": "close",
    "pencil": "edit",
    "pen": "edit",
    "user": "person",
    "bars": "menu",
    "hamburger": "menu",
    "nav_menu": "menu",
    "sliders": "tune",
    "eye": "visibility",
    "eye_off": "visibility_off",
    "eye_slash": "visibility_off",
    "copy": "content_copy",
    "clipboard": "content_paste",
    "calendar": "calendar_today",
    "clock": "schedule",
    "magnifying_glass": "search",
    "external_link": "open_in_new",
    "find": "search",
    "back": "arrow_back",
    "success": "check_circle",
    "house": "home",
    "home_icon": "home",
    "adjustments": "tune",
    "account": "person",
    "exclamation_triangle": "warning",
    "alert_triangle": "warning",
    "info_circle": "info",
    "download_cloud": "cloud_download",
    "upload_cloud": "cloud_upload",
    "log_out": "logout",
    "sign_out": "logout",
}

CANONICAL_MS_AXES = {"fill": "FILL", "grad": "GRAD", "opsz": "opsz", "wght": "wght"}
MS_FONT_AXES_RE = re.compile(
    r"Material(?:\+|%20|\s)Symbols(?:\+|%20|\s)(?:Outlined|Rounded|Sharp):([A-Za-z0-9_,]+)@",
    re.IGNORECASE,
)
NEUTRAL_OKLCH_RE = re.compile(
    r"--md-sys-color-(?:surface[a-z-]*|on-surface[a-z-]*|outline[a-z-]*|shadow|scrim|"
    r"inverse-surface|inverse-on-surface)\b|--md-ref-palette-neutral(?:-variant)?-\d+\b|"
    r"\b(?:currentColor|white|black|gr[ae]y)\b",
    re.IGNORECASE,
)

HEX_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})"
    r"(?![0-9a-zA-Z_-])"
)
FUNC_COLOR_RE = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\s*\(")
TIME_RE = re.compile(r"(?<![\w-])(\d*\.?\d+)(m?s)\b")
EASING_KEYWORD_RE = re.compile(
    r"(?:^|[\s,(])(ease|ease-in|ease-out|ease-in-out|step-start|step-end)\b"
)
CURVE_FUNC_RE = re.compile(r"\b(cubic-bezier|steps)\s*\(")
CUBIC_BEZIER_CALL_RE = re.compile(r"cubic-bezier\s*\([^)]+\)")
PROP_VALUE_RE = re.compile(r"^(?P<prop>-{0,2}[a-zA-Z][\w-]*)\s*:\s*(?P<value>[\s\S]*?)\s*$")

MOTION_PROPS = (
    "transition", "transition-duration", "transition-timing-function",
    "animation", "animation-duration", "animation-timing-function",
)
RADIUS_PROPS = (
    "border-radius", "border-top-left-radius", "border-top-right-radius",
    "border-bottom-left-radius", "border-bottom-right-radius",
    "border-start-start-radius", "border-start-end-radius",
    "border-end-start-radius", "border-end-end-radius",
)

INTERACTIVE_SELECTOR_RE = re.compile(
    r"(?:^|[\s,>+~.:#\[])(?:btn|button|icon-button|iconbutton|icon-btn|fab|chip"
    r"|tab|tab-item|nav-item|navitem|list-item|listitem|menu-item|menuitem"
    r"|checkbox|radio|switch|segmented|toggle|control|select|input|text-field"
    r"|toolbar-btn|group-btn|split-btn__action|split-btn__arrow|split-btn__trigger)",
    re.IGNORECASE,
)
DECORATIVE_SUBELEMENT_RE = re.compile(
    r"(?:__|-)(?:icon|chevron|label|divider|pill|scrim|dot|morph|box)\b"
    r"|(?:__|-)(?:track|thumb|handle|indicator|checkmark|stop)\b"
    r"|__(?:ring|circle|avatar|badge)\b",
    re.IGNORECASE,
)
RANGE_INPUT_ATTR_RE = re.compile(
    r"\[[^\]]*\btype\s*=\s*(?:[\"']range[\"']|range\b)",
    re.IGNORECASE,
)
SLIDER_NON_CONTROL_WRAPPER_RE = re.compile(
    r"(?:^|[-_])(?:range|slider)s?(?:__|[-_]+(?:block|wrap(?:per)?|container|box|group|row|col|column|label|title|header|footer|value|readout|ticks?|stops?|track|thumb|handle|fill|field|panel|card|section|bar|area|meta|info|hint|text|icon))(?![a-z0-9])"
    r"|(?:__|[-_])(?:block|wrap(?:per)?|container|box|group|row|col|column|label|title|header|footer|value|readout|track|thumb|handle|fill|panel|card|section)$",
    re.IGNORECASE,
)
FIXED_MENU_WRAPPER_RE = re.compile(
    r"(?:fab[-_]?menu[-_]?(?:container|wrap(?:per)?)|floating[-_]?menu[-_]?(?:container|wrap(?:per)?))",
    re.IGNORECASE,
)
INTERACTIVE_ELEMENT_RE = re.compile(
    r"<(?:button|a\s|input|select|textarea|details|summary)"
    r"|\brole\s*=\s*[\"'](?:button|switch|checkbox|radio|tab|menuitem|option|slider|combobox)[\"']",
    re.IGNORECASE,
)

STYLE_ATTR_RE = re.compile(r"""\bstyle\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
TAG_ATTRS_PAT = r"""(?:[^>"'{}]|"[^"]*"|'[^']*'|\{(?:[^{}]|\{[^}]*\})*\})*"""
SPAN_ELEM_RE = re.compile(rf"""<span\b({TAG_ATTRS_PAT})>([^<]*)</span>""", re.IGNORECASE)
MS_CLASS_RE = re.compile(
    r"""\bclass\s*=\s*(?:"[^"]*\bmaterial-symbols-(?:outlined|rounded|sharp)\b[^"]*"|'[^']*\bmaterial-symbols-(?:outlined|rounded|sharp)\b[^']*')""",
    re.IGNORECASE,
)
ICON_SPAN_RE = re.compile(
    r"""<span\b([^>]*\bclass\s*=\s*["'][^"']*\bmaterial-symbols-(?:outlined|rounded|sharp)\b[^"']*["'][^>]*)>([^<]*)</span>""",
    re.IGNORECASE,
)
LEGACY_MD_TAG_RE = re.compile(rf"""<(/?)(md-[a-z0-9-]+)\b({TAG_ATTRS_PAT})>""", re.IGNORECASE)
LEGACY_MWC_REF_RE = re.compile(r"@material/web\b|md3e-material-web\.css|esm\.run/@material/web", re.IGNORECASE)
LEGACY_MWC_CLASS_RE = re.compile(
    r"(?<![\w-])(?:md3e-size-(?:xs|s|m|l|xl)|md3e-width-(?:narrow|wide)|md3e-fab-(?:medium|large))(?![\w-])",
    re.IGNORECASE,
)
OPEN_TAG_RE = re.compile(rf"""<([a-z][a-z0-9:-]*)\b({TAG_ATTRS_PAT})(/?)>""", re.IGNORECASE)
COLOR_MIX_RE = re.compile(r"color-mix\s*\(([^()]+|\([^()]*\))*\)")
COMPOSITE_SPRING_VAR_RE = re.compile(
    r"var\(\s*--md-sys-motion-(?:fast|default|slow)-(?:spatial|effects)(?:-bezier)?\s*\)"
)
FULL_RADIUS_VALUE_RE = re.compile(
    r"(?:var\(\s*--md-sys-shape-corner-full\s*\)|\b9999px\b|\b999px\b)"
)

TOKEN_FILE_HINTS = ("tokens", "theme", "palette", "design-system", "md3e-")


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    fix: str
    path: str
    line: int
    snippet: str = ""

    def to_dict(self) -> dict:
        return {
            "code": self.code, "severity": self.severity, "message": self.message,
            "fix": self.fix, "path": self.path, "line": self.line,
            "snippet": self.snippet,
        }


@dataclass
class FileReport:
    path: str
    findings: list[Finding] = field(default_factory=list)


@dataclass
class RuleBlock:
    selector: str
    start_line: int
    in_reduced_motion: bool
    declarations: list[tuple[str, str, int, str]] = field(default_factory=list)
    in_forced_colors: bool = False
    custom_color_vars: dict[str, tuple[str, int, str]] = field(default_factory=dict)
    in_reduced_transparency: bool = False
    in_prefers_contrast: bool = False


LAYOUT_ALLOW_DISCRETE_PROPS = frozenset({
    "flex-direction",
    "grid-template-columns",
    "grid-template-rows",
    "flex-wrap",
    "gap",
    "row-gap",
    "column-gap",
})
OPEN_STATE_PSEUDO_RE = re.compile(r"(?::popover-open|\.\:popover-open|\[open\b|:open\b)", re.I)


def _strip_functional_pseudo(text: str, name: str) -> str:
    """Remove `:name(...)` functional pseudos with balanced parentheses."""
    out: list[str] = []
    i = 0
    low = text.lower()
    pat = f":{name}("
    n = len(text)
    while i < n:
        if low.startswith(pat, i):
            depth = 1
            j = i + len(pat)
            while j < n and depth > 0:
                if text[j] == "(":
                    depth += 1
                elif text[j] == ")":
                    depth -= 1
                j += 1
            i = j
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _extract_balanced_call_args(text: str, start_idx: int) -> tuple[str, int]:
    """Given index at `(`, return `(inner, end_idx_after_close)`."""
    depth = 1
    j = start_idx + 1
    n = len(text)
    while j < n and depth > 0:
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
        j += 1
    return text[start_idx + 1 : j - 1 if depth == 0 else j], j


def _branch_specificity(branch: str) -> tuple[int, int, int]:
    """Compute CSS specificity `(a, b, c)` honouring `:where()` = 0 and `:is()/:not()/:has()` max arg."""
    s = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', "[]", branch.strip())
    s = _strip_functional_pseudo(s, "where")
    a = b = c = 0

    def eval_segment(seg: str) -> tuple[int, int, int]:
        la = lb = lc = 0
        # Recursively fold :is(...), :not(...), :has(...)
        buf: list[str] = []
        idx = 0
        low_seg = seg.lower()
        while idx < len(seg):
            matched_fn = None
            for fn in ("is", "not", "has", "matches"):
                if low_seg.startswith(f":{fn}(", idx):
                    matched_fn = fn
                    break
            if matched_fn:
                inner, end_i = _extract_balanced_call_args(seg, idx + len(matched_fn) + 1)
                args = split_top_level_commas(inner)
                best = max((_branch_specificity(arg) for arg in args if arg.strip()), default=(0, 0, 0))
                la += best[0]
                lb += best[1]
                lc += best[2]
                idx = end_i
            else:
                buf.append(seg[idx])
                idx += 1
        rem = "".join(buf)
        # Strip ::pseudo-elements first -> c += 1 each
        la += len(re.findall(r"#[a-zA-Z_-][a-zA-Z0-9_-]*", rem))
        rem = re.sub(r"#[a-zA-Z_-][a-zA-Z0-9_-]*", " ", rem)
        pe_matches = re.findall(r"::[a-zA-Z_-][a-zA-Z0-9_-]*(?:\([^)]*\))?", rem)
        lc += len(pe_matches)
        rem = re.sub(r"::[a-zA-Z_-][a-zA-Z0-9_-]*(?:\([^)]*\))?", " ", rem)
        # Attribute selectors & classes & single-colon pseudo-classes -> b += 1 each
        lb += len(re.findall(r"\[[^\]]*\]", rem))
        rem = re.sub(r"\[[^\]]*\]", " ", rem)
        lb += len(re.findall(r"\.[a-zA-Z_-][a-zA-Z0-9_-]*", rem))
        rem = re.sub(r"\.[a-zA-Z_-][a-zA-Z0-9_-]*", " ", rem)
        lb += len(re.findall(r":[a-zA-Z_-][a-zA-Z0-9_-]*(?:\([^)]*\))?", rem))
        rem = re.sub(r":[a-zA-Z_-][a-zA-Z0-9_-]*(?:\([^)]*\))?", " ", rem)
        # Remaining type selectors (skip combinators & universal *)
        for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_-]*", rem):
            lc += 1
        return (la, lb, lc)

    ta, tb, tc = eval_segment(s)
    return (a + ta, b + tb, c + tc)


def _selector_subject_tokens(sel: str) -> set[str]:
    """Extract normalized class/id tokens from a selector for RT overlap matching."""
    tokens = set(re.findall(r"(?:\.|#)[a-zA-Z_-][a-zA-Z0-9_-]*", sel))
    if not tokens:
        for t in re.findall(r"\b(?:dialog|aside|header|nav|section|footer)\b", sel.lower()):
            tokens.add(t)
    return tokens


def _selector_stem(branch: str) -> str:
    """Extract canonical base component selector stem before state pseudos/attributes."""
    s = re.sub(r":popover-open|\.\:popover-open|\[open[^\]]*\]|\[data-state[^\]]*\]|:open\b|:focus-visible|:hover|:active", "", branch, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _extract_keyframe_props(cleaned_css: str) -> dict[str, set[str]]:
    """Map @keyframes names to animated CSS property names."""
    kf_map: dict[str, set[str]] = {}
    for m in re.finditer(r"@keyframes\s+([a-zA-Z0-9_-]+)\s*\{", cleaned_css):
        name = m.group(1)
        depth = 1
        j = m.end()
        n = len(cleaned_css)
        while j < n and depth > 0:
            if cleaned_css[j] == "{":
                depth += 1
            elif cleaned_css[j] == "}":
                depth -= 1
            j += 1
        body = cleaned_css[m.end() : j - 1 if depth == 0 else j]
        props = {pm.group(1).lower() for pm in re.finditer(r"([a-z-]+)\s*:", body, re.I)}
        kf_map[name] = props
    return kf_map


# ===========================================================================
# Contrast & HTML Exemption Helpers
# ===========================================================================

OPAQUE_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")
SYS_COLOR_VAR_RE = re.compile(r"^var\(\s*(--md-sys-color-[a-z0-9-]+)(?:\s*,[^)]*)?\s*\)$", re.IGNORECASE)
CANONICAL_COLOR_PAIRS = (
    ("primary", "on-primary"),
    ("primary-container", "on-primary-container"),
    ("secondary", "on-secondary"),
    ("secondary-container", "on-secondary-container"),
    ("tertiary", "on-tertiary"),
    ("tertiary-container", "on-tertiary-container"),
    ("error", "on-error"),
    ("error-container", "on-error-container"),
    ("surface", "on-surface"),
    ("surface-container-low", "on-surface"),
    ("surface-container", "on-surface"),
    ("surface-container-high", "on-surface-variant"),
    ("inverse-surface", "inverse-on-surface"),
    ("primary-fixed", "on-primary-fixed"),
    ("secondary-fixed", "on-secondary-fixed"),
    ("tertiary-fixed", "on-tertiary-fixed"),
)


def _srgb_luminance(hex_color: str) -> float:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

    def _chan(v: float) -> float:
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    return 0.2126 * _chan(r) + 0.7152 * _chan(g) + 0.0722 * _chan(b)


def srgb_contrast_ratio(hex_a: str, hex_b: str) -> float:
    la = _srgb_luminance(hex_a)
    lb = _srgb_luminance(hex_b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


VOID_HTML_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
EXEMPT_ATTR_OR_CLASS_RE = re.compile(
    r"\bdata-md3e-exempt\b|\brole\s*=\s*[\"'](?:grid|treegrid)[\"']|"
    r"\b(?:class|id)\s*=\s*[\"'][^\"']*\b(?:chart|plot|graph|axis|axes|"
    r"trajectory|replay[-_]?viewport|canvas[-_]?viewport|map[-_]?viewport|"
    r"data-table|stats-table|telemetry-table|analytics-grid|oscilloscope)\b",
    re.IGNORECASE,
)


def find_exempt_line_set(markup_clean: str) -> set[int]:
    """Return 1-based line numbers inside explicit data-view / analytical subtrees."""
    exempt_lines: set[int] = set()
    # Mark explicit analytical <svg> blocks directly from opening tag to closing </svg>
    for svg_m in re.finditer(r"<svg\b([^>]*)>([\s\S]*?)</svg>", markup_clean, re.IGNORECASE):
        attrs, inner = svg_m.group(1), svg_m.group(2)
        is_chart_svg = bool(
            re.search(r"chart|plot|graph|axis|axes|trajectory|replay", attrs, re.I)
            or (
                re.search(r"<(?:line|polyline)\b|\bclass\s*=\s*[\"'][^\"']*\b(?:axis|gridline)\b", inner, re.I)
                and not re.search(r"wave|sparkline|md3e-loading|morph-btn", attrs + inner, re.I)
            )
        )
        if is_chart_svg:
            start_ln = markup_clean[:svg_m.start()].count("\n") + 1
            end_ln = markup_clean[:svg_m.end()].count("\n") + 1
            exempt_lines.update(range(start_ln, end_ln + 1))

    tag_re = re.compile(rf"<(/?)([a-zA-Z][a-zA-Z0-9:-]*)\b({TAG_ATTRS_PAT})(/?)>")
    stack: list[tuple[str, int, bool]] = []
    for m in tag_re.finditer(markup_clean):
        is_close = m.group(1) == "/"
        tag = m.group(2).lower()
        attrs = m.group(3)
        self_closing = bool(m.group(4)) or tag in VOID_HTML_TAGS
        ln = markup_clean[:m.start()].count("\n") + 1
        end_ln = markup_clean[:m.end()].count("\n") + 1
        if not is_close:
            is_exempt = bool(
                tag in ("canvas", "table")
                or EXEMPT_ATTR_OR_CLASS_RE.search(attrs)
            )
            if self_closing:
                if is_exempt or any(item[2] for item in stack):
                    exempt_lines.update(range(ln, end_ln + 1))
            else:
                stack.append((tag, ln, is_exempt))
        else:
            for idx in range(len(stack) - 1, -1, -1):
                open_tag, open_ln, is_exempt = stack[idx]
                if open_tag == tag:
                    del stack[idx:]
                    if is_exempt:
                        exempt_lines.update(range(open_ln, end_ln + 1))
                    break
    for _, open_ln, is_exempt in stack:
        if is_exempt:
            exempt_lines.update(range(open_ln, markup_clean.count("\n") + 2))
    return exempt_lines


# ===========================================================================
# Parsing helpers
# ===========================================================================

def is_token_file(path: pathlib.Path) -> bool:
    name = path.name.lower()
    posix = str(path).replace("\\", "/").lower()
    return any(h in name for h in TOKEN_FILE_HINTS) or "/tokens/" in posix


def strip_css_comments(text: str) -> str:
    """Replace /* ... */ comments with same number of newlines to preserve line numbers."""
    def _repl(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")
    return re.sub(r"/\*[\s\S]*?\*/", _repl, text)


def extract_style_blocks(html_text: str) -> list[tuple[str, int]]:
    """Return [(css_text, start_line)] for every <style>...</style> block."""
    blocks: list[tuple[str, int]] = []
    for m in re.finditer(r"<style\b[^>]*>([\s\S]*?)</style>", html_text, re.IGNORECASE):
        start_line = html_text[:m.start(1)].count("\n") + 1
        blocks.append((m.group(1), start_line))
    return blocks


def strip_tag_blocks(text: str, tag: str) -> str:
    """Replace <tag>...</tag> bodies with blank lines so line numbers remain exact."""
    pattern = re.compile(rf"<{tag}\b[^>]*>[\s\S]*?</{tag}>", re.IGNORECASE)
    return pattern.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def strip_html_comments(text: str) -> str:
    """Replace <!-- ... --> comments with blank lines so line numbers remain exact."""
    return re.sub(r"<!--[\s\S]*?-->", lambda m: "\n" * m.group(0).count("\n"), text)


def iter_icon_matches(text: str) -> list[re.Match[str]]:
    """Return Material Symbols <span> matches across single/multi-line tags."""
    matches: list[re.Match[str]] = []
    for m in SPAN_ELEM_RE.finditer(text):
        if MS_CLASS_RE.search(m.group(1)):
            matches.append(m)
    matches.sort(key=lambda m: m.start())
    return matches


def parse_css_rules(css_text: str, base_line: int = 1) -> list[RuleBlock]:
    """Brace-aware CSS rule extractor tracking reduced-motion & forced-colors."""
    cleaned = strip_css_comments(css_text)
    rules: list[RuleBlock] = []
    stack: list[tuple[str, bool, bool, bool, bool, int]] = []
    current_decls: dict[int, list[tuple[str, str, int, str]]] = {}
    current_custom_colors: dict[int, dict[str, tuple[str, int, str]]] = {}
    buf: list[str] = []
    buf_start_line = base_line
    lineno = base_line
    in_string: str | None = None
    escape = False

    def flush_declarations(text_chunk: str, chunk_start_line: int) -> tuple[list[tuple[str, str, int, str]], dict[str, tuple[str, int, str]]]:
        out: list[tuple[str, str, int, str]] = []
        custom_colors: dict[str, tuple[str, int, str]] = {}
        cur_line = chunk_start_line
        for piece in text_chunk.split(";"):
            nl_before = len(piece) - len(piece.lstrip("\r\n"))
            piece_line = cur_line + piece[:nl_before].count("\n")
            cur_line += piece.count("\n")
            stripped = piece.strip()
            if not stripped:
                continue
            m = PROP_VALUE_RE.match(stripped)
            if not m:
                continue
            prop = m.group("prop").lower()
            val = m.group("value")
            clean_snip = re.sub(r"\s+", " ", stripped)
            if prop.startswith("--"):
                if prop.startswith("--md-sys-color-"):
                    clean_v = strip_important(val).strip()
                    if OPAQUE_HEX_RE.fullmatch(clean_v):
                        custom_colors[prop] = (clean_v, piece_line, clean_snip)
                continue
            out.append((prop, val, piece_line, clean_snip))
        return out, custom_colors

    i = 0
    n = len(cleaned)
    while i < n:
        ch = cleaned[i]
        if escape:
            buf.append(ch)
            escape = False
            if ch == "\n":
                lineno += 1
            i += 1
            continue
        if ch == "\\" and in_string:
            buf.append(ch)
            escape = True
            i += 1
            continue
        if in_string:
            buf.append(ch)
            if ch == in_string:
                in_string = None
            if ch == "\n":
                lineno += 1
            i += 1
            continue
        if ch in ('"', "'"):
            in_string = ch
            buf.append(ch)
            i += 1
            continue
        if ch == "{":
            header = "".join(buf).strip()
            if ";" in header and stack:
                # Pending declarations before a nested rule block
                prefix, nested_sel = header.rsplit(";", 1)
                p_decls, p_colors = flush_declarations(prefix, buf_start_line)
                current_decls.setdefault(len(stack) - 1, []).extend(p_decls)
                current_custom_colors.setdefault(len(stack) - 1, {}).update(p_colors)
                header = nested_sel.strip()
            is_rm = bool(re.search(r"prefers-reduced-motion\s*:\s*reduce", header, re.I))
            is_fc = bool(re.search(r"forced-colors\s*:\s*active", header, re.I))
            is_rt = bool(re.search(r"prefers-reduced-transparency\s*:\s*reduce", header, re.I))
            is_hc = bool(re.search(r"prefers-contrast\s*:\s*more", header, re.I))
            parent_rm = stack[-1][1] if stack else False
            parent_fc = stack[-1][2] if stack else False
            parent_rt = stack[-1][3] if stack else False
            parent_hc = stack[-1][4] if stack else False
            stack.append((header, parent_rm or is_rm, parent_fc or is_fc, parent_rt or is_rt, parent_hc or is_hc, lineno))
            current_decls[len(stack) - 1] = []
            current_custom_colors[len(stack) - 1] = {}
            buf = []
            buf_start_line = lineno
        elif ch == "}":
            body = "".join(buf)
            if stack:
                idx = len(stack) - 1
                sel, in_rm, in_fc, in_rt, in_hc, sel_line = stack.pop()
                b_decls, b_colors = flush_declarations(body, buf_start_line)
                decls = current_decls.pop(idx, []) + b_decls
                c_colors = {**current_custom_colors.pop(idx, {}), **b_colors}
                if sel and not sel.startswith("@") and (decls or c_colors):
                    rules.append(RuleBlock(sel, sel_line, in_rm, decls, in_fc, c_colors, in_rt, in_hc))
            buf = []
            buf_start_line = lineno
        else:
            if not buf and ch in (" ", "\t", "\r", "\n"):
                if ch == "\n":
                    lineno += 1
                    buf_start_line = lineno
                i += 1
                continue
            buf.append(ch)
            if ch == "\n":
                lineno += 1
        i += 1
    return rules


def iter_inline_declarations(style_val: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for piece in style_val.split(";"):
        piece = piece.strip()
        if not piece:
            continue
        m = PROP_VALUE_RE.match(piece)
        if not m:
            continue
        prop = m.group("prop").lower()
        if prop.startswith("--"):
            continue
        out.append((prop, m.group("value")))
    return out


def parse_px(value: str) -> float | None:
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*px", value.strip())
    return float(m.group(1)) if m else None


def is_var(value: str) -> bool:
    return "var(" in value


def normalize_selector_base(selector: str) -> str:
    return re.sub(r"::(?:before|after)\b", "", selector).strip()


# ===========================================================================
# Declaration-level checks
# ===========================================================================

def strip_important(value: str) -> str:
    return re.sub(r"\s*!important\s*$", "", value.strip(), flags=re.IGNORECASE)


def split_top_level_commas(value: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for idx, ch in enumerate(value):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            parts.append(value[start:idx].strip())
            start = idx + 1
    parts.append(value[start:].strip())
    return [p for p in parts if p]


def _strip_nested_parens(text: str) -> str:
    out: list[str] = []
    depth = 0
    for ch in text:
        if ch == "(":
            if depth == 0:
                out.append(" __PAREN__ ")
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return "".join(out)


def check_hex(cx, value, lineno, line) -> None:
    if cx.token_file:
        return
    cleaned = re.sub(r"url\(\s*#[\w-]+\s*\)", "", value, flags=re.IGNORECASE)
    hit = HEX_RE.search(cleaned)
    if hit:
        cx.add("MD3E001", "info",
               f"Hardcoded colour {hit.group(0)} (project token convention).",
               "Prefer a colour role token, e.g. var(--md-sys-color-primary) or "
               "var(--md-sys-color-surface-container-high), so light/dark and contrast themes propagate automatically.",
               cx.path, lineno, line)


def check_func_color(cx, value, lineno, line) -> None:
    if cx.token_file:
        return
    m = FUNC_COLOR_RE.search(value)
    if m:
        cx.add("MD3E002", "info",
               f"Hardcoded colour via {m.group(0).strip()[:-1]}(...) (project token convention).",
               "Prefer a colour role token or a state-layer overlay in currentColor via opacity / color-mix(in oklab, ...).",
               cx.path, lineno, line)


def check_color_mix(cx, value, lineno, line) -> None:
    if "color-mix(" not in value.lower() and not re.search(r"color-mix\s*\(", value, re.I):
        return
    idx = 0
    for cm in re.finditer(r"color-mix\s*\(", value, re.I):
        if cm.start() < idx:
            continue
        depth = 0
        end = len(value)
        for j in range(cm.end() - 1, len(value)):
            if value[j] == "(":
                depth += 1
            elif value[j] == ")":
                depth -= 1
                if depth == 0:
                    end = j
                    break
        inner = value[cm.end():end]
        idx = end + 1

        top_args = [a.strip() for a in _strip_nested_parens(inner).split(",")]
        stop_args = top_args[1:] if len(top_args) > 1 else top_args
        bare_number = any(
            re.search(r"(?<![\w.-])(?:\d*\.\d+|\d+)(?!\s*%)(?=\s|$)", seg)
            for seg in stop_args
        )
        unscaled_opacity_var = (
            bool(re.search(r"var\(\s*--md-sys-state-[a-z-]+-opacity\s*\)", inner))
            and not re.search(r"(?:\*\s*100%|100%\s*\*)", inner)
        )
        if bare_number or unscaled_opacity_var:
            cx.add("MD3E018", "error",
                   "color-mix() requires percentage weights, not unitless opacity decimals.",
                   "Multiply opacity tokens by 100% inside calc(), e.g. "
                   "calc(var(--md-sys-state-hover-state-layer-opacity) * 100%), "
                   "or use a ::after state-layer overlay with CSS opacity.",
                   cx.path, lineno, line)

        if top_args and re.match(r"^\s*in\s+oklch\b", top_args[0], re.I) and NEUTRAL_OKLCH_RE.search(inner):
            cx.add("MD3E018", "error",
                   "color-mix(in oklch, ...) on neutral or surface colours can trigger Chromium's powerless-hue reddish shift.",
                   "Always use `color-mix(in oklab, ...)` when tinting or mixing neutral, surface, outline, shadow, or `currentColor` values.",
                   cx.path, lineno, line)


def _extract_color_role(val: str) -> str | None:
    m = SYS_COLOR_VAR_RE.fullmatch(strip_important(val).strip())
    if not m:
        return None
    name = m.group(1).lower()
    return name[len("--md-sys-color-"):] if name.startswith("--md-sys-color-") else None


def check_role_pairing_and_contrast(
    cx,
    decls: list[tuple[str, str, int, str]],
    *,
    is_data_view: bool = False,
) -> None:
    bg_decl = None
    fg_decl = None
    font_size_px = 14.0
    is_bold = False
    for prop, value, lineno, raw in decls:
        if prop in ("background-color", "background"):
            bg_decl = (value, lineno, raw)
        elif prop == "color":
            fg_decl = (value, lineno, raw)
        elif prop == "font-size":
            px = parse_px(strip_important(value))
            if px is not None:
                font_size_px = px
        elif prop == "font-weight":
            fw = strip_important(value).lower()
            if fw == "bold" or (fw.isdigit() and int(fw) >= 700):
                is_bold = True

    if not bg_decl or not fg_decl:
        return

    bg_val, bg_ln, bg_raw = bg_decl
    fg_val, fg_ln, fg_raw = fg_decl
    lineno = max(bg_ln, fg_ln)
    snippet = f"{bg_raw}; {fg_raw}"

    bg_role = _extract_color_role(bg_val)
    fg_role = _extract_color_role(fg_val)
    if bg_role and fg_role:
        mismatch = False
        if bg_role in ("primary", "secondary", "tertiary", "error"):
            if (fg_role.startswith("on-") or fg_role.startswith("inverse-on-")) and fg_role != f"on-{bg_role}":
                mismatch = True
        elif bg_role.endswith("-container") and not bg_role.startswith("surface-"):
            if (fg_role.startswith("on-") or fg_role.startswith("inverse-on-")) and fg_role != f"on-{bg_role}":
                mismatch = True
        elif bg_role.startswith("surface"):
            if re.match(r"^(?:on-(?:primary|secondary|tertiary|error)|inverse-on-surface)", fg_role):
                mismatch = True
        elif bg_role == "inverse-surface":
            if (fg_role.startswith("on-") or fg_role.startswith("inverse-on-")) and fg_role != "inverse-on-surface":
                mismatch = True
        elif re.match(r"^(primary|secondary|tertiary)-fixed(?:-dim)?$", bg_role):
            base = bg_role.split("-")[0]
            if fg_role.startswith(("on-", "inverse-on-")) and fg_role not in (f"on-{base}-fixed", f"on-{base}-fixed-variant"):
                mismatch = True

        if mismatch:
            cx.add(
                "MD3E024", "error",
                f"Semantic role mismatch: foreground `--md-sys-color-{fg_role}` paired with container `--md-sys-color-{bg_role}`.",
                "Always pair each M3 container role with its own `on-` counterpart (e.g. `primary-container` -> `on-primary-container`) so WCAG contrast holds across light/dark themes.",
                cx.path, lineno, snippet,
            )

    if cx.token_file or is_data_view:
        return

    bg_hex = strip_important(bg_val).strip()
    fg_hex = strip_important(fg_val).strip()
    if OPAQUE_HEX_RE.fullmatch(bg_hex) and OPAQUE_HEX_RE.fullmatch(fg_hex):
        ratio = srgb_contrast_ratio(fg_hex, bg_hex)
        min_ratio = 3.0 if (font_size_px >= 24.0 or (is_bold and font_size_px >= 18.67)) else 4.5
        if ratio < min_ratio:
            cx.add(
                "MD3E024", "error",
                f"WCAG contrast failure: {fg_hex} on {bg_hex} is {ratio:.2f}:1 (< {min_ratio:.1f}:1 minimum).",
                "Use an official semantic container/`on-` role pair or adjust tone separation to meet WCAG AA contrast.",
                cx.path, lineno, snippet,
            )


def check_radius(cx, prop, value, lineno, line) -> None:
    if prop not in RADIUS_PROPS or is_var(value) or "inherit" in value:
        return
    if "50%" in value:
        cx.add("MD3E011", "warning",
               "`border-radius: 50%` is the pre-M3 roundedness hack. The shape "
               "scale names this value.",
               "Use var(--md-sys-shape-corner-full) or a bounded height/2 token.",
               cx.path, lineno, line)
        return
    for slash_group in value.split("/"):
        for part in slash_group.strip().split():
            px = parse_px(part)
            if px is None or px in CORNER_SCALE_PX or px in FULL_PX:
                continue
            if 0 < px <= 2:
                continue
            cx.add("MD3E003", "info",
                   f"Corner radius {px:g}px is outside the default 10-step MD3E scale (project convention).",
                   "Consider one of the ten steps (0/4/8/12/16/20/28/32/48/full) unless intentionally customized for brand shape.",
                   cx.path, lineno, line)


def check_font_size(cx, prop, value, lineno, line) -> None:
    if prop != "font-size" or is_var(value):
        return
    clean_val = strip_important(value)
    if any(fn in clean_val for fn in ("calc(", "clamp(", "min(", "max(")) or "%" in clean_val:
        return
    px = parse_px(clean_val)
    if px is not None:
        if px not in TYPE_SCALE_PX:
            cx.add("MD3E007", "info",
                   f"font-size {px:g}px is outside the default M3 11-size type scale (project convention).",
                   "Consider var(--md-sys-typescale-<role>-size) (11 / 12 / 14 / 16 / 22 / 24 / 28 / 32 / 36 / 45 / 57).",
                   cx.path, lineno, line)
        return
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*rem", clean_val)
    if m and round(float(m.group(1)), 5) not in TYPE_SCALE_REM:
        cx.add("MD3E007", "info",
               f"font-size {m.group(1)}rem is outside the default M3 type scale (project convention).",
               "Consider var(--md-sys-typescale-<role>-size).", cx.path, lineno, line)


def _is_official_bezier(expr: str) -> bool:
    compact = re.sub(r"\s+", "", expr)
    if compact in OFFICIAL_WEB_CURVES:
        return True
    m = re.fullmatch(r"cubic-bezier\(([^)]+)\)", compact)
    if not m:
        return False
    parts = m.group(1).split(",")
    if len(parts) != 4:
        return False
    try:
        nums = tuple(round(float(p), 4) for p in parts)
    except ValueError:
        return False
    return nums in OFFICIAL_WEB_CURVE_TUPLES


def check_motion(cx, prop, value, lineno, line, in_reduced_motion: bool = False) -> None:
    if prop not in MOTION_PROPS:
        return

    # MD3E019: Composite spring token inside `animation:` shorthand alongside an explicit duration
    if prop == "animation" and COMPOSITE_SPRING_VAR_RE.search(value) and TIME_RE.search(value):
        cx.add("MD3E019", "warning",
               "Composite motion token used inside `animation:` shorthand with an explicit duration.",
               "Composite --md-sys-motion-<speed>-<type> tokens include a duration, so CSS "
               "parses the second time as animation-delay. Use the easing-only token "
               "var(--md-sys-motion-<speed>-<type>-easing) instead.",
               cx.path, lineno, line)

    segments = split_top_level_commas(strip_important(value))
    for seg in segments:
        if is_var(seg) or LINEAR_SPRING_RE.search(seg):
            continue

        stripped = seg.strip()
        if in_reduced_motion and (
            stripped in ("none", "0s", "0ms")
            or re.fullmatch(
                r"(?:[a-z-]+\s+)?(?:0|\d+(?:\.\d+)?)\s*m?s\s+(?:linear|cubic-bezier\(\s*0\s*,\s*0\s*,\s*1\s*,\s*1\s*\))",
                stripped,
            )
        ):
            continue
        if stripped in ("none", "inherit", "unset"):
            continue

        # Official M3E Web cubic-bezier curves are first-class valid implementations
        beziers = [b.group(0) for b in CUBIC_BEZIER_CALL_RE.finditer(seg)]
        if beziers and all(_is_official_bezier(b) for b in beziers) and not EASING_KEYWORD_RE.search(seg):
            continue

        has_time = bool(TIME_RE.search(seg))
        has_easing = bool(EASING_KEYWORD_RE.search(seg) or CURVE_FUNC_RE.search(seg))
        if not (has_time or has_easing):
            continue
        cx.add("MD3E004", "warning",
               "Motion uses uncalibrated duration/easing instead of an M3E spring or official Web curve.",
               "Use a spring token (`var(--md-sys-motion-default-spatial)`), JS `md3e-spring.js`, or an official M3E Web cubic-bezier curve (`--md-sys-motion-*-bezier`).",
               cx.path, lineno, line)
        return


def check_shadow(cx, prop, value, lineno, line) -> None:
    if prop != "box-shadow" or value.strip() in ("none", "inherit", "unset"):
        return
    if not is_var(value) or "rgba(" in value:
        cx.add("MD3E010", "info",
               "box-shadow used to express depth.",
               "M3 expresses elevation with tonal surface colour "
               "(var(--md-sys-color-surface-container-*)). Shadows are a "
               "fallback for legibility: var(--md-sys-elevation-level1..5).",
               cx.path, lineno, line)


def check_bento_decl(cx, prop, value, lineno, line, *, in_forced_colors: bool = False) -> None:
    if getattr(cx, "mode", "strict") not in ("desktop-bento", "personal-studio") or cx.token_file or in_forced_colors:
        return
    clean_v = strip_important(value).lower()
    if prop in BORDER_PROPS:
        if re.search(r"\b1px\b", clean_v) and "transparent" not in clean_v and clean_v not in ("none", "0", "0px"):
            cx.add(
                "MD3E101", "custom",
                f"1px border (`{prop}`) deviates from opt-in Desktop Bento borderless nesting.",
                "For Bento cards/panels, express depth with 4+ `--md-sys-color-surface-container-*` luminance tiers (keep functional borders on analytical data tables/charts or inside `@media (forced-colors: active)`).",
                cx.path, lineno, line,
            )
    elif prop == "box-shadow" and clean_v not in ("none", "inherit", "unset", ""):
        cx.add(
            "MD3E101", "custom",
            "Rectangular `box-shadow` used on opt-in Desktop Bento container.",
            "For Bento panels, prefer `surface-container-*` tonal steps or wrapper `filter: drop-shadow(...)` for non-rectangular shapes.",
            cx.path, lineno, line,
        )


def check_misc(cx, prop, value, lineno, line) -> None:
    if prop == "text-transform" and "uppercase" in value:
        cx.add("MD3E012", "info",
               "Uppercase label text.",
               "M3 uses sentence case for buttons, labels and tabs. "
               "Uppercasing was an M2 convention.",
               cx.path, lineno, line)
    if prop in ("outline", "outline-width") and strip_important(value) in ("none", "0", "0px"):
        cx.add("MD3E005", "error",
               "Focus outline removed.",
               "Keyboard users lose positional feedback. Provide a :focus-visible ring "
               "(3px solid var(--md-sys-color-secondary) with 2px offset) or "
               "`outline: 2px solid transparent` inside a :focus-within container.",
               cx.path, lineno, line)
    if (prop == "transition-property" and re.search(r"\ball\b", value)) or (
        prop == "transition" and re.search(r"(?:^|,)\s*all\b", value)
    ):
        cx.add("MD3E013", "warning",
               "`transition: all` animates properties you did not intend, "
               "including layout-affecting ones.",
               "Name the property and pair it with an M3E spring or official Web curve token.",
               cx.path, lineno, line)


# ===========================================================================
# Checker engine
# ===========================================================================

def _rightmost_compound_selector(sel: str) -> str:
    paren_depth = 0
    bracket_depth = 0
    in_quote: str | None = None
    escape = False
    last_start = 0
    for idx, ch in enumerate(sel):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if in_quote:
            if ch == in_quote:
                in_quote = None
            continue
        if ch in ('"', "'"):
            in_quote = ch
        elif ch == "(" and bracket_depth == 0:
            paren_depth += 1
        elif ch == ")" and bracket_depth == 0:
            paren_depth = max(0, paren_depth - 1)
        elif ch == "[":
            bracket_depth += 1
        elif ch == "]":
            bracket_depth = max(0, bracket_depth - 1)
        elif paren_depth == 0 and bracket_depth == 0 and ch in (" ", "\t", "\n", "\r", ">", "+", "~"):
            last_start = idx + 1
    return sel[last_start:].strip()


def _selector_targets_range_slider(sel: str) -> bool:
    s = sel.strip()
    if not s or "::" in s:
        return False
    subject = _rightmost_compound_selector(s)
    if not subject or "::" in subject:
        return False
    if RANGE_INPUT_ATTR_RE.search(subject):
        return True
    cleaned = re.sub(r"\[[^\]]*\]", " ", subject)
    cleaned = re.sub(r":(?!is\(|where\(|has\()[a-zA-Z_-]+(?:\([^)]*\))?", " ", cleaned)
    for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_-]*", cleaned):
        if re.search(r"(?:^|[^a-zA-Z0-9])(?:range|slider)(?![a-zA-Z0-9])", tok, re.I):
            if not SLIDER_NON_CONTROL_WRAPPER_RE.search(tok):
                return True
    return False


def _selector_is_fixed_menu_wrapper(sel: str) -> bool:
    s = sel.strip()
    if not s or "::" in s:
        return False
    subject = _rightmost_compound_selector(s)
    if not subject or "::" in subject:
        return False
    return bool(FIXED_MENU_WRAPPER_RE.search(subject))


FLOATING_LABEL_CLASS_RE = re.compile(
    r"(?:^|[.\s>+~\[])(?:[a-z0-9_-]*(?:text-field|md3e-field|outlined-field|floating)[a-z0-9_-]*(?:__|-)label|"
    r"floating-label|outlined-label|md3e-field__label|md3e-text-field__label)\b",
    re.IGNORECASE,
)
ROOT_SUBJECT_RE = re.compile(r"^(?:html|body|:root)(?=$|[.\[:#])", re.IGNORECASE)
DIALOG_LOCK_TRIGGER_RE = re.compile(
    r"(?:dialog|modal|scroll[-_]?lock|no[-_]?scroll|noscroll|is-locked|lock[-_]?scroll|has-dialog)",
    re.IGNORECASE,
)
HDR_BROAD_SUBJECT_RE = re.compile(r"^(?:body|p|\*)(?=$|[.\[:#])", re.IGNORECASE)
WIDGET_STATE_SELECTOR_RE = re.compile(
    r":focus-visible|\[[^\]]*(?:data-highlighted|data-selected|aria-selected|aria-checked|"
    r"data-range-start|data-in-range|data-range-end|data-today|data-active|data-focus-visible)[^\]]*\]",
    re.IGNORECASE,
)
WIDGET_ROLE_HINTS = {
    "listbox": re.compile(r"listbox|option|select|combobox|cmd-item|data-highlighted|data-selected|aria-selected", re.IGNORECASE),
    "menu": re.compile(r"menu|menuitem|menuitemcheckbox|popover|data-highlighted|aria-checked|data-selected", re.IGNORECASE),
    "grid": re.compile(r"grid|gridcell|datepicker|date-picker|calendar|day|data-selected|aria-selected|data-range-start|data-in-range|data-range-end", re.IGNORECASE),
}


def _selector_targets_floating_label(sel: str) -> bool:
    s = sel.strip()
    if not s or "::" in s:
        return False
    subject = _rightmost_compound_selector(s)
    if not subject or "::" in subject:
        return False
    if FLOATING_LABEL_CLASS_RE.search(subject):
        return True
    if re.match(r"^label(?=$|[.\[:#])", subject, re.I) and re.search(
        r"text-field|md3e-field|outlined|floating", s, re.I
    ):
        return True
    return False


def _rule_has_opaque_background(rule: RuleBlock) -> tuple[int, str] | None:
    if any(p in ("mask-image", "-webkit-mask-image") for p, _, _, _ in rule.declarations):
        return None
    if any(p == "background-clip" and strip_important(v).lower() == "text" for p, v, _, _ in rule.declarations):
        return None
    for prop, value, lineno, raw in rule.declarations:
        if prop in ("background", "background-color"):
            clean_v = strip_important(value).lower()
            if clean_v and clean_v not in ("transparent", "none", "inherit", "initial", "unset"):
                return (lineno, raw)
    return None


def _rule_is_root_dialog_scroll_lock(rule: RuleBlock, *, doc_has_dialog: bool = False) -> tuple[int, str] | None:
    branches = split_top_level_commas(rule.selector)
    root_branches = [b for b in branches if ROOT_SUBJECT_RE.match(_rightmost_compound_selector(b))]
    if not root_branches:
        return None
    overflow_decl = next(
        (
            (lineno, raw)
            for prop, value, lineno, raw in rule.declarations
            if prop in ("overflow", "overflow-y", "overflow-block")
            and strip_important(value).lower().split()[0:1] in (["hidden"], ["clip"])
        ),
        None,
    )
    if overflow_decl is None:
        return None
    for b in root_branches:
        if DIALOG_LOCK_TRIGGER_RE.search(b):
            return overflow_decl
        if doc_has_dialog and re.search(r":has\s*\(|\.(?:is-open|open|active|locked)\b|\[(?:data-open|open|aria-modal)", b, re.I):
            return overflow_decl
    return None


class Checker:
    def __init__(self, path: pathlib.Path, *, is_snippet: bool = False, mode: str = "strict") -> None:
        self.path_obj = path
        self.path = str(path)
        self.ext = path.suffix.lower()
        self.token_file = is_token_file(path)
        self.is_snippet = is_snippet
        self.mode = "strict" if mode == "default" else mode
        self.findings: list[Finding] = []

    def add(self, code, severity, message, fix, path, line, snippet="") -> None:
        self.findings.append(
            Finding(code, severity, message, fix, path, line, snippet.strip()[:140])
        )

    def run(self, text: str) -> list[Finding]:
        if self.ext in CSS_EXTENSIONS:
            self.audit_css(text, base_line=1, check_file_rules=not self.is_snippet)
        elif self.ext in HTML_EXTENSIONS or self.ext in (".vue", ".svelte", ".astro"):
            self.audit_markup_document(text)
        else:
            # JS / TS / JSX / TSX / PHP fallback
            self.audit_generic_code(text)
        return self.findings

    def _collect_hit_area_selectors(self, rules: list[RuleBlock]) -> set[str]:
        covered: set[str] = set()
        for rule in rules:
            for sel in rule.selector.split(","):
                s = sel.strip()
                if not ("::before" in s or "::after" in s):
                    continue
                decl_map = {p: v for p, v, _, _ in rule.declarations}
                has_48_dim = any(
                    (
                        "var(--md-sys-touch-target-min)" in decl_map.get(p, "")
                        or (parse_px(decl_map.get(p, "")) or 0) >= MIN_TOUCH_TARGET
                    )
                    for p in ("height", "min-height", "block-size", "min-block-size")
                )
                has_48_width = any(
                    (
                        "var(--md-sys-touch-target-min)" in decl_map.get(p, "")
                        or (parse_px(decl_map.get(p, "")) or 0) >= MIN_TOUCH_TARGET
                    )
                    for p in ("width", "min-width", "inline-size", "min-inline-size")
                )
                has_inset_expand = any(
                    p in ("inset", "inset-block") and ("-" in decl_map[p] or "var(--md-sys-touch-target-min)" in decl_map[p])
                    for p in decl_map
                )
                has_axis_inset_pair = (
                    "inset-block" in decl_map and "-" in decl_map["inset-block"]
                    and "inset-inline" in decl_map and "-" in decl_map["inset-inline"]
                )
                if (
                    (has_48_dim and has_48_width)
                    or (has_48_dim and has_inset_expand)
                    or ("inset" in decl_map and "-" in decl_map.get("inset", ""))
                    or has_axis_inset_pair
                ):
                    covered.add(normalize_selector_base(s))
        return covered

    def _check_rule_slider_and_menu_traps(
        self,
        rule: RuleBlock,
        appearance_none_selectors: set[str],
        pointer_events_none_selectors: set[str],
    ) -> None:
        sel_branches = split_top_level_commas(rule.selector)

        # MD3E027 (a): Slider setting accent-color without appearance: none / -webkit-appearance: none
        slider_branches = [s for s in sel_branches if _selector_targets_range_slider(s)]
        if slider_branches:
            accent_decl = next(
                (
                    (lineno, raw)
                    for prop, value, lineno, raw in rule.declarations
                    if prop == "accent-color"
                    and strip_important(value).lower() not in ("auto", "inherit", "initial", "unset", "")
                ),
                None,
            )
            if accent_decl is not None:
                has_appearance_none = any(
                    prop in ("appearance", "-webkit-appearance") and strip_important(value).lower() == "none"
                    for prop, value, _, _ in rule.declarations
                ) or all(s.strip() in appearance_none_selectors for s in slider_branches)
                if not has_appearance_none:
                    self.add(
                        "MD3E027",
                        "warning",
                        "Range slider sets `accent-color` without `appearance: none` (renders OS-native border/thumb instead of M3E track & 4x44dp handle).",
                        "Add `-webkit-appearance: none; appearance: none;` (with `background: transparent; border: none; outline: 2px solid transparent;`) and style `::-webkit-slider-runnable-track` / `::-webkit-slider-thumb` and `::-moz-range-*`.",
                        self.path,
                        accent_decl[0],
                        accent_decl[1],
                    )

        # MD3E027 (b): position: fixed floating/FAB menu wrapper missing pointer-events: none
        wrapper_branches = [s for s in sel_branches if _selector_is_fixed_menu_wrapper(s)]
        if wrapper_branches:
            fixed_decl = next(
                (
                    (lineno, raw)
                    for prop, value, lineno, raw in rule.declarations
                    if prop == "position" and strip_important(value).lower() == "fixed"
                ),
                None,
            )
            if fixed_decl is not None:
                has_pointer_none = any(
                    prop == "pointer-events" and strip_important(value).lower() == "none"
                    for prop, value, _, _ in rule.declarations
                ) or all(s.strip() in pointer_events_none_selectors for s in wrapper_branches)
                if not has_pointer_none:
                    self.add(
                        "MD3E027",
                        "warning",
                        f"Fixed floating/FAB menu container `{rule.selector}` omits `pointer-events: none`, creating an invisible pointer hit-trap over nearby inputs/sliders.",
                        "Set `pointer-events: none;` on the fixed menu wrapper and re-enable `pointer-events: auto;` on the trigger button and open menu items.",
                        self.path,
                        fixed_decl[0],
                        fixed_decl[1],
                    )

    def _audit_rule_block(
        self,
        rule: RuleBlock,
        hit_covered: set[str],
        morphing_bases: set[str],
        appearance_none_selectors: set[str] | None = None,
        pointer_events_none_selectors: set[str] | None = None,
        *,
        doc_has_dialog: bool = False,
    ) -> bool:
        has_motion = False
        is_data_view_rule = any(DATA_VIEW_SELECTOR_RE.search(s) for s in rule.selector.split(","))
        is_shape_rule = bool(SHAPE_SELECTOR_RE.search(rule.selector)) or any(
            (p in ("mask-image", "-webkit-mask-image") and strip_important(v).lower() != "none")
            or (p == "clip-path" and bool(re.search(r"\b(?:polygon|path|url)\s*\(", v, re.I)))
            for p, v, _, _ in rule.declarations
        )
        # Check custom --md-sys-color-* pairs defined in this selector block (MD3E024)
        for bg_role, fg_role in CANONICAL_COLOR_PAIRS:
            bg_entry = rule.custom_color_vars.get(f"--md-sys-color-{bg_role}")
            fg_entry = rule.custom_color_vars.get(f"--md-sys-color-{fg_role}")
            if bg_entry and fg_entry:
                ratio = srgb_contrast_ratio(fg_entry[0], bg_entry[0])
                if ratio < 4.5:
                    self.add(
                        "MD3E024", "error",
                        f"Contrast failure in `{rule.selector}`: `--md-sys-color-{fg_role}` ({fg_entry[0]}) on `--md-sys-color-{bg_role}` ({bg_entry[0]}) is {ratio:.2f}:1 (< 4.5:1 WCAG AA).",
                        "Adjust token tones so every container/`on-` pair reaches >= 4.5:1 (>= 7.0:1 for high contrast).",
                        self.path, fg_entry[1], fg_entry[2],
                    )

        check_role_pairing_and_contrast(self, rule.declarations, is_data_view=is_data_view_rule)

        for prop, value, lineno, raw in rule.declarations:
            if not is_data_view_rule:
                check_hex(self, value, lineno, raw)
                check_func_color(self, value, lineno, raw)
                check_radius(self, prop, value, lineno, raw)
                check_font_size(self, prop, value, lineno, raw)
            check_color_mix(self, value, lineno, raw)
            check_motion(self, prop, value, lineno, raw, in_reduced_motion=rule.in_reduced_motion)
            if is_shape_rule and prop == "box-shadow" and strip_important(value).lower() not in ("none", "inherit", "unset", ""):
                self.add(
                    "MD3E023",
                    "warning",
                    "Rectangular `box-shadow` applied directly on a non-rectangular masked/morphing shape.",
                    "Remove `box-shadow` and apply `filter: drop-shadow(...)` on a parent wrapper (e.g. `.md3e-shape-shadow-wrap`).",
                    self.path, lineno, raw,
                )
            elif not is_data_view_rule:
                check_shadow(self, prop, value, lineno, raw)
                check_bento_decl(self, prop, value, lineno, raw, in_forced_colors=rule.in_forced_colors)
            check_misc(self, prop, value, lineno, raw)

            if prop in MOTION_PROPS and not rule.in_reduced_motion and strip_important(value).lower() not in ("none", "0s", "0ms", "inherit", "unset"):
                if (
                    TIME_RE.search(value)
                    or "var(--md-sys-motion-" in value
                    or "var(--md-bento-motion-" in value
                    or "var(--md-comp-loading-indicator-" in value
                    or LINEAR_SPRING_RE.search(value)
                    or CUBIC_BEZIER_CALL_RE.search(value)
                ):
                    has_motion = True

        # Check 9999px radius on a rule whose base selector transitions border-radius
        if not self.token_file and not is_data_view_rule:
            rule_bases = {re.split(r"[:\[]", s.strip())[0].strip() for s in rule.selector.split(",")}
            if any(rb == mb or rb.startswith(mb + ".") for rb in rule_bases for mb in morphing_bases):
                for prop, value, lineno, raw in rule.declarations:
                    if prop in RADIUS_PROPS and FULL_RADIUS_VALUE_RE.search(value):
                        self.add(
                            "MD3E019",
                            "warning",
                            "`border-radius: var(--md-sys-shape-corner-full)` (9999px) snaps or flashes a `0px` "
                            "sharp rectangle under spring overshoot (`> 1.0`) when animated.",
                            "Use a bounded `height / 2` radius (e.g. `20px` `--md-sys-shape-corner-large-increased` on "
                            "40px controls, `24px`, or `calc(var(--md-bento-control-height, 48px) / 2)`) so underdamped "
                            "springs never drive `border-radius` negative and clamp to `0px`.",
                            self.path, lineno, raw,
                        )

        # Touch target & visual height inflation checks (MD3E006)
        if not self.token_file and not is_data_view_rule:
            self._check_rule_touch_target(rule, hit_covered)

        # Native slider border & fixed FAB/floating menu pointer hit-trap checks (MD3E027)
        if not is_data_view_rule:
            self._check_rule_slider_and_menu_traps(
                rule,
                appearance_none_selectors or set(),
                pointer_events_none_selectors or set(),
            )

        # Outlined floating label opaque background bleed check (MD3E029)
        if not self.token_file and not is_data_view_rule and not rule.in_forced_colors:
            branches = split_top_level_commas(rule.selector)
            if any(_selector_targets_floating_label(b) for b in branches):
                opaque_bg = _rule_has_opaque_background(rule)
                if opaque_bg is not None:
                    self.add(
                        "MD3E029",
                        "warning",
                        "Floating text-field `<label>` applies an opaque `background` patch that bleeds on frosted/gradient/nested surfaces.",
                        "Use a `<fieldset><legend>` transparent border cutout (or `mask-image`) instead of an opaque label background.",
                        self.path,
                        opaque_bg[0],
                        opaque_bg[1],
                    )

        # Root html/body dialog scroll-locking check (MD3E029 / MD3E202)
        if not self.token_file and not is_data_view_rule:
            scroll_lock = _rule_is_root_dialog_scroll_lock(rule, doc_has_dialog=doc_has_dialog)
            if scroll_lock is not None:
                is_studio = self.mode == "personal-studio"
                self.add(
                    "MD3E202" if is_studio else "MD3E029",
                    "custom" if is_studio else "warning",
                    "Root `html`/`body` scroll-lock (`overflow: hidden`) causes layout shift and breaks sticky containers with `<dialog>`.",
                    "Remove root `html`/`body` `overflow: hidden`; use `dialog:modal { overscroll-behavior: contain; }` and `dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }`.",
                    self.path,
                    scroll_lock[0],
                    scroll_lock[1],
                )

        return has_motion

    def _check_rule_touch_target(self, rule: RuleBlock, hit_covered: set[str]) -> None:
        selectors = [s.strip() for s in rule.selector.split(",")]
        interactive = [
            s for s in selectors
            if INTERACTIVE_SELECTOR_RE.search(s)
            and "::" not in s
            and not DECORATIVE_SUBELEMENT_RE.search(s)
        ]
        if not interactive:
            return
        if all(DENSE_ROW_SELECTOR_RE.search(s) or DATA_VIEW_SELECTOR_RE.search(s) for s in interactive):
            return

        decl_map: dict[str, tuple[str, int, str]] = {}
        for prop, value, lineno, raw in rule.declarations:
            decl_map[prop] = (value, lineno, raw)

        # Detect visual height inflation: height: 32px/40px combined with min-height: 48px on same box
        h_val = decl_map.get("height") or decl_map.get("block-size")
        min_h_val = decl_map.get("min-height") or decl_map.get("min-block-size")
        if h_val and min_h_val:
            h_px = parse_px(h_val[0])
            mh_px = parse_px(min_h_val[0])
            mh_is_48 = (mh_px is not None and mh_px >= M3_RECOMMENDED_TARGET) or "var(--md-sys-touch-target-min)" in min_h_val[0]
            if h_px is not None and h_px < M3_RECOMMENDED_TARGET and mh_is_48:
                self.add(
                    "MD3E006", "warning",
                    f"`min-height: 48px` on a {h_px:g}px button inflates its visual container height.",
                    "Keep `height: 32px` / `40px` on the visual button and expand only the "
                    "invisible hit area to 48px using a `::before` pseudo-element.",
                    self.path, min_h_val[1], min_h_val[2],
                )
                return

        # Skip rules covered by a ::before/::after 48px hit area
        if all(normalize_selector_base(re.split(r"(?<!:):(?!:)", s)[0]) in hit_covered or s in hit_covered for s in interactive):
            return

        for axis_props in (("height", "min-height", "block-size", "min-block-size"),
                           ("width", "min-width", "inline-size", "min-inline-size")):
            small_hit = None
            has_48_guard = False
            for p in axis_props:
                if p not in decl_map:
                    continue
                val, ln, raw = decl_map[p]
                if "var(--md-sys-touch-target-min)" in val:
                    has_48_guard = True
                    continue
                px = parse_px(val)
                if px is not None:
                    if px >= M3_RECOMMENDED_TARGET:
                        has_48_guard = True
                    elif small_hit is None:
                        small_hit = (px, ln, raw)
            if small_hit and not has_48_guard:
                px, ln, raw = small_hit
                if px < WCAG_MIN_TARGET:
                    self.add(
                        "MD3E006", "error",
                        f"Interactive target is {px:g}px on one axis, below the WCAG 2.2 AA {WCAG_MIN_TARGET:g}x{WCAG_MIN_TARGET:g}px floor.",
                        "Expand the clickable hit area to >= 24px minimum (recommended 48x48px via `::before`).",
                        self.path, ln, raw,
                    )
                else:
                    self.add(
                        "MD3E006", "warning",
                        f"Interactive target is {px:g}px on one axis (satisfies WCAG {WCAG_MIN_TARGET:g}px AA floor, below M3 recommended {M3_RECOMMENDED_TARGET:g}px touch target).",
                        "Keep visual height 32px/40px and expand the pointer hit area to 48px via an invisible `::before` pseudo-element.",
                        self.path, ln, raw,
                    )

    def _check_ms_font_axes(self, text: str, base_line: int = 1) -> None:
        lines = text.splitlines()
        for m in MS_FONT_AXES_RE.finditer(text):
            raw_axes = [a.strip() for a in m.group(1).split(",") if a.strip()]
            expected_axes = sorted(
                (CANONICAL_MS_AXES.get(a.lower(), a) for a in raw_axes),
                key=str.lower,
            )
            if raw_axes != expected_axes:
                rel_ln = text[:m.start()].count("\n")
                ln = base_line + rel_ln
                snippet = lines[rel_ln] if rel_ln < len(lines) else ""
                expected_str = ",".join(expected_axes)
                self.add(
                    "MD3E017", "error",
                    f"Google Fonts Material Symbols axes `{m.group(1)}` are not in alphabetical order (HTTP 400).",
                    f"Reorder axes to `{expected_str}` (Google Fonts CSS2 requires alphabetical order: `FILL,GRAD,opsz,wght`) and match the `@` value tuples in the same order.",
                    self.path, ln, snippet,
                )

    def _check_css_brace_balance(self, css_text: str, base_line: int = 1) -> None:
        cleaned = strip_css_comments(css_text)
        css_lines = css_text.splitlines()
        stack: list[tuple[int, str]] = []
        header_buf: list[str] = []
        in_string: str | None = None
        escape = False
        lineno = base_line

        for ch in cleaned:
            if escape:
                escape = False
                if ch == "\n":
                    lineno += 1
                continue
            if ch == "\\" and in_string:
                escape = True
                continue
            if in_string:
                if ch == in_string:
                    in_string = None
                if ch == "\n":
                    lineno += 1
                continue
            if ch in ('"', "'"):
                in_string = ch
                continue
            if ch == "{":
                header = re.sub(r"\s+", " ", "".join(header_buf)).strip()[:80] or "{"
                stack.append((lineno, header))
                header_buf.clear()
            elif ch == "}":
                header_buf.clear()
                if stack:
                    stack.pop()
                else:
                    idx = lineno - base_line
                    snip = css_lines[idx] if 0 <= idx < len(css_lines) else "}"
                    self.add(
                        "MD3E028",
                        "error",
                        "Unexpected closing CSS brace `}` (unbalanced block or duplicate closing brace).",
                        "Remove the stray `}` or add the matching opening `{` (check `@keyframes` and `@media` blocks).",
                        self.path,
                        lineno,
                        snip,
                    )
            elif ch == ";":
                header_buf.clear()
            else:
                if ch == "\n":
                    lineno += 1
                    header_buf.append(" ")
                elif len(header_buf) < 160:
                    header_buf.append(ch)

        for open_ln, header in stack:
            idx = open_ln - base_line
            snip = css_lines[idx] if 0 <= idx < len(css_lines) else header
            self.add(
                "MD3E028",
                "error",
                f"Unclosed CSS block `{header}` (missing closing `}}`).",
                "Add the matching closing `}` to balance every `@keyframes`, `@media`, and selector block.",
                self.path,
                open_ln,
                snip,
            )

    def _audit_personal_studio_css(
        self,
        cleaned_css: str,
        rules: list[RuleBlock],
        *,
        has_reduced_transparency: bool = False,
        linked_studio_css: bool = False,
        check_hdr_file_rules: bool = True,
    ) -> None:
        if self.mode != "personal-studio":
            return

        has_rt_support = has_reduced_transparency or bool(
            re.search(r"data-reduced-transparency", cleaned_css, re.I)
        )

        # Ban global .studio-caustic-field ambient light-bleed overlays even in snippets/linked docs
        for r in rules:
            if re.search(r"\.studio-caustic-field\b", r.selector, re.I):
                self.add(
                    "MD3E201",
                    "custom",
                    "Global `.studio-caustic-field` ambient light-bleed overlay pollutes dark canvas purity.",
                    "Delete `.studio-caustic-field`; keep dark `--md-sys-color-surface` pure and rely on real UI cards and card-local specular/spotlight highlights.",
                    self.path,
                    r.start_line,
                    r.selector,
                )

        # Adaptive HDR optical hygiene: forbid broad HDR / constrained-high on body or p
        for r in rules:
            branches = split_top_level_commas(r.selector)
            broad_branches = [b for b in branches if HDR_BROAD_SUBJECT_RE.match(_rightmost_compound_selector(b))]
            if not broad_branches:
                continue
            for prop, val, lineno, raw in r.declarations:
                clean_v = strip_important(val).lower()
                if prop == "dynamic-range-limit" and clean_v in ("constrained-high", "high", "no-limit"):
                    self.add(
                        "MD3E201",
                        "custom",
                        f"HDR `dynamic-range-limit: {clean_v}` must not be applied broadly to `{', '.join(broad_branches)}`.",
                        "Keep `body` and `p` prose at `dynamic-range-limit: standard`; restrict `constrained-high` to self-luminous micro-details (spotlight, specular rim, active indicators, scrubber focus).",
                        self.path,
                        lineno,
                        raw,
                    )
                elif re.search(r"color\(\s*display-p3\b|--md-studio-hdr-boost", val, re.I):
                    self.add(
                        "MD3E201",
                        "custom",
                        f"HDR / Display-P3 boost must not be applied broadly to `{', '.join(broad_branches)}`.",
                        "Restrict `color(display-p3 ...)` and `--md-studio-hdr-boost` to self-luminous micro-details (spotlight, specular rim, active indicators, scrubber focus); keep body/prose in SDR.",
                        self.path,
                        lineno,
                        raw,
                    )

        if self.is_snippet or linked_studio_css:
            return

        has_hdr_css = bool(
            re.search(
                r"dynamic-range\s*:\s*high\b|dynamic-range-limit\s*:\s*constrained-high\b|color\(\s*display-p3\b",
                cleaned_css,
                re.I,
            )
        )
        if has_hdr_css and check_hdr_file_rules:
            has_sdr_fallback = bool(
                re.search(r"dynamic-range-limit\s*:\s*standard\b|data-studio-hdr\s*=\s*[\"']off[\"']", cleaned_css, re.I)
            )
            has_contrast_fallback = bool(
                re.search(r"prefers-contrast\s*:\s*more\b|data-contrast\s*=\s*[\"']high[\"']|forced-colors\s*:\s*active\b", cleaned_css, re.I)
            )
            if not has_sdr_fallback:
                self.add(
                    "MD3E201",
                    "custom",
                    "Personal Studio HDR optical CSS lacks an SDR / `[data-studio-hdr=\"off\"]` fallback.",
                    "Add `dynamic-range-limit: standard` and `[data-studio-hdr=\"off\"]` SDR collapse rules.",
                    self.path,
                    1,
                    "",
                )
            if not has_rt_support:
                self.add(
                    "MD3E201",
                    "custom",
                    "Personal Studio HDR optical CSS lacks a `prefers-reduced-transparency: reduce` fallback.",
                    "Collapse HDR specular/glass boosts to `dynamic-range-limit: standard` inside `@media (prefers-reduced-transparency: reduce)` / `[data-reduced-transparency=\"true\"]`.",
                    self.path,
                    1,
                    "",
                )
            if not has_contrast_fallback:
                self.add(
                    "MD3E201",
                    "custom",
                    "Personal Studio HDR optical CSS lacks a `prefers-contrast: more` / `forced-colors` fallback.",
                    "Collapse HDR boosts inside `@media (prefers-contrast: more)`, `[data-contrast=\"high\"]`, and `@media (forced-colors: active)`.",
                    self.path,
                    1,
                    "",
                )

        if re.search(r"--md-studio-(?:blur-px|glass-alpha|glass-saturate)\s*:", cleaned_css) and not has_rt_support:
            self.add(
                "MD3E201",
                "custom",
                "Personal Studio optical glass variables declared without a reduced-transparency fallback.",
                "Pair `--md-studio-*` glass properties with `@media (prefers-reduced-transparency: reduce)` / `[data-reduced-transparency=\"true\"]` solid surface fallbacks.",
                self.path,
                1,
                "",
            )

        dialog_rules = [
            r for r in rules
            if re.search(
                r"(?:^|[\s,>+~])dialog\b[^,{]*(?::modal|::backdrop)|\.studio-cmd-dialog\b",
                r.selector,
                re.I,
            )
        ]
        if dialog_rules:
            has_overscroll_contain = any(
                prop in ("overscroll-behavior", "overscroll-behavior-y", "overscroll-behavior-block")
                and strip_important(val).lower() in ("contain", "none")
                for r in dialog_rules
                for prop, val, _, _ in r.declarations
            )
            if not has_overscroll_contain:
                self.add(
                    "MD3E202",
                    "custom",
                    "Personal Studio `<dialog>` modal/backdrop styling lacks `overscroll-behavior: contain`.",
                    "Set `overscroll-behavior: contain;` on `dialog:modal` and `dialog::backdrop` so scrolling never leaks behind the modal.",
                    self.path,
                    dialog_rules[0].start_line,
                    dialog_rules[0].selector,
                )

    def audit_css(
        self,
        css_text: str,
        base_line: int = 1,
        *,
        check_file_rules: bool = True,
        linked_motion_css: bool = False,
        has_reduced_transparency_doc: bool = False,
        linked_studio_css: bool = False,
        doc_has_dialog: bool = False,
    ) -> None:
        self._check_css_brace_balance(css_text, base_line=base_line)
        cleaned_css = strip_css_comments(css_text)
        if self.ext in CSS_EXTENSIONS and not self.token_file:
            css_lines = css_text.splitlines()
            for m in LEGACY_MWC_REF_RE.finditer(cleaned_css):
                rel_ln = cleaned_css[:m.start()].count("\n")
                ln = base_line + rel_ln
                snip = css_lines[rel_ln] if rel_ln < len(css_lines) else m.group(0)
                self.add(
                    "MD3E020", "error",
                    f"Legacy `@material/web` dependency `{m.group(0)}` is no longer supported.",
                    "Remove `@import` references to `md3e-material-web.css` / `@material/web` and style native elements with MD3E CSS tokens.",
                    self.path, ln, snip,
                )
        self._check_ms_font_axes(cleaned_css, base_line=base_line)
        rules = parse_css_rules(css_text, base_line=base_line)
        hit_covered = self._collect_hit_area_selectors(rules)

        # Collect selectors that transition border-radius, or declare appearance:none / pointer-events:none
        morphing_bases: set[str] = set()
        appearance_none_selectors: set[str] = set()
        pointer_events_none_selectors: set[str] = set()
        for rule in rules:
            rule_sels = split_top_level_commas(rule.selector)
            for prop, value, _, _ in rule.declarations:
                if prop in ("transition", "transition-property") and any(
                    k in value for k in ("border-radius", "border-start", "border-end", "border-top", "border-bottom")
                ):
                    for s in rule_sels:
                        morphing_bases.add(re.split(r"[:\[]", s.strip())[0].strip())
                elif prop in ("appearance", "-webkit-appearance") and strip_important(value).lower() == "none":
                    for s in rule_sels:
                        if "::" not in s:
                            appearance_none_selectors.add(s.strip())
                elif prop == "pointer-events" and strip_important(value).lower() == "none":
                    for s in rule_sels:
                        if "::" not in s:
                            pointer_events_none_selectors.add(s.strip())

        has_motion = False
        has_keyframes = bool(re.search(r"@keyframes\b", cleaned_css))
        has_reduced_transparency = has_reduced_transparency_doc or bool(
            re.search(r"prefers-reduced-transparency\s*:\s*reduce\b", cleaned_css, re.I)
        )
        blur_hit: tuple[int, str] | None = None
        for rule in rules:
            if self._audit_rule_block(
                rule,
                hit_covered,
                morphing_bases,
                appearance_none_selectors,
                pointer_events_none_selectors,
                doc_has_dialog=doc_has_dialog,
            ):
                has_motion = True
            if blur_hit is None:
                for prop, value, lineno, raw in rule.declarations:
                    if prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in value:
                        blur_hit = (lineno, raw)
                        break

        if blur_hit and not has_reduced_transparency:
            self.add(
                "MD3E022", "error",
                "`backdrop-filter: blur(...)` used without a `@media (prefers-reduced-transparency: reduce)` fallback.",
                "Prefer opaque tonal `surface-container-*` elevation first, or use `md3e-blur.css` / pair blur with `color-mix(in oklab, ...)` and `@media (prefers-reduced-transparency: reduce)`.",
                self.path, blur_hit[0], blur_hit[1],
            )

        if check_file_rules:
            self._audit_rt_specificity(rules)
            self._audit_keyframe_fill_cascade(rules, cleaned_css)
            self._audit_allow_discrete_layout_drops(rules)

        self._audit_personal_studio_css(
            cleaned_css,
            rules,
            has_reduced_transparency=has_reduced_transparency,
            linked_studio_css=linked_studio_css,
            check_hdr_file_rules=check_file_rules,
        )

        if not check_file_rules:
            return

        has_hover = ":hover" in cleaned_css
        has_focus_visible = ":focus-visible" in cleaned_css
        has_reduced = "prefers-reduced-motion" in cleaned_css
        has_dark = ("prefers-color-scheme" in cleaned_css or "data-theme" in cleaned_css)

        if has_hover and not has_focus_visible:
            self.add(
                "MD3E005", "error",
                "Stylesheet styles :hover states but defines no :focus-visible.",
                "Add `:focus-visible { outline: 3px solid var(--md-sys-color-secondary); outline-offset: 2px; }`.",
                self.path, 0, "",
            )

        if (has_keyframes or (has_motion and not linked_motion_css)) and not has_reduced and not self.token_file:
            self.add(
                "MD3E008", "warning",
                "Motion defined without a prefers-reduced-motion path.",
                "Include `@media (prefers-reduced-motion: reduce)` (or link `md3e-motion.css` "
                "for token-only transitions and guard custom `@keyframes`).",
                self.path, 0, "",
            )

        role_defs = len(re.findall(r"--md-sys-color-[a-z-]+\s*:", cleaned_css))
        if role_defs >= 5 and not has_dark and not self.token_file:
            self.add(
                "MD3E009", "warning",
                f"{role_defs} colour roles defined without a dark scheme.",
                'Redefine the roles under `[data-theme="dark"]` and `@media (prefers-color-scheme: dark)`.',
                self.path, 0, "",
            )

    def _audit_desktop_bento_document(self, text: str, combined_css: str, markup_only: str) -> None:
        if self.mode not in ("desktop-bento", "personal-studio") or self.is_snippet or self.token_file:
            return
        is_full_doc = bool(re.search(r"<!doctype\s+html|<html\b", text, re.I))
        if not is_full_doc:
            return

        markup_clean = strip_html_comments(markup_only)
        has_doc_exempt = bool(re.search(r"<(?:html|body|main)\b[^>]*\bdata-md3e-exempt\b", markup_clean, re.I))
        has_hero_card = bool(re.search(r"bento-card--hero|data-bento-hero\b", text, re.I))
        has_analytical_view = bool(
            re.search(r"<(?:canvas|table)\b|\brole\s*=\s*[\"'](?:grid|treegrid)[\"']|\bdata-md3e-exempt\b", markup_clean, re.I)
            or re.search(r"<svg\b[^>]*(?:chart|plot|graph|axis|trajectory|replay|telemetry)", markup_clean, re.I)
        )
        if has_doc_exempt or (has_analytical_view and not has_hero_card):
            return

        surface_tiers = set(
            re.findall(
                r"--md-sys-color-surface-container(?:-(?:lowest|low|high|highest))?\b",
                combined_css,
            )
        )
        if len(surface_tiers) < 4:
            self.add(
                "MD3E102", "custom",
                f"Opt-in Desktop Bento preset uses only {len(surface_tiers)} `surface-container-*` tier(s) (4+ recommended for Bento dashboards).",
                "Layer 4+ luminance tokens (`surface-container-lowest`, `-low`, `surface-container`, `-high`, `-highest`), or exempt analytical views with `data-md3e-exempt=\"data-view\"`.",
                self.path, 1, "",
            )

        has_outer = bool(re.search(r"--md-sys-shape-corner-extra-large\b|\b28px\b", combined_css))
        has_inner = bool(re.search(r"--md-sys-shape-corner-large\b|\b16px\b", combined_css))
        if not (has_outer and has_inner):
            self.add(
                "MD3E103", "custom",
                "Opt-in Desktop Bento dashboard is missing concentric outer (`corner-extra-large` 28px) / inner (`corner-large` 16px) corner radii.",
                "Use `--md-sys-shape-corner-extra-large` (28px) on Bento cards and step inner wells down to `--md-sys-shape-corner-large` (16px).",
                self.path, 1, "",
            )

        has_morph_and_drop = (
            bool(re.search(r"md3e-morph\.js|\.md3e-shape-", text))
            and "drop-shadow(" in combined_css
        )
        has_wave_and_spark = (
            bool(re.search(r"wave", text, re.I))
            and bool(re.search(r"sparkline|spark-line|spark-stroke", text, re.I))
        )
        has_kpi_scale = bool(re.search(r"--md-sys-typescale-display-(?:large|medium)-size", combined_css))
        if not (has_morph_and_drop and has_wave_and_spark and has_kpi_scale):
            self.add(
                "MD3E104", "custom",
                "Opt-in Desktop Bento Hero preset is missing signature Hero anchors (morphing shape CTA with `drop-shadow()`, wave + sparkline SVG, or `>=3x` Display KPI).",
                "Include a Hero Bento card with decorative wave backdrop, sparkline SVG, `md3e-morph.js` CTA, and Display KPI — or mark analytical data views with `data-md3e-exempt=\"data-view\"`.",
                self.path, 1, "",
            )

    def _audit_personal_studio_document(
        self,
        text: str,
        combined_css: str,
        markup_clean: str,
        lines: list[str],
        exempt_lines: set[int],
        *,
        linked_studio_css: bool = False,
        linked_blur_css: bool = False,
    ) -> None:
        if self.mode != "personal-studio":
            return

        # 1. Ban .studio-caustic-field HTML elements & check focusable controls inside <dialog> (snippets + full docs)
        for m in re.finditer(rf"<([a-z][a-z0-9:-]*)\b({TAG_ATTRS_PAT})>", markup_clean, re.I):
            attrs = m.group(2)
            if re.search(r"\bstudio-caustic-field\b", attrs):
                ln = markup_clean[:m.start()].count("\n") + 1
                if ln not in exempt_lines:
                    self.add(
                        "MD3E201",
                        "custom",
                        "Global `.studio-caustic-field` ambient light-bleed element pollutes dark `--md-sys-color-surface` purity.",
                        "Delete `<div class=\"studio-caustic-field\">` and rely on real UI cards, dividers, and card-local specular/spotlight highlights.",
                        self.path,
                        ln,
                        lines[ln - 1] if ln - 1 < len(lines) else "",
                    )

        dialog_blocks = list(re.finditer(rf"<dialog\b({TAG_ATTRS_PAT})>([\s\S]*?)</dialog>", markup_clean, re.I))
        for dm in dialog_blocks:
            ln = markup_clean[:dm.start()].count("\n") + 1
            if ln in exempt_lines:
                continue
            inner = dm.group(2)
            if self.is_snippet and (
                not inner.strip() or re.fullmatch(r"(?:<!--[\s\S]*?-->|\s|\.\.\.|…)+", inner)
            ):
                continue
            has_focusable = bool(
                re.search(
                    r"""<(?:button|select|textarea|summary)\b(?![^>]*\bdisabled\b)"""
                    r"""|<input\b(?![^>]*\bdisabled\b)(?![^>]*\btype\s*=\s*["']hidden["'])"""
                    r"""|<a\b[^>]*\bhref\s*="""
                    r"""|\btabindex\s*=\s*(?:"(?:0|[1-9]\d*)"|'(?:0|[1-9]\d*)'|(?:0|[1-9]\d*)\b)""",
                    inner,
                    re.I,
                )
            )
            if not has_focusable:
                line_text = lines[ln - 1] if ln - 1 < len(lines) else ""
                self.add(
                    "MD3E202",
                    "custom",
                    "Modal `<dialog>` contains no keyboard-focusable control.",
                    "Include at least one enabled `<input>`, `<button>`, `<a href>`, or `tabindex=\"0\"` control inside `<dialog>`.",
                    self.path,
                    ln,
                    line_text,
                )

        if self.is_snippet or self.token_file:
            return
        is_full_doc = bool(re.search(r"<!doctype\s+html|<html\b", text, re.I))
        if not is_full_doc:
            return

        has_doc_exempt = bool(re.search(r"<(?:html|body|main)\b[^>]*\bdata-md3e-exempt\b", markup_clean, re.I))
        has_hero_card = bool(re.search(r"bento-card--hero|data-bento-hero\b", text, re.I))
        has_analytical_view = bool(
            re.search(r"<(?:canvas|table)\b|\brole\s*=\s*[\"'](?:grid|treegrid)[\"']|\bdata-md3e-exempt\b", markup_clean, re.I)
            or re.search(r"<svg\b[^>]*(?:chart|plot|graph|axis|trajectory|replay|telemetry)", markup_clean, re.I)
        )
        if has_doc_exempt or (has_analytical_view and not has_hero_card):
            return

        # 2. Full-doc Layer 4 optical glass + clean canvas + HDR + reduced-transparency hygiene (MD3E201)
        has_studio_profile = bool(re.search(r"""data-studio-profile\s*=\s*(?:"personal-studio"|'personal-studio')""", text, re.I))
        has_studio_tokens = linked_studio_css or bool(re.search(r"--md-studio-(?:blur-px|glass-alpha)\s*:", combined_css))
        if not (has_studio_profile and has_studio_tokens):
            self.add(
                "MD3E201",
                "custom",
                "Personal Studio document is missing `data-studio-profile=\"personal-studio\"` or `md3e-studio.css` tokens.",
                "Set `data-studio-profile=\"personal-studio\"` on `<html>` and link `md3e-studio.css` (Layer 4).",
                self.path,
                1,
                "",
            )

        has_optical_glass = linked_blur_css or bool(re.search(r"\bmd3e-blur-", markup_clean)) or "backdrop-filter" in combined_css
        if not has_optical_glass:
            self.add(
                "MD3E201",
                "custom",
                "Personal Studio document is missing optical glass (`.md3e-blur-*` or `backdrop-filter`).",
                "Include `.md3e-blur-*` optical glass chrome (`md3e-blur.css`) over real UI cards without global caustic blobs.",
                self.path,
                1,
                "",
            )

        has_rt_support = (
            linked_blur_css
            or linked_studio_css
            or bool(re.search(r"prefers-reduced-transparency\s*:\s*reduce\b", combined_css, re.I))
            or bool(re.search(r"data-reduced-transparency", text, re.I))
        )
        if not has_rt_support:
            self.add(
                "MD3E201",
                "custom",
                "Personal Studio optical glass layer lacks reduced-transparency support.",
                "Link `md3e-blur.css` / `md3e-studio.css` or provide `@media (prefers-reduced-transparency: reduce)` solid surface fallbacks.",
                self.path,
                1,
                "",
            )

        has_hdr_css = bool(
            re.search(
                r"dynamic-range\s*:\s*high\b|dynamic-range-limit\s*:\s*constrained-high\b|color\(\s*display-p3\b",
                combined_css,
                re.I,
            )
        )
        if has_hdr_css and not linked_studio_css:
            has_sdr_fallback = bool(
                re.search(r"dynamic-range-limit\s*:\s*standard\b|data-studio-hdr\s*=\s*[\"']off[\"']", combined_css, re.I)
            )
            has_contrast_fallback = bool(
                re.search(r"prefers-contrast\s*:\s*more\b|data-contrast\s*=\s*[\"']high[\"']|forced-colors\s*:\s*active\b", combined_css, re.I)
            )
            if not has_sdr_fallback:
                self.add(
                    "MD3E201",
                    "custom",
                    "Personal Studio HDR optical CSS lacks an SDR / `[data-studio-hdr=\"off\"]` fallback.",
                    "Add `dynamic-range-limit: standard` and `[data-studio-hdr=\"off\"]` SDR collapse rules (or link `md3e-studio.css`).",
                    self.path,
                    1,
                    "",
                )
            if not has_contrast_fallback:
                self.add(
                    "MD3E201",
                    "custom",
                    "Personal Studio HDR optical CSS lacks a `prefers-contrast: more` / `forced-colors` fallback.",
                    "Collapse HDR boosts inside `@media (prefers-contrast: more)`, `[data-contrast=\"high\"]`, and `@media (forced-colors: active)`.",
                    self.path,
                    1,
                    "",
                )

    def _audit_rt_specificity(self, rules: list[RuleBlock]) -> None:
        if self.is_snippet:
            return
        rt_none_rules: list[tuple[RuleBlock, list[tuple[int, int, int]], set[str]]] = []
        blur_rules: list[tuple[RuleBlock, int, str, list[tuple[int, int, int]], set[str]]] = []

        for r in rules:
            if r.in_reduced_transparency:
                has_none = any(
                    prop in ("backdrop-filter", "-webkit-backdrop-filter")
                    and strip_important(val).lower() in ("none", "unset", "initial")
                    for prop, val, _, _ in r.declarations
                )
                if has_none:
                    specs = [_branch_specificity(b) for b in split_top_level_commas(r.selector) if b.strip()]
                    rt_none_rules.append((r, specs, _selector_subject_tokens(r.selector)))
            elif not r.in_prefers_contrast and not r.in_forced_colors:
                for prop, val, lineno, raw in r.declarations:
                    if prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in val:
                        specs = [_branch_specificity(b) for b in split_top_level_commas(r.selector) if b.strip()]
                        blur_rules.append((r, lineno, raw, specs, _selector_subject_tokens(r.selector)))
                        break

        if not rt_none_rules or not blur_rules:
            return

        for br, lineno, raw, b_specs, b_tokens in blur_rules:
            if not b_specs or not b_tokens:
                continue
            matching_rt = [
                (rt_r, rt_specs)
                for rt_r, rt_specs, rt_tokens in rt_none_rules
                if (rt_tokens & b_tokens) or "*" in rt_r.selector
            ]
            if not matching_rt:
                continue
            best_rt_spec = max(
                (spec for _, rt_specs in matching_rt for spec in rt_specs),
                default=(0, 0, 0),
            )
            min_blur_spec = min(b_specs)
            if best_rt_spec < min_blur_spec:
                self.add(
                    "MD3E022",
                    "error",
                    f"`backdrop-filter: blur(...)` selector `{br.selector}` (specificity {min_blur_spec}) overrides lower-specificity `@media (prefers-reduced-transparency: reduce)` fallback ({best_rt_spec}).",
                    "Wrap non-essential qualifiers (`:not(...)`) inside `:where(...)` so `@media (prefers-reduced-transparency: reduce)` wins CSS specificity.",
                    self.path,
                    lineno,
                    raw,
                )

    def _audit_keyframe_fill_cascade(
        self,
        rules: list[RuleBlock],
        cleaned_css: str,
        full_text: str | None = None,
    ) -> None:
        if self.is_snippet or self.token_file:
            return
        kf_props = _extract_keyframe_props(cleaned_css)
        if not kf_props:
            return

        has_anim_cleanup = False
        if full_text:
            for sm in re.finditer(r"<script\b[^>]*>([\s\S]*?)</script>", full_text, re.I):
                if re.search(r"\b(?:animationend|animationcancel)\b", sm.group(1)):
                    has_anim_cleanup = True
                    break

        transitioned_bases: set[str] = set()
        for r in rules:
            for prop, val, _, _ in r.declarations:
                if prop in ("transition", "transition-property") and re.search(r"\b(?:transform|opacity)\b", val, re.I):
                    for b in split_top_level_commas(r.selector):
                        stem = re.split(r"[:\[]", b.strip())[0].split(".")[-1]
                        if stem:
                            transitioned_bases.add(f".{stem}")

        for r in rules:
            if r.in_reduced_motion:
                continue
            anim_names: list[str] = []
            fill_modes: list[str] = []
            anim_line = r.start_line
            anim_raw = r.selector
            for prop, val, lineno, raw in r.declarations:
                low_v = strip_important(val).lower()
                if prop == "animation-name":
                    anim_names.extend([t.strip() for t in split_top_level_commas(val)])
                    anim_line, anim_raw = lineno, raw
                elif prop == "animation-fill-mode":
                    fill_modes.extend([t.strip().lower() for t in split_top_level_commas(val)])
                    anim_line, anim_raw = lineno, raw
                elif prop == "animation":
                    for seg in split_top_level_commas(low_v):
                        toks = seg.split()
                        for t in toks:
                            if t in ("both", "forwards"):
                                fill_modes.append(t)
                        for kf in kf_props:
                            if kf.lower() in toks:
                                anim_names.append(kf)
                    anim_line, anim_raw = lineno, raw

            if not any(fm in ("both", "forwards") for fm in fill_modes):
                continue
            locks_tr_op = any(
                (kf_props.get(kf, set()) & {"transform", "opacity"})
                or any(k.lower() == kf.lower() and (ps & {"transform", "opacity"}) for k, ps in kf_props.items())
                for kf in anim_names
            )
            if not locks_tr_op:
                continue

            is_enter_cls = bool(re.search(r"stagger-enter|card-enter|is-[a-z-]*enter", r.selector, re.I))
            shares_transition = any(tb in r.selector for tb in transitioned_bases)
            if (is_enter_cls or shares_transition) and not has_anim_cleanup:
                self.add(
                    "MD3E019",
                    "warning",
                    f"`{r.selector}` retains `animation-fill-mode: both|forwards` on `transform`/`opacity` without `animationend` cleanup, locking inline/state styles via CSS Animation cascade.",
                    "Remove the entrance class on `animationend`/`animationcancel`, or switch to `animation-fill-mode: backwards`.",
                    self.path,
                    anim_line,
                    anim_raw,
                )

    def _audit_allow_discrete_layout_drops(self, rules: list[RuleBlock]) -> None:
        if self.token_file:
            return
        discrete_stems: set[str] = set()
        for r in rules:
            has_discrete = any(
                (prop == "transition-behavior" and "allow-discrete" in val.lower())
                or (prop == "transition" and "allow-discrete" in val.lower())
                for prop, val, _, _ in r.declarations
            )
            if not has_discrete:
                continue
            for b in split_top_level_commas(r.selector):
                if OPEN_STATE_PSEUDO_RE.search(b):
                    continue
                stem = _selector_stem(b)
                if stem:
                    discrete_stems.add(stem)

        if not discrete_stems:
            return

        base_props_by_stem: dict[str, set[str]] = {s: set() for s in discrete_stems}
        open_rules: list[tuple[str, RuleBlock, list[tuple[str, int, str]]]] = []

        for r in rules:
            for b in split_top_level_commas(r.selector):
                stem = _selector_stem(b)
                if stem not in discrete_stems:
                    continue
                if OPEN_STATE_PSEUDO_RE.search(b):
                    hits = [(prop, ln, raw) for prop, _, ln, raw in r.declarations if prop in LAYOUT_ALLOW_DISCRETE_PROPS]
                    if hits:
                        open_rules.append((stem, r, hits))
                else:
                    for prop, _, _, _ in r.declarations:
                        if prop in LAYOUT_ALLOW_DISCRETE_PROPS:
                            base_props_by_stem[stem].add(prop)

        for stem, open_r, hits in open_rules:
            base_props = base_props_by_stem.get(stem, set())
            missing = [(prop, ln, raw) for prop, ln, raw in hits if prop not in base_props]
            if missing:
                prop_list = ", ".join(f"`{p}`" for p, _, _ in missing)
                self.add(
                    "MD3E029",
                    "warning",
                    f"`{open_r.selector}` sets {prop_list} only in its `:popover-open`/`[open]` state while `{stem}` uses `transition-behavior: allow-discrete`, causing layout collapse/squishing during close exit.",
                    f"Move {prop_list} onto the base `{stem}` rule so layout direction/columns/gap persist throughout the exit transition.",
                    self.path,
                    missing[0][1],
                    missing[0][2],
                )

    def _audit_complex_components_document(
        self,
        text: str,
        combined_css: str,
        all_rules: list[RuleBlock],
        markup_clean: str,
        lines: list[str],
        exempt_lines: set[int],
        *,
        linked_studio_css: bool = False,
        has_custom_external_css: bool = False,
    ) -> None:
        is_studio = self.mode == "personal-studio"
        dialog_code = "MD3E202" if is_studio else "MD3E029"
        dialog_sev = "custom" if is_studio else "warning"

        # 1. Native <dialog> redundant role="dialog" / aria-modal (applies to snippets + full docs)
        for m in re.finditer(rf"<dialog\b({TAG_ATTRS_PAT})>", markup_clean, re.I):
            attrs = m.group(1)
            ln = markup_clean[:m.start()].count("\n") + 1
            if ln in exempt_lines:
                continue
            line_text = lines[ln - 1] if ln - 1 < len(lines) else ""
            if re.search(r"""\brole\s*=\s*(?:"dialog"|'dialog')""", attrs, re.I):
                self.add(
                    dialog_code,
                    dialog_sev,
                    "Native `<dialog>` has implicit dialog semantics; remove redundant `role=\"dialog\"`.",
                    "Remove `role=\"dialog\"` from `<dialog>` and use native `.showModal()` / `closedby=\"any\"` with `aria-labelledby` or `aria-label`.",
                    self.path,
                    ln,
                    line_text,
                )
            if re.search(r"""\baria-modal\s*=""", attrs, re.I):
                self.add(
                    dialog_code,
                    dialog_sev,
                    "Native `<dialog>` opened via `.showModal()` handles modality natively; remove redundant `aria-modal`.",
                    "Remove `aria-modal` from `<dialog>` and open modals with `.showModal()`.",
                    self.path,
                    ln,
                    line_text,
                )

        if self.is_snippet or self.token_file:
            return
        is_full_doc = bool(re.search(r"<!doctype\s+html|<html\b", text, re.I))
        if not is_full_doc:
            return

        # 2. JS root scroll-lock inside <script> on a document with <dialog>
        first_dialog = re.search(rf"<dialog\b({TAG_ATTRS_PAT})>", markup_clean, re.I)
        if first_dialog:
            for sm in re.finditer(r"<script\b[^>]*>([\s\S]*?)</script>", text, re.I):
                js_body = sm.group(1)
                js_clean = re.sub(r"//[^\n]*|/\*[\s\S]*?\*/", "", js_body)
                lock_m = re.search(
                    r"document\.(?:body|documentElement)\.style\.overflow(?:Y|Block)?\s*=\s*['\"](?:hidden|clip)['\"]",
                    js_clean,
                )
                if lock_m:
                    base_ln = text[:sm.start(1)].count("\n") + 1
                    ln = base_ln + js_clean[:lock_m.start()].count("\n")
                    self.add(
                        dialog_code,
                        dialog_sev,
                        "Script applies root `html`/`body` `overflow: hidden` scroll-lock alongside `<dialog>`.",
                        "Remove `document.body/documentElement.style.overflow = 'hidden'`; use `dialog:modal { overscroll-behavior: contain; }`.",
                        self.path,
                        ln,
                        lock_m.group(0),
                    )

        # 3. Full-doc <dialog> requires dialog:modal { overscroll-behavior: contain; }
        if first_dialog and not has_custom_external_css:
            has_modal_overscroll = linked_studio_css or any(
                re.search(
                    r"(?:^|[\s,>+~])(?:dialog\b[^,{]*:modal|\.md3e-dialog\b[^,{]*:modal|\.studio-cmd-dialog\b[^,{]*:modal)",
                    rule.selector,
                    re.I,
                )
                and any(
                    prop in ("overscroll-behavior", "overscroll-behavior-y", "overscroll-behavior-block")
                    and strip_important(val).lower() in ("contain", "none")
                    for prop, val, _, _ in rule.declarations
                )
                for rule in all_rules
            )
            if not has_modal_overscroll:
                d_ln = markup_clean[:first_dialog.start()].count("\n") + 1
                self.add(
                    dialog_code,
                    dialog_sev,
                    "`<dialog>` modal lacks `dialog:modal { overscroll-behavior: contain; }` scroll containment.",
                    "Add `dialog:modal { overscroll-behavior: contain; }` and `dialog::backdrop { overflow: hidden; overscroll-behavior: contain; }` (or link `md3e-studio.css`).",
                    self.path,
                    d_ln,
                    lines[d_ln - 1] if d_ln - 1 < len(lines) else "",
                )

        # 4. Custom Select / Date Picker / Menu Contract (MD3E029)
        if has_custom_external_css:
            return
        widget_re = re.compile(
            rf"""<([a-z][a-z0-9:-]*)\b({TAG_ATTRS_PAT}\b(?:role\s*=\s*(?:"(listbox|menu|grid)"|'(listbox|menu|grid)')|focusgroup\s*=\s*(?:"[^"]*\bmenu\b[^"]*"|'[^']*\bmenu\b[^']*'))[^>]*?)>""",
            re.I,
        )
        for wm in widget_re.finditer(markup_clean):
            tag = wm.group(1).lower()
            attrs = wm.group(2)
            role = (wm.group(3) or wm.group(4) or "menu").lower()
            ln = markup_clean[:wm.start()].count("\n") + 1
            if re.search(r"\bdata-md3e-exempt\b", attrs, re.I):
                continue
            if role == "grid" and (
                ln in exempt_lines and re.search(r"\b(?:data-table|stats-table|telemetry-table|analytics-grid)\b", attrs, re.I)
            ):
                continue
            if role != "grid" and ln in exempt_lines:
                continue

            if linked_studio_css and role == "listbox" and re.search(r"studio-cmd-(?:list|dialog__list)", attrs, re.I):
                continue

            stems: set[str] = set()
            id_m = re.search(r"""\bid\s*=\s*(?:"([^"]*)"|'([^']*)')""", attrs, re.I)
            if id_m:
                wid = (id_m.group(1) or id_m.group(2) or "").strip()
                if len(wid) >= 3:
                    stems.add(wid)
                    if "__" in wid:
                        stems.add(wid.split("__", 1)[0])
            cls_m = re.search(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""", attrs, re.I)
            if cls_m:
                for c in (cls_m.group(1) or cls_m.group(2) or "").split():
                    if c.startswith("md3e-blur"):
                        continue
                    if len(c) >= 3:
                        stems.add(c)
                        if "__" in c:
                            stems.add(c.split("__", 1)[0])
                        if "--" in c:
                            stems.add(c.split("--", 1)[0])

            role_hint_re = WIDGET_ROLE_HINTS[role]
            has_state_css = any(
                WIDGET_STATE_SELECTOR_RE.search(rule.selector)
                and (
                    any(stem in rule.selector for stem in stems)
                    or role_hint_re.search(rule.selector)
                )
                for rule in all_rules
            )
            if not has_state_css:
                self.add(
                    "MD3E029",
                    "warning",
                    f"Custom `[role=\"{role}\"]` widget (`<{tag}>`) lacks keyboard-focus or active-state styling (`[data-highlighted]`, `:focus-visible`, `aria-selected`, `[data-selected]`).",
                    f"Add `:focus-visible`, `[data-highlighted]`, `aria-selected`, or `[data-selected]` token rules for `[role=\"{role}\"]` items/cells.",
                    self.path,
                    ln,
                    lines[ln - 1] if ln - 1 < len(lines) else "",
                )

    def audit_markup_document(self, text: str) -> None:
        linked_motion_css = bool(re.search(r"md3e-motion\.css", text))
        linked_studio_css = bool(re.search(r"md3e-studio\.css", text))
        linked_blur_css = bool(re.search(r"md3e-blur\.css", text))
        markup_only = strip_tag_blocks(strip_tag_blocks(text, "script"), "style")
        markup_clean = strip_html_comments(markup_only)
        exempt_lines = find_exempt_line_set(markup_clean)
        lines = markup_clean.splitlines()
        doc_has_dialog = bool(re.search(r"<dialog\b", markup_clean, re.I))

        has_custom_external_css = False
        for lm in re.finditer(r"""<link\b([^>]*\brel\s*=\s*["']stylesheet["'][^>]*)>""", markup_clean, re.I):
            href_m = re.search(r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')""", lm.group(1), re.I)
            href = (href_m.group(1) or href_m.group(2) or "") if href_m else ""
            if href and not re.search(r"fonts\.googleapis\.com|md3e-[a-z0-9-]+\.css", href, re.I):
                has_custom_external_css = True
                break

        # 1. Audit all <style> blocks using full CSS parser
        style_blocks = extract_style_blocks(text)
        combined_css = strip_css_comments("\n".join(blk for blk, _ in style_blocks))
        has_rt_doc = bool(re.search(r"prefers-reduced-transparency\s*:\s*reduce\b", combined_css, re.I))
        all_rules: list[RuleBlock] = []
        for blk, start_line in style_blocks:
            all_rules.extend(parse_css_rules(blk, base_line=start_line))
            self.audit_css(
                blk,
                base_line=start_line,
                check_file_rules=False,
                linked_motion_css=linked_motion_css,
                has_reduced_transparency_doc=has_rt_doc,
                linked_studio_css=linked_studio_css,
                doc_has_dialog=doc_has_dialog,
            )

        if not self.is_snippet and style_blocks:
            self._audit_rt_specificity(all_rules)
            self._audit_keyframe_fill_cascade(all_rules, combined_css, text)
            self._audit_allow_discrete_layout_drops(all_rules)
            has_hover = ":hover" in combined_css
            has_focus_visible = ":focus-visible" in combined_css
            has_reduced = "prefers-reduced-motion" in combined_css
            has_keyframes = "@keyframes" in combined_css
            has_motion_decl = bool(re.search(r"(?:transition|animation)[^;]*(?:var\(--md-sys-motion-|var\(--md-bento-motion-|\d+m?s)", combined_css))
            if has_hover and not has_focus_visible:
                self.add(
                    "MD3E005", "error",
                    "Document styles :hover states without :focus-visible.",
                    "Add `:focus-visible` indicator styling for keyboard users.",
                    self.path, 0, "",
                )
            if (has_keyframes or (has_motion_decl and not linked_motion_css)) and not has_reduced:
                self.add(
                    "MD3E008", "warning",
                    "Custom motion/keyframes defined without a prefers-reduced-motion path.",
                    "Add `@media (prefers-reduced-motion: reduce)` handling.",
                    self.path, 0, "",
                )

        # 2. Inline style="..." checks outside <script>/<style> (honouring data-view exemptions)
        for i, line in enumerate(lines, start=1):
            is_exempt_line = i in exempt_lines
            is_floating_label_line = bool(
                re.search(r"<label\b[^>]*(?:md3e-text-field__label|md3e-field__label|floating-label|outlined-label)", line, re.I)
            )
            for sm in STYLE_ATTR_RE.finditer(line):
                style_val = sm.group(1) if sm.group(1) is not None else sm.group(2)
                inline_decls = iter_inline_declarations(style_val)
                check_role_pairing_and_contrast(
                    self,
                    [(p, v, i, line) for p, v in inline_decls],
                    is_data_view=is_exempt_line,
                )
                for prop, val in inline_decls:
                    if not is_exempt_line:
                        check_hex(self, val, i, line)
                        check_func_color(self, val, i, line)
                        check_radius(self, prop, val, i, line)
                        check_font_size(self, prop, val, i, line)
                        check_shadow(self, prop, val, i, line)
                        check_bento_decl(self, prop, val, i, line)
                        if (
                            is_floating_label_line
                            and prop in ("background", "background-color")
                            and strip_important(val).lower() not in ("transparent", "none", "inherit", "initial", "unset", "")
                        ):
                            self.add(
                                "MD3E029",
                                "warning",
                                "Floating text-field `<label>` applies an inline opaque `background` patch.",
                                "Use a `<fieldset><legend>` transparent cutout (or `mask-image`) instead of a solid label background.",
                                self.path,
                                i,
                                line,
                            )
                    check_color_mix(self, val, i, line)
                    check_motion(self, prop, val, i, line)
                    check_misc(self, prop, val, i, line)
                    if not self.token_file and prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in val:
                        self.add(
                            "MD3E022", "error",
                            "Inline `backdrop-filter: blur(...)` cannot honour `prefers-reduced-transparency: reduce`.",
                            "Move frosted glass styles to `md3e-blur.css` or CSS with `@media (prefers-reduced-transparency: reduce)`.",
                            self.path, i, line,
                        )

        # 3. HTML component, icon, tag, accessibility & desktop-bento / personal-studio / complex-component checks
        self._audit_desktop_bento_document(text, combined_css, markup_only)
        self._audit_personal_studio_document(
            text,
            combined_css,
            markup_clean,
            lines,
            exempt_lines,
            linked_studio_css=linked_studio_css,
            linked_blur_css=linked_blur_css,
        )
        self._audit_complex_components_document(
            text,
            combined_css,
            all_rules,
            markup_clean,
            lines,
            exempt_lines,
            linked_studio_css=linked_studio_css,
            has_custom_external_css=has_custom_external_css,
        )
        self._audit_html_semantics(markup_only, full_text=text, exempt_lines=exempt_lines)

    def _check_multiple_primary_filled_buttons(self, markup_clean: str, lines: list[str], exempt_lines: set[int]) -> None:
        if self.token_file:
            return
        token_re = re.compile(rf"<(/?)([a-zA-Z][a-zA-Z0-9:-]*)\b({TAG_ATTRS_PAT})(/?)>")
        # Each scope frame: [tag_name, open_line, filled_count, reported_2nd]
        scopes: list[list] = [["document", 1, 0, False]]
        for m in token_re.finditer(markup_clean):
            is_close = m.group(1) == "/"
            tag = m.group(2).lower()
            attrs = m.group(3)
            self_closing = bool(m.group(4)) or tag in VOID_HTML_TAGS
            ln = markup_clean[:m.start()].count("\n") + 1
            if not is_close:
                starts_scope = bool(
                    tag in ("section", "dialog", "form")
                    or re.search(r"\bpopover\b", attrs, re.I)
                )
                is_enabled_filled = bool(
                    ln not in exempt_lines
                    and not re.search(r"\bdisabled\b", attrs, re.I)
                    and tag in ("button", "a")
                    and re.search(r"(?<![\w-])(?:md3e-btn--filled|btn-filled|btn--filled)(?![\w-])", attrs, re.I)
                )
                if is_enabled_filled:
                    scopes[-1][2] += 1
                    if scopes[-1][2] == 2 and not scopes[-1][3]:
                        scopes[-1][3] = True
                        self.add(
                            "MD3E025", "info",
                            f"Multiple enabled primary `filled` buttons in `{scopes[-1][0]}` view (project convention).",
                            "Use at most one primary `filled` CTA per view/surface; demote secondary actions to tonal, outlined, or text.",
                            self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
                        )
                if starts_scope and not self_closing:
                    scopes.append([tag, ln, 0, False])
            else:
                for idx in range(len(scopes) - 1, 0, -1):
                    if scopes[idx][0] == tag:
                        del scopes[idx:]
                        break

    def _check_modern_semantics_and_token_classes(
        self,
        markup_clean: str,
        full_text: str,
        lines: list[str],
        exempt_lines: set[int],
    ) -> None:
        # 1. Reject legacy @material/web / md3e-material-web.css references (MD3E020)
        uncommented_full = re.sub(
            r"(?m)(?<!:)//[^\n]*",
            "",
            strip_css_comments(strip_html_comments(full_text)),
        )
        full_lines = full_text.splitlines()
        for m in LEGACY_MWC_REF_RE.finditer(uncommented_full):
            ln = uncommented_full[:m.start()].count("\n") + 1
            snip = full_lines[ln - 1] if ln - 1 < len(full_lines) else m.group(0)
            self.add(
                "MD3E020", "error",
                f"Legacy `@material/web` dependency `{m.group(0)}` is no longer supported.",
                "Remove `@material/web` / `md3e-material-web.css` and style native semantic HTML (`<button>`, `<input>`, `<dialog>`, or Headless UI primitives) directly with MD3E CSS tokens.",
                self.path, ln, snip,
            )

        # Reject <md-*> custom element tags (MD3E020)
        reported_md_lines: set[int] = set()
        for m in LEGACY_MD_TAG_RE.finditer(markup_clean):
            ln = markup_clean[:m.start()].count("\n") + 1
            if ln in reported_md_lines:
                continue
            reported_md_lines.add(ln)
            tag_name = m.group(2).lower()
            self.add(
                "MD3E020", "error",
                f"Legacy Web Component tag `<{tag_name}>` is removed in unified semantic MD3E.",
                f"Replace `<{tag_name}>` with native semantic HTML (`<button>`, `<input>`, `<dialog>`, `role=\"switch\"`) + `.md3e-*` classes or Headless UI primitives (Radix UI / Base UI).",
                self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
            )

        # 2. Validate native/headless ARIA contracts (MD3E020) & MD3E modifier bindings (MD3E026)
        interactive_roles = {"button", "switch", "checkbox", "tab", "menuitem", "option", "slider", "link"}
        for m in OPEN_TAG_RE.finditer(markup_clean):
            tag = m.group(1).lower()
            attrs = m.group(2)
            if tag.startswith("md-"):
                continue
            ln = markup_clean[:m.start()].count("\n") + 1
            if ln in exempt_lines:
                continue
            line_text = lines[ln - 1] if ln - 1 < len(lines) else ""
            has_jsx_spread = "{..." in attrs

            # Check boolean / tristate ARIA attribute values when literal
            for am in re.finditer(
                r"""\b(aria-(?:pressed|expanded|selected|checked|disabled|modal))\s*=\s*(?:"([^"]*)"|'([^']*)')""",
                attrs,
                re.I,
            ):
                attr_name = am.group(1).lower()
                val = (am.group(2) if am.group(2) is not None else am.group(3)).strip().lower()
                if any(ch in val for ch in ("{", "}", "$")):
                    continue
                allowed = {"true", "false"}
                if attr_name in ("aria-checked", "aria-pressed"):
                    allowed.update({"mixed", "undefined"})
                elif attr_name == "aria-expanded":
                    allowed.add("undefined")
                if val not in allowed:
                    self.add(
                        "MD3E020", "error",
                        f"Invalid ARIA state literal `{attr_name}=\"{val}\"` on `<{tag}>`.",
                        f"Set `{attr_name}` to `\"true\"` / `\"false\"` (or valid ARIA token) instead of `{val!r}`.",
                        self.path, ln, line_text,
                    )

            role_m = re.search(r"""\brole\s*=\s*(?:"([^"]*)"|'([^']*)')""", attrs, re.I)
            role = (role_m.group(1) if role_m.group(1) is not None else role_m.group(2)).strip().lower() if role_m else ""
            if role and not has_jsx_spread:
                if (role == "switch" or (role == "checkbox" and tag != "input")) and not re.search(r"\baria-checked\s*=", attrs, re.I):
                    self.add(
                        "MD3E020", "error",
                        f"`<{tag} role=\"{role}\">` is missing required `aria-checked` state.",
                        "Bind `aria-checked=\"true\"` / `\"false\"` (or controlled headless state) cleanly.",
                        self.path, ln, line_text,
                    )
                if (
                    tag in ("div", "span")
                    and role in interactive_roles
                    and not re.search(r"\btabindex\s*=", attrs, re.I)
                    and not re.search(r"""\bdisabled\b|\baria-disabled\s*=\s*(?:"true"|'true')""", attrs, re.I)
                ):
                    self.add(
                        "MD3E020", "error",
                        f"Non-semantic `<{tag} role=\"{role}\">` lacks `tabindex` keyboard focusability.",
                        "Prefer native `<button>` / `<a href>` / `<input>`, or add `tabindex=\"0\"` + Enter/Space handling.",
                        self.path, ln, line_text,
                    )
                if role == "combobox" and not re.search(r"\baria-expanded\s*=", attrs, re.I):
                    self.add(
                        "MD3E020", "error",
                        f"`<{tag} role=\"combobox\">` is missing `aria-expanded` state.",
                        "Bind `aria-expanded=\"true\"` / `\"false\"` on combobox controls.",
                        self.path, ln, line_text,
                    )
                if role == "slider" and tag != "input" and not re.search(r"\baria-valuenow\s*=", attrs, re.I):
                    self.add(
                        "MD3E020", "error",
                        f"Custom `<{tag} role=\"slider\">` is missing `aria-valuenow`.",
                        "Prefer native `<input type=\"range\" class=\"md3e-range\">` or provide `aria-valuenow` / `min` / `max`.",
                        self.path, ln, line_text,
                    )

            cls_attr_m = re.search(r"""\b(?:class|className)\s*=\s*(?:"([^"]*)"|'([^']*)')""", attrs, re.I)
            if cls_attr_m and not has_jsx_spread:
                cls_val = cls_attr_m.group(1) if cls_attr_m.group(1) is not None else cls_attr_m.group(2)
                cls_set_check = set(cls_val.split())
                if (
                    any(c in cls_set_check for c in ("context-menu", "md3e-context-menu", "bento-context-menu"))
                    and role != "menu"
                    and not re.search(r"\bfocusgroup\s*=", attrs, re.I)
                ):
                    self.add(
                        "MD3E020", "error",
                        f"Context menu container `<{tag}>` lacks `role=\"menu\"` (or `focusgroup=\"menu\"`).",
                        "Expose `role=\"menu\"` with `role=\"menuitem\"` children, ArrowUp/ArrowDown/Home/End/Escape handling, and outside-dismiss.",
                        self.path, ln, line_text,
                    )

            # Check MD3E token class bindings (MD3E026)
            for cm in re.finditer(r"""\b(?:class|className)\s*=\s*(?:"([^"]*)"|'([^']*)')""", attrs, re.I):
                raw_cls = cm.group(1) if cm.group(1) is not None else cm.group(2)
                if any(ch in raw_cls for ch in ("{", "}", "$")):
                    continue
                cls_tokens = raw_cls.split()
                cls_set = set(cls_tokens)
                if LEGACY_MWC_CLASS_RE.search(raw_cls):
                    bad_cls = LEGACY_MWC_CLASS_RE.search(raw_cls).group(0)
                    self.add(
                        "MD3E026", "warning",
                        f"Deprecated MWC bridge class `{bad_cls}` has been replaced by native token classes.",
                        "Use semantic base + modifier classes (e.g. `.md3e-btn .md3e-btn--m .md3e-btn--square` or `.md3e-fab--medium`).",
                        self.path, ln, line_text,
                    )
                btn_mods = [c for c in cls_tokens if c.startswith("md3e-btn--")]
                if btn_mods and "md3e-btn" not in cls_set:
                    self.add(
                        "MD3E026", "warning",
                        f"MD3E button modifier `{btn_mods[0]}` used without base class `md3e-btn`.",
                        "Pair modifier classes with the base `.md3e-btn` class.",
                        self.path, ln, line_text,
                    )
                icon_btn_mods = [c for c in cls_tokens if c.startswith("md3e-icon-btn--")]
                if icon_btn_mods and "md3e-icon-btn" not in cls_set:
                    self.add(
                        "MD3E026", "warning",
                        f"MD3E icon-button modifier `{icon_btn_mods[0]}` used without base class `md3e-icon-btn`.",
                        "Pair modifier classes with the base `.md3e-icon-btn` class.",
                        self.path, ln, line_text,
                    )
                shape_mods = [c for c in cls_tokens if c.startswith("md3e-shape-") and c != "md3e-shape-shadow-wrap"]
                if shape_mods and "md3e-shape" not in cls_set:
                    self.add(
                        "MD3E026", "warning",
                        f"MD3E shape mask modifier `{shape_mods[0]}` used without base class `md3e-shape`.",
                        "Include the base `md3e-shape` class alongside `.md3e-shape-<name>` so CSS mask containment & fallback work.",
                        self.path, ln, line_text,
                    )
                blur_mods = [c for c in cls_tokens if c.startswith("md3e-blur--")]
                has_blur_base = any(
                    c == "md3e-blur" or (c.startswith("md3e-blur-") and not c.startswith("md3e-blur--"))
                    for c in cls_set
                )
                if blur_mods and not has_blur_base:
                    self.add(
                        "MD3E026", "warning",
                        f"MD3E blur modifier `{blur_mods[0]}` used without a base `md3e-blur*` surface class.",
                        "Pair blur size modifiers with `.md3e-blur-surface*` or `.md3e-blur-primary` so reduced-transparency fallbacks apply.",
                        self.path, ln, line_text,
                    )

    def _audit_html_semantics(self, markup_only: str, *, full_text: str, exempt_lines: set[int] | None = None) -> None:
        markup_clean = strip_html_comments(markup_only)
        lines = markup_clean.splitlines()
        if exempt_lines is None:
            exempt_lines = find_exempt_line_set(markup_clean)

        self._check_modern_semantics_and_token_classes(markup_clean, full_text, lines, exempt_lines)
        self._check_multiple_primary_filled_buttons(markup_clean, lines, exempt_lines)

        # Check full document Material Symbols font link (MD3E017)
        is_full_doc = (
            not self.is_snippet
            and bool(re.search(r"<!doctype\s+html|<html\b", full_text, re.I))
        )
        uses_ligature_icons = bool(re.search(r"\bmaterial-symbols-(?:outlined|rounded|sharp)\b", markup_clean))
        has_ms_font_link = bool(
            re.search(r"Material\+Symbols|Material\s+Symbols", full_text)
        )
        if is_full_doc and uses_ligature_icons and not has_ms_font_link:
            self.add(
                "MD3E017", "error",
                "Page uses Material Symbols ligature icons without loading the Material Symbols stylesheet.",
                "Add Google Fonts Material Symbols `<link>` with `&display=block` in `<head>`, "
                "or render inline `<svg>` icons in offline builds.",
                self.path, 1, "",
            )

        # Check Google Fonts Material Symbols URL axis order (MD3E017)
        self._check_ms_font_axes(markup_clean, base_line=1)

        # Check icon ligatures across single-line and multi-line tags (MD3E017)
        for m in iter_icon_matches(markup_clean):
            glyph = m.group(2).strip()
            if not glyph or any(tok in glyph for tok in ("{", "}", "$", "<")):
                continue
            ln = markup_clean[:m.start()].count("\n") + 1
            line_text = lines[ln - 1] if ln - 1 < len(lines) else ""
            if glyph in BAD_ICON_ALIASES:
                self.add(
                    "MD3E017", "error",
                    f"Icon name `{glyph}` is not a Material Symbols ligature.",
                    f"Replace `{glyph}` with `{BAD_ICON_ALIASES[glyph]}` (see references/icons.md).",
                    self.path, ln, line_text,
                )
            elif not re.fullmatch(r"[a-z0-9_]+", glyph):
                self.add(
                    "MD3E017", "error",
                    f"Invalid Material Symbols ligature `{glyph}` (must be lowercase snake_case).",
                    "Use lowercase `snake_case` Material Symbols names (never hyphens, spaces, or camelCase).",
                    self.path, ln, line_text,
                )

        # Check deprecated controls line by line
        for i, line in enumerate(lines, start=1):
            if re.search(r"bottom[-_]app[-_]bar", line, re.I):
                self.add(
                    "MD3E015", "info",
                    "Bottom app bar is deprecated in M3E.",
                    "Replace with a docked or floating toolbar (64dp height).",
                    self.path, i, line,
                )
            if re.search(r"\b(?:md3e-fab--small|fab[-_]small|small[-_]fab)\b", line, re.I):
                if i not in exempt_lines:
                    self.add(
                        "MD3E016", "warning",
                        "Small FAB (40dp) is deprecated in MD3E.",
                        "Use Standard FAB (56dp) or Medium FAB (80dp, corner 20dp).",
                        self.path, i, line,
                    )

        # Check decorative icons inside buttons/links missing aria-hidden="true" (MD3E021)
        # and icon-only controls missing accessible names (MD3E014).
        reported_a11y_lines: set[int] = set()
        ctrl_re = re.compile(
            rf"<(button|a)\b({TAG_ATTRS_PAT})>([\s\S]*?)</\1>",
            re.IGNORECASE,
        )
        for m in ctrl_re.finditer(markup_clean):
            attrs = m.group(2)
            inner = m.group(3)
            ctrl_line = markup_clean[:m.start()].count("\n") + 1
            has_ctrl_label = bool(
                re.search(
                    r'\b(?:aria-label|aria-labelledby|label|title)\s*=\s*(?:"[^"]*\S[^"]*"|\'[^\']*\S[^\']*\'|\{[^}]*\S[^}]*\})',
                    attrs,
                    re.I,
                )
            )
            inner_no_icons = re.sub(r"<span\b[^>]*\bmaterial-symbols-[^>]*>[^<]*</span>", "", inner, flags=re.I)
            inner_no_icons = re.sub(r"<svg\b[\s\S]*?</svg>", "", inner_no_icons, flags=re.I)
            has_visible_text = bool(re.sub(r"<[^>]+>", "", inner_no_icons).strip())
            has_img_alt = bool(re.search(r'<img\b[^>]*\balt\s*=\s*(?:"[^"]*\S[^"]*"|\'[^\']*\S[^\']*\')', inner, re.I))
            has_svg_title = bool(re.search(r"<svg\b[^>]*>[\s\S]*?<title\b[^>]*>[^<]+</title>", inner, re.I))
            icon_matches = iter_icon_matches(inner)
            has_icon_child = bool(icon_matches or re.search(r"<(?:svg|img)\b", inner, re.I))
            if (
                not has_ctrl_label
                and not has_visible_text
                and not has_img_alt
                and not has_svg_title
                and has_icon_child
                and ctrl_line not in reported_a11y_lines
            ):
                reported_a11y_lines.add(ctrl_line)
                self.add(
                    "MD3E014", "error",
                    "Icon-only control without an accessible name.",
                    "Add `aria-label` (or a visually hidden span) to the interactive control.",
                    self.path, ctrl_line, lines[ctrl_line - 1] if ctrl_line - 1 < len(lines) else "",
                )
            if not (has_ctrl_label or has_visible_text or has_img_alt or has_svg_title):
                continue
            for icon_m in icon_matches:
                icon_attrs = icon_m.group(1)
                if not re.search(r"""\baria-hidden\s*=\s*(?:["']true["']|\{true\})""", icon_attrs, re.I):
                    ln = markup_clean[:m.start(3) + icon_m.start()].count("\n") + 1
                    self.add(
                        "MD3E021", "warning",
                        "Decorative Material Symbols icon inside a labelled control is missing `aria-hidden=\"true\"`.",
                        "Add `aria-hidden=\"true\"` to the icon element so screen readers do not read the raw ligature name.",
                        self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
                    )

    def audit_generic_code(self, text: str) -> None:
        # Handle JSX/TSX/JS/TS lines + HTML-like snippets cleanly
        markup_clean = strip_html_comments(text)
        exempt_lines = find_exempt_line_set(markup_clean)
        lines = text.splitlines()
        selector = ""
        depth = 0
        for i, raw in enumerate(lines, start=1):
            is_exempt_line = i in exempt_lines
            is_data_sel = bool(selector and any(DATA_VIEW_SELECTOR_RE.search(s) for s in selector.split(",")))
            # Also check inline style="..." in JSX/PHP templates
            for sm in STYLE_ATTR_RE.finditer(raw):
                style_val = sm.group(1) if sm.group(1) is not None else sm.group(2)
                inline_decls = iter_inline_declarations(style_val)
                check_role_pairing_and_contrast(
                    self,
                    [(p, v, i, raw) for p, v in inline_decls],
                    is_data_view=is_exempt_line,
                )
                for prop, val in inline_decls:
                    if not is_exempt_line:
                        check_hex(self, val, i, raw)
                        check_func_color(self, val, i, raw)
                        check_radius(self, prop, val, i, raw)
                        check_font_size(self, prop, val, i, raw)
                        check_shadow(self, prop, val, i, raw)
                        check_bento_decl(self, prop, val, i, raw)
                    check_color_mix(self, val, i, raw)
                    check_motion(self, prop, val, i, raw)
                    check_misc(self, prop, val, i, raw)
                    if not self.token_file and prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in val:
                        self.add(
                            "MD3E022", "error",
                            "Inline `backdrop-filter: blur(...)` cannot honour `prefers-reduced-transparency: reduce`.",
                            "Move frosted glass styles to `md3e-blur.css` or CSS with `@media (prefers-reduced-transparency: reduce)`.",
                            self.path, i, raw,
                        )

            if "{" in raw and not raw.strip().startswith("<"):
                candidate = raw.split("{", 1)[0].strip()
                if candidate and not candidate.startswith("@"):
                    selector = candidate
                depth += 1
            if not raw.strip().startswith(("//", "*", "/*", "import ", "export ", "const ", "let ", "var ")):
                for piece in raw.split(";"):
                    piece = piece.strip()
                    m = PROP_VALUE_RE.match(piece)
                    if m and not m.group("prop").startswith("--"):
                        prop = m.group("prop").lower()
                        val = m.group("value")
                        if not (is_exempt_line or is_data_sel):
                            check_hex(self, val, i, raw)
                            check_func_color(self, val, i, raw)
                            check_radius(self, prop, val, i, raw)
                            check_font_size(self, prop, val, i, raw)
                            check_shadow(self, prop, val, i, raw)
                            check_bento_decl(self, prop, val, i, raw)
                        check_color_mix(self, val, i, raw)
                        check_motion(self, prop, val, i, raw)
                        check_misc(self, prop, val, i, raw)
            if "}" in raw:
                depth = max(0, depth - raw.count("}"))
                if depth == 0:
                    selector = ""
        self._audit_html_semantics(text, full_text=text, exempt_lines=exempt_lines)


# ===========================================================================
# Markdown fenced-block auditing (--markdown)
# ===========================================================================

FENCE_LANG_EXT = {
    "html": ".html",
    "htm": ".html",
    "css": ".css",
    "scss": ".scss",
    "less": ".less",
    "jsx": ".jsx",
    "tsx": ".tsx",
    "vue": ".vue",
    "svelte": ".svelte",
}


def audit_markdown(path: pathlib.Path, text: str, *, mode: str = "strict") -> list[Finding]:
    mode = normalize_mode(mode)
    findings: list[Finding] = []
    fence_re = re.compile(r"```([a-zA-Z0-9_-]+)\s*\n([\s\S]*?)```")
    for m in fence_re.finditer(text):
        lang = m.group(1).lower()
        ext = FENCE_LANG_EXT.get(lang)
        if not ext:
            continue
        code = m.group(2)
        start_line = text[:m.start(2)].count("\n") + 1
        virtual_path = path.with_name(f"{path.name}{ext}")
        sub_findings = Checker(virtual_path, is_snippet=True, mode=mode).run(code)
        for f in sub_findings:
            f.path = str(path)
            if f.line > 0:
                f.line = start_line + f.line - 1
            findings.append(f)
    return findings


# ===========================================================================
# Driver
# ===========================================================================

def iter_files(paths: list[str], exclude: list[str], *, include_markdown: bool = False) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    allowed = set(CODE_EXTENSIONS)
    if include_markdown:
        allowed.add(".md")
    for raw in paths:
        p = pathlib.Path(raw)
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if not child.is_file() or child.suffix.lower() not in allowed:
                    continue
                if {part.lower() for part in child.parts} & SKIP_DIRS:
                    continue
                if any(x.lower() in str(child).lower() for x in exclude):
                    continue
                out.append(child)
        else:
            print(f"warning: {raw} does not exist", file=sys.stderr)
    return out


def audit(paths: list[str], exclude: list[str], *, include_markdown: bool = False, mode: str = "strict") -> tuple[list[FileReport], int]:
    mode = normalize_mode(mode)
    files = iter_files(paths, exclude, include_markdown=include_markdown)
    reports: list[FileReport] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        if path.suffix.lower() == ".md":
            findings = audit_markdown(path, text, mode=mode) if include_markdown else []
        else:
            findings = Checker(path, mode=mode).run(text)
        if findings:
            reports.append(FileReport(str(path), findings))
    return reports, len(files)


def render_text(reports: list[FileReport], min_severity: str, scanned: int, *, mode: str = "strict") -> None:
    shown_counts = {s: 0 for s in SEVERITIES}
    total_counts = {s: 0 for s in SEVERITIES}
    for report in reports:
        for f in report.findings:
            total_counts[f.severity] += 1
        shown = [f for f in report.findings
                 if SEVERITY_RANK[f.severity] <= SEVERITY_RANK[min_severity]]
        if not shown:
            continue
        shown.sort(key=lambda f: (SEVERITY_RANK[f.severity], f.line))
        print(f"\n\033[1m{report.path}\033[0m")
        for f in shown:
            shown_counts[f.severity] += 1
            print(f"  [{f.severity.upper():<7}] {f.code}"
                  + (f"  line {f.line}" if f.line else ""))
            print(f"            {f.message}")
            print(f"            fix: {f.fix}")
            if f.snippet:
                print(f"            > {f.snippet}")

    err_n = total_counts["error"]
    warn_n = total_counts["warning"]
    info_n = total_counts["info"]
    cust_n = total_counts["custom"]
    official_score = max(0, 100 - 15 * err_n - 5 * warn_n)
    official_verdict = "FAIL" if err_n else ("WARNING" if warn_n else "PASS")

    print("\n" + "=" * 72)
    print(
        f"MD3E audit ({mode}): {official_verdict} (official score {official_score}/100)   "
        f"{err_n} ERROR, {warn_n} WARNING, {info_n} INFO, {cust_n} CUSTOM   ({scanned} file(s) scanned)"
    )
    if not any(total_counts.values()):
        print("All checks passed. Nothing to fix.")
        return
    print("Fix priority: ERROR (official/WCAG) -> WARNING (recommended) -> INFO (project defaults); CUSTOM does not affect Official Score.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit front-end code against layered M3E, Web adaptation & product extension rules.")
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--markdown", action="store_true",
                        help="also audit HTML/CSS fenced code blocks in .md files")
    parser.add_argument("--mode", type=normalize_mode, default="strict",
                        help="audit policy profile: strict (default, alias: default), desktop-bento, or personal-studio")
    parser.add_argument("--exclude", default="",
                        help="comma-separated substrings to skip")
    parser.add_argument("--fail-on", type=normalize_severity, default="error",
                        help="severity threshold that fails the run (error, warning/warn, info, custom; default: error)")
    parser.add_argument("--min-severity", type=normalize_severity, default=None,
                        help="lowest severity to report (default: custom in desktop-bento/personal-studio, info in strict)")
    args = parser.parse_args(argv)
    min_sev = args.min_severity or ("custom" if args.mode in ("desktop-bento", "personal-studio") else "info")

    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    reports, scanned = audit(args.paths, exclude, include_markdown=args.markdown, mode=args.mode)

    counts = {
        s: sum(1 for r in reports for f in r.findings if f.severity == s)
        for s in SEVERITIES
    }
    official_score = max(0, 100 - 15 * counts["error"] - 5 * counts["warning"])
    official_verdict = "FAIL" if counts["error"] else ("WARNING" if counts["warning"] else "PASS")

    if args.json:
        print(json.dumps({
            "mode": args.mode,
            "official_compliance": {
                "verdict": official_verdict,
                "score": official_score,
                "error": counts["error"],
                "warning": counts["warning"],
                "info": counts["info"],
            },
            "custom_extensions": {
                "active": args.mode in ("desktop-bento", "personal-studio"),
                "custom": counts["custom"],
            },
            "summary": counts,
            "files_scanned": scanned,
            "files": [
                {"path": r.path, "findings": [f.to_dict() for f in r.findings]}
                for r in reports
            ],
        }, indent=2))
    else:
        render_text(reports, min_sev, scanned, mode=args.mode)

    worst = min((SEVERITY_RANK[f.severity] for r in reports for f in r.findings),
                default=len(SEVERITIES))
    return 1 if worst <= SEVERITY_RANK[args.fail_on] else 0


if __name__ == "__main__":
    sys.exit(main())
