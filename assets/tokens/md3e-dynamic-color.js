/**
 * md3e-dynamic-color.js — Zero-dependency Browser & SSR Material Color Utilities (MCU)
 *
 * Implements:
 * - Official MCU image colour extraction: QuantizerWu + QuantizerWsmeans
 *   (QuantizerCelebi) + Score (proportion & chroma suitability ranking)
 * - Full CAM16 / HCT solver and DynamicScheme (SPEC_2025 & SPEC_2021)
 * - Pure-CSS dynamic theme injector (`applyDynamicSeed`) & standalone CSS exporter
 *
 * Parity note: shares exact numeric math, SPEC_2025 contrast curves, Fixed-role
 * light/dark invariance, WCAG hard-floor guards, and deterministic LCG seeding
 * with `scripts/color_to_css.py`.
 */

export const VARIANTS = Object.freeze([
  'tonal-spot',
  'expressive',
  'vibrant',
  'neutral',
  'monochrome',
  'fidelity',
]);

export const UI_VARIANTS = Object.freeze([
  'tonal-spot',
  'expressive',
  'vibrant',
  'neutral',
  'monochrome',
]);

export const ROLE_ORDER = Object.freeze([
  'primary', 'on-primary', 'primary-container', 'on-primary-container',
  'primary-fixed', 'primary-fixed-dim', 'on-primary-fixed', 'on-primary-fixed-variant',
  'secondary', 'on-secondary', 'secondary-container', 'on-secondary-container',
  'secondary-fixed', 'secondary-fixed-dim', 'on-secondary-fixed', 'on-secondary-fixed-variant',
  'tertiary', 'on-tertiary', 'tertiary-container', 'on-tertiary-container',
  'tertiary-fixed', 'tertiary-fixed-dim', 'on-tertiary-fixed', 'on-tertiary-fixed-variant',
  'error', 'on-error', 'error-container', 'on-error-container',
  'surface', 'on-surface', 'surface-variant', 'on-surface-variant',
  'surface-dim', 'surface-bright',
  'surface-container-lowest', 'surface-container-low',
  'surface-container', 'surface-container-high', 'surface-container-highest',
  'outline', 'outline-variant',
  'inverse-surface', 'inverse-on-surface', 'inverse-primary',
  'scrim', 'shadow', 'surface-tint',
]);

const WHITE_POINT_D65 = [95.047, 100.0, 108.883];

const SRGB_TO_XYZ = [
  [0.41233895, 0.35762064, 0.18051042],
  [0.2126, 0.7152, 0.0722],
  [0.01932141, 0.11916382, 0.95034478],
];

const XYZ_TO_SRGB = [
  [3.2413774792388685, -1.5376652402851851, -0.49885366846268053],
  [-0.9691452513005321, 1.8758853451067872, 0.04156585616912061],
  [0.05562093689691305, -0.20395524564742123, 1.0571799111220335],
];

const SCALED_DISCOUNT_FROM_LINRGB = [
  [0.001200833568784504, 0.002389694492170889, 0.0002795742885861124],
  [0.0005891086651375999, 0.0029785502573438758, 0.0003270666104008398],
  [0.00010146692491640572, 0.0005364214359186694, 0.0032979401770712076],
];

const LINRGB_FROM_SCALED_DISCOUNT = [
  [1373.2198709594231, -1100.4251190754821, -7.278681089101213],
  [-271.815969077903, 559.6580465940733, -32.46047482791194],
  [1.9622899599665666, -57.173814538844006, 308.7233197812385],
];

const Y_FROM_LINRGB = [0.2126, 0.7152, 0.0722];

const CRITICAL_PLANES = [
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
];

function pyRound(x) {
  const sign = x < 0 ? -1 : 1;
  const ax = Math.abs(x);
  const n = Math.floor(ax);
  const frac = ax - n;
  let r;
  if (frac > 0.5) r = n + 1;
  else if (frac < 0.5) r = n;
  else r = (n % 2 === 0) ? n : n + 1;
  return sign * r;
}

function clamp(lo, hi, x) {
  return x < lo ? lo : (x > hi ? hi : x);
}

function clampInt(lo, hi, x) {
  return x < lo ? lo : (x > hi ? hi : x);
}

function signum(x) {
  return x > 0 ? 1.0 : (x < 0 ? -1.0 : 0.0);
}

function lerp(start, stop, amount) {
  return (1.0 - amount) * start + amount * stop;
}

function sanitizeDegrees(deg) {
  const r = deg % 360.0;
  return r < 0.0 ? r + 360.0 : r;
}

function sanitizeRadians(rad) {
  const twoPi = 2.0 * Math.PI;
  return ((rad % twoPi) + twoPi) % twoPi;
}

function matmul(vec, mat) {
  return [
    vec[0] * mat[0][0] + vec[1] * mat[0][1] + vec[2] * mat[0][2],
    vec[0] * mat[1][0] + vec[1] * mat[1][1] + vec[2] * mat[1][2],
    vec[0] * mat[2][0] + vec[1] * mat[2][1] + vec[2] * mat[2][2],
  ];
}

function linearized(rgbComponent) {
  const normalized = rgbComponent / 255.0;
  if (normalized <= 0.040449936) {
    return (normalized / 12.92) * 100.0;
  }
  return (((normalized + 0.055) / 1.055) ** 2.4) * 100.0;
}

function delinearized(rgbComponent) {
  const normalized = rgbComponent / 100.0;
  const out = normalized <= 0.0031308
    ? normalized * 12.92
    : 1.055 * (normalized ** (1.0 / 2.4)) - 0.055;
  return clampInt(0, 255, pyRound(out * 255.0));
}

function trueDelinearized(rgbComponent) {
  const normalized = rgbComponent / 100.0;
  const out = normalized <= 0.0031308
    ? normalized * 12.92
    : 1.055 * (normalized ** (1.0 / 2.4)) - 0.055;
  return out * 255.0;
}

export function argbFromRgb(r, g, b) {
  return ((0xFF << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)) >>> 0;
}

function argbFromLinrgb(linrgb) {
  return argbFromRgb(
    delinearized(linrgb[0]),
    delinearized(linrgb[1]),
    delinearized(linrgb[2]),
  );
}

export function hexToArgb(hexColor) {
  let cleaned = String(hexColor || '').trim().replace(/^#/, '');
  if (cleaned.length === 3) {
    cleaned = cleaned.split('').map((c) => c + c).join('');
  }
  if (!/^[0-9a-fA-F]{6}$/.test(cleaned)) {
    throw new Error(`Expected 6-digit hex colour, got ${JSON.stringify(hexColor)}`);
  }
  return ((0xFF << 24) | parseInt(cleaned, 16)) >>> 0;
}

export function argbToHex(argb) {
  return '#' + (argb & 0xFFFFFF).toString(16).padStart(6, '0').toUpperCase();
}

export function normalizeHex(hexColor) {
  return argbToHex(hexToArgb(hexColor));
}

function labF(t) {
  const e = 216.0 / 24389.0;
  const kappa = 24389.0 / 27.0;
  return t > e ? Math.sign(t) * (Math.abs(t) ** (1.0 / 3.0)) : (kappa * t + 16.0) / 116.0;
}

function labInvf(ft) {
  const e = 216.0 / 24389.0;
  const kappa = 24389.0 / 27.0;
  const ft3 = ft * ft * ft;
  return ft3 > e ? ft3 : (116.0 * ft - 16.0) / kappa;
}

function yFromLstar(lstar) {
  return 100.0 * labInvf((lstar + 16.0) / 116.0);
}

function lstarFromY(y) {
  return 116.0 * labF(y / 100.0) - 16.0;
}

export function lstarFromArgb(argb) {
  const r = linearized((argb >>> 16) & 0xFF);
  const g = linearized((argb >>> 8) & 0xFF);
  const b = linearized(argb & 0xFF);
  const y = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return 116.0 * labF(y / 100.0) - 16.0;
}

function argbFromLstar(lstar) {
  const y = yFromLstar(lstar);
  const c = delinearized(y);
  return argbFromRgb(c, c, c);
}

export function labFromArgb(argb) {
  const r = linearized((argb >>> 16) & 0xFF);
  const g = linearized((argb >>> 8) & 0xFF);
  const b = linearized(argb & 0xFF);
  const [x, y, z] = matmul([r, g, b], SRGB_TO_XYZ);
  const fx = labF(x / WHITE_POINT_D65[0]);
  const fy = labF(y / WHITE_POINT_D65[1]);
  const fz = labF(z / WHITE_POINT_D65[2]);
  return [116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz)];
}

export function argbFromLab(lVal, aVal, bVal) {
  const fy = (lVal + 16.0) / 116.0;
  const fx = aVal / 500.0 + fy;
  const fz = fy - bVal / 200.0;
  const x = labInvf(fx) * WHITE_POINT_D65[0];
  const y = labInvf(fy) * WHITE_POINT_D65[1];
  const z = labInvf(fz) * WHITE_POINT_D65[2];
  return argbFromLinrgb(matmul([x, y, z], XYZ_TO_SRGB));
}

export function srgbContrastRatio(hexA, hexB) {
  function lum(h) {
    const argb = hexToArgb(h);
    const r = linearized((argb >>> 16) & 0xFF) / 100.0;
    const g = linearized((argb >>> 8) & 0xFF) / 100.0;
    const b = linearized(argb & 0xFF) / 100.0;
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  const la = lum(hexA);
  const lb = lum(hexB);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

// ---------------------------------------------------------------------------
// MCU Image Quantization (QuantizerWu + QuantizerWsmeans + QuantizerCelebi)
// & Suitability Scoring (Score)
// ---------------------------------------------------------------------------

const WU_INDEX_BITS = 5;
const WU_SIDE_LENGTH = 33;
const WU_TOTAL_SIZE = 35937;
const WSMEANS_MAX_ITERATIONS = 10;
const WSMEANS_MIN_MOVEMENT_DISTANCE = 3.0;

class DeterministicRandom {
  constructor(seed = 0x42688) {
    this.state = seed >>> 0;
  }

  nextFloat() {
    this.state = (Math.imul(this.state, 1664525) + 1013904223) >>> 0;
    return this.state / 4294967296.0;
  }
}

function wuIndex(r, g, b) {
  return (r << (WU_INDEX_BITS * 2)) + (r << (WU_INDEX_BITS + 1)) + r + (g << WU_INDEX_BITS) + g + b;
}

class QuantizerWu {
  _volume(cube, m) {
    return (
      m[wuIndex(cube.r1, cube.g1, cube.b1)]
      - m[wuIndex(cube.r1, cube.g1, cube.b0)]
      - m[wuIndex(cube.r1, cube.g0, cube.b1)]
      + m[wuIndex(cube.r1, cube.g0, cube.b0)]
      - m[wuIndex(cube.r0, cube.g1, cube.b1)]
      + m[wuIndex(cube.r0, cube.g1, cube.b0)]
      + m[wuIndex(cube.r0, cube.g0, cube.b1)]
      - m[wuIndex(cube.r0, cube.g0, cube.b0)]
    );
  }

  _bottom(cube, direction, m) {
    if (direction === 0) {
      return -m[wuIndex(cube.r0, cube.g1, cube.b1)] + m[wuIndex(cube.r0, cube.g1, cube.b0)] + m[wuIndex(cube.r0, cube.g0, cube.b1)] - m[wuIndex(cube.r0, cube.g0, cube.b0)];
    }
    if (direction === 1) {
      return -m[wuIndex(cube.r1, cube.g0, cube.b1)] + m[wuIndex(cube.r1, cube.g0, cube.b0)] + m[wuIndex(cube.r0, cube.g0, cube.b1)] - m[wuIndex(cube.r0, cube.g0, cube.b0)];
    }
    return -m[wuIndex(cube.r1, cube.g1, cube.b0)] + m[wuIndex(cube.r1, cube.g0, cube.b0)] + m[wuIndex(cube.r0, cube.g1, cube.b0)] - m[wuIndex(cube.r0, cube.g0, cube.b0)];
  }

  _top(cube, direction, pos, m) {
    if (direction === 0) {
      return m[wuIndex(pos, cube.g1, cube.b1)] - m[wuIndex(pos, cube.g1, cube.b0)] - m[wuIndex(pos, cube.g0, cube.b1)] + m[wuIndex(pos, cube.g0, cube.b0)];
    }
    if (direction === 1) {
      return m[wuIndex(cube.r1, pos, cube.b1)] - m[wuIndex(cube.r1, pos, cube.b0)] - m[wuIndex(cube.r0, pos, cube.b1)] + m[wuIndex(cube.r0, pos, cube.b0)];
    }
    return m[wuIndex(cube.r1, cube.g1, pos)] - m[wuIndex(cube.r1, cube.g0, pos)] - m[wuIndex(cube.r0, cube.g1, pos)] + m[wuIndex(cube.r0, cube.g0, pos)];
  }

  _variance(cube) {
    const dr = this._volume(cube, this.momentsR);
    const dg = this._volume(cube, this.momentsG);
    const db = this._volume(cube, this.momentsB);
    const xx = (
      this.moments[wuIndex(cube.r1, cube.g1, cube.b1)]
      - this.moments[wuIndex(cube.r1, cube.g1, cube.b0)]
      - this.moments[wuIndex(cube.r1, cube.g0, cube.b1)]
      + this.moments[wuIndex(cube.r1, cube.g0, cube.b0)]
      - this.moments[wuIndex(cube.r0, cube.g1, cube.b1)]
      + this.moments[wuIndex(cube.r0, cube.g1, cube.b0)]
      + this.moments[wuIndex(cube.r0, cube.g0, cube.b1)]
      - this.moments[wuIndex(cube.r0, cube.g0, cube.b0)]
    );
    const hyp = dr * dr + dg * dg + db * db;
    const vol = this._volume(cube, this.weights);
    return xx - hyp / vol;
  }

  _maximize(cube, direction, first, last, wholeR, wholeG, wholeB, wholeW) {
    const botR = this._bottom(cube, direction, this.momentsR);
    const botG = this._bottom(cube, direction, this.momentsG);
    const botB = this._bottom(cube, direction, this.momentsB);
    const botW = this._bottom(cube, direction, this.weights);
    let maxVal = 0.0;
    let cutLoc = -1;
    for (let i = first; i < last; i++) {
      const halfR = botR + this._top(cube, direction, i, this.momentsR);
      const halfG = botG + this._top(cube, direction, i, this.momentsG);
      const halfB = botB + this._top(cube, direction, i, this.momentsB);
      const halfW = botW + this._top(cube, direction, i, this.weights);
      if (halfW === 0) continue;
      let temp = (halfR * halfR + halfG * halfG + halfB * halfB) / halfW;
      const remR = wholeR - halfR;
      const remG = wholeG - halfG;
      const remB = wholeB - halfB;
      const remW = wholeW - halfW;
      if (remW === 0) continue;
      temp += (remR * remR + remG * remG + remB * remB) / remW;
      if (temp > maxVal) {
        maxVal = temp;
        cutLoc = i;
      }
    }
    return [cutLoc, maxVal];
  }

  _cut(one, two) {
    const wholeR = this._volume(one, this.momentsR);
    const wholeG = this._volume(one, this.momentsG);
    const wholeB = this._volume(one, this.momentsB);
    const wholeW = this._volume(one, this.weights);
    const [cutR, maxR] = this._maximize(one, 0, one.r0 + 1, one.r1, wholeR, wholeG, wholeB, wholeW);
    const [cutG, maxG] = this._maximize(one, 1, one.g0 + 1, one.g1, wholeR, wholeG, wholeB, wholeW);
    const [cutB, maxB] = this._maximize(one, 2, one.b0 + 1, one.b1, wholeR, wholeG, wholeB, wholeW);

    two.r1 = one.r1;
    two.g1 = one.g1;
    two.b1 = one.b1;
    if (maxR >= maxG && maxR >= maxB) {
      if (cutR < 0) return false;
      one.r1 = cutR;
      two.r0 = cutR;
      two.g0 = one.g0;
      two.b0 = one.b0;
    } else if (maxG >= maxR && maxG >= maxB) {
      one.g1 = cutG;
      two.r0 = one.r0;
      two.g0 = cutG;
      two.b0 = one.b0;
    } else {
      one.b1 = cutB;
      two.r0 = one.r0;
      two.g0 = one.g0;
      two.b0 = cutB;
    }
    one.vol = (one.r1 - one.r0) * (one.g1 - one.g0) * (one.b1 - one.b0);
    two.vol = (two.r1 - two.r0) * (two.g1 - two.g0) * (two.b1 - two.b0);
    return true;
  }

  quantize(pixels, maxColors = 128) {
    if (!pixels || pixels.length === 0) return [];
    this.weights = new Array(WU_TOTAL_SIZE).fill(0);
    this.momentsR = new Array(WU_TOTAL_SIZE).fill(0);
    this.momentsG = new Array(WU_TOTAL_SIZE).fill(0);
    this.momentsB = new Array(WU_TOTAL_SIZE).fill(0);
    this.moments = new Array(WU_TOTAL_SIZE).fill(0);

    const counts = new Map();
    for (let i = 0; i < pixels.length; i++) {
      const px = pixels[i] >>> 0;
      counts.set(px, (counts.get(px) ?? 0) + 1);
    }

    const bitsRemove = 8 - WU_INDEX_BITS;
    for (const [px, cnt] of counts.entries()) {
      const red = (px >>> 16) & 0xFF;
      const green = (px >>> 8) & 0xFF;
      const blue = px & 0xFF;
      const index = wuIndex((red >> bitsRemove) + 1, (green >> bitsRemove) + 1, (blue >> bitsRemove) + 1);
      this.weights[index] += cnt;
      this.momentsR[index] += cnt * red;
      this.momentsG[index] += cnt * green;
      this.momentsB[index] += cnt * blue;
      this.moments[index] += cnt * (red * red + green * green + blue * blue);
    }

    for (let r = 1; r < WU_SIDE_LENGTH; r++) {
      const area = new Array(WU_SIDE_LENGTH).fill(0);
      const areaR = new Array(WU_SIDE_LENGTH).fill(0);
      const areaG = new Array(WU_SIDE_LENGTH).fill(0);
      const areaB = new Array(WU_SIDE_LENGTH).fill(0);
      const area2 = new Array(WU_SIDE_LENGTH).fill(0);
      for (let g = 1; g < WU_SIDE_LENGTH; g++) {
        let line = 0;
        let lineR = 0;
        let lineG = 0;
        let lineB = 0;
        let line2 = 0;
        for (let b = 1; b < WU_SIDE_LENGTH; b++) {
          const index = wuIndex(r, g, b);
          line += this.weights[index];
          lineR += this.momentsR[index];
          lineG += this.momentsG[index];
          lineB += this.momentsB[index];
          line2 += this.moments[index];
          area[b] += line;
          areaR[b] += lineR;
          areaG[b] += lineG;
          areaB[b] += lineB;
          area2[b] += line2;
          const prevIdx = wuIndex(r - 1, g, b);
          this.weights[index] = this.weights[prevIdx] + area[b];
          this.momentsR[index] = this.momentsR[prevIdx] + areaR[b];
          this.momentsG[index] = this.momentsG[prevIdx] + areaG[b];
          this.momentsB[index] = this.momentsB[prevIdx] + areaB[b];
          this.moments[index] = this.moments[prevIdx] + area2[b];
        }
      }
    }

    const cubes = Array.from({ length: maxColors }, () => ({ r0: 0, r1: 0, g0: 0, g1: 0, b0: 0, b1: 0, vol: 0 }));
    cubes[0].r1 = WU_SIDE_LENGTH - 1;
    cubes[0].g1 = WU_SIDE_LENGTH - 1;
    cubes[0].b1 = WU_SIDE_LENGTH - 1;
    const volVar = new Array(maxColors).fill(0.0);
    let generated = maxColors;
    let nxt = 0;
    for (let i = 1; i < maxColors; i++) {
      if (this._cut(cubes[nxt], cubes[i])) {
        volVar[nxt] = cubes[nxt].vol > 1 ? this._variance(cubes[nxt]) : 0.0;
        volVar[i] = cubes[i].vol > 1 ? this._variance(cubes[i]) : 0.0;
      } else {
        volVar[nxt] = 0.0;
        i--;
      }
      nxt = 0;
      let bestV = volVar[0];
      for (let j = 1; j <= i; j++) {
        if (volVar[j] > bestV) {
          bestV = volVar[j];
          nxt = j;
        }
      }
      if (bestV <= 0.0) {
        generated = i + 1;
        break;
      }
    }

    const results = [];
    for (let k = 0; k < generated; k++) {
      const cube = cubes[k];
      const w = this._volume(cube, this.weights);
      if (w > 0) {
        const r = pyRound(this._volume(cube, this.momentsR) / w);
        const g = pyRound(this._volume(cube, this.momentsG) / w);
        const b = pyRound(this._volume(cube, this.momentsB) / w);
        results.push(argbFromRgb(r, g, b));
      }
    }
    return results;
  }
}

function quantizeWsmeans(inputPixels, startingClusters, maxColors) {
  if (!inputPixels || inputPixels.length === 0) return new Map();
  const pixelToCount = new Map();
  const points = [];
  for (let i = 0; i < inputPixels.length; i++) {
    const px = inputPixels[i] >>> 0;
    const prev = pixelToCount.get(px);
    if (prev === undefined) {
      pixelToCount.set(px, 1);
      points.push(labFromArgb(px));
    } else {
      pixelToCount.set(px, prev + 1);
    }
  }
  const pointCount = pixelToCount.size;
  const counts = Array.from(pixelToCount.values());

  let clusterCount = Math.min(maxColors, pointCount);
  if (startingClusters.length > 0) {
    clusterCount = Math.min(clusterCount, startingClusters.length);
  }

  const clusters = startingClusters.slice(0, clusterCount).map((c) => labFromArgb(c >>> 0));
  const rng = new DeterministicRandom(0x42688);
  while (clusters.length < clusterCount) {
    clusters.push([rng.nextFloat() * 100.0, rng.nextFloat() * 201.0 - 100.0, rng.nextFloat() * 201.0 - 100.0]);
  }

  const clusterIndices = new Array(pointCount);
  for (let i = 0; i < pointCount; i++) {
    clusterIndices[i] = Math.floor(rng.nextFloat() * clusterCount);
  }
  const pixelCountSums = new Array(clusterCount).fill(0);

  for (let iteration = 0; iteration < WSMEANS_MAX_ITERATIONS; iteration++) {
    const distMatrix = Array.from({ length: clusterCount }, (_, i) =>
      Array.from({ length: clusterCount }, (__, j) => ({ distance: 0.0, index: j })),
    );
    for (let i = 0; i < clusterCount; i++) {
      const clI = clusters[i];
      for (let j = i + 1; j < clusterCount; j++) {
        const clJ = clusters[j];
        const dl = clI[0] - clJ[0];
        const da = clI[1] - clJ[1];
        const db = clI[2] - clJ[2];
        const d = dl * dl + da * da + db * db;
        distMatrix[j][i] = { distance: d, index: i };
        distMatrix[i][j] = { distance: d, index: j };
      }
      distMatrix[i].sort((a, b) => a.distance - b.distance || a.index - b.index);
    }

    let pointsMoved = 0;
    for (let i = 0; i < pointCount; i++) {
      const [p0, p1, p2] = points[i];
      const prevC = clusterIndices[i];
      const [c0, c1, c2] = clusters[prevC];
      const prevDist = (p0 - c0) ** 2 + (p1 - c1) ** 2 + (p2 - c2) ** 2;
      let minDist = prevDist;
      let newC = -1;
      const row = distMatrix[prevC];
      for (let k = 0; k < clusterCount; k++) {
        const { distance: distVal, index: j } = row[k];
        if (distVal >= 4.0 * prevDist) break;
        const [cj0, cj1, cj2] = clusters[j];
        const d = (p0 - cj0) ** 2 + (p1 - cj1) ** 2 + (p2 - cj2) ** 2;
        if (d < minDist) {
          minDist = d;
          newC = j;
        }
      }
      if (newC !== -1) {
        const distChange = Math.abs(Math.sqrt(minDist) - Math.sqrt(prevDist));
        if (distChange > WSMEANS_MIN_MOVEMENT_DISTANCE) {
          pointsMoved++;
          clusterIndices[i] = newC;
        }
      }
    }

    if (pointsMoved === 0 && iteration !== 0) break;

    const compA = new Array(clusterCount).fill(0.0);
    const compB = new Array(clusterCount).fill(0.0);
    const compC = new Array(clusterCount).fill(0.0);
    pixelCountSums.fill(0);
    for (let i = 0; i < pointCount; i++) {
      const ci = clusterIndices[i];
      const cnt = counts[i];
      const [p0, p1, p2] = points[i];
      pixelCountSums[ci] += cnt;
      compA[ci] += p0 * cnt;
      compB[ci] += p1 * cnt;
      compC[ci] += p2 * cnt;
    }
    for (let i = 0; i < clusterCount; i++) {
      const cnt = pixelCountSums[i];
      clusters[i] = cnt === 0
        ? [0.0, 0.0, 0.0]
        : [compA[i] / cnt, compB[i] / cnt, compC[i] / cnt];
    }
  }

  const out = new Map();
  for (let i = 0; i < clusterCount; i++) {
    const cnt = pixelCountSums[i];
    if (cnt === 0) continue;
    const argb = argbFromLab(clusters[i][0], clusters[i][1], clusters[i][2]);
    if (!out.has(argb)) out.set(argb, cnt);
  }
  return out;
}

export function quantizeCelebi(pixels, maxColors = 128) {
  if (!pixels || pixels.length === 0) return new Map();
  const wuClusters = new QuantizerWu().quantize(pixels, maxColors);
  return quantizeWsmeans(pixels, wuClusters, maxColors);
}

export function scoreColors(
  colorsToPopulation,
  { desired = 4, fallbackArgb = 0xFF6750A4, filter = true } = {},
) {
  const entriesSource = colorsToPopulation instanceof Map
    ? Array.from(colorsToPopulation.entries())
    : Object.entries(colorsToPopulation || {}).map(([k, v]) => [Number(k) >>> 0, v]);

  if (entriesSource.length === 0) {
    const hct = Hct.fromInt(fallbackArgb >>> 0);
    return [{
      argb: fallbackArgb >>> 0,
      hex: argbToHex(fallbackArgb),
      hue: pyRound(hct.hue * 100) / 100,
      chroma: pyRound(hct.chroma * 100) / 100,
      tone: pyRound(hct.tone * 100) / 100,
      population: 0,
      score: 0.0,
    }];
  }

  const huePop = new Array(360).fill(0);
  let popSum = 0;
  const entries = [];
  for (const [argb, pop] of entriesSource) {
    const uArgb = argb >>> 0;
    const hct = Hct.fromInt(uArgb);
    entries.push({ argb: uArgb, hct, pop });
    const hueIdx = Math.floor(hct.hue) % 360;
    huePop[hueIdx] += pop;
    popSum += pop;
  }
  if (popSum <= 0) popSum = 1;

  const hueExcited = new Array(360).fill(0.0);
  for (let h = 0; h < 360; h++) {
    const prop = huePop[h] / popSum;
    for (let i = h - 14; i < h + 16; i++) {
      const nh = ((i % 360) + 360) % 360;
      hueExcited[nh] += prop;
    }
  }

  const scored = [];
  for (const item of entries) {
    const hueRound = Math.floor(item.hct.hue + 0.5) % 360;
    const prop = hueExcited[hueRound];
    if (filter && (item.hct.chroma < 5.0 || prop <= 0.01)) continue;
    const propScore = prop * 100.0 * 0.7;
    const chromaWeight = item.hct.chroma < 48.0 ? 0.1 : 0.3;
    const chromaScore = (item.hct.chroma - 48.0) * chromaWeight;
    scored.push({ score: propScore + chromaScore, argb: item.argb, hct: item.hct, pop: item.pop });
  }

  scored.sort((a, b) => b.score - a.score || b.argb - a.argb);

  const chosen = [];
  for (let diffDeg = 90; diffDeg >= 15; diffDeg--) {
    chosen.length = 0;
    for (const item of scored) {
      const dup = chosen.some((ch) => (180.0 - Math.abs(Math.abs(item.hct.hue - ch.hct.hue) - 180.0)) < diffDeg);
      if (!dup) chosen.push(item);
      if (chosen.length >= desired) break;
    }
    if (chosen.length >= desired) break;
  }

  if (chosen.length === 0) {
    const hct = Hct.fromInt(fallbackArgb >>> 0);
    return [{
      argb: fallbackArgb >>> 0,
      hex: argbToHex(fallbackArgb),
      hue: pyRound(hct.hue * 100) / 100,
      chroma: pyRound(hct.chroma * 100) / 100,
      tone: pyRound(hct.tone * 100) / 100,
      population: 0,
      score: 0.0,
    }];
  }

  return chosen.map((item) => ({
    argb: item.argb,
    hex: argbToHex(item.argb),
    hue: pyRound(item.hct.hue * 100) / 100,
    chroma: pyRound(item.hct.chroma * 100) / 100,
    tone: pyRound(item.hct.tone * 100) / 100,
    population: item.pop,
    score: pyRound(item.score * 100) / 100,
  }));
}

export function extractSeedsFromRgba(rgbaBytes, { desired = 4, maxColors = 128 } = {}) {
  const opaque = [];
  const translucent = [];
  for (let i = 0; i <= rgbaBytes.length - 4; i += 4) {
    const a = rgbaBytes[i + 3];
    if (a === 255) {
      opaque.push(argbFromRgb(rgbaBytes[i], rgbaBytes[i + 1], rgbaBytes[i + 2]));
    } else if (a >= 64) {
      translucent.push(argbFromRgb(rgbaBytes[i], rgbaBytes[i + 1], rgbaBytes[i + 2]));
    }
  }
  const pixels = opaque.length >= 16 ? opaque : opaque.concat(translucent);
  const quantized = quantizeCelebi(pixels, maxColors);
  const candidates = scoreColors(quantized, { desired });
  return {
    primarySeed: candidates[0].hex,
    candidates,
  };
}

export async function extractSeedsFromImage(source, { maxDimension = 128, desired = 4 } = {}) {
  if (typeof document === 'undefined') {
    throw new Error('extractSeedsFromImage requires a browser DOM with HTMLCanvasElement; use extractSeedsFromRgba in headless/SSR.');
  }

  let drawable = null;
  let natW = 0;
  let natH = 0;
  let revokeUrl = '';

  try {
    if (typeof HTMLCanvasElement !== 'undefined' && source instanceof HTMLCanvasElement) {
      drawable = source;
      natW = source.width;
      natH = source.height;
    } else if (typeof ImageBitmap !== 'undefined' && source instanceof ImageBitmap) {
      drawable = source;
      natW = source.width;
      natH = source.height;
    } else if (typeof HTMLImageElement !== 'undefined' && source instanceof HTMLImageElement) {
      if (!source.complete) {
        await new Promise((resolve, reject) => {
          source.addEventListener('load', resolve, { once: true });
          source.addEventListener('error', () => reject(new Error('Image load failed')), { once: true });
        });
      }
      drawable = source;
      natW = source.naturalWidth || source.width;
      natH = source.naturalHeight || source.height;
    } else {
      const img = new Image();
      if (typeof Blob !== 'undefined' && source instanceof Blob) {
        revokeUrl = URL.createObjectURL(source);
        img.src = revokeUrl;
      } else if (typeof source === 'string') {
        img.crossOrigin = 'anonymous';
        img.src = source;
      } else {
        throw new Error('Unsupported image source passed to extractSeedsFromImage');
      }
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = () => reject(new Error('Could not decode uploaded image'));
      });
      if (typeof img.decode === 'function') {
        try { await img.decode(); } catch { /* onload already succeeded */ }
      }
      drawable = img;
      natW = img.naturalWidth || img.width;
      natH = img.naturalHeight || img.height;
    }

    if (!natW || !natH) {
      throw new Error('Image has zero dimensions');
    }

    const scale = Math.min(1.0, maxDimension / Math.max(1, natW, natH));
    const w = Math.max(1, Math.round(natW * scale));
    const h = Math.max(1, Math.round(natH * scale));
    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    if (!ctx) throw new Error('Could not create 2D canvas context');
    ctx.drawImage(drawable, 0, 0, w, h);
    const data = ctx.getImageData(0, 0, w, h).data;
    const extracted = extractSeedsFromRgba(data, { desired });
    return {
      ...extracted,
      width: natW,
      height: natH,
      sampledWidth: w,
      sampledHeight: h,
    };
  } finally {
    if (revokeUrl) URL.revokeObjectURL(revokeUrl);
  }
}

// ---------------------------------------------------------------------------
// CAM16 & HCT Solver
// ---------------------------------------------------------------------------

function makeDefaultViewingConditions() {
  const wp = WHITE_POINT_D65;
  const adaptingLuminance = (200.0 / Math.PI) * yFromLstar(50.0) / 100.0;
  const backgroundLstar = 50.0;
  const surround = 2.0;
  const rw = wp[0] * 0.401288 + wp[1] * 0.650173 + wp[2] * -0.051461;
  const gw = wp[0] * -0.250268 + wp[1] * 1.204414 + wp[2] * 0.045854;
  const bw = wp[0] * -0.002079 + wp[1] * 0.048952 + wp[2] * 0.953127;
  const f = 0.8 + surround / 10.0;
  const c = f >= 0.9 ? lerp(0.59, 0.69, (f - 0.9) * 10.0) : lerp(0.525, 0.59, (f - 0.8) * 10.0);
  const d = clamp(0.0, 1.0, f * (1.0 - (1.0 / 3.6) * Math.exp((-adaptingLuminance - 42.0) / 92.0)));
  const nc = f;
  const rgbD = [
    d * (100.0 / rw) + 1.0 - d,
    d * (100.0 / gw) + 1.0 - d,
    d * (100.0 / bw) + 1.0 - d,
  ];
  const k = 1.0 / (5.0 * adaptingLuminance + 1.0);
  const k4 = k ** 4;
  const k4f = 1.0 - k4;
  const fl = k4 * adaptingLuminance + 0.1 * k4f * k4f * ((5.0 * adaptingLuminance) ** (1.0 / 3.0));
  const n = yFromLstar(backgroundLstar) / wp[1];
  const z = 1.48 + Math.sqrt(n);
  const nbb = 0.725 / (n ** 0.2);
  const ncb = nbb;
  const af = [
    (fl * rgbD[0] * rw / 100.0) ** 0.42,
    (fl * rgbD[1] * gw / 100.0) ** 0.42,
    (fl * rgbD[2] * bw / 100.0) ** 0.42,
  ];
  const rgbe = af.map((a) => 400.0 * a / (a + 27.13));
  const aw = (2.0 * rgbe[0] + rgbe[1] + 0.05 * rgbe[2]) * nbb;
  return { n, aw, nbb, ncb, c, nc, rgbD, fl, flRoot: fl ** 0.25, z };
}

const VC_DEFAULT = makeDefaultViewingConditions();

function cam16FromInt(argb, vc = VC_DEFAULT) {
  const rl = linearized((argb >>> 16) & 0xFF);
  const gl = linearized((argb >>> 8) & 0xFF);
  const bl = linearized(argb & 0xFF);
  const [x, y, z] = matmul([rl, gl, bl], SRGB_TO_XYZ);
  const rc = 0.401288 * x + 0.650173 * y - 0.051461 * z;
  const gc = -0.250268 * x + 1.204414 * y + 0.045854 * z;
  const bc = -0.002079 * x + 0.048952 * y + 0.953127 * z;
  const rd = vc.rgbD[0] * rc;
  const gd = vc.rgbD[1] * gc;
  const bd = vc.rgbD[2] * bc;
  const raf = (vc.fl * Math.abs(rd) / 100.0) ** 0.42;
  const gaf = (vc.fl * Math.abs(gd) / 100.0) ** 0.42;
  const baf = (vc.fl * Math.abs(bd) / 100.0) ** 0.42;
  const ra = signum(rd) * 400.0 * raf / (raf + 27.13);
  const ga = signum(gd) * 400.0 * gaf / (gaf + 27.13);
  const ba = signum(bd) * 400.0 * baf / (baf + 27.13);
  const a = (11.0 * ra + -12.0 * ga + ba) / 11.0;
  const b = (ra + ga - 2.0 * ba) / 9.0;
  const u = (20.0 * ra + 20.0 * ga + 21.0 * ba) / 20.0;
  const p2 = (40.0 * ra + 20.0 * ga + ba) / 20.0;
  const hue = sanitizeDegrees((Math.atan2(b, a) * 180.0) / Math.PI);
  const ac = p2 * vc.nbb;
  const j = 100.0 * ((ac / vc.aw) ** (vc.c * vc.z));
  const huePrime = hue < 20.14 ? hue + 360.0 : hue;
  const ehue = 0.25 * (Math.cos((huePrime * Math.PI) / 180.0 + 2.0) + 3.8);
  const p1 = (50000.0 / 13.0) * ehue * vc.nc * vc.ncb;
  const t = p1 * Math.hypot(a, b) / (u + 0.305);
  const alpha = (t ** 0.9) * ((1.64 - (0.29 ** vc.n)) ** 0.73);
  const c = alpha * Math.sqrt(j / 100.0);
  return [hue, c, j];
}

function chromaticAdaptation(component) {
  const af = Math.abs(component) ** 0.42;
  return signum(component) * 400.0 * af / (af + 27.13);
}

function invChromaticAdaptation(adapted) {
  const aa = Math.abs(adapted);
  const base = Math.max(0.0, 27.13 * aa / (400.0 - aa));
  return signum(adapted) * (base ** (1.0 / 0.42));
}

function hueOfLinrgb(linrgb) {
  const sd = matmul(linrgb, SCALED_DISCOUNT_FROM_LINRGB);
  const ra = chromaticAdaptation(sd[0]);
  const ga = chromaticAdaptation(sd[1]);
  const ba = chromaticAdaptation(sd[2]);
  const a = (11.0 * ra + -12.0 * ga + ba) / 11.0;
  const b = (ra + ga - 2.0 * ba) / 9.0;
  return Math.atan2(b, a);
}

function inCyclicOrder(a, b, c) {
  return sanitizeRadians(b - a) < sanitizeRadians(c - a);
}

function nthVertex(y, n) {
  const [kr, kg, kb] = Y_FROM_LINRGB;
  const ca = n % 4 <= 1 ? 0.0 : 100.0;
  const cb = n % 2 === 0 ? 0.0 : 100.0;
  if (n < 4) {
    const r = (y - ca * kg - cb * kb) / kr;
    return r >= 0.0 && r <= 100.0 ? [r, ca, cb] : [-1.0, -1.0, -1.0];
  }
  if (n < 8) {
    const g = (y - cb * kr - ca * kb) / kg;
    return g >= 0.0 && g <= 100.0 ? [cb, g, ca] : [-1.0, -1.0, -1.0];
  }
  const b = (y - ca * kr - cb * kg) / kb;
  return b >= 0.0 && b <= 100.0 ? [ca, cb, b] : [-1.0, -1.0, -1.0];
}

function bisectToLimit(y, targetHue) {
  let left = [-1.0, -1.0, -1.0];
  let right = left;
  let leftHue = 0.0;
  let initialized = false;
  let uncut = true;
  for (let n = 0; n < 12; n++) {
    const mid = nthVertex(y, n);
    if (mid[0] < 0.0) continue;
    const midHue = hueOfLinrgb(mid);
    if (!initialized) {
      left = right = mid;
      leftHue = midHue;
      initialized = true;
      continue;
    }
    const rightHue = hueOfLinrgb(right);
    if (uncut || inCyclicOrder(leftHue, midHue, rightHue)) {
      uncut = false;
      if (inCyclicOrder(leftHue, targetHue, midHue)) {
        right = mid;
      } else {
        left = mid;
        leftHue = midHue;
      }
    }
  }

  for (let axis = 0; axis < 3; axis++) {
    if (left[axis] === right[axis]) continue;
    let lPlane;
    let rPlane;
    if (left[axis] < right[axis]) {
      lPlane = Math.floor(trueDelinearized(left[axis]) - 0.5);
      rPlane = Math.ceil(trueDelinearized(right[axis]) - 0.5);
    } else {
      lPlane = Math.ceil(trueDelinearized(left[axis]) - 0.5);
      rPlane = Math.floor(trueDelinearized(right[axis]) - 0.5);
    }
    for (let it = 0; it < 8; it++) {
      if (Math.abs(rPlane - lPlane) <= 1) break;
      const mPlane = Math.floor((lPlane + rPlane) / 2);
      const coord = CRITICAL_PLANES[Math.max(0, Math.min(CRITICAL_PLANES.length - 1, mPlane))];
      const t = (coord - left[axis]) / (right[axis] - left[axis]);
      const mid = [
        left[0] + (right[0] - left[0]) * t,
        left[1] + (right[1] - left[1]) * t,
        left[2] + (right[2] - left[2]) * t,
      ];
      const midHue = hueOfLinrgb(mid);
      if (inCyclicOrder(leftHue, targetHue, midHue)) {
        right = mid;
        rPlane = mPlane;
      } else {
        left = mid;
        leftHue = midHue;
        lPlane = mPlane;
      }
    }
  }
  return [
    (left[0] + right[0]) / 2.0,
    (left[1] + right[1]) / 2.0,
    (left[2] + right[2]) / 2.0,
  ];
}

function findResultByJ(hueRad, chroma, y) {
  let j = Math.sqrt(y) * 11.0;
  const vc = VC_DEFAULT;
  const tInnerCoeff = 1.0 / ((1.64 - (0.29 ** vc.n)) ** 0.73);
  const ehue = 0.25 * (Math.cos(hueRad + 2.0) + 3.8);
  const p1 = ehue * (50000.0 / 13.0) * vc.nc * vc.ncb;
  const hSin = Math.sin(hueRad);
  const hCos = Math.cos(hueRad);
  const [kr, kg, kb] = Y_FROM_LINRGB;
  for (let it = 0; it < 5; it++) {
    const jn = j / 100.0;
    const alpha = (chroma === 0.0 || j === 0.0) ? 0.0 : chroma / Math.sqrt(jn);
    const t = (alpha * tInnerCoeff) ** (1.0 / 0.9);
    const ac = vc.aw * (jn ** (1.0 / vc.c / vc.z));
    const p2 = ac / vc.nbb;
    const denom = 23.0 * p1 + 11.0 * t * hCos + 108.0 * t * hSin;
    if (denom === 0.0) return 0;
    const gamma = (23.0 * (p2 + 0.305) * t) / denom;
    const a = gamma * hCos;
    const b = gamma * hSin;
    const ra = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0;
    const ga = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0;
    const ba = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0;
    if (Math.abs(ra) >= 400.0 || Math.abs(ga) >= 400.0 || Math.abs(ba) >= 400.0) return 0;
    const linrgb = matmul(
      [invChromaticAdaptation(ra), invChromaticAdaptation(ga), invChromaticAdaptation(ba)],
      LINRGB_FROM_SCALED_DISCOUNT,
    );
    if (linrgb[0] < 0.0 || linrgb[1] < 0.0 || linrgb[2] < 0.0) return 0;
    const fnj = kr * linrgb[0] + kg * linrgb[1] + kb * linrgb[2];
    if (fnj <= 0.0) return 0;
    if (it === 4 || Math.abs(fnj - y) < 0.002) {
      if (linrgb[0] > 100.01 || linrgb[1] > 100.01 || linrgb[2] > 100.01) return 0;
      return argbFromLinrgb(linrgb);
    }
    j = j - ((fnj - y) * j) / (2.0 * fnj);
  }
  return 0;
}

export function hctSolveToInt(hueDeg, chroma, tone) {
  if (chroma < 1e-4 || tone < 1e-4 || tone > 99.9999) {
    return argbFromLstar(clamp(0.0, 100.0, tone));
  }
  const sanHue = sanitizeDegrees(hueDeg);
  const hueRad = (sanHue * Math.PI) / 180.0;
  const y = yFromLstar(tone);
  const exact = findResultByJ(hueRad, chroma, y);
  if (exact !== 0) return exact >>> 0;
  return argbFromLinrgb(bisectToLimit(y, hueRad));
}

export class Hct {
  constructor(argb, hue, chroma, tone) {
    this.argb = argb >>> 0;
    this.hue = hue;
    this.chroma = chroma;
    this.tone = tone;
  }

  static fromInt(argb) {
    const u = argb >>> 0;
    const [h, c] = cam16FromInt(u);
    const t = lstarFromArgb(u);
    return new Hct(u, h, c, t);
  }

  static fromHct(hue, chroma, tone) {
    return Hct.fromInt(hctSolveToInt(hue, chroma, tone));
  }

  get hex() {
    return argbToHex(this.argb);
  }

  static isBlue(hue) { return hue >= 250.0 && hue < 270.0; }
  static isYellow(hue) { return hue >= 105.0 && hue < 125.0; }
  static isCyan(hue) { return hue >= 170.0 && hue < 207.0; }
}

export class TonalPalette {
  constructor(hue, chroma) {
    this.hue = sanitizeDegrees(hue);
    this.chroma = Math.max(0.0, chroma);
    this._cache = new Map();
  }

  tone(toneVal, chromaMultiplier = 1.0) {
    if (Math.abs(chromaMultiplier - 1.0) < 1e-6 && Math.abs(toneVal - pyRound(toneVal)) < 1e-6) {
      const ti = pyRound(toneVal);
      if (!this._cache.has(ti)) {
        this._cache.set(ti, hctSolveToInt(this.hue, this.chroma, ti));
      }
      return this._cache.get(ti);
    }
    return hctSolveToInt(this.hue, this.chroma * chromaMultiplier, toneVal);
  }

  getHct(toneVal, chromaMultiplier = 1.0) {
    return Hct.fromInt(this.tone(toneVal, chromaMultiplier));
  }
}

function isDisliked(hct) {
  const h = pyRound(hct.hue);
  return h >= 90 && h <= 111 && pyRound(hct.chroma) > 16 && pyRound(hct.tone) < 65;
}

function fixIfDisliked(hct) {
  return isDisliked(hct) ? Hct.fromHct(hct.hue, hct.chroma, 70.0) : hct;
}

function temperatureComplement(source) {
  const hctsByHue = [];
  const temps = [];
  for (let h = 0; h < 360; h++) {
    const c = Hct.fromHct(h, source.chroma, source.tone);
    hctsByHue.push(c);
    const [, a, b] = labFromArgb(c.argb);
    const hue = sanitizeDegrees((Math.atan2(b, a) * 180.0) / Math.PI);
    const ch = Math.hypot(a, b);
    temps.push(-0.5 + 0.02 * (ch ** 1.07) * Math.cos((sanitizeDegrees(hue - 50.0) * Math.PI) / 180.0));
  }
  const indexed = Array.from({ length: 360 }, (_, i) => i).sort((a, b) => temps[a] - temps[b]);
  const coldestIdx = indexed[0];
  const warmestIdx = indexed[359];
  const coldestTemp = temps[coldestIdx];
  const warmestTemp = temps[warmestIdx];
  const tRange = warmestTemp - coldestTemp;
  if (tRange === 0.0) return source;
  const srcHue = pyRound(source.hue) % 360;
  const srcRel = (temps[srcHue] - coldestTemp) / tRange;
  const targetRel = 1.0 - srcRel;
  const isBetween = (angle, a, b) => (a > b ? (a <= angle || angle <= b) : (a <= angle && angle <= b));
  const cHue = coldestIdx;
  const wHue = warmestIdx;
  const sToW = isBetween(source.hue, cHue, wHue);
  const startH = sToW ? wHue : cHue;
  const endH = sToW ? cHue : wHue;
  let bestH = srcHue;
  let bestErr = 1e9;
  for (let add = 0; add <= 360; add++) {
    const h = Math.trunc(sanitizeDegrees(startH + add)) % 360;
    if (!isBetween(h, startH, endH)) continue;
    const rel = (temps[h] - coldestTemp) / tRange;
    const err = Math.abs(targetRel - rel);
    if (err < bestErr) {
      bestErr = err;
      bestH = h;
    }
  }
  return hctsByHue[bestH];
}

const Contrast = {
  ratioOfTones(ta, tb) {
    const ya = yFromLstar(clamp(0.0, 100.0, ta));
    const yb = yFromLstar(clamp(0.0, 100.0, tb));
    const lighter = ya > yb ? ya : yb;
    const darker = ya > yb ? yb : ya;
    return (lighter + 5.0) / (darker + 5.0);
  },
  lighter(tone, ratio) {
    if (tone < 0.0 || tone > 100.0) return -1.0;
    const dy = yFromLstar(tone);
    const ly = ratio * (dy + 5.0) - 5.0;
    const real = (ly + 5.0) / (dy + 5.0);
    if (real < ratio && Math.abs(real - ratio) > 0.04) return -1.0;
    const rv = lstarFromY(ly) + 0.4;
    return rv >= 0.0 && rv <= 100.0 ? rv : -1.0;
  },
  darker(tone, ratio) {
    if (tone < 0.0 || tone > 100.0) return -1.0;
    const ly = yFromLstar(tone);
    const dy = (ly + 5.0) / ratio - 5.0;
    const real = (ly + 5.0) / (dy + 5.0);
    if (real < ratio && Math.abs(real - ratio) > 0.04) return -1.0;
    const rv = lstarFromY(dy) - 0.4;
    return rv >= 0.0 && rv <= 100.0 ? rv : -1.0;
  },
  lighterUnsafe(tone, ratio) {
    const res = Contrast.lighter(tone, ratio);
    return res < 0.0 ? 100.0 : res;
  },
  darkerUnsafe(tone, ratio) {
    const res = Contrast.darker(tone, ratio);
    return res < 0.0 ? 0.0 : res;
  },
};

function contrastCurveGet(low, normal, medium, high, level) {
  if (level <= -1.0) return low;
  if (level < 0.0) return lerp(low, normal, level + 1.0);
  if (level < 0.5) return lerp(normal, medium, level / 0.5);
  if (level < 1.0) return lerp(medium, high, (level - 0.5) / 0.5);
  return high;
}

function getCurve2025Get(defaultContrast, level) {
  if (defaultContrast === 1.5) return contrastCurveGet(1.5, 1.5, 3.0, 4.5, level);
  if (defaultContrast === 3.0) return contrastCurveGet(3.0, 3.0, 4.5, 7.0, level);
  if (defaultContrast === 4.5) return contrastCurveGet(4.5, 4.5, 7.0, 11.0, level);
  if (defaultContrast === 6.0) return contrastCurveGet(6.0, 6.0, 7.0, 11.0, level);
  if (defaultContrast === 7.0) return contrastCurveGet(7.0, 7.0, 11.0, 21.0, level);
  if (defaultContrast === 9.0) return contrastCurveGet(9.0, 9.0, 11.0, 21.0, level);
  if (defaultContrast === 11.0) return contrastCurveGet(11.0, 11.0, 21.0, 21.0, level);
  if (defaultContrast === 21.0) return contrastCurveGet(21.0, 21.0, 21.0, 21.0, level);
  return contrastCurveGet(defaultContrast, defaultContrast, 7.0, 21.0, level);
}

function tonePrefersLightFg(tone) {
  return pyRound(tone) < 60;
}

function foregroundTone(bgTone, ratio) {
  const lighterT = Contrast.lighterUnsafe(bgTone, ratio);
  const darkerT = Contrast.darkerUnsafe(bgTone, ratio);
  const lRatio = Contrast.ratioOfTones(lighterT, bgTone);
  const dRatio = Contrast.ratioOfTones(darkerT, bgTone);
  if (tonePrefersLightFg(bgTone)) {
    const negligible = Math.abs(lRatio - dRatio) < 0.1 && lRatio < ratio && dRatio < ratio;
    return (lRatio >= ratio || lRatio >= dRatio || negligible) ? lighterT : darkerT;
  }
  return (dRatio >= ratio || dRatio >= lRatio) ? darkerT : lighterT;
}

function findBestToneForChroma(hue, chroma, tone, dec) {
  let ans = tone;
  let best = Hct.fromHct(hue, chroma, ans);
  while (best.chroma < chroma) {
    if (tone < 0 || tone > 100) break;
    tone += dec ? -1.0 : 1.0;
    const cand = Hct.fromHct(hue, chroma, tone);
    if (best.chroma < cand.chroma) {
      best = cand;
      ans = tone;
    }
  }
  return ans;
}

function tMaxC(pal, lo = 0.0, hi = 100.0, mult = 1.0) {
  const ans = findBestToneForChroma(pal.hue, pal.chroma * mult, 100.0, true);
  return clamp(lo, hi, ans);
}

function tMinC(pal, lo = 0.0, hi = 100.0) {
  const ans = findBestToneForChroma(pal.hue, pal.chroma, 0.0, false);
  return clamp(lo, hi, ans);
}

function findDesiredChromaByTone(hue, chroma, tone, dec) {
  let ans = tone;
  let closest = Hct.fromHct(hue, chroma, tone);
  if (closest.chroma < chroma) {
    let peak = closest.chroma;
    while (closest.chroma < chroma) {
      ans += dec ? -1.0 : 1.0;
      const cand = Hct.fromHct(hue, chroma, ans);
      if (peak > cand.chroma || Math.abs(cand.chroma - chroma) < 0.4) break;
      if (Math.abs(cand.chroma - chroma) < Math.abs(closest.chroma - chroma)) closest = cand;
      peak = Math.max(peak, cand.chroma);
    }
  }
  return ans;
}

function getRotatedHue(src, bps, rots) {
  const n = Math.min(bps.length - 1, rots.length);
  const h = src.hue;
  for (let i = 0; i < n; i++) {
    if (bps[i] <= h && h < bps[i + 1]) return sanitizeDegrees(h + rots[i]);
  }
  return h;
}

function getPiecewiseHue(src, bps, hues) {
  const n = Math.min(bps.length - 1, hues.length);
  const h = src.hue;
  for (let i = 0; i < n; i++) {
    if (bps[i] <= h && h < bps[i + 1]) return sanitizeDegrees(hues[i]);
  }
  return h;
}

function buildPalettes(seedHct, variant, isDark, specVersion) {
  const h = seedHct.hue;
  const c = seedHct.chroma;
  const effectiveSpec = (variant === 'monochrome' || variant === 'fidelity') ? '2021' : specVersion;

  if (effectiveSpec === '2025') {
    let p;
    let s;
    let t;
    let nh;
    let nc;
    let nvc;
    let ec;
    if (variant === 'neutral') {
      p = new TonalPalette(h, Hct.isBlue(h) ? 12.0 : 8.0);
      s = new TonalPalette(h, Hct.isBlue(h) ? 6.0 : 4.0);
      t = new TonalPalette(getRotatedHue(seedHct, [0, 38, 105, 161, 204, 278, 333, 360], [-32, 26, 10, -39, 24, -15, -32]), 20.0);
      nh = h;
      nc = 1.4;
      nvc = nc * 2.2;
      ec = 50.0;
    } else if (variant === 'tonal-spot') {
      p = new TonalPalette(h, isDark ? 26.0 : 32.0);
      s = new TonalPalette(h, 16.0);
      t = new TonalPalette(getRotatedHue(seedHct, [0, 20, 71, 161, 333, 360], [-40, 48, -32, 40, -32]), 28.0);
      nh = h;
      nc = 5.0;
      nvc = nc * 1.7;
      ec = 60.0;
    } else if (variant === 'expressive') {
      p = new TonalPalette(h, isDark ? 36.0 : 48.0);
      s = new TonalPalette(getRotatedHue(seedHct, [0, 105, 140, 204, 253, 278, 300, 333, 360], [-160, 155, -100, 96, -96, -156, -165, -160]), isDark ? 16.0 : 24.0);
      t = new TonalPalette(getRotatedHue(seedHct, [0, 105, 140, 204, 253, 278, 300, 333, 360], [-165, 160, -105, 101, -101, -160, -170, -165]), 48.0);
      nh = getRotatedHue(seedHct, [0, 71, 124, 253, 278, 300, 360], [10, 0, 10, 0, 10, 0]);
      nc = isDark ? (Hct.isYellow(nh) ? 6.0 : 14.0) : 18.0;
      nvc = nc * (nh >= 105.0 && nh < 125.0 ? 1.6 : 2.3);
      ec = 64.0;
    } else if (variant === 'vibrant') {
      p = new TonalPalette(h, 74.0);
      s = new TonalPalette(getRotatedHue(seedHct, [0, 38, 105, 140, 333, 360], [-14, 10, -14, 10, -14]), 56.0);
      t = new TonalPalette(getRotatedHue(seedHct, [0, 38, 71, 105, 140, 161, 253, 333, 360], [-72, 35, 24, -24, 62, 50, 62, -72]), 56.0);
      nh = getRotatedHue(seedHct, [0, 38, 105, 140, 333, 360], [-14, 10, -14, 10, -14]);
      nc = 28.0;
      nvc = nc * 1.29;
      ec = 80.0;
    } else {
      throw new Error(`Unsupported variant: ${variant}`);
    }
    const eh = getPiecewiseHue(seedHct, [0, 3, 13, 23, 33, 43, 153, 273, 360], [12, 22, 32, 12, 22, 32, 22, 12]);
    return {
      primary: p,
      secondary: s,
      tertiary: t,
      neutral: new TonalPalette(nh, nc),
      neutralVariant: new TonalPalette(nh, nvc),
      error: new TonalPalette(eh, ec),
    };
  }

  if (variant === 'monochrome') {
    return {
      primary: new TonalPalette(h, 0.0),
      secondary: new TonalPalette(h, 0.0),
      tertiary: new TonalPalette(h, 0.0),
      neutral: new TonalPalette(h, 0.0),
      neutralVariant: new TonalPalette(h, 0.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  if (variant === 'neutral') {
    return {
      primary: new TonalPalette(h, 12.0),
      secondary: new TonalPalette(h, 8.0),
      tertiary: new TonalPalette(h, 16.0),
      neutral: new TonalPalette(h, 2.0),
      neutralVariant: new TonalPalette(h, 2.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  if (variant === 'tonal-spot') {
    return {
      primary: new TonalPalette(h, 36.0),
      secondary: new TonalPalette(h, 16.0),
      tertiary: new TonalPalette(h + 60.0, 24.0),
      neutral: new TonalPalette(h, 6.0),
      neutralVariant: new TonalPalette(h, 8.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  if (variant === 'expressive') {
    const sh = getRotatedHue(seedHct, [0, 21, 51, 121, 151, 191, 271, 321, 360], [45, 95, 45, 20, 45, 90, 45, 45]);
    const th = getRotatedHue(seedHct, [0, 21, 51, 121, 151, 191, 271, 321, 360], [120, 120, 20, 45, 20, 15, 20, 120]);
    return {
      primary: new TonalPalette(h + 240.0, 40.0),
      secondary: new TonalPalette(sh, 24.0),
      tertiary: new TonalPalette(th, 32.0),
      neutral: new TonalPalette(h + 15.0, 8.0),
      neutralVariant: new TonalPalette(h + 15.0, 12.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  if (variant === 'vibrant') {
    const sh = getRotatedHue(seedHct, [0, 41, 61, 101, 131, 181, 251, 301, 360], [18, 15, 10, 12, 15, 18, 15, 12]);
    const th = getRotatedHue(seedHct, [0, 41, 61, 101, 131, 181, 251, 301, 360], [35, 30, 20, 25, 30, 35, 30, 25]);
    return {
      primary: new TonalPalette(h, 200.0),
      secondary: new TonalPalette(sh, 24.0),
      tertiary: new TonalPalette(th, 32.0),
      neutral: new TonalPalette(h, 10.0),
      neutralVariant: new TonalPalette(h, 12.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  if (variant === 'fidelity') {
    const comp = fixIfDisliked(temperatureComplement(seedHct));
    return {
      primary: new TonalPalette(h, c),
      secondary: new TonalPalette(h, Math.max(c - 32.0, c * 0.5)),
      tertiary: new TonalPalette(comp.hue, comp.chroma),
      neutral: new TonalPalette(h, c / 8.0),
      neutralVariant: new TonalPalette(h, c / 8.0 + 4.0),
      error: new TonalPalette(25.0, 84.0),
    };
  }
  throw new Error(`Unsupported variant: ${variant}`);
}

function solve2025Pair(roleARaw, roleBRaw, delta, polarity, constraint, isDark, bgA, reqA, bgB, reqB, roleAHasPair = false, roleBHasPair = true) {
  const absDelta = (
    polarity === 'darker'
    || (polarity === 'relative_lighter' && isDark)
    || (polarity === 'relative_darker' && !isDark)
  ) ? -delta : delta;

  const applyBgAndClamp = (toneVal, bgT, req) => {
    let tv = toneVal;
    if (bgT != null && req != null) {
      if (!(Contrast.ratioOfTones(bgT, tv) >= req)) {
        tv = foregroundTone(bgT, req);
      }
    }
    return tv >= 57.0 ? clamp(65.0, 100.0, tv) : clamp(0.0, 49.0, tv);
  };

  const applyPair = (selfRaw, refResolved, amRoleA, bgT, req) => {
    const relDelta = absDelta * (amRoleA ? 1.0 : -1.0);
    let st;
    if (constraint === 'exact') {
      st = clamp(0.0, 100.0, refResolved + relDelta);
    } else if (constraint === 'nearer') {
      st = relDelta > 0.0
        ? clamp(0.0, 100.0, clamp(refResolved, refResolved + relDelta, selfRaw))
        : clamp(0.0, 100.0, clamp(refResolved + relDelta, refResolved, selfRaw));
    } else {
      st = relDelta > 0.0
        ? clamp(refResolved + relDelta, 100.0, selfRaw)
        : clamp(0.0, refResolved + relDelta, selfRaw);
    }
    return applyBgAndClamp(st, bgT, req);
  };

  const resA = !roleAHasPair
    ? applyBgAndClamp(roleARaw, bgA, reqA)
    : applyPair(roleARaw, applyBgAndClamp(roleBRaw, bgB, reqB), true, bgA, reqA);
  const resB = roleBHasPair
    ? applyPair(roleBRaw, resA, false, bgB, reqB)
    : applyBgAndClamp(roleBRaw, bgB, reqB);
  return [resA, resB];
}

function resolvePairedTones(roleATone, roleBTone, delta, polarity, constraint, isDark, bgA, reqA, bgB, reqB, aIsBg, bIsBg) {
  const absDelta = (
    polarity === 'darker'
    || (polarity === 'relative_lighter' && isDark)
    || (polarity === 'relative_darker' && !isDark)
  ) ? -delta : delta;

  const finish = (toneVal, bgT, req, isBg) => {
    let tv = toneVal;
    if (bgT != null && req != null) {
      if (!(Contrast.ratioOfTones(bgT, tv) >= req)) tv = foregroundTone(bgT, req);
    }
    if (isBg) tv = tv >= 57.0 ? clamp(65.0, 100.0, tv) : clamp(0.0, 49.0, tv);
    return tv;
  };

  const refB = finish(roleBTone, bgB, reqB, bIsBg);
  let tA;
  if (constraint === 'exact') {
    tA = clamp(0.0, 100.0, refB + absDelta);
  } else if (constraint === 'nearer') {
    tA = absDelta > 0
      ? clamp(0.0, 100.0, clamp(refB, refB + absDelta, roleATone))
      : clamp(0.0, 100.0, clamp(refB + absDelta, refB, roleATone));
  } else {
    tA = absDelta > 0
      ? clamp(refB + absDelta, 100.0, roleATone)
      : clamp(0.0, refB + absDelta, roleATone);
  }
  tA = finish(tA, bgA, reqA, aIsBg);
  return [tA, refB];
}

function resolveFg(bgTone, initialTone, desiredRatio, contrastLevel, isBg = false) {
  let ans = initialTone == null
    ? foregroundTone(bgTone, desiredRatio)
    : ((Contrast.ratioOfTones(bgTone, initialTone) >= desiredRatio && contrastLevel >= 0.0)
      ? initialTone
      : foregroundTone(bgTone, desiredRatio));
  if (isBg) ans = ans >= 57.0 ? clamp(65.0, 100.0, ans) : clamp(0.0, 49.0, ans);
  return ans;
}

function surfaceChromaMult(variant, nh, isDark, role) {
  if (role === 'surface_dim' && !isDark) {
    if (variant === 'neutral') return 2.5;
    if (variant === 'tonal-spot') return 1.7;
    if (variant === 'expressive') return Hct.isYellow(nh) ? 2.7 : 1.75;
    if (variant === 'vibrant') return 1.36;
  } else if (role === 'surface_bright' && isDark) {
    if (variant === 'neutral') return 2.5;
    if (variant === 'tonal-spot') return 1.7;
    if (variant === 'expressive') return Hct.isYellow(nh) ? 2.7 : 1.75;
    if (variant === 'vibrant') return 1.36;
  } else if (role === 'surface_container_low') {
    if (variant === 'neutral') return 1.3;
    if (variant === 'tonal-spot') return 1.25;
    if (variant === 'expressive') return Hct.isYellow(nh) ? 1.3 : 1.15;
    if (variant === 'vibrant') return 1.08;
  } else if (role === 'surface_container') {
    if (variant === 'neutral') return 1.6;
    if (variant === 'tonal-spot') return 1.4;
    if (variant === 'expressive') return Hct.isYellow(nh) ? 1.6 : 1.3;
    if (variant === 'vibrant') return 1.15;
  } else if (role === 'surface_container_high') {
    if (variant === 'neutral') return 1.9;
    if (variant === 'tonal-spot') return 1.5;
    if (variant === 'expressive') return Hct.isYellow(nh) ? 1.95 : 1.45;
    if (variant === 'vibrant') return 1.22;
  } else if (['surface_container_highest', 'on_surface', 'on_surface_variant', 'outline', 'outline_variant'].includes(role)) {
    if (variant === 'neutral') return 2.2;
    if (variant === 'tonal-spot') return 1.7;
    if (variant === 'expressive') {
      if (role === 'surface_container_highest') return Hct.isYellow(nh) ? 2.3 : 1.6;
      return Hct.isYellow(nh) ? (isDark ? 3.0 : 2.3) : 1.6;
    }
    if (variant === 'vibrant' && role === 'surface_container_highest') return 1.29;
  }
  return 1.0;
}

export function generateScheme(
  seedHex,
  {
    variant = 'expressive',
    isDark = false,
    contrastLevel = 0.0,
    specVersion = '2025',
    minPairContrast = null,
  } = {},
) {
  const seedHct = Hct.fromInt(hexToArgb(seedHex));
  const effectiveSpec = (variant === 'monochrome' || variant === 'fidelity') ? '2021' : specVersion;
  const pals = buildPalettes(seedHct, variant, isDark, effectiveSpec);
  const { primary: p, secondary: s, tertiary: t, neutral: n, neutralVariant: nv, error: e } = pals;
  const nh = n.hue;

  const roles = {};
  const roleTones = {};
  const put = (name, pal, toneVal, mult = 1.0) => {
    roleTones[name] = toneVal;
    roles[name] = argbToHex(pal.tone(toneVal, mult));
  };

  if (effectiveSpec === '2025') {
    const isYelN = Hct.isYellow(nh);
    const sT = isDark ? 4.0 : (isYelN ? 99.0 : (variant === 'vibrant' ? 97.0 : 98.0));
    let dimT = isDark ? 4.0 : (isYelN ? 90.0 : (variant === 'vibrant' ? 85.0 : 87.0));
    let briT = isDark ? 18.0 : (isYelN ? 99.0 : (variant === 'vibrant' ? 97.0 : 98.0));
    const lowT = isDark ? 6.0 : (isYelN ? 98.0 : (variant === 'vibrant' ? 95.0 : 96.0));
    const conT = isDark ? 9.0 : (isYelN ? 96.0 : (variant === 'vibrant' ? 92.0 : 94.0));
    let hiT = isDark ? 12.0 : (isYelN ? 94.0 : (variant === 'vibrant' ? 90.0 : 92.0));
    let hstT = isDark ? 15.0 : (isYelN ? 92.0 : (variant === 'vibrant' ? 88.0 : 90.0));

    if (contrastLevel >= 0.5 && isDark) {
      hiT = contrastLevel < 1.0 ? 17.0 : 22.0;
      hstT = contrastLevel < 1.0 ? 22.0 : 26.0;
      briT = contrastLevel < 1.0 ? 22.0 : 28.0;
    } else if (contrastLevel >= 0.5 && !isDark) {
      hiT = Math.min(hiT, contrastLevel < 1.0 ? 88.0 : 85.0);
      hstT = Math.min(hstT, contrastLevel < 1.0 ? 84.0 : 80.0);
      dimT = Math.min(dimT, contrastLevel < 1.0 ? 80.0 : 75.0);
    }
    const highestT = isDark ? briT : dimT;

    put('surface', n, sT);
    put('surface-dim', n, dimT, surfaceChromaMult(variant, nh, isDark, 'surface_dim'));
    put('surface-bright', n, briT, surfaceChromaMult(variant, nh, isDark, 'surface_bright'));
    put('surface-container-lowest', n, isDark ? 0.0 : 100.0);
    put('surface-container-low', n, lowT, surfaceChromaMult(variant, nh, isDark, 'surface_container_low'));
    put('surface-container', n, conT, surfaceChromaMult(variant, nh, isDark, 'surface_container'));
    put('surface-container-high', n, hiT, surfaceChromaMult(variant, nh, isDark, 'surface_container_high'));
    put('surface-container-highest', n, hstT, surfaceChromaMult(variant, nh, isDark, 'surface_container_highest'));
    put('surface-variant', n, hstT, surfaceChromaMult(variant, nh, isDark, 'surface_container_highest'));

    const onSInit = variant === 'vibrant' ? tMaxC(n, 0.0, 100.0, 1.1) : null;
    const onST = resolveFg(highestT, onSInit, getCurve2025Get(isDark ? 11.0 : 9.0, contrastLevel), contrastLevel);
    put('on-surface', n, onST, surfaceChromaMult(variant, nh, isDark, 'on_surface'));

    const onSvT = resolveFg(highestT, null, getCurve2025Get(isDark ? 6.0 : 4.5, contrastLevel), contrastLevel);
    put('on-surface-variant', n, onSvT, surfaceChromaMult(variant, nh, isDark, 'on_surface_variant'));

    const outT = resolveFg(highestT, null, getCurve2025Get(3.0, contrastLevel), contrastLevel);
    put('outline', n, outT, surfaceChromaMult(variant, nh, isDark, 'outline'));

    const ovT = resolveFg(highestT, null, getCurve2025Get(1.5, contrastLevel), contrastLevel);
    put('outline-variant', n, ovT, surfaceChromaMult(variant, nh, isDark, 'outline_variant'));

    const invST = isDark ? 98.0 : 4.0;
    put('inverse-surface', n, invST);
    put('inverse-on-surface', n, resolveFg(invST, null, getCurve2025Get(7.0, contrastLevel), contrastLevel));

    let pRaw;
    let pcRaw;
    if (variant === 'neutral') {
      pRaw = isDark ? 80.0 : 40.0;
      pcRaw = isDark ? 30.0 : 90.0;
    } else if (variant === 'tonal-spot') {
      pRaw = isDark ? 80.0 : tMaxC(p);
      pcRaw = isDark ? tMinC(p, 35.0, 93.0) : tMaxC(p, 0.0, 90.0);
    } else if (variant === 'expressive') {
      pRaw = tMaxC(p, 0.0, Hct.isYellow(p.hue) ? 25.0 : (Hct.isCyan(p.hue) ? 88.0 : 98.0));
      pcRaw = isDark ? tMaxC(p, 30.0, 93.0) : tMaxC(p, 78.0, Hct.isCyan(p.hue) ? 88.0 : 90.0);
    } else {
      pRaw = tMaxC(p, 0.0, Hct.isCyan(p.hue) ? 88.0 : 98.0);
      pcRaw = isDark ? tMinC(p, 66.0, 93.0) : tMaxC(p, 66.0, Hct.isCyan(p.hue) ? 88.0 : 93.0);
    }
    const pReq = getCurve2025Get(4.5, contrastLevel);
    const pcReq = contrastLevel > 0.0 ? getCurve2025Get(1.5, contrastLevel) : null;
    const [pcT, pT] = solve2025Pair(pcRaw, pRaw, 5.0, 'relative_lighter', 'farther', isDark, highestT, pcReq, highestT, pReq);
    put('primary', p, pT);
    put('on-primary', p, resolveFg(pT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('primary-container', p, pcT);
    put('on-primary-container', p, resolveFg(pcT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('inverse-primary', p, resolveFg(invST, tMaxC(p), getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('surface-tint', p, pT);

    let sRaw;
    let scRaw;
    if (variant === 'neutral') {
      sRaw = isDark ? tMinC(s, 0.0, 98.0) : tMaxC(s);
      scRaw = isDark ? 25.0 : 90.0;
    } else if (variant === 'vibrant') {
      sRaw = tMaxC(s, 0.0, isDark ? 90.0 : 98.0);
      scRaw = isDark ? tMinC(s, 30.0, 40.0) : tMaxC(s, 84.0, 90.0);
    } else if (variant === 'expressive') {
      sRaw = isDark ? 80.0 : tMaxC(s);
      scRaw = isDark ? 15.0 : tMaxC(s, 90.0, 95.0);
    } else {
      sRaw = isDark ? 80.0 : tMaxC(s);
      scRaw = isDark ? 25.0 : 90.0;
    }
    const [scT, sT2] = solve2025Pair(scRaw, sRaw, 5.0, 'relative_lighter', 'farther', isDark, highestT, pcReq, highestT, pReq);
    put('secondary', s, sT2);
    put('on-secondary', s, resolveFg(sT2, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('secondary-container', s, scT);
    put('on-secondary-container', s, resolveFg(scT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));

    const tRaw = (variant === 'expressive' || variant === 'vibrant')
      ? tMaxC(t, 0.0, Hct.isCyan(t.hue) ? 88.0 : (isDark ? 98.0 : 100.0))
      : (isDark ? tMaxC(t, 0.0, 98.0) : tMaxC(t));
    let tcRaw;
    if (variant === 'neutral') tcRaw = isDark ? tMaxC(t, 0.0, 93.0) : tMaxC(t, 0.0, 96.0);
    else if (variant === 'tonal-spot') tcRaw = tMaxC(t, 0.0, isDark ? 93.0 : 100.0);
    else if (variant === 'expressive') tcRaw = tMaxC(t, 75.0, Hct.isCyan(t.hue) ? 88.0 : (isDark ? 93.0 : 100.0));
    else tcRaw = isDark ? tMaxC(t, 0.0, 93.0) : tMaxC(t, 72.0, 100.0);
    const [tcT, tT] = solve2025Pair(tcRaw, tRaw, 5.0, 'relative_lighter', 'farther', isDark, highestT, pcReq, highestT, pReq);
    put('tertiary', t, tT);
    put('on-tertiary', t, resolveFg(tT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('tertiary-container', t, tcT);
    put('on-tertiary-container', t, resolveFg(tcT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));

    const eRaw = isDark ? tMinC(e, 0.0, 98.0) : tMaxC(e);
    const ecRaw = isDark ? tMinC(e, 30.0, 93.0) : tMaxC(e, 0.0, 90.0);
    const [ecT, eT] = solve2025Pair(ecRaw, eRaw, 5.0, 'relative_lighter', 'farther', isDark, highestT, pcReq, highestT, pReq);
    put('error', e, eT);
    put('on-error', e, resolveFg(eT, null, getCurve2025Get(6.0, contrastLevel), contrastLevel));
    put('error-container', e, ecT);
    put('on-error-container', e, resolveFg(ecT, null, getCurve2025Get(4.5, contrastLevel), contrastLevel));

    if (!isDark) {
      const lightScheme = contrastLevel !== 0.0
        ? generateScheme(seedHex, { variant, isDark: false, contrastLevel: 0.0, specVersion, minPairContrast })
        : null;
      for (const [fam, pal] of [['primary', p], ['secondary', s], ['tertiary', t]]) {
        let fxT = lightScheme == null ? roleTones[`${fam}-container`] : lstarFromArgb(hexToArgb(lightScheme[`${fam}-fixed`]));
        if (contrastLevel > 0.0) {
          fxT = resolveFg(highestT, fxT, getCurve2025Get(1.5, contrastLevel), contrastLevel, true);
        }
        const fxdT = clamp(0.0, 100.0, fxT - 5.0);
        put(`${fam}-fixed`, pal, fxT);
        put(`${fam}-fixed-dim`, pal, fxdT);
        put(`on-${fam}-fixed`, pal, resolveFg(fxdT, null, getCurve2025Get(7.0, contrastLevel), contrastLevel));
        put(`on-${fam}-fixed-variant`, pal, resolveFg(fxdT, null, getCurve2025Get(4.5, contrastLevel), contrastLevel));
      }
    }
  } else {
    const isMono = variant === 'monochrome';
    const isFid = variant === 'fidelity';
    const sT = isDark ? 6.0 : 98.0;
    const dimT = isDark ? 6.0 : contrastCurveGet(87.0, 87.0, 80.0, 75.0, contrastLevel);
    const briT = isDark ? contrastCurveGet(24.0, 24.0, 29.0, 34.0, contrastLevel) : 98.0;
    const lowT = isDark ? contrastCurveGet(10.0, 10.0, 11.0, 12.0, contrastLevel) : contrastCurveGet(96.0, 96.0, 96.0, 95.0, contrastLevel);
    const conT = isDark ? contrastCurveGet(12.0, 12.0, 16.0, 20.0, contrastLevel) : contrastCurveGet(94.0, 94.0, 92.0, 90.0, contrastLevel);
    const hiT = isDark ? contrastCurveGet(17.0, 17.0, 21.0, 25.0, contrastLevel) : contrastCurveGet(92.0, 92.0, 88.0, 85.0, contrastLevel);
    const hstT = isDark ? contrastCurveGet(22.0, 22.0, 26.0, 30.0, contrastLevel) : contrastCurveGet(90.0, 90.0, 84.0, 80.0, contrastLevel);
    const highestT = isDark ? briT : dimT;

    put('surface', n, sT);
    put('surface-dim', n, dimT);
    put('surface-bright', n, briT);
    put('surface-container-lowest', n, isDark ? contrastCurveGet(4.0, 4.0, 2.0, 0.0, contrastLevel) : 100.0);
    put('surface-container-low', n, lowT);
    put('surface-container', n, conT);
    put('surface-container-high', n, hiT);
    put('surface-container-highest', n, hstT);
    put('surface-variant', nv, isDark ? 30.0 : 90.0);
    put('on-surface', n, resolveFg(highestT, isDark ? 90.0 : 10.0, contrastCurveGet(4.5, 7.0, 11.0, 21.0, contrastLevel), contrastLevel));
    put('on-surface-variant', nv, resolveFg(highestT, isDark ? 80.0 : 30.0, contrastCurveGet(3.0, 4.5, 7.0, 11.0, contrastLevel), contrastLevel));
    put('outline', nv, resolveFg(highestT, isDark ? 60.0 : 50.0, contrastCurveGet(1.5, 3.0, 4.5, 7.0, contrastLevel), contrastLevel));
    put('outline-variant', nv, resolveFg(highestT, isDark ? 30.0 : 80.0, contrastCurveGet(1.0, 1.0, 3.0, 4.5, contrastLevel), contrastLevel));
    const invST = isDark ? 90.0 : 20.0;
    put('inverse-surface', n, invST);
    put('inverse-on-surface', n, resolveFg(invST, isDark ? 20.0 : 95.0, contrastCurveGet(4.5, 7.0, 11.0, 21.0, contrastLevel), contrastLevel));

    const accReq = contrastCurveGet(3.0, 4.5, 7.0, 7.0, contrastLevel);
    const cReq = contrastCurveGet(1.0, 1.0, 3.0, 4.5, contrastLevel);
    const onReq = contrastCurveGet(4.5, 7.0, 11.0, 21.0, contrastLevel);
    const onCReq = contrastCurveGet(3.0, 4.5, 7.0, 11.0, contrastLevel);

    const do2021Family = (fam, pal, mainInit, onInit, contInit, onContInit) => {
      const [mt, ct] = resolvePairedTones(mainInit, contInit, 10.0, 'nearer', 'nearer', isDark, highestT, accReq, highestT, cReq, true, true);
      put(fam, pal, mt);
      put(`on-${fam}`, pal, resolveFg(mt, onInit, onReq, contrastLevel));
      put(`${fam}-container`, pal, ct);
      put(`on-${fam}-container`, pal, resolveFg(ct, onContInit, onCReq, contrastLevel));
      return mt;
    };

    const pInit = isMono ? (isDark ? 100.0 : 0.0) : (isDark ? 80.0 : 40.0);
    const onPInit = isMono ? (isDark ? 10.0 : 90.0) : (isDark ? 20.0 : 100.0);
    const pcInit = isFid ? seedHct.tone : (isMono ? (isDark ? 85.0 : 25.0) : (isDark ? 30.0 : 90.0));
    const onPcInit = isFid ? foregroundTone(pcInit, 4.5) : (isMono ? (isDark ? 0.0 : 100.0) : (isDark ? 90.0 : 30.0));
    const pT = do2021Family('primary', p, pInit, onPInit, pcInit, onPcInit);
    put('inverse-primary', p, resolveFg(invST, isDark ? 40.0 : 80.0, accReq, contrastLevel));
    put('surface-tint', p, pT);

    const scInit0 = isMono ? (isDark ? 30.0 : 85.0) : (isDark ? 30.0 : 90.0);
    const scInit = isFid ? findDesiredChromaByTone(s.hue, s.chroma, scInit0, !isDark) : scInit0;
    const onScInit = isMono ? (isDark ? 90.0 : 10.0) : (isFid ? foregroundTone(scInit, 4.5) : (isDark ? 90.0 : 30.0));
    do2021Family('secondary', s, isDark ? 80.0 : 40.0, isMono ? (isDark ? 10.0 : 100.0) : (isDark ? 20.0 : 100.0), scInit, onScInit);

    const tInit = isMono ? (isDark ? 90.0 : 25.0) : (isDark ? 80.0 : 40.0);
    const onTInit = isMono ? (isDark ? 10.0 : 90.0) : (isDark ? 20.0 : 100.0);
    const tcInit = isMono ? (isDark ? 60.0 : 49.0) : (isFid ? fixIfDisliked(t.getHct(seedHct.tone)).tone : (isDark ? 30.0 : 90.0));
    const onTcInit = isMono ? (isDark ? 0.0 : 100.0) : (isFid ? foregroundTone(tcInit, 4.5) : (isDark ? 90.0 : 30.0));
    do2021Family('tertiary', t, tInit, onTInit, tcInit, onTcInit);

    do2021Family('error', e, isDark ? 80.0 : 40.0, isDark ? 20.0 : 100.0, isDark ? 30.0 : 90.0, isDark ? 90.0 : 30.0);

    if (!isDark) {
      for (const [fam, pal, fT, onF, onFv] of [
        ['primary', p, isMono ? 40.0 : 90.0, isMono ? 100.0 : 10.0, isMono ? 90.0 : 30.0],
        ['secondary', s, isMono ? 80.0 : 90.0, 10.0, isMono ? 25.0 : 30.0],
        ['tertiary', t, isMono ? 40.0 : 90.0, isMono ? 100.0 : 10.0, isMono ? 90.0 : 30.0],
      ]) {
        put(`${fam}-fixed`, pal, resolveFg(highestT, fT, cReq, contrastLevel, true));
        put(`${fam}-fixed-dim`, pal, clamp(0.0, 100.0, roleTones[`${fam}-fixed`] - 10.0));
        const bottleneckT = onF >= 50.0 ? roleTones[`${fam}-fixed`] : roleTones[`${fam}-fixed-dim`];
        put(`on-${fam}-fixed`, pal, resolveFg(bottleneckT, onF, onReq, contrastLevel));
        put(`on-${fam}-fixed-variant`, pal, resolveFg(bottleneckT, onFv, onCReq, contrastLevel));
      }
    }
  }

  roles.scrim = '#000000';
  roles.shadow = '#000000';

  const floor = minPairContrast != null
    ? minPairContrast
    : (contrastLevel >= 1.0 ? 7.0 : (contrastLevel >= 0.5 ? 6.0 : 4.5));

  const guardPairs = [
    ['primary', 'on-primary', p],
    ['primary-container', 'on-primary-container', p],
    ['secondary', 'on-secondary', s],
    ['secondary-container', 'on-secondary-container', s],
    ['tertiary', 'on-tertiary', t],
    ['tertiary-container', 'on-tertiary-container', t],
    ['error', 'on-error', e],
    ['error-container', 'on-error-container', e],
    ['surface', 'on-surface', n],
    ['surface-container-low', 'on-surface', n],
    ['surface-container', 'on-surface', n],
    ['surface-container-high', 'on-surface-variant', n],
    ['inverse-surface', 'inverse-on-surface', n],
  ];

  for (const [bgName, fgName, fgPal] of guardPairs) {
    if (srgbContrastRatio(roles[bgName], roles[fgName]) >= floor) continue;
    const wMax = srgbContrastRatio(roles[bgName], '#FFFFFF');
    const bMax = srgbContrastRatio(roles[bgName], '#000000');
    if (Math.max(wMax, bMax) < floor) {
      const bgT = lstarFromArgb(hexToArgb(roles[bgName]));
      const nudgedT = bgT < 57.0
        ? Contrast.darkerUnsafe(100.0, floor + 0.6)
        : Contrast.lighterUnsafe(0.0, floor + 0.6);
      roles[bgName] = argbToHex(fgPal.tone(nudgedT));
    }
    const bgT = lstarFromArgb(hexToArgb(roles[bgName]));
    let bestHex = roles[fgName];
    let bestRatio = srgbContrastRatio(roles[bgName], bestHex);
    for (const deltaReq of [floor + 0.5, floor + 1.5, 11.0, 21.0]) {
      const candT = foregroundTone(bgT, deltaReq);
      const candHex = argbToHex(fgPal.tone(candT));
      const cr = srgbContrastRatio(roles[bgName], candHex);
      if (cr > bestRatio) {
        bestRatio = cr;
        bestHex = candHex;
      }
      if (cr >= floor) break;
    }
    if (bestRatio < floor) {
      const wCr = srgbContrastRatio(roles[bgName], '#FFFFFF');
      const bCr = srgbContrastRatio(roles[bgName], '#000000');
      bestHex = wCr >= bCr ? '#FFFFFF' : '#000000';
    }
    roles[fgName] = bestHex;
  }

  if (isDark) {
    const lightFixed = generateScheme(seedHex, { variant, isDark: false, contrastLevel, specVersion, minPairContrast });
    for (const fam of ['primary', 'secondary', 'tertiary']) {
      for (const key of [`${fam}-fixed`, `${fam}-fixed-dim`, `on-${fam}-fixed`, `on-${fam}-fixed-variant`]) {
        roles[key] = lightFixed[key];
      }
    }
  } else {
    const fxStep = effectiveSpec === '2025' ? 5.0 : 10.0;
    for (const [fam, pal] of [['primary', p], ['secondary', s], ['tertiary', t]]) {
      const fRole = `${fam}-fixed`;
      const fdRole = `${fam}-fixed-dim`;
      const onRole = `on-${fam}-fixed`;
      const onvRole = `on-${fam}-fixed-variant`;
      let fT = lstarFromArgb(hexToArgb(roles[fRole]));
      let fdT = lstarFromArgb(hexToArgb(roles[fdRole]));
      const minExisting = Math.min(
        srgbContrastRatio(roles[fRole], roles[onRole]),
        srgbContrastRatio(roles[fdRole], roles[onRole]),
        srgbContrastRatio(roles[fRole], roles[onvRole]),
        srgbContrastRatio(roles[fdRole], roles[onvRole]),
      );
      if (minExisting >= floor) continue;

      const lightText = fT < 57.0;
      let bottleneckT;
      if (lightText) {
        const capT = Contrast.darkerUnsafe(100.0, floor + 0.6);
        if (fT > capT || srgbContrastRatio(roles[fRole], '#FFFFFF') < floor) {
          fT = Math.min(fT, capT);
          fdT = clamp(0.0, 100.0, Math.min(fdT, fT - fxStep));
          roles[fRole] = argbToHex(pal.tone(fT));
          roles[fdRole] = argbToHex(pal.tone(fdT));
        }
        bottleneckT = fT;
      } else {
        const floorT = Contrast.lighterUnsafe(0.0, floor + 0.6);
        if (fdT < floorT || srgbContrastRatio(roles[fdRole], '#000000') < floor) {
          fdT = Math.max(fdT, floorT);
          fT = clamp(0.0, 100.0, Math.max(fT, fdT + fxStep));
          roles[fRole] = argbToHex(pal.tone(fT));
          roles[fdRole] = argbToHex(pal.tone(fdT));
        }
        bottleneckT = fdT;
      }

      for (const fgRole of [onRole, onvRole]) {
        const curCr = Math.min(
          srgbContrastRatio(roles[fRole], roles[fgRole]),
          srgbContrastRatio(roles[fdRole], roles[fgRole]),
        );
        if (curCr >= floor) continue;
        let bestHex = roles[fgRole];
        let bestMin = curCr;
        for (const deltaReq of [floor + 0.5, floor + 1.5, 11.0, 21.0]) {
          const candT = foregroundTone(bottleneckT, deltaReq);
          const candHex = argbToHex(pal.tone(candT));
          const crBoth = Math.min(
            srgbContrastRatio(roles[fRole], candHex),
            srgbContrastRatio(roles[fdRole], candHex),
          );
          if (crBoth > bestMin) {
            bestMin = crBoth;
            bestHex = candHex;
          }
          if (crBoth >= floor) break;
        }
        if (bestMin < floor) {
          const wCr = Math.min(srgbContrastRatio(roles[fRole], '#FFFFFF'), srgbContrastRatio(roles[fdRole], '#FFFFFF'));
          const bCr = Math.min(srgbContrastRatio(roles[fRole], '#000000'), srgbContrastRatio(roles[fdRole], '#000000'));
          bestHex = wCr >= bCr ? '#FFFFFF' : '#000000';
        }
        roles[fgRole] = bestHex;
      }
    }
  }

  return roles;
}

// ---------------------------------------------------------------------------
// CSS Generation & DOM Application Helpers
// ---------------------------------------------------------------------------

function formatProps(roles, indent = '  ', diffFrom = null) {
  const out = [];
  for (const k of ROLE_ORDER) {
    const val = roles[k];
    if (diffFrom && diffFrom[k] === val) continue;
    out.push(`${indent}--md-sys-color-${k}: ${val};`);
  }
  return out;
}

function emitSelectorBlock(lines, selector, roles, indent = '', diffFrom = null) {
  const props = formatProps(roles, `${indent}  `, diffFrom);
  if (props.length === 0) return;
  lines.push(`${indent}${selector} {`);
  lines.push(...props);
  lines.push(`${indent}}`);
}

function renderVariantBlocks(seedHex, variant, { specVersion = '2025', prefixSel = '[data-seed="custom"]', includeDefaultNoAttr = false } = {}) {
  const vSel = `${prefixSel}[data-color-variant="${variant}"]`;
  const baseSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant]), ${vSel}`
    : vSel;

  const lightStd = generateScheme(seedHex, { variant, isDark: false, contrastLevel: 0.0, specVersion });
  const darkStd = generateScheme(seedHex, { variant, isDark: true, contrastLevel: 0.0, specVersion });
  const lightMed = generateScheme(seedHex, { variant, isDark: false, contrastLevel: 0.5, specVersion });
  const darkMed = generateScheme(seedHex, { variant, isDark: true, contrastLevel: 0.5, specVersion });
  const lightHi = generateScheme(seedHex, { variant, isDark: false, contrastLevel: 1.0, specVersion });
  const darkHi = generateScheme(seedHex, { variant, isDark: true, contrastLevel: 1.0, specVersion });

  const lines = [`/* Variant: ${variant} (seed ${normalizeHex(seedHex)}, spec ${specVersion}) */`];
  emitSelectorBlock(lines, baseSels, lightStd);

  lines.push('@media (prefers-color-scheme: dark) {');
  const sysSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant]):where(:not([data-theme="light"])), ${vSel}:where(:not([data-theme="light"]))`
    : `${vSel}:where(:not([data-theme="light"]))`;
  emitSelectorBlock(lines, sysSels, darkStd, '  ');
  lines.push('}');

  const expSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-theme="dark"], ${vSel}[data-theme="dark"]`
    : `${vSel}[data-theme="dark"]`;
  emitSelectorBlock(lines, expSels, darkStd);

  const medLSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-contrast="medium"]:not([data-theme="dark"]), ${vSel}[data-contrast="medium"]:not([data-theme="dark"])`
    : `${vSel}[data-contrast="medium"]:not([data-theme="dark"])`;
  emitSelectorBlock(lines, medLSels, lightMed, '', lightStd);

  lines.push('@media (prefers-color-scheme: dark) {');
  const medSysSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-contrast="medium"]:not([data-theme="light"]), ${vSel}[data-contrast="medium"]:not([data-theme="light"])`
    : `${vSel}[data-contrast="medium"]:not([data-theme="light"])`;
  emitSelectorBlock(lines, medSysSels, darkMed, '  ', darkStd);
  lines.push('}');

  const medExpSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-theme="dark"][data-contrast="medium"], ${vSel}[data-theme="dark"][data-contrast="medium"]`
    : `${vSel}[data-theme="dark"][data-contrast="medium"]`;
  emitSelectorBlock(lines, medExpSels, darkMed, '', darkStd);

  const hiLSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-contrast="high"]:not([data-theme="dark"]), ${vSel}[data-contrast="high"]:not([data-theme="dark"])`
    : `${vSel}[data-contrast="high"]:not([data-theme="dark"])`;
  emitSelectorBlock(lines, hiLSels, lightHi, '', lightStd);

  lines.push('@media (prefers-color-scheme: dark) {');
  const hiSysSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-contrast="high"]:not([data-theme="light"]), ${vSel}[data-contrast="high"]:not([data-theme="light"])`
    : `${vSel}[data-contrast="high"]:not([data-theme="light"])`;
  emitSelectorBlock(lines, hiSysSels, darkHi, '  ', darkStd);
  lines.push('}');

  const hiExpSels = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-theme="dark"][data-contrast="high"], ${vSel}[data-theme="dark"][data-contrast="high"]`
    : `${vSel}[data-theme="dark"][data-contrast="high"]`;
  emitSelectorBlock(lines, hiExpSels, darkHi, '', darkStd);

  lines.push('@media (prefers-contrast: more) {');
  const osHiL = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant]):where(:not([data-theme="dark"]):not([data-contrast="medium"])), ${vSel}:where(:not([data-theme="dark"]):not([data-contrast="medium"]))`
    : `${vSel}:where(:not([data-theme="dark"]):not([data-contrast="medium"]))`;
  emitSelectorBlock(lines, osHiL, lightHi, '  ', lightStd);
  lines.push('  @media (prefers-color-scheme: dark) {');
  const osHiSd = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant]):where(:not([data-theme="light"]):not([data-contrast="medium"])), ${vSel}:where(:not([data-theme="light"]):not([data-contrast="medium"]))`
    : `${vSel}:where(:not([data-theme="light"]):not([data-contrast="medium"]))`;
  emitSelectorBlock(lines, osHiSd, darkHi, '    ', darkStd);
  lines.push('  }');
  const osHiEd = includeDefaultNoAttr
    ? `${prefixSel}:not([data-color-variant])[data-theme="dark"]:where(:not([data-contrast="medium"])), ${vSel}[data-theme="dark"]:where(:not([data-contrast="medium"]))`
    : `${vSel}[data-theme="dark"]:where(:not([data-contrast="medium"]))`;
  emitSelectorBlock(lines, osHiEd, darkHi, '  ', darkStd);
  lines.push('}');
  lines.push('');
  return lines;
}

export function renderCustomSeedCss(seedHex, { specVersion = '2025', seedName = 'custom' } = {}) {
  const norm = normalizeHex(seedHex);
  const lines = [`/* Dynamic seed ${norm} for [data-seed="${seedName}"] (SPEC_${specVersion}) */`, ''];
  UI_VARIANTS.forEach((variant, idx) => {
    lines.push(
      ...renderVariantBlocks(norm, variant, {
        specVersion,
        prefixSel: `[data-seed="${seedName}"]`,
        includeDefaultNoAttr: idx === 0,
      }),
    );
  });
  return lines.join('\n');
}

export function renderStandaloneCss(seedHex, { variant = 'expressive', specVersion = '2025' } = {}) {
  const norm = normalizeHex(seedHex);
  const lightStd = generateScheme(norm, { variant, isDark: false, contrastLevel: 0.0, specVersion });
  const darkStd = generateScheme(norm, { variant, isDark: true, contrastLevel: 0.0, specVersion });
  const lightMed = generateScheme(norm, { variant, isDark: false, contrastLevel: 0.5, specVersion });
  const darkMed = generateScheme(norm, { variant, isDark: true, contrastLevel: 0.5, specVersion });
  const lightHi = generateScheme(norm, { variant, isDark: false, contrastLevel: 1.0, specVersion });
  const darkHi = generateScheme(norm, { variant, isDark: true, contrastLevel: 1.0, specVersion });

  const lines = [
    '/* ============================================================================',
    ` * Custom MD3E Colour Scheme — Seed ${norm} | Variant ${variant} | Spec ${specVersion}`,
    ' * Generated by md3e-dynamic-color.js (MCU QuantizerCelebi + Score + HCT)',
    ' * Import AFTER md3e-tokens.css so all system roles reflect your brand seed.',
    ' * ========================================================================== */',
    '',
  ];
  emitSelectorBlock(lines, ':root', lightStd);
  lines.push('');
  lines.push('@media (prefers-color-scheme: dark) {');
  emitSelectorBlock(lines, ':root:where(:not([data-theme="light"]))', darkStd, '  ');
  lines.push('}');
  lines.push('');
  emitSelectorBlock(lines, '[data-theme="dark"]', darkStd);
  lines.push('');
  emitSelectorBlock(lines, '[data-contrast="medium"]:not([data-theme="dark"])', lightMed, '', lightStd);
  lines.push('@media (prefers-color-scheme: dark) {');
  emitSelectorBlock(lines, '[data-contrast="medium"]:not([data-theme="light"])', darkMed, '  ', darkStd);
  lines.push('}');
  emitSelectorBlock(lines, '[data-theme="dark"][data-contrast="medium"]', darkMed, '', darkStd);
  lines.push('');
  emitSelectorBlock(lines, '[data-contrast="high"]:not([data-theme="dark"])', lightHi, '', lightStd);
  lines.push('@media (prefers-color-scheme: dark) {');
  emitSelectorBlock(lines, '[data-contrast="high"]:not([data-theme="light"])', darkHi, '  ', darkStd);
  lines.push('}');
  emitSelectorBlock(lines, '[data-theme="dark"][data-contrast="high"]', darkHi, '', darkStd);
  lines.push('@media (prefers-contrast: more) {');
  emitSelectorBlock(lines, ':is(:root, [data-theme="light"]):where(:not([data-theme="dark"]):not([data-contrast="medium"]))', lightHi, '  ', lightStd);
  lines.push('  @media (prefers-color-scheme: dark) {');
  emitSelectorBlock(lines, ':root:where(:not([data-theme="light"]):not([data-contrast="medium"]))', darkHi, '    ', darkStd);
  lines.push('  }');
  emitSelectorBlock(lines, '[data-theme="dark"]:where(:not([data-contrast="medium"]))', darkHi, '  ', darkStd);
  lines.push('}');
  lines.push('');
  return lines.join('\n');
}

export function applyDynamicSeed(
  seedHex,
  {
    root = typeof document !== 'undefined' ? document.documentElement : null,
    specVersion = '2025',
    styleId = 'md3e-dynamic-seed-styles',
    seedName = 'custom',
  } = {},
) {
  const norm = normalizeHex(seedHex);
  const css = renderCustomSeedCss(norm, { specVersion, seedName });
  if (typeof document !== 'undefined' && root) {
    let styleEl = document.getElementById(styleId);
    if (!styleEl) {
      styleEl = document.createElement('style');
      styleEl.id = styleId;
      document.head.appendChild(styleEl);
    }
    styleEl.textContent = css;
    root.dataset.seed = seedName;
    root.dataset.customSeed = norm;
  }
  return { seedHex: norm, css };
}

export function clearDynamicSeed({
  root = typeof document !== 'undefined' ? document.documentElement : null,
  styleId = 'md3e-dynamic-seed-styles',
} = {}) {
  if (typeof document !== 'undefined') {
    const styleEl = document.getElementById(styleId);
    if (styleEl) styleEl.remove();
  }
  if (root) {
    delete root.dataset.customSeed;
    if (root.dataset.seed === 'custom') {
      delete root.dataset.seed;
    }
  }
}
