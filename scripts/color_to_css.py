#!/usr/bin/env python3
"""Convert a Material 3 Expressive seed colour into complete CSS custom properties.

Pure Python standard-library implementation of Google's HCT (Hue-Chroma-Tone /
CAM16 + CIE L*) colour space, Tonal Palettes, and Official Material Color
Utilities (MCU) DynamicScheme rules (supporting both 2025 M3 Expressive and
2021 legacy specs).

Features
--------
- Generates all 37 standard ``--md-sys-color-*`` roles (plus M3E 2025 ``*-dim``
  roles when appropriate) for Light, System Dark, Explicit Dark, Medium Contrast
  (0.5 -> >= 6:1 paired), and High Contrast (1.0 -> >= 7:1 paired).
- Implements official scheme variants:
    tonal-spot   Balanced default Material theme
    expressive   Detached, high-variety hues + tinted neutral surfaces (2025 M3E)
    vibrant      High-chroma accent palettes + tinted surfaces
    neutral      Near-greyscale restrained palette
    monochrome   Pure greyscale accessible palette
    fidelity     True-to-seed primary container & complement tertiary
- Guards every emitted background/on-background pair so paired contrast ratios
  always meet >= 4.5:1 (standard), >= 6.0:1 (medium), and >= 7.0:1 (high).

Usage
-----
    python scripts/color_to_css.py --seed "#0B57D0" --variant expressive
    python scripts/color_to_css.py --image wallpaper.jpg --variant expressive --emit-css brand.css
    python scripts/color_to_css.py --seed "#146C2E" --variant vibrant --emit-css brand.css
    python scripts/color_to_css.py --seed "#6750A4" --variant tonal-spot --json
    python scripts/color_to_css.py --emit-presets assets/tokens/md3e-palettes.css
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from dataclasses import dataclass
from typing import Callable

# ---------------------------------------------------------------------------
# Constants & Preset Seeds
# ---------------------------------------------------------------------------

VARIANTS = ("tonal-spot", "expressive", "vibrant", "neutral", "monochrome", "fidelity")
UI_VARIANTS = ("tonal-spot", "expressive", "vibrant", "neutral", "monochrome")

PRESET_SEEDS: dict[str, str] = {
    "purple": "#6750A4",
    "ocean": "#0B57D0",
    "emerald": "#146C2E",
    "amber": "#8F4C00",
    "rose": "#9C4146",
    "teal": "#006A6A",
}

WHITE_POINT_D65 = (95.047, 100.0, 108.883)

SRGB_TO_XYZ = (
    (0.41233895, 0.35762064, 0.18051042),
    (0.2126, 0.7152, 0.0722),
    (0.01932141, 0.11916382, 0.95034478),
)

XYZ_TO_SRGB = (
    (3.2413774792388685, -1.5376652402851851, -0.49885366846268053),
    (-0.9691452513005321, 1.8758853451067872, 0.04156585616912061),
    (0.05562093689691305, -0.20395524564742123, 1.0571799111220335),
)

SCALED_DISCOUNT_FROM_LINRGB = (
    (0.001200833568784504, 0.002389694492170889, 0.0002795742885861124),
    (0.0005891086651375999, 0.0029785502573438758, 0.0003270666104008398),
    (0.00010146692491640572, 0.0005364214359186694, 0.0032979401770712076),
)

LINRGB_FROM_SCALED_DISCOUNT = (
    (1373.2198709594231, -1100.4251190754821, -7.278681089101213),
    (-271.815969077903, 559.6580465940733, -32.46047482791194),
    (1.9622899599665666, -57.173814538844006, 308.7233197812385),
)

Y_FROM_LINRGB = (0.2126, 0.7152, 0.0722)

CRITICAL_PLANES = (
    0.015176349177441876, 0.045529047532325624, 0.07588174588720938,
    0.10623444424209313, 0.13658714259697685, 0.16693984095186062,
    0.19729253930674434, 0.2276452376616281, 0.2579979360165119,
    0.28835063437139563, 0.3188300904430532, 0.350925934958123,
    0.3848314933096426, 0.42057480301049466, 0.458183274052838,
    0.4976837250274023, 0.5391024159806381, 0.5824650784040898,
    0.6277969426914107, 0.6751227633498623, 0.7244668422128921,
    0.775853049866786, 0.829304845476233, 0.8848452951698498,
    0.942497089126609, 1.0022825574869039, 1.0642236851973577,
    1.1283421258858297, 1.1946592148522128, 1.2631959812511864,
    1.3339731595349034, 1.407011200216447, 1.4823302800086415,
    1.5599503113873272, 1.6398909516233677, 1.7221716113234105,
    1.8068114625156377, 1.8938294463134073, 1.9832442801866852,
    2.075074464868551, 2.1693382909216234, 2.2660538449872063,
    2.36523901573795, 2.4669114995532007, 2.5710888059345764,
    2.6777882626779785, 2.7870270208169257, 2.898822059350997,
    3.0131901897720907, 3.1301480604002863, 3.2497121605402226,
    3.3718988244681087, 3.4967242352587946, 3.624204428461639,
    3.754355295633311, 3.887192587735158, 4.022731918402185,
    4.160988767090289, 4.301978482107941, 4.445716283538092,
    4.592217266055746, 4.741496401646282, 4.893568542229298,
    5.048448422192488, 5.20615066083972, 5.3666897647573375,
    5.5300801301023865, 5.696336044816294, 5.865471690767354,
    6.037501145825082, 6.212438385869475, 6.390297286737924,
    6.571091626112461, 6.7548350853498045, 6.941541251256611,
    7.131223617812143, 7.323895587840543, 7.5195704746346665,
    7.7182615035334345, 7.919981813454504, 8.124744458384042,
    8.332562408825165, 8.543448553206703, 8.757415699253682,
    8.974476575321063, 9.194643831691977, 9.417930041841839,
    9.644347703669503, 9.873909240696694, 10.106627003236781,
    10.342513269534024, 10.58158024687427, 10.8238400726681,
    11.069304815507364, 11.317986476196008, 11.569896988756009,
    11.825048221409341, 12.083451977536606, 12.345119996613247,
    12.610063955123938, 12.878295467455942, 13.149826086772048,
    13.42466730586372, 13.702830557985108, 13.984327217668513,
    14.269168601521828, 14.55736596900856, 14.848930523210871,
    15.143873411576273, 15.44220572664832, 15.743938506781891,
    16.04908273684337, 16.35764934889634, 16.66964922287304,
    16.985093187232053, 17.30399201960269, 17.62635644741625,
    17.95219714852476, 18.281524751807332, 18.614349837764564,
    18.95068293910138, 19.290534541298456, 19.633915083172692,
    19.98083495742689, 20.331304511189067, 20.685334046541502,
    21.042933821039977, 21.404114048223256, 21.76888489811322,
    22.137256497705877, 22.50923893145328, 22.884842241736916,
    23.264076429332462, 23.6469514538663, 24.033477234264016,
    24.42366364919083, 24.817520537484558, 25.21505769858089,
    25.61628489293138, 26.021211842414342, 26.429848230738664,
    26.842203703840827, 27.258287870275353, 27.678110301598522,
    28.10168053274597, 28.529008062403893, 28.96010235337422,
    29.39497283293396, 29.83362889318845, 30.276079891419332,
    30.722335150426627, 31.172403958865512, 31.62629557157785,
    32.08401920991837, 32.54558406207592, 33.010999283389665,
    33.4802739966603, 33.953417292456834, 34.430438229418264,
    34.911345834551085, 35.39614910352207, 35.88485700094671,
    36.37747846067349, 36.87402238606382, 37.37449765026789,
    37.87891309649659, 38.38727753828926, 38.89959975977785,
    39.41588851594697, 39.93615253289054, 40.460400508064545,
    40.98864111053629, 41.520882981230194, 42.05713473317016,
    42.597404951718396, 43.141702194811224, 43.6900349931913,
    44.24241185063697, 44.798841244188324, 45.35933162429004,
    45.9238914150275, 46.492529014366246, 47.065252794385046,
    47.64207110150265, 48.22299225670853, 48.80802455580172,
    49.39717626962773, 49.99045564431377, 50.587870901502655,
    51.18943023858524, 51.795141828931015, 52.40501382211622,
    53.01905434414925, 53.63727149769373, 54.25967336229057,
    54.88626799457913, 55.51706342851751, 56.15206767559195,
    56.79128872503457, 57.43473454404029, 58.08241307798374,
    58.73433225063587, 59.39049996437927, 60.05092410042254,
    60.715612519013825, 61.384573059654815, 62.0578135413135,
    62.735341762637835, 63.41716550216888, 64.10329251855351,
    64.7937305507569, 65.48848731827564, 66.18757052134946,
    66.89098784117393, 67.5987469401116, 68.3108554619044,
    69.02732103188626, 69.74815125719155, 70.47335372696505,
    71.20293601257253, 71.93690566779976, 72.67527022905559,
    73.41803711557042, 74.16521382959137, 74.91680785657107,
    75.67282666535208, 76.4332777083467, 77.1981684217121,
    77.96750622552105, 78.74129852392784, 79.51955270533015,
    80.30227614252548, 81.08947619286588, 81.88116019840942,
    82.67733548606896, 83.47800936775866, 84.2831891405383,
    85.09288208675498, 85.90709547418204, 86.72583655615548,
    87.54911257170744, 88.37693074570615, 89.20929828898212,
    90.04622239845142, 90.88771025724523, 91.73376903483619,
    92.58440588716114, 93.43962795674011, 94.2994423727912,
    95.16385625134173, 96.03287679533522, 96.9065110947403,
    97.78476622666346, 98.66764925546465, 99.5551672328759,
)


# ---------------------------------------------------------------------------
# Low-level colour space helpers (sRGB <-> Linear <-> XYZ <-> L*a*b*)
# ---------------------------------------------------------------------------

def _clamp(lo: float, hi: float, x: float) -> float:
    return lo if x < lo else (hi if x > hi else x)


def _clamp_int(lo: int, hi: int, x: int) -> int:
    return lo if x < lo else (hi if x > hi else x)


def _signum(x: float) -> float:
    return 1.0 if x > 0 else (-1.0 if x < 0 else 0.0)


def _lerp(start: float, stop: float, amount: float) -> float:
    return (1.0 - amount) * start + amount * stop


def _sanitize_degrees(deg: float) -> float:
    deg = deg % 360.0
    return deg + 360.0 if deg < 0.0 else deg


def _sanitize_radians(rad: float) -> float:
    return (rad % (2.0 * math.pi) + 2.0 * math.pi) % (2.0 * math.pi)


def _matmul(vec: tuple[float, float, float], mat: tuple[tuple[float, float, float], ...]) -> tuple[float, float, float]:
    return (
        vec[0] * mat[0][0] + vec[1] * mat[0][1] + vec[2] * mat[0][2],
        vec[0] * mat[1][0] + vec[1] * mat[1][1] + vec[2] * mat[1][2],
        vec[0] * mat[2][0] + vec[1] * mat[2][1] + vec[2] * mat[2][2],
    )


def _linearized(rgb_component: int) -> float:
    normalized = rgb_component / 255.0
    if normalized <= 0.040449936:
        return normalized / 12.92 * 100.0
    return ((normalized + 0.055) / 1.055) ** 2.4 * 100.0


def _delinearized(rgb_component: float) -> int:
    normalized = rgb_component / 100.0
    if normalized <= 0.0031308:
        out = normalized * 12.92
    else:
        out = 1.055 * (normalized ** (1.0 / 2.4)) - 0.055
    return _clamp_int(0, 255, round(out * 255.0))


def _true_delinearized(rgb_component: float) -> float:
    normalized = rgb_component / 100.0
    if normalized <= 0.0031308:
        out = normalized * 12.92
    else:
        out = 1.055 * (normalized ** (1.0 / 2.4)) - 0.055
    return out * 255.0


def _argb_from_rgb(r: int, g: int, b: int) -> int:
    return (0xFF << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)


def _argb_from_linrgb(linrgb: tuple[float, float, float]) -> int:
    return _argb_from_rgb(
        _delinearized(linrgb[0]),
        _delinearized(linrgb[1]),
        _delinearized(linrgb[2]),
    )


def hex_to_argb(hex_color: str) -> int:
    cleaned = hex_color.strip().lstrip("#")
    if len(cleaned) == 3:
        cleaned = "".join(c * 2 for c in cleaned)
    if len(cleaned) != 6:
        raise ValueError(f"Expected 6-digit hex colour, got {hex_color!r}")
    val = int(cleaned, 16)
    return (0xFF << 24) | val


def argb_to_hex(argb: int) -> str:
    return f"#{(argb & 0xFFFFFF):06X}"


def _lab_f(t: float) -> float:
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    return math.copysign(abs(t) ** (1.0 / 3.0), t) if t > e else (kappa * t + 16.0) / 116.0


def _lab_invf(ft: float) -> float:
    e = 216.0 / 24389.0
    kappa = 24389.0 / 27.0
    ft3 = ft * ft * ft
    return ft3 if ft3 > e else (116.0 * ft - 16.0) / kappa


def y_from_lstar(lstar: float) -> float:
    return 100.0 * _lab_invf((lstar + 16.0) / 116.0)


def lstar_from_y(y: float) -> float:
    return 116.0 * _lab_f(y / 100.0) - 16.0


def lstar_from_argb(argb: int) -> float:
    r = _linearized((argb >> 16) & 0xFF)
    g = _linearized((argb >> 8) & 0xFF)
    b = _linearized(argb & 0xFF)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 116.0 * _lab_f(y / 100.0) - 16.0


def argb_from_lstar(lstar: float) -> int:
    y = y_from_lstar(lstar)
    c = _delinearized(y)
    return _argb_from_rgb(c, c, c)


def lab_from_argb(argb: int) -> tuple[float, float, float]:
    r = _linearized((argb >> 16) & 0xFF)
    g = _linearized((argb >> 8) & 0xFF)
    b = _linearized(argb & 0xFF)
    x, y, z = _matmul((r, g, b), SRGB_TO_XYZ)
    fx = _lab_f(x / WHITE_POINT_D65[0])
    fy = _lab_f(y / WHITE_POINT_D65[1])
    fz = _lab_f(z / WHITE_POINT_D65[2])
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def argb_from_lab(l_val: float, a_val: float, b_val: float) -> int:
    fy = (l_val + 16.0) / 116.0
    fx = a_val / 500.0 + fy
    fz = fy - b_val / 200.0
    x = _lab_invf(fx) * WHITE_POINT_D65[0]
    y = _lab_invf(fy) * WHITE_POINT_D65[1]
    z = _lab_invf(fz) * WHITE_POINT_D65[2]
    linrgb = _matmul((x, y, z), XYZ_TO_SRGB)
    return _argb_from_linrgb(linrgb)


# ---------------------------------------------------------------------------
# MCU Image Quantization (QuantizerWu + QuantizerWsmeans + QuantizerCelebi)
# & Suitability Scoring (Score)
# ---------------------------------------------------------------------------

_WU_INDEX_BITS = 5
_WU_SIDE_LENGTH = 33
_WU_TOTAL_SIZE = 35937  # 33^3
_WSMEANS_MAX_ITERATIONS = 10
_WSMEANS_MIN_MOVEMENT_DISTANCE = 3.0


class _DeterministicRandom:
    """Portable 32-bit LCG shared with md3e-dynamic-color.js for exact parity."""

    def __init__(self, seed: int = 0x42688) -> None:
        self._state = seed & 0xFFFFFFFF

    def next_float(self) -> float:
        self._state = (self._state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self._state / 4294967296.0


@dataclass
class _WuBox:
    r0: int = 0
    r1: int = 0
    g0: int = 0
    g1: int = 0
    b0: int = 0
    b1: int = 0
    vol: int = 0


class QuantizerWu:
    """Xiaolin Wu's orthogonal RGB colour cube quantizer matching MCU."""

    @staticmethod
    def _idx(r: int, g: int, b: int) -> int:
        return (r << (_WU_INDEX_BITS * 2)) + (r << (_WU_INDEX_BITS + 1)) + r + (g << _WU_INDEX_BITS) + g + b

    def _volume(self, cube: _WuBox, m: list[int]) -> int:
        idx = self._idx
        return (
            m[idx(cube.r1, cube.g1, cube.b1)]
            - m[idx(cube.r1, cube.g1, cube.b0)]
            - m[idx(cube.r1, cube.g0, cube.b1)]
            + m[idx(cube.r1, cube.g0, cube.b0)]
            - m[idx(cube.r0, cube.g1, cube.b1)]
            + m[idx(cube.r0, cube.g1, cube.b0)]
            + m[idx(cube.r0, cube.g0, cube.b1)]
            - m[idx(cube.r0, cube.g0, cube.b0)]
        )

    def _bottom(self, cube: _WuBox, direction: int, m: list[int]) -> int:
        idx = self._idx
        if direction == 0:
            return -m[idx(cube.r0, cube.g1, cube.b1)] + m[idx(cube.r0, cube.g1, cube.b0)] + m[idx(cube.r0, cube.g0, cube.b1)] - m[idx(cube.r0, cube.g0, cube.b0)]
        if direction == 1:
            return -m[idx(cube.r1, cube.g0, cube.b1)] + m[idx(cube.r1, cube.g0, cube.b0)] + m[idx(cube.r0, cube.g0, cube.b1)] - m[idx(cube.r0, cube.g0, cube.b0)]
        return -m[idx(cube.r1, cube.g1, cube.b0)] + m[idx(cube.r1, cube.g0, cube.b0)] + m[idx(cube.r0, cube.g1, cube.b0)] - m[idx(cube.r0, cube.g0, cube.b0)]

    def _top(self, cube: _WuBox, direction: int, pos: int, m: list[int]) -> int:
        idx = self._idx
        if direction == 0:
            return m[idx(pos, cube.g1, cube.b1)] - m[idx(pos, cube.g1, cube.b0)] - m[idx(pos, cube.g0, cube.b1)] + m[idx(pos, cube.g0, cube.b0)]
        if direction == 1:
            return m[idx(cube.r1, pos, cube.b1)] - m[idx(cube.r1, pos, cube.b0)] - m[idx(cube.r0, pos, cube.b1)] + m[idx(cube.r0, pos, cube.b0)]
        return m[idx(cube.r1, cube.g1, pos)] - m[idx(cube.r1, cube.g0, pos)] - m[idx(cube.r0, cube.g1, pos)] + m[idx(cube.r0, cube.g0, pos)]

    def _variance(self, cube: _WuBox) -> float:
        idx = self._idx
        dr = self._volume(cube, self.moments_r)
        dg = self._volume(cube, self.moments_g)
        db = self._volume(cube, self.moments_b)
        xx = (
            self.moments[idx(cube.r1, cube.g1, cube.b1)]
            - self.moments[idx(cube.r1, cube.g1, cube.b0)]
            - self.moments[idx(cube.r1, cube.g0, cube.b1)]
            + self.moments[idx(cube.r1, cube.g0, cube.b0)]
            - self.moments[idx(cube.r0, cube.g1, cube.b1)]
            + self.moments[idx(cube.r0, cube.g1, cube.b0)]
            + self.moments[idx(cube.r0, cube.g0, cube.b1)]
            - self.moments[idx(cube.r0, cube.g0, cube.b0)]
        )
        hyp = dr * dr + dg * dg + db * db
        vol = self._volume(cube, self.weights)
        return xx - (hyp / vol)

    def _maximize(
        self,
        cube: _WuBox,
        direction: int,
        first: int,
        last: int,
        whole_r: int,
        whole_g: int,
        whole_b: int,
        whole_w: int,
    ) -> tuple[int, float]:
        bot_r = self._bottom(cube, direction, self.moments_r)
        bot_g = self._bottom(cube, direction, self.moments_g)
        bot_b = self._bottom(cube, direction, self.moments_b)
        bot_w = self._bottom(cube, direction, self.weights)
        max_val = 0.0
        cut_loc = -1
        for i in range(first, last):
            half_r = bot_r + self._top(cube, direction, i, self.moments_r)
            half_g = bot_g + self._top(cube, direction, i, self.moments_g)
            half_b = bot_b + self._top(cube, direction, i, self.moments_b)
            half_w = bot_w + self._top(cube, direction, i, self.weights)
            if half_w == 0:
                continue
            temp = (half_r * half_r + half_g * half_g + half_b * half_b) / half_w
            rem_r = whole_r - half_r
            rem_g = whole_g - half_g
            rem_b = whole_b - half_b
            rem_w = whole_w - half_w
            if rem_w == 0:
                continue
            temp += (rem_r * rem_r + rem_g * rem_g + rem_b * rem_b) / rem_w
            if temp > max_val:
                max_val = temp
                cut_loc = i
        return cut_loc, max_val

    def _cut(self, one: _WuBox, two: _WuBox) -> bool:
        whole_r = self._volume(one, self.moments_r)
        whole_g = self._volume(one, self.moments_g)
        whole_b = self._volume(one, self.moments_b)
        whole_w = self._volume(one, self.weights)
        cut_r, max_r = self._maximize(one, 0, one.r0 + 1, one.r1, whole_r, whole_g, whole_b, whole_w)
        cut_g, max_g = self._maximize(one, 1, one.g0 + 1, one.g1, whole_r, whole_g, whole_b, whole_w)
        cut_b, max_b = self._maximize(one, 2, one.b0 + 1, one.b1, whole_r, whole_g, whole_b, whole_w)

        two.r1, two.g1, two.b1 = one.r1, one.g1, one.b1
        if max_r >= max_g and max_r >= max_b:
            if cut_r < 0:
                return False
            one.r1 = cut_r
            two.r0, two.g0, two.b0 = cut_r, one.g0, one.b0
        elif max_g >= max_r and max_g >= max_b:
            one.g1 = cut_g
            two.r0, two.g0, two.b0 = one.r0, cut_g, one.b0
        else:
            one.b1 = cut_b
            two.r0, two.g0, two.b0 = one.r0, one.g0, cut_b

        one.vol = (one.r1 - one.r0) * (one.g1 - one.g0) * (one.b1 - one.b0)
        two.vol = (two.r1 - two.r0) * (two.g1 - two.g0) * (two.b1 - two.b0)
        return True

    def quantize(self, pixels: list[int], max_colors: int = 128) -> list[int]:
        if not pixels:
            return []
        self.weights = [0] * _WU_TOTAL_SIZE
        self.moments_r = [0] * _WU_TOTAL_SIZE
        self.moments_g = [0] * _WU_TOTAL_SIZE
        self.moments_b = [0] * _WU_TOTAL_SIZE
        self.moments = [0] * _WU_TOTAL_SIZE

        counts: dict[int, int] = {}
        for px in pixels:
            counts[px] = counts.get(px, 0) + 1

        bits_remove = 8 - _WU_INDEX_BITS
        idx_fn = self._idx
        for px, cnt in counts.items():
            red = (px >> 16) & 0xFF
            green = (px >> 8) & 0xFF
            blue = px & 0xFF
            index = idx_fn((red >> bits_remove) + 1, (green >> bits_remove) + 1, (blue >> bits_remove) + 1)
            self.weights[index] += cnt
            self.moments_r[index] += cnt * red
            self.moments_g[index] += cnt * green
            self.moments_b[index] += cnt * blue
            self.moments[index] += cnt * (red * red + green * green + blue * blue)

        for r in range(1, _WU_SIDE_LENGTH):
            area = [0] * _WU_SIDE_LENGTH
            area_r = [0] * _WU_SIDE_LENGTH
            area_g = [0] * _WU_SIDE_LENGTH
            area_b = [0] * _WU_SIDE_LENGTH
            area2 = [0] * _WU_SIDE_LENGTH
            for g in range(1, _WU_SIDE_LENGTH):
                line = line_r = line_g = line_b = line2 = 0
                for b in range(1, _WU_SIDE_LENGTH):
                    index = idx_fn(r, g, b)
                    line += self.weights[index]
                    line_r += self.moments_r[index]
                    line_g += self.moments_g[index]
                    line_b += self.moments_b[index]
                    line2 += self.moments[index]
                    area[b] += line
                    area_r[b] += line_r
                    area_g[b] += line_g
                    area_b[b] += line_b
                    area2[b] += line2
                    prev_idx = idx_fn(r - 1, g, b)
                    self.weights[index] = self.weights[prev_idx] + area[b]
                    self.moments_r[index] = self.moments_r[prev_idx] + area_r[b]
                    self.moments_g[index] = self.moments_g[prev_idx] + area_g[b]
                    self.moments_b[index] = self.moments_b[prev_idx] + area_b[b]
                    self.moments[index] = self.moments[prev_idx] + area2[b]

        cubes = [_WuBox() for _ in range(max_colors)]
        cubes[0].r1 = cubes[0].g1 = cubes[0].b1 = _WU_SIDE_LENGTH - 1
        vol_var = [0.0] * max_colors
        generated = max_colors
        nxt = 0
        i = 1
        while i < max_colors:
            if self._cut(cubes[nxt], cubes[i]):
                vol_var[nxt] = self._variance(cubes[nxt]) if cubes[nxt].vol > 1 else 0.0
                vol_var[i] = self._variance(cubes[i]) if cubes[i].vol > 1 else 0.0
            else:
                vol_var[nxt] = 0.0
                i -= 1
            nxt = 0
            best_v = vol_var[0]
            for j in range(1, i + 1):
                if vol_var[j] > best_v:
                    best_v = vol_var[j]
                    nxt = j
            if best_v <= 0.0:
                generated = i + 1
                break
            i += 1

        results: list[int] = []
        for k in range(generated):
            cube = cubes[k]
            w = self._volume(cube, self.weights)
            if w > 0:
                r = round(self._volume(cube, self.moments_r) / w)
                g = round(self._volume(cube, self.moments_g) / w)
                b = round(self._volume(cube, self.moments_b) / w)
                results.append(_argb_from_rgb(r, g, b))
        return results


def _quantize_wsmeans(input_pixels: list[int], starting_clusters: list[int], max_colors: int) -> dict[int, int]:
    if not input_pixels:
        return {}
    pixel_to_count: dict[int, int] = {}
    points: list[tuple[float, float, float]] = []
    counts: list[int] = []
    for px in input_pixels:
        prev = pixel_to_count.get(px)
        if prev is None:
            pixel_to_count[px] = 1
            points.append(lab_from_argb(px))
        else:
            pixel_to_count[px] = prev + 1
    point_count = len(pixel_to_count)
    counts = [pixel_to_count[px] for px in pixel_to_count]

    cluster_count = min(max_colors, point_count)
    if starting_clusters:
        cluster_count = min(cluster_count, len(starting_clusters))

    clusters: list[tuple[float, float, float]] = [lab_from_argb(c) for c in starting_clusters[:cluster_count]]
    rng = _DeterministicRandom(0x42688)
    while len(clusters) < cluster_count:
        clusters.append((rng.next_float() * 100.0, rng.next_float() * 201.0 - 100.0, rng.next_float() * 201.0 - 100.0))

    cluster_indices = [math.floor(rng.next_float() * cluster_count) for _ in range(point_count)]
    pixel_count_sums = [0] * cluster_count

    for iteration in range(_WSMEANS_MAX_ITERATIONS):
        dist_matrix: list[list[tuple[float, int]]] = [[(0.0, j) for j in range(cluster_count)] for _ in range(cluster_count)]
        for i in range(cluster_count):
            cl_i = clusters[i]
            for j in range(i + 1, cluster_count):
                cl_j = clusters[j]
                dl = cl_i[0] - cl_j[0]
                da = cl_i[1] - cl_j[1]
                db = cl_i[2] - cl_j[2]
                d = dl * dl + da * da + db * db
                dist_matrix[j][i] = (d, i)
                dist_matrix[i][j] = (d, j)
            dist_matrix[i].sort(key=lambda item: (item[0], item[1]))

        points_moved = 0
        for i in range(point_count):
            p0, p1, p2 = points[i]
            prev_c = cluster_indices[i]
            c0, c1, c2 = clusters[prev_c]
            prev_dist = (p0 - c0) ** 2 + (p1 - c1) ** 2 + (p2 - c2) ** 2
            min_dist = prev_dist
            new_c = -1
            for dist_val, j in dist_matrix[prev_c]:
                if dist_val >= 4.0 * prev_dist:
                    break
                cj0, cj1, cj2 = clusters[j]
                d = (p0 - cj0) ** 2 + (p1 - cj1) ** 2 + (p2 - cj2) ** 2
                if d < min_dist:
                    min_dist = d
                    new_c = j
            if new_c != -1:
                dist_change = abs(math.sqrt(min_dist) - math.sqrt(prev_dist))
                if dist_change > _WSMEANS_MIN_MOVEMENT_DISTANCE:
                    points_moved += 1
                    cluster_indices[i] = new_c

        if points_moved == 0 and iteration != 0:
            break

        comp_a = [0.0] * cluster_count
        comp_b = [0.0] * cluster_count
        comp_c = [0.0] * cluster_count
        for i in range(cluster_count):
            pixel_count_sums[i] = 0
        for i in range(point_count):
            ci = cluster_indices[i]
            cnt = counts[i]
            p0, p1, p2 = points[i]
            pixel_count_sums[ci] += cnt
            comp_a[ci] += p0 * cnt
            comp_b[ci] += p1 * cnt
            comp_c[ci] += p2 * cnt
        for i in range(cluster_count):
            cnt = pixel_count_sums[i]
            if cnt == 0:
                clusters[i] = (0.0, 0.0, 0.0)
            else:
                clusters[i] = (comp_a[i] / cnt, comp_b[i] / cnt, comp_c[i] / cnt)

    out: dict[int, int] = {}
    for i in range(cluster_count):
        cnt = pixel_count_sums[i]
        if cnt == 0:
            continue
        argb = argb_from_lab(*clusters[i])
        if argb not in out:
            out[argb] = cnt
    return out


def quantize_celebi(pixels: list[int], max_colors: int = 128) -> dict[int, int]:
    """Run two-stage MCU QuantizerCelebi (Wu + Wsmeans)."""
    if not pixels:
        return {}
    wu_clusters = QuantizerWu().quantize(pixels, max_colors)
    return _quantize_wsmeans(pixels, wu_clusters, max_colors)


def score_colors(
    colors_to_population: dict[int, int],
    *,
    desired: int = 4,
    fallback_argb: int = 0xFF6750A4,
    filter_unsuitable: bool = True,
) -> list[dict[str, object]]:
    """Rank quantized colours with official MCU Score weights & hue deduplication."""
    if not colors_to_population:
        hct = Hct.from_int(fallback_argb)
        return [{
            "argb": fallback_argb,
            "hex": argb_to_hex(fallback_argb),
            "hue": round(hct.hue, 2),
            "chroma": round(hct.chroma, 2),
            "tone": round(hct.tone, 2),
            "population": 0,
            "score": 0.0,
        }]

    hue_pop = [0] * 360
    pop_sum = 0
    entries: list[tuple[int, Hct, int]] = []
    for argb, pop in colors_to_population.items():
        hct = Hct.from_int(argb)
        entries.append((argb, hct, pop))
        hue_idx = math.floor(hct.hue) % 360
        hue_pop[hue_idx] += pop
        pop_sum += pop

    if pop_sum <= 0:
        pop_sum = 1

    hue_excited = [0.0] * 360
    for h in range(360):
        prop = hue_pop[h] / pop_sum
        for i in range(h - 14, h + 16):
            hue_excited[i % 360] += prop

    scored: list[tuple[float, int, Hct, int]] = []
    for argb, hct, pop in entries:
        hue_round = math.floor(hct.hue + 0.5) % 360
        prop = hue_excited[hue_round]
        if filter_unsuitable and (hct.chroma < 5.0 or prop <= 0.01):
            continue
        prop_score = prop * 100.0 * 0.7
        chroma_weight = 0.1 if hct.chroma < 48.0 else 0.3
        chroma_score = (hct.chroma - 48.0) * chroma_weight
        scored.append((prop_score + chroma_score, argb, hct, pop))

    scored.sort(key=lambda item: (-item[0], -item[1]))

    chosen: list[tuple[float, int, Hct, int]] = []
    for diff_deg in range(90, 14, -1):
        chosen.clear()
        for item in scored:
            cand_h = item[2].hue
            if not any((180.0 - abs(abs(cand_h - ch[2].hue) - 180.0)) < diff_deg for ch in chosen):
                chosen.append(item)
            if len(chosen) >= desired:
                break
        if len(chosen) >= desired:
            break

    if not chosen:
        hct = Hct.from_int(fallback_argb)
        return [{
            "argb": fallback_argb,
            "hex": argb_to_hex(fallback_argb),
            "hue": round(hct.hue, 2),
            "chroma": round(hct.chroma, 2),
            "tone": round(hct.tone, 2),
            "population": 0,
            "score": 0.0,
        }]

    return [
        {
            "argb": argb,
            "hex": argb_to_hex(argb),
            "hue": round(hct.hue, 2),
            "chroma": round(hct.chroma, 2),
            "tone": round(hct.tone, 2),
            "population": pop,
            "score": round(sc, 2),
        }
        for sc, argb, hct, pop in chosen
    ]


def extract_seeds_from_rgba(
    rgba_bytes: bytes | bytearray | memoryview,
    *,
    desired: int = 4,
    max_colors: int = 128,
) -> list[dict[str, object]]:
    """Extract ranked Material seed candidates from raw RGBA byte buffers."""
    mv = memoryview(rgba_bytes)
    opaque_pixels: list[int] = []
    translucent_pixels: list[int] = []
    for i in range(0, len(mv) - 3, 4):
        a = mv[i + 3]
        if a == 255:
            opaque_pixels.append(_argb_from_rgb(mv[i], mv[i + 1], mv[i + 2]))
        elif a >= 64:
            translucent_pixels.append(_argb_from_rgb(mv[i], mv[i + 1], mv[i + 2]))
    pixels = opaque_pixels if len(opaque_pixels) >= 16 else (opaque_pixels + translucent_pixels)
    quantized = quantize_celebi(pixels, max_colors=max_colors)
    return score_colors(quantized, desired=desired)


def _decode_image_rgba_stdlib(image_path: pathlib.Path, max_dimension: int = 128) -> bytes:
    """Pure-stdlib RGBA decoder (PNG / BMP / PPM) with nearest/box downscale when Pillow is absent."""
    import struct
    import zlib

    raw = image_path.read_bytes()
    width = height = 0
    rgba = bytearray()

    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        pos = 8
        idat_chunks: list[bytes] = []
        bit_depth = color_type = 0
        plte = b""
        while pos + 8 <= len(raw):
            length, chunk_type = struct.unpack(">I4s", raw[pos:pos + 8])
            data = raw[pos + 8:pos + 8 + length]
            pos += 12 + length
            if chunk_type == b"IHDR":
                width, height, bit_depth, color_type, comp, filt, interlace = struct.unpack(">IIBBBBB", data)
                if bit_depth != 8 or comp != 0 or filt != 0 or interlace != 0:
                    raise ValueError(f"Unsupported PNG encoding in {image_path}; install Pillow for interlaced/16-bit PNGs")
            elif chunk_type == b"PLTE":
                plte = data
            elif chunk_type == b"IDAT":
                idat_chunks.append(data)
            elif chunk_type == b"IEND":
                break

        bpp_map = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
        if color_type not in bpp_map:
            raise ValueError(f"Unsupported PNG colour type {color_type}")
        bpp = bpp_map[color_type]
        stride = width * bpp
        decompressed = zlib.decompress(b"".join(idat_chunks))
        prev_row = bytearray(stride)
        rgba = bytearray(width * height * 4)

        def paeth(a: int, b: int, c: int) -> int:
            p = a + b - c
            pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
            return a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)

        off = 0
        for y in range(height):
            ftype = decompressed[off]
            off += 1
            row = bytearray(decompressed[off:off + stride])
            off += stride
            for x in range(stride):
                left = row[x - bpp] if x >= bpp else 0
                up = prev_row[x]
                up_left = prev_row[x - bpp] if x >= bpp else 0
                if ftype == 1:
                    row[x] = (row[x] + left) & 0xFF
                elif ftype == 2:
                    row[x] = (row[x] + up) & 0xFF
                elif ftype == 3:
                    row[x] = (row[x] + ((left + up) >> 1)) & 0xFF
                elif ftype == 4:
                    row[x] = (row[x] + paeth(left, up, up_left)) & 0xFF
                elif ftype != 0:
                    raise ValueError(f"Invalid PNG filter {ftype}")
            prev_row = row
            out_base = y * width * 4
            for x in range(width):
                px_off = x * bpp
                out_off = out_base + x * 4
                if color_type == 6:
                    rgba[out_off:out_off + 4] = row[px_off:px_off + 4]
                elif color_type == 2:
                    rgba[out_off:out_off + 3] = row[px_off:px_off + 3]
                    rgba[out_off + 3] = 255
                elif color_type == 3:
                    idx = row[px_off] * 3
                    rgba[out_off:out_off + 3] = plte[idx:idx + 3]
                    rgba[out_off + 3] = 255
                elif color_type == 4:
                    v = row[px_off]
                    rgba[out_off] = rgba[out_off + 1] = rgba[out_off + 2] = v
                    rgba[out_off + 3] = row[px_off + 1]
                else:
                    v = row[px_off]
                    rgba[out_off] = rgba[out_off + 1] = rgba[out_off + 2] = v
                    rgba[out_off + 3] = 255
    elif raw[:2] == b"BM" and len(raw) >= 54:
        pixel_offset = struct.unpack_from("<I", raw, 10)[0]
        width, raw_h = struct.unpack_from("<Ii", raw, 18)
        bpp = struct.unpack_from("<H", raw, 28)[0]
        if bpp not in (24, 32):
            raise ValueError(f"Unsupported BMP bpp {bpp}; install Pillow")
        top_down = raw_h < 0
        height = abs(raw_h)
        step = bpp // 8
        row_size = ((width * step + 3) // 4) * 4
        rgba = bytearray(width * height * 4)
        for y in range(height):
            src_y = y if top_down else (height - 1 - y)
            src_row = pixel_offset + src_y * row_size
            dst_row = y * width * 4
            for x in range(width):
                s = src_row + x * step
                d = dst_row + x * 4
                rgba[d] = raw[s + 2]
                rgba[d + 1] = raw[s + 1]
                rgba[d + 2] = raw[s]
                rgba[d + 3] = raw[s + 3] if step == 4 else 255
    elif raw[:2] == b"P6":
        import re as _re
        tokens = _re.match(rb"P6\s+(?:#[^\n]*\n\s*)*(\d+)\s+(?:#[^\n]*\n\s*)*(\d+)\s+(?:#[^\n]*\n\s*)*(\d+)\s", raw)
        if not tokens:
            raise ValueError("Invalid PPM P6 header")
        width, height, maxval = int(tokens.group(1)), int(tokens.group(2)), int(tokens.group(3))
        if maxval != 255:
            raise ValueError("Only 8-bit PPM supported without Pillow")
        body = raw[tokens.end():]
        rgba = bytearray(width * height * 4)
        for i in range(width * height):
            s = i * 3
            d = i * 4
            rgba[d:d + 3] = body[s:s + 3]
            rgba[d + 3] = 255
    else:
        raise ValueError(f"Unsupported image format for {image_path} without Pillow (install pillow)")

    if max(width, height) > max_dimension:
        scale = max_dimension / max(width, height)
        nw = max(1, round(width * scale))
        nh = max(1, round(height * scale))
        scaled = bytearray(nw * nh * 4)
        for dy in range(nh):
            sy = min(height - 1, int(dy * height / nh))
            for dx in range(nw):
                sx = min(width - 1, int(dx * width / nw))
                s_idx = (sy * width + sx) * 4
                d_idx = (dy * nw + dx) * 4
                scaled[d_idx:d_idx + 4] = rgba[s_idx:s_idx + 4]
        return bytes(scaled)
    return bytes(rgba)


def extract_seeds_from_image_file(
    image_path: pathlib.Path,
    *,
    max_dimension: int = 128,
    desired: int = 4,
) -> list[dict[str, object]]:
    """Decode any image file and extract ranked MCU dynamic colour seeds."""
    try:
        from PIL import Image, ImageOps  # type: ignore
    except ImportError:
        rgba = _decode_image_rgba_stdlib(image_path, max_dimension=max_dimension)
        return extract_seeds_from_rgba(rgba, desired=desired)

    with Image.open(image_path) as raw_img:
        img = ImageOps.exif_transpose(raw_img).convert("RGBA")
        w, h = img.size
        if max(w, h) > max_dimension:
            scale = max_dimension / max(1, w, h)
            img = img.resize(
                (max(1, round(w * scale)), max(1, round(h * scale))),
                Image.Resampling.BILINEAR,
            )
        return extract_seeds_from_rgba(img.tobytes(), desired=desired)


def srgb_contrast_ratio(hex_a: str, hex_b: str) -> float:
    def lum(h: str) -> float:
        argb = hex_to_argb(h)
        r = _linearized((argb >> 16) & 0xFF) / 100.0
        g = _linearized((argb >> 8) & 0xFF) / 100.0
        b = _linearized(argb & 0xFF) / 100.0
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    la, lb = lum(hex_a), lum(hex_b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ---------------------------------------------------------------------------
# CAM16 & HCT Solver (Exact MCU ViewingConditions & Solver)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ViewingConditions:
    n: float
    aw: float
    nbb: float
    ncb: float
    c: float
    nc: float
    rgb_d: tuple[float, float, float]
    fl: float
    fl_root: float
    z: float

    @classmethod
    def default(cls) -> "ViewingConditions":
        wp = WHITE_POINT_D65
        adapting_luminance = (200.0 / math.pi) * y_from_lstar(50.0) / 100.0
        background_lstar = 50.0
        surround = 2.0
        rw = wp[0] * 0.401288 + wp[1] * 0.650173 + wp[2] * -0.051461
        gw = wp[0] * -0.250268 + wp[1] * 1.204414 + wp[2] * 0.045854
        bw = wp[0] * -0.002079 + wp[1] * 0.048952 + wp[2] * 0.953127
        f = 0.8 + surround / 10.0
        c = _lerp(0.59, 0.69, (f - 0.9) * 10.0) if f >= 0.9 else _lerp(0.525, 0.59, (f - 0.8) * 10.0)
        d = _clamp(0.0, 1.0, f * (1.0 - (1.0 / 3.6) * math.exp((-adapting_luminance - 42.0) / 92.0)))
        nc = f
        rgb_d = (
            d * (100.0 / rw) + 1.0 - d,
            d * (100.0 / gw) + 1.0 - d,
            d * (100.0 / bw) + 1.0 - d,
        )
        k = 1.0 / (5.0 * adapting_luminance + 1.0)
        k4 = k ** 4
        k4f = 1.0 - k4
        fl = k4 * adapting_luminance + 0.1 * k4f * k4f * ((5.0 * adapting_luminance) ** (1.0 / 3.0))
        n = y_from_lstar(background_lstar) / wp[1]
        z = 1.48 + math.sqrt(n)
        nbb = 0.725 / (n ** 0.2)
        ncb = nbb
        af = (
            (fl * rgb_d[0] * rw / 100.0) ** 0.42,
            (fl * rgb_d[1] * gw / 100.0) ** 0.42,
            (fl * rgb_d[2] * bw / 100.0) ** 0.42,
        )
        rgbe = tuple(400.0 * a / (a + 27.13) for a in af)
        aw = (2.0 * rgbe[0] + rgbe[1] + 0.05 * rgbe[2]) * nbb
        return cls(n, aw, nbb, ncb, c, nc, rgb_d, fl, fl ** 0.25, z)


VC_DEFAULT = ViewingConditions.default()


def cam16_from_int(argb: int, vc: ViewingConditions = VC_DEFAULT) -> tuple[float, float, float]:
    """Return (hue, chroma, j) in CAM16."""
    rl = _linearized((argb >> 16) & 0xFF)
    gl = _linearized((argb >> 8) & 0xFF)
    bl = _linearized(argb & 0xFF)
    x, y, z = _matmul((rl, gl, bl), SRGB_TO_XYZ)
    rc = 0.401288 * x + 0.650173 * y - 0.051461 * z
    gc = -0.250268 * x + 1.204414 * y + 0.045854 * z
    bc = -0.002079 * x + 0.048952 * y + 0.953127 * z
    rd, gd, bd = vc.rgb_d[0] * rc, vc.rgb_d[1] * gc, vc.rgb_d[2] * bc
    raf = (vc.fl * abs(rd) / 100.0) ** 0.42
    gaf = (vc.fl * abs(gd) / 100.0) ** 0.42
    baf = (vc.fl * abs(bd) / 100.0) ** 0.42
    ra = _signum(rd) * 400.0 * raf / (raf + 27.13)
    ga = _signum(gd) * 400.0 * gaf / (gaf + 27.13)
    ba = _signum(bd) * 400.0 * baf / (baf + 27.13)
    a = (11.0 * ra + -12.0 * ga + ba) / 11.0
    b = (ra + ga - 2.0 * ba) / 9.0
    u = (20.0 * ra + 20.0 * ga + 21.0 * ba) / 20.0
    p2 = (40.0 * ra + 20.0 * ga + ba) / 20.0
    hue = _sanitize_degrees(math.degrees(math.atan2(b, a)))
    ac = p2 * vc.nbb
    j = 100.0 * ((ac / vc.aw) ** (vc.c * vc.z))
    hue_prime = hue + 360.0 if hue < 20.14 else hue
    ehue = 0.25 * (math.cos(math.radians(hue_prime) + 2.0) + 3.8)
    p1 = (50000.0 / 13.0) * ehue * vc.nc * vc.ncb
    t = p1 * math.hypot(a, b) / (u + 0.305)
    alpha = (t ** 0.9) * ((1.64 - (0.29 ** vc.n)) ** 0.73)
    c = alpha * math.sqrt(j / 100.0)
    return (hue, c, j)


def _chromatic_adaptation(component: float) -> float:
    af = abs(component) ** 0.42
    return _signum(component) * 400.0 * af / (af + 27.13)


def _inv_chromatic_adaptation(adapted: float) -> float:
    aa = abs(adapted)
    base = max(0.0, 27.13 * aa / (400.0 - aa))
    return _signum(adapted) * (base ** (1.0 / 0.42))


def _hue_of_linrgb(linrgb: tuple[float, float, float]) -> float:
    sd = _matmul(linrgb, SCALED_DISCOUNT_FROM_LINRGB)
    ra = _chromatic_adaptation(sd[0])
    ga = _chromatic_adaptation(sd[1])
    ba = _chromatic_adaptation(sd[2])
    a = (11.0 * ra + -12.0 * ga + ba) / 11.0
    b = (ra + ga - 2.0 * ba) / 9.0
    return math.atan2(b, a)


def _in_cyclic_order(a: float, b: float, c: float) -> bool:
    return _sanitize_radians(b - a) < _sanitize_radians(c - a)


def _nth_vertex(y: float, n: int) -> tuple[float, float, float]:
    kr, kg, kb = Y_FROM_LINRGB
    ca = 0.0 if n % 4 <= 1 else 100.0
    cb = 0.0 if n % 2 == 0 else 100.0
    if n < 4:
        r = (y - ca * kg - cb * kb) / kr
        return (r, ca, cb) if 0.0 <= r <= 100.0 else (-1.0, -1.0, -1.0)
    if n < 8:
        g = (y - cb * kr - ca * kb) / kg
        return (cb, g, ca) if 0.0 <= g <= 100.0 else (-1.0, -1.0, -1.0)
    b = (y - ca * kr - cb * kg) / kb
    return (ca, cb, b) if 0.0 <= b <= 100.0 else (-1.0, -1.0, -1.0)


def _bisect_to_limit(y: float, target_hue: float) -> tuple[float, float, float]:
    left = (-1.0, -1.0, -1.0)
    right = left
    left_hue = 0.0
    initialized = False
    uncut = True
    for n in range(12):
        mid = _nth_vertex(y, n)
        if mid[0] < 0.0:
            continue
        mid_hue = _hue_of_linrgb(mid)
        if not initialized:
            left = right = mid
            left_hue = mid_hue
            initialized = True
            continue
        right_hue = _hue_of_linrgb(right)
        if uncut or _in_cyclic_order(left_hue, mid_hue, right_hue):
            uncut = False
            if _in_cyclic_order(left_hue, target_hue, mid_hue):
                right = mid
            else:
                left = mid
                left_hue = mid_hue

    for axis in range(3):
        if left[axis] == right[axis]:
            continue
        if left[axis] < right[axis]:
            l_plane = math.floor(_true_delinearized(left[axis]) - 0.5)
            r_plane = math.ceil(_true_delinearized(right[axis]) - 0.5)
        else:
            l_plane = math.ceil(_true_delinearized(left[axis]) - 0.5)
            r_plane = math.floor(_true_delinearized(right[axis]) - 0.5)
        for _ in range(8):
            if abs(r_plane - l_plane) <= 1:
                break
            m_plane = math.floor((l_plane + r_plane) / 2)
            coord = CRITICAL_PLANES[max(0, min(len(CRITICAL_PLANES) - 1, m_plane))]
            t = (coord - left[axis]) / (right[axis] - left[axis])
            mid = (
                left[0] + (right[0] - left[0]) * t,
                left[1] + (right[1] - left[1]) * t,
                left[2] + (right[2] - left[2]) * t,
            )
            mid_hue = _hue_of_linrgb(mid)
            if _in_cyclic_order(left_hue, target_hue, mid_hue):
                right = mid
                r_plane = m_plane
            else:
                left = mid
                left_hue = mid_hue
                l_plane = m_plane
    return (
        (left[0] + right[0]) / 2.0,
        (left[1] + right[1]) / 2.0,
        (left[2] + right[2]) / 2.0,
    )


def _find_result_by_j(hue_rad: float, chroma: float, y: float) -> int:
    j = math.sqrt(y) * 11.0
    vc = VC_DEFAULT
    t_inner_coeff = 1.0 / ((1.64 - (0.29 ** vc.n)) ** 0.73)
    ehue = 0.25 * (math.cos(hue_rad + 2.0) + 3.8)
    p1 = ehue * (50000.0 / 13.0) * vc.nc * vc.ncb
    h_sin, h_cos = math.sin(hue_rad), math.cos(hue_rad)
    kr, kg, kb = Y_FROM_LINRGB
    for it in range(5):
        jn = j / 100.0
        alpha = 0.0 if (chroma == 0.0 or j == 0.0) else chroma / math.sqrt(jn)
        t = (alpha * t_inner_coeff) ** (1.0 / 0.9)
        ac = vc.aw * (jn ** (1.0 / vc.c / vc.z))
        p2 = ac / vc.nbb
        denom = 23.0 * p1 + 11.0 * t * h_cos + 108.0 * t * h_sin
        if denom == 0.0:
            return 0
        gamma = 23.0 * (p2 + 0.305) * t / denom
        a = gamma * h_cos
        b = gamma * h_sin
        ra = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
        ga = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
        ba = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
        if abs(ra) >= 400.0 or abs(ga) >= 400.0 or abs(ba) >= 400.0:
            return 0
        linrgb = _matmul(
            (
                _inv_chromatic_adaptation(ra),
                _inv_chromatic_adaptation(ga),
                _inv_chromatic_adaptation(ba),
            ),
            LINRGB_FROM_SCALED_DISCOUNT,
        )
        if linrgb[0] < 0.0 or linrgb[1] < 0.0 or linrgb[2] < 0.0:
            return 0
        fnj = kr * linrgb[0] + kg * linrgb[1] + kb * linrgb[2]
        if fnj <= 0.0:
            return 0
        if it == 4 or abs(fnj - y) < 0.002:
            if linrgb[0] > 100.01 or linrgb[1] > 100.01 or linrgb[2] > 100.01:
                return 0
            return _argb_from_linrgb(linrgb)
        j = j - (fnj - y) * j / (2.0 * fnj)
    return 0


def hct_solve_to_int(hue_deg: float, chroma: float, tone: float) -> int:
    if chroma < 1e-4 or tone < 1e-4 or tone > 99.9999:
        return argb_from_lstar(_clamp(0.0, 100.0, tone))
    hue_deg = _sanitize_degrees(hue_deg)
    hue_rad = math.radians(hue_deg)
    y = y_from_lstar(tone)
    exact = _find_result_by_j(hue_rad, chroma, y)
    if exact != 0:
        return exact
    return _argb_from_linrgb(_bisect_to_limit(y, hue_rad))


@dataclass(frozen=True)
class Hct:
    argb: int
    hue: float
    chroma: float
    tone: float

    @classmethod
    def from_int(cls, argb: int) -> "Hct":
        h, c, _ = cam16_from_int(argb)
        t = lstar_from_argb(argb)
        return cls(argb=argb, hue=h, chroma=c, tone=t)

    @classmethod
    def from_hct(cls, hue: float, chroma: float, tone: float) -> "Hct":
        return cls.from_int(hct_solve_to_int(hue, chroma, tone))

    @property
    def hex(self) -> str:
        return argb_to_hex(self.argb)

    @staticmethod
    def is_blue(hue: float) -> bool:
        return 250.0 <= hue < 270.0

    @staticmethod
    def is_yellow(hue: float) -> bool:
        return 105.0 <= hue < 125.0

    @staticmethod
    def is_cyan(hue: float) -> bool:
        return 170.0 <= hue < 207.0


class TonalPalette:
    def __init__(self, hue: float, chroma: float) -> None:
        self.hue = _sanitize_degrees(hue)
        self.chroma = max(0.0, chroma)
        self._cache: dict[int, int] = {}

    def tone(self, tone_val: float, chroma_multiplier: float = 1.0) -> int:
        if abs(chroma_multiplier - 1.0) < 1e-6 and abs(tone_val - round(tone_val)) < 1e-6:
            ti = int(round(tone_val))
            if ti not in self._cache:
                self._cache[ti] = hct_solve_to_int(self.hue, self.chroma, ti)
            return self._cache[ti]
        return hct_solve_to_int(self.hue, self.chroma * chroma_multiplier, tone_val)

    def get_hct(self, tone_val: float, chroma_multiplier: float = 1.0) -> Hct:
        return Hct.from_int(self.tone(tone_val, chroma_multiplier))


# ---------------------------------------------------------------------------
# MCU Dislike Analyzer, Temperature Cache & Contrast Helpers
# ---------------------------------------------------------------------------

def _is_disliked(hct: Hct) -> bool:
    return (90 <= round(hct.hue) <= 111) and (round(hct.chroma) > 16) and (round(hct.tone) < 65)


def fix_if_disliked(hct: Hct) -> Hct:
    return Hct.from_hct(hct.hue, hct.chroma, 70.0) if _is_disliked(hct) else hct


def _temperature_complement(source: Hct) -> Hct:
    hcts_by_hue = [Hct.from_hct(float(h), source.chroma, source.tone) for h in range(360)]
    temps: list[float] = []
    for c in hcts_by_hue:
        _, a, b = lab_from_argb(c.argb)
        hue = _sanitize_degrees(math.degrees(math.atan2(b, a)))
        ch = math.hypot(a, b)
        temps.append(-0.5 + 0.02 * (ch ** 1.07) * math.cos(math.radians(_sanitize_degrees(hue - 50.0))))
    indexed = sorted(range(360), key=lambda idx: temps[idx])
    coldest_idx, warmest_idx = indexed[0], indexed[-1]
    coldest_temp, warmest_temp = temps[coldest_idx], temps[warmest_idx]
    t_range = warmest_temp - coldest_temp
    if t_range == 0.0:
        return source
    src_hue = round(source.hue) % 360
    src_rel = (temps[src_hue] - coldest_temp) / t_range
    target_rel = 1.0 - src_rel

    def is_between(angle: float, a: float, b: float) -> bool:
        return (a <= angle or angle <= b) if a > b else (a <= angle <= b)

    c_hue, w_hue = float(coldest_idx), float(warmest_idx)
    s_to_w = is_between(source.hue, c_hue, w_hue)
    start_h = w_hue if s_to_w else c_hue
    end_h = c_hue if s_to_w else w_hue
    best_h = src_hue
    best_err = 1e9
    for add in range(361):
        h = int(_sanitize_degrees(start_h + add)) % 360
        if not is_between(float(h), start_h, end_h):
            continue
        rel = (temps[h] - coldest_temp) / t_range
        err = abs(target_rel - rel)
        if err < best_err:
            best_err = err
            best_h = h
    return hcts_by_hue[best_h]


class Contrast:
    @staticmethod
    def ratio_of_tones(ta: float, tb: float) -> float:
        ya = y_from_lstar(_clamp(0.0, 100.0, ta))
        yb = y_from_lstar(_clamp(0.0, 100.0, tb))
        lighter, darker = (ya, yb) if ya > yb else (yb, ya)
        return (lighter + 5.0) / (darker + 5.0)

    @staticmethod
    def lighter(tone: float, ratio: float) -> float:
        if tone < 0.0 or tone > 100.0:
            return -1.0
        dy = y_from_lstar(tone)
        ly = ratio * (dy + 5.0) - 5.0
        real = (ly + 5.0) / (dy + 5.0)
        if real < ratio and abs(real - ratio) > 0.04:
            return -1.0
        rv = lstar_from_y(ly) + 0.4
        return rv if 0.0 <= rv <= 100.0 else -1.0

    @staticmethod
    def darker(tone: float, ratio: float) -> float:
        if tone < 0.0 or tone > 100.0:
            return -1.0
        ly = y_from_lstar(tone)
        dy = (ly + 5.0) / ratio - 5.0
        real = (ly + 5.0) / (dy + 5.0)
        if real < ratio and abs(real - ratio) > 0.04:
            return -1.0
        rv = lstar_from_y(dy) - 0.4
        return rv if 0.0 <= rv <= 100.0 else -1.0

    @staticmethod
    def lighter_unsafe(tone: float, ratio: float) -> float:
        res = Contrast.lighter(tone, ratio)
        return 100.0 if res < 0.0 else res

    @staticmethod
    def darker_unsafe(tone: float, ratio: float) -> float:
        res = Contrast.darker(tone, ratio)
        return 0.0 if res < 0.0 else res


@dataclass(frozen=True)
class ContrastCurve:
    low: float
    normal: float
    medium: float
    high: float

    def get(self, level: float) -> float:
        if level <= -1.0:
            return self.low
        if level < 0.0:
            return _lerp(self.low, self.normal, level + 1.0)
        if level < 0.5:
            return _lerp(self.normal, self.medium, level / 0.5)
        if level < 1.0:
            return _lerp(self.medium, self.high, (level - 0.5) / 0.5)
        return self.high


def _get_curve_2025(default_contrast: float) -> ContrastCurve:
    if default_contrast == 1.5:
        return ContrastCurve(1.5, 1.5, 3.0, 4.5)
    if default_contrast == 3.0:
        return ContrastCurve(3.0, 3.0, 4.5, 7.0)
    if default_contrast == 4.5:
        return ContrastCurve(4.5, 4.5, 7.0, 11.0)
    if default_contrast == 6.0:
        return ContrastCurve(6.0, 6.0, 7.0, 11.0)
    if default_contrast == 7.0:
        return ContrastCurve(7.0, 7.0, 11.0, 21.0)
    if default_contrast == 9.0:
        return ContrastCurve(9.0, 9.0, 11.0, 21.0)
    if default_contrast == 11.0:
        return ContrastCurve(11.0, 11.0, 21.0, 21.0)
    if default_contrast == 21.0:
        return ContrastCurve(21.0, 21.0, 21.0, 21.0)
    return ContrastCurve(default_contrast, default_contrast, 7.0, 21.0)


def _tone_prefers_light_fg(tone: float) -> bool:
    return round(tone) < 60


def foreground_tone(bg_tone: float, ratio: float) -> float:
    lighter_t = Contrast.lighter_unsafe(bg_tone, ratio)
    darker_t = Contrast.darker_unsafe(bg_tone, ratio)
    l_ratio = Contrast.ratio_of_tones(lighter_t, bg_tone)
    d_ratio = Contrast.ratio_of_tones(darker_t, bg_tone)
    if _tone_prefers_light_fg(bg_tone):
        negligible = abs(l_ratio - d_ratio) < 0.1 and l_ratio < ratio and d_ratio < ratio
        return lighter_t if (l_ratio >= ratio or l_ratio >= d_ratio or negligible) else darker_t
    return darker_t if (d_ratio >= ratio or d_ratio >= l_ratio) else lighter_t


def _find_best_tone_for_chroma(hue: float, chroma: float, tone: float, dec: bool) -> float:
    ans = tone
    best = Hct.from_hct(hue, chroma, ans)
    while best.chroma < chroma:
        if tone < 0 or tone > 100:
            break
        tone += -1.0 if dec else 1.0
        cand = Hct.from_hct(hue, chroma, tone)
        if best.chroma < cand.chroma:
            best = cand
            ans = tone
    return ans


def t_max_c(pal: TonalPalette, lo: float = 0.0, hi: float = 100.0, mult: float = 1.0) -> float:
    ans = _find_best_tone_for_chroma(pal.hue, pal.chroma * mult, 100.0, True)
    return _clamp(lo, hi, ans)


def t_min_c(pal: TonalPalette, lo: float = 0.0, hi: float = 100.0) -> float:
    ans = _find_best_tone_for_chroma(pal.hue, pal.chroma, 0.0, False)
    return _clamp(lo, hi, ans)


def find_desired_chroma_by_tone(hue: float, chroma: float, tone: float, dec: bool) -> float:
    ans = tone
    closest = Hct.from_hct(hue, chroma, tone)
    if closest.chroma < chroma:
        peak = closest.chroma
        while closest.chroma < chroma:
            ans += -1.0 if dec else 1.0
            cand = Hct.from_hct(hue, chroma, ans)
            if peak > cand.chroma or abs(cand.chroma - chroma) < 0.4:
                break
            if abs(cand.chroma - chroma) < abs(closest.chroma - chroma):
                closest = cand
            peak = max(peak, cand.chroma)
    return ans


def _get_rotated_hue(src: Hct, bps: list[float], rots: list[float]) -> float:
    n = min(len(bps) - 1, len(rots))
    h = src.hue
    for i in range(n):
        if bps[i] <= h < bps[i + 1]:
            return _sanitize_degrees(h + rots[i])
    return h


def _get_piecewise_hue(src: Hct, bps: list[float], hues: list[float]) -> float:
    n = min(len(bps) - 1, len(hues))
    h = src.hue
    for i in range(n):
        if bps[i] <= h < bps[i + 1]:
            return _sanitize_degrees(hues[i])
    return h


# ---------------------------------------------------------------------------
# Palettes (SPEC_2021 and SPEC_2025 PHONE)
# ---------------------------------------------------------------------------

def build_palettes(
    seed_hct: Hct,
    variant: str,
    is_dark: bool,
    spec_version: str,
) -> dict[str, TonalPalette]:
    h, c = seed_hct.hue, seed_hct.chroma
    # Fallback variants without 2025 spec formulas to 2021
    effective_spec = "2021" if variant in ("monochrome", "fidelity") else spec_version

    if effective_spec == "2025":
        if variant == "neutral":
            p = TonalPalette(h, 12.0 if Hct.is_blue(h) else 8.0)
            s = TonalPalette(h, 6.0 if Hct.is_blue(h) else 4.0)
            t = TonalPalette(_get_rotated_hue(seed_hct, [0, 38, 105, 161, 204, 278, 333, 360], [-32, 26, 10, -39, 24, -15, -32]), 20.0)
            nh, nc = h, 1.4
            nvc = nc * 2.2
            ec = 50.0
        elif variant == "tonal-spot":
            p = TonalPalette(h, 26.0 if is_dark else 32.0)
            s = TonalPalette(h, 16.0)
            t = TonalPalette(_get_rotated_hue(seed_hct, [0, 20, 71, 161, 333, 360], [-40, 48, -32, 40, -32]), 28.0)
            nh, nc = h, 5.0
            nvc = nc * 1.7
            ec = 60.0
        elif variant == "expressive":
            p = TonalPalette(h, 36.0 if is_dark else 48.0)
            s = TonalPalette(_get_rotated_hue(seed_hct, [0, 105, 140, 204, 253, 278, 300, 333, 360], [-160, 155, -100, 96, -96, -156, -165, -160]), 16.0 if is_dark else 24.0)
            t = TonalPalette(_get_rotated_hue(seed_hct, [0, 105, 140, 204, 253, 278, 300, 333, 360], [-165, 160, -105, 101, -101, -160, -170, -165]), 48.0)
            nh = _get_rotated_hue(seed_hct, [0, 71, 124, 253, 278, 300, 360], [10, 0, 10, 0, 10, 0])
            nc = (6.0 if Hct.is_yellow(nh) else 14.0) if is_dark else 18.0
            nvc = nc * (1.6 if 105.0 <= nh < 125.0 else 2.3)
            ec = 64.0
        elif variant == "vibrant":
            p = TonalPalette(h, 74.0)
            s = TonalPalette(_get_rotated_hue(seed_hct, [0, 38, 105, 140, 333, 360], [-14, 10, -14, 10, -14]), 56.0)
            t = TonalPalette(_get_rotated_hue(seed_hct, [0, 38, 71, 105, 140, 161, 253, 333, 360], [-72, 35, 24, -24, 62, 50, 62, -72]), 56.0)
            nh = _get_rotated_hue(seed_hct, [0, 38, 105, 140, 333, 360], [-14, 10, -14, 10, -14])
            nc = 28.0
            nvc = nc * 1.29
            ec = 80.0
        else:
            raise ValueError(f"Unsupported variant: {variant}")

        eh = _get_piecewise_hue(seed_hct, [0, 3, 13, 23, 33, 43, 153, 273, 360], [12, 22, 32, 12, 22, 32, 22, 12])
        return {
            "primary": p, "secondary": s, "tertiary": t,
            "neutral": TonalPalette(nh, nc),
            "neutral_variant": TonalPalette(nh, nvc),
            "error": TonalPalette(eh, ec),
        }

    # 2021 Spec Palettes
    if variant == "monochrome":
        return {
            "primary": TonalPalette(h, 0.0), "secondary": TonalPalette(h, 0.0),
            "tertiary": TonalPalette(h, 0.0), "neutral": TonalPalette(h, 0.0),
            "neutral_variant": TonalPalette(h, 0.0), "error": TonalPalette(25.0, 84.0),
        }
    if variant == "neutral":
        return {
            "primary": TonalPalette(h, 12.0), "secondary": TonalPalette(h, 8.0),
            "tertiary": TonalPalette(h, 16.0), "neutral": TonalPalette(h, 2.0),
            "neutral_variant": TonalPalette(h, 2.0), "error": TonalPalette(25.0, 84.0),
        }
    if variant == "tonal-spot":
        return {
            "primary": TonalPalette(h, 36.0), "secondary": TonalPalette(h, 16.0),
            "tertiary": TonalPalette(h + 60.0, 24.0), "neutral": TonalPalette(h, 6.0),
            "neutral_variant": TonalPalette(h, 8.0), "error": TonalPalette(25.0, 84.0),
        }
    if variant == "expressive":
        s_h = _get_rotated_hue(seed_hct, [0, 21, 51, 121, 151, 191, 271, 321, 360], [45, 95, 45, 20, 45, 90, 45, 45])
        t_h = _get_rotated_hue(seed_hct, [0, 21, 51, 121, 151, 191, 271, 321, 360], [120, 120, 20, 45, 20, 15, 20, 120])
        return {
            "primary": TonalPalette(h + 240.0, 40.0), "secondary": TonalPalette(s_h, 24.0),
            "tertiary": TonalPalette(t_h, 32.0), "neutral": TonalPalette(h + 15.0, 8.0),
            "neutral_variant": TonalPalette(h + 15.0, 12.0), "error": TonalPalette(25.0, 84.0),
        }
    if variant == "vibrant":
        s_h = _get_rotated_hue(seed_hct, [0, 41, 61, 101, 131, 181, 251, 301, 360], [18, 15, 10, 12, 15, 18, 15, 12])
        t_h = _get_rotated_hue(seed_hct, [0, 41, 61, 101, 131, 181, 251, 301, 360], [35, 30, 20, 25, 30, 35, 30, 25])
        return {
            "primary": TonalPalette(h, 200.0), "secondary": TonalPalette(s_h, 24.0),
            "tertiary": TonalPalette(t_h, 32.0), "neutral": TonalPalette(h, 10.0),
            "neutral_variant": TonalPalette(h, 12.0), "error": TonalPalette(25.0, 84.0),
        }
    if variant == "fidelity":
        comp = fix_if_disliked(_temperature_complement(seed_hct))
        return {
            "primary": TonalPalette(h, c),
            "secondary": TonalPalette(h, max(c - 32.0, c * 0.5)),
            "tertiary": TonalPalette(comp.hue, comp.chroma),
            "neutral": TonalPalette(h, c / 8.0),
            "neutral_variant": TonalPalette(h, c / 8.0 + 4.0),
            "error": TonalPalette(25.0, 84.0),
        }
    raise ValueError(f"Unsupported variant: {variant}")


# ---------------------------------------------------------------------------
# DynamicColor & DynamicScheme Solver
# ---------------------------------------------------------------------------

def _solve_2025_pair(
    role_a_raw: float,
    role_b_raw: float,
    delta: float,
    polarity: str,
    constraint: str,
    is_dark: bool,
    bg_a: float | None,
    req_a: float | None,
    bg_b: float | None,
    req_b: float | None,
    *,
    role_a_has_pair: bool = False,
    role_b_has_pair: bool = True,
) -> tuple[float, float]:
    """Exact port of MCU ColorCalculationDelegateImpl2025.getTone.

    In PHONE 2025 spec, ``*_container`` is ``roleA`` and has NO toneDeltaPair
    (resolved first via its background/contrastCurve + [0..49]/[65..100] clamp),
    while the main accent (``primary`` / ``secondary`` / ``tertiary`` / ``error``)
    is ``roleB`` with ``ToneDeltaPair(container, accent, 5, "relative_lighter", "farther")``.
    """
    abs_delta = -delta if (
        polarity == "darker"
        or (polarity == "relative_lighter" and is_dark)
        or (polarity == "relative_darker" and not is_dark)
    ) else delta

    def apply_bg_and_clamp(tone_val: float, bg_t: float | None, req: float | None) -> float:
        if bg_t is not None and req is not None:
            if not (Contrast.ratio_of_tones(bg_t, tone_val) >= req):
                tone_val = foreground_tone(bg_t, req)
        return _clamp(65.0, 100.0, tone_val) if tone_val >= 57.0 else _clamp(0.0, 49.0, tone_val)

    def apply_pair(self_raw: float, ref_resolved: float, am_role_a: bool, bg_t: float | None, req: float | None) -> float:
        rel_delta = abs_delta * (1.0 if am_role_a else -1.0)
        if constraint == "exact":
            st = _clamp(0.0, 100.0, ref_resolved + rel_delta)
        elif constraint == "nearer":
            if rel_delta > 0.0:
                st = _clamp(0.0, 100.0, _clamp(ref_resolved, ref_resolved + rel_delta, self_raw))
            else:
                st = _clamp(0.0, 100.0, _clamp(ref_resolved + rel_delta, ref_resolved, self_raw))
        else:  # farther
            if rel_delta > 0.0:
                st = _clamp(ref_resolved + rel_delta, 100.0, self_raw)
            else:
                st = _clamp(0.0, ref_resolved + rel_delta, self_raw)
        return apply_bg_and_clamp(st, bg_t, req)

    # Solve non-paired anchor (roleA container) first when only roleB carries toneDeltaPair
    res_a = apply_bg_and_clamp(role_a_raw, bg_a, req_a) if not role_a_has_pair else apply_pair(role_a_raw, apply_bg_and_clamp(role_b_raw, bg_b, req_b), True, bg_a, req_a)
    res_b = apply_pair(role_b_raw, res_a, False, bg_b, req_b) if role_b_has_pair else apply_bg_and_clamp(role_b_raw, bg_b, req_b)
    return res_a, res_b


def _resolve_paired_tones(
    role_a_tone: float,
    role_b_tone: float,
    delta: float,
    polarity: str,
    constraint: str,
    is_dark: bool,
    bg_a: float | None,
    req_a: float | None,
    bg_b: float | None,
    req_b: float | None,
    a_is_bg: bool,
    b_is_bg: bool,
) -> tuple[float, float]:
    """Port of MCU ColorCalculationDelegateImpl2021 paired-role resolution."""
    abs_delta = -delta if (
        polarity == "darker"
        or (polarity == "relative_lighter" and is_dark)
        or (polarity == "relative_darker" and not is_dark)
    ) else delta

    def finish(tone_val: float, bg_t: float | None, req: float | None, is_bg: bool) -> float:
        if bg_t is not None and req is not None:
            if not (Contrast.ratio_of_tones(bg_t, tone_val) >= req):
                tone_val = foreground_tone(bg_t, req)
        if is_bg:
            tone_val = _clamp(65.0, 100.0, tone_val) if tone_val >= 57.0 else _clamp(0.0, 49.0, tone_val)
        return tone_val

    ref_b = finish(role_b_tone, bg_b, req_b, b_is_bg)
    if constraint == "exact":
        t_a = _clamp(0.0, 100.0, ref_b + abs_delta)
    elif constraint == "nearer":
        if abs_delta > 0:
            t_a = _clamp(0.0, 100.0, _clamp(ref_b, ref_b + abs_delta, role_a_tone))
        else:
            t_a = _clamp(0.0, 100.0, _clamp(ref_b + abs_delta, ref_b, role_a_tone))
    else:
        if abs_delta > 0:
            t_a = _clamp(ref_b + abs_delta, 100.0, role_a_tone)
        else:
            t_a = _clamp(0.0, ref_b + abs_delta, role_a_tone)
    t_a = finish(t_a, bg_a, req_a, a_is_bg)
    return t_a, ref_b


def _resolve_fg(bg_tone: float, initial_tone: float | None, desired_ratio: float, contrast_level: float, is_bg: bool = False) -> float:
    if initial_tone is None:
        ans = foreground_tone(bg_tone, desired_ratio)
    else:
        ans = initial_tone if (Contrast.ratio_of_tones(bg_tone, initial_tone) >= desired_ratio and contrast_level >= 0.0) else foreground_tone(bg_tone, desired_ratio)
    if is_bg:
        ans = _clamp(65.0, 100.0, ans) if ans >= 57.0 else _clamp(0.0, 49.0, ans)
    return ans


def _surface_chroma_mult(variant: str, nh: float, is_dark: bool, role: str) -> float:
    if role == "surface_dim" and not is_dark:
        if variant == "neutral":
            return 2.5
        if variant == "tonal-spot":
            return 1.7
        if variant == "expressive":
            return 2.7 if Hct.is_yellow(nh) else 1.75
        if variant == "vibrant":
            return 1.36
    elif role == "surface_bright" and is_dark:
        if variant == "neutral":
            return 2.5
        if variant == "tonal-spot":
            return 1.7
        if variant == "expressive":
            return 2.7 if Hct.is_yellow(nh) else 1.75
        if variant == "vibrant":
            return 1.36
    elif role == "surface_container_low":
        if variant == "neutral":
            return 1.3
        if variant == "tonal-spot":
            return 1.25
        if variant == "expressive":
            return 1.3 if Hct.is_yellow(nh) else 1.15
        if variant == "vibrant":
            return 1.08
    elif role == "surface_container":
        if variant == "neutral":
            return 1.6
        if variant == "tonal-spot":
            return 1.4
        if variant == "expressive":
            return 1.6 if Hct.is_yellow(nh) else 1.3
        if variant == "vibrant":
            return 1.15
    elif role == "surface_container_high":
        if variant == "neutral":
            return 1.9
        if variant == "tonal-spot":
            return 1.5
        if variant == "expressive":
            return 1.95 if Hct.is_yellow(nh) else 1.45
        if variant == "vibrant":
            return 1.22
    elif role in ("surface_container_highest", "on_surface", "on_surface_variant", "outline", "outline_variant"):
        if variant == "neutral":
            return 2.2
        if variant == "tonal-spot":
            return 1.7
        if variant == "expressive":
            if role in ("surface_container_highest",):
                return 2.3 if Hct.is_yellow(nh) else 1.6
            return (3.0 if is_dark else 2.3) if Hct.is_yellow(nh) else 1.6
        if variant == "vibrant" and role == "surface_container_highest":
            return 1.29
    return 1.0


def generate_scheme(
    seed_hex: str,
    variant: str = "expressive",
    is_dark: bool = False,
    contrast_level: float = 0.0,
    spec_version: str = "2025",
    min_pair_contrast: float | None = None,
) -> dict[str, str]:
    """Compute all 37 MD3E colour roles for a (seed, variant, is_dark, contrast_level)."""
    seed_hct = Hct.from_int(hex_to_argb(seed_hex))
    effective_spec = "2021" if variant in ("monochrome", "fidelity") else spec_version
    pals = build_palettes(seed_hct, variant, is_dark, effective_spec)
    p, s, t = pals["primary"], pals["secondary"], pals["tertiary"]
    n, nv, e = pals["neutral"], pals["neutral_variant"], pals["error"]
    nh = n.hue

    roles: dict[str, str] = {}
    role_tones: dict[str, float] = {}

    def put(name: str, pal: TonalPalette, tone_val: float, mult: float = 1.0) -> None:
        role_tones[name] = tone_val
        roles[name] = argb_to_hex(pal.tone(tone_val, mult))

    if effective_spec == "2025":
        is_yel_n = Hct.is_yellow(nh)
        # 1. Surface ladder (PHONE 2025 spec)
        s_t = 4.0 if is_dark else (99.0 if is_yel_n else (97.0 if variant == "vibrant" else 98.0))
        dim_t = 4.0 if is_dark else (90.0 if is_yel_n else (85.0 if variant == "vibrant" else 87.0))
        bri_t = 18.0 if is_dark else (99.0 if is_yel_n else (97.0 if variant == "vibrant" else 98.0))
        low_t = 6.0 if is_dark else (98.0 if is_yel_n else (95.0 if variant == "vibrant" else 96.0))
        con_t = 9.0 if is_dark else (96.0 if is_yel_n else (92.0 if variant == "vibrant" else 94.0))
        hi_t = 12.0 if is_dark else (94.0 if is_yel_n else (90.0 if variant == "vibrant" else 92.0))
        hst_t = 15.0 if is_dark else (92.0 if is_yel_n else (88.0 if variant == "vibrant" else 90.0))

        # Subtle surface step separation under medium/high contrast
        if contrast_level >= 0.5 and is_dark:
            hi_t = 17.0 if contrast_level < 1.0 else 22.0
            hst_t = 22.0 if contrast_level < 1.0 else 26.0
            bri_t = 22.0 if contrast_level < 1.0 else 28.0
        elif contrast_level >= 0.5 and not is_dark:
            hi_t = min(hi_t, 88.0 if contrast_level < 1.0 else 85.0)
            hst_t = min(hst_t, 84.0 if contrast_level < 1.0 else 80.0)
            dim_t = min(dim_t, 80.0 if contrast_level < 1.0 else 75.0)

        highest_t = bri_t if is_dark else dim_t

        put("surface", n, s_t)
        put("surface-dim", n, dim_t, _surface_chroma_mult(variant, nh, is_dark, "surface_dim"))
        put("surface-bright", n, bri_t, _surface_chroma_mult(variant, nh, is_dark, "surface_bright"))
        put("surface-container-lowest", n, 0.0 if is_dark else 100.0)
        put("surface-container-low", n, low_t, _surface_chroma_mult(variant, nh, is_dark, "surface_container_low"))
        put("surface-container", n, con_t, _surface_chroma_mult(variant, nh, is_dark, "surface_container"))
        put("surface-container-high", n, hi_t, _surface_chroma_mult(variant, nh, is_dark, "surface_container_high"))
        put("surface-container-highest", n, hst_t, _surface_chroma_mult(variant, nh, is_dark, "surface_container_highest"))
        put("surface-variant", n, hst_t, _surface_chroma_mult(variant, nh, is_dark, "surface_container_highest"))

        on_s_init = t_max_c(n, 0.0, 100.0, 1.1) if variant == "vibrant" else None
        on_s_req = _get_curve_2025(11.0 if is_dark else 9.0).get(contrast_level)
        on_s_t = _resolve_fg(highest_t, on_s_init, on_s_req, contrast_level)
        put("on-surface", n, on_s_t, _surface_chroma_mult(variant, nh, is_dark, "on_surface"))

        on_sv_req = _get_curve_2025(6.0 if is_dark else 4.5).get(contrast_level)
        on_sv_t = _resolve_fg(highest_t, None, on_sv_req, contrast_level)
        put("on-surface-variant", n, on_sv_t, _surface_chroma_mult(variant, nh, is_dark, "on_surface_variant"))

        out_req = _get_curve_2025(3.0).get(contrast_level)
        out_t = _resolve_fg(highest_t, None, out_req, contrast_level)
        put("outline", n, out_t, _surface_chroma_mult(variant, nh, is_dark, "outline"))

        ov_req = _get_curve_2025(1.5).get(contrast_level)
        ov_t = _resolve_fg(highest_t, None, ov_req, contrast_level)
        put("outline-variant", n, ov_t, _surface_chroma_mult(variant, nh, is_dark, "outline_variant"))

        inv_s_t = 98.0 if is_dark else 4.0
        put("inverse-surface", n, inv_s_t)
        put("inverse-on-surface", n, _resolve_fg(inv_s_t, None, _get_curve_2025(7.0).get(contrast_level), contrast_level))

        # 2. Primary, Secondary, Tertiary, Error (2025 PHONE spec)
        # Primary
        if variant == "neutral":
            p_raw = 80.0 if is_dark else 40.0
            pc_raw = 30.0 if is_dark else 90.0
        elif variant == "tonal-spot":
            p_raw = 80.0 if is_dark else t_max_c(p)
            pc_raw = t_min_c(p, 35.0, 93.0) if is_dark else t_max_c(p, 0.0, 90.0)
        elif variant == "expressive":
            p_raw = t_max_c(p, 0.0, 25.0 if Hct.is_yellow(p.hue) else (88.0 if Hct.is_cyan(p.hue) else 98.0))
            pc_raw = t_max_c(p, 30.0, 93.0) if is_dark else t_max_c(p, 78.0, 88.0 if Hct.is_cyan(p.hue) else 90.0)
        else:  # vibrant
            p_raw = t_max_c(p, 0.0, 88.0 if Hct.is_cyan(p.hue) else 98.0)
            pc_raw = t_min_c(p, 66.0, 93.0) if is_dark else t_max_c(p, 66.0, 88.0 if Hct.is_cyan(p.hue) else 93.0)

        p_req = _get_curve_2025(4.5).get(contrast_level)
        pc_req = _get_curve_2025(1.5).get(contrast_level) if contrast_level > 0.0 else None
        pc_t, p_t = _solve_2025_pair(pc_raw, p_raw, 5.0, "relative_lighter", "farther", is_dark, highest_t, pc_req, highest_t, p_req)
        put("primary", p, p_t)
        put("on-primary", p, _resolve_fg(p_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("primary-container", p, pc_t)
        put("on-primary-container", p, _resolve_fg(pc_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("inverse-primary", p, _resolve_fg(inv_s_t, t_max_c(p), _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("surface-tint", p, p_t)

        # Secondary
        if variant == "neutral":
            s_raw = t_min_c(s, 0.0, 98.0) if is_dark else t_max_c(s)
            sc_raw = 25.0 if is_dark else 90.0
        elif variant == "vibrant":
            s_raw = t_max_c(s, 0.0, 90.0 if is_dark else 98.0)
            sc_raw = t_min_c(s, 30.0, 40.0) if is_dark else t_max_c(s, 84.0, 90.0)
        elif variant == "expressive":
            s_raw = 80.0 if is_dark else t_max_c(s)
            sc_raw = 15.0 if is_dark else t_max_c(s, 90.0, 95.0)
        else:
            s_raw = 80.0 if is_dark else t_max_c(s)
            sc_raw = 25.0 if is_dark else 90.0
        sc_t, s_t = _solve_2025_pair(sc_raw, s_raw, 5.0, "relative_lighter", "farther", is_dark, highest_t, pc_req, highest_t, p_req)
        put("secondary", s, s_t)
        put("on-secondary", s, _resolve_fg(s_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("secondary-container", s, sc_t)
        put("on-secondary-container", s, _resolve_fg(sc_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))

        # Tertiary
        if variant in ("expressive", "vibrant"):
            t_raw = t_max_c(t, 0.0, 88.0 if Hct.is_cyan(t.hue) else (98.0 if is_dark else 100.0))
        else:
            t_raw = t_max_c(t, 0.0, 98.0) if is_dark else t_max_c(t)
        if variant == "neutral":
            tc_raw = t_max_c(t, 0.0, 93.0) if is_dark else t_max_c(t, 0.0, 96.0)
        elif variant == "tonal-spot":
            tc_raw = t_max_c(t, 0.0, 93.0 if is_dark else 100.0)
        elif variant == "expressive":
            tc_raw = t_max_c(t, 75.0, 88.0 if Hct.is_cyan(t.hue) else (93.0 if is_dark else 100.0))
        else:  # vibrant
            tc_raw = t_max_c(t, 0.0, 93.0) if is_dark else t_max_c(t, 72.0, 100.0)
        tc_t, t_t = _solve_2025_pair(tc_raw, t_raw, 5.0, "relative_lighter", "farther", is_dark, highest_t, pc_req, highest_t, p_req)
        put("tertiary", t, t_t)
        put("on-tertiary", t, _resolve_fg(t_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("tertiary-container", t, tc_t)
        put("on-tertiary-container", t, _resolve_fg(tc_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))

        # Error
        e_raw = t_min_c(e, 0.0, 98.0) if is_dark else t_max_c(e)
        ec_raw = t_min_c(e, 30.0, 93.0) if is_dark else t_max_c(e, 0.0, 90.0)
        ec_t, e_t = _solve_2025_pair(ec_raw, e_raw, 5.0, "relative_lighter", "farther", is_dark, highest_t, pc_req, highest_t, p_req)
        put("error", e, e_t)
        put("on-error", e, _resolve_fg(e_t, None, _get_curve_2025(6.0).get(contrast_level), contrast_level))
        put("error-container", e, ec_t)
        put("on-error-container", e, _resolve_fg(ec_t, None, _get_curve_2025(4.5).get(contrast_level), contrast_level))

        # Fixed roles (theme-invariant: computed in light theme, copied below for dark)
        if not is_dark:
            light_scheme = (
                generate_scheme(seed_hex, variant, False, 0.0, spec_version, min_pair_contrast=min_pair_contrast)
                if contrast_level != 0.0
                else None
            )
            for fam, pal in (("primary", p), ("secondary", s), ("tertiary", t)):
                if light_scheme is None:
                    fx_t = role_tones[f"{fam}-container"]
                else:
                    fx_t = lstar_from_argb(hex_to_argb(light_scheme[f"{fam}-fixed"]))
                if contrast_level > 0.0:
                    fx_t = _resolve_fg(highest_t, fx_t, _get_curve_2025(1.5).get(contrast_level), contrast_level, is_bg=True)
                fxd_t = _clamp(0.0, 100.0, fx_t - 5.0)
                put(f"{fam}-fixed", pal, fx_t)
                put(f"{fam}-fixed-dim", pal, fxd_t)
                put(f"on-{fam}-fixed", pal, _resolve_fg(fxd_t, None, _get_curve_2025(7.0).get(contrast_level), contrast_level))
                put(f"on-{fam}-fixed-variant", pal, _resolve_fg(fxd_t, None, _get_curve_2025(4.5).get(contrast_level), contrast_level))
    else:
        # 2021 Spec (used for monochrome/fidelity or explicit --spec 2021)
        is_mono = variant == "monochrome"
        is_fid = variant == "fidelity"
        s_t = 6.0 if is_dark else 98.0
        dim_t = 6.0 if is_dark else ContrastCurve(87.0, 87.0, 80.0, 75.0).get(contrast_level)
        bri_t = ContrastCurve(24.0, 24.0, 29.0, 34.0).get(contrast_level) if is_dark else 98.0
        low_t = ContrastCurve(10.0, 10.0, 11.0, 12.0).get(contrast_level) if is_dark else ContrastCurve(96.0, 96.0, 96.0, 95.0).get(contrast_level)
        con_t = ContrastCurve(12.0, 12.0, 16.0, 20.0).get(contrast_level) if is_dark else ContrastCurve(94.0, 94.0, 92.0, 90.0).get(contrast_level)
        hi_t = ContrastCurve(17.0, 17.0, 21.0, 25.0).get(contrast_level) if is_dark else ContrastCurve(92.0, 92.0, 88.0, 85.0).get(contrast_level)
        hst_t = ContrastCurve(22.0, 22.0, 26.0, 30.0).get(contrast_level) if is_dark else ContrastCurve(90.0, 90.0, 84.0, 80.0).get(contrast_level)
        highest_t = bri_t if is_dark else dim_t

        put("surface", n, s_t)
        put("surface-dim", n, dim_t)
        put("surface-bright", n, bri_t)
        put("surface-container-lowest", n, ContrastCurve(4.0, 4.0, 2.0, 0.0).get(contrast_level) if is_dark else 100.0)
        put("surface-container-low", n, low_t)
        put("surface-container", n, con_t)
        put("surface-container-high", n, hi_t)
        put("surface-container-highest", n, hst_t)
        put("surface-variant", nv, 30.0 if is_dark else 90.0)
        put("on-surface", n, _resolve_fg(highest_t, 90.0 if is_dark else 10.0, ContrastCurve(4.5, 7.0, 11.0, 21.0).get(contrast_level), contrast_level))
        put("on-surface-variant", nv, _resolve_fg(highest_t, 80.0 if is_dark else 30.0, ContrastCurve(3.0, 4.5, 7.0, 11.0).get(contrast_level), contrast_level))
        put("outline", nv, _resolve_fg(highest_t, 60.0 if is_dark else 50.0, ContrastCurve(1.5, 3.0, 4.5, 7.0).get(contrast_level), contrast_level))
        put("outline-variant", nv, _resolve_fg(highest_t, 30.0 if is_dark else 80.0, ContrastCurve(1.0, 1.0, 3.0, 4.5).get(contrast_level), contrast_level))
        inv_s_t = 90.0 if is_dark else 20.0
        put("inverse-surface", n, inv_s_t)
        put("inverse-on-surface", n, _resolve_fg(inv_s_t, 20.0 if is_dark else 95.0, ContrastCurve(4.5, 7.0, 11.0, 21.0).get(contrast_level), contrast_level))

        acc_req = ContrastCurve(3.0, 4.5, 7.0, 7.0).get(contrast_level)
        c_req = ContrastCurve(1.0, 1.0, 3.0, 4.5).get(contrast_level)
        on_req = ContrastCurve(4.5, 7.0, 11.0, 21.0).get(contrast_level)
        on_c_req = ContrastCurve(3.0, 4.5, 7.0, 11.0).get(contrast_level)

        def do_2021_family(fam: str, pal: TonalPalette, main_init: float, on_init: float, cont_init: float, on_cont_init: float) -> float:
            mt, ct = _resolve_paired_tones(main_init, cont_init, 10.0, "nearer", "nearer", is_dark, highest_t, acc_req, highest_t, c_req, True, True)
            put(fam, pal, mt)
            put(f"on-{fam}", pal, _resolve_fg(mt, on_init, on_req, contrast_level))
            put(f"{fam}-container", pal, ct)
            put(f"on-{fam}-container", pal, _resolve_fg(ct, on_cont_init, on_c_req, contrast_level))
            return mt

        p_init = (100.0 if is_dark else 0.0) if is_mono else (80.0 if is_dark else 40.0)
        on_p_init = (10.0 if is_dark else 90.0) if is_mono else (20.0 if is_dark else 100.0)
        pc_init = seed_hct.tone if is_fid else ((85.0 if is_dark else 25.0) if is_mono else (30.0 if is_dark else 90.0))
        on_pc_init = foreground_tone(pc_init, 4.5) if is_fid else ((0.0 if is_dark else 100.0) if is_mono else (90.0 if is_dark else 30.0))
        p_t = do_2021_family("primary", p, p_init, on_p_init, pc_init, on_pc_init)
        put("inverse-primary", p, _resolve_fg(inv_s_t, 40.0 if is_dark else 80.0, acc_req, contrast_level))
        put("surface-tint", p, p_t)

        sc_init_0 = (30.0 if is_dark else 85.0) if is_mono else (30.0 if is_dark else 90.0)
        sc_init = find_desired_chroma_by_tone(s.hue, s.chroma, sc_init_0, not is_dark) if is_fid else sc_init_0
        on_sc_init = (90.0 if is_dark else 10.0) if is_mono else (foreground_tone(sc_init, 4.5) if is_fid else (90.0 if is_dark else 30.0))
        do_2021_family("secondary", s, 80.0 if is_dark else 40.0, (10.0 if is_dark else 100.0) if is_mono else (20.0 if is_dark else 100.0), sc_init, on_sc_init)

        t_init = (90.0 if is_dark else 25.0) if is_mono else (80.0 if is_dark else 40.0)
        on_t_init = (10.0 if is_dark else 90.0) if is_mono else (20.0 if is_dark else 100.0)
        tc_init = (60.0 if is_dark else 49.0) if is_mono else (fix_if_disliked(t.get_hct(seed_hct.tone)).tone if is_fid else (30.0 if is_dark else 90.0))
        on_tc_init = (0.0 if is_dark else 100.0) if is_mono else (foreground_tone(tc_init, 4.5) if is_fid else (90.0 if is_dark else 30.0))
        do_2021_family("tertiary", t, t_init, on_t_init, tc_init, on_tc_init)

        do_2021_family("error", e, 80.0 if is_dark else 40.0, 20.0 if is_dark else 100.0, 30.0 if is_dark else 90.0, 90.0 if is_dark else 30.0)

        if not is_dark:
            for fam, pal, f_t, fd_t, on_f, on_fv in (
                ("primary", p, 40.0 if is_mono else 90.0, 30.0 if is_mono else 80.0, 100.0 if is_mono else 10.0, 90.0 if is_mono else 30.0),
                ("secondary", s, 80.0 if is_mono else 90.0, 70.0 if is_mono else 80.0, 10.0, 25.0 if is_mono else 30.0),
                ("tertiary", t, 40.0 if is_mono else 90.0, 30.0 if is_mono else 80.0, 100.0 if is_mono else 10.0, 90.0 if is_mono else 30.0),
            ):
                put(f"{fam}-fixed", pal, _resolve_fg(highest_t, f_t, c_req, contrast_level, is_bg=True))
                put(f"{fam}-fixed-dim", pal, _clamp(0.0, 100.0, role_tones[f"{fam}-fixed"] - 10.0))
                bottleneck_t = role_tones[f"{fam}-fixed"] if on_f >= 50.0 else role_tones[f"{fam}-fixed-dim"]
                put(f"on-{fam}-fixed", pal, _resolve_fg(bottleneck_t, on_f, on_req, contrast_level))
                put(f"on-{fam}-fixed-variant", pal, _resolve_fg(bottleneck_t, on_fv, on_c_req, contrast_level))

    roles["scrim"] = "#000000"
    roles["shadow"] = "#000000"

    # WCAG hard-floor guard: sRGB gamut quantization or low-contrast baseline pairs
    # must still meet exact WCAG thresholds for agents.
    floor = min_pair_contrast
    if floor is None:
        floor = 7.0 if contrast_level >= 1.0 else (6.0 if contrast_level >= 0.5 else 4.5)
    guard_pairs = [
        ("primary", "on-primary", p),
        ("primary-container", "on-primary-container", p),
        ("secondary", "on-secondary", s),
        ("secondary-container", "on-secondary-container", s),
        ("tertiary", "on-tertiary", t),
        ("tertiary-container", "on-tertiary-container", t),
        ("error", "on-error", e),
        ("error-container", "on-error-container", e),
        ("surface", "on-surface", n),
        ("surface-container-low", "on-surface", n),
        ("surface-container", "on-surface", n),
        ("surface-container-high", "on-surface-variant", n),
        ("inverse-surface", "inverse-on-surface", n),
    ]
    for bg_name, fg_name, fg_pal in guard_pairs:
        if srgb_contrast_ratio(roles[bg_name], roles[fg_name]) >= floor:
            continue
        # If even pure white/black cannot hit floor against bg_name, nudge container out of gray dead-zone
        w_max = srgb_contrast_ratio(roles[bg_name], "#FFFFFF")
        b_max = srgb_contrast_ratio(roles[bg_name], "#000000")
        if max(w_max, b_max) < floor:
            bg_t = lstar_from_argb(hex_to_argb(roles[bg_name]))
            if bg_t < 57.0:
                nudged_t = Contrast.darker_unsafe(100.0, floor + 0.6)
            else:
                nudged_t = Contrast.lighter_unsafe(0.0, floor + 0.6)
            roles[bg_name] = argb_to_hex(fg_pal.tone(nudged_t))
        bg_t = lstar_from_argb(hex_to_argb(roles[bg_name]))
        best_hex = roles[fg_name]
        best_ratio = srgb_contrast_ratio(roles[bg_name], best_hex)
        for delta_req in (floor + 0.5, floor + 1.5, 11.0, 21.0):
            cand_t = foreground_tone(bg_t, delta_req)
            cand_hex = argb_to_hex(fg_pal.tone(cand_t))
            cr = srgb_contrast_ratio(roles[bg_name], cand_hex)
            if cr > best_ratio:
                best_ratio = cr
                best_hex = cand_hex
            if cr >= floor:
                break
        if best_ratio < floor:
            w_cr = srgb_contrast_ratio(roles[bg_name], "#FFFFFF")
            b_cr = srgb_contrast_ratio(roles[bg_name], "#000000")
            best_hex = "#FFFFFF" if w_cr >= b_cr else "#000000"
        roles[fg_name] = best_hex

    if is_dark:
        light_fixed = generate_scheme(seed_hex, variant, False, contrast_level, spec_version, min_pair_contrast=min_pair_contrast)
        for fam in ("primary", "secondary", "tertiary"):
            for key in (f"{fam}-fixed", f"{fam}-fixed-dim", f"on-{fam}-fixed", f"on-{fam}-fixed-variant"):
                roles[key] = light_fixed[key]
    else:
        fx_step = 5.0 if effective_spec == "2025" else 10.0
        for fam, pal in (("primary", p), ("secondary", s), ("tertiary", t)):
            f_role = f"{fam}-fixed"
            fd_role = f"{fam}-fixed-dim"
            on_role = f"on-{fam}-fixed"
            onv_role = f"on-{fam}-fixed-variant"
            f_t = lstar_from_argb(hex_to_argb(roles[f_role]))
            fd_t = lstar_from_argb(hex_to_argb(roles[fd_role]))
            min_existing = min(
                srgb_contrast_ratio(roles[f_role], roles[on_role]),
                srgb_contrast_ratio(roles[fd_role], roles[on_role]),
                srgb_contrast_ratio(roles[f_role], roles[onv_role]),
                srgb_contrast_ratio(roles[fd_role], roles[onv_role]),
            )
            if min_existing >= floor:
                continue

            light_text = f_t < 57.0
            if light_text:
                cap_t = Contrast.darker_unsafe(100.0, floor + 0.6)
                if f_t > cap_t or max(srgb_contrast_ratio(roles[f_role], "#FFFFFF"), 0.0) < floor:
                    f_t = min(f_t, cap_t)
                    fd_t = _clamp(0.0, 100.0, min(fd_t, f_t - fx_step))
                    roles[f_role] = argb_to_hex(pal.tone(f_t))
                    roles[fd_role] = argb_to_hex(pal.tone(fd_t))
                bottleneck_t = f_t
            else:
                floor_t = Contrast.lighter_unsafe(0.0, floor + 0.6)
                if fd_t < floor_t or srgb_contrast_ratio(roles[fd_role], "#000000") < floor:
                    fd_t = max(fd_t, floor_t)
                    f_t = _clamp(0.0, 100.0, max(f_t, fd_t + fx_step))
                    roles[f_role] = argb_to_hex(pal.tone(f_t))
                    roles[fd_role] = argb_to_hex(pal.tone(fd_t))
                bottleneck_t = fd_t

            for fg_role in (on_role, onv_role):
                cur_cr = min(
                    srgb_contrast_ratio(roles[f_role], roles[fg_role]),
                    srgb_contrast_ratio(roles[fd_role], roles[fg_role]),
                )
                if cur_cr >= floor:
                    continue
                best_hex = roles[fg_role]
                best_min = cur_cr
                for delta_req in (floor + 0.5, floor + 1.5, 11.0, 21.0):
                    cand_t = foreground_tone(bottleneck_t, delta_req)
                    cand_hex = argb_to_hex(pal.tone(cand_t))
                    cr_both = min(
                        srgb_contrast_ratio(roles[f_role], cand_hex),
                        srgb_contrast_ratio(roles[fd_role], cand_hex),
                    )
                    if cr_both > best_min:
                        best_min = cr_both
                        best_hex = cand_hex
                    if cr_both >= floor:
                        break
                if best_min < floor:
                    w_cr = min(srgb_contrast_ratio(roles[f_role], "#FFFFFF"), srgb_contrast_ratio(roles[fd_role], "#FFFFFF"))
                    b_cr = min(srgb_contrast_ratio(roles[f_role], "#000000"), srgb_contrast_ratio(roles[fd_role], "#000000"))
                    best_hex = "#FFFFFF" if w_cr >= b_cr else "#000000"
                roles[fg_role] = best_hex

    return roles


# ---------------------------------------------------------------------------
# CSS Formatting Helpers
# ---------------------------------------------------------------------------

ROLE_ORDER = (
    "primary", "on-primary", "primary-container", "on-primary-container",
    "primary-fixed", "primary-fixed-dim", "on-primary-fixed", "on-primary-fixed-variant",
    "secondary", "on-secondary", "secondary-container", "on-secondary-container",
    "secondary-fixed", "secondary-fixed-dim", "on-secondary-fixed", "on-secondary-fixed-variant",
    "tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container",
    "tertiary-fixed", "tertiary-fixed-dim", "on-tertiary-fixed", "on-tertiary-fixed-variant",
    "error", "on-error", "error-container", "on-error-container",
    "surface", "on-surface", "surface-variant", "on-surface-variant",
    "surface-dim", "surface-bright",
    "surface-container-lowest", "surface-container-low",
    "surface-container", "surface-container-high", "surface-container-highest",
    "outline", "outline-variant",
    "inverse-surface", "inverse-on-surface", "inverse-primary",
    "scrim", "shadow", "surface-tint",
)


def _format_props(roles: dict[str, str], indent: str = "  ", diff_from: dict[str, str] | None = None) -> list[str]:
    lines: list[str] = []
    for k in ROLE_ORDER:
        val = roles[k]
        if diff_from is not None and diff_from.get(k) == val:
            continue
        lines.append(f"{indent}--md-sys-color-{k}: {val};")
    return lines


def _emit_selector_block(lines: list[str], selector: str, roles: dict[str, str], indent: str = "", diff_from: dict[str, str] | None = None) -> None:
    props = _format_props(roles, indent=indent + "  ", diff_from=diff_from)
    if not props:
        return
    lines.append(f"{indent}{selector} {{")
    lines.extend(props)
    lines.append(f"{indent}}}")


def render_variant_blocks(
    seed_hex: str,
    variant: str,
    spec_version: str = "2025",
    *,
    prefix_sel: str = "",
    include_default_no_attr: bool = False,
) -> list[str]:
    """Render light, system-dark, explicit-dark, medium, and high contrast blocks."""
    v_sel = f'{prefix_sel}[data-color-variant="{variant}"]'
    if include_default_no_attr:
        base_sels = f"{prefix_sel}:not([data-color-variant]), {v_sel}" if prefix_sel else f":root, {v_sel}"
    else:
        base_sels = v_sel

    light_std = generate_scheme(seed_hex, variant, False, 0.0, spec_version)
    dark_std = generate_scheme(seed_hex, variant, True, 0.0, spec_version)
    light_med = generate_scheme(seed_hex, variant, False, 0.5, spec_version)
    dark_med = generate_scheme(seed_hex, variant, True, 0.5, spec_version)
    light_hi = generate_scheme(seed_hex, variant, False, 1.0, spec_version)
    dark_hi = generate_scheme(seed_hex, variant, True, 1.0, spec_version)

    lines: list[str] = []
    lines.append(f"/* Variant: {variant} (seed {seed_hex.upper()}, spec {spec_version}) */")
    # Light Standard
    _emit_selector_block(lines, base_sels, light_std)

    # Dark Standard (system + explicit)
    lines.append("@media (prefers-color-scheme: dark) {")
    if include_default_no_attr and prefix_sel:
        sys_sels = f'{prefix_sel}:not([data-color-variant]):where(:not([data-theme="light"])), {v_sel}:where(:not([data-theme="light"]))'
    elif include_default_no_attr:
        sys_sels = f':root:where(:not([data-theme="light"])), {v_sel}:where(:not([data-theme="light"]))'
    else:
        sys_sels = f'{v_sel}:where(:not([data-theme="light"]))'
    _emit_selector_block(lines, sys_sels, dark_std, indent="  ")
    lines.append("}")

    exp_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-theme="dark"], {v_sel}[data-theme="dark"]'
        if (include_default_no_attr and prefix_sel)
        else (f'[data-theme="dark"], {v_sel}[data-theme="dark"]' if include_default_no_attr else f'{v_sel}[data-theme="dark"]')
    )
    _emit_selector_block(lines, exp_sels, dark_std)

    # Medium Contrast (explicit data-contrast="medium")
    med_l_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-contrast="medium"]:not([data-theme="dark"]), {v_sel}[data-contrast="medium"]:not([data-theme="dark"])'
        if include_default_no_attr
        else f'{v_sel}[data-contrast="medium"]:not([data-theme="dark"])'
    )
    _emit_selector_block(lines, med_l_sels, light_med, diff_from=light_std)

    lines.append("@media (prefers-color-scheme: dark) {")
    med_sys_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-contrast="medium"]:not([data-theme="light"]), {v_sel}[data-contrast="medium"]:not([data-theme="light"])'
        if include_default_no_attr
        else f'{v_sel}[data-contrast="medium"]:not([data-theme="light"])'
    )
    _emit_selector_block(lines, med_sys_sels, dark_med, indent="  ", diff_from=dark_std)
    lines.append("}")

    med_exp_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-theme="dark"][data-contrast="medium"], {v_sel}[data-theme="dark"][data-contrast="medium"]'
        if include_default_no_attr
        else f'{v_sel}[data-theme="dark"][data-contrast="medium"]'
    )
    _emit_selector_block(lines, med_exp_sels, dark_med, diff_from=dark_std)

    # High Contrast (explicit data-contrast="high" + @media (prefers-contrast: more))
    hi_l_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-contrast="high"]:not([data-theme="dark"]), {v_sel}[data-contrast="high"]:not([data-theme="dark"])'
        if include_default_no_attr
        else f'{v_sel}[data-contrast="high"]:not([data-theme="dark"])'
    )
    _emit_selector_block(lines, hi_l_sels, light_hi, diff_from=light_std)

    lines.append("@media (prefers-color-scheme: dark) {")
    hi_sys_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-contrast="high"]:not([data-theme="light"]), {v_sel}[data-contrast="high"]:not([data-theme="light"])'
        if include_default_no_attr
        else f'{v_sel}[data-contrast="high"]:not([data-theme="light"])'
    )
    _emit_selector_block(lines, hi_sys_sels, dark_hi, indent="  ", diff_from=dark_std)
    lines.append("}")

    hi_exp_sels = (
        f'{prefix_sel}:not([data-color-variant])[data-theme="dark"][data-contrast="high"], {v_sel}[data-theme="dark"][data-contrast="high"]'
        if include_default_no_attr
        else f'{v_sel}[data-theme="dark"][data-contrast="high"]'
    )
    _emit_selector_block(lines, hi_exp_sels, dark_hi, diff_from=dark_std)

    # OS prefers-contrast: more (honour explicit [data-contrast="medium"] if set)
    lines.append("@media (prefers-contrast: more) {")
    os_hi_l = (
        f'{prefix_sel}:not([data-color-variant]):where(:not([data-theme="dark"]):not([data-contrast="medium"])), {v_sel}:where(:not([data-theme="dark"]):not([data-contrast="medium"]))'
        if include_default_no_attr
        else f'{v_sel}:where(:not([data-theme="dark"]):not([data-contrast="medium"]))'
    )
    _emit_selector_block(lines, os_hi_l, light_hi, indent="  ", diff_from=light_std)
    lines.append("  @media (prefers-color-scheme: dark) {")
    os_hi_sd = (
        f'{prefix_sel}:not([data-color-variant]):where(:not([data-theme="light"]):not([data-contrast="medium"])), {v_sel}:where(:not([data-theme="light"]):not([data-contrast="medium"]))'
        if include_default_no_attr
        else f'{v_sel}:where(:not([data-theme="light"]):not([data-contrast="medium"]))'
    )
    _emit_selector_block(lines, os_hi_sd, dark_hi, indent="    ", diff_from=dark_std)
    lines.append("  }")
    os_hi_ed = (
        f'{prefix_sel}:not([data-color-variant])[data-theme="dark"]:where(:not([data-contrast="medium"])), {v_sel}[data-theme="dark"]:where(:not([data-contrast="medium"]))'
        if include_default_no_attr
        else f'{v_sel}[data-theme="dark"]:where(:not([data-contrast="medium"]))'
    )
    _emit_selector_block(lines, os_hi_ed, dark_hi, indent="  ", diff_from=dark_std)
    lines.append("}")
    lines.append("")
    return lines


def render_standalone_css(
    seed_hex: str,
    variant: str = "expressive",
    spec_version: str = "2025",
    *,
    image_source: str | None = None,
    candidates: list[dict[str, object]] | None = None,
) -> str:
    """Render a standalone brand stylesheet overriding :root / dark / contrast tokens."""
    light_std = generate_scheme(seed_hex, variant, False, 0.0, spec_version)
    dark_std = generate_scheme(seed_hex, variant, True, 0.0, spec_version)
    light_med = generate_scheme(seed_hex, variant, False, 0.5, spec_version)
    dark_med = generate_scheme(seed_hex, variant, True, 0.5, spec_version)
    light_hi = generate_scheme(seed_hex, variant, False, 1.0, spec_version)
    dark_hi = generate_scheme(seed_hex, variant, True, 1.0, spec_version)

    lines = [
        "/* ============================================================================",
        f" * Custom MD3E Colour Scheme — Seed {seed_hex.upper()} | Variant {variant} | Spec {spec_version}",
    ]
    if image_source:
        cand_str = ", ".join(str(c["hex"]) for c in (candidates or []))
        lines.append(f" * Extracted from image: {image_source}" + (f" (candidates: {cand_str})" if cand_str else ""))
    lines.extend([
        " * Generated by: python scripts/color_to_css.py",
        " * Import AFTER md3e-tokens.css so all system roles reflect your brand seed.",
        " * ========================================================================== */",
        "",
    ])
    _emit_selector_block(lines, ":root", light_std)
    lines.append("")
    lines.append("@media (prefers-color-scheme: dark) {")
    _emit_selector_block(lines, ':root:where(:not([data-theme="light"]))', dark_std, indent="  ")
    lines.append("}")
    lines.append("")
    _emit_selector_block(lines, '[data-theme="dark"]', dark_std)
    lines.append("")
    _emit_selector_block(lines, '[data-contrast="medium"]:not([data-theme="dark"])', light_med, diff_from=light_std)
    lines.append("@media (prefers-color-scheme: dark) {")
    _emit_selector_block(lines, '[data-contrast="medium"]:not([data-theme="light"])', dark_med, indent="  ", diff_from=dark_std)
    lines.append("}")
    _emit_selector_block(lines, '[data-theme="dark"][data-contrast="medium"]', dark_med, diff_from=dark_std)
    lines.append("")
    _emit_selector_block(lines, '[data-contrast="high"]:not([data-theme="dark"])', light_hi, diff_from=light_std)
    lines.append("@media (prefers-color-scheme: dark) {")
    _emit_selector_block(lines, '[data-contrast="high"]:not([data-theme="light"])', dark_hi, indent="  ", diff_from=dark_std)
    lines.append("}")
    _emit_selector_block(lines, '[data-theme="dark"][data-contrast="high"]', dark_hi, diff_from=dark_std)
    lines.append("@media (prefers-contrast: more) {")
    _emit_selector_block(lines, ':is(:root, [data-theme="light"]):where(:not([data-theme="dark"]):not([data-contrast="medium"]))', light_hi, indent="  ", diff_from=light_std)
    lines.append("  @media (prefers-color-scheme: dark) {")
    _emit_selector_block(lines, ':root:where(:not([data-theme="light"]):not([data-contrast="medium"]))', dark_hi, indent="    ", diff_from=dark_std)
    lines.append("  }")
    _emit_selector_block(lines, '[data-theme="dark"]:where(:not([data-contrast="medium"]))', dark_hi, indent="  ", diff_from=dark_std)
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def render_base_variants_css(spec_version: str = "2025") -> str:
    """Render SPEC_2025 variant overrides for baseline purple (#6750A4)."""
    lines: list[str] = []
    for variant in UI_VARIANTS:
        lines.extend(
            render_variant_blocks(
                PRESET_SEEDS["purple"],
                variant,
                spec_version=spec_version,
                prefix_sel="",
                include_default_no_attr=False,
            )
        )
    return "\n".join(lines).rstrip()


def sync_base_variants_in_tokens(tokens_path: pathlib.Path, spec_version: str = "2025") -> None:
    """Update the generated baseline variants section inside md3e-tokens.css."""
    start_marker = "/* === BEGIN GENERATED BASELINE VARIANTS === */"
    end_marker = "/* === END GENERATED BASELINE VARIANTS === */"
    content = tokens_path.read_text(encoding="utf-8")
    if start_marker not in content or end_marker not in content:
        raise ValueError(f"Markers not found in {tokens_path}")
    prefix, rest = content.split(start_marker, 1)
    _, suffix = rest.split(end_marker, 1)
    generated = render_base_variants_css(spec_version=spec_version)
    new_content = f"{prefix}{start_marker}\n{generated}\n{end_marker}{suffix}"
    tokens_path.write_text(new_content, encoding="utf-8")


def render_presets_css(spec_version: str = "2025") -> str:
    """Render assets/tokens/md3e-palettes.css covering multi-seed x multi-variant presets."""
    lines = [
        "/* ============================================================================",
        " * md3e-palettes.css — Multi-Seed & Multi-Variant MD3E Colour Schemes",
        " *",
        " * GENERATED FILE — do not edit by hand.",
        " * Regenerate with:  python scripts/color_to_css.py --emit-presets \\",
        " *                       assets/tokens/md3e-palettes.css",
        " *",
        " * Usage: set `data-seed` + `data-color-variant` + optional `data-theme` /",
        " * `data-contrast` (`medium` | `high`) on <html>:",
        ' *   <html data-seed="ocean" data-color-variant="expressive">',
        " * ========================================================================== */",
        "",
    ]
    for seed_name, seed_hex in PRESET_SEEDS.items():
        if seed_name == "purple":
            # Purple presets live in md3e-tokens.css; support explicit [data-seed="purple"]
            # when switching dynamically only if needed, though [data-seed="purple"] falls
            # cleanly back to md3e-tokens.css. Emit non-purple seeds here to keep CSS lean.
            continue
        lines.append(f"/* ==================== SEED: {seed_name.upper()} ({seed_hex}) ==================== */")
        for idx, variant in enumerate(UI_VARIANTS):
            lines.extend(
                render_variant_blocks(
                    seed_hex,
                    variant,
                    spec_version=spec_version,
                    prefix_sel=f'[data-seed="{seed_name}"]',
                    include_default_no_attr=(idx == 0),
                )
            )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Material 3 Expressive dynamic colour CSS from any seed hex."
    )
    parser.add_argument("--seed", default="#6750A4", help="Seed colour in #RRGGBB hex (default: #6750A4)")
    parser.add_argument("--image", metavar="PATH", help="Extract Material seed colour from an image file (QuantizerCelebi + Score)")
    parser.add_argument("--variant", choices=VARIANTS, default="expressive", help="DynamicScheme variant")
    parser.add_argument("--spec", choices=("2025", "2021"), default="2025", help="MCU colour spec version")
    parser.add_argument("--json", action="store_true", help="Emit JSON for light/dark × standard/medium/high")
    parser.add_argument("--emit-css", metavar="PATH", help="Write standalone brand token CSS to PATH")
    parser.add_argument("--emit-presets", metavar="PATH", help="Write multi-seed presets CSS to PATH")
    parser.add_argument("--sync-base-variants", metavar="PATH", help="Update baseline variant blocks inside md3e-tokens.css")
    args = parser.parse_args(argv)

    if args.sync_base_variants:
        tok_path = pathlib.Path(args.sync_base_variants)
        sync_base_variants_in_tokens(tok_path, spec_version=args.spec)
        print(f"synced baseline variants in {tok_path}")
        return 0

    if args.emit_presets:
        out_path = pathlib.Path(args.emit_presets)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_presets_css(spec_version=args.spec), encoding="utf-8")
        print(f"wrote {out_path}")
        return 0

    seed_hex = args.seed
    extracted_candidates: list[dict[str, object]] | None = None
    image_source: str | None = None
    if args.image:
        img_path = pathlib.Path(args.image)
        extracted_candidates = extract_seeds_from_image_file(img_path)
        seed_hex = str(extracted_candidates[0]["hex"])
        image_source = img_path.name

    if args.json:
        payload: dict[str, object] = {
            "seed": seed_hex.upper(),
            "variant": args.variant,
            "spec": args.spec,
            "schemes": {
                "light": {
                    "standard": generate_scheme(seed_hex, args.variant, False, 0.0, args.spec),
                    "medium": generate_scheme(seed_hex, args.variant, False, 0.5, args.spec),
                    "high": generate_scheme(seed_hex, args.variant, False, 1.0, args.spec),
                },
                "dark": {
                    "standard": generate_scheme(seed_hex, args.variant, True, 0.0, args.spec),
                    "medium": generate_scheme(seed_hex, args.variant, True, 0.5, args.spec),
                    "high": generate_scheme(seed_hex, args.variant, True, 1.0, args.spec),
                },
            },
        }
        if extracted_candidates is not None:
            payload["extracted_candidates"] = extracted_candidates
        print(json.dumps(payload, indent=2))
        return 0

    css = render_standalone_css(
        seed_hex,
        args.variant,
        args.spec,
        image_source=image_source,
        candidates=extracted_candidates,
    )
    if args.emit_css:
        out_path = pathlib.Path(args.emit_css)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(css, encoding="utf-8")
        print(f"wrote {out_path}")
        return 0

    print(css)
    return 0


if __name__ == "__main__":
    sys.exit(main())
