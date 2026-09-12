#!/usr/bin/env python3
"""Audit front-end code for Material 3 Expressive (MD3E) compliance.

Deterministic static checks for the rules that models and humans most often
break when "doing Material Design": hardcoded colours, off-scale corner radii,
duration/easing motion instead of springs, unfocusable controls, sub-48px
targets and type sizes that are not on the scale.

Usage
-----
    python audit_md3e.py <path>...            # files or directories
    python audit_md3e.py src --json           # machine-readable
    python audit_md3e.py src --fail-on warn   # stricter CI gate
    python audit_md3e.py src --exclude vendor,node_modules

Exit status is 1 when findings at or above the --fail-on severity exist,
otherwise 0. Token/theme files are auto-detected and exempted from the
hardcoded-colour checks, because that is exactly where raw values belong.

Finding codes
-------------
    MD3E001  hardcoded hex colour                 (error)
    MD3E002  hardcoded rgb()/hsl() colour         (error)
    MD3E003  corner radius off the shape scale    (error)
    MD3E004  duration/easing instead of a spring  (error)
    MD3E005  focus indicator removed / missing    (error)
    MD3E006  interactive target under 48px        (warn)
    MD3E007  font-size off the type scale         (warn)
    MD3E008  no prefers-reduced-motion path       (warn)
    MD3E009  colour roles without a dark scheme   (warn)
    MD3E010  box-shadow used for elevation        (info)
    MD3E011  border-radius: 50% instead of full   (warn)
    MD3E012  uppercase label text                 (info)
    MD3E013  `transition: all`                    (warn)
    MD3E014  icon-only control, no accessible name(warn)
    MD3E015  deprecated bottom app bar            (info)
    MD3E016  deprecated small FAB (40dp)          (warn)
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

CODE_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".styl",
    ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".php",
}
SKIP_DIRS = {
    "node_modules", "dist", "build", ".next", ".nuxt", "vendor",
    "coverage", ".git", ".cache", "__pycache__",
}

# --- Design system facts the checks are built on ---------------------------

# Shape corner scale: ten steps. Anything else is off-scale.
CORNER_SCALE_PX = {0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 28.0, 32.0, 48.0}
FULL_PX = {999.0, 9999.0, 1000.0}

# Type scale sizes (px). Every M3 text style resolves to one of these.
TYPE_SCALE_PX = {11.0, 12.0, 14.0, 16.0, 22.0, 24.0, 28.0, 32.0, 36.0, 45.0, 57.0}
TYPE_SCALE_REM = {round(v / 16.0, 5) for v in TYPE_SCALE_PX}

MIN_TOUCH_TARGET = 48.0

HEX_RE = re.compile(
    r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})"
    r"(?![0-9a-zA-Z_-])"
)
FUNC_COLOR_RE = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\s*\(")
TIME_RE = re.compile(r"(?<![\w-])(\d*\.?\d+)(m?s)\b")
EASING_KEYWORD_RE = re.compile(
    r"(?:^|[\s,(])(ease|ease-in|ease-out|ease-in-out|step-start|step-end)\b")
CURVE_FUNC_RE = re.compile(r"\b(cubic-bezier|steps)\s*\(")
PROP_VALUE_RE = re.compile(r"^(?P<prop>-{0,2}[a-zA-Z][\w-]*)\s*:\s*(?P<value>.*?)\s*$")

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
    r"(?:^|[\s,>+~.:#\[])(?:btn|button|icon-button|iconbutton|fab|chip|tab|tab-item"
    r"|nav-item|navitem|list-item|listitem|menu-item|menuitem|checkbox|radio"
    r"|switch|segmented|toggle|control|select|input|text-field)",
    re.IGNORECASE,
)
INTERACTIVE_ELEMENT_RE = re.compile(
    r"<(?:button|a\s|input|select|textarea|md-filled-button|md-outlined-button"
    r"|md-text-button|md-elevated-button|md-filled-tonal-button|md-icon-button"
    r"|md-fab|md-extended-fab|md-checkbox|md-radio|md-switch|md-chip-set)",
    re.IGNORECASE,
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


# ===========================================================================
# Parsing helpers
# ===========================================================================

def is_token_file(path: pathlib.Path) -> bool:
    name = path.name.lower()
    posix = str(path).replace("\\", "/").lower()
    return any(h in name for h in TOKEN_FILE_HINTS) or "/tokens/" in posix


def looks_like_selector_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith(("/*", "*", "//", "}")):
        return False
    if ":" not in stripped:
        return True
    # `color: red` is a declaration; `.foo:hover {` is a selector.
    head = stripped.split(":", 1)[0]
    return not re.fullmatch(r"-{0,2}[a-zA-Z][\w-]*", head.strip())


def iter_declarations(line: str):
    """Yield (prop, value) for every declaration on a line.

    Handles both one-per-line stylesheets and minified one-liners such as
    `.btn { height: 36px; font-size: 13px; }`, which a naive single-match
    parser silently under-reports.
    """
    if looks_like_selector_line(line):
        if "{" in line:
            line = line.split("{", 1)[1]
            if "}" in line:
                line = line.rsplit("}", 1)[0]
        else:
            return
    for piece in line.split(";"):
        piece = piece.strip()
        if not piece or piece.startswith(("/*", "//", "*")):
            continue
        m = PROP_VALUE_RE.match(piece)
        if not m:
            continue
        prop = m.group("prop").lower()
        if prop.startswith("--"):
            continue            # token definition: raw values belong here
        yield prop, m.group("value")


def parse_px(value: str) -> float | None:
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*px", value.strip())
    return float(m.group(1)) if m else None


def is_var(value: str) -> bool:
    return "var(" in value


# ===========================================================================
# Declaration-level checks
# ===========================================================================

def check_radius(cx, prop, value, path, lineno, line) -> None:
    if prop not in RADIUS_PROPS:
        return
    if is_var(value) or "inherit" in value:
        return
    if "50%" in value:
        cx.add("MD3E011", "warn",
               "`border-radius: 50%` is the pre-M3 roundedness hack. The shape "
               "scale names this value.",
               "Use var(--md-sys-shape-corner-full).", path, lineno, line)
        return
    for slash_group in value.split("/"):
        for part in slash_group.strip().split():
            px = parse_px(part)
            if px is None or px in CORNER_SCALE_PX or px in FULL_PX:
                continue
            if 0 < px <= 2:
                continue        # hairline helper, not a shape statement
            cx.add("MD3E003", "error",
                   f"Corner radius {px:g}px is not on the MD3E shape scale.",
                   "Use one of the ten steps: none 0 / extra-small 4 / small 8 / "
                   "medium 12 / large 16 / large-increased 20 / extra-large 28 / "
                   "extra-large-increased 32 / extra-extra-large 48 / full.",
                   path, lineno, line)


def check_font_size(cx, prop, value, path, lineno, line) -> None:
    if prop != "font-size" or is_var(value):
        return
    if any(fn in value for fn in ("calc(", "clamp(", "min(", "max(")) or "%" in value:
        return
    px = parse_px(value)
    if px is not None:
        if px not in TYPE_SCALE_PX:
            cx.add("MD3E007", "warn",
                   f"font-size {px:g}px is not on the M3 type scale.",
                   "Use var(--md-sys-typescale-<role>-size). The scale is "
                   "11 / 12 / 14 / 16 / 22 / 24 / 28 / 32 / 36 / 45 / 57.",
                   path, lineno, line)
        return
    m = re.fullmatch(r"(-?\d*\.?\d+)\s*rem", value.strip())
    if m and round(float(m.group(1)), 5) not in TYPE_SCALE_REM:
        cx.add("MD3E007", "warn",
               f"font-size {m.group(1)}rem is not on the M3 type scale.",
               "Use var(--md-sys-typescale-<role>-size).", path, lineno, line)


def check_motion(cx, prop, value, path, lineno, line) -> None:
    if prop not in MOTION_PROPS or is_var(value):
        return
    has_time = bool(TIME_RE.search(value))
    has_easing = bool(EASING_KEYWORD_RE.search(value) or CURVE_FUNC_RE.search(value))
    if not (has_time or has_easing):
        return
    cx.add("MD3E004", "error",
           "Motion uses hand-written duration/easing instead of a spring token.",
           "M3E replaces duration + easing with motion springs. Use "
           "var(--md-sys-motion-default-spatial) for position, size, rotation "
           "and corner radius, or var(--md-sys-motion-fast-effects) for colour "
           "and opacity. Regenerate assets/tokens/md3e-motion.css with "
           "scripts/spring_to_css.py if those tokens are missing.",
           path, lineno, line)


def check_touch_target(cx, selector, prop, value, path, lineno, line) -> None:
    if prop not in ("height", "width", "min-height", "min-width", "max-height"):
        return
    if not selector or not INTERACTIVE_SELECTOR_RE.search(selector) or is_var(value):
        return
    px = parse_px(value)
    if px is None or px >= MIN_TOUCH_TARGET:
        return
    cx.add("MD3E006", "warn",
           f"Interactive element is {px:g}px on one axis; the minimum touch "
           f"target is {MIN_TOUCH_TARGET:g}px.",
           "Keep the visual element small but preserve a 48px hit area: "
           "min-height: var(--md-sys-touch-target-min) plus padding, or a "
           "::before overlay.", path, lineno, line)


def check_shadow(cx, prop, value, path, lineno, line) -> None:
    if prop != "box-shadow" or value.strip() in ("none", "inherit", "unset"):
        return
    if not is_var(value) or "rgba(" in value:
        cx.add("MD3E010", "info",
               "box-shadow used to express depth.",
               "M3 expresses elevation with tonal surface colour "
               "(var(--md-sys-color-surface-container-*)). Shadows are a "
               "fallback for legibility: var(--md-sys-elevation-level1..5).",
               path, lineno, line)


class Checker:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = str(path)
        self.token_file = is_token_file(path)
        self.findings: list[Finding] = []

    def add(self, code, severity, message, fix, path, line, snippet="") -> None:
        self.findings.append(Finding(code, severity, message, fix, path, line,
                                     snippet.strip()[:140]))

    def run(self, text: str) -> list[Finding]:
        self.check_line_based(text.splitlines())
        self.check_file_level(text, text.splitlines())
        return self.findings

    def check_line_based(self, lines: list[str]) -> None:
        selector = ""
        depth = 0
        for i, raw in enumerate(lines, start=1):
            if "{" in raw:
                candidate = raw.split("{", 1)[0].strip()
                if candidate and not candidate.startswith("@"):
                    selector = candidate
                depth += 1
            for prop, value in iter_declarations(raw):
                self.check_hex(value, i, raw)
                self.check_func_color(value, i, raw)
                check_radius(self, prop, value, self.path, i, raw)
                check_font_size(self, prop, value, self.path, i, raw)
                check_motion(self, prop, value, self.path, i, raw)
                check_touch_target(self, selector, prop, value, self.path, i, raw)
                check_shadow(self, prop, value, self.path, i, raw)
                self.check_misc(prop, value, i, raw)
            if "}" in raw:
                depth = max(0, depth - raw.count("}"))
                if depth == 0:
                    selector = ""

    def check_hex(self, value, lineno, line) -> None:
        if self.token_file:
            return
        hit = HEX_RE.search(value)
        if hit:
            self.add("MD3E001", "error",
                     f"Hardcoded colour {hit.group(0)}.",
                     "Use a colour role, e.g. var(--md-sys-color-primary) or "
                     "var(--md-sys-color-surface-container-high). Roles carry "
                     "light/dark and contrast behaviour; hex does not.",
                     self.path, lineno, line)

    def check_func_color(self, value, lineno, line) -> None:
        if self.token_file:
            return
        m = FUNC_COLOR_RE.search(value)
        if m:
            self.add("MD3E002", "error",
                     f"Hardcoded colour via {m.group(0).strip()[:-1]}(...).",
                     "Use a colour role token. A state layer is an overlay in "
                     "the content's on-colour at 0.08 hover / 0.10 focus / "
                     "0.10 pressed / 0.16 dragged, not a bespoke rgba().",
                     self.path, lineno, line)

    def check_misc(self, prop, value, lineno, line) -> None:
        if prop == "text-transform" and "uppercase" in value:
            self.add("MD3E012", "info",
                     "Uppercase label text.",
                     "M3 uses sentence case for buttons, labels and tabs. "
                     "Uppercasing was an M2 convention.",
                     self.path, lineno, line)
        if prop in ("outline", "outline-width") and value.strip() in ("none", "0", "0px"):
            self.add("MD3E005", "error",
                     "Focus outline removed.",
                     "Keyboard users lose all positional feedback. Replace it "
                     "with an inset focus ring: 2px solid "
                     "var(--md-sys-color-secondary) and a 2px gap, applied on "
                     ":focus-visible.",
                     self.path, lineno, line)
        if prop == "transition" and value.strip().startswith("all"):
            self.add("MD3E013", "warn",
                     "`transition: all` animates properties you did not intend, "
                     "including layout-affecting ones.",
                     "Name the property and pair it with a spring token, e.g. "
                     "`transform var(--md-sys-motion-default-spatial)`.",
                     self.path, lineno, line)

    def check_file_level(self, text: str, lines: list[str]) -> None:
        has_hover = ":hover" in text or "onMouseEnter" in text
        has_focus_visible = ":focus-visible" in text or "focusVisible" in text
        has_reduced = "prefers-reduced-motion" in text
        has_dark = (text.count("prefers-color-scheme") > 0 or "data-theme" in text)

        has_motion = False
        for line in lines:
            for prop, value in iter_declarations(line):
                if prop in MOTION_PROPS and TIME_RE.search(value):
                    has_motion = True
                    break
            if has_motion:
                break

        is_stylesheet = self.path.lower().endswith((".css", ".scss", ".less", ".sass"))

        if has_hover and not has_focus_visible:
            self.add("MD3E005", "warn",
                     "File styles hover states but defines no :focus-visible.",
                     "Every interactive element needs a focus indicator of the "
                     "same quality as its hover state: :focus-visible { outline: "
                     "2px solid var(--md-sys-color-secondary); outline-offset: "
                     "2px; } or an inset ring.", self.path, 0, "")

        if has_motion and not has_reduced and is_stylesheet:
            self.add("MD3E008", "warn",
                     "Motion defined without a prefers-reduced-motion path.",
                     "Wrap spring-based movement in @media "
                     "(prefers-reduced-motion: reduce) and keep only a short "
                     "cross-fade.", self.path, 0, "")

        role_defs = len(re.findall(r"--md-sys-color-[a-z-]+\s*:", text))
        if role_defs >= 5 and not has_dark and not self.token_file:
            self.add("MD3E009", "warn",
                     f"{role_defs} colour roles defined but no dark scheme.",
                     "A colour role points into a tonal palette; it is not a "
                     "fixed colour. Redefine the same roles under "
                     '[data-theme=\"dark\"] and honour prefers-color-scheme.',
                     self.path, 0, "")

        for i, line in enumerate(lines, start=1):
            if INTERACTIVE_ELEMENT_RE.search(line):
                has_label = bool(re.search(r'\b(aria-label|label)=["\']', line, re.I))
                if not has_label:
                    if re.search(r"<(?:button|md-icon-button|md-fab)[^>]*>\s*<(?:svg|img|md-icon)", line, re.I) or re.search(r"<md-icon-button\b", line, re.I):
                        self.add("MD3E014", "warn",
                                 "Icon-only control without an accessible name.",
                                 "Add aria-label, or a visually hidden span. "
                                 "Material web components need label= or aria-label.",
                                 self.path, i, line)
            if re.search(r"bottom[-_]app[-_]bar", line, re.I):
                self.add("MD3E015", "info",
                         "Bottom app bar is deprecated in M3E.",
                         "Replace with a docked toolbar, or a floating toolbar "
                         "when actions need more room or flexible placement.",
                         self.path, i, line)
            if re.search(r"<md-fab[^>]*\bsize=[\"']small[\"']", line, re.I) or re.search(r"\b(fab[-_]small|small[-_]fab)\b", line, re.I):
                self.add("MD3E016", "warn",
                         "Small FAB (40dp) is deprecated in MD3E.",
                         "Small FAB (40dp) was deprecated in M3 Expressive. "
                         "Use Standard FAB (56dp) or Medium FAB (80dp, corner 20dp).",
                         self.path, i, line)


# ===========================================================================
# Driver
# ===========================================================================

def iter_files(paths: list[str], exclude: list[str]) -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for raw in paths:
        p = pathlib.Path(raw)
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if not child.is_file() or child.suffix.lower() not in CODE_EXTENSIONS:
                    continue
                if {part.lower() for part in child.parts} & SKIP_DIRS:
                    continue
                if any(x.lower() in str(child).lower() for x in exclude):
                    continue
                out.append(child)
        else:
            print(f"warning: {raw} does not exist", file=sys.stderr)
    return out


def audit(paths: list[str], exclude: list[str]) -> tuple[list[FileReport], int]:
    files = iter_files(paths, exclude)
    reports: list[FileReport] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        findings = Checker(path).run(text)
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
    print("Fix in this order: MD3E001/002 colour roles, MD3E004 motion springs, "
          "MD3E005 focus, MD3E003 shape scale.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit front-end code against Material 3 Expressive rules.")
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--exclude", default="",
                        help="comma-separated substrings to skip")
    parser.add_argument("--fail-on", choices=SEVERITIES, default="error",
                        help="severity that makes the run fail (default: error)")
    parser.add_argument("--min-severity", choices=SEVERITIES, default="info",
                        help="lowest severity to report (default: info)")
    args = parser.parse_args(argv)

    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    reports, scanned = audit(args.paths, exclude)

    if args.json:
        print(json.dumps({
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
