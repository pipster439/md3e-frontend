#!/usr/bin/env python3
"""Generate official Material 3 Expressive (MaterialShapes) CSS masks and morphing loader.

Pure Python standard-library port of AOSP ``androidx.graphics.shapes``
(``RoundedPolygon``, ``RoundedCorner``, ``Cubic``) and Jetpack Compose Material 3
``MaterialShapes`` (all 35 normalized presets) plus ``LoadingIndicatorDefaults``.

Outputs ``assets/tokens/md3e-shapes.css`` containing:
- ``--md-sys-shape-mask-<name>`` data-URI SVG masks for all 35 official shapes
- ``.md3e-shape`` and ``.md3e-shape-<name>`` container helpers using both
  ``-webkit-mask-image`` and standard ``mask-image`` with ``@supports`` fallback
- ``.md3e-shape-shadow-wrap`` using ``filter: drop-shadow()`` for masked shapes
- ``.md3e-loading-indicator`` & ``.md3e-loading-indicator--contained`` animating CSS
  ``d: path(...)`` across the official 7-polygon indeterminate sequence:
  SoftBurst -> Cookie9Sided -> Pentagon -> Pill -> Sunny -> Cookie4Sided -> Oval
  with rotation-safe scaling, ``spring(damping=0.6, stiffness=200)`` easing,
  ``4666ms`` global rotation, and ``prefers-reduced-motion: reduce`` support.

Usage
-----
    python scripts/shapes_to_css.py --emit-css assets/tokens/md3e-shapes.css
    python scripts/shapes_to_css.py --list
    python scripts/shapes_to_css.py --svg cookie-9-sided
"""

from __future__ import annotations

import argparse
import math
import pathlib
import sys
import urllib.parse
from dataclasses import dataclass

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import spring_to_css  # noqa: E402

DISTANCE_EPSILON = 1e-4

# Exact 35 official shape names matching androidx.compose.material3.MaterialShapes
SHAPE_NAMES = (
    "circle",
    "square",
    "slanted",
    "arch",
    "fan",
    "arrow",
    "semi-circle",
    "oval",
    "pill",
    "triangle",
    "diamond",
    "clam-shell",
    "pentagon",
    "gem",
    "sunny",
    "very-sunny",
    "cookie-4-sided",
    "cookie-6-sided",
    "cookie-7-sided",
    "cookie-9-sided",
    "cookie-12-sided",
    "ghostish",
    "clover-4-leaf",
    "clover-8-leaf",
    "burst",
    "soft-burst",
    "boom",
    "soft-boom",
    "flower",
    "puffy",
    "puffy-diamond",
    "pixel-circle",
    "pixel-triangle",
    "bun",
    "heart",
)

# Official LoadingIndicatorDefaults.IndeterminateIndicatorPolygons (LoadingIndicator.kt)
LOADING_SEQUENCE = (
    "soft-burst",
    "cookie-9-sided",
    "pentagon",
    "pill",
    "sunny",
    "cookie-4-sided",
    "oval",
)

MORPH_SAMPLES = 36


# ---------------------------------------------------------------------------
# 2D Vector & Cubic Bezier Port (androidx.graphics.shapes)
# ---------------------------------------------------------------------------

def _clamp(lo: float, hi: float, v: float) -> float:
    return lo if v < lo else (hi if v > hi else v)


def _lerp(a: float, b: float, t: float) -> float:
    return (1.0 - t) * a + t * b


def _v_add(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] + b[0], a[1] + b[1])


def _v_sub(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] - b[0], a[1] - b[1])


def _v_mul(a: tuple[float, float], s: float) -> tuple[float, float]:
    return (a[0] * s, a[1] * s)


def _v_dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _v_len(a: tuple[float, float]) -> float:
    return math.hypot(a[0], a[1])


def _v_rot90(a: tuple[float, float]) -> tuple[float, float]:
    return (-a[1], a[0])


def _v_dir(x: float, y: float) -> tuple[float, float]:
    d = math.hypot(x, y)
    if d <= 1e-9:
        return (1.0, 0.0)
    return (x / d, y / d)


@dataclass(frozen=True)
class CornerRounding:
    radius: float = 0.0
    smoothing: float = 0.0


UNROUNDED = CornerRounding(0.0, 0.0)


@dataclass(frozen=True)
class Cubic:
    p: tuple[float, float, float, float, float, float, float, float]

    @property
    def a0x(self) -> float: return self.p[0]
    @property
    def a0y(self) -> float: return self.p[1]
    @property
    def c0x(self) -> float: return self.p[2]
    @property
    def c0y(self) -> float: return self.p[3]
    @property
    def c1x(self) -> float: return self.p[4]
    @property
    def c1y(self) -> float: return self.p[5]
    @property
    def a1x(self) -> float: return self.p[6]
    @property
    def a1y(self) -> float: return self.p[7]

    def zero_length(self) -> bool:
        return abs(self.a0x - self.a1x) < DISTANCE_EPSILON and abs(self.a0y - self.a1y) < DISTANCE_EPSILON

    def point_on_curve(self, t: float) -> tuple[float, float]:
        u = 1.0 - t
        u3 = u * u * u
        t3 = t * t * t
        c0 = 3.0 * t * u * u
        c1 = 3.0 * t * t * u
        x = self.a0x * u3 + self.c0x * c0 + self.c1x * c1 + self.a1x * t3
        y = self.a0y * u3 + self.c0y * c0 + self.c1y * c1 + self.a1y * t3
        return (x, y)

    def split(self, t: float) -> tuple["Cubic", "Cubic"]:
        u = 1.0 - t
        mx, my = self.point_on_curve(t)
        return (
            Cubic((
                self.a0x, self.a0y,
                self.a0x * u + self.c0x * t, self.a0y * u + self.c0y * t,
                self.a0x * u * u + self.c0x * 2 * u * t + self.c1x * t * t,
                self.a0y * u * u + self.c0y * 2 * u * t + self.c1y * t * t,
                mx, my,
            )),
            Cubic((
                mx, my,
                self.c0x * u * u + self.c1x * 2 * u * t + self.a1x * t * t,
                self.c0y * u * u + self.c1y * 2 * u * t + self.a1y * t * t,
                self.c1x * u + self.a1x * t, self.c1y * u + self.a1y * t,
                self.a1x, self.a1y,
            )),
        )

    def reverse(self) -> "Cubic":
        return Cubic((self.a1x, self.a1y, self.c1x, self.c1y, self.c0x, self.c0y, self.a0x, self.a0y))

    def transformed(self, fn) -> "Cubic":
        x0, y0 = fn(self.a0x, self.a0y)
        x1, y1 = fn(self.c0x, self.c0y)
        x2, y2 = fn(self.c1x, self.c1y)
        x3, y3 = fn(self.a1x, self.a1y)
        return Cubic((x0, y0, x1, y1, x2, y2, x3, y3))

    @classmethod
    def straight_line(cls, x0: float, y0: float, x1: float, y1: float) -> "Cubic":
        return cls((
            x0, y0,
            _lerp(x0, x1, 1.0 / 3.0), _lerp(y0, y1, 1.0 / 3.0),
            _lerp(x0, x1, 2.0 / 3.0), _lerp(y0, y1, 2.0 / 3.0),
            x1, y1,
        ))

    @classmethod
    def circular_arc(cls, cx: float, cy: float, x0: float, y0: float, x1: float, y1: float) -> "Cubic":
        p0d = _v_dir(x0 - cx, y0 - cy)
        p1d = _v_dir(x1 - cx, y1 - cy)
        rot_p0 = _v_rot90(p0d)
        rot_p1 = _v_rot90(p1d)
        clockwise = _v_dot(rot_p0, (x1 - cx, y1 - cy)) >= 0.0
        cosa = _clamp(-1.0, 1.0, _v_dot(p0d, p1d))
        if cosa > 0.999 or abs(1.0 - cosa) < 1e-7:
            return cls.straight_line(x0, y0, x1, y1)
        r = math.hypot(x0 - cx, y0 - cy)
        k = (
            r * (4.0 / 3.0)
            * (math.sqrt(max(0.0, 2.0 * (1.0 - cosa))) - math.sqrt(max(0.0, 1.0 - cosa * cosa)))
            / (1.0 - cosa)
            * (1.0 if clockwise else -1.0)
        )
        return cls((
            x0, y0,
            x0 + rot_p0[0] * k, y0 + rot_p0[1] * k,
            x1 - rot_p1[0] * k, y1 - rot_p1[1] * k,
            x1, y1,
        ))


def _line_intersection(p0: tuple[float, float], d0: tuple[float, float], p1: tuple[float, float], d1: tuple[float, float]) -> tuple[float, float] | None:
    rot_d1 = _v_rot90(d1)
    den = _v_dot(d0, rot_d1)
    if abs(den) < DISTANCE_EPSILON:
        return None
    num = _v_dot(_v_sub(p1, p0), rot_d1)
    if abs(den) < DISTANCE_EPSILON * abs(num):
        return None
    return _v_add(p0, _v_mul(d0, num / den))


class RoundedCorner:
    def __init__(self, p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], rounding: CornerRounding | None) -> None:
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        v01 = _v_sub(p0, p1)
        v21 = _v_sub(p2, p1)
        d01 = _v_len(v01)
        d21 = _v_len(v21)
        if d01 > 0.0 and d21 > 0.0:
            self.d1 = (v01[0] / d01, v01[1] / d01)
            self.d2 = (v21[0] / d21, v21[1] / d21)
            self.corner_radius = rounding.radius if rounding else 0.0
            self.smoothing = rounding.smoothing if rounding else 0.0
            self.cos_angle = _clamp(-1.0, 1.0, _v_dot(self.d1, self.d2))
            self.sin_angle = math.sqrt(max(0.0, 1.0 - self.cos_angle * self.cos_angle))
            self.expected_round_cut = (
                self.corner_radius * (self.cos_angle + 1.0) / self.sin_angle
                if self.sin_angle > 1e-3
                else 0.0
            )
        else:
            self.d1 = (0.0, 0.0)
            self.d2 = (0.0, 0.0)
            self.corner_radius = 0.0
            self.smoothing = 0.0
            self.cos_angle = 0.0
            self.sin_angle = 0.0
            self.expected_round_cut = 0.0

    @property
    def expected_cut(self) -> float:
        return (1.0 + self.smoothing) * self.expected_round_cut

    def _actual_smoothing(self, allowed_cut: float) -> float:
        if allowed_cut > self.expected_cut:
            return self.smoothing
        if allowed_cut > self.expected_round_cut and (self.expected_cut - self.expected_round_cut) > 1e-9:
            return self.smoothing * (allowed_cut - self.expected_round_cut) / (self.expected_cut - self.expected_round_cut)
        return 0.0

    def _compute_flanking_curve(
        self,
        actual_round_cut: float,
        actual_smoothing: float,
        corner: tuple[float, float],
        side_start: tuple[float, float],
        circle_inter: tuple[float, float],
        other_inter: tuple[float, float],
        center: tuple[float, float],
        actual_r: float,
    ) -> Cubic:
        side_dir = _v_dir(side_start[0] - corner[0], side_start[1] - corner[1])
        curve_start = _v_add(corner, _v_mul(side_dir, actual_round_cut * (1.0 + actual_smoothing)))
        mid = ((circle_inter[0] + other_inter[0]) / 2.0, (circle_inter[1] + other_inter[1]) / 2.0)
        p = (_lerp(circle_inter[0], mid[0], actual_smoothing), _lerp(circle_inter[1], mid[1], actual_smoothing))
        curve_end = _v_add(center, _v_mul(_v_dir(p[0] - center[0], p[1] - center[1]), actual_r))
        tangent = _v_rot90(_v_sub(curve_end, center))
        anchor_end = _line_intersection(side_start, side_dir, curve_end, tangent) or circle_inter
        anchor_start = ((curve_start[0] + anchor_end[0] * 2.0) / 3.0, (curve_start[1] + anchor_end[1] * 2.0) / 3.0)
        return Cubic((curve_start[0], curve_start[1], anchor_start[0], anchor_start[1], anchor_end[0], anchor_end[1], curve_end[0], curve_end[1]))

    def get_cubics(self, allowed_cut0: float, allowed_cut1: float) -> list[Cubic]:
        allowed_cut = min(allowed_cut0, allowed_cut1)
        if (
            self.expected_round_cut < DISTANCE_EPSILON
            or allowed_cut < DISTANCE_EPSILON
            or self.corner_radius < DISTANCE_EPSILON
        ):
            return [Cubic.straight_line(self.p1[0], self.p1[1], self.p1[0], self.p1[1])]

        actual_round_cut = min(allowed_cut, self.expected_round_cut)
        s0 = self._actual_smoothing(allowed_cut0)
        s1 = self._actual_smoothing(allowed_cut1)
        actual_r = self.corner_radius * actual_round_cut / self.expected_round_cut
        center_dist = math.hypot(actual_r, actual_round_cut)
        bisector = ((self.d1[0] + self.d2[0]) / 2.0, (self.d1[1] + self.d2[1]) / 2.0)
        if _v_len(bisector) < 1e-6:
            return [Cubic.straight_line(self.p1[0], self.p1[1], self.p1[0], self.p1[1])]
        center = _v_add(self.p1, _v_mul(_v_dir(bisector[0], bisector[1]), center_dist))
        ci0 = _v_add(self.p1, _v_mul(self.d1, actual_round_cut))
        ci2 = _v_add(self.p1, _v_mul(self.d2, actual_round_cut))
        flank0 = self._compute_flanking_curve(actual_round_cut, s0, self.p1, self.p0, ci0, ci2, center, actual_r)
        flank2 = self._compute_flanking_curve(actual_round_cut, s1, self.p1, self.p2, ci2, ci0, center, actual_r).reverse()
        arc = Cubic.circular_arc(center[0], center[1], flank0.a1x, flank0.a1y, flank2.a0x, flank2.a0y)
        return [flank0, arc, flank2]


class RoundedPolygon:
    def __init__(self, cubics: list[Cubic], cx: float, cy: float) -> None:
        self.cubics = cubics
        self.cx = cx
        self.cy = cy

    @classmethod
    def from_vertices(
        cls,
        vertices: list[tuple[float, float]],
        rounding: CornerRounding = UNROUNDED,
        per_vertex_rounding: list[CornerRounding] | None = None,
        cx: float | None = None,
        cy: float | None = None,
    ) -> "RoundedPolygon":
        n = len(vertices)
        assert n >= 3
        corners_obj = [
            RoundedCorner(
                vertices[(i + n - 1) % n],
                vertices[i],
                vertices[(i + 1) % n],
                per_vertex_rounding[i] if per_vertex_rounding is not None else rounding,
            )
            for i in range(n)
        ]
        cut_adjusts: list[tuple[float, float]] = []
        for i in range(n):
            nxt = (i + 1) % n
            exp_rc = corners_obj[i].expected_round_cut + corners_obj[nxt].expected_round_cut
            exp_c = corners_obj[i].expected_cut + corners_obj[nxt].expected_cut
            side = math.hypot(vertices[i][0] - vertices[nxt][0], vertices[i][1] - vertices[nxt][1])
            if exp_rc > side and exp_rc > 1e-9:
                cut_adjusts.append((side / exp_rc, 0.0))
            elif exp_c > side and (exp_c - exp_rc) > 1e-9:
                cut_adjusts.append((1.0, (side - exp_rc) / (exp_c - exp_rc)))
            else:
                cut_adjusts.append((1.0, 1.0))

        corner_cubics: list[list[Cubic]] = []
        for i in range(n):
            allowed = []
            for delta in (0, 1):
                rc_ratio, c_ratio = cut_adjusts[(i + n - 1 + delta) % n]
                allowed.append(
                    corners_obj[i].expected_round_cut * rc_ratio
                    + (corners_obj[i].expected_cut - corners_obj[i].expected_round_cut) * c_ratio
                )
            corner_cubics.append(corners_obj[i].get_cubics(allowed[0], allowed[1]))

        features: list[list[Cubic]] = []
        for i in range(n):
            features.append(corner_cubics[i])
            c_end = corner_cubics[i][-1]
            c_nxt = corner_cubics[(i + 1) % n][0]
            features.append([Cubic.straight_line(c_end.a1x, c_end.a1y, c_nxt.a0x, c_nxt.a0y)])

        # Flatten with AOSP first-feature-split mechanism for contiguous loop closure
        out: list[Cubic] = []
        first_c: Cubic | None = None
        last_c: Cubic | None = None
        split_start: list[Cubic] | None = None
        split_end: list[Cubic] | None = None
        if features and len(features[0]) == 3:
            s0, s1 = features[0][1].split(0.5)
            split_start = [features[0][0], s0]
            split_end = [s1, features[0][2]]

        for idx in range(len(features) + 1):
            if idx == 0 and split_end is not None:
                f_cubics = split_end
            elif idx == len(features):
                if split_start is not None:
                    f_cubics = split_start
                else:
                    break
            else:
                f_cubics = features[idx]

            for c in f_cubics:
                if not c.zero_length():
                    if last_c is not None:
                        out.append(last_c)
                    last_c = c
                    if first_c is None:
                        first_c = c
                elif last_c is not None:
                    p = list(last_c.p)
                    p[6], p[7] = c.a1x, c.a1y
                    last_c = Cubic(tuple(p))  # type: ignore[arg-type]

        if last_c is not None and first_c is not None:
            out.append(Cubic((
                last_c.a0x, last_c.a0y, last_c.c0x, last_c.c0y,
                last_c.c1x, last_c.c1y, first_c.a0x, first_c.a0y,
            )))
        if cx is None or cy is None:
            cx = sum(v[0] for v in vertices) / n
            cy = sum(v[1] for v in vertices) / n
        return cls(out, cx, cy)

    def transformed(self, fn) -> "RoundedPolygon":
        nx, ny = fn(self.cx, self.cy)
        return RoundedPolygon([c.transformed(fn) for c in self.cubics], nx, ny)

    def rotated_deg(self, deg: float, cx: float = 0.0, cy: float = 0.0) -> "RoundedPolygon":
        rad = math.radians(deg)
        ca, sa = math.cos(rad), math.sin(rad)
        return self.transformed(lambda x, y: ((x - cx) * ca - (y - cy) * sa + cx, (x - cx) * sa + (y - cy) * ca + cy))

    def bounds(self) -> tuple[float, float, float, float]:
        # Sample cubics finely enough for exact axis-aligned bounds
        xs: list[float] = []
        ys: list[float] = []
        for c in self.cubics:
            for s in range(9):
                x, y = c.point_on_curve(s / 8.0)
                xs.append(x)
                ys.append(y)
        return (min(xs), min(ys), max(xs), max(ys))

    def normalized(self) -> "RoundedPolygon":
        min_x, min_y, max_x, max_y = self.bounds()
        w, h = max_x - min_x, max_y - min_y
        side = max(w, h)
        if side <= 1e-9:
            return self
        ox = (side - w) / 2.0 - min_x
        oy = (side - h) / 2.0 - min_y
        return self.transformed(lambda x, y: ((x + ox) / side, (y + oy) / side))

    def max_radius_from_center(self) -> float:
        r2 = 0.0
        for c in self.cubics:
            for t in (0.0, 0.25, 0.5, 0.75):
                x, y = c.point_on_curve(t)
                r2 = max(r2, (x - 0.5) ** 2 + (y - 0.5) ** 2)
        return math.sqrt(r2)

    @classmethod
    def regular(cls, num_vertices: int, radius: float = 1.0, rounding: CornerRounding = UNROUNDED, per_vertex_rounding: list[CornerRounding] | None = None) -> "RoundedPolygon":
        verts = [(radius * math.cos(2 * math.pi * i / num_vertices), radius * math.sin(2 * math.pi * i / num_vertices)) for i in range(num_vertices)]
        return cls.from_vertices(verts, rounding=rounding, per_vertex_rounding=per_vertex_rounding, cx=0.0, cy=0.0)

    @classmethod
    def circle(cls, num_vertices: int = 8, radius: float = 1.0) -> "RoundedPolygon":
        poly_r = radius / math.cos(math.pi / num_vertices)
        return cls.regular(num_vertices, radius=poly_r, rounding=CornerRounding(radius))

    @classmethod
    def rectangle(cls, width: float = 2.0, height: float = 2.0, rounding: CornerRounding = UNROUNDED, per_vertex_rounding: list[CornerRounding] | None = None) -> "RoundedPolygon":
        hw, hh = width / 2.0, height / 2.0
        verts = [(hw, hh), (-hw, hh), (-hw, -hh), (hw, -hh)]
        return cls.from_vertices(verts, rounding=rounding, per_vertex_rounding=per_vertex_rounding, cx=0.0, cy=0.0)

    @classmethod
    def star(cls, num_per_radius: int, radius: float = 1.0, inner_radius: float = 0.5, rounding: CornerRounding = UNROUNDED) -> "RoundedPolygon":
        verts: list[tuple[float, float]] = []
        for i in range(num_per_radius):
            a0 = math.pi / num_per_radius * (2 * i)
            verts.append((radius * math.cos(a0), radius * math.sin(a0)))
            a1 = math.pi / num_per_radius * (2 * i + 1)
            verts.append((inner_radius * math.cos(a1), inner_radius * math.sin(a1)))
        return cls.from_vertices(verts, rounding=rounding, cx=0.0, cy=0.0)


# ---------------------------------------------------------------------------
# All 35 Official MaterialShapes Presets (from MaterialShapes.kt)
# ---------------------------------------------------------------------------

def _do_repeat(
    points: list[tuple[tuple[float, float], CornerRounding]],
    reps: int,
    center: tuple[float, float] = (0.5, 0.5),
    mirroring: bool = False,
) -> list[tuple[tuple[float, float], CornerRounding]]:
    cx, cy = center
    if mirroring:
        angles = [math.degrees(math.atan2(y - cy, x - cx)) for (x, y), _ in points]
        dists = [math.hypot(x - cx, y - cy) for (x, y), _ in points]
        actual_reps = reps * 2
        section = 360.0 / actual_reps
        out: list[tuple[tuple[float, float], CornerRounding]] = []
        for r in range(actual_reps):
            for idx in range(len(points)):
                i = idx if (r % 2 == 0) else (len(points) - 1 - idx)
                if i > 0 or (r % 2 == 0):
                    a_deg = section * r + (angles[i] if (r % 2 == 0) else (section - angles[i] + 2.0 * angles[0]))
                    a = math.radians(a_deg)
                    out.append(((math.cos(a) * dists[i] + cx, math.sin(a) * dists[i] + cy), points[i][1]))
        return out
    out = []
    np_count = len(points)
    for k in range(np_count * reps):
        pt, cr = points[k % np_count]
        ang = math.radians((k // np_count) * 360.0 / reps)
        ca, sa = math.cos(ang), math.sin(ang)
        dx, dy = pt[0] - cx, pt[1] - cy
        out.append(((dx * ca - dy * sa + cx, dx * sa + dy * ca + cy), cr))
    return out


def _custom_polygon(
    points: list[tuple[tuple[float, float], CornerRounding]],
    reps: int,
    center: tuple[float, float] = (0.5, 0.5),
    mirroring: bool = False,
) -> RoundedPolygon:
    rep = _do_repeat(points, reps, center, mirroring)
    return RoundedPolygon.from_vertices(
        [p for p, _ in rep],
        per_vertex_rounding=[cr for _, cr in rep],
        cx=center[0],
        cy=center[1],
    )


def build_shape(name: str) -> RoundedPolygon:
    c15 = CornerRounding(0.15)
    c20 = CornerRounding(0.20)
    c30 = CornerRounding(0.30)
    c50 = CornerRounding(0.50)
    c100 = CornerRounding(1.00)
    CR = CornerRounding

    if name == "circle":
        poly = RoundedPolygon.circle(num_vertices=10)
    elif name == "square":
        poly = RoundedPolygon.rectangle(1.0, 1.0, rounding=c30)
    elif name == "slanted":
        poly = _custom_polygon([((0.926, 0.970), CR(0.189, 0.811)), ((-0.021, 0.967), CR(0.187, 0.057))], 2)
    elif name == "arch":
        poly = RoundedPolygon.regular(4, per_vertex_rounding=[c100, c100, c20, c20]).rotated_deg(-135.0)
    elif name == "fan":
        poly = _custom_polygon([((1.004, 1.000), CR(0.148, 0.417)), ((0.000, 1.000), CR(0.151)), ((0.000, -0.003), CR(0.148)), ((0.978, 0.020), CR(0.803))], 1)
    elif name == "arrow":
        poly = _custom_polygon([((0.500, 0.892), CR(0.313)), ((-0.216, 1.050), CR(0.207)), ((0.499, -0.160), CR(0.215, 1.000)), ((1.225, 1.060), CR(0.211))], 1)
    elif name == "semi-circle":
        poly = RoundedPolygon.rectangle(1.6, 1.0, per_vertex_rounding=[c20, c20, c100, c100])
    elif name == "oval":
        poly = RoundedPolygon.circle().transformed(lambda x, y: (x, y * 0.64)).rotated_deg(-45.0)
    elif name == "pill":
        poly = _custom_polygon([((0.961, 0.039), CR(0.426)), ((1.001, 0.428), UNROUNDED), ((1.000, 0.609), CR(1.000))], reps=2, mirroring=True)
    elif name == "triangle":
        poly = RoundedPolygon.regular(3, rounding=c20).rotated_deg(-90.0)
    elif name == "diamond":
        poly = _custom_polygon([((0.500, 1.096), CR(0.151, 0.524)), ((0.040, 0.500), CR(0.159))], 2)
    elif name == "clam-shell":
        poly = _custom_polygon([((0.171, 0.841), CR(0.159)), ((-0.020, 0.500), CR(0.140)), ((0.170, 0.159), CR(0.159))], 2)
    elif name == "pentagon":
        poly = _custom_polygon([((0.500, -0.009), CR(0.172)), ((1.030, 0.365), CR(0.164)), ((0.828, 0.970), CR(0.169))], reps=1, mirroring=True)
    elif name == "gem":
        poly = _custom_polygon([((0.499, 1.023), CR(0.241, 0.778)), ((-0.005, 0.792), CR(0.208)), ((0.073, 0.258), CR(0.228)), ((0.433, 0.000), CR(0.491))], reps=1, mirroring=True)
    elif name == "sunny":
        poly = RoundedPolygon.star(8, inner_radius=0.8, rounding=c15)
    elif name == "very-sunny":
        poly = _custom_polygon([((0.500, 1.080), CR(0.085)), ((0.358, 0.843), CR(0.085))], 8)
    elif name == "cookie-4-sided":
        poly = _custom_polygon([((1.237, 1.236), CR(0.258)), ((0.500, 0.918), CR(0.233))], 4)
    elif name == "cookie-6-sided":
        poly = _custom_polygon([((0.723, 0.884), CR(0.394)), ((0.500, 1.099), CR(0.398))], 6)
    elif name == "cookie-7-sided":
        poly = RoundedPolygon.star(7, inner_radius=0.75, rounding=c50).rotated_deg(-90.0)
    elif name == "cookie-9-sided":
        poly = RoundedPolygon.star(9, inner_radius=0.8, rounding=c50).rotated_deg(-90.0)
    elif name == "cookie-12-sided":
        poly = RoundedPolygon.star(12, inner_radius=0.8, rounding=c50).rotated_deg(-90.0)
    elif name == "ghostish":
        poly = _custom_polygon([((0.500, 0.0), CR(1.0)), ((1.0, 0.0), CR(1.0)), ((1.0, 1.140), CR(0.254, 0.106)), ((0.575, 0.906), CR(0.253))], reps=1, mirroring=True)
    elif name == "clover-4-leaf":
        poly = _custom_polygon([((0.500, 0.074), UNROUNDED), ((0.725, -0.099), CR(0.476))], reps=4, mirroring=True)
    elif name == "clover-8-leaf":
        poly = _custom_polygon([((0.500, 0.036), UNROUNDED), ((0.758, -0.101), CR(0.209))], reps=8)
    elif name == "burst":
        poly = _custom_polygon([((0.500, -0.006), CR(0.006)), ((0.592, 0.158), CR(0.006))], reps=12)
    elif name == "soft-burst":
        poly = _custom_polygon([((0.193, 0.277), CR(0.053)), ((0.176, 0.055), CR(0.053))], reps=10)
    elif name == "boom":
        poly = _custom_polygon([((0.457, 0.296), CR(0.007)), ((0.500, -0.051), CR(0.007))], reps=15)
    elif name == "soft-boom":
        poly = _custom_polygon([((0.733, 0.454), UNROUNDED), ((0.839, 0.437), CR(0.532)), ((0.949, 0.449), CR(0.439, 1.000)), ((0.998, 0.478), CR(0.174))], reps=16, mirroring=True)
    elif name == "flower":
        poly = _custom_polygon([((0.370, 0.187), UNROUNDED), ((0.416, 0.049), CR(0.381)), ((0.479, 0.001), CR(0.095))], reps=8, mirroring=True)
    elif name == "puffy":
        poly = _custom_polygon([
            ((0.500, 0.053), UNROUNDED), ((0.545, -0.040), CR(0.405)), ((0.670, -0.035), CR(0.426)),
            ((0.717, 0.066), CR(0.574)), ((0.722, 0.128), UNROUNDED), ((0.777, 0.002), CR(0.360)),
            ((0.914, 0.149), CR(0.660)), ((0.926, 0.289), CR(0.660)), ((0.881, 0.346), UNROUNDED),
            ((0.940, 0.344), CR(0.126)), ((1.003, 0.437), CR(0.255)),
        ], reps=2, mirroring=True).transformed(lambda x, y: (x, y * 0.742))
    elif name == "puffy-diamond":
        poly = _custom_polygon([((0.870, 0.130), CR(0.146)), ((0.818, 0.357), UNROUNDED), ((1.000, 0.332), CR(0.853))], reps=4, mirroring=True)
    elif name == "pixel-circle":
        poly = _custom_polygon([
            ((0.500, 0.000), UNROUNDED), ((0.704, 0.000), UNROUNDED), ((0.704, 0.065), UNROUNDED),
            ((0.843, 0.065), UNROUNDED), ((0.843, 0.148), UNROUNDED), ((0.926, 0.148), UNROUNDED),
            ((0.926, 0.296), UNROUNDED), ((1.000, 0.296), UNROUNDED),
        ], reps=2, mirroring=True)
    elif name == "pixel-triangle":
        poly = _custom_polygon([
            ((0.110, 0.500), UNROUNDED), ((0.113, 0.000), UNROUNDED), ((0.287, 0.000), UNROUNDED),
            ((0.287, 0.087), UNROUNDED), ((0.421, 0.087), UNROUNDED), ((0.421, 0.170), UNROUNDED),
            ((0.560, 0.170), UNROUNDED), ((0.560, 0.265), UNROUNDED), ((0.674, 0.265), UNROUNDED),
            ((0.675, 0.344), UNROUNDED), ((0.789, 0.344), UNROUNDED), ((0.789, 0.439), UNROUNDED),
            ((0.888, 0.439), UNROUNDED),
        ], reps=1, mirroring=True)
    elif name == "bun":
        poly = _custom_polygon([((0.796, 0.500), UNROUNDED), ((0.853, 0.518), c100), ((0.992, 0.631), c100), ((0.968, 1.000), c100)], reps=2, mirroring=True)
    elif name == "heart":
        poly = _custom_polygon([((0.500, 0.268), CR(0.016)), ((0.792, -0.066), CR(0.958)), ((1.064, 0.276), c100), ((0.501, 0.946), CR(0.129))], reps=1, mirroring=True)
    else:
        raise ValueError(f"Unknown MaterialShape: {name}")

    return poly.normalized()


def polygon_to_svg_path(poly: RoundedPolygon, scale: float = 100.0, prec: int = 2) -> str:
    """Serialize normalized [0..1] RoundedPolygon cubics into an SVG path on 100x100 viewBox."""
    fmt = lambda v: f"{(v - 0.5) * scale + 50.0:.{prec}f}".rstrip("0").rstrip(".") if "." in f"{(v - 0.5) * scale + 50.0:.{prec}f}" else f"{(v - 0.5) * scale + 50.0:.{prec}f}"

    def _f(val: float) -> str:
        s = f"{((val - 0.5) * scale + 50.0):.{prec}f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return "0" if s == "-0" else s

    parts = [f"M{_f(poly.cubics[0].a0x)} {_f(poly.cubics[0].a0y)}"]
    for c in poly.cubics:
        parts.append(f"C{_f(c.c0x)} {_f(c.c0y)} {_f(c.c1x)} {_f(c.c1y)} {_f(c.a1x)} {_f(c.a1y)}")
    parts.append("Z")
    return "".join(parts)


def resample_polygon_for_morph(
    poly: RoundedPolygon,
    num_segments: int = MORPH_SAMPLES,
    scale_factor: float = 0.84,
) -> str:
    """Resample a closed RoundedPolygon uniformly by arc length into ``num_segments``
    cubic Bezier commands, clockwise-wound and aligned to 12 o'clock (top), for
    smooth CSS ``d: path(...)`` morphing across heterogeneous shapes.
    """
    pts: list[tuple[float, float]] = []
    sub_steps = 12
    for c in poly.cubics:
        for s in range(sub_steps):
            pts.append(c.point_on_curve(s / sub_steps))
    n = len(pts)

    # Signed area in screen space (+y down): positive = clockwise
    area2 = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    if area2 < 0:
        pts.reverse()

    # Rotate array so start point sits closest to 12 o'clock (angle = -pi/2)
    def top_score(pt: tuple[float, float]) -> float:
        ang = math.atan2(pt[1] - 0.5, pt[0] - 0.5)
        diff = (ang - (-math.pi / 2.0) + math.pi) % (2.0 * math.pi) - math.pi
        return abs(diff)

    start_idx = min(range(n), key=lambda idx: top_score(pts[idx]))
    pts = pts[start_idx:] + pts[:start_idx]
    pts.append(pts[0])  # closed loop

    cum = [0.0]
    for i in range(n):
        cum.append(cum[-1] + math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]))
    total_len = cum[-1]

    def point_at_arc(s: float) -> tuple[float, float]:
        s = s % total_len
        lo, hi = 0, n
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if cum[mid] <= s:
                lo = mid
            else:
                hi = mid
        seg_l = cum[lo + 1] - cum[lo]
        t = (s - cum[lo]) / seg_l if seg_l > 1e-9 else 0.0
        return (_lerp(pts[lo][0], pts[lo + 1][0], t), _lerp(pts[lo][1], pts[lo + 1][1], t))

    anchors = [point_at_arc(total_len * k / num_segments) for k in range(num_segments)]
    eps = total_len / (num_segments * 8.0)
    tangents: list[tuple[float, float]] = []
    for k in range(num_segments):
        s_mid = total_len * k / num_segments
        pm = point_at_arc(s_mid - eps)
        pp = point_at_arc(s_mid + eps)
        tangents.append(_v_dir(pp[0] - pm[0], pp[1] - pm[1]))

    handle_len = (total_len / num_segments) / 3.0

    def _f(v: float) -> str:
        val = (v - 0.5) * 100.0 * scale_factor + 50.0
        s = f"{val:.2f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return "0" if s == "-0" else s

    parts = [f"M{_f(anchors[0][0])} {_f(anchors[0][1])}"]
    for k in range(num_segments):
        nxt = (k + 1) % num_segments
        a0, t0 = anchors[k], tangents[k]
        a1, t1 = anchors[nxt], tangents[nxt]
        c0 = (a0[0] + t0[0] * handle_len, a0[1] + t0[1] * handle_len)
        c1 = (a1[0] - t1[0] * handle_len, a1[1] - t1[1] * handle_len)
        parts.append(f"C{_f(c0[0])} {_f(c0[1])} {_f(c1[0])} {_f(c1[1])} {_f(a1[0])} {_f(a1[1])}")
    parts.append("Z")
    return "".join(parts)


def make_svg_data_uri(path_d: str) -> str:
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path fill='#000' d='{path_d}'/></svg>"
    encoded = urllib.parse.quote(svg, safe="':/=,()")
    return f'url("data:image/svg+xml,{encoded}")'


def compute_loading_paths() -> list[tuple[str, str]]:
    polys = [(name, build_shape(name)) for name in LOADING_SEQUENCE]
    max_r = max(p.max_radius_from_center() for _, p in polys)
    # Our SVG viewport is already 38x38 inside the 48x48 box, so we only
    # need rotation-safe padding (0.485 / max_r keeps every rotated tip inside [1.5, 98.5]).
    safe_scale = min(0.96, 0.485 / max_r)
    return [(name, resample_polygon_for_morph(p, MORPH_SAMPLES, scale_factor=safe_scale)) for name, p in polys]


def render_css() -> str:
    morph_easing = spring_to_css.to_linear(0.6, 200.0, 650)
    loading_paths = compute_loading_paths()
    soft_burst_path = loading_paths[0][1]

    lines: list[str] = [
        "/* ============================================================================",
        " * md3e-shapes.css — Official 35 MaterialShapes & Morphing Loading Indicator",
        " *",
        " * GENERATED FILE — do not edit by hand.",
        " * Regenerate with:  python scripts/shapes_to_css.py --emit-css \\",
        " *                       assets/tokens/md3e-shapes.css",
        " *",
        " * Geometry ported from AOSP androidx.compose.material3.MaterialShapes",
        " * (35 normalized RoundedPolygon presets) and LoadingIndicatorDefaults.",
        " * ========================================================================== */",
        "",
        ":root {",
        "  --md-comp-loading-indicator-rotation-duration: 4666ms;",
        "  --md-comp-loading-indicator-morph-cycle-duration: 4550ms;",
        "  --md-comp-loading-indicator-reduced-pulse-duration: 1500ms;",
        f"  --md-comp-loading-indicator-morph-easing: {morph_easing};",
    ]
    for name in SHAPE_NAMES:
        d = polygon_to_svg_path(build_shape(name))
        lines.append(f"  --md-sys-shape-mask-{name}: {make_svg_data_uri(d)};")
    lines.append("}")
    lines.append("")

    lines.extend([
        "/* ============================================================================",
        " * Shape Containers (Images, Avatars, Illustrations & Decorative Crops)",
        " * Uses both -webkit-mask-image and standard mask-image, with @supports fallback.",
        " * ========================================================================== */",
        ".md3e-shape {",
        "  display: inline-block;",
        "  aspect-ratio: 1;",
        "  overflow: hidden;",
        "  -webkit-mask-size: contain;",
        "  mask-size: contain;",
        "  -webkit-mask-repeat: no-repeat;",
        "  mask-repeat: no-repeat;",
        "  -webkit-mask-position: center;",
        "  mask-position: center;",
        "}",
        "",
        "@supports (not (mask-image: url(\"\"))) and (not (-webkit-mask-image: url(\"\"))) {",
        "  .md3e-shape {",
        "    border-radius: var(--md-sys-shape-corner-extra-large);",
        "  }",
        "}",
        "",
        "/* Wrap masked shapes here to render soft shadow without rectangular box-shadow clipping */",
        ".md3e-shape-shadow-wrap {",
        "  display: inline-flex;",
        "  filter: drop-shadow(0 4px 10px color-mix(in oklab, var(--md-sys-color-shadow) 24%, transparent));",
        "}",
        "",
    ])

    for name in SHAPE_NAMES:
        lines.append(f".md3e-shape-{name} {{")
        lines.append(f"  -webkit-mask-image: var(--md-sys-shape-mask-{name});")
        lines.append(f"  mask-image: var(--md-sys-shape-mask-{name});")
        lines.append("}")

    lines.extend([
        "",
        "/* ============================================================================",
        " * Official 7-Polygon Morphing Loading Indicator (LoadingIndicatorDefaults)",
        " * SoftBurst -> Cookie9Sided -> Pentagon -> Pill -> Sunny -> Cookie4Sided -> Oval",
        " * ========================================================================== */",
        ".md3e-loading-indicator {",
        "  display: inline-grid;",
        "  place-items: center;",
        "  width: 48px;",
        "  height: 48px;",
        "  border-radius: var(--md-sys-shape-corner-full);",
        "}",
        "",
        ".md3e-loading-indicator--contained {",
        "  background: var(--md-sys-color-primary-container);",
        "}",
        "",
        ".md3e-loading-indicator__svg {",
        "  width: 38px;",
        "  height: 38px;",
        "  color: var(--md-sys-color-primary);",
        "  animation: md3e-loader-spin var(--md-comp-loading-indicator-rotation-duration, 4666ms) var(--md-sys-motion-easing-linear, linear) infinite;",
        "  transform-origin: center;",
        "}",
        "",
        ".md3e-loading-indicator--contained .md3e-loading-indicator__svg {",
        "  color: var(--md-sys-color-on-primary-container);",
        "}",
        "",
        ".md3e-loading-indicator__path {",
        f'  d: path("{soft_burst_path}");',
        "  fill: currentColor;",
        "  animation: md3e-loader-morph-7 var(--md-comp-loading-indicator-morph-cycle-duration, 4550ms) var(--md-comp-loading-indicator-morph-easing) infinite;",
        "}",
        "",
        "@keyframes md3e-loader-spin {",
        "  from { transform: rotate(0deg); }",
        "  to { transform: rotate(360deg); }",
        "}",
        "",
        "@keyframes md3e-loader-morph-7 {",
    ])

    steps = len(loading_paths)
    for idx, (sname, path_d) in enumerate(loading_paths):
        pct = f"{(idx * 100.0 / steps):.4f}".rstrip("0").rstrip(".")
        lines.append(f"  {pct}% {{ /* {sname} */")
        lines.append(f'    d: path("{path_d}");')
        lines.append("    animation-timing-function: var(--md-comp-loading-indicator-morph-easing);")
        lines.append("  }")
    lines.append(f"  100% {{ /* {loading_paths[0][0]} wrap */")
    lines.append(f'    d: path("{soft_burst_path}");')
    lines.append("  }")
    lines.extend([
        "}",
        "",
        "@media (prefers-reduced-motion: reduce) {",
        "  .md3e-loading-indicator__svg {",
        "    animation: md3e-loader-reduced-pulse var(--md-comp-loading-indicator-reduced-pulse-duration, 1500ms) var(--md-sys-motion-easing-linear, linear) infinite;",
        "  }",
        "  .md3e-loading-indicator__path {",
        "    animation: none;",
        "  }",
        "  @keyframes md3e-loader-reduced-pulse {",
        "    0%, 100% { opacity: 0.45; }",
        "    50% { opacity: 1; }",
        "  }",
        "}",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate official 35 MD3E MaterialShapes CSS masks & loader.")
    parser.add_argument("--list", action="store_true", help="List all 35 official shape names")
    parser.add_argument("--svg", metavar="NAME", help="Print standalone SVG markup for shape NAME")
    parser.add_argument("--emit-css", metavar="PATH", help="Write full md3e-shapes.css to PATH")
    args = parser.parse_args(argv)

    if args.list:
        for idx, name in enumerate(SHAPE_NAMES, 1):
            print(f"{idx:>2}. {name:<18} .md3e-shape-{name}")
        return 0

    if args.svg:
        d = polygon_to_svg_path(build_shape(args.svg))
        print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path fill="currentColor" d="{d}"/></svg>')
        return 0

    css = render_css()
    if args.emit_css:
        out_path = pathlib.Path(args.emit_css)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(css, encoding="utf-8")
        print(f"wrote {out_path} ({len(SHAPE_NAMES)} shapes + 7-polygon LoadingIndicator)")
        return 0

    print(css[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
