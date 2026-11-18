/**
 * md3e-morph.js — Real-time MD3E Shape Morphing Engine
 *
 * Zero-dependency ES module porting AOSP `androidx.graphics.shapes`
 * (`RoundedPolygon`, `RoundedCorner`, `Cubic`, `Morph` + `DoubleMapper`) and all
 * 35 official `androidx.compose.material3.MaterialShapes` presets.
 *
 * Drives seamless frame-by-frame SVG `<path d="...">` morphing via
 * `requestAnimationFrame` + `assets/tokens/md3e-spring.js` with full velocity
 * continuity on mid-flight interruption and `prefers-reduced-motion` safety.
 */

import { createSpringAnimator, resolveSpringPreset } from './md3e-spring.js';

const DISTANCE_EPSILON = 1e-4;
const PROGRESS_EPSILON = 1e-5;

export const SHAPE_NAMES = Object.freeze([
  'circle',
  'square',
  'slanted',
  'arch',
  'fan',
  'arrow',
  'semi-circle',
  'oval',
  'pill',
  'triangle',
  'diamond',
  'clam-shell',
  'pentagon',
  'gem',
  'sunny',
  'very-sunny',
  'cookie-4-sided',
  'cookie-6-sided',
  'cookie-7-sided',
  'cookie-9-sided',
  'cookie-12-sided',
  'ghostish',
  'clover-4-leaf',
  'clover-8-leaf',
  'burst',
  'soft-burst',
  'boom',
  'soft-boom',
  'flower',
  'puffy',
  'puffy-diamond',
  'pixel-circle',
  'pixel-triangle',
  'bun',
  'heart',
]);

// Official LoadingIndicatorDefaults.IndeterminateIndicatorPolygons (LoadingIndicator.kt)
export const LOADING_SEQUENCE = Object.freeze([
  'soft-burst',
  'cookie-9-sided',
  'pentagon',
  'pill',
  'sunny',
  'cookie-4-sided',
  'oval',
]);

function clamp(lo, hi, v) {
  return v < lo ? lo : v > hi ? hi : v;
}

function lerp(a, b, t) {
  return (1 - t) * a + t * b;
}

function vAdd(a, b) {
  return [a[0] + b[0], a[1] + b[1]];
}

function vSub(a, b) {
  return [a[0] - b[0], a[1] - b[1]];
}

function vMul(a, s) {
  return [a[0] * s, a[1] * s];
}

function vDot(a, b) {
  return a[0] * b[0] + a[1] * b[1];
}

function vLen(a) {
  return Math.hypot(a[0], a[1]);
}

function vRot90(a) {
  return [-a[1], a[0]];
}

function vDir(x, y) {
  const d = Math.hypot(x, y);
  return d <= 1e-9 ? [1, 0] : [x / d, y / d];
}

export class CornerRounding {
  constructor(radius = 0, smoothing = 0) {
    this.radius = radius;
    this.smoothing = smoothing;
  }
}

export const UNROUNDED = Object.freeze(new CornerRounding(0, 0));

export class Cubic {
  constructor(points) {
    this.p = points instanceof Float64Array ? points : Float64Array.from(points);
  }

  get a0x() { return this.p[0]; }
  get a0y() { return this.p[1]; }
  get c0x() { return this.p[2]; }
  get c0y() { return this.p[3]; }
  get c1x() { return this.p[4]; }
  get c1y() { return this.p[5]; }
  get a1x() { return this.p[6]; }
  get a1y() { return this.p[7]; }

  zeroLength() {
    return (
      Math.abs(this.a0x - this.a1x) < DISTANCE_EPSILON
      && Math.abs(this.a0y - this.a1y) < DISTANCE_EPSILON
    );
  }

  pointOnCurve(t) {
    const u = 1 - t;
    const u3 = u * u * u;
    const t3 = t * t * t;
    const c0 = 3 * t * u * u;
    const c1 = 3 * t * t * u;
    return [
      this.a0x * u3 + this.c0x * c0 + this.c1x * c1 + this.a1x * t3,
      this.a0y * u3 + this.c0y * c0 + this.c1y * c1 + this.a1y * t3,
    ];
  }

  approxLength(steps = 8) {
    let len = 0;
    let prevX = this.a0x;
    let prevY = this.a0y;
    for (let s = 1; s <= steps; s++) {
      const [nx, ny] = this.pointOnCurve(s / steps);
      len += Math.hypot(nx - prevX, ny - prevY);
      prevX = nx;
      prevY = ny;
    }
    return len;
  }

  split(t) {
    const clampedT = clamp(0, 1, t);
    const u = 1 - clampedT;
    const [mx, my] = this.pointOnCurve(clampedT);
    const left = new Cubic([
      this.a0x, this.a0y,
      this.a0x * u + this.c0x * clampedT,
      this.a0y * u + this.c0y * clampedT,
      this.a0x * u * u + this.c0x * 2 * u * clampedT + this.c1x * clampedT * clampedT,
      this.a0y * u * u + this.c0y * 2 * u * clampedT + this.c1y * clampedT * clampedT,
      mx, my,
    ]);
    const right = new Cubic([
      mx, my,
      this.c0x * u * u + this.c1x * 2 * u * clampedT + this.a1x * clampedT * clampedT,
      this.c0y * u * u + this.c1y * 2 * u * clampedT + this.a1y * clampedT * clampedT,
      this.c1x * u + this.a1x * clampedT,
      this.c1y * u + this.a1y * clampedT,
      this.a1x, this.a1y,
    ]);
    return [left, right];
  }

  reverse() {
    return new Cubic([
      this.a1x, this.a1y,
      this.c1x, this.c1y,
      this.c0x, this.c0y,
      this.a0x, this.a0y,
    ]);
  }

  transformed(fn) {
    const [x0, y0] = fn(this.a0x, this.a0y);
    const [x1, y1] = fn(this.c0x, this.c0y);
    const [x2, y2] = fn(this.c1x, this.c1y);
    const [x3, y3] = fn(this.a1x, this.a1y);
    return new Cubic([x0, y0, x1, y1, x2, y2, x3, y3]);
  }

  static straightLine(x0, y0, x1, y1) {
    return new Cubic([
      x0, y0,
      lerp(x0, x1, 1 / 3), lerp(y0, y1, 1 / 3),
      lerp(x0, x1, 2 / 3), lerp(y0, y1, 2 / 3),
      x1, y1,
    ]);
  }

  static circularArc(cx, cy, x0, y0, x1, y1) {
    const p0d = vDir(x0 - cx, y0 - cy);
    const p1d = vDir(x1 - cx, y1 - cy);
    const rotP0 = vRot90(p0d);
    const rotP1 = vRot90(p1d);
    const clockwise = vDot(rotP0, [x1 - cx, y1 - cy]) >= 0;
    const cosa = clamp(-1, 1, vDot(p0d, p1d));
    if (cosa > 0.999 || Math.abs(1 - cosa) < 1e-7) {
      return Cubic.straightLine(x0, y0, x1, y1);
    }
    const r = Math.hypot(x0 - cx, y0 - cy);
    const k = (
      r * (4 / 3)
      * (Math.sqrt(Math.max(0, 2 * (1 - cosa))) - Math.sqrt(Math.max(0, 1 - cosa * cosa)))
      / (1 - cosa)
      * (clockwise ? 1 : -1)
    );
    return new Cubic([
      x0, y0,
      x0 + rotP0[0] * k, y0 + rotP0[1] * k,
      x1 - rotP1[0] * k, y1 - rotP1[1] * k,
      x1, y1,
    ]);
  }

  static interpolate(c0, c1, progress) {
    const out = new Float64Array(8);
    const p0 = c0.p;
    const p1 = c1.p;
    for (let i = 0; i < 8; i++) {
      out[i] = lerp(p0[i], p1[i], progress);
    }
    return new Cubic(out);
  }
}

function lineIntersection(p0, d0, p1, d1) {
  const rotD1 = vRot90(d1);
  const den = vDot(d0, rotD1);
  if (Math.abs(den) < DISTANCE_EPSILON) return null;
  const num = vDot(vSub(p1, p0), rotD1);
  if (Math.abs(den) < DISTANCE_EPSILON * Math.abs(num)) return null;
  return vAdd(p0, vMul(d0, num / den));
}

class RoundedCorner {
  constructor(p0, p1, p2, rounding) {
    this.p0 = p0;
    this.p1 = p1;
    this.p2 = p2;
    const v01 = vSub(p0, p1);
    const v21 = vSub(p2, p1);
    const d01 = vLen(v01);
    const d21 = vLen(v21);
    if (d01 > 0 && d21 > 0) {
      this.d1 = [v01[0] / d01, v01[1] / d01];
      this.d2 = [v21[0] / d21, v21[1] / d21];
      this.cornerRadius = rounding ? rounding.radius : 0;
      this.smoothing = rounding ? rounding.smoothing : 0;
      this.cosAngle = clamp(-1, 1, vDot(this.d1, this.d2));
      this.sinAngle = Math.sqrt(Math.max(0, 1 - this.cosAngle * this.cosAngle));
      this.expectedRoundCut = this.sinAngle > 1e-3
        ? this.cornerRadius * (this.cosAngle + 1) / this.sinAngle
        : 0;
    } else {
      this.d1 = [0, 0];
      this.d2 = [0, 0];
      this.cornerRadius = 0;
      this.smoothing = 0;
      this.cosAngle = 0;
      this.sinAngle = 0;
      this.expectedRoundCut = 0;
    }
  }

  get expectedCut() {
    return (1 + this.smoothing) * this.expectedRoundCut;
  }

  _actualSmoothing(allowedCut) {
    if (allowedCut > this.expectedCut) return this.smoothing;
    if (allowedCut > this.expectedRoundCut && (this.expectedCut - this.expectedRoundCut) > 1e-9) {
      return this.smoothing * (allowedCut - this.expectedRoundCut) / (this.expectedCut - this.expectedRoundCut);
    }
    return 0;
  }

  _computeFlankingCurve(actualRoundCut, actualSmoothing, corner, sideStart, circleInter, otherInter, center, actualR) {
    const sideDir = vDir(sideStart[0] - corner[0], sideStart[1] - corner[1]);
    const curveStart = vAdd(corner, vMul(sideDir, actualRoundCut * (1 + actualSmoothing)));
    const mid = [(circleInter[0] + otherInter[0]) / 2, (circleInter[1] + otherInter[1]) / 2];
    const p = [lerp(circleInter[0], mid[0], actualSmoothing), lerp(circleInter[1], mid[1], actualSmoothing)];
    const curveEnd = vAdd(center, vMul(vDir(p[0] - center[0], p[1] - center[1]), actualR));
    const tangent = vRot90(vSub(curveEnd, center));
    const anchorEnd = lineIntersection(sideStart, sideDir, curveEnd, tangent) || circleInter;
    const anchorStart = [(curveStart[0] + anchorEnd[0] * 2) / 3, (curveStart[1] + anchorEnd[1] * 2) / 3];
    return new Cubic([
      curveStart[0], curveStart[1],
      anchorStart[0], anchorStart[1],
      anchorEnd[0], anchorEnd[1],
      curveEnd[0], curveEnd[1],
    ]);
  }

  getCubics(allowedCut0, allowedCut1) {
    const allowedCut = Math.min(allowedCut0, allowedCut1);
    if (
      this.expectedRoundCut < DISTANCE_EPSILON
      || allowedCut < DISTANCE_EPSILON
      || this.cornerRadius < DISTANCE_EPSILON
    ) {
      return [Cubic.straightLine(this.p1[0], this.p1[1], this.p1[0], this.p1[1])];
    }
    const actualRoundCut = Math.min(allowedCut, this.expectedRoundCut);
    const s0 = this._actualSmoothing(allowedCut0);
    const s1 = this._actualSmoothing(allowedCut1);
    const actualR = this.cornerRadius * actualRoundCut / this.expectedRoundCut;
    const centerDist = Math.hypot(actualR, actualRoundCut);
    const bisector = [(this.d1[0] + this.d2[0]) / 2, (this.d1[1] + this.d2[1]) / 2];
    if (vLen(bisector) < 1e-6) {
      return [Cubic.straightLine(this.p1[0], this.p1[1], this.p1[0], this.p1[1])];
    }
    const center = vAdd(this.p1, vMul(vDir(bisector[0], bisector[1]), centerDist));
    const ci0 = vAdd(this.p1, vMul(this.d1, actualRoundCut));
    const ci2 = vAdd(this.p1, vMul(this.d2, actualRoundCut));
    const flank0 = this._computeFlankingCurve(actualRoundCut, s0, this.p1, this.p0, ci0, ci2, center, actualR);
    const flank2 = this._computeFlankingCurve(actualRoundCut, s1, this.p1, this.p2, ci2, ci0, center, actualR).reverse();
    const arc = Cubic.circularArc(center[0], center[1], flank0.a1x, flank0.a1y, flank2.a0x, flank2.a0y);
    return [flank0, arc, flank2];
  }
}

export class RoundedPolygon {
  constructor(cubics, cx = 0.5, cy = 0.5) {
    this.cubics = cubics;
    this.cx = cx;
    this.cy = cy;
  }

  static fromVertices(vertices, { rounding = UNROUNDED, perVertexRounding = null, cx = null, cy = null } = {}) {
    const n = vertices.length;
    if (n < 3) throw new Error('RoundedPolygon requires at least 3 vertices');

    const cornersObj = vertices.map((v, i) => new RoundedCorner(
      vertices[(i + n - 1) % n],
      v,
      vertices[(i + 1) % n],
      perVertexRounding ? perVertexRounding[i] : rounding,
    ));

    const cutAdjusts = [];
    for (let i = 0; i < n; i++) {
      const nxt = (i + 1) % n;
      const expRc = cornersObj[i].expectedRoundCut + cornersObj[nxt].expectedRoundCut;
      const expC = cornersObj[i].expectedCut + cornersObj[nxt].expectedCut;
      const side = Math.hypot(vertices[i][0] - vertices[nxt][0], vertices[i][1] - vertices[nxt][1]);
      if (expRc > side && expRc > 1e-9) {
        cutAdjusts.push([side / expRc, 0]);
      } else if (expC > side && (expC - expRc) > 1e-9) {
        cutAdjusts.push([1, (side - expRc) / (expC - expRc)]);
      } else {
        cutAdjusts.push([1, 1]);
      }
    }

    const cornerCubics = [];
    for (let i = 0; i < n; i++) {
      const allowed = [];
      for (let delta = 0; delta < 2; delta++) {
        const [rcRatio, cRatio] = cutAdjusts[(i + n - 1 + delta) % n];
        allowed.push(
          cornersObj[i].expectedRoundCut * rcRatio
          + (cornersObj[i].expectedCut - cornersObj[i].expectedRoundCut) * cRatio,
        );
      }
      cornerCubics.push(cornersObj[i].getCubics(allowed[0], allowed[1]));
    }

    const features = [];
    for (let i = 0; i < n; i++) {
      features.push(cornerCubics[i]);
      const cEnd = cornerCubics[i][cornerCubics[i].length - 1];
      const cNxt = cornerCubics[(i + 1) % n][0];
      features.push([Cubic.straightLine(cEnd.a1x, cEnd.a1y, cNxt.a0x, cNxt.a0y)]);
    }

    const out = [];
    let firstC = null;
    let lastC = null;
    let splitStart = null;
    let splitEnd = null;
    if (features.length && features[0].length === 3) {
      const [s0, s1] = features[0][1].split(0.5);
      splitStart = [features[0][0], s0];
      splitEnd = [s1, features[0][2]];
    }

    for (let idx = 0; idx <= features.length; idx++) {
      let fCubics;
      if (idx === 0 && splitEnd) {
        fCubics = splitEnd;
      } else if (idx === features.length) {
        if (splitStart) fCubics = splitStart;
        else break;
      } else {
        fCubics = features[idx];
      }

      for (const c of fCubics) {
        if (!c.zeroLength()) {
          if (lastC) out.push(lastC);
          lastC = c;
          if (!firstC) firstC = c;
        } else if (lastC) {
          const nextPts = Float64Array.from(lastC.p);
          nextPts[6] = c.a1x;
          nextPts[7] = c.a1y;
          lastC = new Cubic(nextPts);
        }
      }
    }

    if (lastC && firstC) {
      out.push(new Cubic([
        lastC.a0x, lastC.a0y, lastC.c0x, lastC.c0y,
        lastC.c1x, lastC.c1y, firstC.a0x, firstC.a0y,
      ]));
    }

    let centerX = cx;
    let centerY = cy;
    if (centerX === null || centerY === null) {
      centerX = vertices.reduce((acc, v) => acc + v[0], 0) / n;
      centerY = vertices.reduce((acc, v) => acc + v[1], 0) / n;
    }
    return new RoundedPolygon(out, centerX, centerY);
  }

  transformed(fn) {
    const [nx, ny] = fn(this.cx, this.cy);
    return new RoundedPolygon(this.cubics.map((c) => c.transformed(fn)), nx, ny);
  }

  rotatedDeg(deg, cx = 0, cy = 0) {
    const rad = (deg * Math.PI) / 180;
    const ca = Math.cos(rad);
    const sa = Math.sin(rad);
    return this.transformed((x, y) => [
      (x - cx) * ca - (y - cy) * sa + cx,
      (x - cx) * sa + (y - cy) * ca + cy,
    ]);
  }

  bounds() {
    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    const includePoint = (x, y) => {
      if (x < minX) minX = x;
      if (y < minY) minY = y;
      if (x > maxX) maxX = x;
      if (y > maxY) maxY = y;
    };
    const solveAxisExtrema = (p0, p1, p2, p3, onRoot) => {
      const a = 3 * (-p0 + 3 * p1 - 3 * p2 + p3);
      const b = 6 * (p0 - 2 * p1 + p2);
      const c = 3 * (p1 - p0);
      if (Math.abs(a) < 1e-12) {
        if (Math.abs(b) > 1e-12) {
          const t = -c / b;
          if (t > 0 && t < 1) onRoot(t);
        }
        return;
      }
      const disc = b * b - 4 * a * c;
      if (disc < 0) return;
      const sq = Math.sqrt(disc);
      const t1 = (-b + sq) / (2 * a);
      const t2 = (-b - sq) / (2 * a);
      if (t1 > 0 && t1 < 1) onRoot(t1);
      if (t2 > 0 && t2 < 1) onRoot(t2);
    };
    for (const c of this.cubics) {
      includePoint(c.a0x, c.a0y);
      includePoint(c.a1x, c.a1y);
      solveAxisExtrema(c.a0x, c.c0x, c.c1x, c.a1x, (t) => {
        const [px, py] = c.pointOnCurve(t);
        includePoint(px, py);
      });
      solveAxisExtrema(c.a0y, c.c0y, c.c1y, c.a1y, (t) => {
        const [px, py] = c.pointOnCurve(t);
        includePoint(px, py);
      });
    }
    return [minX, minY, maxX, maxY];
  }

  normalized() {
    const [minX, minY, maxX, maxY] = this.bounds();
    const w = maxX - minX;
    const h = maxY - minY;
    const side = Math.max(w, h);
    if (side <= 1e-9) return this;
    const ox = (side - w) / 2 - minX;
    const oy = (side - h) / 2 - minY;
    return this.transformed((x, y) => [(x + ox) / side, (y + oy) / side]);
  }

  static regular(numVertices, radius = 1, rounding = UNROUNDED, perVertexRounding = null) {
    const verts = [];
    for (let i = 0; i < numVertices; i++) {
      const a = (2 * Math.PI * i) / numVertices;
      verts.push([radius * Math.cos(a), radius * Math.sin(a)]);
    }
    return RoundedPolygon.fromVertices(verts, { rounding, perVertexRounding, cx: 0, cy: 0 });
  }

  static circle(numVertices = 8, radius = 1) {
    const polyR = radius / Math.cos(Math.PI / numVertices);
    return RoundedPolygon.regular(numVertices, polyR, new CornerRounding(radius));
  }

  static rectangle(width = 2, height = 2, rounding = UNROUNDED, perVertexRounding = null) {
    const hw = width / 2;
    const hh = height / 2;
    return RoundedPolygon.fromVertices(
      [[hw, hh], [-hw, hh], [-hw, -hh], [hw, -hh]],
      { rounding, perVertexRounding, cx: 0, cy: 0 },
    );
  }

  static star(numPerRadius, radius = 1, innerRadius = 0.5, rounding = UNROUNDED) {
    const verts = [];
    for (let i = 0; i < numPerRadius; i++) {
      const a0 = (Math.PI / numPerRadius) * (2 * i);
      verts.push([radius * Math.cos(a0), radius * Math.sin(a0)]);
      const a1 = (Math.PI / numPerRadius) * (2 * i + 1);
      verts.push([innerRadius * Math.cos(a1), innerRadius * Math.sin(a1)]);
    }
    return RoundedPolygon.fromVertices(verts, { rounding, cx: 0, cy: 0 });
  }
}

// ---------------------------------------------------------------------------
// All 35 Official MaterialShapes Presets (from MaterialShapes.kt)
// ---------------------------------------------------------------------------

function doRepeat(points, reps, center = [0.5, 0.5], mirroring = false) {
  const [cx, cy] = center;
  if (mirroring) {
    const angles = points.map(([[x, y]]) => (Math.atan2(y - cy, x - cx) * 180) / Math.PI);
    const dists = points.map(([[x, y]]) => Math.hypot(x - cx, y - cy));
    const actualReps = reps * 2;
    const section = 360 / actualReps;
    const out = [];
    for (let r = 0; r < actualReps; r++) {
      for (let idx = 0; idx < points.length; idx++) {
        const i = r % 2 === 0 ? idx : points.length - 1 - idx;
        if (i > 0 || r % 2 === 0) {
          const aDeg = section * r + (r % 2 === 0 ? angles[i] : section - angles[i] + 2 * angles[0]);
          const a = (aDeg * Math.PI) / 180;
          out.push([[Math.cos(a) * dists[i] + cx, Math.sin(a) * dists[i] + cy], points[i][1]]);
        }
      }
    }
    return out;
  }

  const out = [];
  const count = points.length;
  for (let k = 0; k < count * reps; k++) {
    const [pt, cr] = points[k % count];
    const ang = (Math.floor(k / count) * 2 * Math.PI) / reps;
    const ca = Math.cos(ang);
    const sa = Math.sin(ang);
    const dx = pt[0] - cx;
    const dy = pt[1] - cy;
    out.push([[dx * ca - dy * sa + cx, dx * sa + dy * ca + cy], cr]);
  }
  return out;
}

function customPolygon(points, reps, center = [0.5, 0.5], mirroring = false) {
  const rep = doRepeat(points, reps, center, mirroring);
  return RoundedPolygon.fromVertices(
    rep.map(([p]) => p),
    {
      perVertexRounding: rep.map(([, cr]) => cr),
      cx: center[0],
      cy: center[1],
    },
  );
}

const SHAPE_CACHE = new Map();

export function buildShape(name) {
  if (name instanceof RoundedPolygon) return name.normalized();
  if (SHAPE_CACHE.has(name)) return SHAPE_CACHE.get(name);

  const CR = (r, s = 0) => new CornerRounding(r, s);
  const c15 = CR(0.15);
  const c20 = CR(0.20);
  const c30 = CR(0.30);
  const c50 = CR(0.50);
  const c100 = CR(1.00);
  let poly;

  switch (name) {
    case 'circle':
      poly = RoundedPolygon.circle(10);
      break;
    case 'square':
      poly = RoundedPolygon.rectangle(1, 1, c30);
      break;
    case 'slanted':
      poly = customPolygon([[[0.926, 0.970], CR(0.189, 0.811)], [[-0.021, 0.967], CR(0.187, 0.057)]], 2);
      break;
    case 'arch':
      poly = RoundedPolygon.regular(4, 1, UNROUNDED, [c100, c100, c20, c20]).rotatedDeg(-135);
      break;
    case 'fan':
      poly = customPolygon([[[1.004, 1.000], CR(0.148, 0.417)], [[0.000, 1.000], CR(0.151)], [[0.000, -0.003], CR(0.148)], [[0.978, 0.020], CR(0.803)]], 1);
      break;
    case 'arrow':
      poly = customPolygon([[[0.500, 0.892], CR(0.313)], [[-0.216, 1.050], CR(0.207)], [[0.499, -0.160], CR(0.215, 1.000)], [[1.225, 1.060], CR(0.211)]], 1);
      break;
    case 'semi-circle':
      poly = RoundedPolygon.rectangle(1.6, 1.0, UNROUNDED, [c20, c20, c100, c100]);
      break;
    case 'oval':
      poly = RoundedPolygon.circle().transformed((x, y) => [x, y * 0.64]).rotatedDeg(-45);
      break;
    case 'pill':
      poly = customPolygon([[[0.961, 0.039], CR(0.426)], [[1.001, 0.428], UNROUNDED], [[1.000, 0.609], CR(1.000)]], 2, [0.5, 0.5], true);
      break;
    case 'triangle':
      poly = RoundedPolygon.regular(3, 1, c20).rotatedDeg(-90);
      break;
    case 'diamond':
      poly = customPolygon([[[0.500, 1.096], CR(0.151, 0.524)], [[0.040, 0.500], CR(0.159)]], 2);
      break;
    case 'clam-shell':
      poly = customPolygon([[[0.171, 0.841], CR(0.159)], [[-0.020, 0.500], CR(0.140)], [[0.170, 0.159], CR(0.159)]], 2);
      break;
    case 'pentagon':
      poly = customPolygon([[[0.500, -0.009], CR(0.172)], [[1.030, 0.365], CR(0.164)], [[0.828, 0.970], CR(0.169)]], 1, [0.5, 0.5], true);
      break;
    case 'gem':
      poly = customPolygon([[[0.499, 1.023], CR(0.241, 0.778)], [[-0.005, 0.792], CR(0.208)], [[0.073, 0.258], CR(0.228)], [[0.433, 0.000], CR(0.491)]], 1, [0.5, 0.5], true);
      break;
    case 'sunny':
      poly = RoundedPolygon.star(8, 1.0, 0.8, c15);
      break;
    case 'very-sunny':
      poly = customPolygon([[[0.500, 1.080], CR(0.085)], [[0.358, 0.843], CR(0.085)]], 8);
      break;
    case 'cookie-4-sided':
      poly = customPolygon([[[1.237, 1.236], CR(0.258)], [[0.500, 0.918], CR(0.233)]], 4);
      break;
    case 'cookie-6-sided':
      poly = customPolygon([[[0.723, 0.884], CR(0.394)], [[0.500, 1.099], CR(0.398)]], 6);
      break;
    case 'cookie-7-sided':
      poly = RoundedPolygon.star(7, 1.0, 0.75, c50).rotatedDeg(-90);
      break;
    case 'cookie-9-sided':
      poly = RoundedPolygon.star(9, 1.0, 0.8, c50).rotatedDeg(-90);
      break;
    case 'cookie-12-sided':
      poly = RoundedPolygon.star(12, 1.0, 0.8, c50).rotatedDeg(-90);
      break;
    case 'ghostish':
      poly = customPolygon([[[0.500, 0.0], CR(1.0)], [[1.0, 0.0], CR(1.0)], [[1.0, 1.140], CR(0.254, 0.106)], [[0.575, 0.906], CR(0.253)]], 1, [0.5, 0.5], true);
      break;
    case 'clover-4-leaf':
      poly = customPolygon([[[0.500, 0.074], UNROUNDED], [[0.725, -0.099], CR(0.476)]], 4, [0.5, 0.5], true);
      break;
    case 'clover-8-leaf':
      poly = customPolygon([[[0.500, 0.036], UNROUNDED], [[0.758, -0.101], CR(0.209)]], 8);
      break;
    case 'burst':
      poly = customPolygon([[[0.500, -0.006], CR(0.006)], [[0.592, 0.158], CR(0.006)]], 12);
      break;
    case 'soft-burst':
      poly = customPolygon([[[0.193, 0.277], CR(0.053)], [[0.176, 0.055], CR(0.053)]], 10);
      break;
    case 'boom':
      poly = customPolygon([[[0.457, 0.296], CR(0.007)], [[0.500, -0.051], CR(0.007)]], 15);
      break;
    case 'soft-boom':
      poly = customPolygon([[[0.733, 0.454], UNROUNDED], [[0.839, 0.437], CR(0.532)], [[0.949, 0.449], CR(0.439, 1.000)], [[0.998, 0.478], CR(0.174)]], 16, [0.5, 0.5], true);
      break;
    case 'flower':
      poly = customPolygon([[[0.370, 0.187], UNROUNDED], [[0.416, 0.049], CR(0.381)], [[0.479, 0.001], CR(0.095)]], 8, [0.5, 0.5], true);
      break;
    case 'puffy':
      poly = customPolygon([
        [[0.500, 0.053], UNROUNDED], [[0.545, -0.040], CR(0.405)], [[0.670, -0.035], CR(0.426)],
        [[0.717, 0.066], CR(0.574)], [[0.722, 0.128], UNROUNDED], [[0.777, 0.002], CR(0.360)],
        [[0.914, 0.149], CR(0.660)], [[0.926, 0.289], CR(0.660)], [[0.881, 0.346], UNROUNDED],
        [[0.940, 0.344], CR(0.126)], [[1.003, 0.437], CR(0.255)],
      ], 2, [0.5, 0.5], true).transformed((x, y) => [x, y * 0.742]);
      break;
    case 'puffy-diamond':
      poly = customPolygon([[[0.870, 0.130], CR(0.146)], [[0.818, 0.357], UNROUNDED], [[1.000, 0.332], CR(0.853)]], 4, [0.5, 0.5], true);
      break;
    case 'pixel-circle':
      poly = customPolygon([
        [[0.500, 0.000], UNROUNDED], [[0.704, 0.000], UNROUNDED], [[0.704, 0.065], UNROUNDED],
        [[0.843, 0.065], UNROUNDED], [[0.843, 0.148], UNROUNDED], [[0.926, 0.148], UNROUNDED],
        [[0.926, 0.296], UNROUNDED], [[1.000, 0.296], UNROUNDED],
      ], 2, [0.5, 0.5], true);
      break;
    case 'pixel-triangle':
      poly = customPolygon([
        [[0.110, 0.500], UNROUNDED], [[0.113, 0.000], UNROUNDED], [[0.287, 0.000], UNROUNDED],
        [[0.287, 0.087], UNROUNDED], [[0.421, 0.087], UNROUNDED], [[0.421, 0.170], UNROUNDED],
        [[0.560, 0.170], UNROUNDED], [[0.560, 0.265], UNROUNDED], [[0.674, 0.265], UNROUNDED],
        [[0.675, 0.344], UNROUNDED], [[0.789, 0.344], UNROUNDED], [[0.789, 0.439], UNROUNDED],
        [[0.888, 0.439], UNROUNDED],
      ], 1, [0.5, 0.5], true);
      break;
    case 'bun':
      poly = customPolygon([[[0.796, 0.500], UNROUNDED], [[0.853, 0.518], c100], [[0.992, 0.631], c100], [[0.968, 1.000], c100]], 2, [0.5, 0.5], true);
      break;
    case 'heart':
      poly = customPolygon([[[0.500, 0.268], CR(0.016)], [[0.792, -0.066], CR(0.958)], [[1.064, 0.276], c100], [[0.501, 0.946], CR(0.129)]], 1, [0.5, 0.5], true);
      break;
    default:
      throw new Error(`Unknown MaterialShape: ${name}`);
  }

  const normalized = poly.normalized();
  SHAPE_CACHE.set(name, normalized);
  return normalized;
}

export const MATERIAL_SHAPES = Object.freeze(
  SHAPE_NAMES.reduce((acc, name) => {
    Object.defineProperty(acc, name, {
      enumerable: true,
      get: () => buildShape(name),
    });
    return acc;
  }, {}),
);

// ---------------------------------------------------------------------------
// Morph: Measured Clockwise Ring Alignment + Control-Point Cubic Subdivision
// ---------------------------------------------------------------------------

function ensureClockwiseAlignedTop(poly) {
  let cubics = poly.cubics.filter((c) => !c.zeroLength());
  if (!cubics.length) {
    return [Cubic.straightLine(0.5, 0.5, 0.5, 0.5)];
  }

  // Compute signed area in screen space (+y down); positive = clockwise.
  const pts = [];
  for (const c of cubics) {
    for (let s = 0; s < 6; s++) pts.push(c.pointOnCurve(s / 6));
  }
  let area2 = 0;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i];
    const b = pts[(i + 1) % pts.length];
    area2 += a[0] * b[1] - b[0] * a[1];
  }
  if (area2 < 0) {
    cubics = cubics.slice().reverse().map((c) => c.reverse());
  }

  // Rotate and split at the perimeter point closest to 12 o'clock (-pi/2)
  // so every shape pair aligns upright with zero angular twist.
  let bestIdx = 0;
  let bestT = 0;
  let bestScore = Infinity;
  for (let i = 0; i < cubics.length; i++) {
    const c = cubics[i];
    for (let s = 0; s < 8; s++) {
      const t = s / 8;
      const [px, py] = c.pointOnCurve(t);
      const ang = Math.atan2(py - 0.5, px - 0.5);
      const diff = Math.abs((((ang + Math.PI / 2) + 3 * Math.PI) % (2 * Math.PI)) - Math.PI);
      if (diff < bestScore) {
        bestScore = diff;
        bestIdx = i;
        bestT = t;
      }
    }
  }

  if (bestT > 0.02 && bestT < 0.98) {
    const [left, right] = cubics[bestIdx].split(bestT);
    const reordered = [];
    if (!right.zeroLength()) reordered.push(right);
    for (let k = 1; k < cubics.length; k++) {
      reordered.push(cubics[(bestIdx + k) % cubics.length]);
    }
    if (!left.zeroLength()) reordered.push(left);
    return reordered;
  }

  const startOffset = bestT >= 0.98 ? (bestIdx + 1) % cubics.length : bestIdx;
  if (startOffset === 0) return cubics;
  return [...cubics.slice(startOffset), ...cubics.slice(0, startOffset)];
}

function measureCubics(cubics) {
  const lengths = cubics.map((c) => Math.max(1e-6, c.approxLength(8)));
  const total = lengths.reduce((a, b) => a + b, 0) || 1;
  let acc = 0;
  return cubics.map((cubic, i) => {
    const start = acc / total;
    acc += lengths[i];
    const end = i === cubics.length - 1 ? 1 : acc / total;
    return { cubic, start, end };
  });
}

function splitMeasured(segment, cutProgress) {
  const span = segment.end - segment.start;
  const localT = span > 1e-9 ? clamp(0, 1, (cutProgress - segment.start) / span) : 0.5;
  const [c0, c1] = segment.cubic.split(localT);
  return [
    { cubic: c0, start: segment.start, end: cutProgress },
    { cubic: c1, start: cutProgress, end: segment.end },
  ];
}

export class DoubleMapper {
  constructor(pairs = [[0, 0], [1, 1]]) {
    const sorted = pairs.slice().sort((a, b) => a[0] - b[0]);
    this.xs = sorted.map((p) => p[0]);
    this.ys = sorted.map((p) => p[1]);
  }

  static _interp(src, dst, v) {
    if (v <= src[0]) return dst[0];
    const last = src.length - 1;
    if (v >= src[last]) return dst[last];
    for (let i = 0; i < last; i++) {
      if (v <= src[i + 1]) {
        const d = src[i + 1] - src[i];
        const t = d > 1e-9 ? (v - src[i]) / d : 0;
        return lerp(dst[i], dst[i + 1], t);
      }
    }
    return dst[last];
  }

  map(x) {
    return DoubleMapper._interp(this.xs, this.ys, x);
  }

  mapBack(y) {
    return DoubleMapper._interp(this.ys, this.xs, y);
  }
}

export class Morph {
  constructor(start, end) {
    this.startPolygon = start instanceof RoundedPolygon ? start.normalized() : buildShape(start);
    this.endPolygon = end instanceof RoundedPolygon ? end.normalized() : buildShape(end);

    const measured1 = measureCubics(ensureClockwiseAlignedTop(this.startPolygon));
    const measured2 = measureCubics(ensureClockwiseAlignedTop(this.endPolygon));

    this.mapper = new DoubleMapper([[0, 0], [1, 1]]);
    this.morphMatch = Morph._match(measured1, measured2, this.mapper);
  }

  static _match(m1, m2, mapper) {
    const matched = [];
    let i1 = 0;
    let i2 = 0;
    let seg1 = i1 < m1.length ? m1[i1++] : null;
    let seg2 = i2 < m2.length ? m2[i2++] : null;

    while (seg1 && seg2) {
      const b1 = i1 === m1.length ? 1 : seg1.end;
      const b2 = mapper.mapBack(i2 === m2.length ? 1 : seg2.end);
      const cut1 = Math.min(b1, b2);
      const cut2 = mapper.map(cut1);

      let emit1;
      if (seg1.end > cut1 + PROGRESS_EPSILON) {
        const [left, right] = splitMeasured(seg1, cut1);
        emit1 = left.cubic;
        seg1 = right;
      } else {
        emit1 = seg1.cubic;
        seg1 = i1 < m1.length ? m1[i1++] : null;
      }

      let emit2;
      if (seg2.end > cut2 + PROGRESS_EPSILON) {
        const [left, right] = splitMeasured(seg2, cut2);
        emit2 = left.cubic;
        seg2 = right;
      } else {
        emit2 = seg2.cubic;
        seg2 = i2 < m2.length ? m2[i2++] : null;
      }

      matched.push([emit1, emit2]);
    }

    return matched;
  }

  asCubics(progress) {
    return this.morphMatch.map(([c1, c2]) => Cubic.interpolate(c1, c2, progress));
  }

  toPolygon(progress) {
    return new RoundedPolygon(
      this.asCubics(progress),
      lerp(this.startPolygon.cx, this.endPolygon.cx, progress),
      lerp(this.startPolygon.cy, this.endPolygon.cy, progress),
    );
  }

  toSvgPath(progress, options) {
    return cubicsToSvgPath(this.asCubics(progress), options);
  }
}

export function cubicsToSvgPath(cubics, { size = 100, scale = 1, precision = 2 } = {}) {
  if (!cubics || !cubics.length) return '';
  const half = size / 2;
  const factor = size * scale;
  const mul = 10 ** precision;
  const fmt = (v) => {
    const num = Math.round(((v - 0.5) * factor + half) * mul) / mul;
    return num === 0 ? '0' : String(num);
  };

  let d = `M${fmt(cubics[0].a0x)} ${fmt(cubics[0].a0y)}`;
  for (let i = 0; i < cubics.length; i++) {
    const c = cubics[i];
    d += `C${fmt(c.c0x)} ${fmt(c.c0y)} ${fmt(c.c1x)} ${fmt(c.c1y)} ${fmt(c.a1x)} ${fmt(c.a1y)}`;
  }
  return `${d}Z`;
}

export function polygonToSvgPath(shape, options) {
  const poly = shape instanceof RoundedPolygon ? shape.normalized() : buildShape(shape);
  return cubicsToSvgPath(poly.cubics, options);
}

export function morphToSvgPath(startShape, endShape, progress, options) {
  return new Morph(startShape, endShape).toSvgPath(progress, options);
}

/**
 * Interactive SVG `<path>` morph controller driven by `md3e-spring.js` + `requestAnimationFrame`.
 */
export function createShapeMorpher(
  pathElement,
  {
    initialShape = 'square',
    spring = 'fast-spatial',
    stiffness = null,
    damping = null,
    size = 100,
    scale = 1,
    precision = 2,
    onProgress = null,
  } = {},
) {
  if (!pathElement || typeof pathElement.setAttribute !== 'function') {
    throw new Error('createShapeMorpher requires a valid SVGPathElement or setAttribute-compatible target');
  }

  let currentProgress = 0;
  let startPoly = buildShape(initialShape);
  let targetPoly = startPoly;
  let activeMorph = new Morph(startPoly, targetPoly);

  const preset = resolveSpringPreset(
    spring.replace(/-(?:spatial|effects)$/, ''),
    spring.endsWith('-effects') ? 'effects' : 'spatial',
  );
  const k = stiffness ?? preset.stiffness;
  const z = damping ?? preset.damping;

  const render = (p) => {
    currentProgress = p;
    const d = activeMorph.toSvgPath(p, { size, scale, precision });
    pathElement.setAttribute('d', d);
    onProgress?.(p, d);
  };

  const animator = createSpringAnimator({
    initialValue: 0,
    stiffness: k,
    damping: z,
    precision: 0.002,
    onUpdate: render,
  });

  let activeSequenceCleanup = null;
  const bindCleanups = new Set();

  // Render initial rest path immediately
  render(0);

  function configure(opts = {}) {
    animator.configure(opts);
  }

  function morphTo(nextShape, { immediate = false, velocity = null } = {}) {
    const nextPoly = nextShape instanceof RoundedPolygon ? nextShape.normalized() : buildShape(nextShape);
    if (!immediate && !animator.isAnimating() && (
      (nextPoly === startPoly && (startPoly === targetPoly || (animator.target === 0 && currentProgress <= 0.001)))
      || (nextPoly === targetPoly && animator.target === 1 && currentProgress >= 0.999)
    )) {
      return;
    }
    const snapNow = immediate
      || (typeof window !== 'undefined' && Boolean(window.matchMedia?.('(prefers-reduced-motion: reduce)').matches));

    if (snapNow) {
      startPoly = nextPoly;
      targetPoly = nextPoly;
      activeMorph = new Morph(startPoly, targetPoly);
      animator.snap(1);
      return;
    }

    // If toggling cleanly back toward startPolygon, reverse target directly (0 <-> 1)
    if (nextPoly === startPoly && startPoly !== targetPoly) {
      const preservedVel = velocity ?? animator.velocity;
      animator.setTarget(0, { velocity: preservedVel });
      return;
    }
    if (nextPoly === targetPoly && startPoly !== targetPoly) {
      const preservedVel = velocity ?? animator.velocity;
      animator.setTarget(1, { velocity: preservedVel });
      return;
    }

    // Mid-flight retargeting: freeze current interpolated polygon cleanly as new start!
    const frozenPoly = currentProgress <= 0.001
      ? startPoly
      : currentProgress >= 0.999
        ? targetPoly
        : activeMorph.toPolygon(currentProgress);
    const preservedVel = velocity ?? (animator.velocity * 0.35);
    startPoly = frozenPoly;
    targetPoly = nextPoly;
    activeMorph = new Morph(startPoly, targetPoly);
    animator.snap(0);
    animator.setTarget(1, preservedVel);
  }

  return {
    get animator() { return animator; },
    get morph() { return activeMorph; },
    configure,
    morphTo,
    bindPressMorph(
      controlEl,
      { restShape = initialShape, pressedShape = 'cookie-9-sided', toggleShape = null, clickFlashMs = 260 } = {},
    ) {
      if (!controlEl) return () => {};
      let isPressed = false;
      let handledByPointer = false;
      let isToggled = controlEl.getAttribute?.('aria-pressed') === 'true';
      let flashTimer = null;
      const effectiveRest = () => (isToggled && toggleShape ? toggleShape : restShape);

      const onDown = (e) => {
        if (e?.button !== undefined && e.button !== 0) return;
        clearTimeout(flashTimer);
        isPressed = true;
        handledByPointer = true;
        morphTo(pressedShape);
      };
      const release = (flipToggle) => {
        if (flipToggle && toggleShape) {
          isToggled = !isToggled;
          controlEl.setAttribute?.('aria-pressed', String(isToggled));
        }
        morphTo(effectiveRest());
      };
      const onUp = () => {
        if (!isPressed) return;
        isPressed = false;
        release(true);
      };
      const onCancel = () => {
        if (!isPressed) return;
        isPressed = false;
        handledByPointer = false;
        release(false);
      };
      const onClick = () => {
        if (handledByPointer) {
          handledByPointer = false;
          return;
        }
        clearTimeout(flashTimer);
        if (toggleShape) {
          isToggled = !isToggled;
          controlEl.setAttribute?.('aria-pressed', String(isToggled));
          morphTo(effectiveRest());
        } else {
          morphTo(pressedShape);
          flashTimer = setTimeout(() => morphTo(effectiveRest()), clickFlashMs);
        }
      };

      controlEl.addEventListener('pointerdown', onDown);
      controlEl.addEventListener('pointerup', onUp);
      controlEl.addEventListener('pointercancel', onCancel);
      controlEl.addEventListener('pointerleave', onCancel);
      controlEl.addEventListener('click', onClick);
      const unbind = () => {
        clearTimeout(flashTimer);
        controlEl.removeEventListener('pointerdown', onDown);
        controlEl.removeEventListener('pointerup', onUp);
        controlEl.removeEventListener('pointercancel', onCancel);
        controlEl.removeEventListener('pointerleave', onCancel);
        controlEl.removeEventListener('click', onClick);
        bindCleanups.delete(unbind);
      };
      bindCleanups.add(unbind);
      return unbind;
    },
    startSequence(
      sequence = LOADING_SEQUENCE,
      { intervalMs = 650, stiffness = 200, damping = 0.6 } = {},
    ) {
      activeSequenceCleanup?.();
      let stepIdx = 0;
      let timerId = null;
      animator.configure({ stiffness, damping });
      morphTo(sequence[0], { immediate: true });
      const advance = () => {
        // Pause sequence advancement ONLY when tab is hidden; never stall in foreground.
        if (typeof document !== 'undefined' && document.hidden === true) return;
        stepIdx = (stepIdx + 1) % sequence.length;
        morphTo(sequence[stepIdx]);
      };
      timerId = setInterval(advance, intervalMs);
      const stopSequence = () => {
        if (timerId !== null) {
          clearInterval(timerId);
          timerId = null;
        }
        if (activeSequenceCleanup === stopSequence) {
          activeSequenceCleanup = null;
        }
      };
      activeSequenceCleanup = stopSequence;
      return stopSequence;
    },
    destroy() {
      activeSequenceCleanup?.();
      for (const unbind of Array.from(bindCleanups)) {
        unbind();
      }
      bindCleanups.clear();
      animator.stop();
    },
  };
}
