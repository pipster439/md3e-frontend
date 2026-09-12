#!/usr/bin/env python3
"""Convert Material 3 Expressive spring tokens (stiffness + damping) into CSS.

The M3 Expressive motion spec publishes motion as *springs*, not as
duration/easing pairs. CSS has no spring primitive, so the faithful
translation is a sampled CSS ``linear()`` easing function:

    1. Solve the damped harmonic oscillator for a unit step response
       (mass = 1, initial velocity = 0).
    2. Find the settling time (last moment the response leaves the
       +/-0.1% tolerance band).
    3. Sample the response at that settling time and emit ``linear(...)``.
       Overshoot is preserved: ``linear()`` values above 1 are legal and
       produce the bounce that makes Expressive motion feel alive.

Official spring parameters (md.sys.motion.spring.<speed>.<type>):

    scheme      type     speed    damping   stiffness
    expressive  spatial  fast     0.60       800
    expressive  spatial  default  0.80       380
    expressive  spatial  slow     0.80       200
    expressive  effects  fast     1.00      3800
    expressive  effects  default  1.00      1600
    expressive  effects  slow     1.00       800
    standard    spatial  fast     0.90      1400
    standard    spatial  default  0.90       700
    standard    spatial  slow     0.90       300
    standard    effects  fast     1.00      3800
    standard    effects  default  1.00      1600
    standard    effects  slow     1.00       800

Effects springs are identical in both schemes: expression belongs to
movement, not to colour. Reference: https://m3.material.io/styles/motion/overview/specs

Usage
-----
    # regenerate the bundled token stylesheet
    python spring_to_css.py --emit-css ../assets/tokens/md3e-motion.css

    # convert an arbitrary custom spring
    python spring_to_css.py --stiffness 500 --damping 0.7

    # print the whole table
    python spring_to_css.py --table
"""

from __future__ import annotations

import argparse
import math
import pathlib
import sys

# (scheme, type, speed) -> (damping_ratio, stiffness)
SPRINGS: dict[tuple[str, str, str], tuple[float, float]] = {
    ("expressive", "spatial", "fast"): (0.6, 800.0),
    ("expressive", "spatial", "default"): (0.8, 380.0),
    ("expressive", "spatial", "slow"): (0.8, 200.0),
    ("expressive", "effects", "fast"): (1.0, 3800.0),
    ("expressive", "effects", "default"): (1.0, 1600.0),
    ("expressive", "effects", "slow"): (1.0, 800.0),
    ("standard", "spatial", "fast"): (0.9, 1400.0),
    ("standard", "spatial", "default"): (0.9, 700.0),
    ("standard", "spatial", "slow"): (0.9, 300.0),
    ("standard", "effects", "fast"): (1.0, 3800.0),
    ("standard", "effects", "default"): (1.0, 1600.0),
    ("standard", "effects", "slow"): (1.0, 800.0),
}

SPEEDS = ("fast", "default", "slow")
TYPES = ("spatial", "effects")

# Legacy M3 easing tokens, kept as a graceful fallback for engines without
# linear() support and for properties that must not overshoot.
LEGACY_EASINGS: dict[str, str] = {
    "linear": "cubic-bezier(0, 0, 1, 1)",
    "standard": "cubic-bezier(0.2, 0, 0, 1)",
    "standard-decelerate": "cubic-bezier(0, 0, 0, 1)",
    "standard-accelerate": "cubic-bezier(0.3, 0, 1, 1)",
    "emphasized": "cubic-bezier(0.2, 0, 0, 1)",
    "emphasized-decelerate": "cubic-bezier(0.05, 0.7, 0.1, 1)",
    "emphasized-accelerate": "cubic-bezier(0.3, 0, 0.8, 0.15)",
}

LEGACY_DURATIONS: dict[str, int] = {
    "short1": 50, "short2": 100, "short3": 150, "short4": 200,
    "medium1": 250, "medium2": 300, "medium3": 350, "medium4": 400,
    "long1": 450, "long2": 500, "long3": 550, "long4": 600,
    "extralong1": 700, "extralong2": 800, "extralong3": 900, "extralong4": 1000,
}


def spring_position(damping: float, stiffness: float, t: float) -> float:
    """Unit-step response of a damped harmonic oscillator (mass = 1).

    x(0) = 0, x'(0) = 0, target = 1. Exact closed form for all regimes.
    """
    w = math.sqrt(stiffness)          # undamped natural frequency
    z = damping

    if abs(z - 1.0) < 1e-9:           # critically damped
        return 1.0 - (1.0 + w * t) * math.exp(-w * t)

    if z < 1.0:                        # underdamped -> overshoots, bounces
        wd = w * math.sqrt(1.0 - z * z)
        return 1.0 - math.exp(-z * w * t) * (
            math.cos(wd * t) + (z * w / wd) * math.sin(wd * t)
        )

    # overdamped -> no overshoot, slow creep
    r = w * math.sqrt(z * z - 1.0)
    r1, r2 = -z * w + r, -z * w - r
    a = r2 / (r1 - r2)
    b = -r1 / (r1 - r2)
    return 1.0 + a * math.exp(r1 * t) + b * math.exp(r2 * t)


def peak_overshoot(damping: float, stiffness: float) -> float:
    """Maximum percentage by which the spring exceeds its target."""
    if damping >= 1.0:
        return 0.0
    step, t, peak = 0.0005, 0.0, 1.0
    while t <= 3.0:
        peak = max(peak, spring_position(damping, stiffness, t))
        t += step
    return (peak - 1.0) * 100.0


def settle_ms(damping: float, stiffness: float, tol: float = 0.001) -> int:
    """Milliseconds until the response stays inside the tolerance band.

    Rounded up to the nearest 10 ms, with a 20 ms tail so the final frame
    is comfortably settled rather than clipped mid-decay.
    """
    step, t, last_out = 0.0005, 0.0, 0.0
    while t <= 4.0:
        if abs(spring_position(damping, stiffness, t) - 1.0) >= tol:
            last_out = t
        t += step
    return int(math.ceil((last_out * 1000.0 + 20.0) / 10.0) * 10)


def to_linear(damping: float, stiffness: float, duration_ms: int,
              samples: int | None = None) -> str:
    """Sample the spring into a CSS ``linear()`` easing function."""
    if samples is None:
        samples = max(24, min(120, round(duration_ms / 8)))
    values = []
    for i in range(samples + 1):
        t = (duration_ms / 1000.0) * (i / samples)
        values.append(spring_position(damping, stiffness, t))
    values[0] = 0.0
    values[-1] = 1.0                       # pin the end: no residual drift
    values = [round(v, 4) for v in values]
    # Trim noise: a value within 0.0002 of its neighbour adds nothing.
    body = ", ".join(f"{v:g}" for v in values)
    return f"linear({body})"


def build_token_map() -> dict[str, dict[str, str]]:
    """scheme -> {token suffix: "linear(...)"}."""
    out: dict[str, dict[str, str]] = {s: {} for s in ("expressive", "standard")}
    for (scheme, kind, speed), (damping, stiffness) in SPRINGS.items():
        out[scheme][f"{speed}-{kind}"] = to_linear(
            damping, stiffness, settle_ms(damping, stiffness)
        )
    return out


def fallback_easing(kind: str) -> str:
    return LEGACY_EASINGS["linear"] if kind == "spatial" else LEGACY_EASINGS["standard-decelerate"]


def render_css() -> str:
    generated: dict[str, dict[str, str]] = {}
    meta: dict[str, tuple[int, float]] = {}
    for (scheme, kind, speed), (damping, stiffness) in SPRINGS.items():
        generated.setdefault(scheme, {})[f"{speed}-{kind}"] = to_linear(
            damping, stiffness, settle_ms(damping, stiffness)
        )
        meta[f"{scheme}-{speed}-{kind}"] = (
            settle_ms(damping, stiffness),
            peak_overshoot(damping, stiffness),
        )

    lines: list[str] = []
    add = lines.append
    add("/* ============================================================================")
    add(" * md3e-motion.css - Material 3 Expressive motion tokens")
    add(" *")
    add(" * GENERATED FILE - do not edit by hand.")
    add(" * Regenerate with:  python scripts/spring_to_css.py --emit-css \\")
    add(" *                       assets/tokens/md3e-motion.css")
    add(" *")
    add(" * The spec publishes motion as springs (stiffness + damping). Each token is")
    add(" * sampled into a CSS linear() easing function that preserves overshoot, so")
    add(" * the bounce that defines Expressive motion survives the trip to the web.")
    add(" *")
    add(" *   use  : transition: transform var(--md-sys-motion-default-spatial);")
    add(" *   never: transition: transform 300ms ease-in-out;")
    add(" *")
    add(" * Reference: https://m3.material.io/styles/motion/overview/specs")
    add(" * ========================================================================== */")
    add("")
    add(":root {")
    add("  /* --- Motion scheme selector -------------------------------------------")
    add("   * The scheme is applied at product level, never baked into a token name.")
    add("   * Swap the attribute to change how the whole product feels.")
    add("   *   <html data-motion-scheme=\"expressive\">  <- Material's recommendation")
    add("   *   <html data-motion-scheme=\"standard\">    <- utilitarian products")
    add("   * -------------------------------------------------------------------- */")
    add("  --md-sys-motion-scheme: expressive;")
    add("")
    add("  /* --- Legacy duration + easing tokens -----------------------------------")
    add("   * Fallback layer. Prefer the spring tokens below; use these only for")
    add("   * engines without linear() support, and never mix the two for the same")
    add("   * property (duration/easing and springs do not compose).")
    add("   * -------------------------------------------------------------------- */")
    for name, ms in LEGACY_DURATIONS.items():
        add(f"  --md-sys-motion-duration-{name}: {ms}ms;")
    add("")
    for name, curve in LEGACY_EASINGS.items():
        add(f"  --md-sys-motion-easing-{name}: {curve};")
    add("}")
    add("")

    for scheme in ("expressive", "standard"):
        label = scheme.capitalize()
        add(f"/* --- {label} motion scheme "
            + "-" * max(0, 58 - len(label)) + " */")
        add(f":root, [data-motion-scheme=\"{scheme}\"] {{"
              if scheme == "expressive" else
              f"[data-motion-scheme=\"{scheme}\"] {{")
        for kind in TYPES:
            add(f"  /* {kind}: "
                + ("position, size, rotation, corner radius - overshoots and bounces"
                   if kind == "spatial" else
                   "colour, opacity - must not overshoot") + " */")
            for speed in SPEEDS:
                add(f"  --md-sys-motion-{speed}-{kind}: "
                    f"{meta[f'{scheme}-{speed}-{kind}'][0]}ms "
                    f"{generated[scheme][f'{speed}-{kind}']};")
            add("")
        add("}")
        add("")

    add("/* --- Graceful degradation ------------------------------------------------")
    add(" * Engines without linear() fall back to the legacy curves. Motion still")
    add(" * reads correctly; it simply loses the bounce.")
    add(" * ----------------------------------------------------------------------- */")
    add("@supports not (transition-timing-function: linear(0, 1)) {")
    add("  :root {")
    for kind in TYPES:
        for speed in SPEEDS:
            add(f"    --md-sys-motion-{speed}-{kind}: "
                f"{400 if speed == 'default' else (200 if speed == 'fast' else 600)}ms "
                f"{fallback_easing(kind)};")
    add("  }")
    add("}")
    add("")
    add("/* --- Reduced motion ------------------------------------------------------")
    add(" * Honour the OS setting. Keep a short cross-fade so state changes remain")
    add(" * legible; remove every spatial spring that moves or scales the UI.")
    add(" * ----------------------------------------------------------------------- */")
    add("@media (prefers-reduced-motion: reduce) {")
    add("  :root {")
    for kind in TYPES:
        for speed in SPEEDS:
            add(f"    --md-sys-motion-{speed}-{kind}: 100ms "
                f"{'linear' if kind == 'spatial' else LEGACY_EASINGS['linear']};")
    add("  }")
    add("}")
    add("")
    add("/* --- Reference: spring parameters behind each token ----------------------")
    for scheme in ("expressive", "standard"):
        for kind in TYPES:
            for speed in SPEEDS:
                damping, stiffness = SPRINGS[(scheme, kind, speed)]
                ms, over = meta[f"{scheme}-{speed}-{kind}"]
                add(f" *  {scheme:<10} {speed:<8} {kind:<8} "
                    f"damping {damping:<4} stiffness {stiffness:<5} "
                    f"-> {ms:>4} ms, peak overshoot {over:5.1f}%")
    add(" */")
    add("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert MD3E spring tokens to CSS linear() easings.")
    parser.add_argument("--stiffness", type=float,
                        help="custom spring stiffness, e.g. 380")
    parser.add_argument("--damping", type=float,
                        help="custom spring damping ratio, e.g. 0.8")
    parser.add_argument("--samples", type=int, default=None,
                        help="override the number of linear() samples")
    parser.add_argument("--table", action="store_true",
                        help="print every token and its parameters")
    parser.add_argument("--emit-css", metavar="PATH",
                        help="write the full token stylesheet to PATH")
    args = parser.parse_args(argv)

    if args.emit_css:
        path = pathlib.Path(args.emit_css)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_css(), encoding="utf-8")
        print(f"wrote {path}")
        return 0

    if args.stiffness is not None or args.damping is not None:
        if args.stiffness is None or args.damping is None:
            parser.error("--stiffness and --damping must be used together")
        ms = settle_ms(args.damping, args.stiffness)
        print(f"stiffness = {args.stiffness}")
        print(f"damping   = {args.damping}")
        print(f"duration  = {ms}ms")
        print(f"overshoot = {peak_overshoot(args.damping, args.stiffness):.1f}%")
        print()
        print(f"transition-timing-function: "
              f"{to_linear(args.damping, args.stiffness, ms, args.samples)};")
        return 0

    if args.table or not argv:
        header = (f"{'scheme':<11}{'speed':<9}{'type':<9}"
                  f"{'damping':>8}{'stiffness':>11}{'duration':>10}{'overshoot':>11}")
        print(header)
        print("-" * len(header))
        for scheme in ("expressive", "standard"):
            for kind in TYPES:
                for speed in SPEEDS:
                    damping, stiffness = SPRINGS[(scheme, kind, speed)]
                    print(f"{scheme:<11}{speed:<9}{kind:<9}"
                          f"{damping:>8.1f}{stiffness:>11.0f}"
                          f"{settle_ms(damping, stiffness):>9}ms"
                          f"{peak_overshoot(damping, stiffness):>10.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
