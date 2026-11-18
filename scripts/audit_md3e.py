#!/usr/bin/env python3
"""Audit front-end code for Material 3 Expressive (MD3E) compliance.

Deterministic static checks for the rules that models and humans most often
break when implementing MD3E: hardcoded colours, off-scale corner radii,
duration/easing motion instead of springs, unfocusable controls, sub-48px
targets, off-scale type sizes, icon ligature/font mistakes, unitless
color-mix(), composite animation delay bugs, 9999px morph snaps, and
mismatched Material Web tags.

Usage
-----
    python audit_md3e.py <path>...            # files or directories
    python audit_md3e.py src --mode=desktop-bento --fail-on warn
    python audit_md3e.py src --json           # machine-readable
    python audit_md3e.py src --fail-on warn   # stricter CI gate
    python audit_md3e.py docs --markdown      # audit HTML/CSS fences in .md
    python audit_md3e.py src --exclude vendor,node_modules

Exit status is 1 when findings at or above the --fail-on severity exist,
otherwise 0. Token/theme files are auto-detected and exempted from the
hardcoded-colour checks, because that is exactly where raw values belong.

Finding codes
-------------
    MD3E001  hardcoded hex colour                           (error)
    MD3E002  hardcoded rgb()/hsl() colour                   (error)
    MD3E003  corner radius off the shape scale              (error)
    MD3E004  duration/easing instead of a spring            (error/info)
    MD3E005  focus indicator removed / missing              (error/warn)
    MD3E006  interactive target <48px or box inflated       (warn)
    MD3E007  font-size off the type scale                   (warn)
    MD3E008  no prefers-reduced-motion path                 (warn)
    MD3E009  colour roles without a dark scheme             (warn)
    MD3E010  box-shadow used for elevation                  (info)
    MD3E011  border-radius: 50% instead of full             (warn)
    MD3E012  uppercase label text                           (info)
    MD3E013  `transition: all`                              (warn)
    MD3E014  icon-only control, no accessible name          (warn)
    MD3E015  deprecated bottom app bar                      (info)
    MD3E016  deprecated small FAB (40dp)                    (warn)
    MD3E017  invalid Material Symbols icon, URL axes, or missing font (error)
    MD3E018  invalid color-mix() opacity or oklch on neutrals (error/warn)
    MD3E019  composite animation delay or 9999px morph snap (warn)
    MD3E020  mismatched <md-*> custom element closing tag   (error)
    MD3E021  decorative icon missing aria-hidden="true"     (warn)
    MD3E022  backdrop-filter blur lacks reduced-transparency (warn)
    MD3E023  box-shadow on masked/morphing shape vs drop-shadow (warn/error)
    MD3E101  [desktop-bento] 1px border or rectangular box-shadow (error)
    MD3E102  [desktop-bento] <4 surface-container nesting tiers   (error)
    MD3E103  [desktop-bento] missing concentric 28px/16px radii   (warn)
    MD3E104  [desktop-bento] missing Hero wave/sparkline/morph anchors (warn)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

SEVERITIES = ("error", "warn", "info")
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITIES)}
AUDIT_MODES = ("strict", "desktop-bento")

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

# --- Design system facts the checks are built on ---------------------------

CORNER_SCALE_PX = {0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 28.0, 32.0, 48.0}
FULL_PX = {999.0, 9999.0, 1000.0}

TYPE_SCALE_PX = {11.0, 12.0, 14.0, 16.0, 22.0, 24.0, 28.0, 32.0, 36.0, 45.0, 57.0}
TYPE_SCALE_REM = {round(v / 16.0, 5) for v in TYPE_SCALE_PX}

MIN_TOUCH_TARGET = 48.0

# Official M3E Web cubic-bezier curves (allowed as official Web equivalents).
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
}

# Curated aliases hallucinated from Lucide / FontAwesome / Heroicons.
BAD_ICON_ALIASES = {
    "plus": "add",
    "trash": "delete",
    "cog": "settings",
    "gear": "settings",
    "bell": "notifications",
    "heart": "favorite",
    "moon": "dark_mode",
    "sun": "light_mode",
    "x": "close",
    "times": "close",
    "pencil": "edit",
    "pen": "edit",
    "user": "person",
    "bars": "menu",
    "hamburger": "menu",
    "sliders": "tune",
    "eye": "visibility",
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
    "adjustments": "tune",
    "account": "person",
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
    r"(?:__|-) (?:icon|chevron|label|divider|pill|scrim|dot|morph|box)\b"
    .replace(" ", ""),
    re.IGNORECASE,
)
INTERACTIVE_ELEMENT_RE = re.compile(
    r"<(?:button|a\s|input|select|textarea|md-filled-button|md-outlined-button"
    r"|md-text-button|md-elevated-button|md-filled-tonal-button|md-icon-button"
    r"|md-filled-icon-button|md-filled-tonal-icon-button|md-outlined-icon-button"
    r"|md-fab|md-extended-fab|md-checkbox|md-radio|md-switch|md-chip-set)",
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
MD_ICON_RE = re.compile(rf"""<md-icon\b({TAG_ATTRS_PAT})>([^<]*)</md-icon>""", re.IGNORECASE)
MD_TAG_RE = re.compile(rf"""<(/?)(md-[a-z0-9-]+)\b({TAG_ATTRS_PAT})>""", re.IGNORECASE)
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
    """Return Material Symbols <span> and <md-icon> matches across single/multi-line tags."""
    matches: list[re.Match[str]] = []
    for m in SPAN_ELEM_RE.finditer(text):
        if MS_CLASS_RE.search(m.group(1)):
            matches.append(m)
    matches.extend(MD_ICON_RE.finditer(text))
    matches.sort(key=lambda m: m.start())
    return matches


def parse_css_rules(css_text: str, base_line: int = 1) -> list[RuleBlock]:
    """Brace-aware CSS rule extractor tracking reduced-motion & forced-colors."""
    cleaned = strip_css_comments(css_text)
    rules: list[RuleBlock] = []
    stack: list[tuple[str, bool, bool, int]] = []
    current_decls: dict[int, list[tuple[str, str, int, str]]] = {}
    buf: list[str] = []
    buf_start_line = base_line
    lineno = base_line
    in_string: str | None = None
    escape = False

    def flush_declarations(text_chunk: str, chunk_start_line: int) -> list[tuple[str, str, int, str]]:
        out: list[tuple[str, str, int, str]] = []
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
            if prop.startswith("--"):
                continue
            out.append((prop, m.group("value"), piece_line, re.sub(r"\s+", " ", stripped)))
        return out

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
                current_decls.setdefault(len(stack) - 1, []).extend(
                    flush_declarations(prefix, buf_start_line)
                )
                header = nested_sel.strip()
            is_rm = bool(re.search(r"prefers-reduced-motion\s*:\s*reduce", header, re.I))
            is_fc = bool(re.search(r"forced-colors\s*:\s*active", header, re.I))
            parent_rm = stack[-1][1] if stack else False
            parent_fc = stack[-1][2] if stack else False
            stack.append((header, parent_rm or is_rm, parent_fc or is_fc, lineno))
            current_decls[len(stack) - 1] = []
            buf = []
            buf_start_line = lineno
        elif ch == "}":
            body = "".join(buf)
            if stack:
                idx = len(stack) - 1
                sel, in_rm, in_fc, sel_line = stack.pop()
                decls = current_decls.pop(idx, []) + flush_declarations(body, buf_start_line)
                if sel and not sel.startswith("@") and decls:
                    rules.append(RuleBlock(sel, sel_line, in_rm, decls, in_fc))
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
        cx.add("MD3E001", "error",
               f"Hardcoded colour {hit.group(0)}.",
               "Use a colour role, e.g. var(--md-sys-color-primary) or "
               "var(--md-sys-color-surface-container-high). Roles carry "
               "light/dark and contrast behaviour; hex does not.",
               cx.path, lineno, line)


def check_func_color(cx, value, lineno, line) -> None:
    if cx.token_file:
        return
    m = FUNC_COLOR_RE.search(value)
    if m:
        cx.add("MD3E002", "error",
               f"Hardcoded colour via {m.group(0).strip()[:-1]}(...).",
               "Use a colour role token. A state layer is an overlay in "
               "the content's on-colour at 0.08 hover / 0.10 focus / "
               "0.10 pressed / 0.16 dragged, not a bespoke rgba().",
               cx.path, lineno, line)


def check_color_mix(cx, value, lineno, line) -> None:
    if "color-mix(" not in value.lower() and not re.search(r"color-mix\s*\(", value, re.I):
        return
    # Extract argument lists of color-mix(...)
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
            sev = "error" if getattr(cx, "mode", "strict") == "desktop-bento" else "warn"
            cx.add("MD3E018", sev,
                   "color-mix(in oklch, ...) on neutral or surface colours can trigger Chromium's powerless-hue reddish shift.",
                   "Use `color-mix(in oklab, ...)` when tinting or mixing neutral, surface, outline, shadow, or `currentColor` values.",
                   cx.path, lineno, line)


def check_radius(cx, prop, value, lineno, line) -> None:
    if prop not in RADIUS_PROPS or is_var(value) or "inherit" in value:
        return
    if "50%" in value:
        cx.add("MD3E011", "warn",
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
            cx.add("MD3E003", "error",
                   f"Corner radius {px:g}px is not on the MD3E shape scale.",
                   "Use one of the ten steps: none 0 / extra-small 4 / small 8 / "
                   "medium 12 / large 16 / large-increased 20 / extra-large 28 / "
                   "extra-large-increased 32 / extra-extra-large 48 / full.",
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
            cx.add("MD3E007", "warn",
                   f"font-size {px:g}px is not on the M3 type scale.",
                   "Use var(--md-sys-typescale-<role>-size). The scale is "
                   "11 / 12 / 14 / 16 / 22 / 24 / 28 / 32 / 36 / 45 / 57.",
                   cx.path, lineno, line)
        return
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*rem", clean_val)
    if m and round(float(m.group(1)), 5) not in TYPE_SCALE_REM:
        cx.add("MD3E007", "warn",
               f"font-size {m.group(1)}rem is not on the M3 type scale.",
               "Use var(--md-sys-typescale-<role>-size).", cx.path, lineno, line)


def check_motion(cx, prop, value, lineno, line, in_reduced_motion: bool = False) -> None:
    if prop not in MOTION_PROPS:
        return

    # MD3E019: Composite spring token inside `animation:` shorthand alongside an explicit duration
    if prop == "animation" and COMPOSITE_SPRING_VAR_RE.search(value) and TIME_RE.search(value):
        cx.add("MD3E019", "warn",
               "Composite motion token used inside `animation:` shorthand with an explicit duration.",
               "Composite --md-sys-motion-<speed>-<type> tokens include a duration, so CSS "
               "parses the second time as animation-delay. Use the easing-only token "
               "var(--md-sys-motion-<speed>-<type>-easing) instead.",
               cx.path, lineno, line)

    segments = split_top_level_commas(strip_important(value))
    for seg in segments:
        if is_var(seg):
            continue

        stripped = seg.strip()
        if in_reduced_motion and (stripped in ("none", "0s", "0ms") or re.fullmatch(r"0m?s\s+linear", stripped)):
            continue
        if stripped in ("none", "inherit", "unset"):
            continue

        # Check if every cubic-bezier in the segment matches official M3E Web curves
        beziers = [re.sub(r"\s+", "", b.group(0)) for b in CUBIC_BEZIER_CALL_RE.finditer(seg)]
        if beziers and all(b in OFFICIAL_WEB_CURVES for b in beziers) and not EASING_KEYWORD_RE.search(seg):
            cx.add("MD3E004", "info",
                   "Motion uses an official M3E Web cubic-bezier curve directly.",
                   "Prefer var(--md-sys-motion-<speed>-<type>) so motion scheme "
                   "switching and prefers-reduced-motion stay centralised.",
                   cx.path, lineno, line)
            return

        has_time = bool(TIME_RE.search(seg))
        has_easing = bool(EASING_KEYWORD_RE.search(seg) or CURVE_FUNC_RE.search(seg))
        if not (has_time or has_easing):
            continue
        cx.add("MD3E004", "error",
               "Motion uses hand-written duration/easing instead of a spring token.",
               "M3E replaces ad-hoc duration + easing with motion springs. Use "
               "var(--md-sys-motion-default-spatial) for movement/shape, or "
               "var(--md-sys-motion-fast-effects) for colour/opacity.",
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
    if getattr(cx, "mode", "strict") != "desktop-bento" or cx.token_file or in_forced_colors:
        return
    clean_v = strip_important(value).lower()
    if prop in BORDER_PROPS:
        if re.search(r"\b1px\b", clean_v) and "transparent" not in clean_v and clean_v not in ("none", "0", "0px"):
            cx.add(
                "MD3E101", "error",
                f"1px border (`{prop}`) violates borderless Desktop Bento tonal nesting.",
                "Remove card/container borders and express depth with 4+ `--md-sys-color-surface-container-*` luminance tiers (keep borders only inside `@media (forced-colors: active)`).",
                cx.path, lineno, line,
            )
    elif prop == "box-shadow" and clean_v not in ("none", "inherit", "unset", ""):
        cx.add(
            "MD3E101", "error",
            "Rectangular `box-shadow` used on Desktop Bento container.",
            "Replace rectangular `box-shadow` with `surface-container-*` tonal steps, or use wrapper `filter: drop-shadow(...)` for non-rectangular shapes.",
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
               "(2px solid var(--md-sys-color-secondary) with 2px offset) or "
               "`outline: 2px solid transparent` inside a :focus-within container.",
               cx.path, lineno, line)
    if (prop == "transition-property" and re.search(r"\ball\b", value)) or (
        prop == "transition" and re.search(r"(?:^|,)\s*all\b", value)
    ):
        cx.add("MD3E013", "warn",
               "`transition: all` animates properties you did not intend, "
               "including layout-affecting ones.",
               "Name the property and pair it with a spring token, e.g. "
               "`transform var(--md-sys-motion-default-spatial)`.",
               cx.path, lineno, line)


# ===========================================================================
# Checker engine
# ===========================================================================

class Checker:
    def __init__(self, path: pathlib.Path, *, is_snippet: bool = False, mode: str = "strict") -> None:
        self.path_obj = path
        self.path = str(path)
        self.ext = path.suffix.lower()
        self.token_file = is_token_file(path)
        self.is_snippet = is_snippet
        self.mode = mode
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
                if (has_48_dim and has_48_width) or (has_48_dim and has_inset_expand) or "inset" in decl_map and "-" in decl_map.get("inset", ""):
                    covered.add(normalize_selector_base(s))
        return covered

    def _audit_rule_block(self, rule: RuleBlock, hit_covered: set[str], morphing_bases: set[str]) -> bool:
        has_motion = False
        is_shape_rule = bool(SHAPE_SELECTOR_RE.search(rule.selector)) or any(
            (p in ("mask-image", "-webkit-mask-image") and strip_important(v).lower() != "none")
            or (p == "clip-path" and bool(re.search(r"\b(?:polygon|path|url)\s*\(", v, re.I)))
            for p, v, _, _ in rule.declarations
        )
        for prop, value, lineno, raw in rule.declarations:
            check_hex(self, value, lineno, raw)
            check_func_color(self, value, lineno, raw)
            check_color_mix(self, value, lineno, raw)
            check_radius(self, prop, value, lineno, raw)
            check_font_size(self, prop, value, lineno, raw)
            check_motion(self, prop, value, lineno, raw, in_reduced_motion=rule.in_reduced_motion)
            if is_shape_rule and prop == "box-shadow" and strip_important(value).lower() not in ("none", "inherit", "unset", ""):
                self.add(
                    "MD3E023",
                    "error" if self.mode == "desktop-bento" else "warn",
                    "Rectangular `box-shadow` applied directly on a non-rectangular masked/morphing shape.",
                    "Remove `box-shadow` and apply `filter: drop-shadow(...)` on a parent wrapper (e.g. `.md3e-shape-shadow-wrap`).",
                    self.path, lineno, raw,
                )
            else:
                check_shadow(self, prop, value, lineno, raw)
                check_bento_decl(self, prop, value, lineno, raw, in_forced_colors=rule.in_forced_colors)
            check_misc(self, prop, value, lineno, raw)

            if prop in MOTION_PROPS and (
                TIME_RE.search(value)
                or "var(--md-sys-motion-" in value
                or "var(--md-bento-motion-" in value
            ):
                has_motion = True

        # Check 9999px radius on a rule whose base selector transitions border-radius
        if not self.token_file:
            rule_bases = {re.split(r"[:\[]", s.strip())[0].strip() for s in rule.selector.split(",")}
            if any(rb == mb or rb.startswith(mb + ".") for rb in rule_bases for mb in morphing_bases):
                for prop, value, lineno, raw in rule.declarations:
                    if prop in RADIUS_PROPS and FULL_RADIUS_VALUE_RE.search(value):
                        self.add(
                            "MD3E019",
                            "error" if self.mode == "desktop-bento" else "warn",
                            "`border-radius: var(--md-sys-shape-corner-full)` (9999px) snaps or flashes a `0px` "
                            "sharp rectangle under spring overshoot (`> 1.0`) when animated.",
                            "Use a bounded `height / 2` radius (e.g. `20px` `--md-sys-shape-corner-large-increased` on "
                            "40px controls, `24px`, or `calc(var(--md-bento-control-height, 48px) / 2)`) so underdamped "
                            "springs never drive `border-radius` negative and clamp to `0px`.",
                            self.path, lineno, raw,
                        )

        # Touch target & visual height inflation checks (MD3E006)
        if not self.token_file:
            self._check_rule_touch_target(rule, hit_covered)

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
        if self.mode == "desktop-bento" and all(DENSE_ROW_SELECTOR_RE.search(s) for s in interactive):
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
            mh_is_48 = (mh_px is not None and mh_px >= MIN_TOUCH_TARGET) or "var(--md-sys-touch-target-min)" in min_h_val[0]
            if h_px is not None and h_px < MIN_TOUCH_TARGET and mh_is_48:
                self.add(
                    "MD3E006", "warn",
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
                    if px >= MIN_TOUCH_TARGET:
                        has_48_guard = True
                    elif small_hit is None:
                        small_hit = (px, ln, raw)
            if small_hit and not has_48_guard:
                px, ln, raw = small_hit
                self.add(
                    "MD3E006", "warn",
                    f"Interactive element is {px:g}px on one axis; the minimum touch target is {MIN_TOUCH_TARGET:g}px.",
                    "Keep the visual element small if intended (32px/40px) and preserve a 48px "
                    "hit area via `::before`, or use `min-height: var(--md-sys-touch-target-min)`.",
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

    def audit_css(self, css_text: str, base_line: int = 1, *, check_file_rules: bool = True, linked_motion_css: bool = False, has_reduced_transparency_doc: bool = False) -> None:
        cleaned_css = strip_css_comments(css_text)
        self._check_ms_font_axes(cleaned_css, base_line=base_line)
        rules = parse_css_rules(css_text, base_line=base_line)
        hit_covered = self._collect_hit_area_selectors(rules)

        # Collect selectors that transition border-radius
        morphing_bases: set[str] = set()
        for rule in rules:
            for prop, value, _, _ in rule.declarations:
                if prop in ("transition", "transition-property") and any(
                    k in value for k in ("border-radius", "border-start", "border-end", "border-top", "border-bottom")
                ):
                    for s in rule.selector.split(","):
                        morphing_bases.add(re.split(r"[:\[]", s.strip())[0].strip())

        has_motion = False
        has_keyframes = bool(re.search(r"@keyframes\b", cleaned_css))
        has_reduced_transparency = has_reduced_transparency_doc or bool(
            re.search(r"prefers-reduced-transparency\s*:\s*reduce\b", cleaned_css, re.I)
        )
        blur_hit: tuple[int, str] | None = None
        for rule in rules:
            if self._audit_rule_block(rule, hit_covered, morphing_bases):
                has_motion = True
            if blur_hit is None:
                for prop, value, lineno, raw in rule.declarations:
                    if prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in value:
                        blur_hit = (lineno, raw)
                        break

        if blur_hit and not has_reduced_transparency:
            self.add(
                "MD3E022", "warn",
                "`backdrop-filter: blur(...)` used without a `@media (prefers-reduced-transparency: reduce)` fallback.",
                "Prefer opaque tonal `surface-container-*` elevation first, or use `.md3e-blur-surface` / pair blur with `color-mix(in oklab, ...)` and `@media (prefers-reduced-transparency: reduce)`.",
                self.path, blur_hit[0], blur_hit[1],
            )

        if not check_file_rules:
            return

        has_hover = ":hover" in cleaned_css
        has_focus_visible = ":focus-visible" in cleaned_css
        has_reduced = "prefers-reduced-motion" in cleaned_css
        has_dark = ("prefers-color-scheme" in cleaned_css or "data-theme" in cleaned_css)

        if has_hover and not has_focus_visible:
            self.add(
                "MD3E005", "warn",
                "Stylesheet styles :hover states but defines no :focus-visible.",
                "Add `:focus-visible { outline: 2px solid var(--md-sys-color-secondary); outline-offset: 2px; }`.",
                self.path, 0, "",
            )

        if (has_keyframes or (has_motion and not linked_motion_css)) and not has_reduced and not self.token_file:
            self.add(
                "MD3E008", "warn",
                "Motion defined without a prefers-reduced-motion path.",
                "Include `@media (prefers-reduced-motion: reduce)` (or link `md3e-motion.css` "
                "for token-only transitions and guard custom `@keyframes`).",
                self.path, 0, "",
            )

        role_defs = len(re.findall(r"--md-sys-color-[a-z-]+\s*:", cleaned_css))
        if role_defs >= 5 and not has_dark and not self.token_file:
            self.add(
                "MD3E009", "warn",
                f"{role_defs} colour roles defined without a dark scheme.",
                'Redefine the roles under `[data-theme="dark"]` and `@media (prefers-color-scheme: dark)`.',
                self.path, 0, "",
            )

    def _audit_desktop_bento_document(self, text: str, combined_css: str, markup_only: str) -> None:
        if self.mode != "desktop-bento" or self.is_snippet or self.token_file:
            return
        is_full_doc = bool(re.search(r"<!doctype\s+html|<html\b", text, re.I))
        if not is_full_doc:
            return

        surface_tiers = set(
            re.findall(
                r"--md-sys-color-surface-container(?:-(?:lowest|low|high|highest))?\b",
                combined_css,
            )
        )
        if len(surface_tiers) < 4:
            self.add(
                "MD3E102", "error",
                f"Desktop Bento document uses only {len(surface_tiers)} `surface-container-*` tier(s) (minimum 4 required for borderless depth).",
                "Layer at least 4 distinct luminance tokens (`surface-container-lowest`, `-low`, `surface-container`, `-high`, `-highest`).",
                self.path, 1, "",
            )

        has_outer = bool(re.search(r"--md-sys-shape-corner-extra-large\b|\b28px\b", combined_css))
        has_inner = bool(re.search(r"--md-sys-shape-corner-large\b|\b16px\b", combined_css))
        if not (has_outer and has_inner):
            self.add(
                "MD3E103", "warn",
                "Desktop Bento document is missing concentric outer (`corner-extra-large` 28px) / inner (`corner-large` 16px) corner radii.",
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
                "MD3E104", "warn",
                "Desktop Bento Hero card is missing required expressive anchors (morphing shape CTA with `drop-shadow()`, wave + sparkline SVG, or `>=3x` Display KPI).",
                "Include a Hero Bento card with decorative wave backdrop, edge-bleed sparkline SVG, `md3e-morph.js` CTA (`filter: drop-shadow()`), and `display-large`/`display-medium` KPI.",
                self.path, 1, "",
            )

    def audit_markup_document(self, text: str) -> None:
        linked_motion_css = bool(re.search(r"md3e-motion\.css", text))
        # 1. Audit all <style> blocks using full CSS parser
        style_blocks = extract_style_blocks(text)
        combined_css = strip_css_comments("\n".join(blk for blk, _ in style_blocks))
        has_rt_doc = bool(re.search(r"prefers-reduced-transparency\s*:\s*reduce\b", combined_css, re.I))
        for blk, start_line in style_blocks:
            self.audit_css(
                blk,
                base_line=start_line,
                check_file_rules=False,
                linked_motion_css=linked_motion_css,
                has_reduced_transparency_doc=has_rt_doc,
            )

        if not self.is_snippet and style_blocks:
            has_hover = ":hover" in combined_css
            has_focus_visible = ":focus-visible" in combined_css
            has_reduced = "prefers-reduced-motion" in combined_css
            has_keyframes = "@keyframes" in combined_css
            has_motion_decl = bool(re.search(r"(?:transition|animation)[^;]*(?:var\(--md-sys-motion-|\d+m?s)", combined_css))
            if has_hover and not has_focus_visible:
                self.add(
                    "MD3E005", "warn",
                    "Document styles :hover states without :focus-visible.",
                    "Add `:focus-visible` indicator styling for keyboard users.",
                    self.path, 0, "",
                )
            if (has_keyframes or (has_motion_decl and not linked_motion_css)) and not has_reduced:
                self.add(
                    "MD3E008", "warn",
                    "Custom motion/keyframes defined without a prefers-reduced-motion path.",
                    "Add `@media (prefers-reduced-motion: reduce)` handling.",
                    self.path, 0, "",
                )

        # 2. Inline style="..." checks outside <script>/<style>
        markup_only = strip_tag_blocks(strip_tag_blocks(text, "script"), "style")
        lines = markup_only.splitlines()
        for i, line in enumerate(lines, start=1):
            for sm in STYLE_ATTR_RE.finditer(line):
                style_val = sm.group(1) if sm.group(1) is not None else sm.group(2)
                for prop, val in iter_inline_declarations(style_val):
                    check_hex(self, val, i, line)
                    check_func_color(self, val, i, line)
                    check_color_mix(self, val, i, line)
                    check_radius(self, prop, val, i, line)
                    check_font_size(self, prop, val, i, line)
                    check_motion(self, prop, val, i, line)
                    check_shadow(self, prop, val, i, line)
                    check_bento_decl(self, prop, val, i, line)
                    check_misc(self, prop, val, i, line)
                    if not self.token_file and prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in val:
                        self.add(
                            "MD3E022", "warn",
                            "Inline `backdrop-filter: blur(...)` cannot honour `prefers-reduced-transparency: reduce`.",
                            "Move frosted glass styles to `.md3e-blur-surface` or CSS with `@media (prefers-reduced-transparency: reduce)`.",
                            self.path, i, line,
                        )

        # 3. HTML component, icon, tag, accessibility & desktop-bento structural checks
        self._audit_desktop_bento_document(text, combined_css, markup_only)
        self._audit_html_semantics(markup_only, full_text=text)

    def _audit_html_semantics(self, markup_only: str, *, full_text: str) -> None:
        markup_clean = strip_html_comments(markup_only)
        lines = markup_clean.splitlines()

        # Check full document Material Symbols font link (MD3E017)
        is_full_doc = (
            not self.is_snippet
            and bool(re.search(r"<!doctype\s+html|<html\b", full_text, re.I))
        )
        uses_ligature_icons = (
            bool(re.search(r"\bmaterial-symbols-(?:outlined|rounded|sharp)\b", markup_clean))
            or bool(re.search(r"<md-icon\b[^>]*>\s*[a-z0-9_ -]+\s*</md-icon>", markup_clean, re.I))
        )
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
            if re.search(r"<md-fab[^>]*\bsize\s*=\s*[\"']small[\"']", line, re.I) or re.search(r"\b(fab[-_]small|small[-_]fab)\b", line, re.I):
                self.add(
                    "MD3E016", "warn",
                    "Small FAB (40dp) is deprecated in MD3E.",
                    "Use Standard FAB (56dp) or Medium FAB (80dp, corner 20dp).",
                    self.path, i, line,
                )

        # Check mismatched or unclosed <md-*> tags across the markup (MD3E020)
        tag_stack: list[tuple[str, int]] = []
        for m in MD_TAG_RE.finditer(markup_clean):
            is_close = m.group(1) == "/"
            tag_name = m.group(2).lower()
            attrs = m.group(3)
            ln = markup_clean[:m.start()].count("\n") + 1
            if not is_close:
                if not attrs.rstrip().endswith("/"):
                    tag_stack.append((tag_name, ln))
            else:
                if not tag_stack:
                    self.add(
                        "MD3E020", "error",
                        f"Unexpected closing tag </{tag_name}> with no matching open tag.",
                        "Match opening and closing <md-*> Web Component tags.",
                        self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
                    )
                elif tag_stack[-1][0] != tag_name:
                    open_tag, open_ln = tag_stack[-1]
                    self.add(
                        "MD3E020", "error",
                        f"Mismatched closing tag </{tag_name}> for <{open_tag}> opened on line {open_ln}.",
                        f"Replace </{tag_name}> with </{open_tag}> so subsequent elements are not swallowed.",
                        self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
                    )
                    tag_stack.pop()
                else:
                    tag_stack.pop()
        for open_tag, open_ln in tag_stack:
            self.add(
                "MD3E020", "error",
                f"Unclosed <{open_tag}> custom element tag opened on line {open_ln}.",
                f"Close <{open_tag}> with </{open_tag}> (or self-close with `/>`).",
                self.path, open_ln, lines[open_ln - 1] if open_ln - 1 < len(lines) else "",
            )

        # Check decorative icons inside buttons/links missing aria-hidden="true" (MD3E021)
        # and icon-only controls missing accessible names (MD3E014).
        reported_a11y_lines: set[int] = set()
        ctrl_re = re.compile(
            rf"<(button|a|md-filled-button|md-filled-tonal-button|md-outlined-button|"
            rf"md-elevated-button|md-text-button|md-icon-button|md-filled-icon-button|"
            rf"md-filled-tonal-icon-button|md-outlined-icon-button|md-fab|md-extended-fab)\b({TAG_ATTRS_PAT})>([\s\S]*?)</\1>",
            re.IGNORECASE,
        )
        for m in ctrl_re.finditer(markup_clean):
            tag = m.group(1).lower()
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
            inner_no_icons = re.sub(r"<md-icon\b[^>]*>[^<]*</md-icon>", "", inner_no_icons, flags=re.I)
            inner_no_icons = re.sub(r"<svg\b[\s\S]*?</svg>", "", inner_no_icons, flags=re.I)
            has_visible_text = bool(re.sub(r"<[^>]+>", "", inner_no_icons).strip())
            has_img_alt = bool(re.search(r'<img\b[^>]*\balt\s*=\s*(?:"[^"]*\S[^"]*"|\'[^\']*\S[^\']*\')', inner, re.I))
            has_svg_title = bool(re.search(r"<svg\b[^>]*>[\s\S]*?<title\b[^>]*>[^<]+</title>", inner, re.I))
            icon_matches = iter_icon_matches(inner)
            has_icon_child = bool(icon_matches or re.search(r"<(?:svg|img)\b", inner, re.I))
            is_icon_only_tag = tag in (
                "md-icon-button", "md-filled-icon-button",
                "md-filled-tonal-icon-button", "md-outlined-icon-button", "md-fab",
            )
            if (
                not has_ctrl_label
                and not has_visible_text
                and not has_img_alt
                and not has_svg_title
                and (has_icon_child or is_icon_only_tag)
                and ctrl_line not in reported_a11y_lines
            ):
                reported_a11y_lines.add(ctrl_line)
                self.add(
                    "MD3E014", "warn",
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
                        "MD3E021", "warn",
                        "Decorative Material Symbols icon inside a labelled control is missing `aria-hidden=\"true\"`.",
                        "Add `aria-hidden=\"true\"` to the icon element so screen readers do not read the raw ligature name.",
                        self.path, ln, lines[ln - 1] if ln - 1 < len(lines) else "",
                    )

    def audit_generic_code(self, text: str) -> None:
        # Handle JSX/TSX/JS/TS lines + HTML-like snippets cleanly
        lines = text.splitlines()
        selector = ""
        depth = 0
        for i, raw in enumerate(lines, start=1):
            # Also check inline style="..." in JSX/PHP templates
            for sm in STYLE_ATTR_RE.finditer(raw):
                style_val = sm.group(1) if sm.group(1) is not None else sm.group(2)
                for prop, val in iter_inline_declarations(style_val):
                    check_hex(self, val, i, raw)
                    check_func_color(self, val, i, raw)
                    check_color_mix(self, val, i, raw)
                    check_radius(self, prop, val, i, raw)
                    check_font_size(self, prop, val, i, raw)
                    check_motion(self, prop, val, i, raw)
                    check_shadow(self, prop, val, i, raw)
                    check_bento_decl(self, prop, val, i, raw)
                    check_misc(self, prop, val, i, raw)
                    if not self.token_file and prop in ("backdrop-filter", "-webkit-backdrop-filter") and "blur(" in val:
                        self.add(
                            "MD3E022", "warn",
                            "Inline `backdrop-filter: blur(...)` cannot honour `prefers-reduced-transparency: reduce`.",
                            "Move frosted glass styles to `.md3e-frosted-surface` or CSS with `@media (prefers-reduced-transparency: reduce)`.",
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
                        check_hex(self, val, i, raw)
                        check_func_color(self, val, i, raw)
                        check_color_mix(self, val, i, raw)
                        check_radius(self, prop, val, i, raw)
                        check_font_size(self, prop, val, i, raw)
                        check_motion(self, prop, val, i, raw)
                        check_shadow(self, prop, val, i, raw)
                        check_bento_decl(self, prop, val, i, raw)
                        check_misc(self, prop, val, i, raw)
            if "}" in raw:
                depth = max(0, depth - raw.count("}"))
                if depth == 0:
                    selector = ""
        self._audit_html_semantics(text, full_text=text)


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


def render_text(reports: list[FileReport], min_severity: str, scanned: int) -> None:
    counts = {s: 0 for s in SEVERITIES}
    for report in reports:
        shown = [f for f in report.findings
                 if SEVERITY_RANK[f.severity] <= SEVERITY_RANK[min_severity]]
        if not shown:
            continue
        shown.sort(key=lambda f: (SEVERITY_RANK[f.severity], f.line))
        print(f"\n\033[1m{report.path}\033[0m")
        for f in shown:
            counts[f.severity] += 1
            print(f"  [{f.severity.upper():<5}] {f.code}"
                  + (f"  line {f.line}" if f.line else ""))
            print(f"          {f.message}")
            print(f"          fix: {f.fix}")
            if f.snippet:
                print(f"          > {f.snippet}")

    verdict = "FAIL" if counts["error"] else ("WARN" if counts["warn"] else "PASS")
    print("\n" + "=" * 66)
    print(f"MD3E audit: {verdict}   {counts['error']} error, {counts['warn']} warn, "
          f"{counts['info']} info   ({scanned} file(s) scanned)")
    if not any(counts.values()):
        print("All checks passed. Nothing to fix.")
        return
    print("Fix in this order: MD3E001/002/017/018/020 errors, MD3E004 motion, "
          "MD3E005 focus, MD3E003 shape scale.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit front-end code against Material 3 Expressive rules.")
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--markdown", action="store_true",
                        help="also audit HTML/CSS fenced code blocks in .md files")
    parser.add_argument("--mode", choices=AUDIT_MODES, default="strict",
                        help="audit policy profile: strict (default) or desktop-bento")
    parser.add_argument("--exclude", default="",
                        help="comma-separated substrings to skip")
    parser.add_argument("--fail-on", choices=SEVERITIES, default="error",
                        help="severity that makes the run fail (default: error)")
    parser.add_argument("--min-severity", choices=SEVERITIES, default="info",
                        help="lowest severity to report (default: info)")
    args = parser.parse_args(argv)

    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    reports, scanned = audit(args.paths, exclude, include_markdown=args.markdown, mode=args.mode)

    if args.json:
        print(json.dumps({
            "mode": args.mode,
            "summary": {
                s: sum(1 for r in reports for f in r.findings if f.severity == s)
                for s in SEVERITIES
            },
            "files_scanned": scanned,
            "files": [
                {"path": r.path, "findings": [f.to_dict() for f in r.findings]}
                for r in reports
            ],
        }, indent=2))
    else:
        render_text(reports, args.min_severity, scanned)

    worst = min((SEVERITY_RANK[f.severity] for r in reports for f in r.findings),
                default=len(SEVERITIES))
    return 1 if worst <= SEVERITY_RANK[args.fail_on] else 0


if __name__ == "__main__":
    sys.exit(main())
